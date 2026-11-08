#!/usr/bin/env python3
"""Unit tests for learning repository examples (Ch.01 - Ch.03) and README link check."""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "examples"))

from ch01_array_linked_list import SinglyLinkedList  # noqa: E402
from ch02_stack_queue import Queue, Stack, is_balanced_brackets  # noqa: E402
from ch03_search_sort import binary_search, merge_sort  # noqa: E402


class TestLearningExamples(unittest.TestCase):
    def test_readme_youtube_playlist_link_starts_at_beginning(self):
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("PLhxdaTcUMi3nRM5mtOdQgO4VEtAEsTiYd", readme)
        self.assertNotIn("index=2", readme)
        self.assertNotIn("&t=1s", readme)

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


if __name__ == "__main__":
    unittest.main()
