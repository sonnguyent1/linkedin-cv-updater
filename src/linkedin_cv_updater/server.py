from fastmcp import FastMCP
import os
from linkedin_cv_updater.logger import get_logger

logger = get_logger(__name__)

# Initialize the FastMCP server
mcp = FastMCP("linkedin-cv-updater")

# Import tools so they are registered with the server
import linkedin_cv_updater.tools.update_experience
import linkedin_cv_updater.tools.update_about
import linkedin_cv_updater.tools.get_about

@mcp.prompt()
def format_linkedin_content(role_description: str = None, about_summary: str = None) -> str:
    """
    A prompt template to help Agents beautifully format raw LinkedIn content before updating the profile.
    """
    prompt = "Please reformat the following text for a professional LinkedIn profile.\n\n"
    if role_description:
        prompt += f"ROLE DESCRIPTION:\n{role_description}\n\n"
        prompt += "FORMATTING RULES for ROLE:\n"
        prompt += "1. Extract key achievements and metrics.\n"
        prompt += "2. Format as a bulleted list starting with strong action verbs.\n"
        prompt += "3. Do not use dense paragraphs.\n\n"
        
    if about_summary:
        prompt += f"ABOUT SUMMARY:\n{about_summary}\n\n"
        prompt += "FORMATTING RULES for ABOUT:\n"
        prompt += "1. Write an engaging, multi-paragraph professional summary.\n"
        prompt += "2. Highlight core skills, passions, and top achievements.\n"
        prompt += "3. Use spacing to make it highly readable.\n"
        
    return prompt

@mcp.prompt()
def extract_project_highlights(project_path: str = ".") -> str:
    """
    Instructs the AI Agent to scan the given project path and extract the most impactful, metric-driven highlights for LinkedIn.
    """
    return f"""
Please analyze the project located at '{project_path}'.
Use your tools to read the README, view architecture diagrams, and scan key configuration files (e.g., package.json, pyproject.toml, docker-compose.yml).

Your goal is to extract the top highlights for a LinkedIn Experience section.

FORMATTING RULES:
1. Synthesize the technical challenges, the stack used, and the business impact.
2. Quantify achievements with metrics where possible (e.g., "Reduced latency by X%", "Led a team of Y").
3. Output the final result as a concise, bulleted list.
4. Each bullet point MUST start with a strong action verb.
"""
