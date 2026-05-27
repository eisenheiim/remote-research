# MCPP

An MCP-based Python project that combines an interactive chatbot with a custom research server for discovering, storing, and exploring arXiv papers.

## What This Project Does

MCPP demonstrates how to connect a single client application to multiple MCP servers and use their tools, prompts, and resources in one workflow. In this repo, the main pieces are:

- an interactive chatbot client
- a custom research MCP server
- a file-based store for paper metadata
- support for filesystem and web-fetch MCP servers

## Why It’s Interesting

This project is useful as a portfolio piece because it shows:

- protocol-based tool orchestration
- async Python development
- LLM tool calling
- server/client separation
- local persistence of structured research data

## Features

- Connects to multiple MCP servers from one client
- Discovers and registers server tools automatically
- Searches arXiv for research papers by topic
- Stores paper metadata in JSON files
- Exposes paper folders and topic data as MCP resources
- Supports both local stdio execution and hosted server mode
- Includes a CLI entry point for easier startup

## Project Structure

```text
MCPP/
├── main.py              # CLI entry point
├── mcp_chatbot.py       # Interactive chatbot client
├── research_server.py   # Custom MCP server for research papers
├── server_config.json   # MCP server definitions
├── pyproject.toml       # Package metadata and dependencies
├── requirements.txt     # Locked dependency set
├── papers/              # Saved paper metadata
├── TESTING_GUIDE.md     # Manual testing instructions
└── README.md
```

## Setup

### Prerequisites

- Python 3.11+
- An OpenAI API key
- Internet access for arXiv lookups and fetch tools

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd MCPP
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -e .
```

### 4. Configure environment variables

Copy `.env.example` to `key.env` and add your API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Run the chatbot

```bash
python main.py
```

or, after installation:

```bash
mcpp
```

### Run the research server

```bash
python main.py research-server
```

## Example Flow

1. Start the chatbot
2. Ask it to search for papers on a topic
3. The chatbot calls the research server
4. The research server searches arXiv and stores results
5. The client reads the stored metadata as a resource
6. The assistant summarizes the results for the user

## MCP Overview

The project follows the standard MCP host/client/server model:

- the chatbot acts as the host
- each MCP connection is handled by a client session
- the research server provides tools, prompts, and resources

That separation keeps the project modular and makes it easier to add more servers later.

## Configuration

### `server_config.json`

This file defines the servers the chatbot connects to.

Example:

```json
{
  "mcpServers": {
    "research": {
      "command": "python",
      "args": ["research_server.py"]
    }
  }
}
```

### Environment variables

- `OPENAI_API_KEY`: required for the chatbot client
- `MCP_TRANSPORT`: optional, forces the research server transport
- `PORT`: optional, used when hosting the research server

## Testing

For manual testing instructions, see [TESTING_GUIDE.md](./TESTING_GUIDE.md).

If you want to validate the Python files quickly, you can run:

```bash
python -m py_compile main.py mcp_chatbot.py research_server.py
```

## Tech Stack

- Python
- MCP
- OpenAI Python SDK
- arXiv API
- FastMCP
- Starlette
- Uvicorn

## Roadmap

- add automated tests
- add GitHub Actions CI
- improve error handling and logging
- add a demo screenshot or short video
- support richer paper summaries and citations

## Notes

- `main.py` is the CLI entry point for the project.
- `mcp_chatbot.py` handles the interactive assistant loop.
- `research_server.py` can run locally with stdio or as a hosted server.

## License

Add a license here if you want to publish this publicly.
