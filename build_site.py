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

CHAPTERS = [
    {
        "id": "ch01",
        "badge": "Ch.01",
        "title": "陣列與單向鏈結串列（Array & Singly Linked List）",
        "complexity": "頭部插入 O(1) ・ 尾部附加 / 搜尋 / 刪除 / 原地反轉 O(n)",
        "summary": "理解連續記憶體配置（Array）與指標節點串接（Linked List）的本質差異，並以 Python Generic 型別實作單向鏈結串列的增刪查與 O(1) 額外空間原地反轉。",
        "file": "examples/ch01_array_linked_list.py",
    },
    {
        "id": "ch02",
        "badge": "Ch.02",
        "title": "堆疊與佇列（Stack & Queue）",
        "complexity": "Push / Pop / Enqueue / Dequeue 均為 O(1)",
        "summary": "掌握後進先出（LIFO）與先進先出（FIFO）兩大抽象資料型態（ADT），並透過 Stack 實作經典的面試常考題：多層括號平衡檢查器。",
        "file": "examples/ch02_stack_queue.py",
    },
    {
        "id": "ch03",
        "badge": "Ch.03",
        "title": "搜尋與排序演算法（Search & Sort Algorithms）",
        "complexity": "二分搜尋法 O(log n) ・ 合併排序法（Merge Sort）O(n log n)",
        "summary": "比較線性搜尋與二分搜尋的效率跨越，並以分治法（Divide & Conquer）實作穩定排序演算法 Merge Sort。",
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


def build_site(out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")

    cards_html: list[str] = []
    for ch in CHAPTERS:
        source_code, live_output = run_example(ch["file"])
        escaped_code = html.escape(source_code)
        escaped_out = html.escape(live_output)
        escaped_title = html.escape(ch["title"])
        escaped_summary = html.escape(ch["summary"])
        escaped_complexity = html.escape(ch["complexity"])
        escaped_file = html.escape(ch["file"])

        cards_html.append(
            f"""
      <article class="chapter-card" id="{ch['id']}">
        <div class="chapter-header">
          <span class="badge">{ch['badge']}</span>
          <h2>{escaped_title}</h2>
        </div>
        <p class="chapter-summary">{escaped_summary}</p>
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

    all_cards = "\n".join(cards_html)

    page_html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>從零開始寫程式，輕鬆搞懂資料結構、演算法 | 紫楓 (Purple Maple)</title>
  <meta name="description" content="紫楓開設之資料結構、演算法與物件導向基本功鐵人賽教學網站與 Python 實作範例。">
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
    </main>

    <footer>
      <p>Created by <strong>紫楓 (Purple Maple)</strong> ・ Powered by Python 3.12 &amp; GitHub Pages</p>
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
