from fastmcp import FastMCP
from linkedin_cv_updater.linkedin_client import LinkedinClient
from linkedin_cv_updater.logger import get_logger
from linkedin_cv_updater.server import mcp

logger = get_logger(__name__)

@mcp.tool()
def get_linkedin_about() -> str:
    """
    Fetches the user's current LinkedIn About/Summary section by connecting to an active Chrome instance via CDP.
    
    CRITICAL PREREQUISITE:
    User must have Chrome running with --remote-debugging-port=9222.
    If this tool returns an error about failing to connect, instruct the user to run the `scripts/start_chrome.sh` script.
    """
    logger.info("Fetching About section via CDP...")

    try:
        client = LinkedinClient()
        result = client.get_about()
        return result

    except Exception as e:
        logger.error(f"Error fetching about section: {e}", exc_info=True)
        return f"Failed to run CDP client: {str(e)}"
