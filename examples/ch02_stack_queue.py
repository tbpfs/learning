#!/usr/bin/env python3
"""
Ch.02 堆疊與佇列（Stack & Queue）
展示 LIFO 堆疊（含經典括號平衡檢查）與 FIFO 佇列的物件導向封裝實作。
"""

from collections import deque
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    """後進先出（LIFO）堆疊。"""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from empty Stack")
        return self._items.pop()

    def peek(self) -> T:
        if not self._items:
            raise IndexError("peek from empty Stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


class Queue(Generic[T]):
    """先進先出（FIFO）佇列。"""

    def __init__(self) -> None:
        self._items: deque[T] = deque()

    def enqueue(self, item: T) -> None:
        self._items.append(item)

    def dequeue(self) -> T:
        if not self._items:
            raise IndexError("dequeue from empty Queue")
        return self._items.popleft()

    def peek(self) -> Optional[T]:
        return self._items[0] if self._items else None

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)


def is_balanced_brackets(expr: str) -> bool:
    """利用 Stack 檢查字串中的 (), [], {} 括號是否成對且順序正確。"""
    pairs = {")": "(", "]": "[", "}": "{"}
    opening = set(pairs.values())
    stack: Stack[str] = Stack()

    for ch in expr:
        if ch in opening:
            stack.push(ch)
        elif ch in pairs:
            if stack.is_empty() or stack.pop() != pairs[ch]:
                return False
    return stack.is_empty()


if __name__ == "__main__":
    print("Ch.02 括號平衡檢查 '{[()]}':", is_balanced_brackets("{[()]}"))
    q: Queue[str] = Queue()
    q.enqueue("Task-1")
    q.enqueue("Task-2")
    print("Ch.02 Queue dequeue:", q.dequeue())
