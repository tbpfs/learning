#!/usr/bin/env python3
"""
book_models.py - Data models, shared localization/SVG QA gates, and Trilingual Atomic
Publication loader for Purple Maple Press (`learn.ai-purplemaple.com/books/<book_id>/`).

Zero external dependencies (Python 3.12 stdlib only). Imported by both `build_site.py`,
`scripts/book_forge.py`, and `tests/test_examples.py` as a single SSOT.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

FB_GROUP_URL = "https://www.facebook.com/share/g/19jsJ8crsC/"
GITHUB_ISSUES_URL = "https://github.com/tbpfs/learning/issues"
SUPPORTED_BOOK_LOCALES: tuple[str, ...] = ("zh-TW", "zh-CN", "en")

ZH_CN_BANNED_TERMS: tuple[str, ...] = (
    # Existing DSA / UI terms
    "陣列", "鏈結串列", "堆疊", "佇列", "雜湊表", "堆積", "演算法", "物件導向",
    "遞迴", "變數", "迴圈", "程式碼", "連結", "試算", "視窗", "資訊", "記憶體",
    "講義", "預設", "紫楓", "點擊展開", "實機執行", "隱私權", "總目錄", "鐵人賽",
    "博客來", "資料結構", "二元搜尋樹", "合併排序", "走訪", "範例", "括號",
    # Book 1 AI Engineering & Community Q&A terms (Taiwan -> Mainland mapping)
    "詞元", "推論", "檢索", "微調", "幻覺", "社團", "卡關", "發問", "一鍵複製",
    "權重", "閘門", "雜訊", "排程", "餘弦", "語意", "切塊", "詞表", "串列",
    "智能體框架中預設", "書架", "專書", "撰寫中", "還原", "顯存預估",
)

# Strictly Traditional-only characters (never shared with Simplified Chinese)
ZH_CN_BANNED_TRAD_CHARS: str = (
    "楓網學實複雜資結構時間點製輸驗證隱權饋幫進選錯誤這還觀關長審閱補總錄鐵賽單書課較維護對蹤層題難試問碼導場義廣頁"
    "詞論檢調覺團發鍵視閘訊餘語塊體計畫圖設備驅動規範編譯寫讀號評測確認線節類標準響應優歷緩衝檔衛鎖鏈轉換產業務連"
)

_CJK_RE = re.compile(r"[\u4e00-\u9fff]")
_EN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9'-]*")
_SVG_DANGEROUS_RE = re.compile(
    r"<\s*(script|foreignObject|image|use|iframe|object|embed)\b"
    r"|<!ENTITY"
    r"|javascript\s*:"
    r"|\bon[a-z]+\s*=",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class BookPart:
    id: str
    title: dict[str, str]
    chapters: tuple[str, ...]


@dataclass(frozen=True)
class BookChapterOutline:
    id: str
    badge: str
    part: str
    example_file: str
    title: dict[str, str]
    short_title: dict[str, str]
    summary: dict[str, str]
    learning_objectives: tuple[str, ...]
    key_topics: tuple[str, ...]
    youtube_references: tuple[str, ...]


@dataclass(frozen=True)
class BookMeta:
    id: str
    cover_image: str
    cover_width: int
    cover_height: int
    status: str
    date_published: str
    date_modified: str
    audience: dict[str, str]
    title: dict[str, str]
    subtitle: dict[str, str]
    eyebrow: dict[str, str]
    description: dict[str, str]
    aeo_capsule: dict[str, str]
    cover_alt: dict[str, str]
    keywords: dict[str, str]
    parts: tuple[BookPart, ...]


@dataclass(frozen=True)
class BookSection:
    id: str
    heading: str
    paragraphs: tuple[str, ...]
    bullets: tuple[str, ...] = ()
    callout_title: str = ""
    callout_body: str = ""


@dataclass(frozen=True)
class BookComparisonTable:
    caption: str
    headers: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class BookPitfall:
    title: str
    symptom: str
    root_cause_and_fix: str


@dataclass(frozen=True)
class QuizQuestion:
    question: str
    options: tuple[str, ...]
    answer_index: int
    explanation: str


@dataclass(frozen=True)
class BookFAQ:
    question: str
    answer: str


@dataclass(frozen=True)
class FurtherReading:
    title: str
    url: str
    note: str


@dataclass(frozen=True)
class BookChapterData:
    book_id: str
    chapter_id: str
    locale: str
    status: str
    badge: str
    part_id: str
    title: str
    short_title: str
    summary: str
    aeo_capsule: str
    reading_minutes: int
    lastmod: str
    example_file: str
    keywords: tuple[str, ...]
    learning_objectives: tuple[str, ...]
    sections: tuple[BookSection, ...]
    diagram_caption: str
    diagram_svg: str
    comparison_table: BookComparisonTable
    code_walkthrough: tuple[str, ...]
    pitfalls: tuple[BookPitfall, ...]
    quiz: tuple[QuizQuestion, ...]
    interview_faqs: tuple[BookFAQ, ...]
    further_reading: tuple[FurtherReading, ...]
    code_replacements: tuple[tuple[str, str], ...] = ()
    output_replacements: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class LoadedBook:
    meta: BookMeta
    outlines: tuple[BookChapterOutline, ...]
    outlines_by_id: dict[str, BookChapterOutline]
    published_chapter_ids: tuple[str, ...]
    chapters_by_locale: dict[str, dict[str, BookChapterData]]


class _TagCounter(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.count += 1


def validate_svg_safe(svg: str, *, max_elements: int = 80) -> list[str]:
    """Validate inline SVG against XSS vectors, required a11y attributes, and DOM budget."""
    errors: list[str] = []
    stripped = svg.strip()
    if not stripped.startswith("<svg") or not stripped.endswith("</svg>"):
        errors.append("diagram_svg must be a single <svg ...>...</svg> element")
        return errors
    if _SVG_DANGEROUS_RE.search(stripped):
        errors.append("diagram_svg contains forbidden tag, entity, event handler, or javascript: URI")
    if "viewBox=" not in stripped:
        errors.append("diagram_svg missing viewBox attribute")
    if 'role="img"' not in stripped:
        errors.append('diagram_svg missing role="img" attribute')
    if "aria-label=" not in stripped:
        errors.append("diagram_svg missing aria-label attribute")
    counter = _TagCounter()
    counter.feed(stripped)
    if counter.count >= max_elements:
        errors.append(f"diagram_svg element count ({counter.count}) >= {max_elements} budget")
    return errors


def count_prose_from_chapter(ch: BookChapterData, locale_code: str) -> int:
    """Count prose length (CJK chars for zh-TW/zh-CN, English words for en) across substantive text."""
    parts: list[str] = [ch.summary, ch.aeo_capsule]
    parts.extend(ch.learning_objectives)
    for sec in ch.sections:
        parts.append(sec.heading)
        parts.extend(sec.paragraphs)
        parts.extend(sec.bullets)
        if sec.callout_title:
            parts.append(sec.callout_title)
        if sec.callout_body:
            parts.append(sec.callout_body)
    parts.extend(ch.code_walkthrough)
    for pf in ch.pitfalls:
        parts.extend((pf.title, pf.symptom, pf.root_cause_and_fix))
    for q in ch.quiz:
        parts.append(q.question)
        parts.extend(q.options)
        parts.append(q.explanation)
    for faq in ch.interview_faqs:
        parts.extend((faq.question, faq.answer))
    joined = "\n".join(parts)
    if locale_code == "en":
        return len(_EN_WORD_RE.findall(joined))
    return len(_CJK_RE.findall(joined))


def audit_chapter_quality(ch: BookChapterData) -> list[str]:
    """Run mechanical QA gates (prose depth, SVG safety, quiz integrity, locale purity)."""
    issues: list[str] = []
    min_prose = 1200 if ch.locale == "en" else 2500
    prose_len = count_prose_from_chapter(ch, ch.locale)
    if prose_len < min_prose:
        unit = "words" if ch.locale == "en" else "CJK chars"
        issues.append(f"prose length {prose_len} {unit} < {min_prose} minimum")

    issues.extend(validate_svg_safe(ch.diagram_svg))

    if len(ch.pitfalls) < 3:
        issues.append(f"pitfalls count {len(ch.pitfalls)} < 3")
    if len(ch.quiz) < 3:
        issues.append(f"quiz count {len(ch.quiz)} < 3")
    for idx, q in enumerate(ch.quiz):
        if len(q.options) < 3:
            issues.append(f"quiz[{idx}] must have >= 3 options")
        if not (0 <= q.answer_index < len(q.options)):
            issues.append(f"quiz[{idx}] answer_index {q.answer_index} out of range")
    if len(ch.interview_faqs) < 3:
        issues.append(f"interview_faqs count {len(ch.interview_faqs)} < 3")

    # Serialize all text fields (excluding code_replacements keys which intentionally contain zh-TW)
    all_visible = json.dumps(
        {
            "title": ch.title,
            "short_title": ch.short_title,
            "summary": ch.summary,
            "aeo_capsule": ch.aeo_capsule,
            "keywords": ch.keywords,
            "learning_objectives": ch.learning_objectives,
            "sections": [
                {
                    "heading": s.heading,
                    "paragraphs": s.paragraphs,
                    "bullets": s.bullets,
                    "callout_title": s.callout_title,
                    "callout_body": s.callout_body,
                }
                for s in ch.sections
            ],
            "diagram_caption": ch.diagram_caption,
            "diagram_svg": ch.diagram_svg,
            "table": {
                "caption": ch.comparison_table.caption,
                "headers": ch.comparison_table.headers,
                "rows": ch.comparison_table.rows,
            },
            "code_walkthrough": ch.code_walkthrough,
            "pitfalls": [
                (p.title, p.symptom, p.root_cause_and_fix) for p in ch.pitfalls
            ],
            "quiz": [(q.question, q.options, q.explanation) for q in ch.quiz],
            "faqs": [(f.question, f.answer) for f in ch.interview_faqs],
            "further_reading": [(r.title, r.note) for r in ch.further_reading],
        },
        ensure_ascii=False,
    )

    if ch.locale == "en":
        leaks = _CJK_RE.findall(all_visible)
        if leaks:
            issues.append(f"English chapter leaked CJK chars: {leaks[:8]}")
    elif ch.locale == "zh-CN":
        for bad in ZH_CN_BANNED_TERMS:
            if bad in all_visible:
                issues.append(f"zh-CN chapter leaked Taiwan term: {bad!r}")
        trad = sorted({c for c in all_visible if c in ZH_CN_BANNED_TRAD_CHARS})
        if trad:
            issues.append(f"zh-CN chapter leaked Traditional chars: {trad[:10]}")

    return issues


def parse_chapter_json(raw: dict[str, Any]) -> BookChapterData:
    """Parse and validate a single chapter JSON object into a frozen BookChapterData."""
    table_raw = raw["comparison_table"]
    table = BookComparisonTable(
        caption=str(table_raw["caption"]),
        headers=tuple(str(h) for h in table_raw["headers"]),
        rows=tuple(tuple(str(c) for c in row) for row in table_raw["rows"]),
    )
    sections = tuple(
        BookSection(
            id=str(s["id"]),
            heading=str(s["heading"]),
            paragraphs=tuple(str(p) for p in s["paragraphs"]),
            bullets=tuple(str(b) for b in s.get("bullets", ())),
            callout_title=str(s.get("callout_title", "")),
            callout_body=str(s.get("callout_body", "")),
        )
        for s in raw["sections"]
    )
    pitfalls = tuple(
        BookPitfall(
            title=str(p["title"]),
            symptom=str(p["symptom"]),
            root_cause_and_fix=str(p["root_cause_and_fix"]),
        )
        for p in raw["pitfalls"]
    )
    quiz = tuple(
        QuizQuestion(
            question=str(q["question"]),
            options=tuple(str(o) for o in q["options"]),
            answer_index=int(q["answer_index"]),
            explanation=str(q["explanation"]),
        )
        for q in raw["quiz"]
    )
    faqs = tuple(
        BookFAQ(question=str(f["question"]), answer=str(f["answer"]))
        for f in raw["interview_faqs"]
    )
    further = tuple(
        FurtherReading(title=str(r["title"]), url=str(r["url"]), note=str(r["note"]))
        for r in raw.get("further_reading", ())
    )
    code_rep = tuple((str(pair[0]), str(pair[1])) for pair in raw.get("code_replacements", ()))
    out_rep = tuple((str(pair[0]), str(pair[1])) for pair in raw.get("output_replacements", ()))
    return BookChapterData(
        book_id=str(raw["book_id"]),
        chapter_id=str(raw["chapter_id"]),
        locale=str(raw["locale"]),
        status=str(raw["status"]),
        badge=str(raw["badge"]),
        part_id=str(raw["part_id"]),
        title=str(raw["title"]),
        short_title=str(raw["short_title"]),
        summary=str(raw["summary"]),
        aeo_capsule=str(raw["aeo_capsule"]),
        reading_minutes=int(raw["reading_minutes"]),
        lastmod=str(raw["lastmod"]),
        example_file=str(raw["example_file"]),
        keywords=tuple(str(k) for k in raw["keywords"]),
        learning_objectives=tuple(str(obj) for obj in raw["learning_objectives"]),
        sections=sections,
        diagram_caption=str(raw["diagram_caption"]),
        diagram_svg=str(raw["diagram_svg"]),
        comparison_table=table,
        code_walkthrough=tuple(str(w) for w in raw["code_walkthrough"]),
        pitfalls=pitfalls,
        quiz=quiz,
        interview_faqs=faqs,
        further_reading=further,
        code_replacements=code_rep,
        output_replacements=out_rep,
    )


def load_book(books_dir: Path, book_id: str) -> LoadedBook:
    """
    Load book metadata, outlines, and chapters under strict Trilingual Atomic Publication Gate:
    A chapter is published ONLY when all 3 locale files exist with status == "published".
    If any chapter has status == "published" in some locales but not all 3, raise ValueError.
    """
    book_dir = books_dir / book_id
    meta_raw = json.loads((book_dir / "book.json").read_text(encoding="utf-8"))
    outlines_raw = json.loads((book_dir / "outlines.json").read_text(encoding="utf-8"))

    parts = tuple(
        BookPart(
            id=str(p["id"]),
            title=dict(p["title"]),
            chapters=tuple(str(c) for c in p["chapters"]),
        )
        for p in meta_raw["parts"]
    )
    meta = BookMeta(
        id=str(meta_raw["id"]),
        cover_image=str(meta_raw["cover_image"]),
        cover_width=int(meta_raw["cover_width"]),
        cover_height=int(meta_raw["cover_height"]),
        status=str(meta_raw["status"]),
        date_published=str(meta_raw["date_published"]),
        date_modified=str(meta_raw["date_modified"]),
        audience=dict(meta_raw["audience"]),
        title=dict(meta_raw["title"]),
        subtitle=dict(meta_raw["subtitle"]),
        eyebrow=dict(meta_raw["eyebrow"]),
        description=dict(meta_raw["description"]),
        aeo_capsule=dict(meta_raw["aeo_capsule"]),
        cover_alt=dict(meta_raw["cover_alt"]),
        keywords=dict(meta_raw["keywords"]),
        parts=parts,
    )

    outlines = tuple(
        BookChapterOutline(
            id=str(o["id"]),
            badge=str(o["badge"]),
            part=str(o["part"]),
            example_file=str(o["example_file"]),
            title=dict(o["title"]),
            short_title=dict(o["short_title"]),
            summary=dict(o["summary"]),
            learning_objectives=tuple(str(x) for x in o["learning_objectives"]),
            key_topics=tuple(str(x) for x in o["key_topics"]),
            youtube_references=tuple(str(x) for x in o.get("youtube_references", ())),
        )
        for o in outlines_raw["chapters"]
    )
    outlines_by_id = {o.id: o for o in outlines}

    chapters_by_locale: dict[str, dict[str, BookChapterData]] = {
        loc: {} for loc in SUPPORTED_BOOK_LOCALES
    }
    published_ids: list[str] = []

    for outline in outlines:
        statuses: dict[str, str | None] = {}
        loaded_per_loc: dict[str, BookChapterData] = {}
        for loc in SUPPORTED_BOOK_LOCALES:
            ch_path = book_dir / "chapters" / loc / f"{outline.id}.json"
            if not ch_path.is_file():
                statuses[loc] = None
                continue
            ch_data = parse_chapter_json(json.loads(ch_path.read_text(encoding="utf-8")))
            if ch_data.book_id != book_id or ch_data.chapter_id != outline.id or ch_data.locale != loc:
                raise ValueError(
                    f"Metadata mismatch in {ch_path}: got ({ch_data.book_id}, {ch_data.chapter_id}, {ch_data.locale})"
                )
            statuses[loc] = ch_data.status
            loaded_per_loc[loc] = ch_data

        pub_locales = [loc for loc, st in statuses.items() if st == "published"]
        if 0 < len(pub_locales) < len(SUPPORTED_BOOK_LOCALES):
            raise ValueError(
                f"Trilingual Atomic Publication Gate violation for {book_id}/{outline.id}: "
                f"statuses={statuses}. All 3 locales must be 'published' before shipping."
            )
        if len(pub_locales) == len(SUPPORTED_BOOK_LOCALES):
            published_ids.append(outline.id)
            for loc in SUPPORTED_BOOK_LOCALES:
                chapters_by_locale[loc][outline.id] = loaded_per_loc[loc]

    return LoadedBook(
        meta=meta,
        outlines=outlines,
        outlines_by_id=outlines_by_id,
        published_chapter_ids=tuple(published_ids),
        chapters_by_locale=chapters_by_locale,
    )


def discover_books(books_dir: Path) -> list[LoadedBook]:
    """Discover and load all books under books_dir sorted by directory name."""
    if not books_dir.is_dir():
        return []
    result: list[LoadedBook] = []
    for child in sorted(books_dir.iterdir()):
        if child.is_dir() and (child / "book.json").is_file():
            result.append(load_book(books_dir, child.name))
    return result
