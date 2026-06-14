import logging
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional
from linkedin_cv_updater.linkedin_client import LinkedinClient
from linkedin_cv_updater.logger import get_logger
from linkedin_cv_updater.server import mcp

logger = get_logger(__name__)

class ExperienceUpdate(BaseModel):
    title: str = Field(description="Job title (e.g., 'Senior Software Engineer')")
    company_name: str = Field(description="Name of the company")
    start_month: int = Field(description="Start month (1-12)")
    start_year: int = Field(description="Start year (e.g., 2021)")
    end_month: Optional[int] = Field(None, description="End month (1-12), null if current")
    end_year: Optional[int] = Field(None, description="End year (e.g., 2024), null if current")
    description: str = Field("", description="Detailed description of the role. MUST use concise, metric-driven bullet points (e.g., '- Led a 3-dev squad...', '- Migrated legacy apps...'). Start each bullet with a strong action verb.")
    location: str = Field("", description="Location of the job")

@mcp.tool()
def update_linkedin_experience(experience: ExperienceUpdate) -> str:
    """
    Updates the user's LinkedIn experience by connecting to an active Chrome instance via CDP.
    
    CRITICAL PREREQUISITE:
    User must have Chrome running with --remote-debugging-port=9222.
    If this tool returns an error about failing to connect, instruct the user to run the `scripts/start_chrome.sh` script provided in this repository.
    
    IMPORTANT INSTRUCTIONS FOR AGENT:
    1. BEFORE calling this tool, you SHOULD analyze the user's local project or codebase to extract achievements.
    2. Consider using the `extract_project_highlights` prompt to help you synthesize technical achievements.
    3. When generating the `description` string, ALWAYS use bullet points. 
    4. Never use dense paragraphs. Quantify achievements with metrics where possible, and start each bullet with a strong action verb.
    Separate bullets with newlines.
    """
    logger.info(f"Adding experience via CDP: {experience.title} at {experience.company_name}")

    try:
        client = LinkedinClient()
        result = client.add_experience(
            title=experience.title,
            company_name=experience.company_name,
            start_month=experience.start_month,
            start_year=experience.start_year,
            end_month=experience.end_month,
            end_year=experience.end_year,
            description=experience.description,
            location=experience.location,
        )
        
        if result == "SUCCESS":
            return f"✅ Successfully added '{experience.title}' at '{experience.company_name}' to your LinkedIn profile!"
        else:
            return f"❌ Failed to update profile.\n\nDetails:\n{result}"

    except Exception as e:
        logger.error(f"Error updating experience: {e}", exc_info=True)
        return f"Failed to run CDP client: {str(e)}"
