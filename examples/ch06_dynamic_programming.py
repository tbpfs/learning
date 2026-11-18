#!/usr/bin/env python3
"""
Ch.06 動態規劃與記憶化搜尋（Dynamic Programming & Memoization）
展示狀態壓縮費氏爬樓梯 O(1) 空間、一維滾動陣列 0/1 背包問題與二分搜尋最佳化之最長遞增子序列（LIS）。
"""

from __future__ import annotations

from bisect import bisect_left
from typing import Sequence


def climb_stairs_dp(n: int) -> int:
    """
    計算爬到第 n 階樓梯的方法數（每次可跨 1 階或 2 階）。
    採用滾動變數狀態壓縮（Space-Optimized Bottom-Up DP）：
    時間複雜度 O(n)，空間複雜度 O(1)。
    """
    if n < 0:
        raise ValueError("階數 n 不得為負數")
    if n <= 1:
        return 1
    prev2, prev1 = 1, 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1


def knapsack_01(weights: Sequence[int], values: Sequence[int], capacity: int) -> int:
    """
    經典 0/1 背包問題：每種物品最多只能選取一次，在總重量不超過 capacity 下求最大總價值。
    採用一維滾動陣列並由後往前（capacity -> w）更新，防止同一物品在同一輪被重複選取：
    時間複雜度 O(N * W)，空間複雜度 O(W)。
    """
    if capacity <= 0 or not weights or not values:
        return 0
    if len(weights) != len(values):
        raise ValueError("weights 與 values 長度必須一致")

    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for curr_cap in range(capacity, w - 1, -1):
            candidate = dp[curr_cap - w] + v
            if candidate > dp[curr_cap]:
                dp[curr_cap] = candidate
    return dp[capacity]


def length_of_lis(nums: Sequence[int]) -> int:
    """
    求解最長嚴格遞增子序列（Longest Increasing Subsequence, LIS）的長度。
    結合貪婪策略與二分搜尋（Patience Sorting），維護各長度遞增子序列的最小結尾元素 tails：
    時間複雜度 O(n log n)，空間複雜度 O(n)。
    """
    tails: list[int] = []
    for x in nums:
        idx = bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    return len(tails)


if __name__ == "__main__":
    stairs_ways = climb_stairs_dp(10)
    max_val = knapsack_01(weights=[10, 20, 30], values=[60, 100, 120], capacity=50)
    lis_len = length_of_lis([10, 9, 2, 5, 3, 7, 101, 18])
    print(f"Ch.06 DP 爬樓梯(n=10): {stairs_ways} | 0/1 背包最大價值: {max_val} | LIS 長度: {lis_len}")
