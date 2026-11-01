"""MCP server exposing BlockWise's deterministic tools to any MCP client.

Owns: registering the read-only tools (forecast lookup, penalty quote, constraint check)
as MCP tools, reusing the same implementations as agents/tools.py.

Must NOT: expose anything that submits bids or changes state. Those require the operator
approval path in the API.

Phase 9. Requires the "agents" extra.
"""

from __future__ import annotations


def build_server():  # -> mcp server object
    """Create the MCP server and register tools from agents.tools.REGISTRY (read-only ones only)."""
    raise NotImplementedError


def main() -> None:
    """Run the server over stdio."""
    raise NotImplementedError
