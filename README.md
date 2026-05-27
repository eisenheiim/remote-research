# MCP - Model Context Protocol Project

A Python-based application that implements the **Model Context Protocol (MCP)** to create intelligent chatbot systems that can interact with multiple data sources and tools through a unified interface.

## Overview

This project demonstrates how to build an MCP client that connects to multiple MCP servers, enabling an AI assistant (powered by Claude) to access tools, resources, and data from various sources including:
- Research paper searching and retrieval
- File system operations
- Web content fetching
- Custom research tools

## Model Context Protocol (MCP) - Core Concepts

### What is MCP?

The **Model Context Protocol** is an open standard that enables AI applications (like Claude) to securely connect to various data sources and tools. It defines how an AI application can:
- Discover available tools and data sources
- Access external resources and services
- Execute operations through a standardized interface
- Maintain secure, authenticated connections

MCP works on a client-server architecture where the AI application acts as a host, connecting to multiple servers that provide different capabilities.

### Key MCP Participants

#### 1. **MCP Host**
- The **AI application** that coordinates and manages connections
- Examples: Claude Desktop, Claude Code, or your chatbot application
- Maintains multiple MCP clients (one per connected server)
- Receives context from servers and uses it to respond to user queries

#### 2. **MCP Client**
- A **component that connects to a single MCP server**
- Created and managed by the MCP Host
- Responsible for:
  - Establishing and maintaining the connection
  - Discovering available tools and resources
  - Forwarding requests to the server
  - Receiving and processing responses
- One client per server (if you connect to 5 servers, you have 5 clients)

#### 3. **MCP Server**
- A **program that provides context, tools, and resources**
- Can run locally (on your machine) or remotely (on a cloud server)
- Examples:
  - Filesystem server (file operations)
  - Database server (query data)
  - API server (fetch external data)
  - Custom server (your own tools)
- Advertises available tools and resources that clients can use

### MCP Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        MCP Host (Your App)                      │
│                     (AI Assistant/Chatbot)                       │
└────────────────────────────────────────────────────────────────┬┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
   ┌─────────┐          ┌─────────┐          ┌─────────┐
   │ MCP     │          │ MCP     │          │ MCP     │
   │ Client  │          │ Client  │          │ Client  │
   └────┬────┘          └────┬────┘          └────┬────┘
        │                    │                    │
        ▼                    ▼                    ▼
   ┌─────────────┐    ┌──────────────┐    ┌──────────────┐
   │ Research    │    │ Filesystem   │    │ Fetch Server │
   │ Server      │    │ Server       │    │              │
   └─────────────┘    └──────────────┘    └──────────────┘
   (Papers/arXiv)    (File Operations)  (Web Content)
```

### MCP Communication Layers

MCP operates on two distinct layers:

#### **Data Layer**
- **What**: JSON-RPC based protocol for communication
- **Includes**: 
  - Tools (executable functions)
  - Resources (data/content access)
  - Prompts (pre-defined queries)
  - Notifications (event broadcasting)
- **Purpose**: Define WHAT can be accessed and HOW to access it

#### **Transport Layer**
- **What**: Communication mechanism for message delivery
- **Types**:
  - **STDIO** (Local): Standard input/output for local servers
  - **HTTP Streaming** (Remote): HTTP protocol for remote servers
- **Purpose**: Define HOW connections are established and maintained

### In This Project

```
Your Application (Host)
        │
        └─► MCP_ChatBot (Client Manager)
                │
                ├─► Research MCP Client ◄─► research_server.py
                │                           (Search papers)
                │
                ├─► Filesystem MCP Client ◄─► @modelcontextprotocol/server-filesystem
                │                            (File operations)
                │
                └─► Fetch MCP Client ◄─► mcp-server-fetch
                                       (Web content)
```

### How Data Flows

1. **User Query** → "Find papers about neural networks"
2. **Host (Your App)** → Receives query
3. **Host** → Asks all connected clients: "What tools can help with this?"
4. **Clients** → Report available tools from their servers
5. **Host** → Uses AI to decide which tool(s) to use
6. **Client** → Sends request to appropriate server
7. **Server** → Executes tool and returns result
8. **Client** → Sends result back to Host
9. **Host** → Processes result and generates response
10. **Response** → Returned to user

## Project Architecture

```
MCPP/
├── main.py                 # Entry point for the application
├── mcp_chatbot.py          # MCP client implementation for chatbot functionality
├── research_server.py      # Custom MCP server for research paper operations
├── server_config.json      # Configuration for MCP servers
├── key.env                 # Environment variables (API keys, credentials)
├── pyproject.toml          # Project dependencies and metadata
├── papers/                 # Storage for downloaded research papers
│   └── llm_reasoning/
│       └── papers_info.json
├── mcp_diagram.txt         # Architecture diagram
├── mcp_summary.md          # MCP documentation reference
└── README.md               # This file
```

## Key Components

### 1. **mcp_chatbot.py** - Core MCP Client
The main chatbot class that:
- Connects to multiple MCP servers using the Model Context Protocol
- Manages tool and prompt availability from connected servers
- Routes user queries to appropriate tools
- Uses OpenAI's API to process natural language and generate responses
- Maintains active sessions with each connected server

**Key Features:**
- Automatic tool discovery from connected MCP servers
- Session management for multiple concurrent connections
- Error handling and recovery mechanisms

### 2. **research_server.py** - Custom MCP Server
A FastMCP-based server that provides:
- `search_papers()`: Search arXiv for academic papers by topic
- Storage of paper metadata and information
- Integration with the arXiv API for paper discovery

**Features:**
- Configurable search parameters
- Automatic paper information storage in JSON format
- Support for multiple research queries

### 3. **server_config.json** - MCP Server Configuration
Defines connections to multiple MCP servers:
- **filesystem**: Node.js-based file system access
- **research**: Custom Python research server
- **fetch**: Web content fetching capabilities

Each server is configured with execution command and parameters.

## Setup Instructions

### Prerequisites
- Python 3.11+
- OpenAI API key
- Internet connection for paper searching and content fetching

### Installation

1. **Clone/navigate to the project directory:**
```bash
cd /Users/sude/Desktop/MCPP
```

2. **Activate the virtual environment:**
```bash
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -e .
```

Or manually install dependencies:
```bash
pip install arxiv mcp nest-asyncio openai python-dotenv
```

4. **Configure API Keys:**
Create or update `key.env` with your credentials:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Running the Chatbot
```bash
python mcp_chatbot.py
```

### Running the Research Server
```bash
python research_server.py
```

### From Main Entry Point
```bash
python main.py
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| arxiv | >=4.0.0 | arXiv paper searching and metadata retrieval |
| mcp | >=1.27.1 | Model Context Protocol implementation |
| nest-asyncio | >=1.6.0 | Async/await support for nested event loops |
| openai | >=1.0.0 | OpenAI Python client library |
| python-dotenv | >=1.2.2 | Environment variable management |

## How It Works

1. **Initialization**: The chatbot loads API keys and initializes connections to configured MCP servers
2. **Server Discovery**: Upon connection, it discovers available tools and prompts from each server
3. **Tool Registration**: Tools are registered with OpenAI as available functions
4. **Query Processing**: User queries are sent to OpenAI with available tools
5. **Tool Execution**: When OpenAI decides a tool is needed, it's called through the appropriate MCP server
6. **Response Generation**: Results are processed and returned to the user

## Project Features

✅ Multi-server MCP client implementation  
✅ Automatic tool discovery and registration  
✅ Academic paper search and retrieval  
✅ Async/await support for concurrent operations  
✅ Error handling and connection management  
✅ Environment-based configuration  

## Configuration

### Server Config (server_config.json)
Each MCP server needs:
- `command`: Executable or command to run the server
- `args`: Arguments to pass to the server command

Example:
```json
{
    "mcpServers": {
        "research": {
            "command": "uv",
            "args": ["run", "research_server.py"]
        }
    }
}
```

## Environment Variables

Create a `key.env` file in the project root:

```env
OPENAI_API_KEY=sk-...          # Your OpenAI API key
```

`OPENAI_API_KEY` is only required for the chatbot client in `mcp_chatbot.py`; the research MCP server can run without it.

**Note**: Never commit `key.env` to version control. Add it to `.gitignore`.

## API Reference

### MCP_ChatBot Class

**Initialization:**
```python
chatbot = MCP_ChatBot()
```

**Available Methods:**
- `connect_to_server(server_name, server_config)`: Establish connection to an MCP server
- `list_available_tools()`: Get all discovered tools
- `list_available_prompts()`: Get all available prompts
- `process_query(user_query)`: Send a query and get a response

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `OPENAI_API_KEY is missing` | Ensure `key.env` exists and contains your API key |
| Server connection fails | Check `server_config.json` paths and commands |
| Tool not discovered | Verify the MCP server is running and responding |
| Async errors | Ensure `nest-asyncio` is installed for nested event loops |

## Future Enhancements

- [ ] Web UI for interactive querying
- [ ] Support for additional MCP servers (database, APIs)
- [ ] Caching mechanism for frequently searched papers
- [ ] Multi-turn conversation memory
- [ ] Streaming responses support
- [ ] Persistent session management

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [arXiv API Documentation](https://arxiv.org/help/api)
- [FastMCP Documentation](https://github.com/jlomnitz/FastMCP)

## License

[Add your license here if applicable]

## Contact & Support

For questions or issues, please refer to the documentation or create an issue in the project repository.

---

**Project Status**: Active Development  
**Last Updated**: May 25, 2026
