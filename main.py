"""Command-line entry point for the MCPP project."""

from __future__ import annotations

import argparse
from typing import Sequence

from mcp_chatbot import main as run_chatbot
from research_server import run_server


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mcpp",
        description="Run the MCP chatbot or supporting research server.",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "chat",
        help="Start the interactive MCP chatbot.",
    )

    subparsers.add_parser(
        "research-server",
        help="Start the research MCP server.",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "research-server":
        run_server()
        return

    run_chatbot()


if __name__ == "__main__":
    main()
