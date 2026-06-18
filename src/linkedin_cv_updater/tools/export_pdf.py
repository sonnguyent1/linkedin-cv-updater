import logging
from pydantic import BaseModel, Field
from linkedin_cv_updater.linkedin_client import LinkedinClient
from linkedin_cv_updater.logger import get_logger
from linkedin_cv_updater.server import mcp
import os

logger = get_logger(__name__)

class ExportPDF(BaseModel):
    output_filename: str = Field("linkedin_cv.pdf", description="The local file path where the PDF will be saved.")

@mcp.tool()
def export_linkedin_pdf(params: ExportPDF) -> str:
    """
    Exports the user's LinkedIn profile as a PDF CV using Playwright's download manager.
    
    CRITICAL PREREQUISITE:
    User must have Chrome running with --remote-debugging-port=9222.
    
    IMPORTANT INSTRUCTIONS FOR AGENT:
    Call this tool as the very last step after you have finished updating the user's LinkedIn Experience and About sections.
    This generates the final physical CV artifact for the user.
    """
    output_path = os.path.abspath(params.output_filename)
    logger.info(f"Exporting LinkedIn Profile PDF to: {output_path}")

    try:
        client = LinkedinClient()
        result = client.export_pdf(output_path)
        
        if result == "SUCCESS":
            return f"✅ Successfully exported your LinkedIn profile as a PDF! Saved to: {output_path}"
        else:
            return f"❌ Failed to export PDF.\n\nDetails:\n{result}"

    except Exception as e:
        logger.error(f"Error exporting PDF: {e}", exc_info=True)
        return f"Failed to run CDP client: {str(e)}"
