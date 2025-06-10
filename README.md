# Q CLI MCP Server

A FastMCP server implementation that allows other AI agents to interact with Amazon Q CLI through the Model Context Protocol (MCP).

## Features

- **q_chat**: Execute Q CLI chat commands with AI assistant
- **q_whoami**: Get current Q CLI user information
- **q_diagnostic**: Run Q CLI diagnostic tests

## Package Structure

```
q_mcp_server/
├── q_cli_mcp/              # Main package directory
│   ├── __init__.py         # Package initialization
│   └── server.py           # MCP server implementation
├── pyproject.toml          # Package configuration
├── requirements.txt        # Dependencies
├── add_to_q.sh            # Installation script
└── README.md              # This file
```

## Installation

### Method 1: Using the installation script
```bash
./add_to_q.sh
```

### Method 2: Manual installation

1. Install the package dependencies:
```bash
uv sync
```

2. Add to Q CLI:
```bash
q mcp add q-cli-proxy --command "uvx" --args "--from /path/to/q_mcp_server q-cli-mcp-server"
```

### Verify Installation

```bash
q mcp list
q mcp status --name q-cli-proxy
```

## Usage

### Running the server directly
```bash
# Using uv (in project environment)
uv run q-cli-mcp-server

# Using uvx (isolated environment)
uvx --from . q-cli-mcp-server
```

### Using with Q CLI
Once added to Q CLI, you can use the tools:
```bash
q "Use the q_chat tool to ask: What is 1+1?"
q "Use the q_whoami tool to get user information"
q "Use the q_diagnostic tool to run diagnostics"
```

## Implementation Details

The server uses FastMCP with proper subprocess handling for Q CLI commands:
- Non-interactive mode with trusted tools
- Proper stdin/stdout management
- Environment variable handling
- Robust error handling and logging
- Proper Python package structure with entry points

## Example Usage

```python
# Call q_chat tool
result = await session.call_tool("q_chat", {"prompt": "1+1"})

# Call q_whoami tool
result = await session.call_tool("q_whoami", {})

# Call q_diagnostic tool
result = await session.call_tool("q_diagnostic", {})
```

## Files

- `q_cli_mcp/server.py`: Main MCP server implementation
- `q_cli_mcp/__init__.py`: Package initialization
- `pyproject.toml`: Project and dependency configuration with entry points
- `requirements.txt`: Python dependencies
- `add_to_q.sh`: Installation script

## Configuration

The MCP server configuration is stored in `.amazonq/mcp.json` and uses uvx for dependency isolation with proper package entry points.
# q-cli-mcp-server
