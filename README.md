# XenoDocs MCP - Up-to-date Documentation For Any Library

[![Website](https://img.shields.io/badge/Website-xenodocs.com-blue)](https://xenodocs.com) [![PyPI Version](https://img.shields.io/pypi/v/xenodocs-mcp-server?color=red)](https://pypi.org/project/xenodocs-mcp-server/) [![MIT licensed](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

## ❌ Without XenoDocs

LLMs rely on outdated or generic information about the libraries you use. You get:

- ❌ Code examples are outdated and based on year-old training data
- ❌ Hallucinated APIs that don't even exist
- ❌ Generic answers for old package versions

## ✅ With XenoDocs

XenoDocs MCP pulls up-to-date, version-specific documentation and code examples straight from the source — and places them directly into your prompt.

Tell your AI assistant to search for library documentation:

```txt
Search for "authentication middleware" in the FastAPI library documentation
```

```txt
Find examples of async functions in the httpx library
```

XenoDocs fetches up-to-date code examples and documentation right into your LLM's context.

- 1️⃣ Write your prompt naturally
- 2️⃣ Ask for specific library documentation
- 3️⃣ Get working code answers

No tab-switching, no hallucinated APIs that don't exist, no outdated code generation.

## �️ Installation

### Requirements

- Python >= 3.10
- VS Code, Cursor, Claude Desktop, or another MCP Client
- XenoDocs API Key (Get yours by creating an account at [xenodocs.com/dashboard](https://xenodocs.com/dashboard))

### Method 1: Using uv (Recommended)

```bash
uv add xenodocs-mcp-server
```

### Method 2: Using pip

```bash
pip install xenodocs-mcp-server
```

<details>
<summary><b>Install in VS Code</b></summary>

Add this to your VS Code MCP config file (`.vscode/mcp.json`). See [VS Code MCP docs](https://code.visualstudio.com/docs/copilot/chat/mcp-servers) for more info.

#### VS Code Local Server Connection

```json
{
  "servers": {
    "xenodocs-mcp-server": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "xenodocs-mcp-server"
      ],
      "env": {
        "XENODOCS_API_KEY": "YOUR_API_KEY"
      }
    }
  },
  "inputs": []
}
```

Alternative configurations:

**Using uv project:**
```json
{
  "servers": {
    "xenodocs-mcp-server": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "xenodocs-mcp-server"],
      "env": {
        "XENODOCS_API_KEY": "YOUR_API_KEY"
      }
    }
  },
  "inputs": []
}
```

**Using Python module:**
```json
{
  "servers": {
    "xenodocs-mcp-server": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "xenodocs_mcp_server.server"],
      "env": {
        "XENODOCS_API_KEY": "YOUR_API_KEY"
      }
    }
  },
  "inputs": []
}
```

</details>

<details>
<summary><b>Install in Cursor</b></summary>

Add to your Cursor MCP configuration (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "xenodocs": {
      "command": "uvx",
      "args": ["xenodocs-mcp-server"],
      "env": {
        "XENODOCS_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Install in Claude Desktop</b></summary>

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "xenodocs": {
      "command": "uvx",
      "args": ["xenodocs-mcp-server"],
      "env": {
        "XENODOCS_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Install in Windsurf</b></summary>

Add to your Windsurf MCP configuration:

```json
{
  "mcpServers": {
    "xenodocs": {
      "command": "uvx",
      "args": ["xenodocs-mcp-server"],
      "env": {
        "XENODOCS_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Install in Zed</b></summary>

Add to your Zed `settings.json`:

```json
{
  "context_servers": {
    "xenodocs": {
      "source": "custom",
      "command": "uvx",
      "args": ["xenodocs-mcp-server"],
      "env": {
        "XENODOCS_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

</details>

## 🔨 Available Tools

XenoDocs MCP provides the following tools that LLMs can use:

- `search_library_name`: Search for matching library names in the XenoDocs documentation database.
  - `library_name` (required): The name or partial name of the library to search for
  - `top_k` (optional): Maximum number of matching libraries to return (default: 3, max: 20)

- `search_library`: Search for specific information within a library's documentation.
  - `library_name` (required): The exact name of the library to search in
  - `query` (required): The search query describing what you're looking for

## 💻 Development

Clone the project and install dependencies:

```bash
git clone https://github.com/Xenodocs/xenodocs-mcp-server.git
cd xenodocs-mcp-server
uv sync
```

Set your API key:

```bash
export XENODOCS_API_KEY="your-api-key"
```

Run the server:

```bash
uv run xenodocs-mcp-server
```

### Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector uv run xenodocs-mcp-server
```

## 🚨 Troubleshooting

<details>
<summary><b>Command Not Found Errors</b></summary>

If you get "command not found" errors:

1. **For uv projects:** Make sure you're in a directory with a `pyproject.toml` file
2. **For pip installation:** Use the Python module method:
   ```json
   {
     "command": "python",
     "args": ["-m", "xenodocs_mcp_server.server"]
   }
   ```

</details>

<details>
<summary><b>API Key Not Found Error</b></summary>

If you see `WARNING: XENODOCS_API_KEY not set!`, make sure you've configured the API key in your MCP client configuration or as a system environment variable.

</details>

<details>
<summary><b>General MCP Client Errors</b></summary>

1. Restart your MCP client completely
2. Check that your installation method is working by running the command manually
3. Check client output/logs for MCP connection errors
4. Verify you have the correct Python version (>=3.10)

</details>

## 📄 License

MIT