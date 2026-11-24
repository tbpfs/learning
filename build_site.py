#!/usr/bin/env python3
"""
build_site.py - Static Site Generator for GitHub Pages (`tbpfs/learning`).
Zero external dependencies. Reads examples/ch01..ch07, executes each once to capture live output,
and renders an SEO/GEO-optimized tutorial portal (`index.html` Hub + `ch01.html`..`ch07.html` Deep-Dive Spokes).
"""

from __future__ import annotations

import argparse
import html
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence

REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from affiliate_config import (  # noqa: E402
    get_chapter_book_recommendation,
    get_learning_resources,
)
from chapter_content import CHAPTERS, ChapterSpec, ComparisonTable  # noqa: E402

ADSENSE_PUBLISHER_ID = "pub-6485917848711473"
ADSENSE_CLIENT_ID = f"ca-{ADSENSE_PUBLISHER_ID}"
ADSENSE_IN_ARTICLE_SLOT_ID = "1673180799"
ENABLE_MANUAL_AD_SLOTS = False  # Pre-approval SEO/UX hygiene: keep <head> verification script + ads.txt, hide empty dashed <ins> boxes until approved
INDEXNOW_KEY = "7f4e9c2a8b1d6035e4a92c7f1b8d3e60"
SITE_LASTMOD = "2026-11-24"

CHAPTER_YOUTUBE_VIDEOS: dict[str, dict[str, Any]] = {
    "ch01": {
        "video_id": "-LmHUlozTqE",
        "title": "[軟體工程師雜談] 輕鬆搞懂資料結構: Array(陣列), Linked list(連結串列) | IT鐵人賽",
        "upload_date": "2020-09-12T12:00:00+08:00",
        "views_label": "67,700+ 次觀看",
        "related": [
            ("2aSyeVdwATA", "【OpenMotion 動態圖解】單向鏈結串列原地反轉 (LeetCode #206) 三指標移動"),
            ("7xBrPbmOsSs", "輕鬆搞懂資料結構總覽（28,200+ 觀看）"),
            ("RObLhJlg2O8", "程式基礎語法：變數、資料型態、運算符號與陣列"),
        ],
    },
    "ch02": {
        "video_id": "0Kiunabmm0w",
        "title": "[軟體工程師雜談] 輕鬆搞懂資料結構: 堆疊(Stack) 與佇列(Queue) | IT鐵人賽",
        "upload_date": "2020-09-13T12:00:00+08:00",
        "views_label": "35,500+ 次觀看",
        "related": [
            ("qys8Cs7J0wE", "【零基礎生活圖解】用洋芋片筒與冬天穿衣服 3 分鐘看懂堆疊 Stack 與括號配對 (LeetCode #20)"),
            ("JSKtJqj2pwc", "輕鬆搞懂資料結構：佇列 Queue 詳解（23,900+ 觀看）"),
            ("hWrZPqJZXyg", "Function 函式總整理：基礎、Overload 與 Recursive 遞迴呼叫堆疊"),
        ],
    },
    "ch03": {
        "video_id": "DVDoyB5qDC4",
        "title": "[軟體工程師雜談] 輕鬆搞懂演算法: 快速排序(Quick Sort) 與搜尋排序複雜度 | IT鐵人賽",
        "upload_date": "2020-09-23T12:00:00+08:00",
        "views_label": "23,800+ 次觀看",
        "related": [
            ("3B4dXDxk_ck", "【OpenMotion 動態圖解】30秒徹底搞懂合併排序 Merge Sort 分治法 O(n log n)"),
            ("C9Xes8wH6Co", "輕鬆搞懂演算法：合併排序 Merge Sort（20,500+ 觀看）"),
            ("iwCUOKhIhAA", "演算法概論與 Big-O 時間複雜度（19,100+ 觀看）"),
            ("zO8kaBEy0M4", "氣泡排序、選擇排序、插入排序詳解（18,100+ 觀看）"),
            ("llSvc4rwxi0", "搜尋演算法：二元搜尋 Binary Search（13,300+ 觀看）"),
        ],
    },
    "ch04": {
        "video_id": "xDwFMffqLbw",
        "title": "[軟體工程師雜談] 輕鬆搞懂資料結構: 樹(Tree) 與雜湊表(Hash Table) | IT鐵人賽",
        "upload_date": "2020-09-16T12:00:00+08:00",
        "views_label": "41,900+ 次觀看",
        "related": [
            ("rr322eEWAUo", "【16:9 動態圖解】雜湊表 Hash Table ＋ LeetCode #1 Two Sum 從 O(n²) 降到 O(n)"),
            ("vPvxEDyxI2w", "輕鬆搞懂資料結構：雜湊 Hash Table（28,000+ 觀看）"),
            ("gA815MIEFg0", "輕鬆搞懂資料結構：集合 Set 與映射 Map（18,900+ 觀看）"),
        ],
    },
    "ch05": {
        "video_id": "c4R27mPT5kY",
        "title": "[軟體工程師雜談] 輕鬆搞懂演算法: 深度優先搜尋(DFS) 與廣度優先搜尋(BFS) | IT鐵人賽",
        "upload_date": "2020-09-27T12:00:00+08:00",
        "views_label": "22,600+ 次觀看",
        "related": [
            ("ebkBxAvyFds", "【零基礎生活圖解】用「水波擴散與迷宮探險」3分鐘看懂 BFS / DFS 與數島嶼 (LeetCode #200)"),
            ("V_ajcNni6wk", "資工系在學些什麼？資料結構、演算法、物件導向（22,600+ 觀看）"),
            ("5hYwLTVK4pY", "資料結構的複雜度 Big-O 總整理（15,000+ 觀看）"),
        ],
    },
    "ch06": {
        "video_id": "M2kYdAA-FHY",
        "title": "[軟體工程師雜談] 輕鬆搞懂演算法: 動態規劃(Dynamic Programming) | IT鐵人賽",
        "upload_date": "2020-09-29T12:00:00+08:00",
        "views_label": "31,700+ 次觀看",
        "related": [
            ("WhoRHltIukc", "【零基礎生活圖解】用「筆記本抄小抄與超商找零錢」3分鐘看懂動態規劃 DP (LeetCode #322)"),
            ("iLK48YAXjio", "常用演算法策略：暴力法、貪婪法、分治法、回溯法、分支限界法（26,800+ 觀看）"),
        ],
    },
    "ch07": {
        "video_id": "klbGg8dmYTM",
        "title": "[軟體工程師雜談] 輕鬆搞懂資料結構: 堆積(Heap) 與優先佇列 | IT鐵人賽",
        "upload_date": "2020-09-17T12:00:00+08:00",
        "views_label": "26,800+ 次觀看",
        "related": [
            ("fHBw99bYLuo", "堆積排序 (Heap Sort)、基數排序、桶排序詳解（13,200+ 觀看）"),
        ],
    },
}


def run_example(rel_path: str) -> tuple[str, str]:
    """Read source file and execute it to capture stdout."""
    script_path = REPO_ROOT / rel_path
    source = script_path.read_text(encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )
    return source, proc.stdout.strip()


def execute_all_examples(chapters: Sequence[ChapterSpec]) -> dict[str, tuple[str, str]]:
    """Execute each chapter script exactly once and cache (source_code, live_output) in memory."""
    cache: dict[str, tuple[str, str]] = {}
    for ch in chapters:
        cache[ch.id] = run_example(ch.file)
    return cache


def render_ad_slot(slot_label: str) -> str:
    """Render a CLS-safe responsive Google AdSense inter-chapter ad container when enabled."""
    if not ENABLE_MANUAL_AD_SLOTS:
        return ""
    escaped_label = html.escape(slot_label)
    return f"""
      <aside class="ad-slot-card" aria-label="{escaped_label}">
        <div class="ad-slot-label">ADVERTISEMENT ・ 贊助廣告（{escaped_label}）</div>
        <div class="ad-slot-inner">
          <ins class="adsbygoogle"
               style="display:block; text-align:center;"
               data-ad-client="{ADSENSE_CLIENT_ID}"
               data-ad-slot="{ADSENSE_IN_ARTICLE_SLOT_ID}"
               data-ad-layout="in-article"
               data-ad-format="fluid"
               data-full-width-responsive="true"></ins>
          <script>
               (adsbygoogle = window.adsbygoogle || []).push({{}});
          </script>
        </div>
      </aside>"""


def render_json_ld_script(payload: dict[str, Any]) -> str:
    """Serialize structured data safely via json.dumps to prevent broken JSON quotes."""
    serialized = json.dumps(payload, ensure_ascii=False, indent=2)
    indented = "\n".join(f"  {line}" for line in serialized.splitlines())
    return f'  <script type="application/ld+json">\n{indented}\n  </script>'


def build_index_json_ld(chapters: Sequence[ChapterSpec], chapter_titles_short: str) -> dict[str, Any]:
    """Build Schema.org Course JSON-LD with hasPart linking to all standalone chapter TechArticles."""
    has_part = [
        {
            "@type": "TechArticle",
            "@id": f"https://learn.ai-purplemaple.com/{ch.id}.html#article",
            "headline": f"{ch.badge} {ch.title}",
            "url": f"https://learn.ai-purplemaple.com/{ch.id}.html",
        }
        for ch in chapters
    ]
    return {
        "@context": "https://schema.org",
        "@type": "Course",
        "@id": "https://learn.ai-purplemaple.com/#course",
        "name": "從零開始寫程式，輕鬆搞懂資料結構、演算法",
        "description": f"紫楓（AI王紫楓 / Purple Maple）開設之 Python 3.12 資料結構、演算法與物件導向實戰教學課程，涵蓋 {chapter_titles_short}。",
        "url": "https://learn.ai-purplemaple.com/",
        "inLanguage": "zh-TW",
        "dateModified": SITE_LASTMOD,
        "isPartOf": {
            "@type": "WebSite",
            "@id": "https://ai-purplemaple.com/#website",
            "name": "紫楓｜AI王紫楓 (Purple Maple) 官方網站",
            "url": "https://ai-purplemaple.com/",
        },
        "provider": {
            "@type": "Person",
            "@id": "https://ai-purplemaple.com/#creator",
            "name": "紫楓 (AI王紫楓 / Purple Maple)",
            "url": "https://ai-purplemaple.com/",
            "sameAs": [
                "https://x.com/tbpfs1",
                "https://www.facebook.com/tbpfs2/",
                "https://www.tiktok.com/@ai_purple_maple",
                "https://www.linkedin.com/in/tbpfs2/",
                "https://portaly.cc/tbpfs",
                "https://blog.ai-purplemaple.com/",
                "https://open.spotify.com/artist/7D7CLJoxLhsMos8xI9H2kx",
                "https://music.apple.com/tw/artist/purple-maple/1745241062",
                "https://music.youtube.com/channel/UCcEBgbHV3rcee1FfgfHXprw",
                "https://www.youtube.com/@PurpleMapleAI",
                "https://www.pixiv.net/users/3503246",
                "https://github.com/tbpfs",
            ],
        },
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [".aeo-capsule", "header.hero h1"],
        },
        "hasPart": has_part,
    }


def build_chapter_json_ld(ch: ChapterSpec) -> dict[str, Any]:
    """Build per-chapter Schema.org @graph with TechArticle, VideoObject, FAQPage, and BreadcrumbList."""
    ch_url = f"https://learn.ai-purplemaple.com/{ch.id}.html"
    creator_ref = {
        "@type": "Person",
        "@id": "https://ai-purplemaple.com/#creator",
        "name": "紫楓 (AI王紫楓 / Purple Maple)",
        "url": "https://ai-purplemaple.com/",
        "sameAs": [
            "https://x.com/tbpfs1",
            "https://www.facebook.com/tbpfs2/",
            "https://www.tiktok.com/@ai_purple_maple",
            "https://www.linkedin.com/in/tbpfs2/",
            "https://portaly.cc/tbpfs",
            "https://blog.ai-purplemaple.com/",
            "https://open.spotify.com/artist/7D7CLJoxLhsMos8xI9H2kx",
            "https://music.apple.com/tw/artist/purple-maple/1745241062",
            "https://music.youtube.com/channel/UCcEBgbHV3rcee1FfgfHXprw",
            "https://www.youtube.com/@PurpleMapleAI",
            "https://www.pixiv.net/users/3503246",
            "https://github.com/tbpfs",
        ],
    }
    yt_meta = CHAPTER_YOUTUBE_VIDEOS.get(ch.id, CHAPTER_YOUTUBE_VIDEOS["ch01"])
    vid_id = yt_meta["video_id"]
    video_node = {
        "@type": "VideoObject",
        "@id": f"{ch_url}#video",
        "name": yt_meta["title"],
        "description": f"紫楓（AI王紫楓 / Purple Maple）IT 鐵人賽實戰教學影片：{ch.badge} {ch.title}。{ch.summary}",
        "thumbnailUrl": [
            f"https://i.ytimg.com/vi/{vid_id}/maxresdefault.jpg",
            f"https://i.ytimg.com/vi/{vid_id}/hqdefault.jpg",
        ],
        "uploadDate": yt_meta["upload_date"],
        "inLanguage": "zh-TW",
        "contentUrl": f"https://www.youtube.com/watch?v={vid_id}",
        "embedUrl": f"https://www.youtube.com/embed/{vid_id}",
        "author": creator_ref,
        "publisher": creator_ref,
    }
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TechArticle",
                "@id": f"{ch_url}#article",
                "headline": f"{ch.badge} {ch.title} — Python 3.12 資料結構與演算法深度講義",
                "description": f"紫楓（AI王紫楓 / Purple Maple）Python 3.12 教學講義：{ch.badge} {ch.title}。{ch.summary}",
                "url": ch_url,
                "mainEntityOfPage": ch_url,
                "image": "https://ai-purplemaple.com/assets/gallery/aily_03.jpg",
                "datePublished": "2026-03-01",
                "dateModified": ch.lastmod,
                "inLanguage": "zh-TW",
                "proficiencyLevel": "Beginner to Intermediate",
                "dependencies": "Python 3.12",
                "keywords": ", ".join(ch.keywords),
                "author": creator_ref,
                "publisher": creator_ref,
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": [".aeo-capsule", "header.hero h1"],
                },
                "video": {"@id": f"{ch_url}#video"},
                "isPartOf": {
                    "@type": "Course",
                    "@id": "https://learn.ai-purplemaple.com/#course",
                    "name": "從零開始寫程式，輕鬆搞懂資料結構、演算法",
                    "url": "https://learn.ai-purplemaple.com/",
                },
            },
            video_node,
            {
                "@type": "FAQPage",
                "@id": f"{ch_url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": faq.question,
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": faq.answer,
                        },
                    }
                    for faq in ch.interview_faqs
                ],
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{ch_url}#breadcrumb",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Python 資料結構與演算法總目錄",
                        "item": "https://learn.ai-purplemaple.com/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": f"{ch.badge} {ch.title}",
                        "item": ch_url,
                    },
                ],
            },
        ],
    }


def render_video_lecture_section(ch: ChapterSpec) -> str:
    """Render an embedded 16:9 YouTube lecture player and supplementary video links for the chapter."""
    yt_meta = CHAPTER_YOUTUBE_VIDEOS.get(ch.id, CHAPTER_YOUTUBE_VIDEOS["ch01"])
    vid_id = yt_meta["video_id"]
    vid_title = html.escape(yt_meta["title"])
    views_label = html.escape(yt_meta["views_label"])
    related_items = "\n".join(
        f'          <li>▶ <a href="https://www.youtube.com/watch?v={r_id}" target="_blank" rel="noopener noreferrer">{html.escape(r_title)}</a></li>'
        for r_id, r_title in yt_meta.get("related", [])
    )
    related_block = (
        f"""
        <div class="concepts-box" style="margin-top: 1rem; margin-bottom: 0;">
          <h3>本章延伸 YouTube 鐵人賽專題教學影片</h3>
          <ul>
{related_items}
          </ul>
        </div>"""
        if related_items
        else ""
    )
    return f"""
      <section class="chapter-card" id="video-lecture">
        <h2>本章對應 YouTube 實戰教學影片（{views_label}）</h2>
        <p class="chapter-summary">建議先觀看紫楓 IT 鐵人賽對應影片建立直覺圖像記憶，再對照下方複雜度表與 Python 3.12 標準庫程式碼動手實作：</p>
        <div class="video-embed-container" style="position: relative; width: 100%; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 6px; border: 1px solid var(--border); background: var(--code-bg);">
          <iframe
            src="https://www.youtube.com/embed/{vid_id}"
            title="{vid_title}"
            loading="lazy"
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            referrerpolicy="strict-origin-when-cross-origin"
            allowfullscreen></iframe>
        </div>
        <div class="meta-bar" style="margin-top: 0.85rem; margin-bottom: 0;">
          <span><strong>主講影片：</strong><a href="https://www.youtube.com/watch?v={vid_id}" target="_blank" rel="noopener noreferrer">{vid_title}</a></span>
          <span><a href="https://www.youtube.com/playlist?list=PLhxdaTcUMi3nRM5mtOdQgO4VEtAEsTiYd" target="_blank" rel="noopener noreferrer">31 集完整鐵人賽播放清單 ↗</a></span>
        </div>{related_block}
      </section>"""


def render_comparison_table(table: ComparisonTable) -> str:
    """Render an accessible, mobile-scrollable HTML comparison table."""
    ths = "".join(f'<th scope="col">{html.escape(h)}</th>' for h in table.headers)
    body_rows: list[str] = []
    for row in table.rows:
        first_cell = f'<th scope="row">{html.escape(row[0])}</th>'
        other_cells = "".join(f"<td>{html.escape(cell)}</td>" for cell in row[1:])
        body_rows.append(f"              <tr>{first_cell}{other_cells}</tr>")
    rows_html = "\n".join(body_rows)
    return f"""
        <div class="table-responsive">
          <table class="comparison-table">
            <caption>{html.escape(table.caption)}</caption>
            <thead>
              <tr>{ths}</tr>
            </thead>
            <tbody>
{rows_html}
            </tbody>
          </table>
        </div>"""


def render_walkthrough(ch: ChapterSpec) -> str:
    """Render step-by-step memory & pointer state walkthrough cards."""
    steps_html: list[str] = []
    for step in ch.walkthrough_steps:
        steps_html.append(
            f"""
          <div class="step-card">
            <div class="step-title">{html.escape(step.step_label)}</div>
            <div class="state-pill"><code>{html.escape(step.state_snapshot)}</code></div>
            <p class="step-desc">{html.escape(step.explanation)}</p>
          </div>"""
        )
    return f"""
      <section class="chapter-card" id="walkthrough">
        <h2>{html.escape(ch.walkthrough_title)}</h2>
        <div class="walkthrough-grid">
{"".join(steps_html)}
        </div>
      </section>"""


def render_pitfalls(ch: ChapterSpec) -> str:
    """Render CPython 3.12 runtime internals & common implementation pitfalls."""
    items_html: list[str] = []
    for pf in ch.pitfalls:
        items_html.append(
            f"""
          <div class="pitfall-card">
            <h3>{html.escape(pf.title)}</h3>
            <p class="pitfall-symptom"><strong>常見錯誤現象：</strong>{html.escape(pf.symptom)}</p>
            <p class="pitfall-fix"><strong>CPython 底層根因與正確對策：</strong>{html.escape(pf.root_cause_and_fix)}</p>
          </div>"""
        )
    return f"""
      <section class="chapter-card" id="pitfalls">
        <h2>Python 3.12 底層實作原理與常見實戰陷阱</h2>
        <div class="pitfall-list">
{"".join(items_html)}
        </div>
      </section>"""


def render_interview_section(ch: ChapterSpec) -> str:
    """Render LeetCode problem mapping table and expandable interview FAQs."""
    lc_rows: list[str] = []
    for lc in ch.leetcode_problems:
        lc_rows.append(
            f"              <tr>"
            f'<th scope="row">LeetCode #{lc.number}</th>'
            f"<td>{html.escape(lc.title)}</td>"
            f"<td><span class=\"diff-badge\">{html.escape(lc.difficulty)}</span></td>"
            f"<td>{html.escape(lc.pattern)}</td>"
            f"</tr>"
        )
    lc_rows_html = "\n".join(lc_rows)

    faq_items: list[str] = []
    for faq_idx, faq in enumerate(ch.interview_faqs):
        open_attr = " open" if faq_idx == 0 else ""
        faq_items.append(
            f"""
          <details class="faq-item"{open_attr}>
            <summary>Q. {html.escape(faq.question)}</summary>
            <div class="faq-answer">
              <p>{html.escape(faq.answer)}</p>
            </div>
          </details>"""
        )

    return f"""
      <section class="chapter-card" id="interview-faq">
        <h2>LeetCode 經典必刷題號與軟體工程師技術面試 FAQ</h2>
        <div class="table-responsive">
          <table class="comparison-table">
            <caption>{html.escape(ch.badge)} 對應 LeetCode 必考白板題與解題模板</caption>
            <thead>
              <tr>
                <th scope="col">題號</th>
                <th scope="col">題目名稱</th>
                <th scope="col">難度</th>
                <th scope="col">核心解題模式與複雜度</th>
              </tr>
            </thead>
            <tbody>
{lc_rows_html}
            </tbody>
          </table>
        </div>
        <div class="faq-list">
{"".join(faq_items)}
        </div>
      </section>"""


def render_feedback_section(ch: ChapterSpec) -> str:
    """Render minimalist helpfulness vote + collapsed private Q&A box on standalone chapter pages."""
    return f"""
      <section class="chapter-card fb-box" id="fbBox" data-chapter="{html.escape(ch.id)}">
        <div class="fb-row">
          <span class="fb-q">這篇講義對你有幫助嗎？</span>
          <div class="fb-btns">
            <button class="fb-chip" type="button" data-fb-vote="1" aria-pressed="false">✓ 有幫助</button>
            <button class="fb-chip" type="button" data-fb-vote="-1" aria-pressed="false">待改進</button>
          </div>
        </div>
        <form class="fb-note" id="fbNoteForm" hidden autocomplete="off">
          <input id="fbNoteInput" maxlength="200" placeholder="選填：哪一段清楚或卡關？（最多 200 字，不公開）" aria-label="選填原因（不公開）">
          <input class="fb-hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
          <button class="btn btn-secondary" id="fbNoteBtn" type="submit">送出回饋</button>
        </form>
        <p class="fb-status" id="fbStatus" aria-live="polite"></p>
        <details class="fb-ask">
          <summary>還有程式觀念卡關？匿名提問給紫楓（整理進本章 FAQ）</summary>
          <p class="fb-ask-sub">為維持閱讀版面純淨、杜絕廣告留言，提問不會直接公開；站長審閱後會將高頻問題補入本章技術 FAQ。</p>
          <form class="fb-ask-form" id="askForm" autocomplete="off">
            <textarea id="askInput" rows="3" maxlength="400" placeholder="輸入你的疑問，例如：為什麼這段時間複雜度是 O(log n)…" aria-label="匿名提問內容" required></textarea>
            <input class="fb-hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
            <div class="fb-ask-foot">
              <button class="btn btn-primary" id="askSendBtn" type="submit">送出提問</button>
              <span class="fb-status" id="askStatus" aria-live="polite"></span>
            </div>
          </form>
        </details>
      </section>"""


def render_deep_dive_callout(ch: ChapterSpec) -> str:
    """Render an asymmetric information-gain callout on index.html linking to the standalone deep-dive page."""
    faq_previews = "\n".join(
        f'            <li><a href="{ch.id}.html#interview-faq">{html.escape(faq.question)}</a></li>'
        for faq in ch.interview_faqs
    )
    lc_badges = " ・ ".join(f"LeetCode #{lc.number}" for lc in ch.leetcode_problems)
    return f"""
        <details class="deep-dive-callout">
          <summary class="deep-dive-callout-header">
            <strong>{html.escape(ch.badge)} 獨立深度講義獨家收錄內容（點擊展開／收合預覽）</strong>
            <span class="lc-tag-row">{html.escape(lc_badges)}</span>
          </summary>
          <p class="deep-dive-table-hint"><strong>完整結構化對照表：</strong><a href="{ch.id}.html#comparison">{html.escape(ch.comparison_table.caption)}</a></p>
          <p class="deep-dive-table-hint"><strong>本章軟體工程師面試必考問答預告：</strong></p>
          <ul class="deep-dive-faq-preview">
{faq_previews}
          </ul>
          <div class="deep-dive-action">
            <a class="btn btn-primary" href="{ch.id}.html">閱讀 {html.escape(ch.badge)} 完整深度講義（複雜度表 ＋ 逐步圖解 ＋ 面試詳解） →</a>
          </div>
        </details>"""


def render_affiliate_resources_section() -> str:
    """Render centralized hot-swappable book & course comparison table with transparent disclosure."""
    rows_html: list[str] = []
    for item in get_learning_resources():
        rel_val = "sponsored noopener noreferrer" if item.is_sponsored else "noopener noreferrer"
        rows_html.append(
            f"""              <tr>
                <td><strong>{html.escape(item.title)}</strong></td>
                <td>{html.escape(item.partner_label)}</td>
                <td>{html.escape(item.audience)}</td>
                <td>{html.escape(item.highlight)}</td>
                <td><a class="btn btn-secondary aff-btn" href="{html.escape(item.url)}" target="_blank" rel="{rel_val}" data-affiliate-partner="{html.escape(item.partner_id)}" data-affiliate-placement="index_table">{html.escape(item.cta_label)}</a></td>
              </tr>"""
        )
    rows_block = "\n".join(rows_html)
    return f"""
      <section class="study-guide-card affiliate-card" id="recommended-resources">
        <h2>紫楓嚴選：Python 資料結構與演算法實體書／線上課程比較表</h2>
        <p class="affiliate-disclosure">合作揭露：以下部分連結為博客來策略聯盟（AP）或合作夥伴推廣連結，透過連結購書或報名課程不會增加您的任何費用，我們可能獲得微薄分潤以支持本站免費開源講義維護。</p>
        <div class="table-responsive">
          <table class="comparison-table">
            <thead>
              <tr>
                <th>推薦書籍／課程</th>
                <th>平台</th>
                <th>適合對象</th>
                <th>與本站章節對應重點</th>
                <th>前往查看</th>
              </tr>
            </thead>
            <tbody>
{rows_block}
            </tbody>
          </table>
        </div>
      </section>"""


def render_chapter_book_callout(ch: ChapterSpec) -> str:
    """Render a compact, zero-image contextual Books.com.tw AP reading card on standalone chapter pages."""
    label, ap_url = get_chapter_book_recommendation(ch.id)
    return f"""
      <aside class="chapter-card affiliate-chapter-card" aria-label="本章延伸書單推薦">
        <div class="aff-ch-row">
          <div>
            <strong>{html.escape(label)}</strong>
            <p class="affiliate-disclosure" style="margin: 0.3rem 0 0;">合作揭露：此為博客來策略聯盟推廣連結，購書價格與原價相同，您的支持將協助本站持續更新免費 Python 教學講義。</p>
          </div>
          <a class="btn btn-secondary aff-btn" href="{html.escape(ap_url)}" target="_blank" rel="sponsored noopener noreferrer" data-affiliate-partner="books_ap_{html.escape(ch.id)}" data-affiliate-placement="chapter_footer">前往博客來查找相關書單 ↗</a>
        </div>
      </aside>"""


def render_chapter_pager(idx: int, chapters: Sequence[ChapterSpec]) -> str:
    """Render Prev / Home (/) / Next navigation bar at the bottom of standalone chapter pages."""
    prev_ch = chapters[idx - 1] if idx > 0 else None
    next_ch = chapters[idx + 1] if idx + 1 < len(chapters) else None

    prev_html = (
        f'<a class="pager-link" href="{prev_ch.id}.html">← 上一章：{html.escape(prev_ch.badge + " " + prev_ch.title.split("（")[0])}</a>'
        if prev_ch
        else '<span class="pager-link pager-disabled">← 已是第一章</span>'
    )
    next_html = (
        f'<a class="pager-link" href="{next_ch.id}.html">下一章：{html.escape(next_ch.badge + " " + next_ch.title.split("（")[0])} →</a>'
        if next_ch
        else '<span class="pager-link pager-disabled">已是最後一章 →</span>'
    )
    return f"""
      <nav class="chapter-pager" aria-label="上下章節導覽">
        {prev_html}
        <a class="pager-link pager-home" href="/">返回全章節總目錄</a>
        {next_html}
      </nav>"""


def render_shared_styles() -> str:
    """Return shared CSS styles — O'Reilly x MIT Press Classic CS Textbook aesthetic."""
    return """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Newsreader:ital,opsz,wght@0,6..72,600;0,6..72,700;1,6..72,500&display=swap">
  <style>
    :root {
      /* O'Reilly x MIT Press Classic CS Textbook Palette */
      --bg: #f6f4ef;               /* Warm archival textbook paper */
      --surface: #ffffff;          /* Clean chapter sheet */
      --surface-alt: #f2efe7;      /* Soft warm marginalia inset */
      --border: #dcd5c7;           /* Archival hairline rule */
      --border-strong: #1c1917;    /* Crisp book typography rule */
      --text: #1c1917;             /* Rich charcoal editorial ink */
      --muted: #57534e;            /* Warm stone secondary text */
      --accent: #15803d;           /* Algorithm Forest Green (Tree / Pass) */
      --accent-strong: #166534;    /* Deep Pine CTA */
      --accent-soft: #eef8f1;
      --success: #047857;          /* Verification Emerald */
      --warning: #b45309;          /* Textbook Amber Marginalia */
      --danger: #b91c1c;
      --code-bg: #161922;          /* High-contrast Dark Code Editor */
      --code-toolbar: #10131b;
      --code-text: #e6edf3;
      --code-muted: #9aa4b8;
      --code-border: #2a3040;
      --aily-split: linear-gradient(90deg, #fb7185 0% 50%, #38bdf8 50% 100%);
      --font-serif: "Newsreader", "Hiragino Mincho ProN", "Yu Mincho", "BIZ UDPMincho", "Noto Serif TC", Georgia, serif;
      --font-sans: "Hiragino Kaku Gothic ProN", "Yu Gothic", "Microsoft JhengHei", "Noto Sans TC", system-ui, -apple-system, sans-serif;
      --font-mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }
    * { box-sizing: border-box; }
    html {
      scroll-behavior: smooth;
      -webkit-font-smoothing: antialiased;
      text-rendering: optimizeLegibility;
    }
    body {
      margin: 0;
      font-family: var(--font-sans);
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.76;
      overflow-x: clip;
    }
    a {
      color: var(--accent);
      text-decoration: none;
      text-underline-offset: 3px;
    }
    a:hover {
      color: var(--accent-strong);
      text-decoration: underline;
    }
    code {
      font-family: var(--font-mono);
      font-size: 0.88em;
      background: var(--surface-alt);
      color: #14532d;
      padding: 0.12rem 0.38rem;
      border-radius: 3px;
      border: 1px solid #e4ded2;
    }
    pre code {
      background: transparent;
      color: inherit;
      padding: 0;
      border: none;
      font-size: inherit;
    }
    .container {
      max-width: 960px;
      margin: 0 auto;
      padding: 2.5rem 1.35rem 4rem;
    }

    /* Book Cover Masthead Hero */
    header.hero {
      background: var(--surface);
      border: 1px solid var(--border);
      border-top: 3px solid var(--border-strong);
      border-left: 6px solid var(--accent);
      border-radius: 4px;
      padding: 2.25rem 2.15rem;
      margin-bottom: 2.25rem;
      box-shadow: 0 2px 10px rgba(28, 25, 23, 0.04);
    }
    .hero-eyebrow {
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      color: var(--accent-strong);
      background: var(--accent-soft);
      border: 1px solid #b6e0c5;
      padding: 0.22rem 0.65rem;
      border-radius: 3px;
      margin-bottom: 0.85rem;
    }
    .hero h1 {
      margin: 0 0 0.85rem;
      font-family: var(--font-serif);
      font-size: clamp(1.65rem, 3.2vw, 2.35rem);
      font-weight: 700;
      line-height: 1.28;
      letter-spacing: -0.01em;
      color: var(--text);
    }
    .hero p {
      margin: 0.5rem 0;
      color: var(--muted);
      font-size: 0.98rem;
    }
    .cta-group {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-top: 1.5rem;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.45rem;
      padding: 0.62rem 1.15rem;
      min-height: 44px;
      border-radius: 4px;
      border: 1.5px solid transparent;
      font-family: inherit;
      font-weight: 700;
      font-size: 0.9rem;
      cursor: pointer;
      transition: background-color 0.16s ease, color 0.16s ease, border-color 0.16s ease, transform 0.16s ease;
    }
    .btn:disabled {
      opacity: 0.55;
      cursor: not-allowed;
    }
    .btn:hover {
      transform: translateY(-1px);
      text-decoration: none;
    }
    .btn-primary {
      background: var(--accent-strong);
      border-color: var(--accent-strong);
      color: #ffffff;
    }
    .btn-primary:hover {
      background: var(--text);
      border-color: var(--text);
      color: #ffffff;
    }
    .btn-secondary {
      background: var(--surface);
      color: var(--text);
      border: 1.5px solid var(--border-strong);
    }
    .btn-secondary:hover {
      background: var(--text);
      color: #ffffff;
    }

    /* Syllabus Table of Contents */
    nav.toc, nav.chapter-switcher {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(235px, 1fr));
      gap: 0.85rem;
      margin-bottom: 1.85rem;
    }
    .toc-item {
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 3px solid var(--border);
      border-radius: 4px;
      padding: 0.95rem 1.1rem;
      display: block;
      transition: border-color 0.16s ease, background-color 0.16s ease;
    }
    .toc-item:hover {
      border-color: var(--accent);
      border-left-color: var(--accent);
      background: var(--accent-soft);
      text-decoration: none;
    }
    .toc-item[aria-current="page"] {
      border-color: var(--accent);
      border-left: 4px solid var(--accent-strong);
      background: var(--accent-soft);
    }
    .toc-item strong {
      display: block;
      color: var(--text);
      margin-top: 0.25rem;
      font-size: 0.94rem;
      line-height: 1.45;
    }
    .section-subnav {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.55rem;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 0.75rem 1rem;
      margin-bottom: 2rem;
      font-size: 0.86rem;
    }
    .section-subnav a {
      padding: 0.3rem 0.7rem;
      border-radius: 3px;
      background: var(--surface-alt);
      border: 1px solid var(--border);
      color: var(--text);
      font-weight: 600;
    }
    .section-subnav a:hover {
      background: var(--accent-strong);
      border-color: var(--accent-strong);
      color: #ffffff;
      text-decoration: none;
    }

    /* Textbook Chapter Cards */
    .chapter-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-top: 2.5px solid var(--border-strong);
      border-radius: 4px;
      padding: 1.85rem 2rem;
      margin-bottom: 2rem;
    }
    .chapter-card h2 {
      margin: 0 0 1rem;
      font-family: var(--font-serif);
      font-size: 1.38rem;
      font-weight: 700;
      color: var(--text);
      line-height: 1.35;
    }
    .chapter-header {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-bottom: 0.7rem;
      padding-bottom: 0.65rem;
      border-bottom: 1px solid var(--border);
    }
    .badge {
      font-family: var(--font-mono);
      background: var(--accent-strong);
      color: #ffffff;
      border: 1px solid var(--accent-strong);
      padding: 0.16rem 0.6rem;
      border-radius: 3px;
      font-weight: 600;
      font-size: 0.78rem;
      letter-spacing: 0.04em;
    }
    .chapter-header h2 {
      margin: 0;
      font-size: 1.38rem;
    }
    .chapter-summary, .deep-intro-text {
      color: var(--muted);
      margin: 0.55rem 0 1.2rem;
      font-size: 0.98rem;
      line-height: 1.78;
    }
    .meta-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 1.2rem;
      font-size: 0.88rem;
      color: var(--muted);
      background: var(--surface-alt);
      border: 1px solid var(--border);
      padding: 0.65rem 1rem;
      border-radius: 4px;
      margin-bottom: 1.05rem;
    }

    /* Academic Complexity & Comparison Tables */
    .table-responsive {
      width: 100%;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      margin: 1rem 0 1.4rem;
      border: 1px solid var(--border);
      border-top: 2px solid var(--border-strong);
      border-radius: 3px;
      background: var(--surface);
    }
    table.comparison-table {
      width: 100%;
      min-width: 560px;
      border-collapse: collapse;
      font-size: 0.9rem;
      text-align: left;
      font-variant-numeric: tabular-nums;
    }
    table.comparison-table caption {
      caption-side: top;
      text-align: left;
      padding: 0.78rem 1rem;
      font-family: var(--font-serif);
      font-weight: 700;
      font-size: 0.98rem;
      color: var(--text);
      border-bottom: 1px solid var(--border);
      background: var(--surface-alt);
    }
    table.comparison-table th,
    table.comparison-table td {
      padding: 0.74rem 1rem;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
      color: var(--muted);
    }
    table.comparison-table thead th {
      font-family: var(--font-mono);
      font-size: 0.8rem;
      color: var(--text);
      background: #ede9df;
      border-bottom: 1.5px solid var(--border-strong);
      font-weight: 600;
    }
    table.comparison-table tbody th {
      color: var(--text);
      font-weight: 700;
      width: 24%;
    }
    table.comparison-table tbody tr:hover td,
    table.comparison-table tbody tr:hover th {
      background: #faf9f5;
    }
    .diff-badge {
      display: inline-block;
      padding: 0.12rem 0.52rem;
      border-radius: 3px;
      font-family: var(--font-mono);
      font-size: 0.75rem;
      font-weight: 600;
      background: var(--accent-soft);
      color: var(--accent-strong);
      border: 1px solid #b6e0c5;
    }

    /* Step-by-Step Algorithm Walkthrough */
    .walkthrough-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 0.95rem;
    }
    .step-card {
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-left: 4px solid var(--accent);
      border-radius: 4px;
      padding: 1.05rem 1.25rem;
    }
    .step-title {
      font-weight: 700;
      color: var(--text);
      margin-bottom: 0.5rem;
    }
    .state-pill {
      background: var(--code-bg);
      border: 1px solid var(--code-border);
      border-radius: 4px;
      padding: 0.5rem 0.8rem;
      margin-bottom: 0.55rem;
      font-family: var(--font-mono);
      font-size: 0.83rem;
      color: #7ee787;
      overflow-x: auto;
    }
    .step-desc {
      margin: 0;
      color: var(--muted);
      font-size: 0.93rem;
    }

    /* O'Reilly-Style Pitfall Marginalia Boxes */
    .pitfall-list {
      display: grid;
      gap: 1rem;
    }
    .pitfall-card {
      background: #fffbeb;
      border: 1px solid #e6cfa0;
      border-left: 4px solid var(--warning);
      border-radius: 4px;
      padding: 1.1rem 1.25rem;
    }
    .pitfall-card h3 {
      margin: 0 0 0.5rem;
      font-size: 1rem;
      font-weight: 700;
      color: #92400e;
    }
    .pitfall-symptom, .pitfall-fix {
      margin: 0.4rem 0 0;
      color: #44403c;
      font-size: 0.92rem;
    }

    /* FAQ & Textbook Accordions */
    .faq-list {
      display: grid;
      gap: 0;
      margin-top: 1.25rem;
      border-top: 2px solid var(--border-strong);
    }
    .faq-item {
      background: transparent;
      border: none;
      border-bottom: 1px solid var(--border);
      border-radius: 0;
      padding: 1rem 0.25rem;
    }
    .faq-item summary {
      cursor: pointer;
      font-weight: 700;
      color: var(--text);
      font-size: 0.98rem;
      list-style: none;
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 1rem;
    }
    .faq-item summary::-webkit-details-marker { display: none; }
    .faq-item summary::after {
      content: "+";
      font-family: var(--font-mono);
      color: var(--accent);
      font-size: 1.15rem;
      flex-shrink: 0;
    }
    .faq-item[open] summary { color: var(--accent-strong); }
    .faq-item[open] summary::after { content: "−"; }
    .faq-answer p {
      margin: 0.65rem 0 0;
      color: var(--muted);
      font-size: 0.94rem;
    }

    .deep-dive-callout {
      margin-top: 1.1rem;
      background: var(--accent-soft);
      border: 1px solid #b6e0c5;
      border-left: 4px solid var(--accent-strong);
      border-radius: 4px;
      padding: 0.95rem 1.2rem;
    }
    .deep-dive-callout-header {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
      cursor: pointer;
      user-select: none;
      color: var(--text);
    }
    details.deep-dive-callout[open] .deep-dive-callout-header {
      margin-bottom: 0.65rem;
    }
    .code-accordion,
    .study-guide-accordion {
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 0.9rem 1.15rem;
      margin-top: 0.8rem;
    }
    .code-accordion-summary,
    .study-guide-summary {
      cursor: pointer;
      font-weight: 700;
      font-size: 0.94rem;
      color: var(--accent-strong);
      user-select: none;
    }
    details.code-accordion[open] .code-accordion-summary,
    details.study-guide-accordion[open] .study-guide-summary {
      margin-bottom: 0.85rem;
    }
    .lc-tag-row {
      font-family: var(--font-mono);
      font-size: 0.76rem;
      font-weight: 600;
      color: var(--accent-strong);
      background: #ffffff;
      border: 1px solid #b6e0c5;
      padding: 0.16rem 0.55rem;
      border-radius: 3px;
    }
    .deep-dive-table-hint {
      margin: 0.35rem 0;
      font-size: 0.9rem;
      color: var(--muted);
    }
    .deep-dive-faq-preview {
      margin: 0.35rem 0 0.95rem;
      padding-left: 1.25rem;
      font-size: 0.89rem;
      color: var(--muted);
    }
    .deep-dive-faq-preview li {
      margin-bottom: 0.25rem;
    }
    .deep-dive-action {
      display: flex;
      justify-content: flex-start;
    }
    .chapter-pager {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 0.85rem;
      background: var(--surface);
      border: 1px solid var(--border);
      border-top: 2px solid var(--border-strong);
      border-radius: 4px;
      padding: 1.1rem 1.35rem;
      margin-top: 2rem;
    }
    .pager-link {
      font-weight: 700;
      font-size: 0.92rem;
    }
    .pager-disabled {
      color: var(--muted);
      opacity: 0.5;
    }

    /* High-Contrast Dark Code Editor & Terminal Output inside Light Textbook */
    .code-container {
      border: 1.5px solid var(--border-strong);
      border-radius: 4px;
      overflow: hidden;
      background: var(--code-bg);
      color: var(--code-text);
      margin-bottom: 1rem;
    }
    .code-toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.5rem 1rem;
      background: var(--code-toolbar);
      border-bottom: 1px solid var(--code-border);
      font-family: var(--font-mono);
      font-size: 0.8rem;
      color: var(--code-muted);
    }
    .copy-btn {
      background: #232838;
      color: #f1f5f9;
      border: 1px solid #3c455c;
      border-radius: 3px;
      padding: 0.4rem 0.85rem;
      min-height: 40px;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: background-color 0.15s ease, border-color 0.15s ease;
    }
    .copy-btn:hover {
      background: var(--accent-strong);
      border-color: var(--accent);
      color: #ffffff;
    }
    pre {
      margin: 0;
      padding: 1.05rem 1.25rem;
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      line-height: 1.62;
      color: var(--code-text);
    }
    .output-box {
      background: #10151d;
      border: 1px solid #263342;
      border-left: 4px solid #34d399;
      border-radius: 4px;
      padding: 0.8rem 1.05rem;
    }
    .output-label {
      font-family: var(--font-mono);
      font-size: 0.76rem;
      font-weight: 600;
      letter-spacing: 0.05em;
      color: #6ee7b7;
      margin-bottom: 0.4rem;
    }
    .output-pre {
      padding: 0;
      color: #d1fae5;
      background: transparent;
      font-size: 0.84rem;
    }

    /* Key Concepts Box */
    .concepts-box {
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-left: 4px solid var(--accent);
      border-radius: 4px;
      padding: 0.95rem 1.2rem;
      margin-bottom: 1.1rem;
    }
    .concepts-box h3 {
      margin: 0 0 0.5rem;
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--accent-strong);
    }
    .concepts-box ul {
      margin: 0;
      padding-left: 1.2rem;
      color: var(--muted);
      font-size: 0.92rem;
    }
    .concepts-box li {
      margin-bottom: 0.35rem;
    }

    /* AdSense Slot (Clean Archival Frame, Hides Automatically When Unfilled) */
    .ad-slot-card {
      background: var(--surface);
      border: 1px dashed var(--border);
      border-radius: 4px;
      padding: 1rem 1.25rem;
      margin: 1.75rem 0 2.25rem;
      min-height: 140px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .ad-slot-card:has(ins[data-ad-status="unfilled"]) {
      display: none;
    }
    .ad-slot-label {
      font-family: var(--font-mono);
      font-size: 0.7rem;
      letter-spacing: 0.1em;
      color: var(--muted);
      text-align: center;
      margin-bottom: 0.5rem;
      opacity: 0.75;
    }
    .ad-slot-inner {
      min-height: 90px;
      width: 100%;
    }
    .study-guide-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-top: 2.5px solid var(--border-strong);
      border-radius: 4px;
      padding: 1.85rem 2rem;
      margin-top: 2rem;
      margin-bottom: 2rem;
    }
    .study-guide-card h2 {
      margin-top: 0;
      font-family: var(--font-serif);
      font-size: 1.35rem;
      color: var(--text);
    }
    .study-guide-card p, .study-guide-card li {
      color: var(--muted);
      font-size: 0.95rem;
    }

    /* Textbook Colophon Footer with Aily 2px Heterochromia Top Edge */
    .privacy-policy-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 3px solid var(--accent);
      border-radius: 4px;
      padding: 1.2rem 1.45rem;
      margin-bottom: 1.5rem;
      text-align: left;
    }
    .privacy-policy-card h3 {
      margin: 0 0 0.5rem;
      font-family: var(--font-serif);
      font-size: 0.98rem;
      color: var(--text);
    }
    .privacy-policy-card p {
      margin: 0 0 0.5rem;
      font-size: 0.84rem;
      line-height: 1.68;
      color: var(--muted);
    }
    footer {
      text-align: center;
      color: var(--muted);
      font-size: 0.86rem;
      margin-top: 3rem;
      padding-top: 1.75rem;
      border-top: 2px solid transparent;
      border-image: var(--aily-split) 1;
    }

    /* Anonymous Feedback & Private Q&A Widget (Crisp Light Textbook Inputs) */
    .fb-hp {
      position: absolute !important;
      width: 1px;
      height: 1px;
      overflow: hidden;
      clip: rect(0 0 0 0);
      white-space: nowrap;
      left: -9999px;
    }
    .fb-box {
      padding: 1.35rem 1.65rem;
    }
    .fb-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
      flex-wrap: wrap;
    }
    .fb-q {
      font-weight: 700;
      font-size: 0.98rem;
      color: var(--text);
    }
    .fb-btns {
      display: flex;
      gap: 0.55rem;
      flex-wrap: wrap;
    }
    .fb-chip {
      min-height: 40px;
      padding: 0 1rem;
      border-radius: 4px;
      border: 1.5px solid var(--border);
      background: var(--surface-alt);
      color: var(--text);
      font: inherit;
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      transition: border-color 0.15s ease, background-color 0.15s ease;
    }
    .fb-chip:hover {
      border-color: var(--accent);
      background: var(--accent-soft);
    }
    .fb-chip.on.up {
      background: var(--accent-soft);
      border-color: var(--accent);
      color: var(--accent-strong);
    }
    .fb-chip.on.down {
      background: #fef2f2;
      border-color: var(--danger);
      color: #991b1b;
    }
    .fb-note {
      display: flex;
      gap: 0.6rem;
      margin-top: 0.85rem;
      flex-wrap: wrap;
    }
    .fb-note[hidden] {
      display: none;
    }
    .fb-note input {
      flex: 1;
      min-width: min(100%, 190px);
      height: 42px;
      padding: 0 0.9rem;
      border-radius: 4px;
      border: 1.5px solid var(--border);
      background: var(--surface);
      color: var(--text);
      font: inherit;
      font-size: 0.9rem;
    }
    .fb-status {
      margin: 0.55rem 0 0;
      font-size: 0.86rem;
      font-weight: 600;
      color: var(--success);
      min-height: 1.1em;
    }
    .fb-status.err {
      color: var(--danger);
    }
    .fb-ask {
      margin-top: 0.95rem;
      padding-top: 0.9rem;
      border-top: 1px solid var(--border);
      font-size: 0.92rem;
    }
    .fb-ask summary {
      cursor: pointer;
      color: var(--accent-strong);
      font-weight: 700;
    }
    .fb-ask-sub {
      margin: 0.55rem 0 0.7rem;
      font-size: 0.85rem;
      color: var(--muted);
    }
    .fb-ask-form textarea {
      width: 100%;
      padding: 0.65rem 0.9rem;
      border-radius: 4px;
      border: 1.5px solid var(--border);
      background: var(--surface);
      color: var(--text);
      font: inherit;
      font-size: 0.92rem;
      resize: vertical;
    }
    .fb-ask-foot {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-top: 0.65rem;
      flex-wrap: wrap;
    }

    /* Key Takeaway / AEO Definition Capsule */
    .aeo-capsule {
      background: var(--accent-soft);
      border: 1px solid #b6e0c5;
      border-left: 4px solid var(--accent-strong);
      border-radius: 4px;
      padding: 0.95rem 1.2rem;
      margin: 0 0 1.5rem;
      font-size: 0.95rem;
      color: var(--text);
      line-height: 1.75;
    }
    .aeo-capsule strong { color: var(--accent-strong); }
    .affiliate-disclosure {
      font-size: 0.84rem;
      color: var(--muted);
      margin: 0.25rem 0 0.9rem;
    }
    .aff-btn {
      white-space: nowrap;
      padding: 0.45rem 0.9rem;
      font-size: 0.85rem;
    }
    .aff-ch-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      flex-wrap: wrap;
    }
    @media (max-width: 640px) {
      .container {
        padding: 1.5rem 1rem 3rem;
      }
      header.hero,
      .chapter-card,
      .study-guide-card {
        padding: 1.35rem 1.15rem;
      }
      .fb-note input,
      .fb-ask-form textarea {
        font-size: 16px;
      }
    }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }
    }
  </style>"""


def render_footer() -> str:
    """Render shared privacy policy & ecosystem footer."""
    return """    <footer id="privacy">
      <div class="privacy-policy-card">
        <h3>隱私權政策與 Cookie 聲明 (Privacy Policy)</h3>
        <p>本網站（learn.ai-purplemaple.com）使用 Google AdSense 第三方廣告服務與 Google Analytics (GA4)／Google Tag Manager 網站流量分析服務。Google 及其合作夥伴會使用 Cookie（包含 DART Cookie），根據使用者造訪本站或其他網站的紀錄提供個人化廣告與匿名流量統計。您可隨時前往 <a href="https://adssettings.google.com/" target="_blank" rel="noopener noreferrer">Google 廣告設定頁面</a> 停用個人化廣告，或查閱 <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener noreferrer">Google 廣告與隱私權政策</a>。本站程式碼複製功能均於瀏覽器本機執行；讀者於章節講義點擊「有幫助／待改進」或提交私密提問時，僅透過加密安全通道傳送匿名回饋內容與 HMAC 雜湊限流識別，絕不公開顯示留言或儲存原始 IP。</p>
      </div>
      <p>Created by <strong><a href="https://ai-purplemaple.com/" target="_blank" rel="noopener noreferrer" style="color: var(--accent);">紫楓 (AI王紫楓 / Purple Maple)</a></strong> ・ <a href="https://blog.ai-purplemaple.com/" target="_blank" rel="noopener noreferrer" style="color: var(--muted);">紫楓技術與創作日誌</a> ・ <a href="https://github.com/tbpfs/learning" target="_blank" rel="noopener noreferrer" style="color: var(--muted);">GitHub 原始碼</a> ・ Powered by Python 3.12 &amp; GitHub Pages ・ <a href="ads.txt">ads.txt</a></p>
    </footer>"""


def render_copy_script(*, include_cms_fetch: bool) -> str:
    """Render copy button handler and (on index.html only) the CMS dynamic tutorials loader."""
    cms_block = ""
    if include_cms_fetch:
        cms_block = """
    if (typeof fetch === 'function') {
      fetch('https://ai-purplemaple.com/api/v1/content')
        .then(function (r) { return r && r.ok ? r.json() : null; })
        .then(function (payload) {
          if (!payload || !payload.ok || !payload.content || !Array.isArray(payload.content.tutorials) || payload.content.tutorials.length === 0) return;
          var container = document.getElementById('cms-tutorials-container');
          if (!container) return;
          payload.content.tutorials.forEach(function (tut, idx) {
            var sec = document.createElement('section');
            sec.className = 'chapter-card';
            var codeId = 'cms-code-' + idx;
            var header = document.createElement('div');
            header.className = 'chapter-header';
            var badge = document.createElement('span');
            badge.className = 'badge';
            badge.textContent = tut.category || '補充講義';
            var h2 = document.createElement('h2');
            h2.textContent = tut.title || '';
            header.appendChild(badge);
            header.appendChild(h2);

            var pSum = document.createElement('p');
            pSum.className = 'chapter-summary';
            pSum.textContent = (tut.summary || '') + (tut.explanation ? ' — ' + tut.explanation : '');

            var compRow = document.createElement('div');
            compRow.className = 'meta-bar';
            var pill = document.createElement('span');
            pill.textContent = tut.complexity || '時間 O(n) / 空間 O(1)';
            compRow.appendChild(pill);

            var wrap = document.createElement('div');
            wrap.className = 'code-container';
            var bar = document.createElement('div');
            bar.className = 'code-toolbar';
            var fnSpan = document.createElement('span');
            fnSpan.textContent = (tut.id || 'supplement_note') + '.py';
            var cpBtn = document.createElement('button');
            cpBtn.type = 'button';
            cpBtn.className = 'copy-btn';
            cpBtn.setAttribute('data-target', codeId);
            cpBtn.textContent = '複製程式碼';
            bar.appendChild(fnSpan);
            bar.appendChild(cpBtn);

            var pre = document.createElement('pre');
            var code = document.createElement('code');
            code.id = codeId;
            code.textContent = tut.code_python || '';
            pre.appendChild(code);
            wrap.appendChild(bar);
            wrap.appendChild(pre);

            sec.appendChild(header);
            sec.appendChild(pSum);
            sec.appendChild(compRow);
            sec.appendChild(wrap);
            container.appendChild(sec);
          });
          bindCopyButtons();
        })
        .catch(function () {});
    }"""

    return f"""  <script>
    function bindCopyButtons() {{
      document.querySelectorAll('.copy-btn').forEach(function (btn) {{
        if (btn.getAttribute('data-bound') === '1') return;
        btn.setAttribute('data-bound', '1');
        btn.addEventListener('click', function () {{
          var targetId = btn.getAttribute('data-target');
          var codeEl = document.getElementById(targetId);
          if (!codeEl || !navigator.clipboard) return;
          navigator.clipboard.writeText(codeEl.textContent || '').then(function () {{
            var orig = btn.textContent;
            btn.textContent = '已複製 ✓';
            if (typeof window.gtag === 'function') {{
              window.gtag('event', 'copy_code', {{ chapter_target: targetId }});
            }}
            setTimeout(function () {{ btn.textContent = orig; }}, 1500);
          }});
        }});
      }});
    }}
    bindCopyButtons();
    document.querySelectorAll('[data-affiliate-partner]').forEach(function (el) {{
      el.addEventListener('click', function () {{
        if (typeof window.gtag === 'function') {{
          window.gtag('event', 'affiliate_click', {{
            partner: el.getAttribute('data-affiliate-partner') || '',
            site: 'learn',
            placement: el.getAttribute('data-affiliate-placement') || 'unknown'
          }});
        }}
      }});
    }});
    (function () {{
      var fbBox = document.getElementById('fbBox');
      if (!fbBox || typeof fetch !== 'function') return;
      var chId = fbBox.getAttribute('data-chapter') || '';
      var apiBase = 'https://ai-purplemaple.com';
      var fbKey = 'learnFb:' + chId;
      var curVote = 0;

      function setStatus(el, msg, isErr) {{
        if (!el) return;
        el.classList.toggle('err', Boolean(isErr));
        el.textContent = msg || '';
      }}

      function errText(code) {{
        if (code === 'rate_limited') return '今天的次數已用完，明天再來';
        if (code === 'too_short') return '請至少輸入 5 個字描述你的疑問';
        if (code === 'too_long') return '字數請控制在 400 字以內';
        return '送出失敗，請稍後再試';
      }}

      function setFbBtns(v) {{
        curVote = v;
        fbBox.querySelectorAll('[data-fb-vote]').forEach(function (b) {{
          var bv = Number(b.getAttribute('data-fb-vote'));
          var on = bv === v;
          b.classList.toggle('on', on);
          b.classList.toggle('up', bv === 1 && on);
          b.classList.toggle('down', bv === -1 && on);
          b.setAttribute('aria-pressed', on ? 'true' : 'false');
        }});
      }}

      function postJson(path, body) {{
        return fetch(apiBase + path, {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify(body)
        }}).then(function (r) {{
          return r.json().catch(function () {{ return {{}}; }}).then(function (d) {{
            if (!r.ok) throw new Error((d && d.error) || 'error');
            return d;
          }});
        }});
      }}

      try {{
        var saved = Number(localStorage.getItem(fbKey) || 0);
        if (saved === 1 || saved === -1) setFbBtns(saved);
      }} catch (_) {{}}

      var fbStatus = document.getElementById('fbStatus');
      var noteForm = document.getElementById('fbNoteForm');

      fbBox.querySelectorAll('[data-fb-vote]').forEach(function (btn) {{
        btn.addEventListener('click', function () {{
          var vote = Number(btn.getAttribute('data-fb-vote'));
          var prevVote = curVote;
          if (vote === prevVote) {{
            if (noteForm) noteForm.hidden = false;
            setStatus(fbStatus, '感謝回饋！歡迎選填一句原因幫助我們補強講義。', false);
            return;
          }}
          setFbBtns(vote);
          postJson('/api/v1/learn-feedback', {{ slug: chId, vote: vote, note: '' }})
            .then(function () {{
              try {{ localStorage.setItem(fbKey, String(vote)); }} catch (_) {{}}
              if (noteForm) noteForm.hidden = false;
              setStatus(fbStatus, '感謝回饋！歡迎選填一句原因幫助我們補強講義。', false);
              if (typeof window.gtag === 'function') {{
                window.gtag('event', 'chapter_feedback', {{ chapter_id: chId, vote: vote }});
              }}
            }})
            .catch(function (err) {{
              setFbBtns(prevVote);
              setStatus(fbStatus, errText(err && err.message), true);
            }});
        }});
      }});

      if (noteForm) {{
        noteForm.addEventListener('submit', function (e) {{
          e.preventDefault();
          var inp = document.getElementById('fbNoteInput');
          var noteBtn = document.getElementById('fbNoteBtn');
          var note = ((inp && inp.value) || '').trim();
          if (!note) return;
          var hp = noteForm.elements.website ? noteForm.elements.website.value : '';
          if (noteBtn) noteBtn.disabled = true;
          postJson('/api/v1/learn-feedback', {{ slug: chId, vote: curVote || 1, note: note, website: hp }})
            .then(function () {{
              if (inp) inp.value = '';
              noteForm.hidden = true;
              setStatus(fbStatus, '✓ 已收到你的回饋，謝謝！', false);
            }})
            .catch(function (err) {{
              setStatus(fbStatus, errText(err && err.message), true);
            }})
            .finally(function () {{
              if (noteBtn) noteBtn.disabled = false;
            }});
        }});
      }}

      var askForm = document.getElementById('askForm');
      if (askForm) {{
        askForm.addEventListener('submit', function (e) {{
          e.preventDefault();
          var inp = document.getElementById('askInput');
          var askStatus = document.getElementById('askStatus');
          var askBtn = document.getElementById('askSendBtn');
          var text = ((inp && inp.value) || '').trim().replace(/\\s+/g, ' ');
          if (text.length < 5) {{
            setStatus(askStatus, errText('too_short'), true);
            if (inp) inp.focus();
            return;
          }}
          var hp = askForm.elements.website ? askForm.elements.website.value : '';
          if (askBtn) askBtn.disabled = true;
          postJson('/api/v1/learn-question', {{ slug: chId, text: text, website: hp }})
            .then(function () {{
              if (inp) inp.value = '';
              setStatus(askStatus, '✓ 已收到提問！站長整理後會補充至本章 FAQ。', false);
              if (typeof window.gtag === 'function') {{
                window.gtag('event', 'chapter_question', {{ chapter_id: chId }});
              }}
            }})
            .catch(function (err) {{
              setStatus(askStatus, errText(err && err.message), true);
            }})
            .finally(function () {{
              if (askBtn) askBtn.disabled = false;
            }});
        }});
      }}
    }})();{cms_block}
  </script>"""


def render_index_page(
    chapters: Sequence[ChapterSpec],
    exec_cache: dict[str, tuple[str, str]],
    chapter_titles_short: str,
) -> str:
    """Render the Course Hub index.html (summary cards + progressive disclosure code sandbox + deep-dive callouts)."""
    cards_html: list[str] = []
    toc_items_html: list[str] = []

    for idx, ch in enumerate(chapters, start=1):
        source_code, live_output = exec_cache[ch.id]
        escaped_code = html.escape(source_code)
        escaped_out = html.escape(live_output)
        escaped_title = html.escape(ch.title)
        escaped_summary = html.escape(ch.summary)
        escaped_complexity = html.escape(ch.complexity)
        escaped_file = html.escape(ch.file)
        concepts_items = "\n".join(f"            <li>{html.escape(pt)}</li>" for pt in ch.concepts)
        short_name = html.escape(ch.title.split("（")[0])
        open_attr = " open" if idx == 1 else ""

        toc_items_html.append(
            f"""      <a class="toc-item" href="#{ch.id}">
        <span class="badge">{ch.badge}</span>
        <strong>{short_name}</strong>
      </a>"""
        )

        cards_html.append(
            f"""
      <article class="chapter-card" id="{ch.id}">
        <div class="chapter-header">
          <span class="badge">{ch.badge}</span>
          <h2><a href="{ch.id}.html" style="color: inherit;">{escaped_title}</a></h2>
          <a href="{ch.id}.html" style="margin-left: auto; font-size: 0.86rem; font-weight: 600;">獨立章節深度講義 ↗</a>
        </div>
        <p class="chapter-summary">{escaped_summary}</p>
        <div class="concepts-box">
          <h3>核心觀念與面試重點解析</h3>
          <ul>
{concepts_items}
          </ul>
        </div>
        <div class="meta-bar">
          <span><strong>時間／空間複雜度：</strong>{escaped_complexity}</span>
          <span><strong>原始碼路徑：</strong><code>{escaped_file}</code></span>
        </div>
        <details class="code-accordion"{open_attr}>
          <summary class="code-accordion-summary">點擊展開／收合 {html.escape(ch.badge)} Python 3.12 完整實作原始碼與實機執行輸出（<code>{escaped_file}</code>）</summary>
          <div class="code-container">
            <div class="code-toolbar">
              <span>Python 3.12 範例實作（{escaped_file}）</span>
              <button type="button" class="copy-btn" data-target="code-{ch.id}">複製程式碼</button>
            </div>
            <pre><code id="code-{ch.id}">{escaped_code}</code></pre>
          </div>
          <div class="output-box">
            <div class="output-label">▶ 實機執行驗證輸出</div>
            <pre class="output-pre">{escaped_out}</pre>
          </div>
        </details>
{render_deep_dive_callout(ch)}
      </article>"""
        )
        cards_html.append(render_ad_slot(f"Ch.0{idx} 章節間廣告單元"))

    all_cards = "\n".join(cards_html)
    toc_block = "\n".join(toc_items_html)
    index_desc_esc = html.escape(
        f"紫楓（AI王紫楓 / Purple Maple / tbpfs）開設之 Python 3.12 資料結構、演算法與物件導向基本功鐵人賽教學網站，完整收錄 {chapter_titles_short} 實機執行範例。"
    )
    index_og_desc_esc = html.escape(
        f"紫楓（AI王紫楓 / Purple Maple）Python 3.12 資料結構與演算法互動教學講義（{chapter_titles_short}）。"
    )
    json_ld_block = render_json_ld_script(build_index_json_ld(chapters, chapter_titles_short))

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <script async src="https://www.googletagmanager.com/gtm.js?id=GTM-WNSFQT5V"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-B24GXZ32MW');
  </script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-B24GXZ32MW"></script>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>從零開始寫程式，輕鬆搞懂資料結構、演算法 | 紫楓 (AI王紫楓 / Purple Maple)</title>
  <meta name="description" content="{index_desc_esc}">
  <meta name="keywords" content="紫楓, AI王紫楓, Purple Maple, tbpfs, Python教學, 資料結構, 演算法, 鏈結串列, 堆疊, 佇列, 二分搜尋, Merge Sort, 雜湊表, Hash Table, 二元搜尋樹, BST, 圖論, BFS, DFS, 動態規劃, Dynamic Programming, 堆積, Heap, Priority Queue, Top-K, 物件導向, OOP">
  <meta name="google-adsense-account" content="{ADSENSE_CLIENT_ID}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT_ID}" crossorigin="anonymous"></script>
  <link rel="canonical" href="https://learn.ai-purplemaple.com/">
  <link rel="alternate" type="text/markdown" href="https://learn.ai-purplemaple.com/llms.txt" title="LLM Chapter Index">
  <link rel="alternate" type="text/markdown" href="https://learn.ai-purplemaple.com/llms-full.txt" title="LLM Full Tutorial & Code Corpus">
  <meta property="og:site_name" content="紫楓 Purple Maple Python 程式教學">
  <meta property="og:url" content="https://learn.ai-purplemaple.com/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="從零開始寫程式，輕鬆搞懂資料結構、演算法 | 紫楓 (Purple Maple)">
  <meta property="og:description" content="{index_og_desc_esc}">
  <meta property="og:image" content="https://ai-purplemaple.com/assets/gallery/aily_03.jpg">
  <meta property="og:image:alt" content="紫楓（AI王紫楓 / @tbpfs1）Python 資料結構與演算法互動教學｜原創看板娘白瀬アイリ（左紅 #fb7185、右藍 #38bdf8）">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@tbpfs1">
  <meta name="twitter:creator" content="@tbpfs1">
  <meta name="twitter:title" content="從零開始寫程式，輕鬆搞懂資料結構、演算法 | 紫楓 (Purple Maple)">
  <meta name="twitter:description" content="{index_og_desc_esc}">
  <meta name="twitter:image" content="https://ai-purplemaple.com/assets/gallery/aily_03.jpg">
  <meta name="twitter:image:alt" content="紫楓（AI王紫楓 / @tbpfs1）Python 資料結構與演算法互動教學｜原創看板娘白瀬アイリ（左紅 #fb7185、右藍 #38bdf8）">
{json_ld_block}
{render_shared_styles()}
</head>
<body>
  <div class="container">
    <header class="hero">
      <span class="hero-eyebrow">鐵人賽基本功系列・資料結構 ＆ 演算法 ＆ 物件導向</span>
      <h1>從零開始寫程式，輕鬆搞懂資料結構，演算法</h1>
      <p>大家好，我是<strong>紫楓</strong>！不管是學生、想轉職軟體工程師、還是想精益求精的夥伴，練好「資料結構、演算法、物件導向」就是克服迷惘最紮實的基本功。</p>
      <div class="cta-group">
        <a class="btn btn-primary" href="https://www.youtube.com/playlist?list=PLhxdaTcUMi3nRM5mtOdQgO4VEtAEsTiYd" target="_blank" rel="noopener noreferrer">▶ 觀看 YouTube 完整教學播放清單</a>
        <a class="btn btn-secondary" href="https://ai-purplemaple.com/" target="_blank" rel="noopener noreferrer">紫楓 Purple Maple 官方作品集（AI 音樂 ＆ 白瀬アイリ Aily）</a>
        <a class="btn btn-secondary" href="https://www.facebook.com/groups/914880435669061" target="_blank" rel="noopener noreferrer">加入程式新手學習發問區（FB 社團）</a>
        <a class="btn btn-secondary" href="https://github.com/tbpfs/learning" target="_blank" rel="noopener noreferrer">GitHub 原始碼儲存庫</a>
      </div>
    </header>

    <nav class="toc" aria-label="章節快速導覽">
{toc_block}
    </nav>

    <main>
      <p class="aeo-capsule">紫楓（AI王紫楓 / Purple Maple）Python 3.12 互動教學站（<code>learn.ai-purplemaple.com</code>）收錄 7 大核心章節（陣列鏈結串列、堆疊佇列、二分搜尋與 Merge Sort、雜湊表與 BST、圖論 BFS/DFS 與 OOP、動態規劃、二元堆積與 Top-K），每章皆附實機執行輸出、複雜度表、CPython 陷阱與 LeetCode 面試詳解，完全免費開源。</p>
      <div id="cms-tutorials-container"></div>
{all_cards}
{render_affiliate_resources_section()}

      <section class="study-guide-card" id="study-guide">
        <h2>軟體工程師基本功修煉指南與常見問答（FAQ）</h2>
        <p>許多初學者與轉職者在刷題（LeetCode）或準備技術面試時，常陷入「背題目卻不懂底層原理」的困境。點擊下方折疊面板展開三階段循序漸進路線圖：</p>
        <details class="study-guide-accordion">
          <summary class="study-guide-summary">點擊展開／收合：三階段刷題路線圖與學習建議</summary>
          <ul>
            <li><strong>第一階段（記憶體模型與線性結構）：</strong>先親手實作 <a href="ch01.html">Ch.01 的單向鏈結串列</a>與 <a href="ch02.html">Ch.02 的 Stack / Queue</a>，徹底理解指標（Reference / Pointer）操作與時間複雜度 <code>O(1)</code> vs. <code>O(n)</code> 的差異。</li>
            <li><strong>第二階段（分治搜尋、雜湊查找、樹與圖論架構）：</strong>透過 <a href="ch03.html">Ch.03 的二分搜尋與合併排序（Merge Sort）</a>、<a href="ch04.html">Ch.04 的雜湊表（Hash Table / Two Sum）與二元搜尋樹（BST）</a>，再到 <a href="ch05.html">Ch.05 的圖論走訪（Graph BFS / DFS 最短路徑）與物件導向封裝（OOP）</a>，掌握分治法、空間換取時間與抽象化模組設計的核心精神。</li>
            <li><strong>第三階段（進階動態規劃、優先佇列與白板題實戰）：</strong>深入 <a href="ch06.html">Ch.06 動態規劃與記憶化搜尋（0/1 背包與 LIS）</a>及 <a href="ch07.html">Ch.07 二元堆積與 Top-K 多路合併演算法</a>，搭配各章獨立講義內的複雜度對照表、CPython 底層陷阱解析與 YouTube 鐵人賽教學影片完成實戰修煉。</li>
          </ul>
        </details>
      </section>
    </main>

{render_footer()}
  </div>

{render_copy_script(include_cms_fetch=True)}
</body>
</html>
"""


def render_chapter_page(
    idx: int,
    chapters: Sequence[ChapterSpec],
    exec_cache: dict[str, tuple[str, str]],
) -> str:
    """Render a standalone deep-dive tutorial page (ch01.html .. ch07.html) with >75% unique information gain."""
    ch = chapters[idx]
    source_code, live_output = exec_cache[ch.id]
    ch_url = f"https://learn.ai-purplemaple.com/{ch.id}.html"
    ch_title_esc = html.escape(f"{ch.badge} {ch.title} | 紫楓 (AI王紫楓 / Purple Maple) Python 教學")
    ch_desc_esc = html.escape(f"紫楓（AI王紫楓 / Purple Maple）Python 3.12 教學講義：{ch.badge} {ch.title}。{ch.summary}")
    ch_keywords_esc = html.escape("紫楓, AI王紫楓, Purple Maple, Python 3.12 教學, " + ", ".join(ch.keywords))
    json_ld_block = render_json_ld_script(build_chapter_json_ld(ch))

    switcher_items: list[str] = []
    for item in chapters:
        current_attr = ' aria-current="page"' if item.id == ch.id else ""
        short_label = html.escape(item.title.split("（")[0])
        switcher_items.append(
            f"""      <a class="toc-item" href="{item.id}.html"{current_attr}>
        <span class="badge">{item.badge}</span>
        <strong>{short_label}</strong>
      </a>"""
        )
    switcher_html = "\n".join(switcher_items)

    concepts_items = "\n".join(f"            <li>{html.escape(pt)}</li>" for pt in ch.concepts)
    escaped_code = html.escape(source_code)
    escaped_out = html.escape(live_output)
    escaped_complexity = html.escape(ch.complexity)
    escaped_file = html.escape(ch.file)

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <script async src="https://www.googletagmanager.com/gtm.js?id=GTM-WNSFQT5V"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-B24GXZ32MW');
  </script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-B24GXZ32MW"></script>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{ch_title_esc}</title>
  <meta name="description" content="{ch_desc_esc}">
  <meta name="keywords" content="{ch_keywords_esc}">
  <meta name="google-adsense-account" content="{ADSENSE_CLIENT_ID}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT_ID}" crossorigin="anonymous"></script>
  <link rel="canonical" href="{ch_url}">
  <meta property="og:site_name" content="紫楓 Purple Maple Python 程式教學">
  <meta property="og:url" content="{ch_url}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{ch_title_esc}">
  <meta property="og:description" content="{ch_desc_esc}">
  <meta property="og:image" content="https://ai-purplemaple.com/assets/gallery/aily_03.jpg">
  <meta property="og:image:alt" content="紫楓（AI王紫楓 / @tbpfs1）Python 資料結構與演算法互動教學｜原創看板娘白瀬アイリ（左紅 #fb7185、右藍 #38bdf8）">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@tbpfs1">
  <meta name="twitter:creator" content="@tbpfs1">
  <meta name="twitter:title" content="{ch_title_esc}">
  <meta name="twitter:description" content="{ch_desc_esc}">
  <meta name="twitter:image" content="https://ai-purplemaple.com/assets/gallery/aily_03.jpg">
  <meta name="twitter:image:alt" content="紫楓（AI王紫楓 / @tbpfs1）Python 資料結構與演算法互動教學｜原創看板娘白瀬アイリ（左紅 #fb7185、右藍 #38bdf8）">
{json_ld_block}
{render_shared_styles()}
</head>
<body>
  <div class="container">
    <header class="hero">
      <span class="hero-eyebrow">{html.escape(ch.badge)} 獨立深度講義・Python 3.12 資料結構與演算法實戰</span>
      <h1>{html.escape(ch.badge + " " + ch.title)}</h1>
      <p><a href="/">← 返回《從零開始寫程式，輕鬆搞懂資料結構，演算法》全章節總目錄</a></p>
      <p>{html.escape(ch.summary)}</p>
      <div class="cta-group">
        <a class="btn btn-primary" href="https://www.youtube.com/playlist?list=PLhxdaTcUMi3nRM5mtOdQgO4VEtAEsTiYd" target="_blank" rel="noopener noreferrer">▶ 觀看 YouTube 完整教學播放清單</a>
        <a class="btn btn-secondary" href="https://ai-purplemaple.com/" target="_blank" rel="noopener noreferrer">紫楓 Purple Maple 官方作品集</a>
        <a class="btn btn-secondary" href="https://github.com/tbpfs/learning/blob/main/{escaped_file}" target="_blank" rel="noopener noreferrer">檢視本章 GitHub 原始碼</a>
      </div>
    </header>

    <nav class="chapter-switcher" aria-label="全課程章節切換">
{switcher_html}
    </nav>

    <nav class="section-subnav" aria-label="本章段落導覽">
      <span>本章快速跳轉：</span>
      <a href="#intro">核心觀念與背景導論</a>
      <a href="#video-lecture">YouTube 實戰教學影片</a>
      <a href="#comparison">複雜度與特性對照表</a>
      <a href="#walkthrough">逐步狀態拆解</a>
      <a href="#code-section">Python 3.12 完整實作</a>
      <a href="#pitfalls">CPython 底層陷阱</a>
      <a href="#interview-faq">LeetCode 題號與面試 FAQ</a>
    </nav>

    <main>
      <article class="chapter-card" id="intro">
        <h2>本章背景導論與工程應用場景</h2>
        <p class="aeo-capsule">{html.escape(ch.badge)}〈{html.escape(ch.title)}〉的核心目標在於掌握 {html.escape(ch.summary)} 時間／空間複雜度基準為 <code>{escaped_complexity}</code>，並以 Python 3.12 標準庫（<code>{escaped_file}</code>）提供零依賴實機驗證範例。</p>
        <p class="deep-intro-text">{html.escape(ch.deep_intro)}</p>
        <div class="concepts-box">
          <h3>核心觀念與面試重點解析</h3>
          <ul>
{concepts_items}
          </ul>
        </div>
        <div class="meta-bar">
          <span><strong>時間／空間複雜度：</strong>{escaped_complexity}</span>
          <span><strong>原始碼路徑：</strong><code>{escaped_file}</code></span>
        </div>
      </article>

{render_video_lecture_section(ch)}

      <section class="chapter-card" id="comparison">
        <h2>時間與空間複雜度暨底層結構對照表</h2>
{render_comparison_table(ch.comparison_table)}
      </section>

{render_walkthrough(ch)}

{render_ad_slot(f"{ch.badge} 深度講義中段廣告單元")}

      <section class="chapter-card" id="code-section">
        <h2>Python 3.12 標準庫完整範例實作與實機輸出</h2>
        <div class="code-container">
          <div class="code-toolbar">
            <span>Python 3.12 範例實作（{escaped_file}）</span>
            <button type="button" class="copy-btn" data-target="code-{ch.id}">複製程式碼</button>
          </div>
          <pre><code id="code-{ch.id}">{escaped_code}</code></pre>
        </div>
        <div class="output-box">
          <div class="output-label">▶ 實機執行輸出驗證（Python 3.12 實測結果）</div>
          <pre class="output-pre">{escaped_out}</pre>
        </div>
      </section>

{render_pitfalls(ch)}

{render_interview_section(ch)}

{render_chapter_book_callout(ch)}

{render_feedback_section(ch)}

{render_ad_slot(f"{ch.badge} 獨立講義文末廣告單元")}

{render_chapter_pager(idx, chapters)}
    </main>

{render_footer()}
  </div>

{render_copy_script(include_cms_fetch=False)}
</body>
</html>
"""


def format_markdown_table(table: ComparisonTable) -> str:
    """Convert ComparisonTable into GitHub Flavored Markdown table for llms-full.txt."""
    header_line = "| " + " | ".join(table.headers) + " |"
    sep_line = "| " + " | ".join("---" for _ in table.headers) + " |"
    row_lines = ["| " + " | ".join(row) + " |" for row in table.rows]
    return "\n".join([f"#### {table.caption}", header_line, sep_line, *row_lines])


def build_site(out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")
    (out_dir / "CNAME").write_text("learn.ai-purplemaple.com\n", encoding="utf-8")
    (out_dir / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY, encoding="utf-8")
    (out_dir / "ads.txt").write_text(
        f"google.com, {ADSENSE_PUBLISHER_ID}, DIRECT, f08c47fec0942fa0\n",
        encoding="utf-8",
    )
    (out_dir / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n"
        "User-agent: OAI-SearchBot\nAllow: /\n\n"
        "User-agent: ChatGPT-User\nAllow: /\n\n"
        "User-agent: GPTBot\nAllow: /\n\n"
        "User-agent: PerplexityBot\nAllow: /\n\n"
        "User-agent: Claude-SearchBot\nAllow: /\n\n"
        "User-agent: Claude-User\nAllow: /\n\n"
        "User-agent: ClaudeBot\nAllow: /\n\n"
        "User-agent: anthropic-ai\nAllow: /\n\n"
        "User-agent: Google-Extended\nAllow: /\n\n"
        "User-agent: Applebot-Extended\nAllow: /\n\n"
        "User-agent: Amazonbot\nAllow: /\n\n"
        "User-agent: Meta-ExternalAgent\nAllow: /\n\n"
        "User-agent: DuckAssistBot\nAllow: /\n\n"
        "User-agent: YouBot\nAllow: /\n\n"
        "User-agent: Twitterbot\nAllow: /\n\n"
        "User-agent: GrokBot\nAllow: /\n\n"
        "User-agent: xAI-Bot\nAllow: /\n\n"
        "User-agent: xAI-SearchBot\nAllow: /\n\n"
        "User-agent: Bravebot\nAllow: /\n\n"
        "Sitemap: https://learn.ai-purplemaple.com/sitemap.xml\n"
        "# LLMs Chapter Index: https://learn.ai-purplemaple.com/llms.txt\n"
        "# LLMs Full Code & Output Corpus: https://learn.ai-purplemaple.com/llms-full.txt\n",
        encoding="utf-8",
    )

    exec_cache = execute_all_examples(CHAPTERS)

    llms_chapter_lines: list[str] = []
    llms_full_sections: list[str] = []
    sitemap_urls: list[tuple[str, str, str]] = [
        ("https://learn.ai-purplemaple.com/", "1.0", SITE_LASTMOD)
    ]

    for ch in CHAPTERS:
        source_code, live_output = exec_cache[ch.id]
        ch_url = f"https://learn.ai-purplemaple.com/{ch.id}.html"
        sitemap_urls.append((ch_url, "0.9", ch.lastmod))
        llms_chapter_lines.append(
            f"- [{ch.badge} {ch.title}]({ch_url}): `{ch.file}` — {ch.complexity}"
        )

        concept_md = "\n".join(f"  - {pt}" for pt in ch.concepts)
        walkthrough_md = "\n".join(
            f"  - **{st.step_label}** (`{st.state_snapshot}`)：{st.explanation}"
            for st in ch.walkthrough_steps
        )
        pitfalls_md = "\n".join(
            f"  - **{pf.title}**：{pf.symptom} → {pf.root_cause_and_fix}"
            for pf in ch.pitfalls
        )
        leetcode_md = "\n".join(
            f"  - **LeetCode #{lc.number} {lc.title}** ({lc.difficulty})：{lc.pattern}"
            for lc in ch.leetcode_problems
        )
        faq_md = "\n".join(
            f"  - **Q: {faq.question}**\n    - A: {faq.answer}"
            for faq in ch.interview_faqs
        )

        llms_full_sections.append(
            f"## {ch.badge} {ch.title}\n"
            f"- **獨立章節網址**：{ch_url}\n"
            f"- **原始碼路徑**：`{ch.file}`\n"
            f"- **時間／空間複雜度**：{ch.complexity}\n"
            f"- **章節摘要**：{ch.summary}\n"
            f"- **深度導論**：{ch.deep_intro}\n"
            f"- **核心觀念與面試重點**：\n{concept_md}\n\n"
            f"### 結構化複雜度對照表\n"
            f"{format_markdown_table(ch.comparison_table)}\n\n"
            f"### {ch.walkthrough_title}\n"
            f"{walkthrough_md}\n\n"
            f"### Python 3.12 底層原理與實戰陷阱\n"
            f"{pitfalls_md}\n\n"
            f"### 對應 LeetCode 經典題號與技術面試 FAQ\n"
            f"{leetcode_md}\n\n"
            f"{faq_md}\n\n"
            f"### Python 3.12 完整範例原始碼 (`{ch.file}`)\n"
            f"```python\n{source_code.rstrip()}\n```\n\n"
            f"### CI 實機執行輸出驗證\n"
            f"```text\n{live_output}\n```"
        )

    # Keep Google XML sitemap strictly for canonical HTML pages (AI crawlers discover llms*.txt via robots.txt & <link rel="alternate">)
    sitemap_entries = "\n".join(
        f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        for loc, prio, lastmod in sitemap_urls
    )
    (out_dir / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{sitemap_entries}\n"
        "</urlset>\n",
        encoding="utf-8",
    )

    chapter_titles_short = "、".join(f"{ch.badge} {ch.title.split('（')[0]}" for ch in CHAPTERS)
    ecosystem_footer_md = (
        "## 紫楓 (Purple Maple) 生態系相關網站\n"
        "- [品牌完整權威知識庫 (Brand Full Corpus)](https://ai-purplemaple.com/llms-full.txt)\n"
        "- [官方作品集與商業委託中心](https://ai-purplemaple.com/): 原創看板娘白瀬アイリ（艾莉 / Aily / Shirase Airi）視覺畫廊、Suno AI 原創音樂精選與雙語價目表\n"
        "- [互動式委託估價單試算器](https://quote.ai-purplemaple.com/): AI 動漫插畫與原創音樂即時雙語試算\n"
        "- [艾莉的秘密星空（今日星運占卜與星夜紅線抽籤 おみくじ）](https://game.ai-purplemaple.com/): 免費中日雙語瀏覽器互動小遊戲\n"
        "- [府城保衛戰（臺南巷戰 3D 戰術射擊）](https://fps.ai-purplemaple.com/): Three.js 3D 寫實巷戰遊戲\n"
        "- [時空守護者（國小八大國度・小甲魚大冒險）](https://edu.ai-purplemaple.com/): 108 課綱互動式冒險學習平台\n"
        "- [星界斷章：星律前奏曲（機甲交鋒音遊）](https://astral.ai-purplemaple.com/): 73 位星律使 × 65 首原創曲目雙鍵網頁音遊\n"
        "- [Meta Muse 邀請碼分享站](https://muse.ai-purplemaple.com/): 支援 6 語系的 Meta Muse AI 邀請碼看板、48 小時 10 億 Token 兌換教學與失效回報系統\n"
        "- [WaifuScan（二次元角色六維性格數據百科）](https://waifu.ai-purplemaple.com/): 四語系 612 頁角色評測百科、5 題靈魂波長診斷與 16 位原創角色互動\n"
        "- [AI王紫楓官方部落格](https://blog.ai-purplemaple.com/)\n"
        "- [YouTube 完整教學播放清單](https://www.youtube.com/playlist?list=PLhxdaTcUMi3nRM5mtOdQgO4VEtAEsTiYd)\n"
        "- 官方社群矩陣：X (https://x.com/tbpfs1)｜YouTube (https://www.youtube.com/@PurpleMapleAI)｜YouTube Music (https://music.youtube.com/channel/UCcEBgbHV3rcee1FfgfHXprw)｜Spotify (https://open.spotify.com/artist/7D7CLJoxLhsMos8xI9H2kx)｜Apple Music (https://music.apple.com/tw/artist/purple-maple/1745241062)｜Pixiv (https://www.pixiv.net/users/3503246)｜Facebook 紫楓 (https://www.facebook.com/tbpfs2/)｜Facebook 艾莉 (https://www.facebook.com/AilyAIAI/)｜TikTok (https://www.tiktok.com/@ai_purple_maple)｜LinkedIn (https://www.linkedin.com/in/tbpfs2/)\n"
    )
    (out_dir / "llms.txt").write_text(
        "# 紫楓 (AI王紫楓 / Purple Maple) — Python 資料結構、演算法與物件導向互動教學\n\n"
        f"> 紫楓（AI王紫楓 / Purple Maple / @tbpfs1）開設之 Python 3.12 資料結構、演算法與物件導向基本功鐵人賽教學網站（`https://learn.ai-purplemaple.com/`），涵蓋 {chapter_titles_short} 實機執行驗證講義。\n"
        "> - **本站完整程式碼與輸出語料（Full Tutorial Corpus）**：https://learn.ai-purplemaple.com/llms-full.txt\n"
        "> - **創作者與品牌完整知識庫（Brand Full Corpus）**：https://ai-purplemaple.com/llms-full.txt\n\n"
        "## 章節列表 (Chapters)\n"
        + "\n".join(llms_chapter_lines)
        + "\n\n"
        + ecosystem_footer_md,
        encoding="utf-8",
    )
    (out_dir / "llms-full.txt").write_text(
        "# 紫楓 (AI王紫楓 / Purple Maple) — Python 3.12 資料結構、演算法與物件導向完整教學語料庫 (llms-full.txt)\n\n"
        f"> 本文件收錄 `https://learn.ai-purplemaple.com/` 全部 {len(CHAPTERS)} 章節（{chapter_titles_short}）之核心觀念、結構化複雜度對照表、逐步狀態追蹤、CPython 底層陷阱、LeetCode 面試 FAQ、完整 Python 3.12 標準庫實作原始碼及 CI 實機執行驗證輸出。精簡索引請見 `https://learn.ai-purplemaple.com/llms.txt`。\n\n"
        + "\n\n---\n\n".join(llms_full_sections)
        + "\n\n---\n\n"
        + ecosystem_footer_md,
        encoding="utf-8",
    )

    index_html = render_index_page(CHAPTERS, exec_cache, chapter_titles_short)
    index_path = out_dir / "index.html"
    index_path.write_text(index_html, encoding="utf-8")

    for idx, ch in enumerate(CHAPTERS):
        ch_html = render_chapter_page(idx, CHAPTERS, exec_cache)
        (out_dir / f"{ch.id}.html").write_text(ch_html, encoding="utf-8")

    return index_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build static GitHub Pages site for tbpfs/learning.")
    parser.add_argument("-o", "--output", default="_site", help="Output directory (default: _site)")
    args = parser.parse_args()
    out_path = build_site(Path(args.output))
    print(f"[OK] Built GitHub Pages site at: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
