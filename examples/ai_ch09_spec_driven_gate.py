#!/usr/bin/env python3
"""
Book 1 Ch.09 從 Vibe Coding 到 Spec-Driven Engineering：自動化規格契約驗證閘門（Spec-to-Test Gate）
示範如何把口頭需求轉化為可機讀的不變量契約（Invariants），在 AI 寫扣後自動攔截回歸漏洞。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Sequence


@dataclass(frozen=True)
class ContractCase:
    name: str
    args: tuple[Any, ...]
    expected: Any


@dataclass(frozen=True)
class SpecContract:
    feature_name: str
    cases: tuple[ContractCase, ...]
    invariants: tuple[tuple[str, Callable[[Callable[..., Any]], bool]], ...]


def verify_implementation_against_spec(
    impl: Callable[..., Any],
    contract: SpecContract,
) -> tuple[bool, list[str]]:
    """逐條檢驗 AI 產出的實作是否同時滿足範例測資與系統不變量。"""
    failures: list[str] = []
    for case in contract.cases:
        try:
            got = impl(*case.args)
        except Exception as exc:
            failures.append(f"Case '{case.name}' 拋出未預期例外: {exc}")
            continue
        if got != case.expected:
            failures.append(f"Case '{case.name}' 預期 {case.expected!r}，實得 {got!r}")
    for inv_name, check_fn in contract.invariants:
        try:
            if not check_fn(impl):
                failures.append(f"Invariant '{inv_name}' 違反契約")
        except Exception as exc:
            failures.append(f"Invariant '{inv_name}' 例外: {exc}")
    return len(failures) == 0, failures


def vibe_coded_discount(price: float, pct: float) -> float:
    """反面教材：Vibe Coding 常見缺邊界保護（未鎖 0..100% 折扣上限，會算出負價格）。"""
    return round(price * (1.0 - pct / 100.0), 2)


def spec_driven_discount(price: float, pct: float) -> float:
    """規格驅動正解：嚴格保證輸入不變量、折扣夾擠與零負價。"""
    if price < 0:
        raise ValueError("price 不可為負數")
    clamped = max(0.0, min(100.0, pct))
    return round(price * (1.0 - clamped / 100.0), 2)


if __name__ == "__main__":
    contract = SpecContract(
        feature_name="pricing.apply_discount",
        cases=(
            ContractCase("normal_20pct", (100.0, 20.0), 80.0),
            ContractCase("clamp_over_100", (100.0, 150.0), 0.0),
            ContractCase("clamp_negative_pct", (100.0, -10.0), 100.0),
        ),
        invariants=(
            ("never_negative", lambda fn: all(fn(p, d) >= 0.0 for p in (0, 50, 999) for d in (-20, 0, 50, 150))),
            ("monotonic_discount", lambda fn: fn(100.0, 10.0) >= fn(100.0, 30.0)),
        ),
    )
    ok_vibe, err_vibe = verify_implementation_against_spec(vibe_coded_discount, contract)
    ok_spec, err_spec = verify_implementation_against_spec(spec_driven_discount, contract)
    print(f"Ch.09 Vibe 版驗收: {ok_vibe} (抓出 {len(err_vibe)} 項漏洞) | Spec 版驗收: {ok_spec} (漏洞={len(err_spec)})")
