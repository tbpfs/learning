#!/usr/bin/env python3
"""
Ch.03 搜尋與排序演算法（Search & Sort Algorithms）
展示二分搜尋法（Binary Search）與合併排序法（Merge Sort）。
"""

from typing import Sequence


def binary_search(sorted_nums: Sequence[int], target: int) -> int:
    """在已排序遞增序列中搜尋 target，回傳索引（0-based）；若不存在則回傳 -1。"""
    left = 0
    right = len(sorted_nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        val = sorted_nums[mid]
        if val == target:
            return mid
        if val < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def merge_sort(nums: Sequence[int]) -> list[int]:
    """使用分治法（Divide & Conquer）實作穩定合併排序，時間複雜度 O(n log n)。"""
    arr = list(nums)
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    merged: list[int] = []
    i = j = 0
    while i < len(left_half) and j < len(right_half):
        if left_half[i] <= right_half[j]:
            merged.append(left_half[i])
            i += 1
        else:
            merged.append(right_half[j])
            j += 1

    if i < len(left_half):
        merged.extend(left_half[i:])
    if j < len(right_half):
        merged.extend(right_half[j:])
    return merged


if __name__ == "__main__":
    sample = [38, 27, 43, 3, 9, 82, 10]
    sorted_sample = merge_sort(sample)
    idx = binary_search(sorted_sample, 27)
    print("Ch.03 Merge Sort 結果:", sorted_sample, "| 27 的索引:", idx)
