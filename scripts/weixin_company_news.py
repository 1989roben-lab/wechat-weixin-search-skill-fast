#!/usr/bin/env python3
import argparse
import asyncio
import json
import os
import sys
import time


DEFAULT_MCP_COMMAND = "/Users/jianghua.hang/.codex/mcp-servers/weixin-search-mcp/.venv/bin/weixin_search_mcp"
DEFAULT_VENV_PYTHON = "/Users/jianghua.hang/.codex/mcp-servers/weixin-search-mcp/.venv/bin/python"
MCP_COMMAND = os.environ.get("WEIXIN_SEARCH_MCP_COMMAND", DEFAULT_MCP_COMMAND)
VENV_PYTHON = os.environ.get("WEIXIN_SEARCH_MCP_PYTHON", DEFAULT_VENV_PYTHON)

if sys.executable != VENV_PYTHON and os.path.exists(VENV_PYTHON):
    os.execv(VENV_PYTHON, [VENV_PYTHON, __file__, *sys.argv[1:]])

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def split_csv(value):
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


async def run(args):
    params = StdioServerParameters(
        command=MCP_COMMAND,
        args=["--transport", "stdio"],
        env={
            "WEIXIN_SEARCH_TIMEOUT": str(args.timeout),
            "WEIXIN_RESOLVE_REAL_URL_IN_SEARCH": "false",
        },
    )
    started = time.perf_counter()
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "weixin_company_news",
                {
                    "company": args.company,
                    "topics": split_csv(args.topics) or None,
                    "exclude_terms": split_csv(args.exclude) or None,
                    "max_results": args.limit,
                    "page": args.page,
                    "max_workers": args.workers,
                },
            )
            elapsed = time.perf_counter() - started
            items = json.loads(result.content[0].text if result.content else "[]")
            print(json.dumps({"elapsed": round(elapsed, 3), "items": items}, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Fast WeChat Official Account company news search")
    parser.add_argument("--company", required=True)
    parser.add_argument("--topics", default="")
    parser.add_argument("--exclude", default="招聘,校园招聘,实习,内推,培训班,课程报名")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=3)
    parser.add_argument("--page", type=int, default=1)
    args = parser.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
