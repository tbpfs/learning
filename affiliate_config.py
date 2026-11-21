#!/usr/bin/env python3
"""
Centralized hot-swappable affiliate link configuration for learn.ai-purplemaple.com.
Supports live Books.com.tw AP (`tbpfs1`) and environment-variable overrides for
Taiwan / global affiliate networks (Affiliates.One, iChannels, Hahow, Udemy, Kobo).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import quote_plus

BOOKS_AP_ID = os.environ.get("PM_BOOKS_AP_ID", "tbpfs1").strip() or "tbpfs1"
BOOKS_AP_CAMPAIGN = os.environ.get("PM_BOOKS_AP_CAMPAIGN", "ap-202611").strip() or "ap-202611"


def build_books_ap_search_url(keyword: str) -> str:
    """Build a zero-404 Books.com.tw AP (博客來策略聯盟) search redirect URL."""
    encoded = quote_plus(keyword.strip())
    return (
        f"https://www.books.com.tw/exep/assp.php/{BOOKS_AP_ID}/"
        f"exep/prod_search.php?key={encoded}&cat=all"
        f"&utm_source={BOOKS_AP_ID}&utm_medium=ap-books"
        f"&utm_content=recommend&utm_campaign={BOOKS_AP_CAMPAIGN}"
    )


def build_books_ap_product_url(product_id: str) -> str:
    """Build a direct Books.com.tw AP product URL for a specific item ID."""
    pid = product_id.strip()
    return (
        f"https://www.books.com.tw/exep/assp.php/{BOOKS_AP_ID}/products/{pid}"
        f"?utm_source={BOOKS_AP_ID}&utm_medium=ap-books"
        f"&utm_content=recommend&utm_campaign={BOOKS_AP_CAMPAIGN}"
    )


@dataclass(frozen=True)
class AffiliateResource:
    partner_id: str
    title: str
    partner_label: str
    audience: str
    highlight: str
    url: str
    cta_label: str
    is_sponsored: bool = True


def get_learning_resources() -> tuple[AffiliateResource, ...]:
    """Return centralized book & course recommendations (hot-swappable via env vars)."""
    hahow_url = os.environ.get(
        "PM_AFFILIATE_HAHOW_URL",
        "https://hahow.in/courses?q=Python+%E8%B3%87%E6%96%99%E7%B5%90%E6%A7%8B",
    ).strip()
    hahow_sponsored = bool(os.environ.get("PM_AFFILIATE_HAHOW_URL", "").strip())

    return (
        AffiliateResource(
            partner_id="books_grokking_algo",
            title="圖解演算法（Grokking Algorithms 中文版）",
            partner_label="博客來 Books.com.tw",
            audience="零基礎入門／轉職視覺化學習",
            highlight="全彩圖解二分搜尋、雜湊表、BFS/DFS 與動態規劃，對應 Ch.01–Ch.06 核心觀念",
            url=build_books_ap_search_url("圖解演算法 Python"),
            cta_label="前往博客來查詢 ↗",
            is_sponsored=True,
        ),
        AffiliateResource(
            partner_id="books_fluent_python",
            title="流暢的 Python（Fluent Python 第二版）",
            partner_label="博客來 Books.com.tw",
            audience="中階工程師／CPython 底層調校",
            highlight="深入拆解 list/dict 記憶體配置、生成器與物件模型，完美銜接各章 CPython 陷阱",
            url=build_books_ap_search_url("流暢的 Python"),
            cta_label="前往博客來查詢 ↗",
            is_sponsored=True,
        ),
        AffiliateResource(
            partner_id="books_dsa_interview",
            title="演算法與資料結構面試實戰（Python 刷題指南）",
            partner_label="博客來 Books.com.tw",
            audience="技術面試／LeetCode 白板題衝刺",
            highlight="針對 Top-K、0/1 背包、雙指標與樹圖遍歷提供系統化解題模板，對應 Ch.04–Ch.07",
            url=build_books_ap_search_url("資料結構 演算法 Python 面試"),
            cta_label="前往博客來查詢 ↗",
            is_sponsored=True,
        ),
        AffiliateResource(
            partner_id="hahow_python_dsa",
            title="Hahow 好學校：Python 程式設計與演算法影音課程",
            partner_label="Hahow 好學校",
            audience="偏好中文影音互動與作業批改者",
            highlight="搭配本站免費 7 章 Python 3.12 原始碼與 YouTube 鐵人賽影片雙軌強化實作力",
            url=hahow_url,
            cta_label="探索相關課程 ↗",
            is_sponsored=hahow_sponsored,
        ),
    )


CHAPTER_BOOK_KEYWORDS: dict[str, tuple[str, str]] = {
    "ch01": ("資料結構 Python 陣列 鏈結串列", "延伸書單：Python 資料結構與記憶體模型精選（博客來）"),
    "ch02": ("資料結構 Python 堆疊 佇列", "延伸書單：Stack／Queue 與資料結構實作精選（博客來）"),
    "ch03": ("圖解演算法 排序 搜尋 Python", "延伸書單：圖解演算法與搜尋排序經典（博客來）"),
    "ch04": ("演算法 雜湊 二元樹 Python", "延伸書單：雜湊表與樹狀結構面試精選（博客來）"),
    "ch05": ("圖論 演算法 物件導向 Python", "延伸書單：圖論演算法與 Python OOP 實戰（博客來）"),
    "ch06": ("動態規劃 演算法 LeetCode Python", "延伸書單：動態規劃與演算法面試刷題指南（博客來）"),
    "ch07": ("演算法 資料結構 堆積 Python", "延伸書單：Heap 優先佇列與系統設計進階書單（博客來）"),
}


def get_chapter_book_recommendation(chapter_id: str) -> tuple[str, str]:
    """Return (label, Books.com.tw AP URL) for a chapter's contextual reading card."""
    keyword, label = CHAPTER_BOOK_KEYWORDS.get(
        chapter_id,
        ("Python 資料結構 演算法", "延伸書單：Python 資料結構與演算法精選（博客來）"),
    )
    return label, build_books_ap_search_url(keyword)
