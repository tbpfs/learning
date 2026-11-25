#!/usr/bin/env python3
"""
Book 1 Ch.05 解剖 AI Agent 核心迴圈：ReAct 有限狀態機（FSM）與步數護欄
以零外部依賴示範 Tool Registry、Think-Act-Observe 迴圈、防無窮迴圈步數上限與對話記憶視窗壓縮。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass(frozen=True)
class AgentAction:
    kind: str  # "tool" | "final"
    tool_name: str = ""
    arguments: dict[str, Any] = field(default_factory=dict)
    final_answer: str = ""


class ToolAgentFSM:
    """具備明確狀態轉移、工具白名單與最大步數護欄的迷你 ReAct Agent。"""

    def __init__(
        self,
        tools: dict[str, Callable[..., Any]],
        planner: Callable[[list[dict[str, str]]], AgentAction],
        *,
        max_steps: int = 5,
        memory_window: int = 6,
    ) -> None:
        self.tools = tools
        self.planner = planner
        self.max_steps = max_steps
        self.memory_window = memory_window

    def _trim_memory(self, history: list[dict[str, str]]) -> list[dict[str, str]]:
        if len(history) <= self.memory_window:
            return history
        return [history[0], *history[-(self.memory_window - 1) :]]

    def run(self, goal: str) -> tuple[str, int, list[str]]:
        history: list[dict[str, str]] = [{"role": "user", "content": goal}]
        trace: list[str] = []
        for step in range(1, self.max_steps + 1):
            action = self.planner(self._trim_memory(history))
            if action.kind == "final":
                trace.append(f"step{step}:FINAL")
                return action.final_answer, step, trace
            if action.tool_name not in self.tools:
                obs = f"ERROR: unknown tool '{action.tool_name}'"
                trace.append(f"step{step}:REJECT({action.tool_name})")
            else:
                try:
                    res = self.tools[action.tool_name](**action.arguments)
                    obs = f"OBSERVATION: {res}"
                    trace.append(f"step{step}:TOOL({action.tool_name})={res}")
                except Exception as exc:
                    obs = f"ERROR: {exc}"
                    trace.append(f"step{step}:ERR({action.tool_name})")
            history.append({"role": "assistant", "content": f"call {action.tool_name}"})
            history.append({"role": "tool", "content": obs})
        raise RuntimeError(f"Agent 超過最大步數上限 ({self.max_steps})，強制中止防止燒光 Token")


if __name__ == "__main__":
    def calc_monthly_cost(daily_req: int, tokens_per_req: int, usd_per_1m: float) -> float:
        return round((daily_req * 30 * tokens_per_req / 1_000_000) * usd_per_1m, 2)

    scripted_actions = iter([
        AgentAction(kind="tool", tool_name="calc_monthly_cost", arguments={"daily_req": 2000, "tokens_per_req": 1500, "usd_per_1m": 0.30}),
        AgentAction(kind="final", final_answer="Estimated monthly LLM API spend is $27.0 USD."),
    ])
    agent = ToolAgentFSM(
        tools={"calc_monthly_cost": calc_monthly_cost},
        planner=lambda _hist: next(scripted_actions),
        max_steps=4,
    )
    ans, steps, trace = agent.run("Calculate monthly API cost for 2000 req/day")
    print(f"Ch.05 Agent 完成步數: {steps} | 軌跡: {trace} | 結論: {ans}")
