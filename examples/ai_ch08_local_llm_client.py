#!/usr/bin/env python3
"""
Book 1 Ch.08 地端開源大模型實戰（LM Studio / Ollama）：零依賴客戶端、雜湊快取與 VRAM 估算
示範 OpenAI-Compatible API 請求封裝、關閉思考模式、剝離 <think> 標籤與 SHA-256 斷點快取（CI 全離線安全）。
"""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Callable

THINK_BLOCK_RE = re.compile(r"<think>.*?</think>", flags=re.DOTALL | re.IGNORECASE)
FENCE_RE = re.compile(r"^```[a-zA-Z0-9_-]*\s*|\s*```$", flags=re.DOTALL)


def estimate_gguf_vram_gb(params_billion: float, quant_bits: float = 4.5, context_k: int = 8) -> float:
    """估算地端模型載入所需顯存（權重空間 ＋ KV Cache ＋ 系統開銷）。"""
    if params_billion <= 0 or quant_bits <= 0:
        raise ValueError("參數規模與量化位元數必須為正數")
    weights_gb = params_billion * (quant_bits / 8.0)
    kv_cache_gb = (context_k / 8.0) * (params_billion * 0.04)
    runtime_overhead_gb = 1.2
    return round(weights_gb + kv_cache_gb + runtime_overhead_gb, 2)


def clean_local_llm_output(raw_text: str) -> str:
    """剝離地端推理模型可能夾帶的 <think> 思考區塊與外層 Markdown 程式碼圍欄。"""
    no_think = THINK_BLOCK_RE.sub("", raw_text).strip()
    return FENCE_RE.sub("", no_think).strip()


class CachedLocalLlmClient:
    """支援斷點雜湊快取與依賴注入傳輸層（Transport）之本機 OpenAI-Compatible 客戶端。"""

    def __init__(
        self,
        model_id: str,
        transport: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> None:
        self.model_id = model_id
        self.transport = transport
        self.cache: dict[str, str] = {}
        self.api_calls = 0

    def _cache_key(self, system_prompt: str, user_prompt: str) -> str:
        raw = json.dumps([self.model_id, system_prompt, user_prompt], ensure_ascii=False)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def complete(self, system_prompt: str, user_prompt: str, *, max_tokens: int = 1024) -> str:
        key = self._cache_key(system_prompt, user_prompt)
        if key in self.cache:
            return self.cache[key]
        payload = {
            "model": self.model_id,
            "reasoning_effort": "none",
            "temperature": 0.2,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        self.api_calls += 1
        resp = self.transport(payload)
        raw_content = resp["choices"][0]["message"]["content"]
        cleaned = clean_local_llm_output(raw_content)
        self.cache[key] = cleaned
        return cleaned


if __name__ == "__main__":
    # CI 環境零網路依賴：使用記憶體內模擬傳輸層示範 <think> 清理與快取命中
    def mock_lm_studio(_payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "choices": [{
                "message": {
                    "content": "<think>internal chain of thought</think>\n```json\n{\"status\": \"ready\"}\n```"
                }
            }]
        }

    client = CachedLocalLlmClient("gemma4-26b-a4b-qat", transport=mock_lm_studio)
    first = client.complete("Return JSON only.", "Ping status")
    second = client.complete("Return JSON only.", "Ping status")
    vram_26b = estimate_gguf_vram_gb(26.0, quant_bits=4.5, context_k=8)
    print(
        f"Ch.08 26B Q4 預估顯存: {vram_26b} GB | "
        f"清理輸出: {first} | 二次呼叫快取命中(API次={client.api_calls}): {first == second}"
    )
