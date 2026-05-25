# Testing the MCP Research Server

## Using MCP Inspector

The MCP Inspector is a testing tool that lets you interact with your MCP server directly.

### Step 1: Install MCP Inspector (One-time setup)
```bash
npm install -g @modelcontextprotocol/inspector
```

### Step 2: Run the Research Server with Inspector
```bash
mcp-inspector python research_server.py
```

This will:
1. Start the research server in STDIO mode
2. Open the MCP Inspector web interface in your browser
3. Allow you to test tools and resources directly

### Alternative: Using uvx
If you prefer using `uvx` (part of uv):
```bash
uvx @modelcontextprotocol/inspector python research_server.py
```

## What You Can Test in MCP Inspector

### Available Tools:
1. **search_papers(topic, max_results)**
   - Search for academic papers on arXiv
   - Example: `search_papers(topic="neural networks", max_results=5)`

2. **extract_info(paper_id)**
   - Get detailed info about a specific paper
   - Example: `extract_info(paper_id="2401.12345")`

### Available Resources:
1. **papers://folders**
   - List all downloaded topic folders

2. **papers://{topic}**
   - Get papers for a specific topic
   - Example: `papers://neural_networks`

### Available Prompts:
1. **generate_search_prompt(topic, num_papers)**
   - Generate a Claude prompt for paper research

## Troubleshooting

### "npm: command not found"
- Install Node.js from https://nodejs.org/
- Then run: `npm install -g @modelcontextprotocol/inspector`

### "mcp-inspector: command not found"
- Try using `npx`: `npx @modelcontextprotocol/inspector python research_server.py`
- Or install globally: `npm install -g @modelcontextprotocol/inspector`

### Server doesn't respond
- Make sure you're in the MCPP directory: `cd /Users/sude/Desktop/MCPP`
- Activate the virtual environment: `source .venv/bin/activate`
- Check that arxiv package is installed: `pip list | grep arxiv`

## Testing with Your Chatbot

Once you've verified the server works with the Inspector, you can test it with your chatbot:
```bash
python mcp_chatbot.py
```

The chatbot will connect to all configured servers and make their tools available to Claude.
