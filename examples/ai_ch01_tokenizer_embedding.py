#!/usr/bin/env python3
"""
Book 1 Ch.01 LLM 底層直覺：手刻迷你 BPE Tokenizer 與詞向量餘弦相似度
零外部依賴示範 Byte Pair Encoding（BPE）子詞合併訓練、編碼、解碼，以及語意向量餘弦相似度計算。
"""

from __future__ import annotations

import math
from collections import Counter
from typing import Sequence


class MiniBPETokenizer:
    """教學用迷你 Byte Pair Encoding (BPE) 分詞器，演示子詞合併與編解碼原理。"""

    def __init__(self) -> None:
        self.merges: list[tuple[str, str]] = []
        self.vocab: dict[str, int] = {}
        self.id_to_token: dict[int, str] = {}

    def train(self, corpus: Sequence[str], num_merges: int = 12) -> None:
        """從文字語料中迭代合併出現頻率最高的相鄰符號對，建立子詞詞表。"""
        word_freqs: Counter[tuple[str, ...]] = Counter()
        for line in corpus:
            for word in line.strip().split():
                symbols = tuple(list(word) + ["</w>"])
                word_freqs[symbols] += 1

        self.merges = []
        for _ in range(num_merges):
            pair_counts: Counter[tuple[str, str]] = Counter()
            for symbols, freq in word_freqs.items():
                for i in range(len(symbols) - 1):
                    pair_counts[(symbols[i], symbols[i + 1])] += freq
            if not pair_counts:
                break
            best_pair = max(pair_counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
            if pair_counts[best_pair] < 2:
                break
            self.merges.append(best_pair)
            merged_token = best_pair[0] + best_pair[1]
            new_word_freqs: Counter[tuple[str, ...]] = Counter()
            for symbols, freq in word_freqs.items():
                updated: list[str] = []
                i = 0
                while i < len(symbols):
                    if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == best_pair:
                        updated.append(merged_token)
                        i += 2
                    else:
                        updated.append(symbols[i])
                        i += 1
                new_word_freqs[tuple(updated)] += freq
            word_freqs = new_word_freqs

        tokens = sorted({tok for symbols in word_freqs for tok in symbols} | {"<unk>"})
        self.vocab = {tok: idx for idx, tok in enumerate(tokens)}
        self.id_to_token = {idx: tok for tok, idx in self.vocab.items()}

    def _encode_word(self, word: str) -> list[str]:
        symbols = list(word) + ["</w>"]
        for a, b in self.merges:
            merged = a + b
            i = 0
            updated: list[str] = []
            while i < len(symbols):
                if i < len(symbols) - 1 and symbols[i] == a and symbols[i + 1] == b:
                    updated.append(merged)
                    i += 2
                else:
                    updated.append(symbols[i])
                    i += 1
            symbols = updated
        return symbols

    def encode(self, text: str) -> list[int]:
        """將輸入文字編碼為 Token ID 串列（未登錄符號退回 <unk>）。"""
        unk_id = self.vocab["<unk>"]
        ids: list[int] = []
        for word in text.strip().split():
            for tok in self._encode_word(word):
                ids.append(self.vocab.get(tok, unk_id))
        return ids

    def decode(self, ids: Sequence[int]) -> str:
        """將 Token ID 串列還原為可讀文字。"""
        pieces = [self.id_to_token.get(i, "<unk>") for i in ids]
        joined = "".join(pieces)
        return joined.replace("</w>", " ").strip()


def cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    """計算兩個高維語意向量之餘弦相似度，值域 [-1.0, 1.0]。"""
    if len(vec_a) != len(vec_b) or not vec_a:
        raise ValueError("向量維度必須相同且不可為空")
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def scaled_dot_product_weights(query: Sequence[float], keys: Sequence[Sequence[float]]) -> list[float]:
    """模擬單頭 Self-Attention 的縮放點積與 Softmax 注意力權重分佈。"""
    dim = len(query)
    scale = math.sqrt(dim)
    logits = [sum(q * k for q, k in zip(query, key)) / scale for key in keys]
    max_logit = max(logits)
    exps = [math.exp(x - max_logit) for x in logits]
    total = sum(exps)
    return [round(e / total, 4) for e in exps]


if __name__ == "__main__":
    corpus = [
        "token token embedding attention",
        "tokenization embedding context window",
        "attention mechanism transformer token",
    ]
    tok = MiniBPETokenizer()
    tok.train(corpus, num_merges=10)
    sample_text = "token attention"
    encoded = tok.encode(sample_text)
    decoded = tok.decode(encoded)

    # 3 維語意示範向量：[程式概念, AI 模型, 料理]
    v_rag = [0.85, 0.92, 0.05]
    v_agent = [0.80, 0.95, 0.02]
    v_ramen = [0.05, 0.03, 0.98]
    sim_ai = cosine_similarity(v_rag, v_agent)
    sim_food = cosine_similarity(v_rag, v_ramen)
    attn = scaled_dot_product_weights(v_rag, [v_agent, v_ramen])

    print(
        f"Ch.01 BPE 詞表大小: {len(tok.vocab)} | "
        f"編碼長度: {len(encoded)} | 還原: '{decoded}' | "
        f"語意相似度(RAG vs Agent): {sim_ai:.4f} | "
        f"(RAG vs Ramen): {sim_food:.4f} | Attention 權重: {attn}"
    )
