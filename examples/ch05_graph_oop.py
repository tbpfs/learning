#!/usr/bin/env python3
"""
Ch.05 圖論走訪與物件導向設計（Graph BFS / DFS & Object-Oriented Programming）
展示鄰接串列（Adjacency List）物件導向封裝、廣度優先搜尋（BFS）、深度優先搜尋（DFS）與無權重圖最短路徑。
"""

from __future__ import annotations

from collections import deque
from typing import Generic, TypeVar

T = TypeVar("T")


class Graph(Generic[T]):
    """以鄰接串列（Adjacency List）封裝之泛型圖論結構，時間複雜度 O(V + E)。"""

    def __init__(self) -> None:
        self._adj: dict[T, list[T]] = {}

    def add_vertex(self, vertex: T) -> None:
        if vertex not in self._adj:
            self._adj[vertex] = []

    def add_edge(self, u: T, v: T, *, bidirectional: bool = True) -> None:
        self.add_vertex(u)
        self.add_vertex(v)
        if v not in self._adj[u]:
            self._adj[u].append(v)
        if bidirectional and u not in self._adj[v]:
            self._adj[v].append(u)

    def neighbors(self, vertex: T) -> list[T]:
        return list(self._adj.get(vertex, []))

    def bfs(self, start: T) -> list[T]:
        """廣度優先搜尋（Breadth-First Search）：利用佇列（Queue）由近而遠逐層擴散走訪，複雜度 O(V + E)。"""
        if start not in self._adj:
            return []
        visited: set[T] = {start}
        queue: deque[T] = deque([start])
        order: list[T] = []
        while queue:
            curr = queue.popleft()
            order.append(curr)
            for nb in self._adj[curr]:
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
        return order

    def dfs(self, start: T) -> list[T]:
        """深度優先搜尋（Depth-First Search）：一條路走到底再回溯（Backtracking），複雜度 O(V + E)。"""
        if start not in self._adj:
            return []
        visited: set[T] = set()
        order: list[T] = []

        def _explore(node: T) -> None:
            visited.add(node)
            order.append(node)
            for nb in self._adj[node]:
                if nb not in visited:
                    _explore(nb)

        _explore(start)
        return order

    def shortest_path_bfs(self, start: T, goal: T) -> list[T] | None:
        """利用 BFS 找出無權重圖中從 start 到 goal 的最少步數最短路徑。"""
        if start not in self._adj or goal not in self._adj:
            return None
        if start == goal:
            return [start]
        parent: dict[T, T | None] = {start: None}
        queue: deque[T] = deque([start])
        while queue:
            curr = queue.popleft()
            for nb in self._adj[curr]:
                if nb not in parent:
                    parent[nb] = curr
                    if nb == goal:
                        path: list[T] = []
                        step: T | None = goal
                        while step is not None:
                            path.append(step)
                            step = parent[step]
                        path.reverse()
                        return path
                    queue.append(nb)
        return None


if __name__ == "__main__":
    g: Graph[str] = Graph()
    for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "E"), ("D", "F"), ("E", "F")]:
        g.add_edge(u, v)
    print(
        "Ch.05 BFS 走訪:",
        g.bfs("A"),
        "| DFS 走訪:",
        g.dfs("A"),
        "| A->F 最短路徑:",
        g.shortest_path_bfs("A", "F"),
    )
