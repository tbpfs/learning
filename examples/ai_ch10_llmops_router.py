#!/usr/bin/env python3
"""
Book 1 Ch.10 AI 系統上線與 LLMOps：雙層模型路由、精確 Token 成本帳本與 Token Bucket 限流器
示範如何依任務難度將日常流量分流至輕量低價模型、保留旗艦模型給複雜推理，並透過限流防爆帳單。
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelTier:
    model_id: str
    input_per_1m_usd: float
    output_per_1m_usd: float


FAST_TIER = ModelTier("flash-lite", input_per_1m_usd=0.15, output_per_1m_usd=0.60)
PRO_TIER = ModelTier("frontier-pro", input_per_1m_usd=2.50, output_per_1m_usd=10.00)


def route_model(task_type: str, context_tokens: int) -> ModelTier:
    """雙層路由策略：分類／摘要／擷取走輕量級；深度架構審查或超長推理才升艙旗艦。"""
    if task_type in {"classify", "summarize", "extract"} and context_tokens <= 16_000:
        return FAST_TIER
    return PRO_TIER


def compute_call_cost_usd(tier: ModelTier, input_tokens: int, output_tokens: int) -> float:
    return (input_tokens / 1_000_000) * tier.input_per_1m_usd + (output_tokens / 1_000_000) * tier.output_per_1m_usd


class TokenBucketLimiter:
    """經典 Token Bucket 演算法：限制每分鐘最大請求突發量，防止迴圈 Bug 瞬間燒光 API 額度。"""

    def __init__(self, capacity: float, refill_per_sec: float) -> None:
        self.capacity = capacity
        self.refill_per_sec = refill_per_sec
        self.tokens = capacity
        self.last_ts = 0.0

    def allow(self, now_sec: float, cost: float = 1.0) -> bool:
        elapsed = max(0.0, now_sec - self.last_ts)
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_per_sec)
        self.last_ts = now_sec
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False


if __name__ == "__main__":
    workload = [
        ("classify", 1200, 100),
        ("summarize", 3500, 350),
        ("extract", 2000, 250),
        ("architecture_review", 8000, 1200),
    ]
    routed_cost = 0.0
    all_pro_cost = 0.0
    for task, inp, out in workload:
        tier = route_model(task, inp)
        routed_cost += compute_call_cost_usd(tier, inp, out)
        all_pro_cost += compute_call_cost_usd(PRO_TIER, inp, out)

    savings_pct = (1.0 - routed_cost / all_pro_cost) * 100.0
    limiter = TokenBucketLimiter(capacity=2.0, refill_per_sec=0.5)
    burst = [limiter.allow(0.0), limiter.allow(0.0), limiter.allow(0.0), limiter.allow(2.0)]
    print(
        f"Ch.10 雙層路由成本: ${routed_cost:.5f} vs 全旗艦: ${all_pro_cost:.5f} "
        f"(省下 {savings_pct:.1f}%) | TokenBucket 突發測試: {burst}"
    )
