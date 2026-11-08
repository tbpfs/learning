#!/usr/bin/env python3
"""
Ch.01 陣列與單向鏈結串列（Array & Singly Linked List）
展示基礎節點（ListNode）與單向鏈結串列（SinglyLinkedList）的插入、刪除、搜尋與反轉操作。
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Iterable, Optional, TypeVar

T = TypeVar("T")


@dataclass
class ListNode(Generic[T]):
    val: T
    next: Optional[ListNode[T]] = None


class SinglyLinkedList(Generic[T]):
    """教學用單向鏈結串列實作（支援頭尾插入、指定值刪除、搜尋與原地反轉）。"""

    def __init__(self, values: Optional[Iterable[T]] = None) -> None:
        self.head: Optional[ListNode[T]] = None
        self._size: int = 0
        if values is not None:
            for v in values:
                self.append(v)

    def __len__(self) -> int:
        return self._size

    def prepend(self, val: T) -> None:
        """在串列頭部插入新節點，時間複雜度 O(1)。"""
        self.head = ListNode(val=val, next=self.head)
        self._size += 1

    def append(self, val: T) -> None:
        """在串列尾部附加新節點，時間複雜度 O(n)。"""
        new_node = ListNode(val=val)
        if self.head is None:
            self.head = new_node
        else:
            curr = self.head
            while curr.next is not None:
                curr = curr.next
            curr.next = new_node
        self._size += 1

    def find(self, target: T) -> int:
        """搜尋目標值首次出現的索引（0-based），若不存在回傳 -1。"""
        idx = 0
        curr = self.head
        while curr is not None:
            if curr.val == target:
                return idx
            curr = curr.next
            idx += 1
        return -1

    def remove(self, target: T) -> bool:
        """刪除首次出現的目標值節點，成功回傳 True，不存在回傳 False。"""
        prev: Optional[ListNode[T]] = None
        curr = self.head
        while curr is not None:
            if curr.val == target:
                if prev is None:
                    self.head = curr.next
                else:
                    prev.next = curr.next
                self._size -= 1
                return True
            prev = curr
            curr = curr.next
        return False

    def reverse(self) -> None:
        """原地（in-place）反轉鏈結串列，時間複雜度 O(n)，空間複雜度 O(1)。"""
        prev: Optional[ListNode[T]] = None
        curr = self.head
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev

    def to_list(self) -> list[T]:
        result: list[T] = []
        curr = self.head
        while curr is not None:
            result.append(curr.val)
            curr = curr.next
        return result


if __name__ == "__main__":
    sll = SinglyLinkedList([10, 20, 30])
    sll.prepend(5)
    sll.remove(20)
    sll.reverse()
    print("Ch.01 SinglyLinkedList 範例結果:", sll.to_list())
