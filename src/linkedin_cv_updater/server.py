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
import linkedin_cv_updater.tools.export_pdf
import linkedin_cv_updater.tools.generate_pdf

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

@mcp.prompt()
def extract_company_name() -> str:
    """
    Instructs the AI Agent to act as an expert repository auditor and identify the specific organization, client, or company name associated with the project.
    """
    return """
Act as an expert repository auditor. Analyze the files in this project to identify the specific organization, client, or company name associated with it. 

To maximize efficiency, prioritize scanning these high-leverage locations sequentially:

1. Root Legal & Documentation: Inspect the 'LICENSE', 'NOTICE', or 'README.md' files for copyright ownership lines.
2. Package & Dependency Configurations: Look at 'package.json' (author, repo, scoped package names), 'pom.xml' or 'build.gradle' (groupId domains), 'go.mod' (module paths), or 'pyproject.toml'.
3. Git Metadata: Check '.git/config' or remote origin URLs, and inspect recent commit logs for contributor email domains (e.g., user@company.com).
4. Environment & Deployment: Review '.env.example' or CI/CD workflows (.github/workflows, .gitlab-ci.yml) for specific staging subdomains, Docker registry targets, or cloud project IDs.
5. Frontend Localization: Scan 'i18n', 'locales', or 'strings.xml' files for customer-facing text containing "Terms of Service", "Privacy Policy", or the brand name.

Provide your findings in the following format:
- Identified Organization: [Name or Best Guess]
- Confidence Score: [Low / Medium / High]
- Supporting Evidence: [List the exact file paths and the specific lines of text/code discovered]
"""

@mcp.prompt()
def beautify_cv() -> str:
    """
    Instructs the AI Agent to process a raw CV (from a PDF or text source) and output a highly optimized, beautifully formatted Markdown string ready for PDF generation.
    """
    return """
Your task is to take the user's raw LinkedIn profile data and restructure it into a beautiful, highly readable Markdown format.

To execute this workflow, follow these exact steps in order:
1. Call the `export_linkedin_pdf` tool to download the user's current LinkedIn profile as a PDF to the local disk.
2. Read the downloaded PDF file to extract the raw text content.
3. Restructure the raw text into optimized Markdown using the Formatting Rules below.
4. Pass the finalized Markdown string directly into the `generate_beautiful_cv` tool to render the physical PDF!

FORMATTING RULES:
1. **Typography**: Use standard Markdown headings (# Name, ## Experience, ### Role) to create a clean visual hierarchy.
2. **Impact**: Rewrite passive descriptions into active, impact-driven bullet points starting with strong action verbs.
3. **Brevity**: Keep the profile summary concise and engaging (3-4 sentences max).
4. **Highlights**: Bold key metrics, technologies, or achievements (e.g., "**Reduced latency by 45%** using **Go**").
5. **Structure**: Ensure sections like "Profile", "Experience", "Education", and "Skills" are clearly demarcated.
"""
