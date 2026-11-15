#!/usr/bin/env python3
"""
Ch.04 雜湊表與二元搜尋樹（Hash Table & Binary Search Tree）
展示鏈結法雜湊表（Chaining Hash Table）、LeetCode #1 Two Sum O(n) 解法與二元搜尋樹中序走訪（In-order Traversal）。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class ChainingHashTable(Generic[K, V]):
    """以鏈結法（Separate Chaining）處理雜湊碰撞的雜湊表實作，平均讀寫複雜度 O(1)。"""

    def __init__(self, bucket_count: int = 8) -> None:
        if bucket_count <= 0:
            raise ValueError("bucket_count 必須為正整數")
        self._buckets: list[list[tuple[K, V]]] = [[] for _ in range(bucket_count)]
        self._size = 0

    def _bucket_index(self, key: K) -> int:
        return hash(key) % len(self._buckets)

    def put(self, key: K, value: V) -> None:
        bucket = self._buckets[self._bucket_index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1

    def get(self, key: K, default: V | None = None) -> V | None:
        bucket = self._buckets[self._bucket_index(key)]
        for existing_key, existing_val in bucket:
            if existing_key == key:
                return existing_val
        return default

    def remove(self, key: K) -> bool:
        bucket = self._buckets[self._bucket_index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def __len__(self) -> int:
        return self._size


def two_sum(nums: Sequence[int], target: int) -> tuple[int, int] | None:
    """經典面試題 Two Sum：利用雜湊表在 O(n) 時間內找出兩數之和等於 target 的索引配對。"""
    seen: dict[int, int] = {}
    for idx, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return (seen[complement], idx)
        seen[num] = idx
    return None


@dataclass
class BSTNode:
    val: int
    left: BSTNode | None = None
    right: BSTNode | None = None


class BinarySearchTree:
    """二元搜尋樹（BST）：左子樹所有鍵值 < 根節點 < 右子樹所有鍵值，中序走訪必為遞增排序序列。"""

    def __init__(self, values: Sequence[int] | None = None) -> None:
        self.root: BSTNode | None = None
        if values:
            for val in values:
                self.insert(val)

    def insert(self, val: int) -> None:
        if self.root is None:
            self.root = BSTNode(val)
            return
        curr = self.root
        while True:
            if val == curr.val:
                return
            if val < curr.val:
                if curr.left is None:
                    curr.left = BSTNode(val)
                    return
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = BSTNode(val)
                    return
                curr = curr.right

    def contains(self, target: int) -> bool:
        curr = self.root
        while curr is not None:
            if target == curr.val:
                return True
            curr = curr.left if target < curr.val else curr.right
        return False

    def inorder(self) -> list[int]:
        result: list[int] = []

        def _traverse(node: BSTNode | None) -> None:
            if node is None:
                return
            _traverse(node.left)
            result.append(node.val)
            _traverse(node.right)

        _traverse(self.root)
        return result


if __name__ == "__main__":
    pair = two_sum([2, 7, 11, 15], 9)
    bst = BinarySearchTree([50, 30, 70, 20, 40, 60, 80])
    print("Ch.04 Two Sum 索引:", pair, "| BST 中序走訪:", bst.inorder(), "| 搜尋 60:", bst.contains(60))
