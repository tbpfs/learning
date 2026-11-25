#!/usr/bin/env python3
"""
Book 1 Ch.02 Context Engineering 與結構化輸出
示範 Token 預算裁切器（Context Window Budgeter）與嚴格 JSON Schema 校驗＋自動錯誤回授重試管線。
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Callable, Sequence


@dataclass(frozen=True)
class ContextBlock:
    role: str
    content: str
    priority: int  # 數值越大越優先保留（如 System Prompt = 100）


def estimate_tokens(text: str) -> int:
    """以輕量啟發式估算中英混排文字之 Token 數（1 漢字約 1.5 token，1 英文詞約 1.3 token）。"""
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin = len(re.findall(r"[A-Za-z0-9_]+", text))
    return max(1, int(cjk * 1.5 + latin * 1.3))


def pack_context_window(blocks: Sequence[ContextBlock], max_tokens: int) -> list[ContextBlock]:
    """在嚴格 Token 上限內，優先保留高優先級區塊並維持原始對話順序。"""
    indexed = list(enumerate(blocks))
    ranked = sorted(indexed, key=lambda item: (-item[1].priority, item[0]))
    selected_indices: set[int] = set()
    used = 0
    for idx, blk in ranked:
        cost = estimate_tokens(blk.content)
        if used + cost <= max_tokens:
            selected_indices.add(idx)
            used += cost
    return [blk for idx, blk in indexed if idx in selected_indices]


def validate_record_schema(data: Any, required_types: dict[str, type]) -> list[str]:
    """驗證模型回傳物件是否符合預期欄位與型別契約，回傳錯誤清單。"""
    if not isinstance(data, dict):
        return ["根節點必須為 JSON Object"]
    errors: list[str] = []
    for field_name, expected_type in required_types.items():
        if field_name not in data:
            errors.append(f"缺少必填欄位 '{field_name}'")
        elif not isinstance(data[field_name], expected_type):
            errors.append(
                f"欄位 '{field_name}' 型別錯誤：預期 {expected_type.__name__}，"
                f"實得 {type(data[field_name]).__name__}"
            )
    return errors


def generate_structured_with_retry(
    llm_call: Callable[[str], str],
    base_prompt: str,
    required_types: dict[str, type],
    max_attempts: int = 3,
) -> tuple[dict[str, Any], int]:
    """以錯誤訊息回授（Retry-with-Feedback）迫使模型產出 100% 合法 JSON。"""
    prompt = base_prompt
    last_errors: list[str] = []
    for attempt in range(1, max_attempts + 1):
        raw = llm_call(prompt).strip()
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.DOTALL).strip()
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            last_errors = [f"JSON 解析失敗: {exc.msg}"]
        else:
            last_errors = validate_record_schema(parsed, required_types)
            if not last_errors:
                return parsed, attempt
        prompt = f"{base_prompt}\n[前次輸出驗證失敗，請修正以下錯誤後僅回傳純 JSON]: {'; '.join(last_errors)}"
    raise ValueError(f"超過最大重試次數 ({max_attempts}): {last_errors}")


if __name__ == "__main__":
    blocks = [
        ContextBlock("system", "You are a strict JSON code reviewer.", priority=100),
        ContextBlock("history", "Old noisy chat message " * 30, priority=10),
        ContextBlock("rag", "Verified API rate limit is 60 req/min.", priority=80),
        ContextBlock("user", "Extract rate limit as JSON.", priority=95),
    ]
    packed = pack_context_window(blocks, max_tokens=40)

    responses = iter([
        '```json\n{"limit": "sixty"}\n```',  # 第 1 次刻意給錯型別
        '{"limit": 60, "unit": "req/min"}',  # 第 2 次收到錯誤回饋後修正
    ])
    result, attempts = generate_structured_with_retry(
        lambda _p: next(responses),
        "Extract rate limit",
        {"limit": int, "unit": str},
    )
    print(
        f"Ch.02 Context 保留區塊: {[b.role for b in packed]} | "
        f"結構化驗證通過(第 {attempts} 次): {result}"
    )
