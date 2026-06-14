import sys
from linkedin_cv_updater.server import mcp

def main():
    """Entry point for the MCP server."""
    # Run the server on standard input/output
    mcp.run()

if __name__ == "__main__":
    main()
