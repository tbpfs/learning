#!/usr/bin/env python3
"""
Ch.07 堆積、優先佇列與 Top-K 演算法（Heap, Priority Queue & Top-K Elements）
展示手寫泛型最小二元堆積（MinHeap）、Top-K 最大元素篩選與合併 K 個已排序序列。
"""

from __future__ import annotations

import heapq
from typing import Any, Generic, Iterable, Optional, Sequence, TypeVar

T = TypeVar("T")


class MinHeap(Generic[T]):
    """以動態陣列封裝之最小二元堆積（Binary Min-Heap），支援 O(log n) 插入與彈出最小值。"""

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
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
        """插入新元素並執行上浮（Sift-Up）維護堆積性質，時間複雜度 O(log n)。"""
        self._data.append(val)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> T:
        """彈出並回傳堆頂最小元素，將尾端元素移至堆頂後執行下沉（Sift-Down），時間複雜度 O(log n)。"""
        if not self._data:
            raise IndexError("pop from empty MinHeap")
        min_val = self._data[0]
        last_val = self._data.pop()
        if self._data:
            self._data[0] = last_val
            self._sift_down(0)
        return min_val

    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            if self._data[idx] < self._data[parent]:  # type: ignore[operator]
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
            if left < n and self._data[left] < self._data[smallest]:  # type: ignore[operator]
                smallest = left
            if right < n and self._data[right] < self._data[smallest]:  # type: ignore[operator]
                smallest = right
            if smallest == idx:
                break
            self._data[idx], self._data[smallest] = self._data[smallest], self._data[idx]
            idx = smallest


def top_k_largest(nums: Sequence[int], k: int) -> list[int]:
    """利用大小固定為 k 的最小堆積，在 O(n log k) 時間與 O(k) 空間內找出前 k 大元素（由大到小回傳）。"""
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
    """利用最小堆積在 O(N log K) 時間內合併 K 個已排序遞增序列（LeetCode #23 核心邏輯）。"""
    heap: list[tuple[int, int, int]] = []
    for list_idx, seq in enumerate(lists):
        if seq:
            heapq.heappush(heap, (seq[0], list_idx, 0))

    merged: list[int] = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        merged.append(val)
        next_idx = elem_idx + 1
        if next_idx < len(lists[list_idx]):
            heapq.heappush(heap, (lists[list_idx][next_idx], list_idx, next_idx))
    return merged


if __name__ == "__main__":
    h = MinHeap([5, 1, 8, 3])
    popped = [h.pop() for _ in range(len(h))]
    top3 = top_k_largest([64, 34, 25, 12, 22, 11, 90], k=3)
    merged_res = merge_k_sorted_lists([[1, 4, 5], [1, 3, 4], [2, 6]])
    print(
        f"Ch.07 MinHeap 依序彈出: {popped} | "
        f"Top-3 最大元素: {top3} | "
        f"合併 K 串列: {merged_res}"
    )
