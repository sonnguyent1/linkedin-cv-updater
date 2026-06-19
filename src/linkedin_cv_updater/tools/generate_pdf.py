import logging
from pydantic import BaseModel, Field
from playwright.sync_api import sync_playwright
import markdown
from linkedin_cv_updater.logger import get_logger
from linkedin_cv_updater.server import mcp
import os

logger = get_logger(__name__)

class GenerateCV(BaseModel):
    markdown_content: str = Field(..., description="The highly formatted, beautified markdown text for the CV.")
    output_filename: str = Field("beautified_cv.pdf", description="The local file path where the generated PDF will be saved.")

@mcp.tool()
def generate_beautiful_cv(params: GenerateCV) -> str:
    """
    Renders beautifully formatted markdown text into a sleek, professionally designed PDF CV using headless Chromium.
    
    IMPORTANT INSTRUCTIONS FOR AGENT:
    Call this tool after you have extracted or reviewed a raw CV and beautified the text in markdown format.
    Pass the finalized markdown string as `markdown_content`.
    """
    output_path = os.path.abspath(params.output_filename)
    logger.info(f"Generating Beautiful PDF CV at: {output_path}")

    # Convert markdown to HTML
    html_body = markdown.markdown(params.markdown_content, extensions=['tables', 'fenced_code'])

    # Wrap in premium CSS template
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --primary-color: #0f172a;
                --secondary-color: #334155;
                --accent-color: #2563eb;
                --bg-color: #ffffff;
                --text-color: #1e293b;
                --border-color: #e2e8f0;
            }}
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background-color: var(--bg-color);
                color: var(--text-color);
                line-height: 1.6;
                margin: 0;
                padding: 40px;
                font-size: 14px;
            }}
            h1 {{
                font-size: 32px;
                font-weight: 700;
                color: var(--primary-color);
                margin-bottom: 8px;
                letter-spacing: -0.02em;
            }}
            h2 {{
                font-size: 20px;
                font-weight: 600;
                color: var(--accent-color);
                margin-top: 32px;
                margin-bottom: 16px;
                border-bottom: 2px solid var(--border-color);
                padding-bottom: 8px;
            }}
            h3 {{
                font-size: 16px;
                font-weight: 600;
                color: var(--primary-color);
                margin-top: 24px;
                margin-bottom: 8px;
            }}
            p {{
                margin-top: 0;
                margin-bottom: 12px;
                color: var(--secondary-color);
            }}
            ul {{
                margin-top: 0;
                margin-bottom: 16px;
                padding-left: 20px;
                color: var(--secondary-color);
            }}
            li {{
                margin-bottom: 6px;
            }}
            a {{
                color: var(--accent-color);
                text-decoration: none;
            }}
            strong {{
                font-weight: 600;
                color: var(--primary-color);
            }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

    try:
        with sync_playwright() as p:
            # Launch headless browser specifically for PDF rendering
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Load the HTML content
            page.set_content(html_template, wait_until="networkidle")
            
            # Generate PDF
            page.pdf(
                path=output_path,
                format="A4",
                print_background=True,
                margin={"top": "20px", "right": "20px", "bottom": "20px", "left": "20px"}
            )
            
            browser.close()
            
        return f"✅ Successfully generated beautiful CV as a PDF! Saved to: {output_path}"

    except Exception as e:
        logger.error(f"Error generating PDF: {e}", exc_info=True)
        return f"❌ Failed to generate PDF. Details: {str(e)}"
