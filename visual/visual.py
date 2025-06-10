# Imports
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("visual")
USER_AGENT = "visual-fastmcp/0.1"

# Define get_code function
async def get_code(url: str) -> str:
    """Fetch the source code of a webpage.

    Args:
        url: The URL of the webpage to fetch.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html"
    }
    async with httpx.AsyncClient() as client:
        try:
            raw_url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            response = await client.get(raw_url, headers=headers, timeout=30.0)
            response.raise_for_status()
            # code_component = extract_code(response.text) 
            code_component = response.text
            return code_component
        except httpx.RequestError as e:
            return f"Request error: {e}"
        except httpx.HTTPStatusError as e:
            return f"HTTP error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

# Create visualize_code tool
@mcp.tool()
async def visualize_code(url: str) -> str:

    """Visualize the code extracted from a Github repository URL in the format of SVG code.

    Args:
        url: The GitHub repository URL
    
    Returns:
        SVG code that visualizes the code structure or hierarchy.
    """

    code = await get_code(url)
    if "error" in code.lower():
        return code
    else:
        return "\n---\n".join(code)


# Run the server
if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

