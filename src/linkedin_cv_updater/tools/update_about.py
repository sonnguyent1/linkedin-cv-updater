import logging
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from linkedin_cv_updater.linkedin_client import LinkedinClient
from linkedin_cv_updater.logger import get_logger
from linkedin_cv_updater.server import mcp

logger = get_logger(__name__)

class AboutUpdate(BaseModel):
    summary: str = Field(description="The new summary/about text for the LinkedIn profile. MUST be an engaging, professional summary highlighting core skills, passions, and top achievements. Break into beautifully formatted paragraphs.")

@mcp.tool()
def update_linkedin_about(about: AboutUpdate) -> str:
    """
    Updates the user's LinkedIn About/Summary section by connecting to an active Chrome instance via CDP.
    
    CRITICAL PREREQUISITE:
    User must have Chrome running with --remote-debugging-port=9222.
    If this tool returns an error about failing to connect, instruct the user to run the `scripts/start_chrome.sh` script provided in this repository.
    
    IMPORTANT INSTRUCTIONS FOR AGENT:
    1. BEFORE calling this tool, you MUST call the `get_linkedin_about` tool to fetch the user's current summary.
    2. Analyze the user's local project or codebase to extract new achievements.
    3. Synthesize the existing ideas with the new project highlights. Do not blindly overwrite the old summary; preserve the core messaging while adding the new highlights.
    4. When generating the `summary` string, write an engaging, multi-paragraph professional summary.
    5. Highlight the user's core skills, top achievements, and professional passions.
    6. Do NOT write a dense block of text. Use spacing and structure to make it highly readable and beautiful.
    """
    logger.info("Updating About section via CDP...")

    try:
        client = LinkedinClient()
        result = client.update_about(summary=about.summary)
        
        if result == "SUCCESS":
            return "✅ Successfully updated your LinkedIn About section!"
        else:
            return f"❌ Failed to update profile.\n\nDetails:\n{result}"

    except Exception as e:
        logger.error(f"Error updating about section: {e}", exc_info=True)
        return f"Failed to run CDP client: {str(e)}"
