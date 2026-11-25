#!/usr/bin/env python3
"""
Book 1 Ch.06 MCP（Model Context Protocol）深度實戰：純標準庫 JSON-RPC 2.0 迷你 MCP Server
零外部依賴完整實作 initialize、tools/list、tools/call 與 resources/list 協定訊息路由。
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class McpToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[[dict[str, Any]], Any]


class MiniMcpServer:
    """符合 JSON-RPC 2.0 與 MCP 核心握手契約的輕量級教學實作。"""

    def __init__(self, server_name: str = "purple-maple-mini-mcp", version: str = "1.0.0") -> None:
        self.server_name = server_name
        self.version = version
        self.tools: dict[str, McpToolSpec] = {}
        self.resources: dict[str, str] = {}

    def register_tool(self, spec: McpToolSpec) -> None:
        self.tools[spec.name] = spec

    def register_resource(self, uri: str, content: str) -> None:
        self.resources[uri] = content

    def handle_request(self, raw_json: str) -> str:
        req = json.loads(raw_json)
        req_id = req.get("id")
        method = req.get("method", "")
        params = req.get("params") or {}

        if req.get("jsonrpc") != "2.0":
            return self._error(req_id, -32600, "Invalid JSON-RPC version")

        if method == "initialize":
            return self._ok(req_id, {
                "protocolVersion": "2025-03-26",
                "serverInfo": {"name": self.server_name, "version": self.version},
                "capabilities": {"tools": {}, "resources": {}},
            })

        if method == "tools/list":
            return self._ok(req_id, {
                "tools": [
                    {
                        "name": t.name,
                        "description": t.description,
                        "inputSchema": t.input_schema,
                    }
                    for t in self.tools.values()
                ]
            })

        if method == "tools/call":
            tname = str(params.get("name", ""))
            args = params.get("arguments") or {}
            if tname not in self.tools:
                return self._error(req_id, -32601, f"Unknown tool: {tname}")
            output = self.tools[tname].handler(args)
            return self._ok(req_id, {"content": [{"type": "text", "text": str(output)}], "isError": False})

        if method == "resources/list":
            return self._ok(req_id, {"resources": [{"uri": u} for u in sorted(self.resources)]})

        return self._error(req_id, -32601, f"Method not found: {method}")

    @staticmethod
    def _ok(req_id: Any, result: dict[str, Any]) -> str:
        return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result}, ensure_ascii=False)

    @staticmethod
    def _error(req_id: Any, code: int, message: str) -> str:
        return json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}, ensure_ascii=False)


if __name__ == "__main__":
    srv = MiniMcpServer()
    srv.register_tool(McpToolSpec(
        name="estimate_vram_gb",
        description="Estimate Q4 GGUF VRAM in GB from parameter count (billions).",
        input_schema={"type": "object", "properties": {"params_b": {"type": "number"}}, "required": ["params_b"]},
        handler=lambda a: round(float(a["params_b"]) * 0.65 + 1.5, 2),
    ))
    srv.register_resource("docs://mcp/spec", "MCP standardizes tool and resource discovery via JSON-RPC 2.0.")

    init_res = json.loads(srv.handle_request(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"})))
    call_res = json.loads(srv.handle_request(json.dumps({
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": "estimate_vram_gb", "arguments": {"params_b": 32}},
    })))
    print(
        f"Ch.06 MCP 握手協定: {init_res['result']['protocolVersion']} | "
        f"tools/call(32B Q4 VRAM GB): {call_res['result']['content'][0]['text']}"
    )
