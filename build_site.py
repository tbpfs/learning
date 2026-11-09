#!/usr/bin/env python3
"""
build_site.py - Static Site Generator for GitHub Pages (`tbpfs/learning`).
Zero external dependencies. Reads examples/ch01..ch03, executes each to capture live output,
and renders a modern, self-contained HTML tutorial portal into `_site/index.html`.
"""

from __future__ import annotations

import argparse
import html
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

ADSENSE_PUBLISHER_ID = "pub-6485917848711473"
ADSENSE_CLIENT_ID = f"ca-{ADSENSE_PUBLISHER_ID}"

CHAPTERS = [
    {
        "id": "ch01",
        "badge": "Ch.01",
        "title": "陣列與單向鏈結串列（Array & Singly Linked List）",
        "complexity": "頭部插入 O(1) ・ 尾部附加 / 搜尋 / 刪除 / 原地反轉 O(n)",
        "summary": "理解連續記憶體配置（Array）與指標節點串接（Linked List）的本質差異，並以 Python Generic 型別實作單向鏈結串列的增刪查與 O(1) 額外空間原地反轉。",
        "concepts": [
            "連續記憶體 vs. 指標串接：陣列（Array / Python list）透過連續記憶體區塊支援 O(1) 隨機索引存取，但在頭部或中間插入元素需搬移後續元素（O(n)）；單向鏈結串列（Singly Linked List）則以 Node 節點與 next 指標動態串接，在已知頭節點時可於 O(1) 時間完成頭部插入（prepend）。",
            "白板題必考「原地反轉（In-place Reverse）」：透過 prev、curr、nxt 三個指標迭代翻轉 next 指向，不需額外建立新串列，空間複雜度嚴格控制在 O(1)，是軟體工程師面試最常出現的基礎題型。",
        ],
        "file": "examples/ch01_array_linked_list.py",
    },
    {
        "id": "ch02",
        "badge": "Ch.02",
        "title": "堆疊與佇列（Stack & Queue）",
        "complexity": "Push / Pop / Enqueue / Dequeue 均為 O(1)",
        "summary": "掌握後進先出（LIFO）與先進先出（FIFO）兩大抽象資料型態（ADT），並透過 Stack 實作經典的面試常考題：多層括號平衡檢查器。",
        "concepts": [
            "堆疊（Stack，後進先出 LIFO）：如同疊盤子，最後放入的元素最先取出。常用於函式呼叫堆疊（Call Stack）、瀏覽器上一頁紀錄、語法括號匹配檢查與深度優先搜尋（DFS）。",
            "佇列（Queue，先進先出 FIFO）：如同排隊買票，最先進入的元素最先處理。在 Python 中切勿使用 list.pop(0)（會導致 O(n) 記憶體搬移），應採用 collections.deque 雙端佇列達成真正的 O(1) 雙端操作，廣泛應用於廣度優先搜尋（BFS）與非同步任務佇列。",
        ],
        "file": "examples/ch02_stack_queue.py",
    },
    {
        "id": "ch03",
        "badge": "Ch.03",
        "title": "搜尋與排序演算法（Search & Sort Algorithms）",
        "complexity": "二分搜尋法 O(log n) ・ 合併排序法（Merge Sort）O(n log n)",
        "summary": "比較線性搜尋與二分搜尋的效率跨越，並以分治法（Divide & Conquer）實作穩定排序演算法 Merge Sort。",
        "concepts": [
            "二分搜尋法（Binary Search）：在「已排序」的序列中，每次比對中間元素即可排除一半搜尋範圍，將搜尋複雜度由線性 O(n) 大幅降至對數級 O(log n)（100 萬筆資料最多只需比對約 20 次）。",
            "合併排序法（Merge Sort）：經典的「分治法（Divide and Conquer）」演算法，先遞迴將陣列對半拆解至單一元素，再以雙指標（Two Pointers）線性合併兩個已排序子陣列。無論最佳、平均或最壞情況，時間複雜度皆穩定維持 O(n log n)，且具備穩定排序（Stable Sort）特性。",
        ],
        "file": "examples/ch03_search_sort.py",
    },
]


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
               data-ad-layout="in-article"
               data-ad-format="fluid"
               data-full-width-responsive="true"></ins>
          <script>
               (adsbygoogle = window.adsbygoogle || []).push({{}});
          </script>
        </div>
      </aside>"""


def build_site(out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")
    (out_dir / "CNAME").write_text("learn.ai-purplemaple.com\n", encoding="utf-8")
    (out_dir / "ads.txt").write_text(
        f"google.com, {ADSENSE_PUBLISHER_ID}, DIRECT, f08c47fec0942fa0\n",
        encoding="utf-8",
    )
    (out_dir / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\nSitemap: https://learn.ai-purplemaple.com/sitemap.xml\n",
        encoding="utf-8",
    )
    (out_dir / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        '  <url>\n'
        '    <loc>https://learn.ai-purplemaple.com/</loc>\n'
        '    <changefreq>monthly</changefreq>\n'
        '    <priority>1.0</priority>\n'
        '  </url>\n'
        '</urlset>\n',
        encoding="utf-8",
    )

    cards_html: list[str] = []
    for idx, ch in enumerate(CHAPTERS, start=1):
        source_code, live_output = run_example(ch["file"])
        escaped_code = html.escape(source_code)
        escaped_out = html.escape(live_output)
        escaped_title = html.escape(ch["title"])
        escaped_summary = html.escape(ch["summary"])
        escaped_complexity = html.escape(ch["complexity"])
        escaped_file = html.escape(ch["file"])
        concepts_items = "\n".join(
            f"            <li>{html.escape(pt)}</li>" for pt in ch.get("concepts", [])
        )

        cards_html.append(
            f"""
      <article class="chapter-card" id="{ch['id']}">
        <div class="chapter-header">
          <span class="badge">{ch['badge']}</span>
          <h2>{escaped_title}</h2>
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
            <button type="button" class="copy-btn" data-target="code-{ch['id']}">複製程式碼</button>
          </div>
          <pre><code id="code-{ch['id']}">{escaped_code}</code></pre>
        </div>
        <div class="output-box">
          <div class="output-label">▶ 實機執行輸出驗證（CI 自動實測結果）</div>
          <pre class="output-pre">{escaped_out}</pre>
        </div>
      </article>"""
        )
        # 在各章節之間插入 AdSense 內嵌廣告單元（與程式碼執行區保持安全間距）
        cards_html.append(render_ad_slot(f"Ch.0{idx} 章節間廣告單元"))

    all_cards = "\n".join(cards_html)

    page_html = f"""<!DOCTYPE html>
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
  <meta name="description" content="紫楓（AI王紫楓 / Purple Maple / tbpfs）開設之 Python 資料結構、演算法與物件導向基本功鐵人賽教學網站與實機執行範例（陣列、鏈結串列、堆疊、佇列、二分搜尋、合併排序）。">
  <meta name="keywords" content="紫楓, AI王紫楓, Purple Maple, tbpfs, Python教學, 資料結構, 演算法, 鏈結串列, 堆疊, 佇列, 二分搜尋, Merge Sort">
  <meta name="google-adsense-account" content="{ADSENSE_CLIENT_ID}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT_ID}" crossorigin="anonymous"></script>
  <link rel="canonical" href="https://learn.ai-purplemaple.com/">
  <meta property="og:site_name" content="紫楓 Purple Maple Python 程式教學">
  <meta property="og:url" content="https://learn.ai-purplemaple.com/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="從零開始寫程式，輕鬆搞懂資料結構、演算法 | 紫楓 (Purple Maple)">
  <meta property="og:description" content="紫楓（AI王紫楓 / Purple Maple）Python 3.12 資料結構與演算法互動教學講義。">
  <meta property="og:image" content="https://ai-purplemaple.com/assets/gallery/aily_03.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@tbpfs1">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Course",
    "name": "從零開始寫程式，輕鬆搞懂資料結構、演算法",
    "description": "紫楓（AI王紫楓 / Purple Maple）開設之 Python 資料結構與演算法實戰教學課程，涵蓋 Array、Linked List、Stack、Queue、Binary Search 與 Merge Sort。",
    "url": "https://learn.ai-purplemaple.com/",
    "inLanguage": "zh-TW",
    "provider": {{
      "@type": "Person",
      "name": "紫楓 (AI王紫楓 / Purple Maple)",
      "url": "https://ai-purplemaple.com/"
    }}
  }}
  </script>
  <style>
    :root {{
      --bg: #0f101a;
      --surface: #181a29;
      --surface-alt: #1f2235;
      --border: #2e334d;
      --text: #eef0f7;
      --muted: #aab1cc;
      --accent: #a78bfa;
      --accent-strong: #8b5cf6;
      --success: #34d399;
      --code-bg: #11131f;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans TC", sans-serif;
      background: radial-gradient(circle at top, #1b1734 0%, var(--bg) 55%);
      color: var(--text);
      line-height: 1.65;
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .container {{
      max-width: 980px;
      margin: 0 auto;
      padding: 2.5rem 1.25rem 4rem;
    }}
    header.hero {{
      background: linear-gradient(135deg, rgba(139, 92, 246, 0.16), rgba(31, 34, 53, 0.92));
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 2.25rem 2rem;
      margin-bottom: 2.25rem;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.32);
    }}
    .hero-eyebrow {{
      display: inline-block;
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--accent);
      background: rgba(167, 139, 250, 0.12);
      border: 1px solid rgba(167, 139, 250, 0.35);
      padding: 0.25rem 0.75rem;
      border-radius: 999px;
      margin-bottom: 0.75rem;
    }}
    .hero h1 {{
      margin: 0 0 0.75rem;
      font-size: clamp(1.6rem, 3.2vw, 2.25rem);
      line-height: 1.3;
    }}
    .hero p {{
      margin: 0.5rem 0;
      color: var(--muted);
    }}
    .cta-group {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.85rem;
      margin-top: 1.5rem;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.65rem 1.2rem;
      border-radius: 10px;
      font-weight: 600;
      font-size: 0.95rem;
      transition: transform 0.15s ease, background 0.15s ease;
    }}
    .btn:hover {{
      transform: translateY(-1px);
      text-decoration: none;
    }}
    .btn-primary {{
      background: var(--accent-strong);
      color: #ffffff;
    }}
    .btn-secondary {{
      background: var(--surface-alt);
      color: var(--text);
      border: 1px solid var(--border);
    }}
    nav.toc {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1rem;
      margin-bottom: 2.25rem;
    }}
    .toc-item {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1rem 1.2rem;
      display: block;
      transition: border-color 0.15s ease;
    }}
    .toc-item:hover {{
      border-color: var(--accent);
      text-decoration: none;
    }}
    .toc-item strong {{
      display: block;
      color: var(--text);
      margin-top: 0.25rem;
    }}
    .chapter-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 1.75rem;
      margin-bottom: 2rem;
    }}
    .chapter-header {{
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-bottom: 0.65rem;
    }}
    .badge {{
      background: rgba(167, 139, 250, 0.18);
      color: var(--accent);
      border: 1px solid rgba(167, 139, 250, 0.4);
      padding: 0.2rem 0.65rem;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.85rem;
    }}
    .chapter-header h2 {{
      margin: 0;
      font-size: 1.35rem;
    }}
    .chapter-summary {{
      color: var(--muted);
      margin: 0.5rem 0 1rem;
    }}
    .meta-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 1.25rem;
      font-size: 0.9rem;
      color: var(--muted);
      background: var(--surface-alt);
      padding: 0.65rem 1rem;
      border-radius: 10px;
      margin-bottom: 1rem;
    }}
    .code-container {{
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      background: var(--code-bg);
      margin-bottom: 1rem;
    }}
    .code-toolbar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.55rem 1rem;
      background: #16192b;
      border-bottom: 1px solid var(--border);
      font-size: 0.85rem;
      color: var(--muted);
    }}
    .copy-btn {{
      background: var(--surface-alt);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 0.28rem 0.7rem;
      font-size: 0.8rem;
      cursor: pointer;
    }}
    .copy-btn:hover {{
      border-color: var(--accent);
    }}
    pre {{
      margin: 0;
      padding: 1rem 1.2rem;
      overflow-x: auto;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.86rem;
      line-height: 1.55;
    }}
    .output-box {{
      background: rgba(52, 211, 153, 0.07);
      border: 1px solid rgba(52, 211, 153, 0.3);
      border-radius: 10px;
      padding: 0.75rem 1rem;
    }}
    .output-label {{
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--success);
      margin-bottom: 0.35rem;
    }}
    .output-pre {{
      padding: 0;
      color: #d1fae5;
      background: transparent;
    }}
    .concepts-box {{
      background: rgba(167, 139, 250, 0.06);
      border-left: 3px solid var(--accent);
      border-radius: 8px;
      padding: 0.85rem 1.15rem;
      margin-bottom: 1rem;
    }}
    .concepts-box h3 {{
      margin: 0 0 0.45rem;
      font-size: 0.95rem;
      color: var(--accent);
    }}
    .concepts-box ul {{
      margin: 0;
      padding-left: 1.2rem;
      color: var(--muted);
      font-size: 0.9rem;
    }}
    .concepts-box li {{
      margin-bottom: 0.35rem;
    }}
    .ad-slot-card {{
      background: rgba(24, 26, 41, 0.75);
      border: 1px dashed var(--border);
      border-radius: 14px;
      padding: 1rem 1.25rem;
      margin: 1.75rem 0 2.25rem;
      min-height: 140px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    .ad-slot-label {{
      font-size: 0.72rem;
      letter-spacing: 0.08em;
      color: var(--muted);
      text-align: center;
      margin-bottom: 0.5rem;
      opacity: 0.75;
    }}
    .ad-slot-inner {{
      min-height: 90px;
      width: 100%;
    }}
    .study-guide-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 1.75rem;
      margin-top: 2rem;
      margin-bottom: 2rem;
    }}
    .study-guide-card h2 {{
      margin-top: 0;
      font-size: 1.3rem;
      color: var(--text);
    }}
    .study-guide-card p, .study-guide-card li {{
      color: var(--muted);
      font-size: 0.94rem;
    }}
    .privacy-policy-card {{
      background: rgba(24, 26, 41, 0.6);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
      margin-bottom: 1.5rem;
      text-align: left;
    }}
    .privacy-policy-card h3 {{
      margin: 0 0 0.5rem;
      font-size: 0.95rem;
      color: var(--accent);
    }}
    .privacy-policy-card p {{
      margin: 0 0 0.5rem;
      font-size: 0.84rem;
      line-height: 1.65;
      color: var(--muted);
    }}
    footer {{
      text-align: center;
      color: var(--muted);
      font-size: 0.88rem;
      margin-top: 3rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border);
    }}
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
        <a class="btn btn-secondary" href="https://www.facebook.com/groups/914880435669061" target="_blank" rel="noopener noreferrer">💬 加入程式新手學習發問區（FB 社團）</a>
        <a class="btn btn-secondary" href="https://github.com/tbpfs/learning" target="_blank" rel="noopener noreferrer">💻 GitHub 原始碼儲存庫</a>
      </div>
    </header>

    <nav class="toc" aria-label="章節快速導覽">
      <a class="toc-item" href="#ch01">
        <span class="badge">Ch.01</span>
        <strong>陣列與單向鏈結串列</strong>
      </a>
      <a class="toc-item" href="#ch02">
        <span class="badge">Ch.02</span>
        <strong>堆疊與佇列（含括號平衡檢查）</strong>
      </a>
      <a class="toc-item" href="#ch03">
        <span class="badge">Ch.03</span>
        <strong>二分搜尋法與合併排序法</strong>
      </a>
    </nav>

    <main>
{all_cards}

      <section class="study-guide-card" id="study-guide">
        <h2>🧭 軟體工程師基本功修煉指南與常見問答（FAQ）</h2>
        <p>許多初學者與轉職者在刷題（LeetCode）或準備技術面試時，常陷入「背題目卻不懂底層原理」的困境。建議依照以下三階段循序漸進：</p>
        <ul>
          <li><strong>第一階段（記憶體模型與線性結構）：</strong>先親手實作 Ch.01 的單向鏈結串列與 Ch.02 的 Stack / Queue，徹底理解指標（Reference / Pointer）操作與時間複雜度 <code>O(1)</code> vs. <code>O(n)</code> 的差異。</li>
          <li><strong>第二階段（遞迴思維與分治演算法）：</strong>透過 Ch.03 的二分搜尋法與合併排序法（Merge Sort），掌握將大問題拆解為子問題的 Divide &amp; Conquer 核心精神，並練習分析遞迴樹深度 <code>O(log n)</code>。</li>
          <li><strong>第三階段（搭配影音逐步除錯）：</strong>複製上方 Python 3.12 範例至本機執行，嘗試自己加入印出節點狀態的 <code>print()</code>，並搭配紫楓的 YouTube 鐵人賽教學影片對照學習。</li>
        </ul>
      </section>
    </main>

    <footer id="privacy">
      <div class="privacy-policy-card">
        <h3>隱私權政策與 Cookie 聲明 (Privacy Policy)</h3>
        <p>本網站（learn.ai-purplemaple.com）使用 Google AdSense 第三方廣告服務與 Google Analytics (GA4)／Google Tag Manager 網站流量分析服務。Google 及其合作夥伴會使用 Cookie（包含 DART Cookie），根據使用者造訪本站或其他網站的紀錄提供個人化廣告與匿名流量統計。您可隨時前往 <a href="https://adssettings.google.com/" target="_blank" rel="noopener noreferrer">Google 廣告設定頁面</a> 停用個人化廣告，或查閱 <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener noreferrer">Google 廣告與隱私權政策</a>。本站程式碼複製功能均於瀏覽器本機執行，不會收集或儲存您的個人識別資料。</p>
      </div>
      <p>Created by <strong><a href="https://ai-purplemaple.com/">紫楓 (Purple Maple)</a></strong> ・ Powered by Python 3.12 &amp; GitHub Pages ・ <a href="ads.txt">ads.txt</a></p>
    </footer>
  </div>

  <script>
    document.querySelectorAll('.copy-btn').forEach(function (btn) {{
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
  </script>
</body>
</html>
"""

    index_path = out_dir / "index.html"
    index_path.write_text(page_html, encoding="utf-8")
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
