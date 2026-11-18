#!/usr/bin/env python3
"""
Ch.07 堆積、優先佇列與 Top-K 演算法（Heap, Priority Queue & Top-K Elements）
展示手寫最小二元堆積（MinHeap）上浮/下沉封裝、Top-K 最大元素篩選與合併 K 個已排序串列。
"""

from __future__ import annotations

import heapq
from typing import Any, Generic, Iterable, Sequence, TypeVar

T = TypeVar("T", bound=Any)


class MinHeap(Generic[T]):
    """以陣列封裝之完全二元樹最小堆積（Binary Min-Heap），支援 O(log n) 插入與彈出最小值。"""

    def __init__(self, items: Iterable[T] | None = None) -> None:
        self._data: list[T] = []
        if items is not None:
            for item in items:
                self.push(item)

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def peek(self) -> T:
        """查看堆頂最小元素，時間複雜度 O(1)。"""
        if not self._data:
            raise IndexError("peek from empty MinHeap")
        return self._data[0]

    def push(self, val: T) -> None:
        """插入新元素並執行上浮（Sift-Up），時間複雜度 O(log n)。"""
        self._data.append(val)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> T:
        """彈出堆頂最小元素並將末尾元素移至堆頂執行下沉（Sift-Down），時間複雜度 O(log n)。"""
        if not self._data:
            raise IndexError("pop from empty MinHeap")
        top = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return top

    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            if self._data[idx] < self._data[parent]:
                self._data[idx], self._data[parent] = self._data[parent], self._data[idx]
                idx = parent
            else:
                break

    def _sift_down(self, idx: int) -> None:
        n = len(self._data)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            if left < n and self._data[left] < self._data[smallest]:
                smallest = left
            if right < n and self._data[right] < self._data[smallest]:
                smallest = right
            if smallest == idx:
                break
            self._data[idx], self._data[smallest] = self._data[smallest], self._data[idx]
            idx = smallest


def top_k_largest(nums: Sequence[int], k: int) -> list[int]:
    """
    利用容量固定為 k 的最小堆積，在 O(n log k) 時間與 O(k) 空間內找出前 k 大元素（由大到小回傳）。
    """
    if k <= 0 or not nums:
        return []
    min_heap: list[int] = []
    for num in nums:
        if len(min_heap) < k:
            heapq.heappush(min_heap, num)
        elif num > min_heap[0]:
            heapq.heapreplace(min_heap, num)
    return sorted(min_heap, reverse=True)


def merge_k_sorted_lists(lists: Sequence[Sequence[int]]) -> list[int]:
    """
    利用優先佇列（Min-Heap 儲存 (元素值, 串列索引, 元素索引)）合併 K 個已排序序列：
    時間複雜度 O(N log K)，空間複雜度 O(K)（不含輸出串列）。
    """
    min_heap: list[tuple[int, int, int]] = []
    for list_idx, seq in enumerate(lists):
        if seq:
            heapq.heappush(min_heap, (seq[0], list_idx, 0))

    merged: list[int] = []
    while min_heap:
        val, list_idx, elem_idx = heapq.heappop(min_heap)
        merged.append(val)
        next_idx = elem_idx + 1
        if next_idx < len(lists[list_idx]):
            heapq.heappush(min_heap, (lists[list_idx][next_idx], list_idx, next_idx))
    return merged


if __name__ == "__main__":
    heap = MinHeap([5, 1, 8, 3])
    popped = [heap.pop() for _ in range(len(heap))]
    top3 = top_k_largest([64, 34, 25, 12, 22, 11, 90, -5], 3)
    merged_k = merge_k_sorted_lists([[1, 4, 5], [1, 3, 4], [2, 6]])
    print(f"Ch.07 MinHeap 依序彈出: {popped} | Top-3 最大元素: {top3} | 合併 K 串列: {merged_k}")
