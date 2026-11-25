#!/usr/bin/env python3
"""
Book 1 Ch.03 生產級 RAG 系統：智慧切塊、BM25 關鍵字檢索、向量檢索與 RRF 混合排序
純 Python 3.12 標準庫完整實作 Overlap Chunking、BM25、TF-IDF Cosine 與 Reciprocal Rank Fusion (RRF)。
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Sequence


def tokenize_mixed(text: str) -> list[str]:
    """支援英文單字與中文單字切分的輕量分詞器。"""
    return re.findall(r"[a-z0-9_]+|[\u4e00-\u9fff]", text.lower())


def chunk_with_overlap(text: str, chunk_size: int = 80, overlap: int = 20) -> list[str]:
    """滑動視窗文字切塊（Chunking with Overlap），防止語意在邊界被腰斬。"""
    if chunk_size <= overlap:
        raise ValueError("chunk_size 必須大於 overlap")
    clean = " ".join(text.split())
    if len(clean) <= chunk_size:
        return [clean]
    chunks: list[str] = []
    step = chunk_size - overlap
    for start in range(0, len(clean), step):
        piece = clean[start : start + chunk_size].strip()
        if piece:
            chunks.append(piece)
        if start + chunk_size >= len(clean):
            break
    return chunks


class HybridRetriever:
    """結合 BM25 精確關鍵字檢索與 TF-IDF 向量檢索的迷你混合檢索引擎（RRF 融合）。"""

    def __init__(self, documents: Sequence[str], k1: float = 1.5, b: float = 0.75) -> None:
        self.docs = list(documents)
        self.k1 = k1
        self.b = b
        self.tokenized = [tokenize_mixed(d) for d in self.docs]
        self.doc_freqs: Counter[str] = Counter()
        for toks in self.tokenized:
            for term in set(toks):
                self.doc_freqs[term] += 1
        self.avg_dl = sum(len(t) for t in self.tokenized) / max(1, len(self.tokenized))
        self.tfidf_vecs = [self._build_tfidf(t) for t in self.tokenized]

    def _idf(self, term: str) -> float:
        n = len(self.docs)
        df = self.doc_freqs.get(term, 0)
        return math.log((n - df + 0.5) / (df + 0.5) + 1.0)

    def _build_tfidf(self, tokens: Sequence[str]) -> dict[str, float]:
        tf = Counter(tokens)
        return {term: (cnt / max(1, len(tokens))) * self._idf(term) for term, cnt in tf.items()}

    def search_bm25(self, query: str) -> list[tuple[int, float]]:
        q_terms = tokenize_mixed(query)
        scores: list[tuple[int, float]] = []
        for idx, toks in enumerate(self.tokenized):
            tf = Counter(toks)
            dl = len(toks)
            score = 0.0
            for term in q_terms:
                if term not in tf:
                    continue
                f = tf[term]
                num = f * (self.k1 + 1.0)
                den = f + self.k1 * (1.0 - self.b + self.b * dl / max(1.0, self.avg_dl))
                score += self._idf(term) * (num / den)
            scores.append((idx, score))
        return sorted(scores, key=lambda kv: (-kv[1], kv[0]))

    def search_vector(self, query: str) -> list[tuple[int, float]]:
        q_vec = self._build_tfidf(tokenize_mixed(query))
        q_norm = math.sqrt(sum(v * v for v in q_vec.values()))
        scores: list[tuple[int, float]] = []
        for idx, d_vec in enumerate(self.tfidf_vecs):
            d_norm = math.sqrt(sum(v * v for v in d_vec.values()))
            if q_norm == 0.0 or d_norm == 0.0:
                sim = 0.0
            else:
                dot = sum(q_vec[t] * d_vec.get(t, 0.0) for t in q_vec)
                sim = dot / (q_norm * d_norm)
            scores.append((idx, sim))
        return sorted(scores, key=lambda kv: (-kv[1], kv[0]))

    def search_hybrid_rrf(self, query: str, top_k: int = 3, rrf_k: int = 60) -> list[tuple[int, float]]:
        """Reciprocal Rank Fusion (RRF)：融合 BM25 與向量排名，無須對齊不同量綱分數。"""
        fused: dict[int, float] = {}
        for ranking in (self.search_bm25(query), self.search_vector(query)):
            for rank, (doc_idx, _score) in enumerate(ranking, start=1):
                fused[doc_idx] = fused.get(doc_idx, 0.0) + 1.0 / (rrf_k + rank)
        return sorted(fused.items(), key=lambda kv: (-kv[1], kv[0]))[:top_k]


if __name__ == "__main__":
    docs = [
        "MCP Model Context Protocol uses JSON-RPC 2.0 to connect agents with local tools.",
        "BM25 excels at exact error codes like ERR_429 while embeddings capture paraphrases.",
        "Python collections.deque achieves O(1) popleft for breadth-first search queues.",
    ]
    retriever = HybridRetriever(docs)
    top = retriever.search_hybrid_rrf("ERR_429 exact keyword BM25", top_k=2)
    chunks = chunk_with_overlap(" ".join(docs), chunk_size=75, overlap=15)
    top_fmt = [(i, round(s, 4)) for i, s in top]
    print(f"Ch.03 切塊數量: {len(chunks)} | RRF 混合檢索 Top-2: {top_fmt}")
