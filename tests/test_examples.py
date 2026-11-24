#!/usr/bin/env python3
"""Unit tests for learning repository examples (Ch.01 - Ch.07), SEO/GEO invariants, and README links."""

import json
import re
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "examples"))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ch01_array_linked_list import SinglyLinkedList  # noqa: E402
from ch02_stack_queue import Queue, Stack, is_balanced_brackets  # noqa: E402
from ch03_search_sort import binary_search, merge_sort  # noqa: E402
from ch04_hash_bst import BinarySearchTree, ChainingHashTable, two_sum  # noqa: E402
from ch05_graph_oop import Graph  # noqa: E402
from ch06_dynamic_programming import climb_stairs_dp, knapsack_01, length_of_lis  # noqa: E402
from ch07_heap_priority_queue import MinHeap, merge_k_sorted_lists, top_k_largest  # noqa: E402


class TestLearningExamples(unittest.TestCase):
    def test_readme_youtube_playlist_link_starts_at_beginning(self):
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("PLhxdaTcUMi3nRM5mtOdQgO4VEtAEsTiYd", readme)
        self.assertNotIn("index=2", readme)
        self.assertNotIn("&t=1s", readme)
        self.assertIn("ch06_dynamic_programming.py", readme)
        self.assertIn("ch07_heap_priority_queue.py", readme)

    def test_singly_linked_list_operations(self):
        sll = SinglyLinkedList([1, 2, 3])
        self.assertEqual(len(sll), 3)
        sll.prepend(0)
        self.assertEqual(sll.to_list(), [0, 1, 2, 3])
        self.assertEqual(sll.find(2), 2)
        self.assertEqual(sll.find(99), -1)

        self.assertTrue(sll.remove(2))
        self.assertFalse(sll.remove(99))
        self.assertEqual(sll.to_list(), [0, 1, 3])

        sll.reverse()
        self.assertEqual(sll.to_list(), [3, 1, 0])

    def test_stack_and_queue_and_brackets(self):
        stack: Stack[int] = Stack()
        self.assertTrue(stack.is_empty())
        stack.push(10)
        stack.push(20)
        self.assertEqual(stack.peek(), 20)
        self.assertEqual(stack.pop(), 20)
        self.assertEqual(stack.pop(), 10)
        with self.assertRaises(IndexError):
            stack.pop()

        queue: Queue[str] = Queue()
        queue.enqueue("a")
        queue.enqueue("b")
        self.assertEqual(queue.peek(), "a")
        self.assertEqual(queue.dequeue(), "a")
        self.assertEqual(queue.dequeue(), "b")
        with self.assertRaises(IndexError):
            queue.dequeue()

        self.assertTrue(is_balanced_brackets("([{}])"))
        self.assertTrue(is_balanced_brackets(""))
        self.assertFalse(is_balanced_brackets("([)]"))
        self.assertFalse(is_balanced_brackets("((("))

    def test_binary_search_and_merge_sort(self):
        unsorted = [64, 34, 25, 12, 22, 11, 90, -5, 25]
        sorted_arr = merge_sort(unsorted)
        self.assertEqual(sorted_arr, sorted(unsorted))
        self.assertEqual(merge_sort([]), [])
        self.assertEqual(merge_sort([42]), [42])

        self.assertEqual(binary_search(sorted_arr, -5), 0)
        self.assertEqual(binary_search(sorted_arr, 90), len(sorted_arr) - 1)
        self.assertEqual(binary_search(sorted_arr, 100), -1)

    def test_hash_table_two_sum_and_bst(self):
        ht: ChainingHashTable[str, int] = ChainingHashTable(bucket_count=4)
        ht.put("aily", 1)
        ht.put("maple", 2)
        ht.put("aily", 99)
        self.assertEqual(len(ht), 2)
        self.assertEqual(ht.get("aily"), 99)
        self.assertIsNone(ht.get("missing"))
        self.assertTrue(ht.remove("maple"))
        self.assertFalse(ht.remove("maple"))
        self.assertEqual(len(ht), 1)

        self.assertEqual(two_sum([2, 7, 11, 15], 9), (0, 1))
        self.assertIsNone(two_sum([1, 2, 3], 100))

        bst = BinarySearchTree([50, 30, 70, 20, 40, 60, 80, 30])
        self.assertEqual(bst.inorder(), [20, 30, 40, 50, 60, 70, 80])
        self.assertTrue(bst.contains(60))
        self.assertFalse(bst.contains(99))

    def test_graph_bfs_dfs_and_shortest_path(self):
        g: Graph[str] = Graph()
        for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "E"), ("D", "F"), ("E", "F")]:
            g.add_edge(u, v)
        self.assertEqual(g.bfs("A"), ["A", "B", "C", "D", "E", "F"])
        self.assertEqual(g.dfs("A"), ["A", "B", "D", "F", "E", "C"])
        self.assertEqual(g.shortest_path_bfs("A", "F"), ["A", "B", "D", "F"])
        self.assertIsNone(g.shortest_path_bfs("A", "Z"))

    def test_dynamic_programming_ch06(self):
        self.assertEqual(climb_stairs_dp(0), 1)
        self.assertEqual(climb_stairs_dp(1), 1)
        self.assertEqual(climb_stairs_dp(10), 89)
        with self.assertRaises(ValueError):
            climb_stairs_dp(-1)

        self.assertEqual(knapsack_01([10, 20, 30], [60, 100, 120], 50), 220)
        self.assertEqual(knapsack_01([10, 20], [60, 100], 0), 0)
        with self.assertRaises(ValueError):
            knapsack_01([10], [60], -5)

        self.assertEqual(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]), 4)
        self.assertEqual(length_of_lis([]), 0)
        self.assertEqual(length_of_lis([7, 7, 7, 7]), 1)

    def test_heap_priority_queue_ch07(self):
        heap: MinHeap[int] = MinHeap([5, 1, 8, 3, 2])
        self.assertEqual(len(heap), 5)
        self.assertFalse(heap.is_empty())
        self.assertEqual(heap.peek(), 1)
        popped = [heap.pop() for _ in range(len(heap))]
        self.assertEqual(popped, [1, 2, 3, 5, 8])
        self.assertTrue(heap.is_empty())
        with self.assertRaises(IndexError):
            heap.pop()
        with self.assertRaises(IndexError):
            heap.peek()

        self.assertEqual(top_k_largest([64, 34, 25, 12, 22, 11, 90], 3), [90, 64, 34])
        self.assertEqual(top_k_largest([], 3), [])
        self.assertEqual(top_k_largest([1, 2], 0), [])

        self.assertEqual(
            merge_k_sorted_lists([[1, 4, 5], [1, 3, 4], [2, 6], []]),
            [1, 1, 2, 3, 4, 4, 5, 6],
        )
        self.assertEqual(merge_k_sorted_lists([]), [])

    def test_build_site_generates_valid_html(self):
        from build_site import CHAPTERS, ENABLE_MANUAL_AD_SLOTS, SITE_LASTMOD, build_site

        with tempfile.TemporaryDirectory() as tmpdir:
            index_path = build_site(Path(tmpdir))
            self.assertTrue(index_path.is_file())
            self.assertTrue((Path(tmpdir) / ".nojekyll").is_file())
            ads_txt = (Path(tmpdir) / "ads.txt").read_text(encoding="utf-8").strip()
            self.assertEqual(
                ads_txt,
                "google.com, pub-6485917848711473, DIRECT, f08c47fec0942fa0",
            )
            html_text = index_path.read_text(encoding="utf-8")
            self.assertIn("<!DOCTYPE html>", html_text)
            self.assertIn("從零開始寫程式，輕鬆搞懂資料結構，演算法", html_text)
            self.assertNotIn('id="fbBox"', html_text)
            self.assertIn("anonymous" if False else "私密提問", html_text)
            for marker in (
                "Ch.01 SinglyLinkedList 範例結果:",
                "Ch.02 括號平衡檢查",
                "Ch.03 Merge Sort 結果:",
                "Ch.04 Two Sum 索引:",
                "Ch.05 BFS 走訪:",
                "Ch.06 DP 爬樓梯(n=10): 89",
                "Ch.07 MinHeap 依序彈出: [1, 3, 5, 8]",
            ):
                self.assertIn(marker, html_text)

            self.assertIn("ca-pub-6485917848711473", html_text)
            self.assertIn("G-B24GXZ32MW", html_text)
            self.assertIn("GTM-WNSFQT5V", html_text)
            expected_idx_ads = len(CHAPTERS) if ENABLE_MANUAL_AD_SLOTS else 0
            self.assertEqual(html_text.count('class="ad-slot-card"'), expected_idx_ads)
            self.assertEqual(html_text.count('data-ad-slot="1673180799"'), expected_idx_ads)
            self.assertEqual(html_text.count('<details class="code-accordion"'), len(CHAPTERS))
            self.assertEqual(html_text.count('<details class="code-accordion" open>'), 1)
            self.assertEqual(html_text.count('<details class="deep-dive-callout">'), len(CHAPTERS))
            self.assertIn('<details class="study-guide-accordion">', html_text)
            self.assertIn("Privacy Policy", html_text)

            # Validate index.html JSON-LD syntax
            idx_ld_match = re.search(
                r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
                html_text,
                re.DOTALL,
            )
            self.assertIsNotNone(idx_ld_match)
            idx_ld = json.loads(idx_ld_match.group(1))
            self.assertEqual(idx_ld["@type"], "Course")
            self.assertEqual(len(idx_ld["hasPart"]), 7)
            self.assertEqual(idx_ld["speakable"]["@type"], "SpeakableSpecification")
            self.assertIn('class="aeo-capsule"', html_text)
            self.assertIn(':has(ins[data-ad-status="unfilled"])', html_text)
            self.assertIn("https://blog.ai-purplemaple.com/", html_text)
            self.assertIn("https://www.youtube.com/@PurpleMapleAI", html_text)
            self.assertIn("折疊面板", html_text)
            for forbidden_tok in ("核心速答：", "本章速答", "grok_note", "chapter-badge", "折疊面版", "@purplemaple_tb", "tbpfs1.blogspot.com"):
                self.assertNotIn(forbidden_tok, html_text, f"index.html leaked forbidden string: {forbidden_tok}")
            self.assertIn("https://www.books.com.tw/exep/assp.php/tbpfs1/", html_text)
            self.assertIn('rel="sponsored noopener noreferrer"', html_text)
            self.assertIn("affiliate_click", html_text)

            for ch_id in ("ch01", "ch02", "ch03", "ch04", "ch05", "ch06", "ch07"):
                ch_file = Path(tmpdir) / f"{ch_id}.html"
                self.assertTrue(ch_file.is_file(), f"Missing standalone chapter page {ch_id}.html")
                ch_html = ch_file.read_text(encoding="utf-8")
                self.assertIn(f"https://learn.ai-purplemaple.com/{ch_id}.html", ch_html)
                self.assertIn(f"教學講義：Ch.0{ch_id[-1]}", ch_html)
                self.assertNotIn('type="text/markdown"', ch_html)
                self.assertNotIn('rel="llms-txt"', ch_html)
                self.assertNotIn('href="index.html"', ch_html)
                self.assertIn('href="/"', ch_html)

                # Verify de-duplication & RWD comparison table on standalone pages
                self.assertNotIn('id="study-guide"', ch_html)
                self.assertNotIn('id="cms-tutorials-container"', ch_html)
                self.assertNotIn('href="#ch02"', ch_html)
                self.assertIn('class="table-responsive"', ch_html)
                self.assertIn('<table class="comparison-table">', ch_html)
                expected_ch_ads = 2 if ENABLE_MANUAL_AD_SLOTS else 0
                self.assertEqual(ch_html.count('data-ad-slot="1673180799"'), expected_ch_ads)
                self.assertIn("ca-pub-6485917848711473", ch_html)
                for fb_tok in (
                    f'data-chapter="{ch_id}"',
                    'id="fbBox"',
                    'aria-pressed="false"',
                    'class="fb-ask"',
                    'id="askForm"',
                    'https://ai-purplemaple.com',
                    '/api/v1/learn-feedback',
                    '/api/v1/learn-question',
                ):
                    self.assertIn(fb_tok, ch_html, f"Missing {fb_tok} in {ch_id}.html")

                class _DomCount(HTMLParser):
                    def __init__(self):
                        super().__init__()
                        self.n = 0
                    def handle_starttag(self, tag, attrs):
                        self.n += 1
                _dc = _DomCount()
                _dc.feed(ch_html)
                self.assertLess(_dc.n, 1500, f"{ch_id}.html DOM element count {_dc.n} >= 1500")

                # Verify pure Chinese prose count >= 1,200 chars (excluding style, script, pre)
                stripped = re.sub(r"<style\b[^>]*>.*?</style>", "", ch_html, flags=re.DOTALL)
                stripped = re.sub(r"<script\b[^>]*>.*?</script>", "", stripped, flags=re.DOTALL)
                stripped = re.sub(r"<pre\b[^>]*>.*?</pre>", "", stripped, flags=re.DOTALL)
                stripped = re.sub(r"<[^>]+>", "", stripped)
                cjk_chars = re.findall(r"[\u4e00-\u9fff]", stripped)
                self.assertGreaterEqual(
                    len(cjk_chars),
                    1200,
                    f"{ch_id}.html prose Chinese char count ({len(cjk_chars)}) is below 1200 threshold!",
                )

                # Verify per-chapter JSON-LD @graph (TechArticle + VideoObject + FAQPage + BreadcrumbList)
                ch_ld_match = re.search(
                    r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
                    ch_html,
                    re.DOTALL,
                )
                self.assertIsNotNone(ch_ld_match, f"Missing JSON-LD in {ch_id}.html")
                ch_ld = json.loads(ch_ld_match.group(1))
                self.assertIn("@graph", ch_ld)
                graph_types = {node["@type"]: node for node in ch_ld["@graph"]}
                self.assertIn("TechArticle", graph_types)
                self.assertIn("VideoObject", graph_types)
                self.assertIn("FAQPage", graph_types)
                self.assertIn("BreadcrumbList", graph_types)
                self.assertIn("headline", graph_types["TechArticle"])
                self.assertIn("author", graph_types["TechArticle"])
                self.assertIn("dateModified", graph_types["TechArticle"])
                self.assertEqual(graph_types["TechArticle"]["speakable"]["@type"], "SpeakableSpecification")
                self.assertIn('class="aeo-capsule"', ch_html)
                self.assertIn("https://www.books.com.tw/exep/assp.php/tbpfs1/", ch_html)
                self.assertIn('rel="sponsored noopener noreferrer"', ch_html)
                self.assertIn("embedUrl", graph_types["VideoObject"])
                self.assertIn("https://www.youtube.com/embed/", ch_html)
                self.assertGreaterEqual(len(graph_types["FAQPage"]["mainEntity"]), 3)

            # Root GEO links, JSON-LD, llms.txt, llms-full.txt, and IndexNow key
            self.assertIn('rel="alternate" type="text/markdown" href="https://learn.ai-purplemaple.com/llms.txt"', html_text)
            self.assertIn('rel="alternate" type="text/markdown" href="https://learn.ai-purplemaple.com/llms-full.txt"', html_text)
            self.assertNotIn('rel="llms-txt"', html_text)
            self.assertIn("https://ai-purplemaple.com/#website", html_text)
            self.assertIn("Ch.07 堆積、優先佇列與 Top-K 演算法", html_text)

            key_text = (Path(tmpdir) / "7f4e9c2a8b1d6035e4a92c7f1b8d3e60.txt").read_text(encoding="utf-8").strip()
            self.assertEqual(key_text, "7f4e9c2a8b1d6035e4a92c7f1b8d3e60")

            llms_txt = (Path(tmpdir) / "llms.txt").read_text(encoding="utf-8")
            self.assertIn("https://learn.ai-purplemaple.com/llms-full.txt", llms_txt)
            self.assertIn("https://ai-purplemaple.com/llms-full.txt", llms_txt)
            self.assertIn("https://learn.ai-purplemaple.com/ch06.html", llms_txt)
            self.assertIn("https://learn.ai-purplemaple.com/ch07.html", llms_txt)
            self.assertNotIn("肉球おみくじ", llms_txt)
            self.assertNotIn("64 位繆思", llms_txt)
            self.assertIn("Meta Muse 邀請碼分享站", llms_txt)

            llms_full = (Path(tmpdir) / "llms-full.txt").read_text(encoding="utf-8")
            for marker in (
                "Ch.01 SinglyLinkedList 範例結果:",
                "Ch.02 括號平衡檢查",
                "Ch.03 Merge Sort 結果:",
                "Ch.04 Two Sum 索引:",
                "Ch.05 BFS 走訪:",
                "Ch.06 DP 爬樓梯(n=10): 89",
                "Ch.07 MinHeap 依序彈出: [1, 3, 5, 8]",
            ):
                self.assertIn(marker, llms_full)

            sitemap_text = (Path(tmpdir) / "sitemap.xml").read_text(encoding="utf-8")
            self.assertIn("https://learn.ai-purplemaple.com/ch01.html", sitemap_text)
            self.assertIn("https://learn.ai-purplemaple.com/ch05.html", sitemap_text)
            self.assertIn("https://learn.ai-purplemaple.com/ch06.html", sitemap_text)
            self.assertIn("https://learn.ai-purplemaple.com/ch07.html", sitemap_text)
            self.assertNotIn("https://learn.ai-purplemaple.com/llms-full.txt", sitemap_text)
            self.assertNotIn("https://learn.ai-purplemaple.com/llms.txt", sitemap_text)
            self.assertIn(f"<lastmod>{SITE_LASTMOD}</lastmod>", sitemap_text)

            robots_text = (Path(tmpdir) / "robots.txt").read_text(encoding="utf-8")
            for bot in ("Twitterbot", "GrokBot", "xAI-Bot", "xAI-SearchBot", "Bravebot"):
                self.assertIn(f"User-agent: {bot}", robots_text)

            self.assertIn('name="twitter:creator" content="@tbpfs1"', html_text)
            self.assertIn('name="twitter:image" content="https://ai-purplemaple.com/assets/gallery/aily_03.jpg"', html_text)
            ch07_html = (Path(tmpdir) / "ch07.html").read_text(encoding="utf-8")
            self.assertIn('name="twitter:title" content="Ch.07 ', ch07_html)
            self.assertIn('name="twitter:description" content="紫楓（AI王紫楓 / Purple Maple）Python 3.12 教學講義：Ch.07 ', ch07_html)
            self.assertIn('>王紫楓（紫楓 / Purple Maple）官方作品集（AI 音樂 ＆ 白瀬アイリ Aily）</a>', html_text)
            self.assertIn('>王紫楓（紫楓 / Purple Maple）</a>', html_text)
            self.assertIn('>王紫楓（紫楓 / Purple Maple）官方作品集</a>', ch07_html)
            self.assertIn('>王紫楓（紫楓 / Purple Maple）</a>', ch07_html)

    def test_trilingual_24_pages_hreflang_and_mechanical_qa(self):
        from build_site import build_site

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            build_site(root)

            # 1) Exact 24 canonical HTML URLs in sitemap.xml
            sitemap = (root / "sitemap.xml").read_text(encoding="utf-8")
            locs = re.findall(r"<loc>(.*?)</loc>", sitemap)
            self.assertEqual(len(locs), 24, f"Expected 24 URLs in sitemap.xml, got {len(locs)}")
            self.assertEqual(len(set(locs)), 24)

            ch_ids = ("ch01", "ch02", "ch03", "ch04", "ch05", "ch06", "ch07")
            zh_cn_banned_terms = (
                "陣列", "鏈結串列", "堆疊", "佇列", "雜湊表", "堆積", "演算法", "物件導向",
                "遞迴", "變數", "迴圈", "程式碼", "連結", "試算", "視窗", "資訊", "記憶體",
                "講義", "預設", "紫楓", "點擊展開", "實機執行", "隱私權", "總目錄", "鐵人賽",
                "博客來", "資料結構", "二元搜尋樹", "合併排序", "走訪", "範例", "括號",
            )
            zh_cn_banned_trad_chars = "楓網學實複雜資結構時間點製輸驗證隱權饋幫進選錯誤這還觀關長審閱補總錄鐵賽單書課較維護對蹤層題難試問碼導場義廣頁"

            class _DomCounter(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.n = 0

                def handle_starttag(self, tag, attrs):
                    self.n += 1

            # 2) Verify all 24 pages: All-to-All bidirectional hreflang, canonical, og:locale, DOM < 1500, /ads.txt
            for page_fn in (None, *(f"{cid}.html" for cid in ch_ids)):
                tw_url = f"https://learn.ai-purplemaple.com/{page_fn or ''}"
                cn_url = f"https://learn.ai-purplemaple.com/zh-cn/{page_fn or ''}"
                en_url = f"https://learn.ai-purplemaple.com/en/{page_fn or ''}"

                locale_specs = (
                    ("zh-TW", "zh-Hant", "zh_TW", root / (page_fn or "index.html"), tw_url),
                    ("zh-CN", "zh-Hans", "zh_CN", root / "zh-cn" / (page_fn or "index.html"), cn_url),
                    ("en", "en", "en_US", root / "en" / (page_fn or "index.html"), en_url),
                )
                for loc_code, hlang, og_loc, fpath, canon in locale_specs:
                    self.assertTrue(fpath.is_file(), f"Missing generated file {fpath}")
                    raw_html = fpath.read_text(encoding="utf-8")
                    self.assertIn(f'<html lang="{hlang}">', raw_html)
                    self.assertIn(f'<link rel="canonical" href="{canon}">', raw_html)
                    self.assertIn(f'<link rel="alternate" hreflang="zh-Hant" href="{tw_url}">', raw_html)
                    self.assertIn(f'<link rel="alternate" hreflang="zh-Hans" href="{cn_url}">', raw_html)
                    self.assertIn(f'<link rel="alternate" hreflang="en" href="{en_url}">', raw_html)
                    self.assertIn(f'<link rel="alternate" hreflang="x-default" href="{tw_url}">', raw_html)
                    self.assertIn(f'<meta property="og:locale" content="{og_loc}">', raw_html)
                    self.assertIn('href="/ads.txt"', raw_html)
                    self.assertNotIn('href="index.html"', raw_html)
                    self.assertIn("GTM-WNSFQT5V", raw_html)
                    self.assertIn("G-B24GXZ32MW", raw_html)
                    self.assertIn("ca-pub-6485917848711473", raw_html)

                    dc = _DomCounter()
                    dc.feed(raw_html)
                    self.assertLess(dc.n, 1500, f"{loc_code}/{page_fn or 'index.html'} DOM={dc.n} >= 1500")

                    # Strip ONLY the language switcher <nav> for full-document localization QA (includes <head>, JSON-LD, <script>, <pre>!)
                    no_switcher = re.sub(
                        r'<nav class="lang-switcher"[^>]*>.*?</nav>',
                        "",
                        raw_html,
                        flags=re.DOTALL,
                    )

                    if loc_code == "en":
                        cjk_leaks = re.findall(r"[\u4e00-\u9fff]", no_switcher)
                        self.assertEqual(
                            cjk_leaks,
                            [],
                            f"English page {fpath.name} leaked CJK chars: {cjk_leaks[:10]}",
                        )
                        self.assertNotIn("books.com.tw", raw_html)
                        self.assertNotIn("cms-tutorials-container", raw_html)
                        if page_fn is not None:
                            self.assertIn('href="/en/"', raw_html)
                            self.assertNotIn('rel="sponsored', raw_html)
                            prose = re.sub(r"<style\b[^>]*>.*?</style>", "", no_switcher, flags=re.DOTALL)
                            prose = re.sub(r"<script\b[^>]*>.*?</script>", "", prose, flags=re.DOTALL)
                            prose = re.sub(r"<pre\b[^>]*>.*?</pre>", "", prose, flags=re.DOTALL)
                            prose = re.sub(r"<[^>]+>", " ", prose)
                            en_words = re.findall(r"[A-Za-z][A-Za-z0-9'-]*", prose)
                            self.assertGreaterEqual(
                                len(en_words),
                                600,
                                f"en/{page_fn} prose word count {len(en_words)} < 600",
                            )
                            # Verify VideoObject inLanguage stays truthful ("zh-Hant") while TechArticle is "en"
                            ld_m = re.search(
                                r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>',
                                raw_html,
                                re.DOTALL,
                            )
                            self.assertIsNotNone(ld_m)
                            g_nodes = {n["@type"]: n for n in json.loads(ld_m.group(1))["@graph"]}
                            self.assertEqual(g_nodes["TechArticle"]["inLanguage"], "en")
                            self.assertEqual(g_nodes["VideoObject"]["inLanguage"], "zh-Hant")
                            self.assertEqual(g_nodes["TechArticle"]["isPartOf"]["@id"], "https://learn.ai-purplemaple.com/en/#course")

                    elif loc_code == "zh-CN":
                        self.assertNotIn("books.com.tw", raw_html)
                        self.assertNotIn("cms-tutorials-container", raw_html)
                        for bad_term in zh_cn_banned_terms:
                            self.assertNotIn(
                                bad_term,
                                no_switcher,
                                f"zh-cn/{page_fn or 'index.html'} leaked Taiwan term '{bad_term}'",
                            )
                        # Check prose + visible metadata + scripts for stray high-frequency Traditional chars
                        no_style = re.sub(r"<style\b[^>]*>.*?</style>", "", no_switcher, flags=re.DOTALL)
                        found_trad = sorted({ch for ch in no_style if ch in zh_cn_banned_trad_chars})
                        self.assertEqual(
                            found_trad,
                            [],
                            f"zh-cn/{page_fn or 'index.html'} leaked Traditional chars: {found_trad}",
                        )
                        if page_fn is not None:
                            self.assertIn('href="/zh-cn/"', raw_html)
                            self.assertNotIn('rel="sponsored', raw_html)
                            prose = re.sub(r"<style\b[^>]*>.*?</style>", "", no_switcher, flags=re.DOTALL)
                            prose = re.sub(r"<script\b[^>]*>.*?</script>", "", prose, flags=re.DOTALL)
                            prose = re.sub(r"<pre\b[^>]*>.*?</pre>", "", prose, flags=re.DOTALL)
                            prose = re.sub(r"<[^>]+>", "", prose)
                            cjk_cnt = len(re.findall(r"[\u4e00-\u9fff]", prose))
                            self.assertGreaterEqual(
                                cjk_cnt,
                                1200,
                                f"zh-cn/{page_fn} prose CJK char count {cjk_cnt} < 1200",
                            )

            # 3) Verify llms.txt references all 3 language editions
            llms_txt = (root / "llms.txt").read_text(encoding="utf-8")
            self.assertIn("https://learn.ai-purplemaple.com/zh-cn/", llms_txt)
            self.assertIn("https://learn.ai-purplemaple.com/en/", llms_txt)
            self.assertIn("https://learn.ai-purplemaple.com/zh-cn/ch07.html", llms_txt)
            self.assertIn("https://learn.ai-purplemaple.com/en/ch07.html", llms_txt)

            # 4) Verify .github/workflows/pages.yml IndexNow JSON payload is valid and covers all 24 HTML + 2 llms*.txt URLs
            wf_text = (REPO_ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
            m_json = re.search(r"-d\s*'(\{.*?\})'", wf_text, flags=re.DOTALL)
            self.assertIsNotNone(m_json, "IndexNow JSON payload missing in pages.yml")
            idx_payload = json.loads(m_json.group(1))
            self.assertEqual(len(idx_payload["urlList"]), 26)
            self.assertIn("https://learn.ai-purplemaple.com/zh-cn/", idx_payload["urlList"])
            self.assertIn("https://learn.ai-purplemaple.com/en/", idx_payload["urlList"])


if __name__ == "__main__":
    unittest.main()
