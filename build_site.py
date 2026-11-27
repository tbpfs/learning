#!/usr/bin/env python3
"""
build_site.py - Static Site Generator for GitHub Pages (`tbpfs/learning`).
Zero external dependencies. Reads examples/ch01..ch07, executes each once to capture live output,
and renders a 24-page trilingual SEO/GEO-optimized tutorial portal:
- `/` + `ch01.html`..`ch07.html` (Traditional Chinese, zh-Hant)
- `/zh-cn/` + `/zh-cn/ch01.html`..`ch07.html` (Mainland Simplified Chinese, zh-Hans)
- `/en/` + `/en/ch01.html`..`ch07.html` (International English, en)
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence
from xml.sax.saxutils import escape as xml_escape

REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from affiliate_config import (  # noqa: E402
    AffiliateResource,
    get_chapter_book_recommendation,
    get_learning_resources,
)
from book_models import (  # noqa: E402
    BookChapterData,
    BookComparisonTable,
    FB_GROUP_URL,
    GITHUB_ISSUES_URL,
    LoadedBook,
    discover_books,
    validate_svg_safe,
)
from chapter_content import CHAPTERS, ChapterSpec, ComparisonTable  # noqa: E402
from i18n import (  # noqa: E402
    LOCALE_BY_CODE,
    LOCALES,
    SITE_BASE_URL,
    asset_canonical_url,
    asset_root_href,
    load_locale_pack,
    localize_code_and_output,
    page_canonical_url,
    page_root_href,
)

ADSENSE_PUBLISHER_ID = "pub-6485917848711473"
ADSENSE_CLIENT_ID = f"ca-{ADSENSE_PUBLISHER_ID}"
ADSENSE_IN_ARTICLE_SLOT_ID = "1673180799"
ENABLE_MANUAL_AD_SLOTS = False  # Pre-approval SEO/UX hygiene: keep <head> verification script + ads.txt, hide empty dashed <ins> boxes until approved
INDEXNOW_KEY = "7f4e9c2a8b1d6035e4a92c7f1b8d3e60"
SITE_LASTMOD = "2026-11-26"
DSA_DATE_PUBLISHED = "2026-03-01"
_TZ_TAIPEI = timezone(timedelta(hours=8))

RSS_FEED_META: dict[str, dict[str, str]] = {
    "zh-TW": {
        "rel_out": "rss.xml",
        "url": f"{SITE_BASE_URL}/rss.xml",
        "link": f"{SITE_BASE_URL}/",
        "lang": "zh-Hant",
        "title": "紫楓出版社｜AI 工程與 Python 技術專書 RSS (繁體中文)",
        "description": "紫楓出版社（Purple Maple Press）免費開源技術專書與 Python 3.12 資料結構演算法講義最新章節摘要 Feed，含實機驗證程式碼與架構圖解導覽。",
        "pub_label": "發布日期：",
        "upd_label": "最後更新：",
    },
    "zh-CN": {
        "rel_out": "zh-cn/rss.xml",
        "url": f"{SITE_BASE_URL}/zh-cn/rss.xml",
        "link": f"{SITE_BASE_URL}/zh-cn/",
        "lang": "zh-Hans",
        "title": "紫枫出版社｜AI 工程与 Python 技术专著 RSS (简体中文)",
        "description": "紫枫出版社（Purple Maple Press）免费开源技术专著与 Python 3.12 数据结构算法讲义最新章节摘要 Feed，含源码实战与架构图解导览。",
        "pub_label": "发布日期：",
        "upd_label": "最后更新：",
    },
    "en": {
        "rel_out": "en/rss.xml",
        "url": f"{SITE_BASE_URL}/en/rss.xml",
        "link": f"{SITE_BASE_URL}/en/",
        "lang": "en",
        "title": "Purple Maple Press | AI Engineering & Python Monographs RSS (English)",
        "description": "Summary RSS feed of new chapters from Purple Maple Press open-source technical monographs and Python 3.12 data structures & algorithms guides.",
        "pub_label": "Published: ",
        "upd_label": "Updated: ",
    },
}


def render_rss_alternate_link(locale_code: str) -> str:
    meta = RSS_FEED_META[locale_code]
    return (
        f'  <link rel="alternate" type="application/rss+xml" '
        f'href="{html.escape(meta["url"])}" title="{html.escape(meta["title"])}">'
    )


def render_dates_meta_html(locale_code: str, date_published: str, date_modified: str) -> str:
    meta = RSS_FEED_META[locale_code]
    pub = html.escape(date_published)
    mod = html.escape(date_modified)
    return (
        f'<span><strong>{html.escape(meta["pub_label"])}</strong><time datetime="{pub}">{pub}</time></span>\n'
        f'          <span><strong>{html.escape(meta["upd_label"])}</strong><time datetime="{mod}">{mod}</time></span>'
    )


def _date_to_rfc2822(date_str: str) -> str:
    try:
        dt = datetime.strptime(date_str[:10], "%Y-%m-%d").replace(tzinfo=_TZ_TAIPEI)
    except ValueError:
        dt = datetime(2026, 11, 25, tzinfo=_TZ_TAIPEI)
    return format_datetime(dt)


def _rss_excerpt(text: str, max_len: int = 240) -> str:
    clean = " ".join(text.split())
    if len(clean) <= max_len:
        return clean
    return clean[: max_len - 1].rstrip(" ，,。.;；:：") + "…"


def build_rss_xml(locale_code: str, items: Sequence[dict[str, str]], limit: int = 30) -> str:
    meta = RSS_FEED_META[locale_code]
    sorted_items = sorted(
        items,
        key=lambda x: (x["pub_date"], x["sort_key"]),
        reverse=True,
    )[:limit]
    latest_mod = max((x["mod_date"] for x in sorted_items), default=SITE_LASTMOD)
    item_blocks: list[str] = []
    for it in sorted_items:
        item_blocks.append(
            "    <item>\n"
            f"      <title>{xml_escape(it['title'])}</title>\n"
            f"      <link>{xml_escape(it['link'])}</link>\n"
            f'      <guid isPermaLink="true">{xml_escape(it["link"])}</guid>\n'
            f"      <pubDate>{xml_escape(_date_to_rfc2822(it['pub_date']))}</pubDate>\n"
            f"      <description>{xml_escape(_rss_excerpt(it['summary']))}</description>\n"
            "    </item>"
        )
    items_xml = "\n".join(item_blocks)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        f"    <title>{xml_escape(meta['title'])}</title>\n"
        f"    <link>{xml_escape(meta['link'])}</link>\n"
        f"    <description>{xml_escape(meta['description'])}</description>\n"
        f"    <language>{xml_escape(meta['lang'])}</language>\n"
        f"    <lastBuildDate>{xml_escape(_date_to_rfc2822(latest_mod))}</lastBuildDate>\n"
        f'    <atom:link href="{xml_escape(meta["url"])}" rel="self" type="application/rss+xml" />\n'
        f"{items_xml}\n"
        "  </channel>\n"
        "</rss>\n"
    )

CREATOR_SAME_AS: list[str] = [
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
]

CHAPTER_YOUTUBE_VIDEOS: dict[str, dict[str, Any]] = {
    "ch01": {
        "video_id": "-LmHUlozTqE",
        "title": "[軟體工程師雜談] 輕鬆搞懂資料結構: Array(陣列), Linked list(連結串列) | IT鐵人賽",
        "upload_date": "2020-09-12T12:00:00+08:00",
        "views_label": "67,700+ 次觀看",
        "related": [
            ("YGZ1S79628s", "【零基礎生活圖解】用「兩排矮到高排隊合併」3分鐘看懂合併排序串列 (LeetCode #21)"),
            ("o2q_HCyf16U", "【零基礎生活圖解】用「固定長度尺子量距離」3分鐘一趟刪除倒數第N站 (LeetCode #19)"),
            ("ov_WvWbEryg", "【零基礎生活圖解】用「操場龜兔賽跑」3分鐘看懂鏈結串列環路檢測 (LeetCode #141)"),
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
            ("wRa59B9N11Q", "【零基礎生活圖解】用「雙筒最低價小抄」3分鐘看懂最小堆疊 Min Stack (LeetCode #155)"),
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
            ("sFypmieNopU", "【零基礎生活圖解】用「VIP包廂守門員」3分鐘看懂堆積 Heap 與 Top-K (LeetCode #215)"),
            ("fHBw99bYLuo", "堆積排序 (Heap Sort)、基數排序、桶排序詳解（13,200+ 觀看）"),
        ],
    },
}

UI_ZH_TW: dict[str, Any] = {
    "site_name": "紫楓 Purple Maple Python 程式教學",
    "brand_creator_name": "紫楓 (AI王紫楓 / Purple Maple)",
    "brand_website_name": "紫楓官方網站｜王紫楓 (Purple Maple)",
    "brand_anchor_portfolio": "王紫楓（紫楓 / Purple Maple）官方作品集（AI 音樂 ＆ 白瀬アイリ Aily）",
    "brand_anchor_portfolio_short": "王紫楓（紫楓 / Purple Maple）官方作品集",
    "brand_anchor_footer": "王紫楓（紫楓 / Purple Maple）",
    "page_title": "從零開始寫程式，輕鬆搞懂資料結構、演算法 | 紫楓 (AI王紫楓 / Purple Maple)",
    "og_title": "從零開始寫程式，輕鬆搞懂資料結構、演算法 | 紫楓 (Purple Maple)",
    "hero_eyebrow": "鐵人賽基本功系列・資料結構 ＆ 演算法 ＆ 物件導向",
    "hero_h1": "從零開始寫程式，輕鬆搞懂資料結構，演算法",
    "hero_intro_html": (
        "大家好，我是<strong>紫楓</strong>！不管是學生、想轉職軟體工程師、還是想精益求精的夥伴，"
        "練好「資料結構、演算法、物件導向」就是克服迷惘最紮實的基本功。"
    ),
    "cta_youtube": "▶ 觀看 YouTube 完整教學播放清單",
    "cta_fb_group": "加入程式與 AI 學習發問社團（FB）",
    "cta_github": "GitHub 原始碼儲存庫",
    "cta_chapter_github": "檢視本章 GitHub 原始碼",
    "og_image_alt": "紫楓（AI王紫楓 / @tbpfs1）Python 資料結構與演算法互動教學｜原創看板娘白瀬アイリ（左紅 #fb7185、右藍 #38bdf8）",
    "index_keywords": (
        "紫楓, AI王紫楓, Purple Maple, tbpfs, Python教學, 資料結構, 演算法, 鏈結串列, 堆疊, 佇列, "
        "二分搜尋, Merge Sort, 雜湊表, Hash Table, 二元搜尋樹, BST, 圖論, BFS, DFS, 動態規劃, "
        "Dynamic Programming, 堆積, Heap, Priority Queue, Top-K, 物件導向, OOP"
    ),
    "index_desc_tpl": (
        "紫楓（AI王紫楓 / Purple Maple / tbpfs）開設之 Python 3.12 資料結構、演算法與物件導向基本功鐵人賽教學網站，"
        "完整收錄 {chapter_titles_short} 實機執行範例。"
    ),
    "index_og_desc_tpl": "紫楓（AI王紫楓 / Purple Maple）Python 3.12 資料結構與演算法互動教學講義（{chapter_titles_short}）。",
    "course_name": "從零開始寫程式，輕鬆搞懂資料結構、演算法",
    "course_desc_tpl": (
        "紫楓（AI王紫楓 / Purple Maple）開設之 Python 3.12 資料結構、演算法與物件導向實戰教學課程，"
        "涵蓋 {chapter_titles_short}。"
    ),
    "index_aeo_capsule": (
        "紫楓（AI王紫楓 / Purple Maple）Python 3.12 互動教學站（<code>ai-purplemaple.com/learn/</code>）"
        "收錄 7 大核心章節（陣列鏈結串列、堆疊佇列、二分搜尋與 Merge Sort、雜湊表與 BST、圖論 BFS/DFS 與 OOP、"
        "動態規劃、二元堆積與 Top-K），每章皆附實機執行輸出、複雜度表、CPython 陷阱與 LeetCode 面試詳解，完全免費開源。"
    ),
    "toc_aria": "章節快速導覽",
    "chapter_switcher_aria": "全課程章節切換",
    "section_subnav_aria": "本章段落導覽",
    "section_subnav_label": "本章快速跳轉：",
    "nav_intro": "核心觀念與背景導論",
    "nav_video": "YouTube 實戰教學影片",
    "nav_comparison": "複雜度與特性對照表",
    "nav_walkthrough": "逐步狀態拆解",
    "nav_code": "Python 3.12 完整實作",
    "nav_pitfalls": "CPython 底層陷阱",
    "nav_interview": "LeetCode 題號與面試 FAQ",
    "chapter_link_cta": "獨立章節深度講義 ↗",
    "concepts_heading": "核心觀念與面試重點解析",
    "label_complexity": "時間／空間複雜度：",
    "label_source_path": "原始碼路徑：",
    "code_accordion_summary_tpl": "點擊展開／收合 {badge} Python 3.12 完整實作原始碼與實機執行輸出（<code>{file}</code>）",
    "code_toolbar_tpl": "Python 3.12 範例實作（{file}）",
    "copy_btn": "複製程式碼",
    "output_label_index": "▶ 實機執行驗證輸出",
    "output_label_chapter": "▶ 實機執行輸出驗證（Python 3.12 實測結果）",
    "deep_dive_summary_tpl": "{badge} 獨立深度講義獨家收錄內容（點擊展開／收合預覽）",
    "deep_dive_table_label": "完整結構化對照表：",
    "deep_dive_faq_label": "本章軟體工程師面試必考問答預告：",
    "deep_dive_cta_tpl": "閱讀 {badge} 完整深度講義（複雜度表 ＋ 逐步圖解 ＋ 面試詳解） →",
    "chapter_title_tpl": "{short_title}｜Python 3.12 互動圖解教學（{badge}）",
    "chapter_desc_tpl": "{summary} 附免費互動視覺化與面試問答。",
    "chapter_keywords_prefix": "紫楓, AI王紫楓, Purple Maple, Python 3.12 教學, ",
    "chapter_eyebrow_tpl": "{badge} 獨立深度講義・Python 3.12 資料結構與演算法實戰",
    "back_to_index_label": "← 返回《從零開始寫程式，輕鬆搞懂資料結構，演算法》全章節總目錄",
    "chapter_intro_heading": "本章背景導論與工程應用場景",
    "chapter_aeo_tpl": (
        "{badge}〈{title}〉的核心目標在於掌握 {summary} 時間／空間複雜度基準為 <code>{complexity}</code>，"
        "並以 Python 3.12 標準庫（<code>{file}</code>）提供零依賴實機驗證範例。"
    ),
    "comparison_heading": "時間與空間複雜度暨底層結構對照表",
    "code_section_heading": "Python 3.12 標準庫完整範例實作與實機輸出",
    "pitfalls_heading": "Python 3.12 底層實作原理與常見實戰陷阱",
    "pitfall_symptom_label": "常見錯誤現象：",
    "pitfall_fix_label": "CPython 底層根因與正確對策：",
    "interview_heading": "LeetCode 經典必刷題號與軟體工程師技術面試 FAQ",
    "interview_table_caption_tpl": "{badge} 對應 LeetCode 必考白板題與解題模板",
    "interview_th_num": "題號",
    "interview_th_title": "題目名稱",
    "interview_th_diff": "難度",
    "interview_th_pattern": "核心解題模式與複雜度",
    "video_heading_tpl": "本章對應 YouTube 實戰教學影片（{views_label}）",
    "video_intro": "建議先觀看紫楓 IT 鐵人賽對應影片建立直覺圖像記憶，再對照下方複雜度表與 Python 3.12 標準庫程式碼動手實作：",
    "video_main_label": "主講影片：",
    "video_playlist_cta": "31 集完整鐵人賽播放清單 ↗",
    "video_related_heading": "本章延伸 YouTube 鐵人賽專題教學影片",
    "video_desc_tpl": "紫楓（AI王紫楓 / Purple Maple）IT 鐵人賽實戰教學影片：{badge} {title}。{summary}",
    "tech_article_headline_tpl": "{badge} {title} — Python 3.12 資料結構與演算法深度講義",
    "breadcrumb_home_name": "Python 資料結構與演算法總目錄",
    "resources_heading": "紫楓嚴選：Python 資料結構與演算法實體書／線上課程比較表",
    "resources_note": "合作揭露：以下部分連結為博客來策略聯盟（AP）或合作夥伴推廣連結，透過連結購書或報名課程不會增加您的任何費用，我們可能獲得微薄分潤以支持本站免費開源講義維護。",
    "resources_th_title": "推薦書籍／課程",
    "resources_th_platform": "平台",
    "resources_th_audience": "適合對象",
    "resources_th_highlight": "與本站章節對應重點",
    "resources_th_action": "前往查看",
    "chapter_resource_aria": "本章延伸書單推薦",
    "chapter_resource_note": "合作揭露：此為博客來策略聯盟推廣連結，購書價格與原價相同，您的支持將協助本站持續更新免費 Python 教學講義。",
    "chapter_resource_cta": "前往博客來查找相關書單 ↗",
    "fb_question": "這篇講義對你有幫助嗎？",
    "fb_yes": "✓ 有幫助",
    "fb_no": "待改進",
    "fb_note_placeholder": "選填：哪一段清楚或卡關？（最多 200 字，不公開）",
    "fb_note_aria": "選填原因（不公開）",
    "fb_note_submit": "送出回饋",
    "fb_ask_summary": "還有程式觀念卡關？匿名提問給紫楓（整理進本章 FAQ）",
    "fb_ask_sub": "為維持閱讀版面純淨、杜絕廣告留言，提問不會直接公開；站長審閱後會將高頻問題補入本章技術 FAQ。",
    "fb_ask_placeholder": "輸入你的疑問，例如：為什麼這段時間複雜度是 O(log n)…",
    "fb_ask_aria": "匿名提問內容",
    "fb_ask_submit": "送出提問",
    "pager_aria": "上下章節導覽",
    "pager_prev_tpl": "← 上一章：{badge} {short}",
    "pager_first": "← 已是第一章",
    "pager_home": "返回全章節總目錄",
    "pager_next_tpl": "下一章：{badge} {short} →",
    "pager_last": "已是最後一章 →",
    "study_guide_heading": "軟體工程師基本功修煉指南與常見問答（FAQ）",
    "study_guide_intro": "許多初學者與轉職者在刷題（LeetCode）或準備技術面試時，常陷入「背題目卻不懂底層原理」的困境。點擊下方折疊面板展開三階段循序漸進路線圖：",
    "study_guide_summary": "點擊展開／收合：三階段刷題路線圖與學習建議",
    "study_guide_items": (
        (
            "第一階段（記憶體模型與線性結構）：",
            '先親手實作 <a href="ch01.html">Ch.01 的單向鏈結串列</a>與 <a href="ch02.html">Ch.02 的 Stack / Queue</a>，徹底理解指標（Reference / Pointer）操作與時間複雜度 <code>O(1)</code> vs. <code>O(n)</code> 的差異。',
        ),
        (
            "第二階段（分治搜尋、雜湊查找、樹與圖論架構）：",
            '透過 <a href="ch03.html">Ch.03 的二分搜尋與合併排序（Merge Sort）</a>、<a href="ch04.html">Ch.04 的雜湊表（Hash Table / Two Sum）與二元搜尋樹（BST）</a>，再到 <a href="ch05.html">Ch.05 的圖論走訪（Graph BFS / DFS 最短路徑）與物件導向封裝（OOP）</a>，掌握分治法、空間換取時間與抽象化模組設計的核心精神。',
        ),
        (
            "第三階段（進階動態規劃、優先佇列與白板題實戰）：",
            '深入 <a href="ch06.html">Ch.06 動態規劃與記憶化搜尋（0/1 背包與 LIS）</a>及 <a href="ch07.html">Ch.07 二元堆積與 Top-K 多路合併演算法</a>，搭配各章獨立講義內的複雜度對照表、CPython 底層陷阱解析與 YouTube 鐵人賽教學影片完成實戰修煉。',
        ),
    ),
    "privacy_heading": "隱私權政策與 Cookie 聲明 (Privacy Policy)",
    "privacy_body_html": (
        '本網站（ai-purplemaple.com/learn/）使用 Google AdSense 第三方廣告服務與 Google Analytics (GA4)／Google Tag Manager 網站流量分析服務。'
        'Google 及其合作夥伴會使用 Cookie（包含 DART Cookie），根據使用者造訪本站或其他網站的紀錄提供個人化廣告與匿名流量統計。'
        '您可隨時前往 <a href="https://adssettings.google.com/" target="_blank" rel="noopener noreferrer">Google 廣告設定頁面</a> 停用個人化廣告，'
        '或查閱 <a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener noreferrer">Google 廣告與隱私權政策</a>。'
        '本站程式碼複製、社團發問模板複製與隨堂互動測驗均於瀏覽器本機執行；讀者於章節講義點擊「有幫助／待改進」時，僅透過加密安全通道傳送匿名滿意度回饋與 HMAC 雜湊限流識別，絕不公開顯示留言或儲存原始 IP。'
    ),
    "footer_blog_label": "紫楓技術與創作日誌",
    "footer_github_label": "GitHub 原始碼",
    "footer_copyright_label": "版權與轉載聲明",
    "footer_copyright_notice": "© 2026 紫楓出版社（Purple Maple / 王紫楓）. All Rights Reserved. 範例程式碼採 MIT 授權；專書內文與原創圖解保留著作權（歡迎附原文連結節錄引用，禁止全文搬運與未授權商用）。",
    "js_copied": "已複製 ✓",
    "js_err_rate": "今天的次數已用完，明天再來",
    "js_err_short": "請至少輸入 5 個字描述你的疑問",
    "js_err_long": "字數請控制在 400 字以內",
    "js_err_generic": "送出失敗，請稍後再試",
    "js_fb_thanks": "感謝回饋！歡迎選填一句原因幫助我們補強講義。",
    "js_fb_local_thanks": "感謝回饋！已記錄於你的本機瀏覽器偏好設定。",
    "js_fb_note_ok": "✓ 已收到你的回饋，謝謝！",
    "qa_heading": "讀到這章有疑問或實作卡關？到紫楓 FB 學習社團發問",
    "qa_body": "為維持閱讀版面純淨、杜絕廣告留言，本章所有技術發問、除錯求助與程式碼健檢統一集中於官方 Facebook 學習社團。點擊下方按鈕可先一鍵複製標準發問模板，再貼到社團發文，紫楓與社群夥伴能更快幫你定位問題！",
    "qa_copy_btn": "一鍵複製發問模板",
    "qa_copy_done": "已複製發問模板 ✓",
    "qa_primary_cta": "前往 FB 學習社團發問 ↗",
    "qa_template_tpl": "【紫楓出版社提問】{chapter_label}\n- 參考頁面：{page_url}\n- 我看到的現象／錯誤訊息：\n- 我已嘗試過的方法：",
    "press_section_heading": "紫楓出版社（Purple Maple Press）技術專書書架",
    "press_section_intro": "比照歐萊禮（O'Reilly）與 MIT Press 教科書標準打造的免費開源技術專書系列：每章皆附實機驗證 Python 3.12 零依賴程式碼、原生架構圖解、生產環境踩坑指南與互動測驗。",
    "book_status_serializing": "連載中（已上線 {pub}/{total} 章）",
    "book_status_complete": "全書完結（共 7 章）",
    "book_cta_open": "翻開專書目錄 →",
    "book_cta_start_ch01": "從 Ch.01 開始讀",
    "book_cta_read_dsa": "前往下方 7 章完整目錄 ↓",
    "dsa_book_title": "Python 3.12 資料結構與演算法精解",
    "dsa_book_desc": "涵蓋陣列與鏈結串列、堆疊佇列、二分搜尋與 Merge Sort、雜湊表與 BST、圖論 BFS/DFS、動態規劃與二元堆積 Top-K，結合 31 集 IT 鐵人賽實戰影片與 LeetCode 經典白板題。",
    "dsa_cover_alt": "紫楓出版社《Python 3.12 資料結構與演算法精解》典藏書封插畫：白瀬アイリ（艾莉 / Aily）解析樹與演算法圖譜（觀看者左側緋紅、右側蒼藍異色瞳）",
    "book_back_to_shelf": "← 返回紫楓出版社總書架",
    "book_back_to_toc": "← 返回《{book_title}》全書目錄",
    "book_toc_heading": "全書章節目錄（4 大篇 × 10 章）",
    "book_sidebar_summary": "全書章節目錄（點擊展開／收合）",
    "book_coming_soon": "撰寫中",
    "book_published_badge": "已上線",
    "book_reading_time_tpl": "預估精讀時間：約 {mins} 分鐘",
    "book_audience_label": "適合讀者：",
    "book_objectives_heading": "讀完本章你將徹底掌握",
    "book_diagram_heading": "核心系統架構與資料流圖解",
    "book_walkthrough_heading": "關鍵程式碼設計拆解",
    "book_pitfalls_heading": "生產環境實戰踩坑與防禦對策",
    "book_pitfall_symptom_label": "線上故障現象：",
    "book_pitfall_fix_label": "底層根因與工程對策：",
    "book_quiz_heading": "隨堂互動測驗（即時檢核觀念）",
    "book_quiz_intro": "點選選項即可於本機瀏覽器即時對答案與查看深度解析，不傳送任何個人資料。",
    "book_quiz_correct": "✓ 答對了！",
    "book_quiz_wrong": "✗ 再想一下 — ",
    "book_faq_heading": "AI 工程師技術面試高頻問答（FAQ）",
    "book_further_heading": "延伸閱讀與官方原始論文／文件",
    "book_pager_home": "返回本書目錄",
    "book_nav_objectives": "學習目標",
    "book_nav_diagram": "架構圖解",
    "book_nav_comparison": "方案對照表",
    "book_nav_code": "Python 實作",
    "book_nav_pitfalls": "生產踩坑",
    "book_nav_quiz": "隨堂測驗",
    "book_nav_faq": "面試 FAQ",
}


def chapter_short_title(ch: ChapterSpec) -> str:
    return ch.short_title or ch.title.split("（")[0]


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
        <div class="ad-slot-label">ADVERTISEMENT · ({escaped_label})</div>
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


def render_hreflang_and_og_locale(locale_code: str, page_filename: str | None) -> str:
    """Render All-to-All bidirectional hreflang (zh-Hant, zh-Hans, en, x-default) & og:locale meta tags."""
    cur = LOCALE_BY_CODE[locale_code]
    lines: list[str] = []
    for loc in LOCALES:
        href = page_canonical_url(loc.code, page_filename)
        lines.append(f'  <link rel="alternate" hreflang="{loc.hreflang}" href="{href}">')
    x_def = page_canonical_url("zh-TW", page_filename)
    lines.append(f'  <link rel="alternate" hreflang="x-default" href="{x_def}">')
    lines.append(f'  <meta property="og:locale" content="{cur.og_locale}">')
    for loc in LOCALES:
        if loc.code != locale_code:
            lines.append(f'  <meta property="og:locale:alternate" content="{loc.og_locale}">')
    return "\n".join(lines)


def render_lang_switcher(locale_code: str, page_filename: str | None) -> str:
    """Render root-absolute language switcher (never index.html) placed cleanly in Hero."""
    items: list[str] = []
    for loc in LOCALES:
        href = page_root_href(loc.code, page_filename)
        if loc.code == locale_code:
            items.append(
                f'        <span class="lang-pill lang-pill-active" lang="{loc.html_lang}" aria-current="true">{html.escape(loc.switcher_label)}</span>'
            )
        else:
            items.append(
                f'        <a class="lang-pill" href="{href}" lang="{loc.html_lang}" hreflang="{loc.hreflang}">{html.escape(loc.switcher_label)}</a>'
            )
    return (
        '      <nav class="lang-switcher" aria-label="Language">\n'
        + "\n".join(items)
        + "\n      </nav>"
    )


def build_index_json_ld(
    locale_code: str,
    ui: dict[str, Any],
    chapters: Sequence[ChapterSpec],
    chapter_titles_short: str,
) -> dict[str, Any]:
    """Build Schema.org Course JSON-LD with locale-isolated @id and hasPart links."""
    loc = LOCALE_BY_CODE[locale_code]
    index_url = page_canonical_url(locale_code, None)
    has_part = [
        {
            "@type": "TechArticle",
            "@id": f"{page_canonical_url(locale_code, f'{ch.id}.html')}#article",
            "headline": f"{ch.badge} {ch.title}",
            "url": page_canonical_url(locale_code, f"{ch.id}.html"),
        }
        for ch in chapters
    ]
    return {
        "@context": "https://schema.org",
        "@type": "Course",
        "@id": f"{index_url}#course",
        "name": ui["course_name"],
        "description": ui["course_desc_tpl"].format(chapter_titles_short=chapter_titles_short),
        "url": index_url,
        "inLanguage": loc.jsonld_lang,
        "dateModified": SITE_LASTMOD,
        "isPartOf": {
            "@type": "WebSite",
            "@id": "https://ai-purplemaple.com/#website",
            "name": ui["brand_website_name"],
            "url": "https://ai-purplemaple.com/",
        },
        "provider": {
            "@type": "Person",
            "@id": "https://ai-purplemaple.com/#creator",
            "name": ui["brand_creator_name"],
            "url": "https://ai-purplemaple.com/",
            "sameAs": CREATOR_SAME_AS,
        },
        "copyrightHolder": {"@id": "https://ai-purplemaple.com/#creator"},
        "copyrightYear": 2026,
        "license": "https://ai-purplemaple.com/privacy.html#copyright",
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [".aeo-capsule", "header.hero h1"],
        },
        "hasPart": has_part,
    }


def build_chapter_json_ld(
    locale_code: str,
    ui: dict[str, Any],
    ch: ChapterSpec,
    yt_videos: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build per-chapter Schema.org @graph with TechArticle, VideoObject, FAQPage, and BreadcrumbList."""
    loc = LOCALE_BY_CODE[locale_code]
    index_url = page_canonical_url(locale_code, None)
    ch_url = page_canonical_url(locale_code, f"{ch.id}.html")
    creator_ref = {
        "@type": "Person",
        "@id": "https://ai-purplemaple.com/#creator",
        "name": ui["brand_creator_name"],
        "url": "https://ai-purplemaple.com/",
        "sameAs": CREATOR_SAME_AS,
    }
    yt_meta = yt_videos.get(ch.id, yt_videos["ch01"])
    vid_id = yt_meta["video_id"]
    video_node = {
        "@type": "VideoObject",
        "@id": f"{ch_url}#video",
        "name": yt_meta["title"],
        "description": ui["video_desc_tpl"].format(badge=ch.badge, title=ch.title, summary=ch.summary),
        "thumbnailUrl": [
            f"https://i.ytimg.com/vi/{vid_id}/maxresdefault.jpg",
            f"https://i.ytimg.com/vi/{vid_id}/hqdefault.jpg",
        ],
        "uploadDate": yt_meta["upload_date"],
        "inLanguage": "zh-Hant",
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
                "headline": ui["tech_article_headline_tpl"].format(badge=ch.badge, title=ch.title),
                "description": ui["chapter_desc_tpl"].format(badge=ch.badge, title=ch.title, summary=ch.summary),
                "url": ch_url,
                "mainEntityOfPage": ch_url,
                "image": "https://ai-purplemaple.com/assets/gallery/aily_03.jpg",
                "datePublished": "2026-03-01",
                "dateModified": ch.lastmod,
                "inLanguage": loc.jsonld_lang,
                "proficiencyLevel": "Beginner to Intermediate",
                "dependencies": "Python 3.12",
                "keywords": ", ".join(ch.keywords),
                "author": creator_ref,
                "publisher": creator_ref,
                "copyrightHolder": {"@id": "https://ai-purplemaple.com/#creator"},
                "copyrightYear": 2026,
                "license": "https://ai-purplemaple.com/privacy.html#copyright",
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": [".aeo-capsule", "header.hero h1"],
                },
                "video": {"@id": f"{ch_url}#video"},
                "isPartOf": {
                    "@type": "Course",
                    "@id": f"{index_url}#course",
                    "name": ui["course_name"],
                    "url": index_url,
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
                        "name": ui["breadcrumb_home_name"],
                        "item": index_url,
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


def render_video_lecture_section(
    ch: ChapterSpec,
    ui: dict[str, Any],
    yt_videos: dict[str, dict[str, Any]],
) -> str:
    """Render an embedded 16:9 YouTube lecture player and supplementary video links for the chapter."""
    yt_meta = yt_videos.get(ch.id, yt_videos["ch01"])
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
          <h3>{html.escape(ui["video_related_heading"])}</h3>
          <ul>
{related_items}
          </ul>
        </div>"""
        if related_items
        else ""
    )
    heading = html.escape(ui["video_heading_tpl"].format(views_label=yt_meta["views_label"]))
    return f"""
      <section class="chapter-card" id="video-lecture">
        <h2>{heading}</h2>
        <p class="chapter-summary">{html.escape(ui["video_intro"])}</p>
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
          <span><strong>{html.escape(ui["video_main_label"])}</strong><a href="https://www.youtube.com/watch?v={vid_id}" target="_blank" rel="noopener noreferrer">{vid_title}</a></span>
          <span><a href="https://www.youtube.com/playlist?list=PLhxdaTcUMi3nRM5mtOdQgO4VEtAEsTiYd" target="_blank" rel="noopener noreferrer">{html.escape(ui["video_playlist_cta"])}</a></span>
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


def render_pitfalls(ch: ChapterSpec, ui: dict[str, Any]) -> str:
    """Render CPython 3.12 runtime internals & common implementation pitfalls."""
    items_html: list[str] = []
    for pf in ch.pitfalls:
        items_html.append(
            f"""
          <div class="pitfall-card">
            <h3>{html.escape(pf.title)}</h3>
            <p class="pitfall-symptom"><strong>{html.escape(ui["pitfall_symptom_label"])}</strong>{html.escape(pf.symptom)}</p>
            <p class="pitfall-fix"><strong>{html.escape(ui["pitfall_fix_label"])}</strong>{html.escape(pf.root_cause_and_fix)}</p>
          </div>"""
        )
    return f"""
      <section class="chapter-card" id="pitfalls">
        <h2>{html.escape(ui["pitfalls_heading"])}</h2>
        <div class="pitfall-list">
{"".join(items_html)}
        </div>
      </section>"""


def render_interview_section(ch: ChapterSpec, ui: dict[str, Any]) -> str:
    """Render LeetCode problem mapping table and expandable interview FAQs."""
    lc_rows: list[str] = []
    for lc in ch.leetcode_problems:
        lc_rows.append(
            f"              <tr>"
            f'<th scope="row">LeetCode #{lc.number}</th>'
            f"<td>{html.escape(lc.title)}</td>"
            f'<td><span class="diff-badge">{html.escape(lc.difficulty)}</span></td>'
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

    caption = html.escape(ui["interview_table_caption_tpl"].format(badge=ch.badge))
    return f"""
      <section class="chapter-card" id="interview-faq">
        <h2>{html.escape(ui["interview_heading"])}</h2>
        <div class="table-responsive">
          <table class="comparison-table">
            <caption>{caption}</caption>
            <thead>
              <tr>
                <th scope="col">{html.escape(ui["interview_th_num"])}</th>
                <th scope="col">{html.escape(ui["interview_th_title"])}</th>
                <th scope="col">{html.escape(ui["interview_th_diff"])}</th>
                <th scope="col">{html.escape(ui["interview_th_pattern"])}</th>
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


def render_feedback_section(
    chapter_slug: str,
    chapter_label: str,
    page_url: str,
    locale_code: str,
    ui: dict[str, Any],
    *,
    fb_mode: str = "api",
) -> str:
    """Render minimalist helpfulness vote + FB Group (zh-TW/zh-CN) or GitHub Issues (en) Q&A card."""
    note_form_html = ""
    if fb_mode == "api":
        note_form_html = f"""
        <form class="fb-note" id="fbNoteForm" hidden autocomplete="off">
          <input id="fbNoteInput" maxlength="200" placeholder="{html.escape(ui["fb_note_placeholder"])}" aria-label="{html.escape(ui["fb_note_aria"])}">
          <input class="fb-hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
          <button class="btn btn-secondary" id="fbNoteBtn" type="submit">{html.escape(ui["fb_note_submit"])}</button>
        </form>"""

    qa_url = GITHUB_ISSUES_URL if locale_code == "en" else FB_GROUP_URL
    qa_template = ui["qa_template_tpl"].format(chapter_label=chapter_label, page_url=page_url)

    return f"""
      <section class="chapter-card fb-box" id="fbBox" data-chapter="{html.escape(chapter_slug)}" data-fb-mode="{html.escape(fb_mode)}">
        <div class="fb-row">
          <span class="fb-q">{html.escape(ui["fb_question"])}</span>
          <div class="fb-btns">
            <button class="fb-chip" type="button" data-fb-vote="1" aria-pressed="false">{html.escape(ui["fb_yes"])}</button>
            <button class="fb-chip" type="button" data-fb-vote="-1" aria-pressed="false">{html.escape(ui["fb_no"])}</button>
          </div>
        </div>{note_form_html}
        <p class="fb-status" id="fbStatus" aria-live="polite"></p>
        <div class="community-qa-card" id="communityQa">
          <h3>{html.escape(ui["qa_heading"])}</h3>
          <p class="community-qa-desc">{html.escape(ui["qa_body"])}</p>
          <div class="community-qa-actions">
            <a class="btn btn-primary" href="{qa_url}" target="_blank" rel="noopener noreferrer" data-qa-link="1">{html.escape(ui["qa_primary_cta"])}</a>
            <button class="btn btn-secondary qa-copy-btn" type="button" data-qa-template="{html.escape(qa_template, quote=True)}">{html.escape(ui["qa_copy_btn"])}</button>
          </div>
          <p class="fb-status" id="qaCopyStatus" aria-live="polite"></p>
        </div>
      </section>"""


def render_deep_dive_callout(ch: ChapterSpec, ui: dict[str, Any]) -> str:
    """Render an asymmetric information-gain callout on index.html linking to the standalone deep-dive page."""
    faq_previews = "\n".join(
        f'            <li><a href="{ch.id}.html#interview-faq">{html.escape(faq.question)}</a></li>'
        for faq in ch.interview_faqs
    )
    lc_badges = " · ".join(f"LeetCode #{lc.number}" for lc in ch.leetcode_problems)
    summary_text = html.escape(ui["deep_dive_summary_tpl"].format(badge=ch.badge))
    cta_text = html.escape(ui["deep_dive_cta_tpl"].format(badge=ch.badge))
    return f"""
        <details class="deep-dive-callout">
          <summary class="deep-dive-callout-header">
            <strong>{summary_text}</strong>
            <span class="lc-tag-row">{html.escape(lc_badges)}</span>
          </summary>
          <p class="deep-dive-table-hint"><strong>{html.escape(ui["deep_dive_table_label"])}</strong><a href="{ch.id}.html#comparison">{html.escape(ch.comparison_table.caption)}</a></p>
          <p class="deep-dive-table-hint"><strong>{html.escape(ui["deep_dive_faq_label"])}</strong></p>
          <ul class="deep-dive-faq-preview">
{faq_previews}
          </ul>
          <div class="deep-dive-action">
            <a class="btn btn-primary" href="{ch.id}.html">{cta_text}</a>
          </div>
        </details>"""


def render_affiliate_resources_section(
    locale_code: str,
    ui: dict[str, Any],
    resources: Sequence[AffiliateResource],
) -> str:
    """Render localized book & documentation comparison table (sponsored on zh-TW, non-sponsored on zh-CN/en)."""
    rows_html: list[str] = []
    for item in resources:
        rel_val = "sponsored noopener noreferrer" if item.is_sponsored else "noopener noreferrer"
        aff_attrs = (
            f' data-affiliate-partner="{html.escape(item.partner_id)}" data-affiliate-placement="index_table"'
            if (item.is_sponsored or locale_code == "zh-TW")
            else ""
        )
        rows_html.append(
            f"""              <tr>
                <td><strong>{html.escape(item.title)}</strong></td>
                <td>{html.escape(item.partner_label)}</td>
                <td>{html.escape(item.audience)}</td>
                <td>{html.escape(item.highlight)}</td>
                <td><a class="btn btn-secondary aff-btn" href="{html.escape(item.url)}" target="_blank" rel="{rel_val}"{aff_attrs}>{html.escape(item.cta_label)}</a></td>
              </tr>"""
        )
    rows_block = "\n".join(rows_html)
    return f"""
      <section class="study-guide-card affiliate-card" id="recommended-resources">
        <h2>{html.escape(ui["resources_heading"])}</h2>
        <p class="affiliate-disclosure">{html.escape(ui["resources_note"])}</p>
        <div class="table-responsive">
          <table class="comparison-table">
            <thead>
              <tr>
                <th>{html.escape(ui["resources_th_title"])}</th>
                <th>{html.escape(ui["resources_th_platform"])}</th>
                <th>{html.escape(ui["resources_th_audience"])}</th>
                <th>{html.escape(ui["resources_th_highlight"])}</th>
                <th>{html.escape(ui["resources_th_action"])}</th>
              </tr>
            </thead>
            <tbody>
{rows_block}
            </tbody>
          </table>
        </div>
      </section>"""


def render_chapter_book_callout(
    locale_code: str,
    ch: ChapterSpec,
    ui: dict[str, Any],
    chapter_resources: dict[str, tuple[str, str]] | None = None,
) -> str:
    """Render Books.com.tw AP reading card on zh-TW, or non-sponsored official docs card on zh-CN / en."""
    if locale_code == "zh-TW":
        label, url = get_chapter_book_recommendation(ch.id)
        rel_val = "sponsored noopener noreferrer"
        aff_attrs = f' data-affiliate-partner="books_ap_{html.escape(ch.id)}" data-affiliate-placement="chapter_footer"'
    else:
        assert chapter_resources is not None
        label, url = chapter_resources[ch.id]
        rel_val = "noopener noreferrer"
        aff_attrs = ""
    return f"""
      <aside class="chapter-card affiliate-chapter-card" aria-label="{html.escape(ui["chapter_resource_aria"])}">
        <div class="aff-ch-row">
          <div>
            <strong>{html.escape(label)}</strong>
            <p class="affiliate-disclosure" style="margin: 0.3rem 0 0;">{html.escape(ui["chapter_resource_note"])}</p>
          </div>
          <a class="btn btn-secondary aff-btn" href="{html.escape(url)}" target="_blank" rel="{rel_val}"{aff_attrs}>{html.escape(ui["chapter_resource_cta"])}</a>
        </div>
      </aside>"""


def render_chapter_pager(
    locale_code: str,
    idx: int,
    chapters: Sequence[ChapterSpec],
    ui: dict[str, Any],
) -> str:
    """Render Prev / Home / Next navigation bar at the bottom of standalone chapter pages."""
    prev_ch = chapters[idx - 1] if idx > 0 else None
    next_ch = chapters[idx + 1] if idx + 1 < len(chapters) else None
    home_href = page_root_href(locale_code, None)

    prev_html = (
        f'<a class="pager-link" href="{prev_ch.id}.html">{html.escape(ui["pager_prev_tpl"].format(badge=prev_ch.badge, short=chapter_short_title(prev_ch)))}</a>'
        if prev_ch
        else f'<span class="pager-link pager-disabled">{html.escape(ui["pager_first"])}</span>'
    )
    next_html = (
        f'<a class="pager-link" href="{next_ch.id}.html">{html.escape(ui["pager_next_tpl"].format(badge=next_ch.badge, short=chapter_short_title(next_ch)))}</a>'
        if next_ch
        else f'<span class="pager-link pager-disabled">{html.escape(ui["pager_last"])}</span>'
    )
    return f"""
      <nav class="chapter-pager" aria-label="{html.escape(ui["pager_aria"])}">
        {prev_html}
        <a class="pager-link pager-home" href="{home_href}">{html.escape(ui["pager_home"])}</a>
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
    :root:lang(zh-Hans) {
      --font-serif: "Newsreader", "Songti SC", "STSong", "SimSun", Georgia, serif;
      --font-sans: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Source Han Sans SC", system-ui, -apple-system, sans-serif;
    }
    :root:lang(en) {
      --font-serif: "Newsreader", Georgia, "Times New Roman", serif;
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
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

    /* Language Switcher Bar */
    .lang-switcher {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.45rem;
      margin-bottom: 1rem;
    }
    .lang-pill {
      display: inline-flex;
      align-items: center;
      padding: 0.24rem 0.72rem;
      min-height: 32px;
      border-radius: 3px;
      border: 1px solid var(--border);
      background: var(--surface-alt);
      color: var(--text);
      font-size: 0.8rem;
      font-weight: 600;
      transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
    }
    a.lang-pill:hover {
      border-color: var(--accent);
      background: var(--accent-soft);
      color: var(--accent-strong);
      text-decoration: none;
    }
    .lang-pill-active {
      background: var(--accent-strong);
      border-color: var(--accent-strong);
      color: #ffffff;
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

    /* Purple Maple Press Bookshelf, Book TOC, Diagrams, Quiz & Community Q&A */
    .read-progress {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 3px;
      background: rgba(28, 25, 23, 0.08);
      z-index: 90;
      pointer-events: none;
    }
    .read-progress-bar {
      width: 100%;
      height: 100%;
      background: var(--accent);
      transform-origin: left center;
      transform: scaleX(0);
      will-change: transform;
    }
    .bookshelf-section {
      background: var(--surface);
      border: 1px solid var(--border);
      border-top: 3px solid var(--border-strong);
      border-radius: 4px;
      padding: 1.8rem 2rem;
      margin-bottom: 2.1rem;
    }
    .bookshelf-section h2 {
      margin: 0 0 0.55rem;
      font-family: var(--font-serif);
      font-size: 1.45rem;
      color: var(--text);
    }
    .bookshelf-intro {
      margin: 0 0 1.35rem;
      color: var(--muted);
      font-size: 0.94rem;
    }
    .bookshelf-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 1.35rem;
    }
    .book-card {
      display: grid;
      grid-template-columns: 148px minmax(0, 1fr);
      gap: 1.15rem;
      align-items: start;
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-left: 4px solid var(--accent-strong);
      border-radius: 4px;
      padding: 1.1rem;
    }
    .book-cover-img {
      width: 100%;
      height: auto;
      display: block;
      border-radius: 4px;
      border: 1px solid var(--border);
      box-shadow: 0 4px 12px rgba(28, 25, 23, 0.1);
      background: var(--surface);
    }
    .book-card-body h3 {
      margin: 0.45rem 0 0.4rem;
      font-family: var(--font-serif);
      font-size: 1.08rem;
      line-height: 1.35;
      color: var(--text);
    }
    .book-card-body p {
      margin: 0 0 0.85rem;
      font-size: 0.87rem;
      color: var(--muted);
      line-height: 1.62;
    }
    .book-card-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
    }
    .book-card-actions .btn {
      padding: 0.46rem 0.82rem;
      min-height: 38px;
      font-size: 0.82rem;
    }
    .book-pill {
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      font-weight: 600;
      padding: 0.14rem 0.52rem;
      border-radius: 3px;
      background: var(--accent-soft);
      color: var(--accent-strong);
      border: 1px solid #b6e0c5;
    }
    .book-hero-grid {
      display: grid;
      grid-template-columns: 200px minmax(0, 1fr);
      gap: 1.6rem;
      align-items: start;
    }
    .book-part-card {
      margin-bottom: 1.4rem;
    }
    .book-part-card h3 {
      margin: 0 0 0.75rem;
      font-family: var(--font-serif);
      font-size: 1.14rem;
      color: var(--accent-strong);
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.4rem;
    }
    .book-toc-list {
      list-style: none;
      margin: 0;
      padding: 0;
      display: grid;
      gap: 0.65rem;
    }
    .book-toc-row {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 0.85rem;
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 0.85rem 1rem;
    }
    .book-toc-row.is-live {
      border-left: 4px solid var(--accent-strong);
      background: var(--surface);
    }
    .book-toc-row.is-soon {
      opacity: 0.84;
    }
    .book-toc-main strong {
      display: block;
      font-size: 0.96rem;
      color: var(--text);
      margin-bottom: 0.2rem;
    }
    .book-toc-main p {
      margin: 0;
      font-size: 0.85rem;
      color: var(--muted);
    }
    .status-live, .status-soon {
      flex-shrink: 0;
      font-family: var(--font-mono);
      font-size: 0.74rem;
      font-weight: 600;
      padding: 0.16rem 0.55rem;
      border-radius: 3px;
    }
    .status-live {
      background: var(--accent-soft);
      color: var(--accent-strong);
      border: 1px solid #b6e0c5;
    }
    .status-soon {
      background: #ece8de;
      color: var(--muted);
      border: 1px solid var(--border);
    }
    .book-container {
      max-width: 1120px;
    }
    .book-layout {
      display: grid;
      grid-template-columns: 245px minmax(0, 1fr);
      gap: 1.65rem;
      align-items: start;
    }
    .book-toc-drawer {
      position: sticky;
      top: 1.25rem;
      background: var(--surface);
      border: 1px solid var(--border);
      border-top: 2.5px solid var(--border-strong);
      border-radius: 4px;
      padding: 0.9rem 1rem;
      font-size: 0.84rem;
    }
    .book-toc-drawer summary {
      cursor: pointer;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 0.65rem;
    }
    .book-sidebar-part {
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--muted);
      margin: 0.75rem 0 0.3rem;
      font-weight: 600;
    }
    .book-sidebar-list {
      list-style: none;
      margin: 0;
      padding: 0;
      display: grid;
      gap: 0.28rem;
    }
    .book-sidebar-link, .book-sidebar-soon {
      display: block;
      padding: 0.32rem 0.5rem;
      border-radius: 3px;
      line-height: 1.38;
    }
    .book-sidebar-link {
      color: var(--text);
      font-weight: 600;
    }
    .book-sidebar-link[aria-current="page"] {
      background: var(--accent-soft);
      color: var(--accent-strong);
      border-left: 3px solid var(--accent-strong);
    }
    .book-sidebar-soon {
      color: var(--muted);
      opacity: 0.72;
    }
    .book-prose {
      max-width: 74ch;
    }
    .book-prose p {
      margin: 0 0 1.05rem;
      color: var(--text);
      font-size: 0.99rem;
      line-height: 1.84;
    }
    .book-prose ul {
      margin: 0 0 1.1rem;
      padding-left: 1.3rem;
      color: var(--muted);
    }
    .book-prose li {
      margin-bottom: 0.42rem;
    }
    .editorial-callout {
      background: var(--accent-soft);
      border: 1px solid #b6e0c5;
      border-left: 4px solid var(--accent-strong);
      border-radius: 4px;
      padding: 0.95rem 1.15rem;
      margin: 1rem 0 1.35rem;
    }
    .editorial-callout strong {
      display: block;
      color: var(--accent-strong);
      margin-bottom: 0.3rem;
    }
    .diagram-figure {
      margin: 1rem 0 0;
      background: #fdfcf9;
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 1rem;
      text-align: center;
    }
    .diagram-figure svg {
      width: 100%;
      max-width: 760px;
      height: auto;
      display: block;
      margin: 0 auto;
    }
    .diagram-figure figcaption {
      margin-top: 0.65rem;
      font-size: 0.84rem;
      color: var(--muted);
    }
    .quiz-card {
      border: 1px solid var(--border);
      border-left: 4px solid var(--accent);
      border-radius: 4px;
      background: var(--surface-alt);
      padding: 1rem 1.15rem;
      margin: 0 0 1.1rem;
    }
    .quiz-card legend {
      font-weight: 700;
      color: var(--text);
      padding: 0 0.35rem;
      font-size: 0.96rem;
    }
    .quiz-options {
      display: grid;
      gap: 0.5rem;
      margin-top: 0.6rem;
    }
    .quiz-opt {
      text-align: left;
      padding: 0.62rem 0.9rem;
      min-height: 44px;
      border-radius: 4px;
      border: 1.5px solid var(--border);
      background: var(--surface);
      color: var(--text);
      font: inherit;
      font-size: 0.9rem;
      cursor: pointer;
      transition: border-color 0.15s ease, background-color 0.15s ease;
    }
    .quiz-opt:hover {
      border-color: var(--accent);
      background: var(--accent-soft);
    }
    .quiz-opt.is-correct {
      background: var(--accent-soft);
      border-color: var(--accent-strong);
      color: var(--accent-strong);
      font-weight: 700;
    }
    .quiz-opt.is-wrong {
      background: #fef2f2;
      border-color: var(--danger);
      color: #991b1b;
    }
    .quiz-feedback {
      margin: 0.7rem 0 0;
      font-size: 0.89rem;
      color: var(--text);
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 4px;
      padding: 0.65rem 0.85rem;
    }
    .community-qa-card {
      margin-top: 1.1rem;
      padding-top: 1rem;
      border-top: 1px solid var(--border);
    }
    .community-qa-card h3 {
      margin: 0 0 0.45rem;
      font-family: var(--font-serif);
      font-size: 1.06rem;
      color: var(--text);
    }
    .community-qa-desc {
      margin: 0 0 0.85rem;
      font-size: 0.88rem;
      color: var(--muted);
    }
    .community-qa-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 0.65rem;
    }
    @media (max-width: 960px) {
      .bookshelf-grid {
        grid-template-columns: 1fr;
      }
      .book-layout {
        grid-template-columns: 1fr;
      }
      .book-toc-drawer {
        position: static;
      }
    }
    @media (max-width: 640px) {
      .container {
        padding: 1.5rem 1rem 3rem;
      }
      header.hero,
      .chapter-card,
      .study-guide-card,
      .bookshelf-section {
        padding: 1.35rem 1.15rem;
      }
      .book-card,
      .book-hero-grid {
        grid-template-columns: 1fr;
      }
      .book-cover-img {
        max-width: 200px;
      }
      .fb-note input {
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


def render_footer(ui: dict[str, Any]) -> str:
    """Render shared privacy policy, dual-license copyright notice & ecosystem footer with main-site trust links."""
    return f"""    <footer id="privacy">
      <div class="privacy-policy-card">
        <h3>{html.escape(ui["privacy_heading"])}</h3>
        <p>{ui["privacy_body_html"]}</p>
      </div>
      <p style="margin-bottom:0.45rem;">{html.escape(ui["footer_copyright_notice"])} · <a href="https://ai-purplemaple.com/privacy.html#copyright" style="color: var(--accent);">{html.escape(ui["footer_copyright_label"])}</a></p>
      <p>Created by <strong><a href="https://ai-purplemaple.com/" style="color: var(--accent);">{html.escape(ui["brand_anchor_footer"])}</a></strong> · <a href="https://ai-purplemaple.com/articles/" style="color: var(--muted);">Articles</a> · <a href="https://ai-purplemaple.com/about.html" style="color: var(--muted);">About</a> · <a href="https://ai-purplemaple.com/contact.html" style="color: var(--muted);">Contact</a> · <a href="https://ai-purplemaple.com/privacy.html" style="color: var(--muted);">Privacy</a> · <a href="https://ai-purplemaple.com/terms.html" style="color: var(--muted);">Terms</a> · <a href="https://github.com/tbpfs/learning" target="_blank" rel="noopener noreferrer" style="color: var(--muted);">{html.escape(ui["footer_github_label"])}</a> · <a href="/ads.txt">ads.txt</a></p>
    </footer>"""


def render_copy_script(ui: dict[str, Any], *, include_cms_fetch: bool) -> str:
    """Render copy button handler, localized feedback/Q&A client, and (on zh-TW index only) CMS loader."""
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

    js_msg = json.dumps(
        {
            "copied": ui["js_copied"],
            "errRate": ui["js_err_rate"],
            "errShort": ui["js_err_short"],
            "errLong": ui["js_err_long"],
            "errGeneric": ui["js_err_generic"],
            "fbThanks": ui["js_fb_thanks"],
            "fbLocalThanks": ui["js_fb_local_thanks"],
            "fbNoteOk": ui["js_fb_note_ok"],
            "qaCopyDone": ui["qa_copy_done"],
            "quizCorrect": ui["book_quiz_correct"],
            "quizWrong": ui["book_quiz_wrong"],
        },
        ensure_ascii=False,
    )

    return f"""  <script>
    var UI_MSG = {js_msg};
    function copyTextSafe(text, onDone) {{
      if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {{
        navigator.clipboard.writeText(text).then(onDone).catch(function () {{ fallbackCopy(text, onDone); }});
      }} else {{
        fallbackCopy(text, onDone);
      }}
    }}
    function fallbackCopy(text, onDone) {{
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.select();
      try {{ document.execCommand('copy'); if (onDone) onDone(); }} catch (_) {{}}
      document.body.removeChild(ta);
    }}
    function bindCopyButtons() {{
      document.querySelectorAll('.copy-btn').forEach(function (btn) {{
        if (btn.getAttribute('data-bound') === '1') return;
        btn.setAttribute('data-bound', '1');
        btn.addEventListener('click', function () {{
          var targetId = btn.getAttribute('data-target');
          var codeEl = document.getElementById(targetId);
          if (!codeEl) return;
          copyTextSafe(codeEl.textContent || '', function () {{
            var orig = btn.textContent;
            btn.textContent = UI_MSG.copied;
            if (typeof window.gtag === 'function') {{
              window.gtag('event', 'copy_code', {{ chapter_target: targetId }});
            }}
            setTimeout(function () {{ btn.textContent = orig; }}, 1500);
          }});
        }});
      }});
    }}
    bindCopyButtons();
    document.querySelectorAll('.qa-copy-btn').forEach(function (btn) {{
      btn.addEventListener('click', function () {{
        var tpl = btn.getAttribute('data-qa-template') || '';
        var st = document.getElementById('qaCopyStatus');
        copyTextSafe(tpl, function () {{
          var orig = btn.textContent;
          btn.textContent = UI_MSG.qaCopyDone;
          if (st) st.textContent = UI_MSG.qaCopyDone;
          if (typeof window.gtag === 'function') {{
            window.gtag('event', 'copy_qa_template', {{ site: 'learn' }});
          }}
          setTimeout(function () {{ btn.textContent = orig; }}, 2000);
        }});
      }});
    }});
    document.querySelectorAll('[data-qa-link]').forEach(function (el) {{
      el.addEventListener('click', function () {{
        if (typeof window.gtag === 'function') {{
          window.gtag('event', 'community_qa_click', {{ site: 'learn', href: el.getAttribute('href') || '' }});
        }}
      }});
    }});
    document.querySelectorAll('.quiz-opt').forEach(function (btn) {{
      btn.addEventListener('click', function () {{
        var card = btn.closest('.quiz-card');
        if (!card) return;
        var chosen = Number(btn.getAttribute('data-opt-idx'));
        var correct = Number(card.getAttribute('data-answer-idx'));
        card.querySelectorAll('.quiz-opt').forEach(function (b) {{
          var idx = Number(b.getAttribute('data-opt-idx'));
          b.classList.remove('is-correct', 'is-wrong');
          b.setAttribute('aria-pressed', idx === chosen ? 'true' : 'false');
          if (idx === correct) b.classList.add('is-correct');
          else if (idx === chosen) b.classList.add('is-wrong');
        }});
        var fb = card.querySelector('.quiz-feedback');
        if (fb) {{
          var prefix = chosen === correct ? UI_MSG.quizCorrect : UI_MSG.quizWrong;
          var exp = fb.getAttribute('data-explanation') || '';
          fb.textContent = prefix + ' ' + exp;
          fb.hidden = false;
        }}
      }});
    }});
    (function () {{
      var bar = document.getElementById('readProgressBar');
      if (!bar) return;
      function updateBar() {{
        var doc = document.documentElement;
        var maxScroll = Math.max(1, doc.scrollHeight - window.innerHeight);
        var ratio = Math.min(1, Math.max(0, window.scrollY / maxScroll));
        bar.style.transform = 'scaleX(' + ratio.toFixed(4) + ')';
      }}
      window.addEventListener('scroll', updateBar, {{ passive: true }});
      updateBar();
    }})();
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
      if (!fbBox) return;
      var chId = fbBox.getAttribute('data-chapter') || '';
      var fbMode = fbBox.getAttribute('data-fb-mode') || 'api';
      var apiBase = ['https://ai-purplemaple.com', 'api', 'v1'].join('/');
      var fbKey = 'learnFb:' + chId;
      var curVote = 0;

      function setStatus(el, msg, isErr) {{
        if (!el) return;
        el.classList.toggle('err', Boolean(isErr));
        el.textContent = msg || '';
      }}

      function errText(code) {{
        if (code === 'rate_limited') return UI_MSG.errRate;
        if (code === 'too_short') return UI_MSG.errShort;
        if (code === 'too_long') return UI_MSG.errLong;
        return UI_MSG.errGeneric;
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

      function postJson(endpoint, body) {{
        return fetch(apiBase + '/' + endpoint, {{
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
          if (fbMode === 'local') {{
            setFbBtns(vote);
            try {{ localStorage.setItem(fbKey, String(vote)); }} catch (_) {{}}
            setStatus(fbStatus, UI_MSG.fbLocalThanks, false);
            if (typeof window.gtag === 'function') {{
              window.gtag('event', 'chapter_feedback', {{ chapter_id: chId, vote: vote }});
            }}
            return;
          }}
          if (typeof fetch !== 'function') return;
          if (vote === prevVote) {{
            if (noteForm) noteForm.hidden = false;
            setStatus(fbStatus, UI_MSG.fbThanks, false);
            return;
          }}
          setFbBtns(vote);
          postJson('learn-feedback', {{ slug: chId, vote: vote, note: '' }})
            .then(function () {{
              try {{ localStorage.setItem(fbKey, String(vote)); }} catch (_) {{}}
              if (noteForm) noteForm.hidden = false;
              setStatus(fbStatus, UI_MSG.fbThanks, false);
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

      if (noteForm && fbMode === 'api' && typeof fetch === 'function') {{
        noteForm.addEventListener('submit', function (e) {{
          e.preventDefault();
          var inp = document.getElementById('fbNoteInput');
          var noteBtn = document.getElementById('fbNoteBtn');
          var note = ((inp && inp.value) || '').trim();
          if (!note) return;
          var hp = noteForm.elements.website ? noteForm.elements.website.value : '';
          if (noteBtn) noteBtn.disabled = true;
          postJson('learn-feedback', {{ slug: chId, vote: curVote || 1, note: note, website: hp }})
            .then(function () {{
              if (inp) inp.value = '';
              noteForm.hidden = true;
              setStatus(fbStatus, UI_MSG.fbNoteOk, false);
            }})
            .catch(function (err) {{
              setStatus(fbStatus, errText(err && err.message), true);
            }})
            .finally(function () {{
              if (noteBtn) noteBtn.disabled = false;
            }});
        }});
      }}
    }})();{cms_block}
  </script>"""


def render_bookshelf_section(
    locale_code: str,
    ui: dict[str, Any],
    books: Sequence[LoadedBook],
) -> str:
    """Render the Purple Maple Press 2-book showcase shelf on localized index pages."""
    cards: list[str] = []
    for book in books:
        meta = book.meta
        pub_count = len(book.published_chapter_ids)
        total_count = len(book.outlines)
        book_href = page_root_href(locale_code, f"books/{meta.id}/")
        status_label = ui["book_status_serializing"].format(pub=pub_count, total=total_count)
        ch01_cta = ""
        if book.published_chapter_ids:
            first_id = book.published_chapter_ids[0]
            first_href = page_root_href(locale_code, f"books/{meta.id}/{first_id}.html")
            ch01_cta = f'<a class="btn btn-secondary" href="{first_href}">{html.escape(ui["book_cta_start_ch01"])}</a>'
        cards.append(
            f"""          <article class="book-card">
            <a href="{book_href}">
              <img class="book-cover-img" src="{html.escape(asset_root_href(meta.cover_image))}" width="{meta.cover_width}" height="{meta.cover_height}" loading="lazy" decoding="async" alt="{html.escape(meta.cover_alt[locale_code])}">
            </a>
            <div class="book-card-body">
              <span class="book-pill">{html.escape(status_label)}</span>
              <h3><a href="{book_href}" style="color: inherit;">{html.escape(meta.title[locale_code])}</a></h3>
              <p>{html.escape(meta.description[locale_code])}</p>
              <div class="book-card-actions">
                <a class="btn btn-primary" href="{book_href}">{html.escape(ui["book_cta_open"])}</a>
                {ch01_cta}
              </div>
            </div>
          </article>"""
        )

    # Book 2 (Classic Python 3.12 DSA Handbook — hosted directly on this index page)
    cards.append(
        f"""          <article class="book-card">
            <a href="#ch01">
              <img class="book-cover-img" src="{html.escape(asset_root_href('/assets/cover-python-dsa.webp'))}" width="640" height="857" loading="lazy" decoding="async" alt="{html.escape(ui["dsa_cover_alt"])}">
            </a>
            <div class="book-card-body">
              <span class="book-pill">{html.escape(ui["book_status_complete"])}</span>
              <h3><a href="#ch01" style="color: inherit;">{html.escape(ui["dsa_book_title"])}</a></h3>
              <p>{html.escape(ui["dsa_book_desc"])}</p>
              <div class="book-card-actions">
                <a class="btn btn-primary" href="#ch01">{html.escape(ui["book_cta_read_dsa"])}</a>
              </div>
            </div>
          </article>"""
    )

    cards_joined = "\n".join(cards)
    return f"""
      <section class="bookshelf-section" id="purple-maple-press">
        <h2>{html.escape(ui["press_section_heading"])}</h2>
        <p class="bookshelf-intro">{html.escape(ui["press_section_intro"])}</p>
        <div class="bookshelf-grid">
{cards_joined}
        </div>
      </section>"""


def render_ai_coding_showcase(locale_code: str) -> str:
    """Render the live AI Coding showcase section featuring Shan Hai Bianjing 3D."""
    img_href = html.escape(asset_root_href("/assets/shan-hai-scroll-3d-demo.webp") + "?v=20261126-v4")
    demo_url = (
        "https://tbpfs.github.io/shan-hai-scroll-3d/?lang=en"
        if locale_code == "en"
        else "https://tbpfs.github.io/shan-hai-scroll-3d/"
    )
    repo_url = "https://github.com/tbpfs/shan-hai-scroll-3d"
    svg_url = (
        "https://tbpfs.github.io/formosa-svg-xray/en/"
        if locale_code == "en"
        else "https://tbpfs.github.io/formosa-svg-xray/"
    )
    packs = {
        "zh-TW": {
            "badge": "AI CODING LIVE DEMO · PURE WEBGL2 v4",
            "title": "《山海汴京圖》v4：千里山海四境 × 山海七靈 3D 活古卷",
            "summary": (
                "第一秒以為是張大千潑彩與宋元水墨古卷，滑鼠一拖或點「踏入畫卷」，整幅畫直接破紙化為 380m × 400m 可 360° 第一人稱自由飛行的四大神話仙境——"
                "從汴水虹橋孤舟與躍水錦鯉、蓬萊雲海雙鯤，直飛不周山 75 公尺天然巨型石拱天門仰望 70 公尺翼展應龍穿門而過，再巡遊青丘九尾靈狐與丹山朱鳳。"
                "由紫楓策劃美術方向、Gemini 4 Neon 以純原生 WebGL2 零外部框架全自動寫成（零貼圖、零模型檔、零音檔），支援即時拉開「3D 線框幕簾」透視 104,700+ 三角形。"
            ),
            "heading": "用純粹東方美術藏掉網頁渲染極限：v4 四境七靈潑墨引擎亮點",
            "points": [
                "千里山海四大仙境（380m × 400m）：47 座喀斯特疊峰自無邊鏡面墨海拔起，涵蓋汴水虹橋、蓬萊雲海、75m 不周天門天然石拱與七層寶塔、青丘丹楓嶼與丹山朝陽峰，支援 Shift 馭風 2.4× 加速與六鍵一鍵巡遊。",
                "山海七靈活體生態（104,700+ 三角形）：70m 雙翼流金應龍、北冥雙鯤、三隻丹山朱鳳、兩隻青丘九尾靈狐、兩隻九色發光靈鹿、28 尾躍水錦鯉與 18 隻熱氣流仙鶴，全數在 GPU 頂點著色器即時游動展翅。",
                "潑彩宣紙去 CG 畫風 × 三大博物館級調色：山腳留白溶入鏡海、宣紙毛細滲墨、水彩水痕邊與灑金紙纖徹底抹去塑膠感，可即時切換「潑彩青綠／墨韻丹砂／幽冥青燈」並配以原生古琴泛音。",
            ],
            "alt": "山海汴京圖 v4 WebGL2 即時 3D 潑彩水墨開放世界：左側灑金宣紙古畫與孤舟倒影、右側 104,700 三角形 3D 拓撲線框對照實機畫面",
            "cta_demo": "踏入 3D 水墨畫卷 (Live Demo)",
            "cta_repo": "GitHub 開源原始碼 (MIT)",
            "cta_svg": "另看：Formosa SVG X-Ray 8 層 3D 台灣圖鑑",
        },
        "zh-CN": {
            "badge": "AI CODING LIVE DEMO · PURE WEBGL2 v4",
            "title": "《山海汴京图》v4：千里山海四境 × 山海七灵 3D 活古卷",
            "summary": (
                "第一秒以为是张大千泼彩与宋元水墨古卷，鼠标一拖或点击「踏入画卷」，整幅画直接破纸化为 380m × 400m 可 360° 第一人称自由飞行的四大神话仙境——"
                "从汴水虹桥孤舟与跃水锦鲤、蓬莱云海双鲲，直飞不周山 75 米天然巨型石拱天门仰望 70 米翼展应龙穿门而过，再巡游青丘九尾灵狐与丹山朱凤。"
                "由紫枫策划美术方向、Gemini 4 Neon 以纯原生 WebGL2 零外部框架全自动写成，支持实时拉开「3D 线框幕帘」透视 104,700+ 三角形。"
            ),
            "heading": "用纯粹东方美术藏掉网页渲染极限：v4 四境七灵泼墨引擎亮点",
            "points": [
                "千里山海四大仙境（380m × 400m）：47 座喀斯特叠峰自无边镜面墨海拔起，涵盖汴水虹桥、蓬莱云海、75m 不周天门天然石拱与七层宝塔、青丘丹枫屿与丹山朝阳峰，支持 Shift 驭风 2.4× 加速与六键一键巡游。",
                "山海七灵活体生态（104,700+ 三角形）：70m 双翼流金应龙、北冥双鲲、三只丹山朱凤、两只青丘九尾灵狐、两只九色发光灵鹿、28 尾跃水锦鲤与 18 只热气流仙鹤，全数在 GPU 顶点着色器实时游动展翅。",
                "泼彩宣纸去 CG 画风 × 三大博物馆级调色：山脚留白溶入镜海、宣纸毛细渗墨、水彩水痕边与洒金纸纤彻底抹去塑料感，可实时切换「泼彩青绿／墨韵丹砂／幽冥青灯」并配以原生古琴泛音。",
            ],
            "alt": "山海汴京图 v4 WebGL2 实时 3D 泼彩水墨开放世界：左侧洒金宣纸古画与孤舟倒影、右侧 104,700 三角形 3D 几何线框幕帘对照实机截图",
            "cta_demo": "踏入 3D 水墨画卷 (Live Demo)",
            "cta_repo": "GitHub 开源源码 (MIT)",
            "cta_svg": "另看：Formosa SVG X-Ray 台湾 3D 图鉴",
        },
        "en": {
            "badge": "AI CODING LIVE DEMO · PURE WEBGL2 v4",
            "title": "Shan Hai Bianjing 3D v4: 4 Mythic Ink Realms & 7 Living Beasts in Pure WebGL2",
            "summary": (
                "At first glance it looks like an antique Zhang Daqian splash-ink hanging scroll — until you drag the mouse "
                "and glide 360° across a 380m × 400m open Song world spanning 4 mythic realms: past the Rainbow Bridge boatman "
                "and Twin Kuns, straight through the 75m Mount Buzhou Celestial Stone Arch as a 70m Winged Yinglong Dragon swoops overhead, "
                "to Qingqiu Nine-Tailed Spirit Foxes and Danshan Vermilion Phoenixes. Autonomously coded by Gemini 4 Neon in zero-dependency "
                "WebGL2 with a live Painting-to-3D-Wireframe reveal curtain across 104,700+ procedural triangles."
            ),
            "heading": "Fine-Art Direction Over Brute-Force 3D: v4 Four-Realm Splash-Ink Highlights",
            "points": [
                "4 Mythic Song Realms (380m × 400m): 47 multi-shouldered karst peaks rising directly from an infinite mirror ink sea across Bianjing Bridge, Penglai Cloud Sea, the 75m Buzhou Celestial Arch & 7-tier Imperial Pagoda, Qingqiu Maple Isle, and Danshan Sun Peak — with Shift 2.4× Wind-Glide flight.",
                "7 Living Animated Shan Hai Jing Creatures (104,700+ tris): a 70m Winged Ink-Gold Yinglong Dragon, Twin Celestial Kuns, 3 Vermilion Phoenixes with 15m silk plumes, 2 Nine-Tailed Spirit Foxes, 2 Luminous Spirit Stags, 28 Leaping Koi, and 18 Ink Cranes — all articulated in GPU vertex shaders.",
                "Capillary Xuan-paper ink-bleed & 3 museum palettes: zero muddy dirt banks, watercolor wet-edge pigment pooling, gold-flecked paper fibers, and instant switching across Splash Jade, Ink & Cinnabar, and Moonlit Gold with synthesized Guqin harmonics.",
            ],
            "alt": "Shan Hai Bianjing 3D v4 real-time WebGL2 split view showing splash-ink Xuan-paper painting with boatman reflection on the left and 104,700-triangle 3D wireframe mesh on the right",
            "cta_demo": "Enter the 3D Ink Scroll (Live Demo)",
            "cta_repo": "View GitHub Source (MIT)",
            "cta_svg": "Also see: Formosa SVG X-Ray Lab",
        },
    }
    p = packs.get(locale_code, packs["zh-TW"])
    pts = "\n".join(f"            <li>{html.escape(x)}</li>" for x in p["points"])
    return f"""
      <section class="chapter-card" id="ai-coding-showcase" aria-labelledby="aiShowcaseTitle" style="border-left: 4px solid #bf3426;">
        <div class="chapter-header">
          <span class="badge">{html.escape(p["badge"])}</span>
          <h2 id="aiShowcaseTitle">{html.escape(p["title"])}</h2>
        </div>
        <p class="chapter-summary">{html.escape(p["summary"])}</p>
        <figure style="margin: 14px 0 16px;">
          <a href="{demo_url}" target="_blank" rel="noopener noreferrer" style="display:block;border-radius:8px;overflow:hidden;border:1px solid rgba(148,163,184,0.28);">
            <img src="{img_href}" width="1200" height="675" loading="lazy" decoding="async" alt="{html.escape(p["alt"])}" style="display:block;width:100%;height:auto;">
          </a>
        </figure>
        <div class="concepts-box">
          <h3>{html.escape(p["heading"])}</h3>
          <ul>
{pts}
          </ul>
        </div>
        <div class="cta-group" style="margin-top: 14px;">
          <a class="btn btn-primary" href="{demo_url}" target="_blank" rel="noopener noreferrer">{html.escape(p["cta_demo"])}</a>
          <a class="btn btn-secondary" href="{repo_url}" target="_blank" rel="noopener noreferrer">{html.escape(p["cta_repo"])}</a>
          <a class="btn btn-secondary" href="{svg_url}" target="_blank" rel="noopener noreferrer">{html.escape(p["cta_svg"])}</a>
        </div>
      </section>"""


def build_book_index_json_ld(
    locale_code: str,
    ui: dict[str, Any],
    book: LoadedBook,
) -> dict[str, Any]:
    """Build Schema.org @graph (Book + Course + BreadcrumbList) for a Press book cover page."""
    loc = LOCALE_BY_CODE[locale_code]
    meta = book.meta
    home_url = page_canonical_url(locale_code, None)
    book_url = page_canonical_url(locale_code, f"books/{meta.id}/")
    cover_abs = asset_canonical_url(meta.cover_image)
    creator_ref = {
        "@type": "Person",
        "@id": "https://ai-purplemaple.com/#creator",
        "name": ui["brand_creator_name"],
        "url": "https://ai-purplemaple.com/",
        "sameAs": CREATOR_SAME_AS,
    }
    has_part = [
        {
            "@type": "TechArticle",
            "@id": f"{page_canonical_url(locale_code, f'books/{meta.id}/{cid}.html')}#article",
            "headline": f"{book.chapters_by_locale[locale_code][cid].badge} {book.chapters_by_locale[locale_code][cid].title}",
            "url": page_canonical_url(locale_code, f"books/{meta.id}/{cid}.html"),
        }
        for cid in book.published_chapter_ids
    ]
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Book",
                "@id": f"{book_url}#book",
                "name": meta.title[locale_code],
                "alternateName": meta.subtitle[locale_code],
                "description": meta.description[locale_code],
                "url": book_url,
                "image": cover_abs,
                "inLanguage": loc.jsonld_lang,
                "bookFormat": "https://schema.org/EBook",
                "isAccessibleForFree": True,
                "datePublished": meta.date_published,
                "dateModified": meta.date_modified,
                "author": creator_ref,
                "publisher": creator_ref,
                "copyrightHolder": {"@id": "https://ai-purplemaple.com/#creator"},
                "copyrightYear": 2026,
                "license": "https://ai-purplemaple.com/privacy.html#copyright",
                "hasPart": has_part,
            },
            {
                "@type": "Course",
                "@id": f"{book_url}#course",
                "name": meta.title[locale_code],
                "description": meta.description[locale_code],
                "url": book_url,
                "inLanguage": loc.jsonld_lang,
                "provider": creator_ref,
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": [".aeo-capsule", "header.hero h1"],
                },
                "hasPart": has_part,
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{book_url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": ui["breadcrumb_home_name"], "item": home_url},
                    {"@type": "ListItem", "position": 2, "name": meta.title[locale_code], "item": book_url},
                ],
            },
        ],
    }


def build_book_chapter_json_ld(
    locale_code: str,
    ui: dict[str, Any],
    book: LoadedBook,
    ch: BookChapterData,
) -> dict[str, Any]:
    """Build Schema.org @graph (TechArticle + FAQPage + 3-level BreadcrumbList) for a book chapter."""
    loc = LOCALE_BY_CODE[locale_code]
    meta = book.meta
    home_url = page_canonical_url(locale_code, None)
    book_url = page_canonical_url(locale_code, f"books/{meta.id}/")
    ch_url = page_canonical_url(locale_code, f"books/{meta.id}/{ch.chapter_id}.html")
    cover_abs = asset_canonical_url(meta.cover_image)
    creator_ref = {
        "@type": "Person",
        "@id": "https://ai-purplemaple.com/#creator",
        "name": ui["brand_creator_name"],
        "url": "https://ai-purplemaple.com/",
        "sameAs": CREATOR_SAME_AS,
    }
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TechArticle",
                "@id": f"{ch_url}#article",
                "headline": f"{ch.badge} {ch.title}",
                "description": ch.summary,
                "url": ch_url,
                "mainEntityOfPage": ch_url,
                "image": cover_abs,
                "datePublished": meta.date_published,
                "dateModified": ch.lastmod,
                "inLanguage": loc.jsonld_lang,
                "dependencies": "Python 3.12",
                "keywords": ", ".join(ch.keywords),
                "author": creator_ref,
                "publisher": creator_ref,
                "copyrightHolder": {"@id": "https://ai-purplemaple.com/#creator"},
                "copyrightYear": 2026,
                "license": "https://ai-purplemaple.com/privacy.html#copyright",
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": [".aeo-capsule", "header.hero h1"],
                },
                "isPartOf": {
                    "@type": "Book",
                    "@id": f"{book_url}#book",
                    "name": meta.title[locale_code],
                    "url": book_url,
                },
            },
            {
                "@type": "FAQPage",
                "@id": f"{ch_url}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": faq.question,
                        "acceptedAnswer": {"@type": "Answer", "text": faq.answer},
                    }
                    for faq in ch.interview_faqs
                ],
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{ch_url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": ui["breadcrumb_home_name"], "item": home_url},
                    {"@type": "ListItem", "position": 2, "name": meta.title[locale_code], "item": book_url},
                    {"@type": "ListItem", "position": 3, "name": f"{ch.badge} {ch.title}", "item": ch_url},
                ],
            },
        ],
    }


def render_book_index_page(
    locale_code: str,
    ui: dict[str, Any],
    book: LoadedBook,
) -> str:
    """Render a localized Press Book Cover & Part I-IV TOC page."""
    loc = LOCALE_BY_CODE[locale_code]
    meta = book.meta
    rel_path = f"books/{meta.id}/"
    book_url = page_canonical_url(locale_code, rel_path)
    home_href = page_root_href(locale_code, None)
    cover_abs = asset_canonical_url(meta.cover_image)
    page_title = f"{meta.title[locale_code]} | {ui['site_name']}"
    pub_set = set(book.published_chapter_ids)
    status_label = ui["book_status_serializing"].format(pub=len(pub_set), total=len(book.outlines))

    start_cta = ""
    if book.published_chapter_ids:
        first_id = book.published_chapter_ids[0]
        start_cta = f'<a class="btn btn-primary" href="{first_id}.html">{html.escape(ui["book_cta_start_ch01"])}</a>'
    fb_cta = (
        f'\n            <a class="btn btn-secondary" href="{FB_GROUP_URL}" target="_blank" rel="noopener noreferrer">{html.escape(ui["cta_fb_group"])}</a>'
        if locale_code in ("zh-TW", "zh-CN")
        else ""
    )

    parts_html: list[str] = []
    for part in meta.parts:
        rows: list[str] = []
        for cid in part.chapters:
            outline = book.outlines_by_id[cid]
            title_txt = outline.title[locale_code]
            summary_txt = outline.summary[locale_code]
            if cid in pub_set:
                rows.append(
                    f"""          <li class="book-toc-row is-live">
            <div class="book-toc-main">
              <strong><a href="{cid}.html">{html.escape(outline.badge)} {html.escape(title_txt)}</a></strong>
              <p>{html.escape(summary_txt)}</p>
            </div>
            <span class="status-live">{html.escape(ui["book_published_badge"])}</span>
          </li>"""
                )
            else:
                rows.append(
                    f"""          <li class="book-toc-row is-soon">
            <div class="book-toc-main">
              <strong><span>{html.escape(outline.badge)} {html.escape(title_txt)}</span></strong>
              <p>{html.escape(summary_txt)}</p>
            </div>
            <span class="status-soon">{html.escape(ui["book_coming_soon"])}</span>
          </li>"""
                )
        rows_joined = "\n".join(rows)
        parts_html.append(
            f"""        <section class="book-part-card" id="{html.escape(part.id)}">
          <h3>{html.escape(part.title[locale_code])}</h3>
          <ol class="book-toc-list">
{rows_joined}
          </ol>
        </section>"""
        )

    parts_joined = "\n".join(parts_html)
    json_ld_block = render_json_ld_script(build_book_index_json_ld(locale_code, ui, book))

    return f"""<!DOCTYPE html>
<html lang="{loc.html_lang}">
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
  <title>{html.escape(page_title)}</title>
  <meta name="description" content="{html.escape(meta.description[locale_code])}">
  <meta name="keywords" content="{html.escape(meta.keywords[locale_code])}">
  <meta name="google-adsense-account" content="{ADSENSE_CLIENT_ID}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT_ID}" crossorigin="anonymous"></script>
  <link rel="canonical" href="{book_url}">
{render_hreflang_and_og_locale(locale_code, rel_path)}
{render_rss_alternate_link(locale_code)}
  <meta property="og:site_name" content="{html.escape(ui["site_name"])}">
  <meta property="og:url" content="{book_url}">
  <meta property="og:type" content="book">
  <meta property="og:title" content="{html.escape(meta.title[locale_code])}">
  <meta property="og:description" content="{html.escape(meta.description[locale_code])}">
  <meta property="og:image" content="{cover_abs}">
  <meta property="og:image:alt" content="{html.escape(meta.cover_alt[locale_code])}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@tbpfs1">
  <meta name="twitter:creator" content="@tbpfs1">
  <meta name="twitter:title" content="{html.escape(meta.title[locale_code])}">
  <meta name="twitter:description" content="{html.escape(meta.description[locale_code])}">
  <meta name="twitter:image" content="{cover_abs}">
  <meta name="twitter:image:alt" content="{html.escape(meta.cover_alt[locale_code])}">
{json_ld_block}
{render_shared_styles()}
</head>
<body>
  <div class="container">
    <header class="hero">
{render_lang_switcher(locale_code, rel_path)}
      <div class="book-hero-grid">
        <img class="book-cover-img" src="{html.escape(asset_root_href(meta.cover_image))}" width="{meta.cover_width}" height="{meta.cover_height}" decoding="async" alt="{html.escape(meta.cover_alt[locale_code])}">
        <div>
          <span class="hero-eyebrow">{html.escape(meta.eyebrow[locale_code])}</span>
          <h1>{html.escape(meta.title[locale_code])}</h1>
          <p><a href="{home_href}">{html.escape(ui["book_back_to_shelf"])}</a></p>
          <p>{html.escape(meta.subtitle[locale_code])}</p>
          <p><strong>{html.escape(ui["book_audience_label"])}</strong>{html.escape(meta.audience[locale_code])}</p>
          <div class="cta-group">
            {start_cta}
            <span class="book-pill" style="align-self: center;">{html.escape(status_label)}</span>{fb_cta}
            <a class="btn btn-secondary" href="https://github.com/tbpfs/learning" target="_blank" rel="noopener noreferrer">{html.escape(ui["cta_github"])}</a>
          </div>
        </div>
      </div>
    </header>

    <main>
      <p class="aeo-capsule">{meta.aeo_capsule[locale_code]}</p>
      <section class="chapter-card" id="book-toc">
        <h2>{html.escape(ui["book_toc_heading"])}</h2>
{parts_joined}
      </section>
    </main>

{render_footer(ui)}
  </div>
{render_copy_script(ui, include_cms_fetch=False)}
</body>
</html>
"""


def render_book_chapter_page(
    locale_code: str,
    ui: dict[str, Any],
    book: LoadedBook,
    ch: BookChapterData,
    source_code: str,
    live_output: str,
) -> str:
    """Render a standalone Purple Maple Press chapter page with sticky TOC, SVG diagram, code & quiz."""
    svg_errors = validate_svg_safe(ch.diagram_svg)
    if svg_errors:
        raise ValueError(f"Invalid diagram_svg in {book.meta.id}/{locale_code}/{ch.chapter_id}: {svg_errors}")

    loc = LOCALE_BY_CODE[locale_code]
    meta = book.meta
    rel_path = f"books/{meta.id}/{ch.chapter_id}.html"
    ch_url = page_canonical_url(locale_code, rel_path)
    book_href = page_root_href(locale_code, f"books/{meta.id}/")
    cover_abs = asset_canonical_url(meta.cover_image)
    page_title = f"{ch.badge} {ch.title} | {meta.title[locale_code]}"
    pub_ids = book.published_chapter_ids
    pub_set = set(pub_ids)
    pub_idx = pub_ids.index(ch.chapter_id)

    # Single shared responsive Book TOC drawer (1 DOM instance -> keeps DOM lean)
    sidebar_parts: list[str] = []
    for part in meta.parts:
        items: list[str] = []
        for cid in part.chapters:
            outline = book.outlines_by_id[cid]
            label = f"{outline.badge} {outline.short_title[locale_code]}"
            if cid in pub_set:
                cur = ' aria-current="page"' if cid == ch.chapter_id else ""
                items.append(f'            <li><a class="book-sidebar-link" href="{cid}.html"{cur}>{html.escape(label)}</a></li>')
            else:
                items.append(
                    f'            <li><span class="book-sidebar-soon">{html.escape(label)} ({html.escape(ui["book_coming_soon"])})</span></li>'
                )
        items_joined = "\n".join(items)
        sidebar_parts.append(
            f"""          <div class="book-sidebar-part">{html.escape(part.title[locale_code])}</div>
          <ul class="book-sidebar-list">
{items_joined}
          </ul>"""
        )

    objectives_html = "\n".join(f"            <li>{html.escape(item)}</li>" for item in ch.learning_objectives)

    prose_sections_html: list[str] = []
    for sec in ch.sections:
        paras = "\n".join(f"          <p>{html.escape(p)}</p>" for p in sec.paragraphs)
        bullets = ""
        if sec.bullets:
            li_items = "\n".join(f"            <li>{html.escape(b)}</li>" for b in sec.bullets)
            bullets = f"\n          <ul>\n{li_items}\n          </ul>"
        callout = ""
        if sec.callout_title and sec.callout_body:
            callout = (
                f'\n          <aside class="editorial-callout">'
                f"<strong>{html.escape(sec.callout_title)}</strong>"
                f"<p style=\"margin:0;\">{html.escape(sec.callout_body)}</p>"
                f"</aside>"
            )
        prose_sections_html.append(
            f"""      <section class="chapter-card" id="{html.escape(sec.id)}">
        <h2>{html.escape(sec.heading)}</h2>
        <div class="book-prose">
{paras}{bullets}{callout}
        </div>
      </section>"""
        )

    # Comparison table
    tbl = ch.comparison_table
    tbl_ths = "".join(f'<th scope="col">{html.escape(h)}</th>' for h in tbl.headers)
    tbl_rows = "\n".join(
        "              <tr>"
        + f'<th scope="row">{html.escape(row[0])}</th>'
        + "".join(f"<td>{html.escape(c)}</td>" for c in row[1:])
        + "</tr>"
        for row in tbl.rows
    )

    walkthrough_items = "\n".join(f"            <li>{html.escape(w)}</li>" for w in ch.code_walkthrough)
    pitfalls_html = "\n".join(
        f"""          <div class="pitfall-card">
            <h3>{html.escape(pf.title)}</h3>
            <p class="pitfall-symptom"><strong>{html.escape(ui["book_pitfall_symptom_label"])}</strong>{html.escape(pf.symptom)}</p>
            <p class="pitfall-fix"><strong>{html.escape(ui["book_pitfall_fix_label"])}</strong>{html.escape(pf.root_cause_and_fix)}</p>
          </div>"""
        for pf in ch.pitfalls
    )

    quiz_blocks: list[str] = []
    for q_idx, q in enumerate(ch.quiz, start=1):
        opts = "\n".join(
            f'            <button class="quiz-opt" type="button" data-opt-idx="{o_idx}" aria-pressed="false">{html.escape(opt)}</button>'
            for o_idx, opt in enumerate(q.options)
        )
        quiz_blocks.append(
            f"""        <fieldset class="quiz-card" data-answer-idx="{q.answer_index}">
          <legend>Q{q_idx}. {html.escape(q.question)}</legend>
          <div class="quiz-options">
{opts}
          </div>
          <p class="quiz-feedback" data-explanation="{html.escape(q.explanation, quote=True)}" hidden aria-live="polite"></p>
        </fieldset>"""
        )

    faq_items = "\n".join(
        f"""          <details class="faq-item"{' open' if idx == 0 else ''}>
            <summary>Q. {html.escape(faq.question)}</summary>
            <div class="faq-answer"><p>{html.escape(faq.answer)}</p></div>
          </details>"""
        for idx, faq in enumerate(ch.interview_faqs)
    )

    further_block = ""
    if ch.further_reading:
        fr_items = "\n".join(
            f'          <li><a href="{html.escape(item.url)}" target="_blank" rel="noopener noreferrer">{html.escape(item.title)}</a> — {html.escape(item.note)}</li>'
            for item in ch.further_reading
        )
        further_block = f"""
      <section class="chapter-card" id="further-reading">
        <h2>{html.escape(ui["book_further_heading"])}</h2>
        <div class="book-prose">
          <ul>
{fr_items}
          </ul>
        </div>
      </section>"""

    # Pager skips unpublished chapters
    prev_cid = pub_ids[pub_idx - 1] if pub_idx > 0 else None
    next_cid = pub_ids[pub_idx + 1] if pub_idx + 1 < len(pub_ids) else None
    if prev_cid:
        po = book.outlines_by_id[prev_cid]
        prev_html = f'<a class="pager-link" href="{prev_cid}.html">{html.escape(ui["pager_prev_tpl"].format(badge=po.badge, short=po.short_title[locale_code]))}</a>'
    else:
        prev_html = f'<span class="pager-link pager-disabled">{html.escape(ui["pager_first"])}</span>'
    if next_cid:
        no = book.outlines_by_id[next_cid]
        next_html = f'<a class="pager-link" href="{next_cid}.html">{html.escape(ui["pager_next_tpl"].format(badge=no.badge, short=no.short_title[locale_code]))}</a>'
    else:
        next_html = f'<span class="pager-link pager-disabled">{html.escape(ui["pager_last"])}</span>'

    json_ld_block = render_json_ld_script(build_book_chapter_json_ld(locale_code, ui, book, ch))
    toolbar_lbl = html.escape(ui["code_toolbar_tpl"].format(file=ch.example_file))
    reading_lbl = html.escape(ui["book_reading_time_tpl"].format(mins=ch.reading_minutes))
    back_book_lbl = html.escape(ui["book_back_to_toc"].format(book_title=meta.title[locale_code]))
    sidebar_joined = "\n".join(sidebar_parts)
    prose_sections_joined = "\n".join(prose_sections_html)
    quiz_blocks_joined = "\n".join(quiz_blocks)

    return f"""<!DOCTYPE html>
<html lang="{loc.html_lang}">
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
  <title>{html.escape(page_title)}</title>
  <meta name="description" content="{html.escape(ch.summary)}">
  <meta name="keywords" content="{html.escape(', '.join(ch.keywords))}">
  <meta name="google-adsense-account" content="{ADSENSE_CLIENT_ID}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT_ID}" crossorigin="anonymous"></script>
  <link rel="canonical" href="{ch_url}">
{render_hreflang_and_og_locale(locale_code, rel_path)}
{render_rss_alternate_link(locale_code)}
  <meta property="og:site_name" content="{html.escape(ui["site_name"])}">
  <meta property="og:url" content="{ch_url}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{html.escape(page_title)}">
  <meta property="og:description" content="{html.escape(ch.summary)}">
  <meta property="og:image" content="{cover_abs}">
  <meta property="og:image:alt" content="{html.escape(meta.cover_alt[locale_code])}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@tbpfs1">
  <meta name="twitter:creator" content="@tbpfs1">
  <meta name="twitter:title" content="{html.escape(page_title)}">
  <meta name="twitter:description" content="{html.escape(ch.summary)}">
  <meta name="twitter:image" content="{cover_abs}">
  <meta name="twitter:image:alt" content="{html.escape(meta.cover_alt[locale_code])}">
{json_ld_block}
{render_shared_styles()}
</head>
<body>
  <div class="read-progress" aria-hidden="true"><div class="read-progress-bar" id="readProgressBar"></div></div>
  <div class="container book-container">
    <header class="hero">
{render_lang_switcher(locale_code, rel_path)}
      <span class="hero-eyebrow">{html.escape(meta.eyebrow[locale_code])} · {html.escape(ch.badge)}</span>
      <h1>{html.escape(ch.badge + " " + ch.title)}</h1>
      <p><a href="{book_href}">{back_book_lbl}</a></p>
      <p>{html.escape(ch.summary)}</p>
      <div class="meta-bar" style="margin-top: 1rem; margin-bottom: 0;">
        <span>{reading_lbl}</span>
        <span><strong>{html.escape(ui["label_source_path"])}</strong><code>{html.escape(ch.example_file)}</code></span>
        {render_dates_meta_html(locale_code, meta.date_published, ch.lastmod)}
      </div>
      <div class="cta-group">
        <a class="btn btn-primary" href="#code-section">{html.escape(ui["book_nav_code"])}</a>
        <a class="btn btn-secondary" href="https://github.com/tbpfs/learning/blob/main/{html.escape(ch.example_file)}" target="_blank" rel="noopener noreferrer">{html.escape(ui["cta_chapter_github"])}</a>
        <a class="btn btn-secondary" href="{book_href}">{html.escape(ui["book_pager_home"])}</a>
      </div>
    </header>

    <nav class="section-subnav" aria-label="{html.escape(ui["section_subnav_aria"])}">
      <span>{html.escape(ui["section_subnav_label"])}</span>
      <a href="#objectives">{html.escape(ui["book_nav_objectives"])}</a>
      <a href="#diagram">{html.escape(ui["book_nav_diagram"])}</a>
      <a href="#comparison">{html.escape(ui["book_nav_comparison"])}</a>
      <a href="#code-section">{html.escape(ui["book_nav_code"])}</a>
      <a href="#pitfalls">{html.escape(ui["book_nav_pitfalls"])}</a>
      <a href="#quiz">{html.escape(ui["book_nav_quiz"])}</a>
      <a href="#interview-faq">{html.escape(ui["book_nav_faq"])}</a>
    </nav>

    <div class="book-layout">
      <aside aria-label="{html.escape(ui["book_toc_heading"])}">
        <details class="book-toc-drawer" open>
          <summary>{html.escape(ui["book_sidebar_summary"])}</summary>
{sidebar_joined}
        </details>
      </aside>

      <main>
        <article class="chapter-card" id="objectives">
          <h2>{html.escape(ui["book_objectives_heading"])}</h2>
          <p class="aeo-capsule">{ch.aeo_capsule}</p>
          <div class="concepts-box">
            <ul>
{objectives_html}
            </ul>
          </div>
        </article>

{prose_sections_joined}

        <section class="chapter-card" id="diagram">
          <h2>{html.escape(ui["book_diagram_heading"])}</h2>
          <figure class="diagram-figure">
            {ch.diagram_svg}
            <figcaption>{html.escape(ch.diagram_caption)}</figcaption>
          </figure>
        </section>

        <section class="chapter-card" id="comparison">
          <h2>{html.escape(ui["comparison_heading"])}</h2>
          <div class="table-responsive">
            <table class="comparison-table">
              <caption>{html.escape(tbl.caption)}</caption>
              <thead>
                <tr>{tbl_ths}</tr>
              </thead>
              <tbody>
{tbl_rows}
              </tbody>
            </table>
          </div>
        </section>

        <section class="chapter-card" id="code-section">
          <h2>{html.escape(ui["code_section_heading"])}</h2>
          <div class="concepts-box">
            <h3>{html.escape(ui["book_walkthrough_heading"])}</h3>
            <ul>
{walkthrough_items}
            </ul>
          </div>
          <div class="code-container">
            <div class="code-toolbar">
              <span>{toolbar_lbl}</span>
              <button type="button" class="copy-btn" data-target="code-{html.escape(meta.id)}-{html.escape(ch.chapter_id)}">{html.escape(ui["copy_btn"])}</button>
            </div>
            <pre><code id="code-{html.escape(meta.id)}-{html.escape(ch.chapter_id)}">{html.escape(source_code)}</code></pre>
          </div>
          <div class="output-box">
            <div class="output-label">{html.escape(ui["output_label_chapter"])}</div>
            <pre class="output-pre">{html.escape(live_output)}</pre>
          </div>
        </section>

        <section class="chapter-card" id="pitfalls">
          <h2>{html.escape(ui["book_pitfalls_heading"])}</h2>
          <div class="pitfall-list">
{pitfalls_html}
          </div>
        </section>

        <section class="chapter-card" id="quiz">
          <h2>{html.escape(ui["book_quiz_heading"])}</h2>
          <p class="chapter-summary">{html.escape(ui["book_quiz_intro"])}</p>
{quiz_blocks_joined}
        </section>

        <section class="chapter-card" id="interview-faq">
          <h2>{html.escape(ui["book_faq_heading"])}</h2>
          <div class="faq-list">
{faq_items}
          </div>
        </section>{further_block}

{render_feedback_section(f"{meta.id}-{ch.chapter_id}", f"{meta.title[locale_code]} — {ch.badge} {ch.title}", ch_url, locale_code, ui, fb_mode="local")}

        <nav class="chapter-pager" aria-label="{html.escape(ui["pager_aria"])}">
          {prev_html}
          <a class="pager-link pager-home" href="{book_href}">{html.escape(ui["book_pager_home"])}</a>
          {next_html}
        </nav>
      </main>
    </div>

{render_footer(ui)}
  </div>
{render_copy_script(ui, include_cms_fetch=False)}
</body>
</html>
"""


def render_index_page(
    locale_code: str,
    ui: dict[str, Any],
    chapters: Sequence[ChapterSpec],
    exec_cache: dict[str, tuple[str, str]],
    chapter_titles_short: str,
    resources: Sequence[AffiliateResource],
    books: Sequence[LoadedBook] = (),
) -> str:
    """Render a localized Course Hub index.html (summary cards + progressive disclosure code sandbox)."""
    loc = LOCALE_BY_CODE[locale_code]
    index_url = page_canonical_url(locale_code, None)
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
        short_name = html.escape(chapter_short_title(ch))
        open_attr = " open" if idx == 1 else ""

        toc_items_html.append(
            f"""      <a class="toc-item" href="#{ch.id}">
        <span class="badge">{ch.badge}</span>
        <strong>{short_name}</strong>
      </a>"""
        )

        acc_summary = ui["code_accordion_summary_tpl"].format(
            badge=html.escape(ch.badge), file=escaped_file
        )
        toolbar_lbl = html.escape(ui["code_toolbar_tpl"].format(file=ch.file))

        cards_html.append(
            f"""
      <article class="chapter-card" id="{ch.id}">
        <div class="chapter-header">
          <span class="badge">{ch.badge}</span>
          <h2><a href="{ch.id}.html" style="color: inherit;">{escaped_title}</a></h2>
          <a href="{ch.id}.html" style="margin-left: auto; font-size: 0.86rem; font-weight: 600;">{html.escape(ui["chapter_link_cta"])}</a>
        </div>
        <p class="chapter-summary">{escaped_summary}</p>
        <div class="concepts-box">
          <h3>{html.escape(ui["concepts_heading"])}</h3>
          <ul>
{concepts_items}
          </ul>
        </div>
        <div class="meta-bar">
          <span><strong>{html.escape(ui["label_complexity"])}</strong>{escaped_complexity}</span>
          <span><strong>{html.escape(ui["label_source_path"])}</strong><code>{escaped_file}</code></span>
          {render_dates_meta_html(locale_code, DSA_DATE_PUBLISHED, ch.lastmod)}
        </div>
        <details class="code-accordion"{open_attr}>
          <summary class="code-accordion-summary">{acc_summary}</summary>
          <div class="code-container">
            <div class="code-toolbar">
              <span>{toolbar_lbl}</span>
              <button type="button" class="copy-btn" data-target="code-{ch.id}">{html.escape(ui["copy_btn"])}</button>
            </div>
            <pre><code id="code-{ch.id}">{escaped_code}</code></pre>
          </div>
          <div class="output-box">
            <div class="output-label">{html.escape(ui["output_label_index"])}</div>
            <pre class="output-pre">{escaped_out}</pre>
          </div>
        </details>
{render_deep_dive_callout(ch, ui)}
      </article>"""
        )
        cards_html.append(render_ad_slot(f"Ch.0{idx} Ad Slot"))

    all_cards = "\n".join(cards_html)
    toc_block = "\n".join(toc_items_html)
    index_desc_esc = html.escape(ui["index_desc_tpl"].format(chapter_titles_short=chapter_titles_short))
    index_og_desc_esc = html.escape(ui["index_og_desc_tpl"].format(chapter_titles_short=chapter_titles_short))
    og_title_esc = html.escape(ui.get("og_title", ui["page_title"]))
    json_ld_block = render_json_ld_script(build_index_json_ld(locale_code, ui, chapters, chapter_titles_short))

    fb_cta = (
        f'\n        <a class="btn btn-secondary" href="{FB_GROUP_URL}" target="_blank" rel="noopener noreferrer">{html.escape(ui["cta_fb_group"])}</a>'
        if locale_code in ("zh-TW", "zh-CN")
        else ""
    )
    cms_div = '\n      <div id="cms-tutorials-container"></div>' if locale_code == "zh-TW" else ""
    bookshelf_html = render_bookshelf_section(locale_code, ui, books) if books else ""
    showcase_html = render_ai_coding_showcase(locale_code)
    study_items_html = "\n".join(
        f"            <li><strong>{html.escape(label)}</strong>{body_html}</li>"
        for label, body_html in ui["study_guide_items"]
    )

    return f"""<!DOCTYPE html>
<html lang="{loc.html_lang}">
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
  <title>{html.escape(ui["page_title"])}</title>
  <meta name="description" content="{index_desc_esc}">
  <meta name="keywords" content="{html.escape(ui["index_keywords"])}">
  <meta name="google-adsense-account" content="{ADSENSE_CLIENT_ID}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT_ID}" crossorigin="anonymous"></script>
  <link rel="canonical" href="{index_url}">
{render_hreflang_and_og_locale(locale_code, None)}
  <link rel="alternate" type="text/markdown" href="{SITE_BASE_URL}/llms.txt" title="LLM Chapter Index">
  <link rel="alternate" type="text/markdown" href="{SITE_BASE_URL}/llms-full.txt" title="LLM Full Tutorial & Code Corpus">
{render_rss_alternate_link(locale_code)}
  <meta property="og:site_name" content="{html.escape(ui["site_name"])}">
  <meta property="og:url" content="{index_url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{og_title_esc}">
  <meta property="og:description" content="{index_og_desc_esc}">
  <meta property="og:image" content="https://ai-purplemaple.com/assets/gallery/aily_03.jpg">
  <meta property="og:image:alt" content="{html.escape(ui["og_image_alt"])}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@tbpfs1">
  <meta name="twitter:creator" content="@tbpfs1">
  <meta name="twitter:title" content="{og_title_esc}">
  <meta name="twitter:description" content="{index_og_desc_esc}">
  <meta name="twitter:image" content="https://ai-purplemaple.com/assets/gallery/aily_03.jpg">
  <meta name="twitter:image:alt" content="{html.escape(ui["og_image_alt"])}">
{json_ld_block}
{render_shared_styles()}
</head>
<body>
  <div class="container">
    <header class="hero">
{render_lang_switcher(locale_code, None)}
      <span class="hero-eyebrow">{html.escape(ui["hero_eyebrow"])}</span>
      <h1>{html.escape(ui["hero_h1"])}</h1>
      <p>{ui["hero_intro_html"]}</p>
      <div class="cta-group">
        <a class="btn btn-primary" href="https://www.youtube.com/playlist?list=PLhxdaTcUMi3nRM5mtOdQgO4VEtAEsTiYd" target="_blank" rel="noopener noreferrer">{html.escape(ui["cta_youtube"])}</a>
        <a class="btn btn-secondary" href="https://ai-purplemaple.com/" target="_blank" rel="noopener noreferrer">{html.escape(ui["brand_anchor_portfolio"])}</a>{fb_cta}
        <a class="btn btn-secondary" href="https://github.com/tbpfs/learning" target="_blank" rel="noopener noreferrer">{html.escape(ui["cta_github"])}</a>
      </div>
    </header>

    <nav class="toc" aria-label="{html.escape(ui["toc_aria"])}">
{toc_block}
    </nav>

    <main>
      <p class="aeo-capsule">{ui["index_aeo_capsule"]}</p>{bookshelf_html}{showcase_html}{cms_div}
{all_cards}
{render_affiliate_resources_section(locale_code, ui, resources)}

      <section class="study-guide-card" id="study-guide">
        <h2>{html.escape(ui["study_guide_heading"])}</h2>
        <p>{html.escape(ui["study_guide_intro"])}</p>
        <details class="study-guide-accordion">
          <summary class="study-guide-summary">{html.escape(ui["study_guide_summary"])}</summary>
          <ul>
{study_items_html}
          </ul>
        </details>
      </section>
    </main>

{render_footer(ui)}
  </div>

{render_copy_script(ui, include_cms_fetch=(locale_code == "zh-TW"))}
</body>
</html>
"""


def render_chapter_page(
    locale_code: str,
    ui: dict[str, Any],
    idx: int,
    chapters: Sequence[ChapterSpec],
    exec_cache: dict[str, tuple[str, str]],
    yt_videos: dict[str, dict[str, Any]],
    chapter_resources: dict[str, tuple[str, str]] | None = None,
) -> str:
    """Render a standalone deep-dive tutorial page (ch01.html .. ch07.html) for a given locale."""
    loc = LOCALE_BY_CODE[locale_code]
    ch = chapters[idx]
    source_code, live_output = exec_cache[ch.id]
    page_filename = f"{ch.id}.html"
    ch_url = page_canonical_url(locale_code, page_filename)
    home_href = page_root_href(locale_code, None)

    short_t = chapter_short_title(ch)
    raw_ch_title = ui["chapter_title_tpl"].format(badge=ch.badge, title=ch.title, short_title=short_t)
    raw_ch_desc = ui["chapter_desc_tpl"].format(badge=ch.badge, title=ch.title, short_title=short_t, summary=ch.summary)
    if locale_code == "en" and len(raw_ch_desc) > 155:
        cut = raw_ch_desc[:154].rsplit(" ", 1)[0].rstrip(",;:- ")
        raw_ch_desc = f"{cut}…"
    ch_title_esc = html.escape(raw_ch_title)
    ch_desc_esc = html.escape(raw_ch_desc)
    ch_keywords_esc = html.escape(ui["chapter_keywords_prefix"] + ", ".join(ch.keywords))
    json_ld_block = render_json_ld_script(build_chapter_json_ld(locale_code, ui, ch, yt_videos))

    switcher_items: list[str] = []
    for item in chapters:
        current_attr = ' aria-current="page"' if item.id == ch.id else ""
        short_label = html.escape(chapter_short_title(item))
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
    ch_eyebrow = html.escape(ui["chapter_eyebrow_tpl"].format(badge=ch.badge))
    ch_aeo = ui["chapter_aeo_tpl"].format(
        badge=html.escape(ch.badge),
        title=html.escape(ch.title),
        summary=html.escape(ch.summary),
        complexity=escaped_complexity,
        file=escaped_file,
    )
    toolbar_lbl = html.escape(ui["code_toolbar_tpl"].format(file=ch.file))

    return f"""<!DOCTYPE html>
<html lang="{loc.html_lang}">
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
{render_hreflang_and_og_locale(locale_code, page_filename)}
{render_rss_alternate_link(locale_code)}
  <meta property="og:site_name" content="{html.escape(ui["site_name"])}">
  <meta property="og:url" content="{ch_url}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{ch_title_esc}">
  <meta property="og:description" content="{ch_desc_esc}">
  <meta property="og:image" content="https://ai-purplemaple.com/assets/gallery/aily_03.jpg">
  <meta property="og:image:alt" content="{html.escape(ui["og_image_alt"])}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@tbpfs1">
  <meta name="twitter:creator" content="@tbpfs1">
  <meta name="twitter:title" content="{ch_title_esc}">
  <meta name="twitter:description" content="{ch_desc_esc}">
  <meta name="twitter:image" content="https://ai-purplemaple.com/assets/gallery/aily_03.jpg">
  <meta name="twitter:image:alt" content="{html.escape(ui["og_image_alt"])}">
{json_ld_block}
{render_shared_styles()}
</head>
<body>
  <div class="container">
    <header class="hero">
{render_lang_switcher(locale_code, page_filename)}
      <span class="hero-eyebrow">{ch_eyebrow}</span>
      <h1>{html.escape(ch.badge + " " + ch.title)}</h1>
      <p><a href="{home_href}">{html.escape(ui["back_to_index_label"])}</a></p>
      <p>{html.escape(ch.summary)}</p>
      <div class="cta-group">
        <a class="btn btn-primary" href="https://www.youtube.com/playlist?list=PLhxdaTcUMi3nRM5mtOdQgO4VEtAEsTiYd" target="_blank" rel="noopener noreferrer">{html.escape(ui["cta_youtube"])}</a>
        <a class="btn btn-secondary" href="https://ai-purplemaple.com/" target="_blank" rel="noopener noreferrer">{html.escape(ui["brand_anchor_portfolio_short"])}</a>
        <a class="btn btn-secondary" href="https://github.com/tbpfs/learning/blob/main/{escaped_file}" target="_blank" rel="noopener noreferrer">{html.escape(ui["cta_chapter_github"])}</a>
      </div>
    </header>

    <nav class="chapter-switcher" aria-label="{html.escape(ui["chapter_switcher_aria"])}">
{switcher_html}
    </nav>

    <nav class="section-subnav" aria-label="{html.escape(ui["section_subnav_aria"])}">
      <span>{html.escape(ui["section_subnav_label"])}</span>
      <a href="#intro">{html.escape(ui["nav_intro"])}</a>
      <a href="#video-lecture">{html.escape(ui["nav_video"])}</a>
      <a href="#comparison">{html.escape(ui["nav_comparison"])}</a>
      <a href="#walkthrough">{html.escape(ui["nav_walkthrough"])}</a>
      <a href="#code-section">{html.escape(ui["nav_code"])}</a>
      <a href="#pitfalls">{html.escape(ui["nav_pitfalls"])}</a>
      <a href="#interview-faq">{html.escape(ui["nav_interview"])}</a>
    </nav>

    <main>
      <article class="chapter-card" id="intro">
        <h2>{html.escape(ui["chapter_intro_heading"])}</h2>
        <p class="aeo-capsule">{ch_aeo}</p>
        <p class="deep-intro-text">{html.escape(ch.deep_intro)}</p>
        <div class="concepts-box">
          <h3>{html.escape(ui["concepts_heading"])}</h3>
          <ul>
{concepts_items}
          </ul>
        </div>
        <div class="meta-bar">
          <span><strong>{html.escape(ui["label_complexity"])}</strong>{escaped_complexity}</span>
          <span><strong>{html.escape(ui["label_source_path"])}</strong><code>{escaped_file}</code></span>
          {render_dates_meta_html(locale_code, DSA_DATE_PUBLISHED, ch.lastmod)}
        </div>
      </article>

{render_video_lecture_section(ch, ui, yt_videos)}

      <section class="chapter-card" id="comparison">
        <h2>{html.escape(ui["comparison_heading"])}</h2>
{render_comparison_table(ch.comparison_table)}
      </section>

{render_walkthrough(ch)}

{render_ad_slot(f"{ch.badge} Mid Ad Slot")}

      <section class="chapter-card" id="code-section">
        <h2>{html.escape(ui["code_section_heading"])}</h2>
        <div class="code-container">
          <div class="code-toolbar">
            <span>{toolbar_lbl}</span>
            <button type="button" class="copy-btn" data-target="code-{ch.id}">{html.escape(ui["copy_btn"])}</button>
          </div>
          <pre><code id="code-{ch.id}">{escaped_code}</code></pre>
        </div>
        <div class="output-box">
          <div class="output-label">{html.escape(ui["output_label_chapter"])}</div>
          <pre class="output-pre">{escaped_out}</pre>
        </div>
      </section>

{render_pitfalls(ch, ui)}

{render_interview_section(ch, ui)}

{render_chapter_book_callout(locale_code, ch, ui, chapter_resources=chapter_resources)}

{render_feedback_section(ch.id, f"{ch.badge} {ch.title}", ch_url, locale_code, ui, fb_mode="api")}

{render_ad_slot(f"{ch.badge} Footer Ad Slot")}

{render_chapter_pager(locale_code, idx, chapters, ui)}
    </main>

{render_footer(ui)}
  </div>

{render_copy_script(ui, include_cms_fetch=False)}
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
        "User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /cdn-cgi/\n\n"
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
        f"Sitemap: {SITE_BASE_URL}/sitemap.xml\n"
        f"# LLMs Chapter Index: {SITE_BASE_URL}/llms.txt\n"
        f"# LLMs Full Code & Output Corpus: {SITE_BASE_URL}/llms-full.txt\n",
        encoding="utf-8",
    )

    assets_src = REPO_ROOT / "assets"
    if assets_src.is_dir():
        shutil.copytree(assets_src, out_dir / "assets", dirs_exist_ok=True)

    books = discover_books(REPO_ROOT / "books")
    book_exec_cache: dict[tuple[str, str], tuple[str, str]] = {}
    for book in books:
        for cid in book.published_chapter_ids:
            ch_tw = book.chapters_by_locale["zh-TW"][cid]
            book_exec_cache[(book.meta.id, cid)] = run_example(ch_tw.example_file)

    raw_exec_cache = execute_all_examples(CHAPTERS)

    llms_chapter_lines: list[str] = []
    llms_zh_cn_lines: list[str] = []
    llms_en_lines: list[str] = []
    llms_full_sections: list[str] = []
    sitemap_urls: list[tuple[str, str, str]] = []
    rss_items_by_locale: dict[str, list[dict[str, str]]] = {
        "zh-TW": [],
        "zh-CN": [],
        "en": [],
    }

    # 1. Build Traditional Chinese (root) + full corpus
    sitemap_urls.append((page_canonical_url("zh-TW", None), "1.0", SITE_LASTMOD))
    for ch in CHAPTERS:
        source_code, live_output = raw_exec_cache[ch.id]
        ch_url = page_canonical_url("zh-TW", f"{ch.id}.html")
        sitemap_urls.append((ch_url, "0.9", ch.lastmod))
        rss_items_by_locale["zh-TW"].append(
            {
                "title": f"{ch.badge} {ch.title}",
                "link": ch_url,
                "summary": ch.summary,
                "pub_date": DSA_DATE_PUBLISHED,
                "mod_date": ch.lastmod,
                "sort_key": f"1-{ch.id}",
            }
        )
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

    chapter_titles_short_tw = "、".join(f"{ch.badge} {chapter_short_title(ch)}" for ch in CHAPTERS)
    index_html = render_index_page(
        "zh-TW",
        UI_ZH_TW,
        CHAPTERS,
        raw_exec_cache,
        chapter_titles_short_tw,
        get_learning_resources(),
        books=books,
    )
    index_path = out_dir / "index.html"
    index_path.write_text(index_html, encoding="utf-8")

    for idx, ch in enumerate(CHAPTERS):
        ch_html = render_chapter_page(
            "zh-TW",
            UI_ZH_TW,
            idx,
            CHAPTERS,
            raw_exec_cache,
            CHAPTER_YOUTUBE_VIDEOS,
        )
        (out_dir / f"{ch.id}.html").write_text(ch_html, encoding="utf-8")

    # 1b. Build Purple Maple Press books (zh-TW)
    for book in books:
        bdir = out_dir / "books" / book.meta.id
        bdir.mkdir(parents=True, exist_ok=True)
        book_url = page_canonical_url("zh-TW", f"books/{book.meta.id}/")
        sitemap_urls.append((book_url, "0.95", book.meta.date_modified))
        llms_chapter_lines.append(
            f"- [專書：{book.meta.title['zh-TW']}]({book_url}): 已上線 {len(book.published_chapter_ids)}/{len(book.outlines)} 章"
        )
        (bdir / "index.html").write_text(render_book_index_page("zh-TW", UI_ZH_TW, book), encoding="utf-8")
        for cid in book.published_chapter_ids:
            bch = book.chapters_by_locale["zh-TW"][cid]
            bsrc, bout = book_exec_cache[(book.meta.id, cid)]
            bch_url = page_canonical_url("zh-TW", f"books/{book.meta.id}/{cid}.html")
            sitemap_urls.append((bch_url, "0.9", bch.lastmod))
            rss_items_by_locale["zh-TW"].append(
                {
                    "title": f"{book.meta.title['zh-TW'].split('：')[0]} — {bch.badge} {bch.title}",
                    "link": bch_url,
                    "summary": bch.summary,
                    "pub_date": book.meta.date_published,
                    "mod_date": bch.lastmod,
                    "sort_key": f"2-{book.meta.id}-{cid}",
                }
            )
            llms_chapter_lines.append(
                f"- [{book.meta.title['zh-TW']} — {bch.badge} {bch.title}]({bch_url}): `{bch.example_file}`"
            )
            (bdir / f"{cid}.html").write_text(
                render_book_chapter_page("zh-TW", UI_ZH_TW, book, bch, bsrc, bout),
                encoding="utf-8",
            )
            sec_md = "\n\n".join(
                f"### {sec.heading}\n" + "\n\n".join(sec.paragraphs) for sec in bch.sections
            )
            llms_full_sections.append(
                f"## {book.meta.title['zh-TW']} — {bch.badge} {bch.title}\n"
                f"- **獨立章節網址**：{bch_url}\n"
                f"- **原始碼路徑**：`{bch.example_file}`\n"
                f"- **章節摘要**：{bch.summary}\n\n"
                f"{sec_md}\n\n"
                f"### Python 3.12 完整範例原始碼 (`{bch.example_file}`)\n"
                f"```python\n{bsrc.rstrip()}\n```\n\n"
                f"### CI 實機執行輸出驗證\n"
                f"```text\n{bout}\n```"
            )

    # 2. Build Simplified Chinese (/zh-cn/) and International English (/en/)
    for loc_code in ("zh-CN", "en"):
        loc = LOCALE_BY_CODE[loc_code]
        pack = load_locale_pack(loc_code)
        loc_chapters: Sequence[ChapterSpec] = pack["chapters"]
        loc_ui: dict[str, Any] = pack["ui"]
        loc_yt: dict[str, dict[str, Any]] = pack["youtube"]
        loc_resources: Sequence[AffiliateResource] = pack["resources"]
        loc_ch_resources: dict[str, tuple[str, str]] = pack["chapter_resources"]
        code_map = pack["code_replacements"]
        out_map = pack["output_replacements"]

        loc_exec_cache: dict[str, tuple[str, str]] = {}
        for ch in loc_chapters:
            raw_src, raw_out = raw_exec_cache[ch.id]
            loc_exec_cache[ch.id] = localize_code_and_output(
                loc_code, ch.id, raw_src, raw_out, code_map, out_map
            )

        sep = "、" if loc_code == "zh-CN" else ", "
        loc_titles_short = sep.join(f"{ch.badge} {chapter_short_title(ch)}" for ch in loc_chapters)

        loc_dir = out_dir / loc.output_subdir
        loc_dir.mkdir(parents=True, exist_ok=True)
        sitemap_urls.append((page_canonical_url(loc_code, None), "1.0", SITE_LASTMOD))

        loc_index_html = render_index_page(
            loc_code,
            loc_ui,
            loc_chapters,
            loc_exec_cache,
            loc_titles_short,
            loc_resources,
            books=books,
        )
        (loc_dir / "index.html").write_text(loc_index_html, encoding="utf-8")

        target_llms_list = llms_zh_cn_lines if loc_code == "zh-CN" else llms_en_lines
        for idx, ch in enumerate(loc_chapters):
            ch_url = page_canonical_url(loc_code, f"{ch.id}.html")
            sitemap_urls.append((ch_url, "0.9", ch.lastmod))
            rss_items_by_locale[loc_code].append(
                {
                    "title": f"{ch.badge} {ch.title}",
                    "link": ch_url,
                    "summary": ch.summary,
                    "pub_date": DSA_DATE_PUBLISHED,
                    "mod_date": ch.lastmod,
                    "sort_key": f"1-{ch.id}",
                }
            )
            target_llms_list.append(
                f"- [{ch.badge} {ch.title}]({ch_url}): `{ch.file}` — {ch.complexity}"
            )
            loc_ch_html = render_chapter_page(
                loc_code,
                loc_ui,
                idx,
                loc_chapters,
                loc_exec_cache,
                loc_yt,
                chapter_resources=loc_ch_resources,
            )
            (loc_dir / f"{ch.id}.html").write_text(loc_ch_html, encoding="utf-8")

        # 2b. Build Purple Maple Press books for zh-CN / en
        for book in books:
            bdir = loc_dir / "books" / book.meta.id
            bdir.mkdir(parents=True, exist_ok=True)
            book_url = page_canonical_url(loc_code, f"books/{book.meta.id}/")
            sitemap_urls.append((book_url, "0.95", book.meta.date_modified))
            target_llms_list.append(
                f"- [{book.meta.title[loc_code]}]({book_url}): {len(book.published_chapter_ids)}/{len(book.outlines)}"
            )
            (bdir / "index.html").write_text(render_book_index_page(loc_code, loc_ui, book), encoding="utf-8")
            for cid in book.published_chapter_ids:
                bch = book.chapters_by_locale[loc_code][cid]
                raw_src, raw_out = book_exec_cache[(book.meta.id, cid)]
                loc_src, loc_out = localize_code_and_output(
                    loc_code,
                    cid,
                    raw_src,
                    raw_out,
                    {cid: bch.code_replacements},
                    {cid: bch.output_replacements},
                )
                bch_url = page_canonical_url(loc_code, f"books/{book.meta.id}/{cid}.html")
                sitemap_urls.append((bch_url, "0.9", bch.lastmod))
                book_short_title = book.meta.title[loc_code].split("：")[0].split(":")[0]
                rss_items_by_locale[loc_code].append(
                    {
                        "title": f"{book_short_title} — {bch.badge} {bch.title}",
                        "link": bch_url,
                        "summary": bch.summary,
                        "pub_date": book.meta.date_published,
                        "mod_date": bch.lastmod,
                        "sort_key": f"2-{book.meta.id}-{cid}",
                    }
                )
                target_llms_list.append(
                    f"- [{book.meta.title[loc_code]} — {bch.badge} {bch.title}]({bch_url}): `{bch.example_file}`"
                )
                (bdir / f"{cid}.html").write_text(
                    render_book_chapter_page(loc_code, loc_ui, book, bch, loc_src, loc_out),
                    encoding="utf-8",
                )

    total_pages = len(sitemap_urls)
    sitemap_entries = "\n".join(
        f"  <url>\n    <loc>{loc_url}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        for loc_url, prio, lastmod in sitemap_urls
    )
    (out_dir / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{sitemap_entries}\n"
        "</urlset>\n",
        encoding="utf-8",
    )

    for loc_code, feed_meta in RSS_FEED_META.items():
        rss_path = out_dir / feed_meta["rel_out"]
        rss_path.parent.mkdir(parents=True, exist_ok=True)
        rss_path.write_text(build_rss_xml(loc_code, rss_items_by_locale[loc_code]), encoding="utf-8")

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
        "- [山海汴京圖 3D v4（清明上河圖 × 山海經純 WebGL2 四境七靈開放水墨世界）](https://tbpfs.github.io/shan-hai-scroll-3d/): 由 Gemini 4 Neon 全自動零外部框架實作之 380m×400m 四大宋代仙境、7 種《山海經》活體神獸（應龍、雙鯤、朱鳳、九尾靈狐、九色靈鹿、錦鯉、仙鶴）與 104,700+ 三角形即時線框幕簾（開源 MIT：https://github.com/tbpfs/shan-hai-scroll-3d）\n"
        "- [Formosa SVG X-Ray（AI Coding 零依賴 8 層 3D 活體台灣 SVG 展示庫）](https://tbpfs.github.io/formosa-svg-xray/): 由 Gemini 4 Neon 全自動打造之九份雨夜、台南神農街與台北 101 單檔互動場景與 3D 圖層炸裂解剖器（開源 MIT：https://github.com/tbpfs/formosa-svg-xray）\n"
        "- [YouTube 完整教學播放清單](https://www.youtube.com/playlist?list=PLhxdaTcUMi3nRM5mtOdQgO4VEtAEsTiYd)\n"
        f"- [紫楓程式與 AI 學習發問社團（Facebook）]({FB_GROUP_URL})\n"
        "- 官方社群矩陣：X (https://x.com/tbpfs1)｜YouTube (https://www.youtube.com/@PurpleMapleAI)｜YouTube Music (https://music.youtube.com/channel/UCcEBgbHV3rcee1FfgfHXprw)｜Spotify (https://open.spotify.com/artist/7D7CLJoxLhsMos8xI9H2kx)｜Apple Music (https://music.apple.com/tw/artist/purple-maple/1745241062)｜Pixiv (https://www.pixiv.net/users/3503246)｜Facebook 紫楓 (https://www.facebook.com/tbpfs2/)｜Facebook 艾莉 (https://www.facebook.com/AilyAIAI/)｜TikTok (https://www.tiktok.com/@ai_purple_maple)｜LinkedIn (https://www.linkedin.com/in/tbpfs2/)\n"
    )
    (out_dir / "llms.txt").write_text(
        "# 紫楓出版社 (Purple Maple Press) — AI 工程與 Python 3.12 資料結構演算法技術專書\n\n"
        f"> 紫楓（AI王紫楓 / Purple Maple / @tbpfs1）創辦之免費開源技術專書出版平台（`{SITE_BASE_URL}/`），提供繁體中文（`/learn/`）、簡體中文（`/learn/zh-cn/`）與英文（`/learn/en/`）三語 {total_pages} 頁完整專書與講義，收錄《AI 工程師實戰聖經》與《Python 3.12 資料結構與演算法精解》（{chapter_titles_short_tw}）。\n"
        f"> - **三語入口**：[繁體中文]({SITE_BASE_URL}/) ｜ [简体中文]({SITE_BASE_URL}/zh-cn/) ｜ [English]({SITE_BASE_URL}/en/)\n"
        f"> - **本站完整程式碼與輸出語料（Full Tutorial Corpus）**：{SITE_BASE_URL}/llms-full.txt\n"
        "> - **創作者與品牌完整知識庫（Brand Full Corpus）**：https://ai-purplemaple.com/llms-full.txt\n\n"
        "## 章節列表 — 繁體中文 (Chapters, zh-Hant)\n"
        + "\n".join(llms_chapter_lines)
        + "\n\n## 章节列表 — 简体中文 (Chapters, zh-Hans)\n"
        + "\n".join(llms_zh_cn_lines)
        + "\n\n## Chapters — English (en)\n"
        + "\n".join(llms_en_lines)
        + "\n\n"
        + ecosystem_footer_md,
        encoding="utf-8",
    )
    (out_dir / "llms-full.txt").write_text(
        "# 紫楓出版社 (Purple Maple Press) — AI 工程與 Python 3.12 完整教學語料庫 (llms-full.txt)\n\n"
        f"> 本文件收錄 `{SITE_BASE_URL}/` 紫楓出版社全站已上線專書章節與 {len(CHAPTERS)} 篇 Python 資料結構演算法講義（{chapter_titles_short_tw}）之核心觀念、架構解析、完整 Python 3.12 標準庫實作原始碼及 CI 實機執行驗證輸出。亦同步提供簡體中文版（`{SITE_BASE_URL}/zh-cn/`）與英文版（`{SITE_BASE_URL}/en/`）；精簡索引請見 `{SITE_BASE_URL}/llms.txt`。\n\n"
        + "\n\n---\n\n".join(llms_full_sections)
        + "\n\n---\n\n"
        + ecosystem_footer_md,
        encoding="utf-8",
    )

    return index_path


_ROOT_OWNED_SKIP = {"CNAME", "robots.txt", "ads.txt", ".nojekyll", f"{INDEXNOW_KEY}.txt"}


def sync_to_portfolio(src_site_dir: Path, dst_learn_dir: Path) -> int:
    """Mirror built _site into ai-purplemaple.com/learn/, excluding root-owned host files."""
    if dst_learn_dir.exists():
        shutil.rmtree(dst_learn_dir)
    dst_learn_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    for item in src_site_dir.rglob("*"):
        rel = item.relative_to(src_site_dir)
        if len(rel.parts) == 1 and rel.name in _ROOT_OWNED_SKIP:
            continue
        target = dst_learn_dir / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            copied += 1
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description="Build static site for Purple Maple Press (/learn/).")
    parser.add_argument("-o", "--output", default="_site", help="Output directory (default: _site)")
    parser.add_argument(
        "--sync-portfolio",
        default="",
        help="Optional target directory (e.g. ../antigravity-portfolio_site/learn) to mirror built pages",
    )
    args = parser.parse_args()
    out_dir = Path(args.output)
    out_path = build_site(out_dir)
    sitemap_text = (out_dir / "sitemap.xml").read_text(encoding="utf-8")
    page_count = sitemap_text.count("<loc>")
    print(f"[OK] Built {page_count}-page trilingual Purple Maple Press site at: {out_path}")
    if args.sync_portfolio:
        dst = Path(args.sync_portfolio).resolve()
        n_files = sync_to_portfolio(out_dir, dst)
        print(f"[OK] Synced {n_files} files into portfolio /learn/ directory: {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
