#!/usr/bin/env python3
"""
build_site.py - Static Site Generator for GitHub Pages (`tbpfs/learning`).
Zero external dependencies. Reads examples/ch01..ch07 and structured deep-dive content from
`chapter_content.py`, executes each script once to capture live stdout, and renders:
  - `_site/index.html` (Course Hub with executable sandbox & deep-dive callouts)
  - `_site/ch01.html` .. `_site/ch07.html` (Standalone 1,200+ CJK char deep-dive tutorials)
  - `_site/llms.txt`, `_site/llms-full.txt`, `_site/sitemap.xml`, `_site/robots.txt`, `_site/ads.txt`
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

from chapter_content import CHAPTERS, ChapterSpec, ComparisonTable  # noqa: E402

ADSENSE_PUBLISHER_ID = "pub-6485917848711473"
ADSENSE_CLIENT_ID = f"ca-{ADSENSE_PUBLISHER_ID}"
ADSENSE_IN_ARTICLE_SLOT_ID = "1673180799"
INDEXNOW_KEY = "7f4e9c2a8b1d6035e4a92c7f1b8d3e60"


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
    """Execute each chapter script exactly once and cache (source_code, live_output) by chapter ID."""
    cache: dict[str, tuple[str, str]] = {}
    for ch in chapters:
        cache[ch.id] = run_example(ch.file)
    return cache


def render_ad_slot(slot_label: str) -> str:
    """Render a CLS-safe responsive Google AdSense inter-chapter ad container."""
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
    """Serialize Schema.org JSON-LD safely via json.dumps."""
    dumped = json.dumps(payload, ensure_ascii=False, indent=2)
    return f'  <script type="application/ld+json">\n{dumped}\n  </script>'


def build_index_json_ld(chapters: Sequence[ChapterSpec], chapter_titles_short: str) -> dict[str, Any]:
    """Build Course + hasPart JSON-LD for the root index page."""
    return {
        "@context": "https://schema.org",
        "@type": "Course",
        "@id": "https://learn.ai-purplemaple.com/#course",
        "name": "從零開始寫程式，輕鬆搞懂資料結構、演算法",
        "description": f"紫楓（AI王紫楓 / Purple Maple）開設之 Python 3.12 資料結構、演算法與物件導向實戰教學課程，涵蓋 {chapter_titles_short}。",
        "url": "https://learn.ai-purplemaple.com/",
        "inLanguage": "zh-TW",
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
        },
        "hasPart": [
            {
                "@type": "TechArticle",
                "@id": f"https://learn.ai-purplemaple.com/{ch.id}.html#article",
                "name": f"{ch.badge} {ch.title}",
                "url": f"https://learn.ai-purplemaple.com/{ch.id}.html",
            }
            for ch in chapters
        ],
    }


def build_chapter_json_ld(ch: ChapterSpec) -> dict[str, Any]:
    """Build @graph JSON-LD (TechArticle + FAQPage + BreadcrumbList) for a standalone chapter page."""
    ch_url = f"https://learn.ai-purplemaple.com/{ch.id}.html"
    creator_ref = {
        "@type": "Person",
        "@id": "https://ai-purplemaple.com/#creator",
        "name": "紫楓 (AI王紫楓 / Purple Maple)",
        "url": "https://ai-purplemaple.com/",
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
                "isPartOf": {
                    "@type": "Course",
                    "@id": "https://learn.ai-purplemaple.com/#course",
                    "name": "從零開始寫程式，輕鬆搞懂資料結構、演算法",
                    "url": "https://learn.ai-purplemaple.com/",
                },
            },
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


SHARED_CSS = """    :root {
      --bg: #0f101a;
      --surface: #181a29;
      --surface-alt: #1f2235;
      --border: #2e334d;
      --text: #eef0f7;
      --muted: #aab1cc;
      --accent: #a78bfa;
      --accent-strong: #8b5cf6;
      --success: #34d399;
      --warning: #fbbf24;
      --code-bg: #11131f;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans TC", sans-serif;
      background: radial-gradient(circle at top, #1b1734 0%, var(--bg) 55%);
      color: var(--text);
      line-height: 1.68;
    }
    a { color: var(--accent); text-decoration: none; }
    a:hover { text-decoration: underline; }
    .container {
      max-width: 980px;
      margin: 0 auto;
      padding: 2.5rem 1.25rem 4rem;
    }
    header.hero {
      background: linear-gradient(135deg, rgba(139, 92, 246, 0.16), rgba(31, 34, 53, 0.92));
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 2.25rem 2rem;
      margin-bottom: 2.25rem;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.32);
    }
    .hero-eyebrow {
      display: inline-block;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--accent);
      background: rgba(167, 139, 250, 0.12);
      border: 1px solid rgba(167, 139, 250, 0.35);
      padding: 0.25rem 0.75rem;
      border-radius: 999px;
      margin-bottom: 0.75rem;
    }
    .hero h1 {
      margin: 0 0 0.75rem;
      font-size: clamp(1.55rem, 3.2vw, 2.2rem);
      line-height: 1.32;
    }
    .hero p {
      margin: 0.5rem 0;
      color: var(--muted);
    }
    .cta-group {
      display: flex;
      flex-wrap: wrap;
      gap: 0.85rem;
      margin-top: 1.5rem;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.65rem 1.2rem;
      border-radius: 10px;
      font-weight: 600;
      font-size: 0.95rem;
      transition: transform 0.15s ease, background 0.15s ease;
    }
    .btn:hover {
      transform: translateY(-1px);
      text-decoration: none;
    }
    .btn-primary {
      background: var(--accent-strong);
      color: #ffffff;
    }
    .btn-secondary {
      background: var(--surface-alt);
      color: var(--text);
      border: 1px solid var(--border);
    }
    nav.toc {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 0.9rem;
      margin-bottom: 2.25rem;
    }
    .toc-item {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 0.95rem 1.15rem;
      display: block;
      transition: border-color 0.15s ease;
    }
    .toc-item:hover, .toc-item[aria-current="page"] {
      border-color: var(--accent);
      text-decoration: none;
    }
    .toc-item[aria-current="page"] {
      background: rgba(167, 139, 250, 0.12);
    }
    .toc-item strong {
      display: block;
      color: var(--text);
      margin-top: 0.25rem;
      font-size: 0.95rem;
    }
    .section-toc {
      display: flex;
      flex-wrap: wrap;
      gap: 0.6rem;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 0.85rem 1.1rem;
      margin-bottom: 1.75rem;
      font-size: 0.88rem;
    }
    .section-toc a {
      background: var(--surface-alt);
      border: 1px solid var(--border);
      padding: 0.3rem 0.75rem;
      border-radius: 999px;
      color: var(--text);
    }
    .section-toc a:hover {
      border-color: var(--accent);
      color: var(--accent);
      text-decoration: none;
    }
    .chapter-card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 1.75rem;
      margin-bottom: 2rem;
    }
    .chapter-header {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-bottom: 0.65rem;
    }
    .badge {
      background: rgba(167, 139, 250, 0.18);
      color: var(--accent);
      border: 1px solid rgba(167, 139, 250, 0.4);
      padding: 0.2rem 0.65rem;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.85rem;
    }
    .chapter-header h2 {
      margin: 0;
      font-size: 1.35rem;
    }
    .chapter-summary {
      color: var(--muted);
      margin: 0.5rem 0 1rem;
    }
    .deep-intro-text {
      color: var(--text);
      margin: 0.75rem 0 1.25rem;
      font-size: 0.98rem;
      line-height: 1.78;
    }
    .meta-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 1.25rem;
      font-size: 0.9rem;
      color: var(--muted);
      background: var(--surface-alt);
      padding: 0.65rem 1rem;
      border-radius: 10px;
      margin-bottom: 1rem;
    }
    .code-container {
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      background: var(--code-bg);
      margin-bottom: 1rem;
    }
    .code-toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.55rem 1rem;
      background: #16192b;
      border-bottom: 1px solid var(--border);
      font-size: 0.85rem;
      color: var(--muted);
    }
    .copy-btn {
      background: var(--surface-alt);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 0.28rem 0.7rem;
      font-size: 0.8rem;
      cursor: pointer;
    }
    .copy-btn:hover {
      border-color: var(--accent);
    }
    pre {
      margin: 0;
      padding: 1rem 1.2rem;
      overflow-x: auto;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.86rem;
      line-height: 1.55;
    }
    .output-box {
      background: rgba(52, 211, 153, 0.07);
      border: 1px solid rgba(52, 211, 153, 0.3);
      border-radius: 10px;
      padding: 0.75rem 1rem;
      margin-bottom: 1rem;
    }
    .output-label {
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--success);
      margin-bottom: 0.35rem;
    }
    .output-pre {
      padding: 0;
      color: #d1fae5;
      background: transparent;
    }
    .concepts-box {
      background: rgba(167, 139, 250, 0.06);
      border-left: 3px solid var(--accent);
      border-radius: 8px;
      padding: 0.85rem 1.15rem;
      margin-bottom: 1rem;
    }
    .concepts-box h3 {
      margin: 0 0 0.45rem;
      font-size: 0.95rem;
      color: var(--accent);
    }
    .concepts-box ul {
      margin: 0;
      padding-left: 1.2rem;
      color: var(--muted);
      font-size: 0.92rem;
    }
    .concepts-box li {
      margin-bottom: 0.4rem;
    }
    .deep-dive-callout {
      background: linear-gradient(135deg, rgba(139, 92, 246, 0.12), rgba(31, 34, 53, 0.85));
      border: 1px solid rgba(167, 139, 250, 0.38);
      border-radius: 12px;
      padding: 1rem 1.25rem;
      margin-top: 1.1rem;
      display: flex;
      flex-direction: column;
      gap: 0.55rem;
    }
    .deep-dive-callout strong {
      color: var(--accent);
      font-size: 0.95rem;
    }
    .deep-dive-callout p {
      margin: 0;
      font-size: 0.88rem;
      color: var(--muted);
    }
    .table-responsive {
      width: 100%;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      margin: 1rem 0 1.5rem;
      border: 1px solid var(--border);
      border-radius: 12px;
      background: var(--surface-alt);
    }
    table.comparison-table {
      width: 100%;
      min-width: 560px;
      border-collapse: collapse;
      font-size: 0.9rem;
      text-align: left;
    }
    table.comparison-table caption {
      caption-side: top;
      text-align: left;
      padding: 0.75rem 1rem;
      font-weight: 700;
      color: var(--accent);
      border-bottom: 1px solid var(--border);
      background: rgba(167, 139, 250, 0.08);
    }
    table.comparison-table th, table.comparison-table td {
      padding: 0.72rem 1rem;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
    }
    table.comparison-table thead th {
      background: #16192b;
      color: var(--text);
      font-weight: 700;
    }
    table.comparison-table tbody th {
      color: var(--text);
      font-weight: 600;
      width: 22%;
    }
    table.comparison-table tbody td {
      color: var(--muted);
    }
    .walkthrough-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 0.95rem;
      margin: 1rem 0;
    }
    .step-card {
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-left: 4px solid var(--success);
      border-radius: 10px;
      padding: 1rem 1.2rem;
    }
    .step-card h3 {
      margin: 0 0 0.45rem;
      font-size: 0.98rem;
      color: var(--success);
    }
    .state-pill {
      display: block;
      background: var(--code-bg);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 0.45rem 0.75rem;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.84rem;
      color: #d1fae5;
      margin-bottom: 0.55rem;
      overflow-x: auto;
    }
    .step-card p {
      margin: 0;
      color: var(--muted);
      font-size: 0.92rem;
    }
    .pitfall-card {
      background: rgba(251, 191, 36, 0.05);
      border: 1px solid rgba(251, 191, 36, 0.3);
      border-left: 4px solid var(--warning);
      border-radius: 10px;
      padding: 1rem 1.2rem;
      margin-bottom: 1rem;
    }
    .pitfall-card h3 {
      margin: 0 0 0.45rem;
      font-size: 0.98rem;
      color: var(--warning);
    }
    .pitfall-card p {
      margin: 0.35rem 0;
      font-size: 0.92rem;
      color: var(--muted);
    }
    details.faq-item {
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.95rem 1.2rem;
      margin-bottom: 0.9rem;
    }
    details.faq-item summary {
      cursor: pointer;
      font-weight: 700;
      color: var(--accent);
      font-size: 0.96rem;
    }
    .faq-answer {
      margin-top: 0.65rem;
      color: var(--muted);
      font-size: 0.93rem;
      line-height: 1.72;
    }
    .chapter-pager {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.85rem;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.15rem 1.4rem;
      margin-top: 2rem;
    }
    .ad-slot-card {
      background: rgba(24, 26, 41, 0.75);
      border: 1px dashed var(--border);
      border-radius: 14px;
      padding: 1rem 1.25rem;
      margin: 1.75rem 0 2.25rem;
      min-height: 140px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .ad-slot-label {
      font-size: 0.72rem;
      letter-spacing: 0.08em;
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
      border-radius: 16px;
      padding: 1.75rem;
      margin-top: 2rem;
      margin-bottom: 2rem;
    }
    .study-guide-card h2 {
      margin-top: 0;
      font-size: 1.3rem;
      color: var(--text);
    }
    .study-guide-card p, .study-guide-card li {
      color: var(--muted);
      font-size: 0.94rem;
    }
    .privacy-policy-card {
      background: rgba(24, 26, 41, 0.6);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
      margin-bottom: 1.5rem;
      text-align: left;
    }
    .privacy-policy-card h3 {
      margin: 0 0 0.5rem;
      font-size: 0.95rem;
      color: var(--accent);
    }
    .privacy-policy-card p {
      margin: 0 0 0.5rem;
      font-size: 0.84rem;
      line-height: 1.65;
      color: var(--muted);
    }
    footer {
      text-align: center;
      color: var(--muted);
      font-size: 0.88rem;
      margin-top: 3rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border);
    }"""


FOOTER_HTML = """    <footer id="privacy">
      <div class="privacy-policy-card">
        <h3>隱私權政策與 Cookie 聲明 (Privacy Policy)</h3>
        <p>本網站（learn.ai-purplemaple.com）使用 Google AdSense 第三方廣告服務與 Google Analytics (GA4)／Google Tag Manager 網站流量分析服務。Google 及其合作夥伴會使用 Cookie（包含 DART Cookie），根據使用者造訪本站或其他網站的紀錄提供個人化廣告與匿名流量統計。您可隨時前往 <a href="https://adssettings.google.com/" target="_blank" rel="noopener noreferrer">Google 廣告設定頁面</a> 停用個人化廣告，或查閱 <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener noreferrer">Google 廣告與隱私權政策</a>。本站程式碼複製功能均於瀏覽器本機執行，不會收集或儲存您的個人識別資料。</p>
      </div>
      <p>Created by <strong><a href="https://ai-purplemaple.com/" target="_blank" rel="noopener noreferrer" style="color: var(--accent);">紫楓 (AI王紫楓 / Purple Maple)</a></strong> ・ <a href="https://quote.ai-purplemaple.com/" target="_blank" rel="noopener noreferrer" style="color: var(--muted);">插畫＆音樂委託試算</a> ・ <a href="https://game.ai-purplemaple.com/" target="_blank" rel="noopener noreferrer" style="color: var(--muted);">白瀬アイリ占卜小遊戲</a> ・ <a href="https://fps.ai-purplemaple.com/" target="_blank" rel="noopener noreferrer" style="color: var(--muted);">府城保衛戰 3D</a> ・ <a href="https://edu.ai-purplemaple.com/" target="_blank" rel="noopener noreferrer" style="color: var(--muted);">時空守護者</a> ・ Powered by Python 3.12 &amp; GitHub Pages ・ <a href="ads.txt">ads.txt</a></p>
    </footer>"""


COPY_BUTTON_JS = """    function bindCopyButtons() {
      document.querySelectorAll('.copy-btn').forEach(function (btn) {
        if (btn.getAttribute('data-bound') === '1') return;
        btn.setAttribute('data-bound', '1');
        btn.addEventListener('click', function () {
          var targetId = btn.getAttribute('data-target');
          var codeEl = document.getElementById(targetId);
          if (!codeEl || !navigator.clipboard) return;
          navigator.clipboard.writeText(codeEl.textContent || '').then(function () {
            var orig = btn.textContent;
            btn.textContent = '已複製 ✓';
            if (typeof window.gtag === 'function') {
              window.gtag('event', 'copy_code', { chapter_target: targetId });
            }
            setTimeout(function () { btn.textContent = orig; }, 1500);
          });
        });
      });
    }
    bindCopyButtons();"""


def render_comparison_table(table: ComparisonTable) -> str:
    """Render semantic HTML comparison table wrapped in .table-responsive."""
    ths = "\n".join(f'              <th scope="col">{html.escape(h)}</th>' for h in table.headers)
    body_rows: list[str] = []
    for row in table.rows:
        first_cell = f'              <th scope="row">{html.escape(row[0])}</th>'
        rest_cells = "\n".join(f"              <td>{html.escape(c)}</td>" for c in row[1:])
        body_rows.append(f"            <tr>\n{first_cell}\n{rest_cells}\n            </tr>")
    rows_html = "\n".join(body_rows)
    return f"""        <div class="table-responsive">
          <table class="comparison-table">
            <caption>{html.escape(table.caption)}</caption>
            <thead>
              <tr>
{ths}
              </tr>
            </thead>
            <tbody>
{rows_html}
            </tbody>
          </table>
        </div>"""


def render_walkthrough(ch: ChapterSpec) -> str:
    """Render Step-by-Step algorithm state walkthrough cards."""
    steps_html: list[str] = []
    for step in ch.walkthrough_steps:
        steps_html.append(
            f"""          <div class="step-card">
            <h3>{html.escape(step.step_label)}</h3>
            <code class="state-pill">{html.escape(step.state_snapshot)}</code>
            <p>{html.escape(step.explanation)}</p>
          </div>"""
        )
    joined = "\n".join(steps_html)
    return f'        <div class="walkthrough-grid">\n{joined}\n        </div>'


def render_pitfalls(ch: ChapterSpec) -> str:
    """Render CPython 3.12 runtime internals & common pitfalls cards."""
    items: list[str] = []
    for pf in ch.pitfalls:
        items.append(
            f"""        <div class="pitfall-card">
          <h3>{html.escape(pf.title)}</h3>
          <p><strong>常見錯誤現象：</strong>{html.escape(pf.symptom)}</p>
          <p><strong>底層根因與正確對策：</strong>{html.escape(pf.root_cause_and_fix)}</p>
        </div>"""
        )
    return "\n".join(items)


def render_interview_section(ch: ChapterSpec) -> str:
    """Render LeetCode problem mapping table and expandable Interview FAQ cards."""
    lc_rows: list[str] = []
    for lc in ch.leetcode_problems:
        lc_rows.append(
            f"""            <tr>
              <th scope="row">LeetCode #{lc.number}</th>
              <td>{html.escape(lc.title)}</td>
              <td>{html.escape(lc.difficulty)}</td>
              <td>{html.escape(lc.pattern)}</td>
            </tr>"""
        )
    lc_table = f"""        <div class="table-responsive">
          <table class="comparison-table">
            <caption>{html.escape(ch.badge)} 對應必刷 LeetCode 經典白板題號與破題模板</caption>
            <thead>
              <tr>
                <th scope="col">題號</th>
                <th scope="col">題目名稱</th>
                <th scope="col">難度</th>
                <th scope="col">核心解題模板與複雜度</th>
              </tr>
            </thead>
            <tbody>
{chr(10).join(lc_rows)}
            </tbody>
          </table>
        </div>"""

    faq_blocks: list[str] = []
    for faq in ch.interview_faqs:
        faq_blocks.append(
            f"""        <details class="faq-item" open>
          <summary>{html.escape(faq.question)}</summary>
          <div class="faq-answer">{html.escape(faq.answer)}</div>
        </details>"""
        )
    return lc_table + "\n" + "\n".join(faq_blocks)


def render_deep_dive_callout(ch: ChapterSpec) -> str:
    """Render the asymmetric information-gain callout panel on index.html pointing to ch0X.html."""
    faq_titles = " ／ ".join(html.escape(faq.question.split("：")[0]) for faq in ch.interview_faqs)
    lc_nums = "、".join(f"#{lc.number}" for lc in ch.leetcode_problems)
    return f"""        <div class="deep-dive-callout">
          <strong>📖 {html.escape(ch.badge)} 獨立深度專論講義（含完整表格與白板題詳解）</strong>
          <p>內含「{html.escape(ch.comparison_table.caption)}」、4 步記憶體狀態拆解、CPython 3.12 底層陷阱剖析，以及 LeetCode {html.escape(lc_nums)} 與 3 道面試必考問答（{faq_titles}）。</p>
          <div>
            <a class="btn btn-primary" href="{ch.id}.html">閱讀 {html.escape(ch.badge)} 完整深度講義與面試題解 →</a>
          </div>
        </div>"""


def render_chapter_pager(idx: int, chapters: Sequence[ChapterSpec]) -> str:
    """Render previous / course hub / next navigation bar at the bottom of standalone chapter pages."""
    prev_html = (
        f'<a class="btn btn-secondary" href="{chapters[idx - 1].id}.html">← 上一章：{html.escape(chapters[idx - 1].badge)}</a>'
        if idx > 0
        else '<span></span>'
    )
    hub_html = '<a class="btn btn-secondary" href="/">🏠 返回全章節總目錄</a>'
    next_html = (
        f'<a class="btn btn-primary" href="{chapters[idx + 1].id}.html">下一章：{html.escape(chapters[idx + 1].badge)} →</a>'
        if idx + 1 < len(chapters)
        else '<a class="btn btn-primary" href="/">🎉 完成全系列！返回總目錄 →</a>'
    )
    return f"""      <nav class="chapter-pager" aria-label="上下章節導覽">
        {prev_html}
        {hub_html}
        {next_html}
      </nav>"""


def render_index_page(
    chapters: Sequence[ChapterSpec],
    exec_cache: dict[str, tuple[str, str]],
) -> str:
    """Render `_site/index.html` (Course Hub + executable code preview + deep-dive callouts)."""
    chapter_titles_short = "、".join(f"{ch.badge} {ch.title.split('（')[0]}" for ch in chapters)
    index_desc_esc = html.escape(
        f"紫楓（AI王紫楓 / Purple Maple / tbpfs）開設之 Python 3.12 資料結構、演算法與物件導向基本功鐵人賽教學網站，完整收錄 {chapter_titles_short} 實機執行範例。"
    )
    index_og_desc_esc = html.escape(
        f"紫楓（AI王紫楓 / Purple Maple）Python 3.12 資料結構與演算法互動教學講義（{chapter_titles_short}）。"
    )
    all_keywords = ["紫楓", "AI王紫楓", "Purple Maple", "tbpfs", "Python教學", "資料結構", "演算法", "物件導向", "OOP"]
    for ch in chapters:
        for kw in ch.keywords:
            if kw not in all_keywords:
                all_keywords.append(kw)
    keywords_esc = html.escape(", ".join(all_keywords))
    json_ld_block = render_json_ld_script(build_index_json_ld(chapters, chapter_titles_short))

    toc_items_html = "\n".join(
        f"""      <a class="toc-item" href="#{ch.id}">
        <span class="badge">{html.escape(ch.badge)}</span>
        <strong>{html.escape(ch.title.split('（')[0])}</strong>
      </a>"""
        for ch in chapters
    )

    cards_html: list[str] = []
    for idx, ch in enumerate(chapters, start=1):
        source_code, live_output = exec_cache[ch.id]
        escaped_code = html.escape(source_code)
        escaped_out = html.escape(live_output)
        escaped_title = html.escape(ch.title)
        escaped_summary = html.escape(ch.summary)
        escaped_complexity = html.escape(ch.complexity)
        escaped_file = html.escape(ch.file)
        concepts_items = "\n".join(f"            <li>{html.escape(pt)}</li>" for pt in ch.concepts)
        callout_html = render_deep_dive_callout(ch)

        cards_html.append(
            f"""      <article class="chapter-card" id="{ch.id}">
        <div class="chapter-header">
          <span class="badge">{ch.badge}</span>
          <h2><a href="{ch.id}.html" style="color: inherit;">{escaped_title}</a></h2>
          <a href="{ch.id}.html" style="margin-left: auto; font-size: 0.86rem;">🔗 獨立章節講義 ↗</a>
        </div>
        <p class="chapter-summary">{escaped_summary}</p>
        <div class="concepts-box">
          <h3>💡 核心觀念與面試重點解析</h3>
          <ul>
{concepts_items}
          </ul>
        </div>
        <div class="meta-bar">
          <span>⏱️ <strong>時間／空間複雜度：</strong>{escaped_complexity}</span>
          <span>📄 <strong>原始碼路徑：</strong><code>{escaped_file}</code></span>
        </div>
        <div class="code-container">
          <div class="code-toolbar">
            <span>Python 3.12 範例實作（{escaped_file}）</span>
            <button type="button" class="copy-btn" data-target="code-{ch.id}">複製程式碼</button>
          </div>
          <pre><code id="code-{ch.id}">{escaped_code}</code></pre>
        </div>
        <div class="output-box">
          <div class="output-label">▶ 實機執行輸出驗證（CI 自動實測結果）</div>
          <pre class="output-pre">{escaped_out}</pre>
        </div>
{callout_html}
      </article>"""
        )
        cards_html.append(render_ad_slot(f"Ch.0{idx} 章節間廣告單元"))

    all_cards = "\n".join(cards_html)

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
  <meta name="keywords" content="{keywords_esc}">
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
  <style>
{SHARED_CSS}
  </style>
</head>
<body>
  <div class="container">
    <header class="hero">
      <span class="hero-eyebrow">鐵人賽基本功系列・資料結構 ＆ 演算法 ＆ 物件導向</span>
      <h1>從零開始寫程式，輕鬆搞懂資料結構，演算法</h1>
      <p>大家好，我是<strong>紫楓</strong>！不管是學生、想轉職軟體工程師、還是想精益求精的夥伴，練好「資料結構、演算法、物件導向」就是克服迷惘最紮實的基本功。</p>
      <div class="cta-group">
        <a class="btn btn-primary" href="https://www.youtube.com/playlist?list=PLhxdaTcUMi3nRM5mtOdQgO4VEtAEsTiYd" target="_blank" rel="noopener noreferrer">▶ 觀看 YouTube 完整教學播放清單</a>
        <a class="btn btn-secondary" href="https://ai-purplemaple.com/" target="_blank" rel="noopener noreferrer">🌸 紫楓 Purple Maple 官方作品集（AI 音樂 ＆ 白瀬アイリ Aily）</a>
        <a class="btn btn-secondary" href="https://www.facebook.com/groups/914880435669061" target="_blank" rel="noopener noreferrer">💬 加入程式新手學習發問區（FB 社團）</a>
        <a class="btn btn-secondary" href="https://github.com/tbpfs/learning" target="_blank" rel="noopener noreferrer">💻 GitHub 原始碼儲存庫</a>
      </div>
    </header>

    <nav class="toc" aria-label="章節快速導覽">
{toc_items_html}
    </nav>

    <main>
      <div id="cms-tutorials-container"></div>
{all_cards}

      <section class="study-guide-card" id="study-guide">
        <h2>🧭 軟體工程師基本功修煉指南與常見問答（FAQ）</h2>
        <p>許多初學者與轉職者在刷題（LeetCode）或準備技術面試時，常陷入「背題目卻不懂底層原理」的困境。建議依照以下三階段循序漸進：</p>
        <ul>
          <li><strong>第一階段（記憶體模型與線性結構）：</strong>先親手實作 Ch.01 的單向鏈結串列與 Ch.02 的 Stack / Queue，徹底理解指標（Reference / Pointer）操作與時間複雜度 <code>O(1)</code> vs. <code>O(n)</code> 的差異。</li>
          <li><strong>第二階段（遞迴分治、雜湊查找、樹與圖論架構）：</strong>透過 Ch.03 的二分搜尋與合併排序（Merge Sort）、Ch.04 的雜湊表（Hash Table / Two Sum）與二元搜尋樹（BST），再到 Ch.05 的圖論走訪（Graph BFS / DFS 最短路徑）與物件導向封裝（OOP），掌握分治法與空間換取時間的核心精神。</li>
          <li><strong>第三階段（面試壓軸進階：動態規劃與堆積 Top-K）：</strong>挑戰 Ch.06 的動態規劃（爬樓梯狀態壓縮、0/1 背包一維逆序更新、LIS 最長遞增子序列）與 Ch.07 的二元最小堆積（MinHeap、Top-K 篩選與 K 路歸併），並點入各章獨立講義研讀複雜度對照表與白板題詳解。</li>
        </ul>
      </section>
    </main>

{FOOTER_HTML}
  </div>

  <script>
{COPY_BUTTON_JS}

    if (typeof fetch === 'function') {{
      fetch('https://ai-purplemaple.com/api/v1/content')
        .then(function (r) {{ return r && r.ok ? r.json() : null; }})
        .then(function (payload) {{
          if (!payload || !payload.ok || !payload.content || !Array.isArray(payload.content.tutorials) || payload.content.tutorials.length === 0) return;
          var container = document.getElementById('cms-tutorials-container');
          if (!container) return;
          payload.content.tutorials.forEach(function (tut, idx) {{
            var sec = document.createElement('section');
            sec.className = 'chapter-card';
            var codeId = 'cms-code-' + idx;
            var header = document.createElement('div');
            header.className = 'chapter-header';
            var badge = document.createElement('span');
            badge.className = 'chapter-badge';
            badge.textContent = tut.category || 'AI 補充講義';
            var h2 = document.createElement('h2');
            h2.textContent = tut.title || '';
            header.appendChild(badge);
            header.appendChild(h2);

            var pSum = document.createElement('p');
            pSum.className = 'chapter-summary';
            pSum.textContent = (tut.summary || '') + (tut.explanation ? ' — ' + tut.explanation : '');

            var compRow = document.createElement('div');
            compRow.className = 'complexity-row';
            var pill = document.createElement('span');
            pill.className = 'complexity-pill';
            pill.textContent = tut.complexity || '時間 O(n) / 空間 O(1)';
            compRow.appendChild(pill);

            var wrap = document.createElement('div');
            wrap.className = 'code-wrapper';
            var bar = document.createElement('div');
            bar.className = 'code-toolbar';
            var fnSpan = document.createElement('span');
            fnSpan.className = 'code-filename';
            fnSpan.textContent = (tut.id || 'grok_note') + '.py';
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
          }});
          bindCopyButtons();
        }})
        .catch(function () {{}});
    }}
  </script>
</body>
</html>
"""


def render_chapter_page(
    idx: int,
    chapters: Sequence[ChapterSpec],
    exec_cache: dict[str, tuple[str, str]],
) -> str:
    """Render standalone deep-dive chapter page (`_site/ch01.html` .. `_site/ch07.html`)."""
    ch = chapters[idx]
    source_code, live_output = exec_cache[ch.id]
    ch_url = f"https://learn.ai-purplemaple.com/{ch.id}.html"
    ch_title_esc = html.escape(f"{ch.badge} {ch.title} | 紫楓 (AI王紫楓 / Purple Maple) Python 教學")
    ch_desc_esc = html.escape(f"紫楓（AI王紫楓 / Purple Maple）Python 3.12 教學講義：{ch.badge} {ch.title}。{ch.summary}")
    ch_keywords_esc = html.escape(", ".join(("紫楓", "AI王紫楓", "Purple Maple", "Python 3.12", *ch.keywords)))
    json_ld_block = render_json_ld_script(build_chapter_json_ld(ch))

    switcher_items: list[str] = []
    for item in chapters:
        current_attr = ' aria-current="page"' if item.id == ch.id else ""
        switcher_items.append(
            f"""      <a class="toc-item" href="{item.id}.html"{current_attr}>
        <span class="badge">{html.escape(item.badge)}</span>
        <strong>{html.escape(item.title.split('（')[0])}</strong>
      </a>"""
        )
    switcher_html = "\n".join(switcher_items)

    concepts_items = "\n".join(f"            <li>{html.escape(pt)}</li>" for pt in ch.concepts)
    table_html = render_comparison_table(ch.comparison_table)
    walkthrough_html = render_walkthrough(ch)
    pitfalls_html = render_pitfalls(ch)
    interview_html = render_interview_section(ch)
    pager_html = render_chapter_pager(idx, chapters)
    ad_mid = render_ad_slot(f"{ch.badge} 獨立講義中段廣告單元")
    ad_bottom = render_ad_slot(f"{ch.badge} 獨立講義結尾廣告單元")

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
  <style>
{SHARED_CSS}
  </style>
</head>
<body>
  <div class="container">
    <header class="hero">
      <span class="hero-eyebrow">鐵人賽基本功系列・{html.escape(ch.badge)} 獨立深度講義</span>
      <h1>{html.escape(ch.badge + " " + ch.title)}</h1>
      <p><a href="/">← 返回《從零開始寫程式，輕鬆搞懂資料結構，演算法》全章節總目錄</a></p>
      <p>{html.escape(ch.summary)}</p>
      <div class="cta-group">
        <a class="btn btn-primary" href="https://www.youtube.com/playlist?list=PLhxdaTcUMi3nRM5mtOdQgO4VEtAEsTiYd" target="_blank" rel="noopener noreferrer">▶ 觀看 YouTube 完整教學播放清單</a>
        <a class="btn btn-secondary" href="https://ai-purplemaple.com/" target="_blank" rel="noopener noreferrer">🌸 紫楓 Purple Maple 官方作品集</a>
        <a class="btn btn-secondary" href="https://github.com/tbpfs/learning/blob/main/{escaped_file}" target="_blank" rel="noopener noreferrer">💻 檢視本章 GitHub 原始碼</a>
      </div>
    </header>

    <nav class="toc" aria-label="全課程章節切換">
{switcher_html}
    </nav>

    <nav class="section-toc" aria-label="本章段落導覽">
      <a href="#overview">📖 背景導論與核心觀念</a>
      <a href="#comparison">📊 複雜度與特性對照表</a>
      <a href="#walkthrough">🔍 演算法逐步狀態拆解</a>
      <a href="#code-section">💻 Python 3.12 完整實作</a>
      <a href="#pitfalls">⚠️ CPython 底層原理與陷阱</a>
      <a href="#interview-faq">🎯 LeetCode 題號與面試 FAQ</a>
    </nav>

    <main>
      <article class="chapter-card" id="{ch.id}">
        <section id="overview">
          <h2>📖 本章背景導論與核心觀念解析</h2>
          <p class="deep-intro-text">{html.escape(ch.deep_intro)}</p>
          <div class="concepts-box">
            <h3>💡 核心觀念與面試重點解析</h3>
            <ul>
{concepts_items}
            </ul>
          </div>
          <div class="meta-bar">
            <span>⏱️ <strong>時間／空間複雜度：</strong>{escaped_complexity}</span>
            <span>📄 <strong>原始碼路徑：</strong><code>{escaped_file}</code></span>
            <span>🔄 <strong>最後更新：</strong>{html.escape(ch.lastmod)}</span>
          </div>
        </section>

        <section id="comparison">
          <h2>📊 時間與空間複雜度及底層特性對照表</h2>
{table_html}
        </section>

        <section id="walkthrough">
          <h2>🔍 {html.escape(ch.walkthrough_title)}</h2>
{walkthrough_html}
        </section>

{ad_mid}

        <section id="code-section">
          <h2>💻 Python 3.12 完整標準庫實作與實機輸出驗證</h2>
          <div class="code-container">
            <div class="code-toolbar">
              <span>Python 3.12 範例實作（{escaped_file}）</span>
              <button type="button" class="copy-btn" data-target="code-{ch.id}">複製程式碼</button>
            </div>
            <pre><code id="code-{ch.id}">{escaped_code}</code></pre>
          </div>
          <div class="output-box">
            <div class="output-label">▶ 實機執行輸出驗證（CI 自動實測結果）</div>
            <pre class="output-pre">{escaped_out}</pre>
          </div>
        </section>

        <section id="pitfalls">
          <h2>⚠️ Python 3.12 (CPython) 底層原理與實戰常見陷阱</h2>
{pitfalls_html}
        </section>

        <section id="interview-faq">
          <h2>🎯 LeetCode 必刷題號對照與技術面試 FAQ 詳解</h2>
{interview_html}
        </section>
      </article>

{ad_bottom}
{pager_html}
    </main>

{FOOTER_HTML}
  </div>

  <script>
{COPY_BUTTON_JS}
  </script>
</body>
</html>
"""


def format_markdown_table(table: ComparisonTable) -> str:
    """Format ComparisonTable as GitHub Flavored Markdown for llms-full.txt."""
    header_line = "| " + " | ".join(table.headers) + " |"
    sep_line = "| " + " | ".join("---" for _ in table.headers) + " |"
    row_lines = ["| " + " | ".join(row) + " |" for row in table.rows]
    return f"#### {table.caption}\n" + "\n".join([header_line, sep_line, *row_lines])


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
        ("https://learn.ai-purplemaple.com/", "1.0", "2026-11-17")
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
            f"  - **{st.step_label}** (`{st.state_snapshot}`): {st.explanation}"
            for st in ch.walkthrough_steps
        )
        pitfall_md = "\n".join(
            f"  - **{pf.title}**：{pf.symptom} → {pf.root_cause_and_fix}"
            for pf in ch.pitfalls
        )
        faq_md = "\n".join(
            f"  - **{faq.question}**\n    {faq.answer}"
            for faq in ch.interview_faqs
        )
        table_md = format_markdown_table(ch.comparison_table)

        llms_full_sections.append(
            f"## {ch.badge} {ch.title}\n"
            f"- **獨立章節網址**：{ch_url}\n"
            f"- **原始碼路徑**：`{ch.file}`\n"
            f"- **時間／空間複雜度**：{ch.complexity}\n"
            f"- **章節摘要**：{ch.summary}\n"
            f"- **背景導論**：{ch.deep_intro}\n"
            f"- **核心觀念與面試重點**：\n{concept_md}\n\n"
            f"{table_md}\n\n"
            f"### {ch.walkthrough_title}\n{walkthrough_md}\n\n"
            f"### Python 3.12 底層原理與常見陷阱\n{pitfall_md}\n\n"
            f"### 技術面試必考 FAQ\n{faq_md}\n\n"
            f"### Python 3.12 完整範例原始碼 (`{ch.file}`)\n"
            f"```python\n{source_code.rstrip()}\n```\n\n"
            f"### CI 實機執行輸出驗證\n"
            f"```text\n{live_output}\n```"
        )

    sitemap_urls.append(("https://learn.ai-purplemaple.com/llms.txt", "0.7", "2026-11-17"))
    sitemap_urls.append(("https://learn.ai-purplemaple.com/llms-full.txt", "0.8", "2026-11-17"))
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
        "- [YouTube 完整教學播放清單](https://www.youtube.com/playlist?list=PLhxdaTcUMi3nRM5mtOdQgO4VEtAEsTiYd)\n"
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
        f"> 本文件收錄 `https://learn.ai-purplemaple.com/` 全部 {len(CHAPTERS)} 章節（{chapter_titles_short}）之核心觀念、複雜度比較表、逐步狀態追蹤、Python 3.12 底層陷阱、面試 FAQ、完整標準庫實作原始碼及 CI 實機執行驗證輸出。精簡索引請見 `https://learn.ai-purplemaple.com/llms.txt`。\n\n"
        + "\n\n---\n\n".join(llms_full_sections)
        + "\n\n---\n\n"
        + ecosystem_footer_md,
        encoding="utf-8",
    )

    index_html = render_index_page(CHAPTERS, exec_cache)
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
