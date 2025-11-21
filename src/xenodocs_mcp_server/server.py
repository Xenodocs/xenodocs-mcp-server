import os
import sys
import httpx
from fastmcp import FastMCP

mcp = FastMCP("xenodocs")

# ============================================================================
# CONFIGURATION
# ============================================================================

def get_config():
    """Get configuration from environment variables"""
    api_url = os.getenv("XENODOCS_API_URL", "https://api.xenodocs.org")
    api_key = os.getenv("XENODOCS_API_KEY", "")
    
    if not api_key:
        print("WARNING: XENODOCS_API_KEY not set!", file=sys.stderr)
    
    return {
        "api_url": api_url,
        "api_key": api_key,
        "timeout": 30
    }

config = get_config()

# ============================================================================
# API CLIENT
# ============================================================================

class XenoDocsAPIClient:
    """Client for XenoDocs backend APIs"""

    def __init__(self, api_url: str, api_key: str, timeout: int = 30):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
            }

    async def _make_request(self, endpoint: str, data: dict) -> dict:
        """Make POST request to XenoDocs API"""
        url = f"{self.api_url}{endpoint}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, headers=self.headers, json=data)
                response.raise_for_status()
                return response.json()

        except httpx.ConnectError:
            return {"success": False, "error": f"Cannot connect to {self.api_url}"}
        except httpx.TimeoutException:
            return {"success": False, "error": "Request timeout"}
        except httpx.HTTPStatusError as e:
            try:
                error_data = e.response.json()
                return {"success": False, "error": error_data.get("error", str(e))}
            except:
                return {"success": False, "error": f"HTTP {e.response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def search_library_name(self, library_name: str, query: str) -> dict:
        """Search for library using AI-powered selection"""
        if not library_name or not library_name.strip():
            return {"success": False, "error": "library_name cannot be empty"}

        if not query or not query.strip():
            return {"success": False, "error": "query cannot be empty"}

        return await self._make_request(
            "/mcp/search-library-name/",
            {"library_name": library_name.strip(), "query": query.strip()}
        )

    async def search_documentation(self, library_name: str, query: str) -> dict:
        """Search library documentation"""
        if not library_name or not library_name.strip():
            return {"success": False, "error": "library_name cannot be empty"}

        if not query or not query.strip():
            return {"success": False, "error": "query cannot be empty"}

        return await self._make_request(
            "/mcp/search-library-docs/",
            {"library_name": library_name.strip(), "query": query.strip(), "top_k": 25}
        )


api_client = XenoDocsAPIClient(
    api_url=config["api_url"],
    api_key=config["api_key"],
    timeout=config["timeout"]
)

# ============================================================================
# MCP TOOLS
# ============================================================================

@mcp.tool()
async def search_library_name(library_name: str, query: str) -> str:
    """
    CRITICAL: Always use this tool FIRST before generating code for any third-party library.
    
    This tool identifies the correct library version and official documentation source.
    Using this prevents hallucinations and ensures you use the most up-to-date APIs.
    
    Usage Strategy:
    1. Call this tool to find the exact library name (e.g., mapping "langchain" to the specific package).
    2. Use the result from this tool to call 'search_latest_documentation'.
    
    Args:
        library_name: The general name of the library (e.g., "langchain", "pydantic", "nextjs").
        query: Specific requirements or version constraints (e.g., "v2 with server actions", "latest stable").
    
    Returns:
        JSON containing the canonical library name and version details.
    """
    result = await api_client.search_library_name(library_name, query)
    return str(result)


@mcp.tool()
async def search_latest_documentation(library_name: str, query: str) -> str:
    """
    Retrieve official, up-to-date code examples and API references for a library.
    
    Use this tool to find the exact syntax, function signatures, and usage patterns.
    Do not rely on your internal training data as it may be outdated; always verify with this tool.
    
    Args:
        library_name: The exact library name returned by the 'search_library_name' tool.
        query: A natural language question about what you need (e.g., "how to create a chain", "authentication middleware example").
    
    Returns:
        JSON string containing relevant documentation snippets and code examples.
    """
    result = await api_client.search_documentation(library_name, query)
    return str(result)


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point for XenoDocs MCP server"""
    print("=" * 60, file=sys.stderr)
    print("XenoDocs MCP Server", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print(f"API: {config['api_url']}", file=sys.stderr)
    print(f"Key: {'✓' if config['api_key'] else '✗ NOT SET'}", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
