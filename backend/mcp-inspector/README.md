# MCP Inspector

MCP inspector is a developer tool for testing and debugging MCP servers via a Visual UI.

## Prerequisites

- Node.js (v22.x or later)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backend/mcp-inspector
```

2. Build the application:
```bash
npm install
```

## Quick Start

Start the server with the specified client port:
```bash
CLIENT_PORT=3000 npx @modelcontextprotocol/inspector
```

## Configuring Additional MCP Servers

You can configure additional MCP servers by updating your `config.json` file:

```json
{
  "mcpServers": {
    "custom-server": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-everything"],
      "env": {
        "PORT": "3003",
        "DEBUG": "true"
      }
    }
  }
}
```

### Troubleshooting Server Configuration

If you encounter issues with server configuration:

1. Verify config.json syntax
2. Check for environment variable conflicts
3. Ensure port availability
4. Enable debug logging:
```bash
DEBUG=* npx @modelcontextprotocol/server-everything
```