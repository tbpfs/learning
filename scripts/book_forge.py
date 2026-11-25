#!/usr/bin/env python3
"""
scripts/book_forge.py - Local LLM (LM Studio) x Antigravity editorial workflow CLI
for Purple Maple Press (`tbpfs/learning`).

Features (zero external dependencies, Python 3.12 stdlib):
- `status`: display Trilingual Atomic Publication status across all books/chapters.
- `check-lm`: verify local LM Studio OpenAI-compatible server & loaded models.
- `draft`: generate a `zh-TW` draft chapter JSON using local LM Studio grounded in
  outlines.json, glossary.json, and the chapter's live-executed Python 3.12 script.
- `translate`: 2-pass local LLM translation (zh-TW -> zh-CN / en) with Glossary Lock,
  reasoning_effort="none", <think> + fence stripping, SHA-256 checkpoint cache, and
  mechanical QA retry loop (max 3 attempts).
- `audit`: run mechanical QA gates across chapters (prose length, SVG XSS/DOM check,
  quiz integrity, zero CJK in en, zero Taiwan/Traditional leaks in zh-CN).

Safety invariants:
- Never overwrites an existing chapter with `status == "published"` unless `--force`.
- Atomic file writes via temp file + `os.replace`.
- Strict `http://` / `https://` scheme allowlist & explicit timeout on all HTTP calls.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any, Callable

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from book_models import (  # noqa: E402
    SUPPORTED_BOOK_LOCALES,
    audit_chapter_quality,
    count_prose_from_chapter,
    parse_chapter_json,
)

DEFAULT_LM_BASE_URL = "http://127.0.0.1:1234/v1"
DEFAULT_TIMEOUT_SEC = 180
MAX_QA_RETRIES = 3

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def validate_endpoint_url(url: str) -> str:
    """Enforce http/https scheme allowlist to prevent file:// or arbitrary URI requests."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError(f"Unsafe or malformed LM endpoint URL: {url!r}")
    return url.rstrip("/")


def strip_model_artifacts(raw_text: str) -> str:
    """Strip <think>...</think> blocks and markdown code fences from local LLM output."""
    cleaned = _THINK_RE.sub("", raw_text).strip()
    cleaned = _FENCE_RE.sub("", cleaned).strip()
    return cleaned


def atomic_write_json(target: Path, payload: dict[str, Any], *, force: bool = False) -> None:
    """Atomically write JSON via temp file + os.replace; refuse overwriting published chapters without --force."""
    if target.is_file() and not force:
        try:
            existing = json.loads(target.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
        if existing.get("status") == "published":
            raise PermissionError(
                f"Refusing to overwrite published chapter {target}. Pass --force to override."
            )
    target.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=".forge_", suffix=".tmp", dir=str(target.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(serialized)
        os.replace(tmp_path, target)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
        raise


def default_http_json(
    url: str,
    *,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    timeout: int = DEFAULT_TIMEOUT_SEC,
) -> dict[str, Any]:
    """Perform a zero-dependency stdlib JSON HTTP request with strict scheme check."""
    validate_endpoint_url(url)
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec B310
        body = resp.read().decode("utf-8")
    return json.loads(body)


def detect_lm_models(
    base_url: str = DEFAULT_LM_BASE_URL,
    http_fn: Callable[..., dict[str, Any]] = default_http_json,
) -> list[str]:
    """Query LM Studio /v1/models and return loaded model identifiers."""
    clean_base = validate_endpoint_url(base_url)
    data = http_fn(f"{clean_base}/models", method="GET", payload=None, timeout=10)
    return [str(item["id"]) for item in data.get("data", []) if "id" in item]


def chat_completion_json(
    *,
    base_url: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2,
    timeout: int = DEFAULT_TIMEOUT_SEC,
    http_fn: Callable[..., dict[str, Any]] = default_http_json,
) -> dict[str, Any]:
    """Call LM Studio /v1/chat/completions with reasoning_effort='none' and parse JSON response."""
    clean_base = validate_endpoint_url(base_url)
    body = {
        "model": model,
        "temperature": temperature,
        "reasoning_effort": "none",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    resp = http_fn(f"{clean_base}/chat/completions", method="POST", payload=body, timeout=timeout)
    content = resp["choices"][0]["message"]["content"]
    cleaned = strip_model_artifacts(content)
    return json.loads(cleaned)


def run_example_script(repo_root: Path, rel_path: str) -> tuple[str, str]:
    """Read and execute the chapter's Python 3.12 example to ground the local LLM prompt."""
    script_path = repo_root / rel_path
    source = script_path.read_text(encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        timeout=15,
        check=True,
    )
    return source, proc.stdout.strip()


def compute_cache_hash(payload: dict[str, Any], target_locale: str, model: str) -> str:
    raw = json.dumps({"payload": payload, "locale": target_locale, "model": model}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def build_draft_prompts(
    book_meta: dict[str, Any],
    outline: dict[str, Any],
    glossary: dict[str, Any],
    source_code: str,
    live_output: str,
) -> tuple[str, str]:
    """Construct O'Reilly-grade Traditional Chinese textbook drafting prompts for local LLM."""
    glossary_lines = "\n".join(
        f"- {t['zh-TW']} ({t['en']})" for t in glossary.get("terms", [])
    )
    system_prompt = (
        "你是紫楓出版社（Purple Maple Press）的資深 AI 系統架構師兼技術專書主編。\n"
        "請用道地的「台灣繁體中文（zh-TW）」撰寫歐萊禮（O'Reilly）等級的深度技術專書章節。\n"
        "嚴格規則：\n"
        "1. 僅回傳合法 JSON，禁止任何 Markdown 圍欄或解說文字。\n"
        "2. 正文總字數必須 >= 2,600 個中文字（sections 至少 4 節、每節 2~3 段紮實工程解析）。\n"
        "3. 必須提供 1 張簡潔原生 SVG 架構圖（viewBox=\"0 0 760 260\" role=\"img\" aria-label=\"...\"，元素數 < 60，嚴禁 <script>/<foreignObject>/事件屬性）。\n"
        "4. 至少 3 個真實生產環境踩坑（pitfalls）、3 題含詳解的互動測驗（quiz）、3 題資深面試問答（interview_faqs）。\n"
        "5. 狀態固定設為 \"draft\"，等待 Antigravity 主編驗收後才會升格為 \"published\"。\n"
        "6. 語氣專業、清晰、有實戰洞見，禁止空洞 AI 腔（例如「在當今快速發展的時代」）。"
    )
    user_prompt = (
        f"書籍：{book_meta['title']['zh-TW']} ({book_meta['id']})\n"
        f"章節：{outline['badge']} {outline['title']['zh-TW']} (id={outline['id']}, part={outline['part']})\n"
        f"摘要：{outline['summary']['zh-TW']}\n"
        f"學習目標：{json.dumps(outline['learning_objectives'], ensure_ascii=False)}\n"
        f"核心關鍵詞：{json.dumps(outline['key_topics'], ensure_ascii=False)}\n"
        f"鎖定術語表：\n{glossary_lines}\n\n"
        f"本章真實可執行 Python 3.12 範例（{outline['example_file']}）：\n"
        f"{source_code}\n\n"
        f"實機執行輸出：\n{live_output}\n\n"
        "請依以下 JSON Schema 輸出完整章節（today="
        f"{date.today().isoformat()}）：\n"
        "{\n"
        '  "book_id": "...", "chapter_id": "...", "locale": "zh-TW", "status": "draft",\n'
        '  "badge": "...", "part_id": "...", "title": "...", "short_title": "...",\n'
        '  "summary": "...", "aeo_capsule": "...", "reading_minutes": 18, "lastmod": "YYYY-MM-DD",\n'
        '  "example_file": "...", "keywords": ["..."], "learning_objectives": ["..."],\n'
        '  "sections": [{"id": "sec1", "heading": "...", "paragraphs": ["..."], "bullets": ["..."], "callout_title": "...", "callout_body": "..."}],\n'
        '  "diagram_caption": "...", "diagram_svg": "<svg viewBox=\\"0 0 760 260\\" role=\\"img\\" aria-label=\\"...\\">...</svg>",\n'
        '  "comparison_table": {"caption": "...", "headers": ["..."], "rows": [["..."]]},\n'
        '  "code_walkthrough": ["..."],\n'
        '  "pitfalls": [{"title": "...", "symptom": "...", "root_cause_and_fix": "..."}],\n'
        '  "quiz": [{"question": "...", "options": ["A", "B", "C", "D"], "answer_index": 0, "explanation": "..."}],\n'
        '  "interview_faqs": [{"question": "...", "answer": "..."}],\n'
        '  "further_reading": [{"title": "...", "url": "https://...", "note": "..."}]\n'
        "}"
    )
    return system_prompt, user_prompt


def build_translate_prompts(
    source_ch: dict[str, Any],
    target_locale: str,
    glossary: dict[str, Any],
    pass_name: str,
    prior_issues: list[str] | None = None,
) -> tuple[str, str]:
    """Construct Pass-1 literal or Pass-2 polish translation prompts with Glossary Lock."""
    glossary_lines = "\n".join(
        f"- {t['zh-TW']} -> {t[target_locale]}" for t in glossary.get("terms", [])
    )
    if target_locale == "zh-CN":
        lang_rules = (
            "目標語言：中國大陸簡體中文（zh-Hans）。\n"
            "嚴禁任何繁體字與台灣慣用語（如：詞元、推論、檢索、微調、幻覺、權重、視窗、切塊、程式碼、講義、紫楓、社團）。\n"
            "必須翻譯 diagram_svg 內所有中文標籤，並補齊 code_replacements 與 output_replacements 以將中文註解與 print 標籤轉為簡體中文。"
        )
    else:
        lang_rules = (
            "Target language: Natural technical International English (en).\n"
            "ZERO Chinese/CJK characters permitted anywhere in the output JSON (including diagram_svg labels, quiz, FAQs, and further_reading).\n"
            "Provide exact code_replacements and output_replacements pairs so the displayed Python docstrings/comments/stdout contain zero CJK characters."
        )
    issue_block = ""
    if prior_issues:
        issue_block = "\n上次機械質檢失敗原因（本次必須全部修復）：\n- " + "\n- ".join(prior_issues)

    system_prompt = (
        f"你是紫楓出版社資深技術書籍譯者（目前階段：{pass_name}）。\n"
        f"{lang_rules}\n"
        "僅回傳合法 JSON，保留所有 key 結構、book_id、chapter_id、example_file、status=\"draft\"，且將 locale 設為 "
        f"\"{target_locale}\"。"
    )
    user_prompt = (
        f"強制鎖定術語表：\n{glossary_lines}\n{issue_block}\n\n"
        f"來源 JSON：\n{json.dumps(source_ch, ensure_ascii=False)}"
    )
    return system_prompt, user_prompt


def forge_draft(
    *,
    repo_root: Path,
    book_id: str,
    chapter_id: str,
    base_url: str,
    model: str | None,
    force: bool = False,
    http_fn: Callable[..., dict[str, Any]] = default_http_json,
) -> Path:
    """Draft a zh-TW chapter JSON via local LM Studio with up to MAX_QA_RETRIES mechanical QA loops."""
    book_dir = repo_root / "books" / book_id
    book_meta = json.loads((book_dir / "book.json").read_text(encoding="utf-8"))
    outlines = json.loads((book_dir / "outlines.json").read_text(encoding="utf-8"))
    glossary = json.loads((book_dir / "glossary.json").read_text(encoding="utf-8"))
    outline = next((c for c in outlines["chapters"] if c["id"] == chapter_id), None)
    if outline is None:
        raise KeyError(f"Unknown chapter {chapter_id!r} in book {book_id!r}")

    chosen_model = model or detect_lm_models(base_url, http_fn=http_fn)[0]
    src_code, live_out = run_example_script(repo_root, outline["example_file"])
    sys_p, usr_p = build_draft_prompts(book_meta, outline, glossary, src_code, live_out)

    last_issues: list[str] = []
    candidate: dict[str, Any] | None = None
    for attempt in range(1, MAX_QA_RETRIES + 1):
        prompt_with_fb = usr_p
        if last_issues:
            prompt_with_fb += "\n\n上次草稿質檢未通過，請補足以下缺項：\n- " + "\n- ".join(last_issues)
        raw = chat_completion_json(
            base_url=base_url,
            model=chosen_model,
            system_prompt=sys_p,
            user_prompt=prompt_with_fb,
            http_fn=http_fn,
        )
        raw["book_id"] = book_id
        raw["chapter_id"] = chapter_id
        raw["locale"] = "zh-TW"
        raw["status"] = "draft"
        raw["example_file"] = outline["example_file"]
        parsed = parse_chapter_json(raw)
        issues = audit_chapter_quality(parsed)
        candidate = raw
        if not issues:
            break
        last_issues = issues
        print(f"[WARN] Draft attempt {attempt}/{MAX_QA_RETRIES} QA issues: {issues}", file=sys.stderr)

    assert candidate is not None
    target = book_dir / "chapters" / "zh-TW" / f"{chapter_id}.json"
    atomic_write_json(target, candidate, force=force)
    return target


def forge_translate(
    *,
    repo_root: Path,
    book_id: str,
    chapter_id: str,
    target_locale: str,
    base_url: str,
    model: str | None,
    force: bool = False,
    http_fn: Callable[..., dict[str, Any]] = default_http_json,
) -> Path:
    """2-pass translate a zh-TW chapter into zh-CN or en with SHA-256 checkpoint & QA retries."""
    if target_locale not in ("zh-CN", "en"):
        raise ValueError(f"Unsupported translation target locale: {target_locale!r}")

    book_dir = repo_root / "books" / book_id
    src_path = book_dir / "chapters" / "zh-TW" / f"{chapter_id}.json"
    if not src_path.is_file():
        raise FileNotFoundError(f"Source zh-TW chapter missing: {src_path}")
    src_data = json.loads(src_path.read_text(encoding="utf-8"))
    glossary = json.loads((book_dir / "glossary.json").read_text(encoding="utf-8"))

    chosen_model = model or detect_lm_models(base_url, http_fn=http_fn)[0]
    cache_dir = book_dir / ".forge_cache"
    cache_key = compute_cache_hash(src_data, target_locale, chosen_model)
    pass1_cache = cache_dir / f"{chapter_id}_{target_locale}_{cache_key}_pass1.json"

    if pass1_cache.is_file():
        pass1_data = json.loads(pass1_cache.read_text(encoding="utf-8"))
    else:
        p1_sys, p1_usr = build_translate_prompts(src_data, target_locale, glossary, "Pass 1 精準直譯")
        pass1_data = chat_completion_json(
            base_url=base_url,
            model=chosen_model,
            system_prompt=p1_sys,
            user_prompt=p1_usr,
            http_fn=http_fn,
        )
        atomic_write_json(pass1_cache, pass1_data, force=True)

    last_issues: list[str] = []
    final_data: dict[str, Any] = pass1_data
    for attempt in range(1, MAX_QA_RETRIES + 1):
        p2_sys, p2_usr = build_translate_prompts(
            final_data,
            target_locale,
            glossary,
            "Pass 2 在地化潤飾與術語校驗",
            prior_issues=last_issues or None,
        )
        polished = chat_completion_json(
            base_url=base_url,
            model=chosen_model,
            system_prompt=p2_sys,
            user_prompt=p2_usr,
            http_fn=http_fn,
        )
        polished["book_id"] = book_id
        polished["chapter_id"] = chapter_id
        polished["locale"] = target_locale
        polished["status"] = "draft"
        polished["example_file"] = src_data["example_file"]
        parsed = parse_chapter_json(polished)
        issues = audit_chapter_quality(parsed)
        final_data = polished
        if not issues:
            break
        last_issues = issues
        print(
            f"[WARN] Translate ({target_locale}) attempt {attempt}/{MAX_QA_RETRIES} QA issues: {issues}",
            file=sys.stderr,
        )

    target = book_dir / "chapters" / target_locale / f"{chapter_id}.json"
    atomic_write_json(target, final_data, force=force)
    return target


def cmd_status(repo_root: Path, book_id: str | None) -> int:
    books_dir = repo_root / "books"
    if not books_dir.is_dir():
        print("[INFO] No books/ directory found.")
        return 0
    targets = [books_dir / book_id] if book_id else sorted(p for p in books_dir.iterdir() if p.is_dir())
    for bdir in targets:
        outlines_path = bdir / "outlines.json"
        if not outlines_path.is_file():
            continue
        outlines = json.loads(outlines_path.read_text(encoding="utf-8"))
        print(f"\n=== Book: {bdir.name} ===")
        print(f"{'Chapter':<8} {'zh-TW':<12} {'zh-CN':<12} {'en':<12} {'Atomic Gate'}")
        print("-" * 62)
        for ch in outlines["chapters"]:
            cid = ch["id"]
            st_map: dict[str, str] = {}
            for loc in SUPPORTED_BOOK_LOCALES:
                p = bdir / "chapters" / loc / f"{cid}.json"
                if not p.is_file():
                    st_map[loc] = "missing"
                else:
                    st_map[loc] = str(json.loads(p.read_text(encoding="utf-8")).get("status", "unknown"))
            gate = "PUBLISHED" if all(v == "published" for v in st_map.values()) else "HOLD"
            print(f"{cid:<8} {st_map['zh-TW']:<12} {st_map['zh-CN']:<12} {st_map['en']:<12} {gate}")
    return 0


def cmd_audit(repo_root: Path, book_id: str) -> int:
    book_dir = repo_root / "books" / book_id
    outlines = json.loads((book_dir / "outlines.json").read_text(encoding="utf-8"))
    failures = 0
    checked = 0
    for ch in outlines["chapters"]:
        cid = ch["id"]
        for loc in SUPPORTED_BOOK_LOCALES:
            p = book_dir / "chapters" / loc / f"{cid}.json"
            if not p.is_file():
                continue
            checked += 1
            parsed = parse_chapter_json(json.loads(p.read_text(encoding="utf-8")))
            issues = audit_chapter_quality(parsed)
            prose = count_prose_from_chapter(parsed, loc)
            if issues:
                failures += 1
                print(f"[FAIL] {book_id}/{loc}/{cid} (status={parsed.status}, prose={prose}): {issues}")
            else:
                print(f"[PASS] {book_id}/{loc}/{cid} (status={parsed.status}, prose={prose})")
    print(f"\nAudit complete: {checked - failures}/{checked} chapters passed.")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Purple Maple Press Local LLM Book Forge CLI")
    parser.add_argument("--base-url", default=DEFAULT_LM_BASE_URL, help="LM Studio OpenAI-compatible base URL")
    parser.add_argument("--model", default=None, help="Explicit model ID (auto-detects first loaded model if omitted)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_st = sub.add_parser("status", help="Show trilingual chapter publication status")
    p_st.add_argument("--book", default=None, help="Optional book ID filter")

    sub.add_parser("check-lm", help="Check local LM Studio connection & loaded models")

    p_dr = sub.add_parser("draft", help="Draft a zh-TW chapter via local LM Studio")
    p_dr.add_argument("--book", required=True)
    p_dr.add_argument("--chapter", required=True)
    p_dr.add_argument("--force", action="store_true", help="Allow overwriting a published chapter")

    p_tr = sub.add_parser("translate", help="2-pass translate a zh-TW chapter into zh-CN or en")
    p_tr.add_argument("--book", required=True)
    p_tr.add_argument("--chapter", required=True)
    p_tr.add_argument("--to", required=True, choices=["zh-CN", "en"])
    p_tr.add_argument("--force", action="store_true", help="Allow overwriting a published chapter")

    p_au = sub.add_parser("audit", help="Run mechanical QA audit on existing chapter JSON files")
    p_au.add_argument("--book", required=True)

    args = parser.parse_args(argv)
    if args.command == "status":
        return cmd_status(REPO_ROOT, args.book)
    if args.command == "check-lm":
        try:
            models = detect_lm_models(args.base_url)
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            print(f"[OFFLINE] Could not reach LM Studio at {args.base_url}: {exc}", file=sys.stderr)
            return 2
        print(f"[OK] LM Studio online at {args.base_url}. Loaded models: {models}")
        return 0
    if args.command == "draft":
        out_path = forge_draft(
            repo_root=REPO_ROOT,
            book_id=args.book,
            chapter_id=args.chapter,
            base_url=args.base_url,
            model=args.model,
            force=args.force,
        )
        print(f"[OK] Wrote draft chapter to: {out_path}")
        return 0
    if args.command == "translate":
        out_path = forge_translate(
            repo_root=REPO_ROOT,
            book_id=args.book,
            chapter_id=args.chapter,
            target_locale=args.to,
            base_url=args.base_url,
            model=args.model,
            force=args.force,
        )
        print(f"[OK] Wrote translated draft to: {out_path}")
        return 0
    if args.command == "audit":
        return cmd_audit(REPO_ROOT, args.book)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
