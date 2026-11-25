#!/usr/bin/env python3
"""
Book 1 Ch.04 RAG 評估與防幻覺：Recall@K、MRR 與引用溯源（Citation Faithfulness）檢查器
演示無須昂貴外部框架即可建立可重現的 RAG 檢索量化評測與回答忠實度驗證。
"""

from __future__ import annotations

import re
from typing import Sequence


def recall_at_k(retrieved_ids: Sequence[str], relevant_ids: set[str], k: int) -> float:
    """計算前 K 筆檢索結果命中多少比例的標準答案文件。"""
    if not relevant_ids or k <= 0:
        return 0.0
    hits = len(set(retrieved_ids[:k]) & relevant_ids)
    return hits / len(relevant_ids)


def mean_reciprocal_rank(runs: Sequence[tuple[Sequence[str], set[str]]]) -> float:
    """計算多筆測試題之 MRR（首個正確文件排越前面分數越高）。"""
    if not runs:
        return 0.0
    total = 0.0
    for retrieved, relevant in runs:
        rr = 0.0
        for rank, doc_id in enumerate(retrieved, start=1):
            if doc_id in relevant:
                rr = 1.0 / rank
                break
        total += rr
    return total / len(runs)


def check_numeric_faithfulness(answer_text: str, source_chunks: Sequence[str]) -> tuple[bool, list[str]]:
    """檢查模型回答中的所有關鍵數字是否皆有出處（防 RAG 數字幻覺）。"""
    source_corpus = " ".join(source_chunks)
    source_nums = set(re.findall(r"\b\d+(?:\.\d+)?%?", source_corpus))
    answer_nums = re.findall(r"\b\d+(?:\.\d+)?%?", answer_text)
    ungrounded = [n for n in answer_nums if n not in source_nums]
    return len(ungrounded) == 0, ungrounded


if __name__ == "__main__":
    eval_runs = [
        (["doc_2", "doc_1", "doc_5"], {"doc_1"}),
        (["doc_3", "doc_4", "doc_2"], {"doc_3"}),
        (["doc_9", "doc_8", "doc_7"], {"doc_7"}),
    ]
    r_at_2 = sum(recall_at_k(r, rel, 2) for r, rel in eval_runs) / len(eval_runs)
    mrr = mean_reciprocal_rank(eval_runs)

    sources = ["US dividend withholding tax treaty rate is 10% for China residents and 30% default NRA."]
    ok_good, bad_good = check_numeric_faithfulness("Default NRA rate is 30%, treaty rate is 10%.", sources)
    ok_halluc, bad_halluc = check_numeric_faithfulness("The rate is 15% under default rules.", sources)
    print(
        f"Ch.04 Recall@2: {r_at_2:.3f} | MRR: {mrr:.3f} | "
        f"忠實回答檢查: {ok_good} (缺漏={bad_good}) | 幻覺偵測: {ok_halluc} (未佐證={bad_halluc})"
    )
