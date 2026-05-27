from __future__ import annotations

import asyncio
import json
import os
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Any

import openai
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / "key.env")

SERVER_CONFIG_PATH = BASE_DIR / "server_config.json"


def _tool_result_text(result: Any) -> str:
    if not getattr(result, "content", None):
        return ""

    parts: list[str] = []
    for item in result.content:
        text = getattr(item, "text", None)
        parts.append(text if text is not None else str(item))
    return "\n".join(parts)


def _prompt_args(parts: list[str]) -> dict[str, str]:
    args: dict[str, str] = {}
    for item in parts:
        if "=" in item:
            key, value = item.split("=", 1)
            args[key] = value
    return args


class MCP_ChatBot:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is missing. Put it in key.env or export it in your shell."
            )

        self.client = openai.OpenAI(api_key=api_key)
        self.exit_stack = AsyncExitStack()
        self.available_tools: list[dict[str, Any]] = []
        self.available_prompts: list[dict[str, Any]] = []
        self.sessions: dict[str, ClientSession] = {}

    async def connect_to_server(self, server_name: str, server_config: dict[str, Any]):
        try:
            server_params = StdioServerParameters(**server_config)
            read, write = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            session = await self.exit_stack.enter_async_context(ClientSession(read, write))
            await session.initialize()

            tools_response = await session.list_tools()
            for tool in tools_response.tools:
                self.sessions[tool.name] = session
                self.available_tools.append(
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema,
                    }
                )

            prompts_response = await session.list_prompts()
            for prompt in prompts_response.prompts or []:
                self.sessions[prompt.name] = session
                self.available_prompts.append(
                    {
                        "name": prompt.name,
                        "description": prompt.description,
                        "arguments": prompt.arguments,
                    }
                )

            resources_response = await session.list_resources()
            for resource in resources_response.resources or []:
                self.sessions[str(resource.uri)] = session
        except Exception as exc:
            print(f"Error connecting to {server_name}: {exc}")

    async def connect_to_servers(self):
        try:
            with SERVER_CONFIG_PATH.open("r", encoding="utf-8") as file:
                data = json.load(file)
            for server_name, server_config in data.get("mcpServers", {}).items():
                await self.connect_to_server(server_name, server_config)
        except Exception as exc:
            print(f"Error loading server config: {exc}")
            raise

    async def process_query(self, query: str):
        messages = [{"role": "user", "content": query}]

        openai_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["input_schema"],
                },
            }
            for tool in self.available_tools
        ]

        while True:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                max_tokens=2024,
                tools=openai_tools or None,
                messages=messages,
            )

            used_tool = False
            for choice in response.choices:
                if choice.message.content:
                    print(choice.message.content)

                if not choice.message.tool_calls:
                    continue

                used_tool = True
                messages.append(
                    {
                        "role": "assistant",
                        "content": choice.message.content,
                        "tool_calls": choice.message.tool_calls,
                    }
                )

                for tool_call in choice.message.tool_calls:
                    tool_name = tool_call.function.name
                    session = self.sessions.get(tool_name)
                    if not session:
                        print(f"Tool '{tool_name}' not found.")
                        continue

                    tool_args = json.loads(tool_call.function.arguments)
                    result = await session.call_tool(tool_name, arguments=tool_args)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": _tool_result_text(result),
                        }
                    )

            if not used_tool:
                return

    async def get_resource(self, resource_uri: str):
        session = self.sessions.get(resource_uri)
        if not session and resource_uri.startswith("papers://"):
            session = next(
                (sess for uri, sess in self.sessions.items() if uri.startswith("papers://")),
                None,
            )

        if not session:
            print(f"Resource '{resource_uri}' not found.")
            return

        try:
            result = await session.read_resource(uri=resource_uri)
            if result and result.contents:
                print(f"\nResource: {resource_uri}")
                print("Content:")
                print(result.contents[0].text)
            else:
                print("No content available.")
        except Exception as exc:
            print(f"Error: {exc}")

    async def list_prompts(self):
        if not self.available_prompts:
            print("No prompts available.")
            return

        print("\nAvailable prompts:")
        for prompt in self.available_prompts:
            print(f"- {prompt['name']}: {prompt['description']}")

    async def execute_prompt(self, prompt_name: str, args: dict[str, str]):
        session = self.sessions.get(prompt_name)
        if not session:
            print(f"Prompt '{prompt_name}' not found.")
            return

        try:
            result = await session.get_prompt(prompt_name, arguments=args)
            if not result or not result.messages:
                return

            prompt_content = result.messages[0].content
            if isinstance(prompt_content, str):
                text = prompt_content
            elif hasattr(prompt_content, "text"):
                text = prompt_content.text
            else:
                text = " ".join(
                    item.text if hasattr(item, "text") else str(item)
                    for item in prompt_content
                )

            print(f"\nExecuting prompt '{prompt_name}'...")
            await self.process_query(text)
        except Exception as exc:
            print(f"Error: {exc}")

    async def chat_loop(self):
        print("\nMCP Chatbot Started!")
        print("Type your queries or 'quit' to exit.")
        print("Use @folders to see available topics")
        print("Use @<topic> to search papers in that topic")
        print("Use /prompts to list available prompts")
        print("Use /prompt <name> <arg1=value1> to execute a prompt")

        while True:
            try:
                query = input("\nQuery: ").strip()
                if not query:
                    continue
                if query.lower() == "quit":
                    return

                if query.startswith("@"):
                    topic = query[1:]
                    resource_uri = "papers://folders" if topic == "folders" else f"papers://{topic}"
                    await self.get_resource(resource_uri)
                    continue

                if query.startswith("/"):
                    parts = query.split()
                    command = parts[0].lower()

                    if command == "/prompts":
                        await self.list_prompts()
                    elif command == "/prompt":
                        if len(parts) < 2:
                            print("Usage: /prompt <name> <arg1=value1> <arg2=value2>")
                            continue
                        await self.execute_prompt(parts[1], _prompt_args(parts[2:]))
                    else:
                        print(f"Unknown command: {command}")
                    continue

                await self.process_query(query)
            except Exception as exc:
                print(f"\nError: {exc}")

    async def cleanup(self):
        await self.exit_stack.aclose()

    async def run_async(self):
        try:
            await self.connect_to_servers()
            await self.chat_loop()
        finally:
            await self.cleanup()

    def run(self):
        asyncio.run(self.run_async())


def main():
    MCP_ChatBot().run()


if __name__ == "__main__":
    main()
