import sys
from linkedin_cv_updater.server import mcp

def main():
    """Entry point for the MCP server."""
    # Run the server on standard input/output
    # We suppress the banner because it breaks JSON-RPC over stdio
    mcp.run(transport="stdio", show_banner=False)

if __name__ == "__main__":
    main()
