import os
import sys
import httpx
import asyncio
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("xenodocs")

# ============================================================================
# CONFIGURATION
# ============================================================================

def get_config():
    """
    Get configuration from environment variables.
    These can be set in VS Code's settings.json or mcp.json config.
    """
    api_url = os.getenv("XENODOCS_API_URL", "https://backend.xenodocs.com")
    api_key = os.getenv("XENODOCS_API_KEY", "")
    
    if not api_key:
        print("WARNING: XENODOCS_API_KEY not set!", file=sys.stderr)
        print("Please configure it in your MCP client settings.", file=sys.stderr)
    
    return {
        "api_url": api_url,
        "api_key": api_key,
        "timeout": 30
    }

config = get_config()

# ============================================================================
# DJANGO API CLIENT
# ============================================================================

class XenoDocsAPIClient:
    """Client for communicating with XenoDocs backend APIs"""

    def __init__(self, api_url: str, api_key: str, timeout: int = 30):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def _make_request(self, endpoint: str, data: dict) -> dict:
        """Make POST request to XenoDocs API with error handling"""
        url = f"{self.api_url}{endpoint}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=data
                )
                response.raise_for_status()
                return response.json()

        except httpx.ConnectError:
            return {
                "status": "error",
                "message": f"Cannot connect to XenoDocs at {self.api_url}. Please check your connection."
            }
        except httpx.TimeoutException:
            return {
                "status": "error",
                "message": "Request timeout - server took too long to respond"
            }
        except httpx.HTTPStatusError as e:
            try:
                error_data = e.response.json()
                return {
                    "status": "error",
                    "message": error_data.get("error", str(e))
                }
            except:
                return {
                    "status": "error",
                    "message": f"HTTP {e.response.status_code}: {str(e)}"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }

    async def search_library_name(self, query: str, top_k: int = 3) -> dict:
        """Search for matching library names via XenoDocs API"""
        if not query or not query.strip():
            return {
                "status": "error",
                "message": "Query cannot be empty",
                "matches": []
            }

        top_k = max(1, min(20, int(top_k)))

        result = await self._make_request(
            "/mcp/search-library-name/",
            {
                "library_name": query.strip(),
                "top_k": top_k
            }
        )

        return result

    async def search_documentation(self, library_name: str, query: str) -> dict:
        """Search library documentation via XenoDocs API"""
        if not library_name or not library_name.strip():
            return {
                "status": "error",
                "context": "Library name cannot be empty"
            }

        if not query or not query.strip():
            return {
                "status": "error",
                "context": "Query cannot be empty"
            }

        result = await self._make_request(
            "/mcp/search-library-docs/",
            {
                "library_name": library_name.strip(),
                "query": query.strip(),
                "top_k": 25
            }
        )

        # Simplify response for MCP tool
        if result.get("status") == "success":
            return {
                "context": result.get("context", ""),
                "chunks_found": result.get("chunks_found", 0)
            }
        else:
            return {
                "context": f"Error: {result.get('message', 'Unknown error')}"
            }

# Initialize API client
api_client = XenoDocsAPIClient(
    api_url=config["api_url"],
    api_key=config["api_key"],
    timeout=config["timeout"]
)

# ============================================================================
# MCP TOOLS
# ============================================================================

@mcp.tool()
async def search_library_name(library_name: str, top_k: int = 3) -> str:
    """
    Search for matching library names in the XenoDocs documentation database.

    Args:
        library_name: The name or partial name of the library to search for
        top_k: Maximum number of matching libraries to return (default: 3, max: 20)

    Returns:
        JSON string with matching library names and their details
    """
    result = await api_client.search_library_name(library_name, top_k)
    return str(result)

@mcp.tool()
async def search_library(library_name: str, query: str) -> str:
    """
    Search for specific information within a library's documentation.

    Args:
        library_name: The exact name of the library to search in
        query: The search query describing what you're looking for

    Returns:
        JSON string with relevant documentation context
    """
    result = await api_client.search_documentation(library_name, query)
    return str(result)

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point for the MCP server"""
    print("=" * 60, file=sys.stderr)
    print("Starting XenoDocs MCP Server", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print(f"API URL: {config['api_url']}", file=sys.stderr)
    print(f"API Key: {'✓ Configured' if config['api_key'] else '✗ NOT SET'}", file=sys.stderr)
    
    if not config['api_key']:
        print("\n⚠️  WARNING: XENODOCS_API_KEY not set!", file=sys.stderr)
        print("Configure it in your MCP client settings (see README)", file=sys.stderr)
    
    print("=" * 60, file=sys.stderr)
    print("Transport: stdio (VS Code/Claude Desktop compatible)", file=sys.stderr)
    print("=" * 60, file=sys.stderr)

    # Use stdio transport for MCP clients
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()