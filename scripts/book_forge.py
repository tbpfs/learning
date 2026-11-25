#!/usr/bin/env python3
"""
scripts/book_forge.py (v2.0) - Automated Local LLM (LM Studio `lms` CLI) x Antigravity
Technical Textbook Production Engine for Purple Maple Press (`tbpfs/learning`).

Adapted from the battle-tested `novel_engine.py v3.0` + `translate_book.py` local-LLM
workflow for O'Reilly-grade technical books:
  - Zero external dependencies (Python 3.12 stdlib only)
  - Automatic `lms` CLI server startup, VRAM-safe model switching & auto-unload on exit
    (use `--no-lms` to skip `lms` subprocess management when running manually or in tests)
  - Proven two-model division of labor (RTX 3080 Ti + 64GB RAM):
      * Draft / Plan / zh-CN: Qwen3.6-35B-A3B (`PRESS_DRAFT_MODEL`)
      * zh-TW Editorial Polish / EN: Gemma4-26B-A4B (`PRESS_POLISH_MODEL`)
  - Golden 4K-6K context window: section-by-section drafting & chunked JSON translation
    with SHA-256 resumable cache under `books/<book_id>/.forge_cache/`
  - Cross-domain O'Reilly style anchor + 12-gram anti-copy detector + technical AI-slop
    regex linter + strict zh-TW / zh-CN / en localization & Python `compile()` QA gates
  - Atomic JSON writes that NEVER overwrite `status == "published"` without `--force`

CLI:
  python scripts/book_forge.py status [--book ai-engineering]
  python scripts/book_forge.py check-lm
  python scripts/book_forge.py plan --book ai-engineering --chapter ch02
  python scripts/book_forge.py draft --book ai-engineering --chapter ch02
  python scripts/book_forge.py translate --book ai-engineering --chapter ch02 --to en|zh-CN
  python scripts/book_forge.py forge --book ai-engineering --chapter ch02 [--from 2 --to 4]
  python scripts/book_forge.py audit --book ai-engineering
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
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
    ZH_CN_BANNED_TERMS,
    ZH_CN_BANNED_TRAD_CHARS,
    audit_chapter_quality,
    count_prose_from_chapter,
    parse_chapter_json,
    validate_svg_safe,
)
from i18n import localize_code_and_output  # noqa: E402

DEFAULT_LM_BASE_URL = os.environ.get("LM_STUDIO_BASE_URL", "http://127.0.0.1:1234/v1")
DEFAULT_DRAFT_MODEL = os.environ.get(
    "PRESS_DRAFT_MODEL",
    "qwen3.6-35b-a3b-uncensored-hauhaucs-aggressive",
)
DEFAULT_POLISH_MODEL = os.environ.get(
    "PRESS_POLISH_MODEL",
    "gemma4-26b-a4b-qat-uncensored-hauhaucs-balanced-mtp",
)
DEFAULT_CONTEXT_LEN = int(os.environ.get("PRESS_LM_CTX", "8192"))
DEFAULT_TIMEOUT_SEC = 240
MAX_QA_RETRIES = 3

LMS_CLI = os.environ.get("LMS_CLI") or shutil.which("lms") or "lms"

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
_FENCE_RE = re.compile(r"^```(?:json|text|markdown)?\s*|\s*```$", re.MULTILINE)
_CJK_RE = re.compile(r"[\u4e00-\u9fff]")

# Cross-domain O'Reilly textbook anchor (Database B-Tree & WAL — completely unrelated to AI/LLM
# so models anchor on concrete engineering prose clarity without copying domain phrases)
CROSS_DOMAIN_TEXTBOOK_ANCHOR = (
    "【目標教科書文筆標竿（跨領域資料庫示範，僅學習其問題導向切入、量化推導與精準動詞，嚴禁照抄任何詞句）】\n"
    "許多後端工程師替資料表加上 B-Tree 索引後，便誤以為查詢效能從此高枕無憂；直到線上訂單表突破五千萬筆、"
    "複合索引的最左前綴遭到不經意的函式包裝破壞，資料庫 CPU 在尖峰時段瞬間飆上 98%，才驚覺索引根本沒有命中。"
    "寫入預寫日誌（Write-Ahead Log, WAL）的設計邏輯同樣建立在硬體物理限制上：與其每次更新隨機跳轉磁碟磁區，"
    "不如先以循序追加（Sequential Append）寫入日誌並刷盤，再由背景程序批次整理髒頁，這道取捨讓吞吐量整整拉開一個數量級。"
)

# Technical AI-slop regex blacklist (zh-TW editorial gate)
TECH_BANNED_SLOP_REGEX: tuple[tuple[str, str], ...] = (
    (r"在當今(快速|高速|蓬勃)發展的時代", "禁用空洞開頭『在當今快速發展的時代』，請直接切入真實工程問題"),
    (r"隨著(AI|人工智慧|大模型|科技)的(快速|飛速|蓬勃)發展", "禁用空洞背景句，請改用具體系統故障或量化指標破題"),
    (r"(總而言之|綜上所述)", "禁用論文罐頭總結詞『總而言之／綜上所述』"),
    (r"(不言而喻|顯而易見|毫無疑問)", "禁用空泛斷言詞，請改給出明確數學或系統依據"),
    (r"是一把雙面刃", "禁用老套比喻『雙面刃』，請直接列出具體取捨與量化代價"),
    (r"不可或缺的重要角色", "禁用空洞修飾『不可或缺的重要角色』"),
)

# Strictly Simplified-only characters that must NOT leak into zh-TW prose
STRICT_SIMPLIFIED_FOR_TW: set[str] = set(
    "这说们为会时对进现关开经应样当听让给发现线图视讯装坏断声响总挥显红蓝绿"
    "药着丝络实复资构间点输验隐权馈帮选错还观长审补录单书课较护踪层题难问码导场义广页"
    "词论检调觉团发键闸余语块体计画备驱动规范编译写读号评测确认节类标准响应优历缓冲档卫锁链转换产业务连"
)

# Mainland tech terms (regex patterns) that must be localized to Taiwan usage in zh-TW prose
ZH_TW_DISALLOWED_MAINLAND_TERMS: tuple[tuple[str, str], ...] = (
    (r"內存", "請改用台灣用語『記憶體』"),
    (r"代碼", "請改用台灣用語『程式碼』"),
    (r"調用", "請改用台灣用語『呼叫』"),
    (r"視頻", "請改用台灣用語『影片』"),
    (r"默認", "請改用台灣用語『預設』"),
    (r"(?<!演)算法", "請改用台灣用語『演算法』"),
    (r"數組", "請改用台灣用語『陣列』"),
    (r"鏈表", "請改用台灣用語『鏈結串列』"),
    (r"信息", "請改用台灣用語『資訊』"),
    (r"創建", "請改用台灣用語『建立』"),
    (r"響應", "請改用台灣用語『回應』"),
    (r"緩存", "請改用台灣用語『快取』"),
)


def validate_endpoint_url(url: str) -> str:
    """Enforce http/https scheme allowlist to prevent file:// or arbitrary URI requests."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError(f"Unsafe or malformed LM endpoint URL: {url!r}")
    return url.rstrip("/")


def strip_model_artifacts(raw_text: str) -> str:
    """Strip <think>...</think> blocks and markdown code fences from local LLM output."""
    cleaned = _THINK_RE.sub("", raw_text or "").strip()
    cleaned = _FENCE_RE.sub("", cleaned).strip()
    return cleaned


def extract_json_object(raw_text: str) -> dict[str, Any]:
    """Extract and parse the outermost JSON object from a local LLM response."""
    cleaned = strip_model_artifacts(raw_text)
    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in model output: {cleaned[:260]!r}")
    parsed = json.loads(match.group(0))
    if not isinstance(parsed, dict):
        raise ValueError("Expected top-level JSON object")
    return parsed


def find_fewshot_overlap(text: str, anchor: str = CROSS_DOMAIN_TEXTBOOK_ANCHOR, min_len: int = 12) -> str | None:
    """Detect verbatim >= min_len char overlap against the cross-domain style anchor."""
    clean_anchor = re.sub(r"【[^】]+】|\s+", "", anchor)
    clean_text = re.sub(r"\s+", "", text)
    if len(clean_anchor) < min_len or len(clean_text) < min_len:
        return None
    for i in range(0, len(clean_anchor) - min_len + 1, 2):
        sub = clean_anchor[i : i + min_len]
        if sub in clean_text:
            return sub
    return None


def run_textbook_section_linter(section: dict[str, Any], *, locale: str = "zh-TW") -> list[str]:
    """Deterministic section-level linter adapted from novel_engine.py for technical books."""
    issues: list[str] = []
    heading = str(section.get("heading") or "").strip()
    paragraphs = [str(p).strip() for p in (section.get("paragraphs") or []) if str(p).strip()]
    bullets = [str(b).strip() for b in (section.get("bullets") or []) if str(b).strip()]
    callout_title = str(section.get("callout_title") or "").strip()
    callout_body = str(section.get("callout_body") or "").strip()

    if not heading:
        issues.append("缺少小節標題 heading")
    if len(paragraphs) < 2:
        issues.append(f"段落數不足（僅 {len(paragraphs)} 段，每節須至少 2～3 段紮實論述）")

    joined = "\n".join([heading, *paragraphs, *bullets, callout_title, callout_body])

    if locale == "zh-TW":
        cjk_count = len(_CJK_RE.findall(joined))
        if cjk_count < 480:
            issues.append(f"本節中文字數不足（{cjk_count} < 480 字），請補充底層機制、數學直覺或實務範例")
        if paragraphs:
            avg_para = sum(len(p) for p in paragraphs) / len(paragraphs)
            if avg_para < 70:
                issues.append(f"段落過於碎裂（平均段長 {avg_para:.1f} < 70 字），請寫成連貫流暢的教科書段落")
        dup = find_fewshot_overlap(joined)
        if dup:
            issues.append(f"照抄跨領域風格範例片段『{dup}』，請改為本章原創內容")
        for pat, msg in TECH_BANNED_SLOP_REGEX:
            m = re.search(pat, joined)
            if m:
                issues.append(f"檢出 AI 罐頭詞『{m.group(0)}』：{msg}")
        bad_simp = sorted({ch for ch in joined if ch in STRICT_SIMPLIFIED_FOR_TW})
        if bad_simp:
            issues.append(f"檢出簡體字滲透：{''.join(bad_simp[:12])}")
        for pat, fix_hint in ZH_TW_DISALLOWED_MAINLAND_TERMS:
            m = re.search(pat, joined)
            if m:
                issues.append(f"檢出非台灣技術用語『{m.group(0)}』：{fix_hint}")
    elif locale == "zh-CN":
        cjk_count = len(_CJK_RE.findall(joined))
        if cjk_count < 450:
            issues.append(f"本节中文字数不足（{cjk_count} < 450 字）")
        for bad_term in ZH_CN_BANNED_TERMS:
            if bad_term in joined:
                issues.append(f"简体版残留台湾用语：{bad_term!r}")
        bad_trad = sorted({ch for ch in joined if ch in ZH_CN_BANNED_TRAD_CHARS})
        if bad_trad:
            issues.append(f"简体版残留繁体字：{''.join(bad_trad[:12])}")
    elif locale == "en":
        cjk_leaks = _CJK_RE.findall(joined)
        if cjk_leaks:
            issues.append(f"English section leaked CJK chars: {cjk_leaks[:8]}")
        words = re.findall(r"[A-Za-z][A-Za-z0-9'-]*", joined)
        if len(words) < 220:
            issues.append(f"English section too short ({len(words)} < 220 words)")

    return issues


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


class LmsController:
    """Manages local LM Studio `lms` CLI headless server startup and VRAM-safe model swaps."""

    def __init__(
        self,
        *,
        enabled: bool = True,
        lms_bin: str = LMS_CLI,
        context_len: int = DEFAULT_CONTEXT_LEN,
        runner: Callable[..., Any] = subprocess.run,
    ) -> None:
        self.enabled = enabled
        self.lms_bin = lms_bin
        self.context_len = context_len
        self.runner = runner
        self.active_model: str | None = None
        self.server_started = False

    def ensure_server(self) -> None:
        if not self.enabled or self.server_started:
            return
        print(f">>> [LMS] 啟動本機 LM Studio API Server ({self.lms_bin}) ...", flush=True)
        self.runner(
            [self.lms_bin, "server", "start", "--cors"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        self.server_started = True
        time.sleep(1.5)

    def switch_model(self, model_key: str, *, force: bool = False) -> None:
        if not self.enabled:
            self.active_model = model_key
            return
        if not force and self.active_model == model_key:
            return
        self.ensure_server()
        print(f">>> [LMS] 切換地端模型 -> {model_key} (ctx={self.context_len}) ...", flush=True)
        self.runner(
            [self.lms_bin, "unload", "--all"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        self.runner(
            [self.lms_bin, "load", model_key, "-c", str(self.context_len), "--ttl", "86400", "-y"],
            check=True,
        )
        self.active_model = model_key
        time.sleep(2.0)

    def unload_all(self) -> None:
        if not self.enabled:
            return
        print(">>> [LMS] 任務完成，釋放本地 GPU 顯存 (lms unload --all) ...", flush=True)
        self.runner(
            [self.lms_bin, "unload", "--all"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        self.active_model = None


def detect_lm_models(
    base_url: str = DEFAULT_LM_BASE_URL,
    http_fn: Callable[..., dict[str, Any]] = default_http_json,
) -> list[str]:
    """Query LM Studio /v1/models and return loaded model identifiers."""
    clean_base = validate_endpoint_url(base_url)
    data = http_fn(f"{clean_base}/models", method="GET", payload=None, timeout=10)
    return [str(item["id"]) for item in data.get("data", []) if "id" in item]


def call_lm_text(
    *,
    base_url: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.35,
    max_tokens: int = 2400,
    reasoning_effort: str = "none",
    use_dry: bool = True,
    timeout: int = DEFAULT_TIMEOUT_SEC,
    http_fn: Callable[..., dict[str, Any]] = default_http_json,
    lms: LmsController | None = None,
) -> str:
    """Call LM Studio chat completions with DRY 400 fallback, unloaded recovery, and tok/s telemetry."""
    clean_base = validate_endpoint_url(base_url)
    body: dict[str, Any] = {
        "model": model,
        "temperature": temperature,
        "min_p": 0.05,
        "top_p": 0.95,
        "max_tokens": max_tokens,
        "reasoning_effort": reasoning_effort,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    if use_dry:
        body["dry_multiplier"] = 0.8

    last_err: Exception | None = None
    for attempt in range(1, 5):
        t0 = time.time()
        try:
            resp = http_fn(f"{clean_base}/chat/completions", method="POST", payload=body, timeout=timeout)
            dt = max(time.time() - t0, 0.05)
            toks = int((resp.get("usage") or {}).get("completion_tokens", 0))
            raw_content = str(resp["choices"][0]["message"].get("content") or "")
            cleaned = strip_model_artifacts(raw_content)
            print(
                f"    -> [{model[:18]}] {toks} toks / {dt:.1f}s ({toks / dt:.1f} tok/s), {len(cleaned)} chars",
                flush=True,
            )
            return cleaned
        except Exception as exc:
            err_body = ""
            if hasattr(exc, "read"):
                try:
                    err_body = exc.read().decode("utf-8", errors="ignore")[:300]  # type: ignore[attr-defined]
                except Exception:
                    pass
            if "dry_multiplier" in body and ("400" in str(exc) or "dry_multiplier" in err_body):
                body.pop("dry_multiplier", None)
                print("    [INFO] 端點不支援 dry_multiplier，自動降級重試。", flush=True)
                continue
            if "unloaded" in err_body.lower() and lms is not None and lms.enabled:
                lms.switch_model(model, force=True)
                continue
            last_err = exc
            print(f"    [WARN call_lm retry {attempt}/4] {exc} {err_body}", flush=True)
            time.sleep(min(2 * attempt, 6))
    assert last_err is not None
    raise last_err


def call_lm_json(
    *,
    base_url: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.25,
    max_tokens: int = 2400,
    reasoning_effort: str = "none",
    use_dry: bool = False,
    timeout: int = DEFAULT_TIMEOUT_SEC,
    http_fn: Callable[..., dict[str, Any]] = default_http_json,
    lms: LmsController | None = None,
) -> dict[str, Any]:
    """Call LM Studio and parse a JSON object with automatic parse-error repair retry."""
    last_err: Exception | None = None
    prompt = user_prompt
    for attempt in range(1, 4):
        raw = call_lm_text(
            base_url=base_url,
            model=model,
            system_prompt=system_prompt,
            user_prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            reasoning_effort=reasoning_effort,
            use_dry=use_dry,
            timeout=timeout,
            http_fn=http_fn,
            lms=lms,
        )
        try:
            return extract_json_object(raw)
        except Exception as exc:
            last_err = exc
            print(f"    [WARN JSON parse retry {attempt}/3] {exc}", flush=True)
            prompt = (
                user_prompt
                + f"\n\n【格式修正警告】你上次的輸出不是合法 JSON（錯誤：{exc}）。"
                "請嚴格只回傳單一合法 JSON 物件，不要加 ```json 圍欄或任何解釋文字！"
            )
    assert last_err is not None
    raise last_err


def run_example_script(repo_root: Path, rel_path: str) -> tuple[str, str]:
    """Read and execute the chapter's Python 3.12 example to ground all local LLM prompts."""
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


def extract_cjk_literals_from_code(source_code: str, live_output: str) -> tuple[list[str], list[str]]:
    """Extract exact Chinese string literals/comments from Python code & stdout for deterministic replacement."""
    code_targets: list[str] = []
    seen: set[str] = set()
    for line in source_code.splitlines():
        if not _CJK_RE.search(line):
            continue
        # Extract quoted strings containing CJK, or full # comments containing CJK
        stripped = line.strip()
        if stripped.startswith("#"):
            if stripped not in seen:
                seen.add(stripped)
                code_targets.append(stripped)
            continue
        for m in re.finditer(r'"""(.*?)"""|\'\'\'(.*?)\'\'\'|"([^"\\]*(?:\\.[^"\\]*)*)"|\'([^\'\\]*(?:\\.[^\'\\]*)*)\'', line):
            val = next((g for g in m.groups() if g is not None), "")
            if _CJK_RE.search(val):
                # Strip f-string brace interpolation into pure CJK text spans
                for piece in re.split(r"\{[^}]*\}", val):
                    if _CJK_RE.search(piece) and piece not in seen:
                        seen.add(piece)
                        code_targets.append(piece)
    # Also capture standalone Chinese lines inside multi-line docstrings
    for line in source_code.splitlines():
        st = line.strip()
        if st and _CJK_RE.search(st) and not st.startswith("#") and '"' not in st and "'" not in st:
            if st not in seen:
                seen.add(st)
                code_targets.append(st)

    out_targets: list[str] = []
    seen_out: set[str] = set()
    for seg in re.split(r"\|", live_output):
        for m in re.finditer(r"[^\s|:=]*[\u4e00-\u9fff][^|:=]*[:：]?", seg):
            piece = m.group(0).strip()
            if piece and piece not in seen_out:
                seen_out.add(piece)
                out_targets.append(piece)
    return code_targets, out_targets


def compute_cache_hash(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def load_cached_json(cache_path: Path, expected_hash: str) -> dict[str, Any] | None:
    if not cache_path.is_file():
        return None
    try:
        obj = json.loads(cache_path.read_text(encoding="utf-8"))
        if obj.get("_cache_hash") == expected_hash and isinstance(obj.get("data"), dict):
            return obj["data"]
    except Exception:
        return None
    return None


def save_cached_json(cache_path: Path, cache_hash: str, data: dict[str, Any]) -> None:
    atomic_write_json(cache_path, {"_cache_hash": cache_hash, "data": data}, force=True)


def extract_active_glossary(glossary: dict[str, Any], text_blob: str, target_locale: str = "zh-TW") -> str:
    """Filter glossary to terms relevant to the current chunk (keeps prompt inside 4K-6K golden window)."""
    terms = glossary.get("terms") or []
    matched = [
        t for t in terms
        if any(k and k.lower() in text_blob.lower() for k in (t.get("zh-TW", ""), t.get("en", "")))
    ]
    selected = matched if matched else terms[:15]
    if target_locale == "zh-TW":
        return "\n".join(f"- {t['zh-TW']} ({t['en']})" for t in selected)
    return "\n".join(f"- {t['zh-TW']} -> {t[target_locale]} ({t['en']})" for t in selected)


def _load_book_context(repo_root: Path, book_id: str, chapter_id: str) -> tuple[Path, dict[str, Any], dict[str, Any], dict[str, Any]]:
    book_dir = repo_root / "books" / book_id
    book_meta = json.loads((book_dir / "book.json").read_text(encoding="utf-8"))
    outlines = json.loads((book_dir / "outlines.json").read_text(encoding="utf-8"))
    glossary = json.loads((book_dir / "glossary.json").read_text(encoding="utf-8"))
    outline = next((c for c in outlines["chapters"] if c["id"] == chapter_id), None)
    if outline is None:
        raise KeyError(f"Unknown chapter {chapter_id!r} in book {book_id!r}")
    return book_dir, book_meta, outline, glossary


def forge_plan(
    *,
    repo_root: Path,
    book_id: str,
    chapter_id: str,
    base_url: str,
    draft_model: str,
    http_fn: Callable[..., dict[str, Any]] = default_http_json,
    lms: LmsController | None = None,
    force_cache: bool = False,
) -> dict[str, Any]:
    """Stage 0: Generate structured 4-section textbook blueprint grounded in real Python 3.12 code."""
    book_dir, book_meta, outline, glossary = _load_book_context(repo_root, book_id, chapter_id)
    src_code, live_out = run_example_script(repo_root, outline["example_file"])
    cache_path = book_dir / ".forge_cache" / f"{chapter_id}_stage0_plan.json"
    ch_hash = compute_cache_hash({"outline": outline, "src": src_code, "out": live_out, "model": draft_model})
    if not force_cache:
        cached = load_cached_json(cache_path, ch_hash)
        if cached is not None:
            print(f"  [CACHE HIT] Stage 0 藍圖：{cache_path.name}", flush=True)
            return cached

    if lms is not None:
        lms.switch_model(draft_model)

    print(f">>> [Stage 0/3] 以 {draft_model} 規劃 {chapter_id} 教學結構藍圖 ...", flush=True)
    sys_p = (
        "你是紫楓出版社（Purple Maple Press）技術專書總架構師，負責為歐萊禮（O'Reilly）等級專書規劃單章教學藍圖。\n"
        "請用繁體中文只回傳單一合法 JSON 物件，嚴禁加任何圍欄或解釋。"
    )
    usr_p = (
        f"書籍：{book_meta['title']['zh-TW']}\n"
        f"章節：{outline['badge']} {outline['title']['zh-TW']}\n"
        f"摘要：{outline['summary']['zh-TW']}\n"
        f"學習目標：{json.dumps(outline['learning_objectives'], ensure_ascii=False)}\n"
        f"關鍵詞：{json.dumps(outline['key_topics'], ensure_ascii=False)}\n"
        f"本章真實 Python 3.12 範例（{outline['example_file']}）：\n{src_code}\n\n"
        f"實機執行輸出：\n{live_out}\n\n"
        "請輸出嚴格符合以下 Schema 的教學藍圖 JSON（共 4 個小節，每節目標約 800 字）：\n"
        "{\n"
        '  "sections": [\n'
        '    {"id": "sec1-...", "heading": "X.1 ...", "goal": "本節要教會什麼", "key_points": ["要點1", "要點2", "要點3"], "callout_idea": "工程筆記切角"}\n'
        "  ],\n"
        '  "diagram_concept": "五階段或三層架構圖要畫哪些方塊與箭頭",\n'
        '  "table_concept": "比較表要對照哪 4~5 種方案與欄位",\n'
        '  "pitfall_topics": ["真實線上踩坑1", "真實線上踩坑2", "真實線上踩坑3"],\n'
        '  "quiz_topics": ["隨堂測驗考點1", "隨堂測驗考點2", "隨堂測驗考點3"],\n'
        '  "faq_topics": ["面試高頻題1", "面試高頻題2", "面試高頻題3", "面試高頻題4"]\n'
        "}"
    )
    plan = call_lm_json(
        base_url=base_url,
        model=draft_model,
        system_prompt=sys_p,
        user_prompt=usr_p,
        temperature=0.35,
        max_tokens=1800,
        reasoning_effort="medium",
        use_dry=False,
        http_fn=http_fn,
        lms=lms,
    )
    save_cached_json(cache_path, ch_hash, plan)
    return plan


def forge_draft(
    *,
    repo_root: Path,
    book_id: str,
    chapter_id: str,
    base_url: str,
    draft_model: str = DEFAULT_DRAFT_MODEL,
    polish_model: str = DEFAULT_POLISH_MODEL,
    force: bool = False,
    http_fn: Callable[..., dict[str, Any]] = default_http_json,
    lms: LmsController | None = None,
) -> Path:
    """
    Stage 0 -> Stage 1 (Section-by-section Qwen3.6 draft) -> Single Model Swap ->
    Stage 2 (Gemma4 editorial polish + mechanical textbook linter) -> atomic zh-TW draft JSON.
    """
    book_dir, book_meta, outline, glossary = _load_book_context(repo_root, book_id, chapter_id)
    src_code, live_out = run_example_script(repo_root, outline["example_file"])
    cache_dir = book_dir / ".forge_cache"

    # Stage 0: Blueprint
    plan = forge_plan(
        repo_root=repo_root,
        book_id=book_id,
        chapter_id=chapter_id,
        base_url=base_url,
        draft_model=draft_model,
        http_fn=http_fn,
        lms=lms,
    )
    sec_plans = list(plan.get("sections") or [])
    if len(sec_plans) < 3:
        raise ValueError(f"Stage 0 plan returned too few sections: {len(sec_plans)}")

    # Stage 1: Section-by-section drafting with draft_model (Golden 4K-6K context window)
    if lms is not None:
        lms.switch_model(draft_model)
    print(f">>> [Stage 1/3] 以 {draft_model} 逐節撰寫初稿（共 {len(sec_plans)} 節＋結構化模組）...", flush=True)

    sys_draft_sec = (
        "你是紫楓出版社資深 AI 系統架構師，正在撰寫歐萊禮等級技術專書單一小節。\n\n"
        f"{CROSS_DOMAIN_TEXTBOOK_ANCHOR}\n\n"
        "【硬性寫作規範】\n"
        "1. 僅回傳合法 JSON：{\"id\":\"...\",\"heading\":\"...\",\"paragraphs\":[\"...\",\"...\",\"...\"],\"bullets\":[\"...\",\"...\"],\"callout_title\":\"...\",\"callout_body\":\"...\"}\n"
        "2. 本節正文須寫 3 段紮實、流暢的工程解析（全節合計 700～950 中文字），切忌碎裂短句與空泛套話。\n"
        "3. 緊密扣合本章真實 Python 3.12 範例與實機輸出，講清楚『為什麼這樣設計、線上會踩什麼坑』。\n"
        "4. 嚴禁『在當今快速發展的時代』『總而言之』『綜上所述』『雙面刃』等 AI 罐頭詞。"
    )

    drafted_sections: list[dict[str, Any]] = []
    prev_tail = ""
    for idx, sp in enumerate(sec_plans, start=1):
        sec_cache = cache_dir / f"{chapter_id}_stage1_sec{idx}.json"
        s_hash = compute_cache_hash({"sp": sp, "prev": prev_tail, "model": draft_model})
        cached_sec = load_cached_json(sec_cache, s_hash)
        if cached_sec is not None:
            print(f"  [CACHE HIT] Stage 1 第 {idx} 節：{sp['heading']}", flush=True)
            sec_obj = cached_sec
        else:
            print(f"  * Stage 1 撰寫第 {idx}/{len(sec_plans)} 節：{sp['heading']}", flush=True)
            active_gloss = extract_active_glossary(glossary, json.dumps(sp, ensure_ascii=False))
            usr_sec = (
                f"章節：{outline['badge']} {outline['title']['zh-TW']}\n"
                f"本節藍圖：{json.dumps(sp, ensure_ascii=False)}\n"
                f"鎖定術語：\n{active_gloss}\n"
                + (f"\n上一節結尾（請自然順接文氣，勿重複）：\n{prev_tail}\n" if prev_tail else "")
                + f"\n本章真實 Python 3.12 範例：\n{src_code}\n\n實機輸出：\n{live_out}\n"
            )
            sec_obj = call_lm_json(
                base_url=base_url,
                model=draft_model,
                system_prompt=sys_draft_sec,
                user_prompt=usr_sec,
                temperature=0.55,
                max_tokens=2200,
                reasoning_effort="none",
                use_dry=True,
                http_fn=http_fn,
                lms=lms,
            )
            sec_obj["id"] = str(sp.get("id") or f"sec{idx}")
            save_cached_json(sec_cache, s_hash, sec_obj)
        drafted_sections.append(sec_obj)
        prev_tail = "\n".join(sec_obj.get("paragraphs") or [])[-350:]

    # Stage 1b: Structured modules (diagram + comparison table + walkthrough)
    mod_a_cache = cache_dir / f"{chapter_id}_stage1_mod_a.json"
    mod_a_hash = compute_cache_hash({"plan": plan, "src": src_code, "out": live_out, "model": draft_model})
    mod_a = load_cached_json(mod_a_cache, mod_a_hash)
    if mod_a is None:
        print("  * Stage 1 產出原生 SVG 架構圖、對照表與程式碼拆解...", flush=True)
        sys_mod_a = (
            "你是技術專書視覺與架構設計編輯，請嚴格只回傳單一合法 JSON。\n"
            "diagram_svg 必須以 <svg viewBox=\"0 0 760 260\" role=\"img\" aria-label=\"...\" xmlns=\"http://www.w3.org/2000/svg\"> 開頭、"
            "以 </svg> 結尾，元素總數 < 55，配色使用暖紙底 #fdfcf9、墨黑 #1c1917、森林綠 #15803d、琥珀 #b45309；"
            "嚴禁 <script>/<foreignObject>/<image>/<use>/on* 事件屬性。"
        )
        usr_mod_a = (
            f"章節：{outline['badge']} {outline['title']['zh-TW']}\n"
            f"架構圖構想：{plan.get('diagram_concept', '')}\n"
            f"對照表構想：{plan.get('table_concept', '')}\n"
            f"程式碼（{outline['example_file']}）：\n{src_code}\n\n實機輸出：\n{live_out}\n\n"
            "請輸出 JSON：\n"
            '{"aeo_capsule":"120字內可獨立被 AI 引用之定義膠囊（可用 <strong> 與 <code>）",'
            '"diagram_caption":"圖 X-1：...",'
            '"diagram_svg":"<svg viewBox=\\"0 0 760 260\\" role=\\"img\\" aria-label=\\"...\\" xmlns=\\"http://www.w3.org/2000/svg\\">...</svg>",'
            '"comparison_table":{"caption":"表 X-1：...","headers":["..."],"rows":[["..."]]},'
            '"code_walkthrough":["設計亮點1","設計亮點2","設計亮點3","設計亮點4"]}'
        )
        for attempt in range(1, MAX_QA_RETRIES + 1):
            cand = call_lm_json(
                base_url=base_url,
                model=draft_model,
                system_prompt=sys_mod_a,
                user_prompt=usr_mod_a,
                temperature=0.3,
                max_tokens=2600,
                reasoning_effort="none",
                http_fn=http_fn,
                lms=lms,
            )
            svg_errs = validate_svg_safe(str(cand.get("diagram_svg") or ""))
            if not svg_errs:
                mod_a = cand
                break
            print(f"    [WARN SVG retry {attempt}/{MAX_QA_RETRIES}] {svg_errs}", flush=True)
            usr_mod_a += f"\n\n上次 SVG 驗證失敗：{svg_errs}，請修復後重新輸出完整 JSON。"
        if mod_a is None:
            raise RuntimeError("Failed to generate a valid safe diagram_svg after retries")
        save_cached_json(mod_a_cache, mod_a_hash, mod_a)

    # Stage 1c: Pitfalls + Quiz + Interview FAQs + Further Reading
    mod_b_cache = cache_dir / f"{chapter_id}_stage1_mod_b.json"
    mod_b_hash = compute_cache_hash({"plan": plan, "outline": outline, "model": draft_model})
    mod_b = load_cached_json(mod_b_cache, mod_b_hash)
    if mod_b is None:
        print("  * Stage 1 產出 3 個生產踩坑、3 題互動測驗與 4 題面試 FAQ...", flush=True)
        sys_mod_b = "你是資深 AI 工程面試官與 SRE，請只輸出單一合法 JSON，內容具體且具實戰含金量。"
        usr_mod_b = (
            f"章節：{outline['badge']} {outline['title']['zh-TW']}\n"
            f"踩坑主題：{json.dumps(plan.get('pitfall_topics', []), ensure_ascii=False)}\n"
            f"測驗考點：{json.dumps(plan.get('quiz_topics', []), ensure_ascii=False)}\n"
            f"面試主題：{json.dumps(plan.get('faq_topics', []), ensure_ascii=False)}\n"
            f"參考來源：{json.dumps(outline.get('youtube_references', []), ensure_ascii=False)}\n\n"
            "請輸出 JSON：\n"
            '{"pitfalls":[{"title":"陷阱 1：...","symptom":"...","root_cause_and_fix":"..."}],'
            '"quiz":[{"question":"...","options":["A","B","C","D"],"answer_index":0,"explanation":"..."}],'
            '"interview_faqs":[{"question":"...","answer":"..."}],'
            '"further_reading":[{"title":"...","url":"https://...","note":"..."}]}'
        )
        mod_b = call_lm_json(
            base_url=base_url,
            model=draft_model,
            system_prompt=sys_mod_b,
            user_prompt=usr_mod_b,
            temperature=0.35,
            max_tokens=2600,
            reasoning_effort="none",
            http_fn=http_fn,
            lms=lms,
        )
        save_cached_json(mod_b_cache, mod_b_hash, mod_b)

    # Stage 2: SINGLE MODEL SWAP -> Gemma4 Editorial Polish + Mechanical Textbook Linter
    if lms is not None:
        lms.switch_model(polish_model)
    print(f">>> [Stage 2/3] 以 {polish_model} 執行純台灣繁中總編精修 ＆ 機械 Linter 守門 ...", flush=True)

    sys_polish_sec = (
        "你是紫楓出版社（Purple Maple Press）台灣繁體中文技術專書總編輯。\n"
        "你的任務是把初稿精修成「100% 純台灣繁體中文、零簡體字、零中國技術用語（嚴禁內存/代碼/調用/視頻/默認/算法/數組/鏈表/信息/創建/響應/緩存）、"
        "零 AI 罐頭詞、專業俐落且易懂」的出版級小節。\n"
        "保留所有技術正確性、數字與公式，只輸出單一合法 JSON（相同鍵值：id, heading, paragraphs, bullets, callout_title, callout_body）。"
    )

    polished_sections: list[dict[str, Any]] = []
    for idx, raw_sec in enumerate(drafted_sections, start=1):
        sec_p_cache = cache_dir / f"{chapter_id}_stage2_sec{idx}.json"
        sp_hash = compute_cache_hash({"raw": raw_sec, "model": polish_model})
        cached_p = load_cached_json(sec_p_cache, sp_hash)
        if cached_p is not None and not run_textbook_section_linter(cached_p, locale="zh-TW"):
            print(f"  [CACHE HIT] Stage 2 第 {idx} 節已過 Linter", flush=True)
            polished_sections.append(cached_p)
            continue

        cur_sec = raw_sec
        for attempt in range(1, MAX_QA_RETRIES + 1):
            lint_before = run_textbook_section_linter(cur_sec, locale="zh-TW")
            fix_block = (
                "\n\n【機械 Linter 必改項目】\n- " + "\n- ".join(lint_before)
                if lint_before
                else "\n\n請進行出版級文字流暢度與純台灣繁中用語潤飾。"
            )
            cur_sec = call_lm_json(
                base_url=base_url,
                model=polish_model,
                system_prompt=sys_polish_sec,
                user_prompt=f"待精修小節 JSON：\n{json.dumps(cur_sec, ensure_ascii=False)}{fix_block}",
                temperature=0.35,
                max_tokens=2300,
                reasoning_effort="none",
                use_dry=True,
                http_fn=http_fn,
                lms=lms,
            )
            cur_sec["id"] = str(raw_sec["id"])
            lint_after = run_textbook_section_linter(cur_sec, locale="zh-TW")
            if not lint_after:
                print(f"    [LINTER PASS] 第 {idx} 節（嘗試 {attempt} 次）", flush=True)
                break
            print(f"    [LINTER RETRY #{attempt}] 第 {idx} 節：{lint_after}", flush=True)
        save_cached_json(sec_p_cache, sp_hash, cur_sec)
        polished_sections.append(cur_sec)

    # Polish structured modules through Gemma4 to eliminate any Qwen Simplified drift
    mod_p_cache = cache_dir / f"{chapter_id}_stage2_mods.json"
    mp_hash = compute_cache_hash({"a": mod_a, "b": mod_b, "model": polish_model})
    polished_mods = load_cached_json(mod_p_cache, mp_hash)
    if polished_mods is None:
        print("  * Stage 2 精修架構圖文字、對照表、踩坑、測驗與面試 FAQ（清除簡體與陸語）...", flush=True)
        sys_polish_mods = (
            "你是台灣繁體中文技術專書校對總編。將輸入 JSON 中所有文字（包含 diagram_svg 內標籤、對照表、踩坑、測驗與 FAQ）"
            "統一修正為 100% 純台灣繁體中文（改用記憶體／程式碼／呼叫／預設／演算法／陣列／鏈結串列／快取／資訊／建立／回應），"
            "完整保留 SVG 結構與 JSON Schema，僅回傳單一合法 JSON。"
        )
        combined_mods = {**mod_a, **mod_b}
        polished_mods = call_lm_json(
            base_url=base_url,
            model=polish_model,
            system_prompt=sys_polish_mods,
            user_prompt=json.dumps(combined_mods, ensure_ascii=False),
            temperature=0.2,
            max_tokens=3600,
            reasoning_effort="none",
            http_fn=http_fn,
            lms=lms,
        )
        if validate_svg_safe(str(polished_mods.get("diagram_svg") or "")):
            polished_mods["diagram_svg"] = mod_a["diagram_svg"]
        save_cached_json(mod_p_cache, mp_hash, polished_mods)

    chapter_payload: dict[str, Any] = {
        "book_id": book_id,
        "chapter_id": chapter_id,
        "locale": "zh-TW",
        "status": "draft",
        "badge": outline["badge"],
        "part_id": outline["part"],
        "title": outline["title"]["zh-TW"],
        "short_title": outline["short_title"]["zh-TW"],
        "summary": outline["summary"]["zh-TW"],
        "aeo_capsule": polished_mods["aeo_capsule"],
        "reading_minutes": 18,
        "lastmod": date.today().isoformat(),
        "example_file": outline["example_file"],
        "keywords": list(outline["key_topics"]) + ["紫楓出版社"],
        "learning_objectives": list(outline["learning_objectives"]),
        "sections": polished_sections,
        "diagram_caption": polished_mods["diagram_caption"],
        "diagram_svg": polished_mods["diagram_svg"],
        "comparison_table": polished_mods["comparison_table"],
        "code_walkthrough": polished_mods["code_walkthrough"],
        "pitfalls": polished_mods["pitfalls"],
        "quiz": polished_mods["quiz"],
        "interview_faqs": polished_mods["interview_faqs"],
        "further_reading": polished_mods.get("further_reading", []),
    }

    parsed = parse_chapter_json(chapter_payload)
    issues = audit_chapter_quality(parsed)
    prose_len = count_prose_from_chapter(parsed, "zh-TW")
    print(f"  [DRAFT AUDIT zh-TW/{chapter_id}] prose={prose_len} chars, issues={issues or 'NONE'}", flush=True)

    target = book_dir / "chapters" / "zh-TW" / f"{chapter_id}.json"
    atomic_write_json(target, chapter_payload, force=force)
    return target


def forge_translate(
    *,
    repo_root: Path,
    book_id: str,
    chapter_id: str,
    target_locale: str,
    base_url: str,
    model: str | None = None,
    force: bool = False,
    http_fn: Callable[..., dict[str, Any]] = default_http_json,
    lms: LmsController | None = None,
) -> Path:
    """
    Chunked two-pass translation (zh-TW -> zh-CN or en) inside the Golden 4K-6K window:
      - `en`: Gemma4-26B-A4B (zero model swap, max_tokens=3200, zero-CJK + Python compile QA)
      - `zh-CN`: Qwen3.6-35B-A3B (zero model swap, zero-Trad + zero-Taiwan-term QA)
    """
    if target_locale not in ("zh-CN", "en"):
        raise ValueError(f"Unsupported translation target locale: {target_locale!r}")

    book_dir, _book_meta, outline, glossary = _load_book_context(repo_root, book_id, chapter_id)
    src_path = book_dir / "chapters" / "zh-TW" / f"{chapter_id}.json"
    if not src_path.is_file():
        raise FileNotFoundError(f"Source zh-TW chapter missing: {src_path}")
    src_data = json.loads(src_path.read_text(encoding="utf-8"))
    raw_code, raw_out = run_example_script(repo_root, src_data["example_file"])

    chosen_model = model or (DEFAULT_POLISH_MODEL if target_locale == "en" else DEFAULT_DRAFT_MODEL)
    if lms is not None:
        lms.switch_model(chosen_model)

    print(f">>> [Stage 3] 以 {chosen_model} 執行 {chapter_id} 分塊翻譯 -> {target_locale} ...", flush=True)
    cache_dir = book_dir / ".forge_cache"
    max_toks = 3200 if target_locale == "en" else 2400

    lang_directive = (
        "Target language: Natural O'Reilly-grade Technical English (en). "
        "ZERO Chinese/CJK characters permitted anywhere in values."
        if target_locale == "en"
        else "目標語言：中國大陸簡體中文（zh-Hans）技術專書用語。"
        "嚴禁任何繁體字與台灣慣用語（禁詞：詞元、推論、檢索、微調、幻覺、權重、視窗、切塊、程式碼、講義、紫楓、社團、陣列、鏈結串列、演算法、預設、記憶體、呼叫、快取）。"
    )

    def _translate_chunk(chunk_name: str, chunk_obj: dict[str, Any], extra_check: Callable[[dict[str, Any]], list[str]] | None = None) -> dict[str, Any]:
        c_path = cache_dir / f"{chapter_id}_tr_{target_locale}_{chunk_name}.json"
        c_hash = compute_cache_hash({"chunk": chunk_obj, "locale": target_locale, "model": chosen_model})
        cached = load_cached_json(c_path, c_hash)
        if cached is not None and (extra_check is None or not extra_check(cached)):
            print(f"  [CACHE HIT] {target_locale}/{chunk_name}", flush=True)
            return cached

        gloss_txt = extract_active_glossary(glossary, json.dumps(chunk_obj, ensure_ascii=False), target_locale)
        sys_p = (
            f"你是紫楓出版社資深技術書籍譯者（目標語系：{target_locale}）。\n"
            f"{lang_directive}\n"
            "嚴格保留輸入 JSON 的所有 Key 結構，只翻譯字串值，僅回傳單一合法 JSON 物件。"
        )
        prior_errs: list[str] = []
        result: dict[str, Any] = chunk_obj
        for attempt in range(1, MAX_QA_RETRIES + 1):
            err_note = "\n\n【上次質檢失敗，請全數修復】\n- " + "\n- ".join(prior_errs) if prior_errs else ""
            usr_p = f"鎖定術語表：\n{gloss_txt}{err_note}\n\n來源 JSON：\n{json.dumps(chunk_obj, ensure_ascii=False)}"
            result = call_lm_json(
                base_url=base_url,
                model=chosen_model,
                system_prompt=sys_p,
                user_prompt=usr_p,
                temperature=0.25,
                max_tokens=max_toks,
                reasoning_effort="none",
                http_fn=http_fn,
                lms=lms,
            )
            errs = _check_translated_blob(result, target_locale)
            if extra_check is not None:
                errs.extend(extra_check(result))
            if not errs:
                break
            prior_errs = errs
            print(f"    [QA RETRY {attempt}/{MAX_QA_RETRIES}] {target_locale}/{chunk_name}: {errs[:4]}", flush=True)
        save_cached_json(c_path, c_hash, result)
        return result

    # Chunk 1: Header + Table + Walkthrough
    head_src = {
        "title": outline["title"].get(target_locale, src_data["title"]),
        "short_title": outline["short_title"].get(target_locale, src_data["short_title"]),
        "summary": outline["summary"].get(target_locale, src_data["summary"]),
        "aeo_capsule": src_data["aeo_capsule"],
        "keywords": src_data["keywords"],
        "learning_objectives": src_data["learning_objectives"],
        "comparison_table": src_data["comparison_table"],
        "code_walkthrough": src_data["code_walkthrough"],
    }
    head_tr = _translate_chunk("head", head_src)

    # Chunk 2..N: Each section individually
    tr_sections: list[dict[str, Any]] = []
    for idx, sec in enumerate(src_data["sections"], start=1):
        sec_tr = _translate_chunk(
            f"sec{idx}",
            sec,
            extra_check=lambda obj: run_textbook_section_linter(obj, locale=target_locale),
        )
        sec_tr["id"] = sec["id"]
        tr_sections.append(sec_tr)

    # Chunk N+1: Diagram SVG + Pitfalls + Quiz + FAQs + Further Reading
    tail_src = {
        "diagram_caption": src_data["diagram_caption"],
        "diagram_svg": src_data["diagram_svg"],
        "pitfalls": src_data["pitfalls"],
        "quiz": src_data["quiz"],
        "interview_faqs": src_data["interview_faqs"],
        "further_reading": src_data.get("further_reading", []),
    }
    tail_tr = _translate_chunk(
        "tail",
        tail_src,
        extra_check=lambda obj: validate_svg_safe(str(obj.get("diagram_svg") or "")),
    )

    # Chunk N+2: Deterministic code_replacements & output_replacements verified by compile()
    code_keys, out_keys = extract_cjk_literals_from_code(raw_code, raw_out)
    rep_src = {
        "code_map": {k: k for k in code_keys},
        "output_map": {k: k for k in out_keys},
    }

    def _verify_code_rep(obj: dict[str, Any]) -> list[str]:
        c_map = obj.get("code_map") or {}
        o_map = obj.get("output_map") or {}
        if not isinstance(c_map, dict) or not isinstance(o_map, dict):
            return ["code_map and output_map must be JSON dicts"]
        code_pairs = [(k, str(c_map.get(k, k))) for k in code_keys]
        out_pairs = [(k, str(o_map.get(k, k))) for k in out_keys]
        try:
            loc_src, loc_out = localize_code_and_output(
                target_locale,
                chapter_id,
                raw_code,
                raw_out,
                {chapter_id: code_pairs},
                {chapter_id: out_pairs},
            )
        except Exception as exc:
            return [f"localize_code_and_output failed: {exc}"]
        return _check_translated_blob({"src": loc_src, "out": loc_out}, target_locale)

    rep_cache = cache_dir / f"{chapter_id}_tr_{target_locale}_coderep.json"
    rep_hash = compute_cache_hash({"rep": rep_src, "locale": target_locale, "model": chosen_model})
    rep_tr = load_cached_json(rep_cache, rep_hash)
    if rep_tr is None or _verify_code_rep(rep_tr):
        sys_rep = (
            f"你是 Python 技術譯者（目標語系：{target_locale}）。\n"
            "輸入的 code_map 與 output_map 鍵值是原始繁體中文程式碼註解／print 標籤，請**絕對不要修改鍵名（key）**，"
            f"僅將每個值（value）翻譯成道地 {target_locale}。若目標是 en，值內禁止任何中文字或全形標點。"
            "只回傳合法 JSON。"
        )
        rep_errs: list[str] = []
        for attempt in range(1, MAX_QA_RETRIES + 1):
            note = "\n上次驗證錯誤：" + "; ".join(rep_errs) if rep_errs else ""
            rep_tr = call_lm_json(
                base_url=base_url,
                model=chosen_model,
                system_prompt=sys_rep,
                user_prompt=json.dumps(rep_src, ensure_ascii=False) + note,
                temperature=0.15,
                max_tokens=2000,
                reasoning_effort="none",
                http_fn=http_fn,
                lms=lms,
            )
            rep_errs = _verify_code_rep(rep_tr)
            if not rep_errs:
                break
            print(f"    [CODEREP RETRY {attempt}/{MAX_QA_RETRIES}] {rep_errs}", flush=True)
        save_cached_json(rep_cache, rep_hash, rep_tr or rep_src)

    c_map_final = (rep_tr or {}).get("code_map") or {}
    o_map_final = (rep_tr or {}).get("output_map") or {}
    code_pairs_final = [[k, str(c_map_final.get(k, k))] for k in code_keys if k in raw_code]
    out_pairs_final = [[k, str(o_map_final.get(k, k))] for k in out_keys if k in raw_out]

    translated_payload: dict[str, Any] = {
        "book_id": book_id,
        "chapter_id": chapter_id,
        "locale": target_locale,
        "status": "draft",
        "badge": src_data["badge"],
        "part_id": src_data["part_id"],
        "title": head_tr["title"],
        "short_title": head_tr["short_title"],
        "summary": head_tr["summary"],
        "aeo_capsule": head_tr["aeo_capsule"],
        "reading_minutes": src_data["reading_minutes"],
        "lastmod": date.today().isoformat(),
        "example_file": src_data["example_file"],
        "keywords": head_tr["keywords"],
        "learning_objectives": head_tr["learning_objectives"],
        "sections": tr_sections,
        "diagram_caption": tail_tr["diagram_caption"],
        "diagram_svg": tail_tr["diagram_svg"],
        "comparison_table": head_tr["comparison_table"],
        "code_walkthrough": head_tr["code_walkthrough"],
        "pitfalls": tail_tr["pitfalls"],
        "quiz": tail_tr["quiz"],
        "interview_faqs": tail_tr["interview_faqs"],
        "further_reading": tail_tr.get("further_reading", []),
        "code_replacements": code_pairs_final,
        "output_replacements": out_pairs_final,
    }

    parsed = parse_chapter_json(translated_payload)
    issues = audit_chapter_quality(parsed)
    prose_len = count_prose_from_chapter(parsed, target_locale)
    print(f"  [TRANSLATE AUDIT {target_locale}/{chapter_id}] prose={prose_len}, issues={issues or 'NONE'}", flush=True)

    target = book_dir / "chapters" / target_locale / f"{chapter_id}.json"
    atomic_write_json(target, translated_payload, force=force)
    return target


def _check_translated_blob(obj: dict[str, Any], target_locale: str) -> list[str]:
    blob = json.dumps(obj, ensure_ascii=False)
    issues: list[str] = []
    if target_locale == "en":
        leaks = _CJK_RE.findall(blob)
        if leaks:
            issues.append(f"English output leaked CJK chars: {leaks[:8]}")
    elif target_locale == "zh-CN":
        for bad in ZH_CN_BANNED_TERMS:
            if bad in blob:
                issues.append(f"zh-CN leaked Taiwan term: {bad!r}")
        trad = sorted({c for c in blob if c in ZH_CN_BANNED_TRAD_CHARS})
        if trad:
            issues.append(f"zh-CN leaked Traditional chars: {''.join(trad[:10])}")
    return issues


def forge_full_chapters(
    *,
    repo_root: Path,
    book_id: str,
    chapter_ids: list[str],
    base_url: str,
    draft_model: str = DEFAULT_DRAFT_MODEL,
    polish_model: str = DEFAULT_POLISH_MODEL,
    force: bool = False,
    http_fn: Callable[..., dict[str, Any]] = default_http_json,
    lms: LmsController | None = None,
) -> list[Path]:
    """
    One-click end-to-end trilingual textbook pipeline with optimal 2-swap GPU scheduling:
      Draft (Qwen -> Gemma) -> Translate EN (Gemma still hot!) -> Translate zh-CN (Qwen) -> Unload VRAM.
    """
    outputs: list[Path] = []
    try:
        for cid in chapter_ids:
            print(f"\n============================================================", flush=True)
            print(f">>> [FORGE] 啟動全自動三語專書流水線：{book_id} / {cid}", flush=True)
            print(f"============================================================", flush=True)
            p_tw = forge_draft(
                repo_root=repo_root,
                book_id=book_id,
                chapter_id=cid,
                base_url=base_url,
                draft_model=draft_model,
                polish_model=polish_model,
                force=force,
                http_fn=http_fn,
                lms=lms,
            )
            outputs.append(p_tw)
            # Gemma4 is STILL loaded after Stage 2 -> translate English with ZERO extra swap!
            p_en = forge_translate(
                repo_root=repo_root,
                book_id=book_id,
                chapter_id=cid,
                target_locale="en",
                base_url=base_url,
                model=polish_model,
                force=force,
                http_fn=http_fn,
                lms=lms,
            )
            outputs.append(p_en)
            # Single swap to Qwen3.6 for Mainland Simplified Chinese
            p_cn = forge_translate(
                repo_root=repo_root,
                book_id=book_id,
                chapter_id=cid,
                target_locale="zh-CN",
                base_url=base_url,
                model=draft_model,
                force=force,
                http_fn=http_fn,
                lms=lms,
            )
            outputs.append(p_cn)
    finally:
        if lms is not None:
            lms.unload_all()
    return outputs


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
            if loc == "zh-TW":
                for sec in parsed.sections:
                    sec_dict = {
                        "heading": sec.heading,
                        "paragraphs": list(sec.paragraphs),
                        "bullets": list(sec.bullets),
                        "callout_title": sec.callout_title,
                        "callout_body": sec.callout_body,
                    }
                    issues.extend(run_textbook_section_linter(sec_dict, locale="zh-TW"))
            prose = count_prose_from_chapter(parsed, loc)
            if issues:
                failures += 1
                print(f"[FAIL] {book_id}/{loc}/{cid} (status={parsed.status}, prose={prose}): {issues}")
            else:
                print(f"[PASS] {book_id}/{loc}/{cid} (status={parsed.status}, prose={prose})")
    print(f"\nAudit complete: {checked - failures}/{checked} chapters passed.")
    return 1 if failures else 0


def _resolve_chapter_ids(chapter: str | None, ch_from: int | None, ch_to: int | None) -> list[str]:
    if chapter:
        return [chapter]
    if ch_from is not None and ch_to is not None:
        return [f"ch{n:02d}" for n in range(ch_from, ch_to + 1)]
    raise ValueError("Must specify either --chapter chXX or both --from N --to M")


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Purple Maple Press Local LLM Book Forge CLI v2.0")
    parser.add_argument("--base-url", default=DEFAULT_LM_BASE_URL, help="LM Studio OpenAI-compatible base URL")
    parser.add_argument("--draft-model", default=DEFAULT_DRAFT_MODEL, help="Model for planning, drafting & zh-CN")
    parser.add_argument("--polish-model", default=DEFAULT_POLISH_MODEL, help="Model for zh-TW polish & en")
    parser.add_argument("--model", default=None, help="Override single model for translate/draft")
    parser.add_argument("--no-lms", action="store_true", help="Do not invoke lms CLI server start / model switching")
    sub = parser.add_subparsers(dest="command", required=True)

    p_st = sub.add_parser("status", help="Show trilingual chapter publication status")
    p_st.add_argument("--book", default=None)

    sub.add_parser("check-lm", help="Check local LM Studio connection & loaded models")

    p_pl = sub.add_parser("plan", help="Stage 0: generate structured 4-section chapter blueprint")
    p_pl.add_argument("--book", required=True)
    p_pl.add_argument("--chapter", required=True)
    p_pl.add_argument("--force", action="store_true")

    p_dr = sub.add_parser("draft", help="Stage 0-2: section-by-section Qwen draft + Gemma4 zh-TW editorial polish")
    p_dr.add_argument("--book", required=True)
    p_dr.add_argument("--chapter", required=True)
    p_dr.add_argument("--force", action="store_true", help="Allow overwriting a published chapter")

    p_tr = sub.add_parser("translate", help="Stage 3: chunked translation (zh-TW -> zh-CN or en)")
    p_tr.add_argument("--book", required=True)
    p_tr.add_argument("--chapter", required=True)
    p_tr.add_argument("--to", required=True, choices=["zh-CN", "en"])
    p_tr.add_argument("--force", action="store_true", help="Allow overwriting a published chapter")

    p_fg = sub.add_parser("forge", help="One-click end-to-end trilingual pipeline (Plan + Draft + Polish + EN + ZH-CN + Audit)")
    p_fg.add_argument("--book", required=True)
    p_fg.add_argument("--chapter", default=None)
    p_fg.add_argument("--from", dest="ch_from", type=int, default=None)
    p_fg.add_argument("--to", dest="ch_to", type=int, default=None)
    p_fg.add_argument("--force", action="store_true")

    p_au = sub.add_parser("audit", help="Run mechanical QA audit on existing chapter JSON files")
    p_au.add_argument("--book", required=True)

    args = parser.parse_args(argv)
    lms = LmsController(enabled=not args.no_lms)
    draft_m = args.model or args.draft_model
    polish_m = args.model or args.polish_model

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
    if args.command == "plan":
        try:
            plan = forge_plan(
                repo_root=REPO_ROOT,
                book_id=args.book,
                chapter_id=args.chapter,
                base_url=args.base_url,
                draft_model=draft_m,
                lms=lms,
                force_cache=args.force,
            )
            print(f"[OK] Planned {len(plan.get('sections', []))} sections for {args.book}/{args.chapter}")
            return 0
        finally:
            lms.unload_all()
    if args.command == "draft":
        try:
            out_path = forge_draft(
                repo_root=REPO_ROOT,
                book_id=args.book,
                chapter_id=args.chapter,
                base_url=args.base_url,
                draft_model=draft_m,
                polish_model=polish_m,
                force=args.force,
                lms=lms,
            )
            print(f"[OK] Wrote polished zh-TW draft chapter to: {out_path}")
            return 0
        finally:
            lms.unload_all()
    if args.command == "translate":
        try:
            out_path = forge_translate(
                repo_root=REPO_ROOT,
                book_id=args.book,
                chapter_id=args.chapter,
                target_locale=args.to,
                base_url=args.base_url,
                model=args.model,
                force=args.force,
                lms=lms,
            )
            print(f"[OK] Wrote translated {args.to} draft to: {out_path}")
            return 0
        finally:
            lms.unload_all()
    if args.command == "forge":
        ch_ids = _resolve_chapter_ids(args.chapter, args.ch_from, args.ch_to)
        forge_full_chapters(
            repo_root=REPO_ROOT,
            book_id=args.book,
            chapter_ids=ch_ids,
            base_url=args.base_url,
            draft_model=draft_m,
            polish_model=polish_m,
            force=args.force,
            lms=lms,
        )
        return cmd_audit(REPO_ROOT, args.book)
    if args.command == "audit":
        return cmd_audit(REPO_ROOT, args.book)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
