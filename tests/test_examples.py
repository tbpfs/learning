#!/usr/bin/env python3
"""Unit tests for learning repository examples (Ch.01 - Ch.07), SEO/GEO invariants, and README links."""

import json
import re
import sys
import tempfile
import unittest
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
        from build_site import CHAPTERS, build_site

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
            self.assertEqual(html_text.count('class="ad-slot-card"'), len(CHAPTERS))
            self.assertEqual(html_text.count('data-ad-slot="1673180799"'), len(CHAPTERS))
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
                self.assertEqual(ch_html.count('data-ad-slot="1673180799"'), 2)

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
            self.assertIn("https://learn.ai-purplemaple.com/llms-full.txt", sitemap_text)
            self.assertIn("<lastmod>2026-11-18</lastmod>", sitemap_text)

            robots_text = (Path(tmpdir) / "robots.txt").read_text(encoding="utf-8")
            for bot in ("Twitterbot", "GrokBot", "xAI-Bot", "xAI-SearchBot", "Bravebot"):
                self.assertIn(f"User-agent: {bot}", robots_text)

            self.assertIn('name="twitter:creator" content="@tbpfs1"', html_text)
            self.assertIn('name="twitter:image" content="https://ai-purplemaple.com/assets/gallery/aily_03.jpg"', html_text)
            ch07_html = (Path(tmpdir) / "ch07.html").read_text(encoding="utf-8")
            self.assertIn('name="twitter:title" content="Ch.07 ', ch07_html)
            self.assertIn('name="twitter:description" content="紫楓（AI王紫楓 / Purple Maple）Python 3.12 教學講義：Ch.07 ', ch07_html)


if __name__ == "__main__":
    unittest.main()
