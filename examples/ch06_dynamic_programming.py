#!/usr/bin/env python3
"""
Ch.06 動態規劃與記憶化搜尋（Dynamic Programming & Memoization）
展示爬樓梯狀態壓縮 O(1) 空間解法、0/1 背包問題（一維滾動陣列）與最長嚴格遞增子序列（LIS O(n log n)）。
"""

from __future__ import annotations

from bisect import bisect_left
from typing import Sequence


def climb_stairs_dp(n: int) -> int:
    """計算爬到第 n 階樓梯的方法數（每次可跨 1 或 2 階）。

    採用自底向上（Bottom-Up）滾動變數狀態壓縮：
    - 時間複雜度：O(n)
    - 空間複雜度：O(1)
    """
    if n < 0:
        raise ValueError("階數 n 必須為非負整數")
    if n <= 1:
        return 1
    prev2, prev1 = 1, 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1


def knapsack_01(weights: Sequence[int], values: Sequence[int], capacity: int) -> int:
    """經典 0/1 背包問題：在背包容量上限 capacity 內，每件物品最多選一次，求最大總價值。

    採用一維滾動陣列並由後往前（capacity -> weight）逆序更新，避免同一物品被重複選取：
    - 時間複雜度：O(N * W)，其中 N 為物品數、W 為 capacity
    - 空間複雜度：O(W)
    """
    if capacity < 0:
        raise ValueError("capacity 必須為非負整數")
    if len(weights) != len(values):
        raise ValueError("weights 與 values 長度必須一致")
    dp: list[int] = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        if w < 0:
            raise ValueError("物品重量不可為負數")
        for cap in range(capacity, w - 1, -1):
            candidate = dp[cap - w] + v
            if candidate > dp[cap]:
                dp[cap] = candidate
    return dp[capacity]


def length_of_lis(nums: Sequence[int]) -> int:
    """最長嚴格遞增子序列（Longest Increasing Subsequence, LeetCode #300）。

    結合貪婪策略與二分搜尋（Patience Sorting）維護最小結尾陣列 tails：
    - 時間複雜度：O(n log n)
    - 空間複雜度：O(n)
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
    print(
        f"Ch.06 DP 爬樓梯(n=10): {stairs_ways} | "
        f"0/1 背包最大價值: {max_val} | "
        f"LIS 長度: {lis_len}"
    )
