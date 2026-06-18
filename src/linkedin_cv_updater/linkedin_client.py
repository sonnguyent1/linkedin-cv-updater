import logging
import os
from typing import Optional
from playwright.sync_api import sync_playwright
from linkedin_cv_updater.logger import get_logger

logger = get_logger(__name__)

class LinkedinClient:
    """
    Client for automating LinkedIn profile updates via Chrome DevTools Protocol (CDP).
    Connects to an already-running Chrome instance to perform UI automation.
    """

    def __init__(self, cdp_url: str = "http://127.0.0.1:9222"):
        self.cdp_url = cdp_url

    def _get_or_create_linkedin_page(self, browser) -> "Page":
        linkedin_page = None
        for context in browser.contexts:
            for page in context.pages:
                if "linkedin.com" in page.url:
                    linkedin_page = page
                    break
            if linkedin_page:
                break
                
        if not linkedin_page:
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            linkedin_page = context.new_page()
            
        return linkedin_page

    def add_experience(
        self,
        title: str,
        company_name: str,
        start_month: int,
        start_year: int,
        end_month: Optional[int] = None,
        end_year: Optional[int] = None,
        description: str = "",
        location: str = "",
    ) -> str:
        logger.info(f"Connecting to Chrome via CDP at {self.cdp_url}")

        with sync_playwright() as p:
            try:
                browser = p.chromium.connect_over_cdp(self.cdp_url)
                
                linkedin_page = self._get_or_create_linkedin_page(browser)

                # Navigate to the experience details page
                profile_id = os.getenv("LINKEDIN_PROFILE_ID", "me")
                logger.info(f"Navigating to LinkedIn Experience page for {profile_id}...")
                linkedin_page.goto(f"https://www.linkedin.com/in/{profile_id}/details/experience/", wait_until="domcontentloaded")
                linkedin_page.wait_for_timeout(3000)

                # Click the + (Add experience) button
                logger.info("Clicking Add Experience button...")
                add_button = linkedin_page.locator("a[href*='edit/forms/position/new']").first
                if not add_button.is_visible():
                    add_button = linkedin_page.get_by_label("Add a position or career break").first
                
                if add_button.is_visible():
                    add_button.click()
                    linkedin_page.wait_for_timeout(1000)
                else:
                    return "ERROR: Could not find the 'Add a position' button."

                # If the menu drops down (Add role vs Add career break)
                add_role_menu = linkedin_page.get_by_text("Add role").first
                if add_role_menu.is_visible():
                    add_role_menu.click()

                linkedin_page.wait_for_timeout(2000)

                # Fill out the form fields
                logger.info("Filling out form fields...")
                
                # Title
                title_input = linkedin_page.get_by_role("combobox", name="Title").first
                if not title_input.is_visible():
                    title_input = linkedin_page.get_by_label("Title").first
                
                title_input.fill(title)
                linkedin_page.wait_for_timeout(1000)
                linkedin_page.keyboard.press("Escape") # Close autocomplete dropdown
                
                # Company Name
                company_input = linkedin_page.get_by_role("combobox", name="Company").first
                if not company_input.is_visible():
                    company_input = linkedin_page.get_by_label("Company or organization").first
                if not company_input.is_visible():
                    company_input = linkedin_page.get_by_label("Company name").first
                
                if company_input.is_visible():
                    company_input.fill(company_name)
                    linkedin_page.wait_for_timeout(1500)
                    linkedin_page.keyboard.press("ArrowDown")
                    linkedin_page.wait_for_timeout(500)
                    linkedin_page.keyboard.press("Enter")
                    linkedin_page.wait_for_timeout(500)
                
                # Employment Type
                emp_type = linkedin_page.get_by_label("Employment type").first
                if emp_type.is_visible():
                    # 12 is Full-time
                    emp_type.select_option(value="12")
                    linkedin_page.wait_for_timeout(500)

                # Start Date
                month_select = linkedin_page.get_by_label("Start date month").locator("select").first
                if not month_select.is_visible():
                    month_select = linkedin_page.get_by_label("Month").first
                if month_select.is_visible():
                    month_select.select_option(value=str(start_month))

                year_select = linkedin_page.get_by_label("Start date year").locator("select").first
                if not year_select.is_visible():
                    year_select = linkedin_page.get_by_label("Year").first
                if year_select.is_visible():
                    year_select.select_option(value=str(start_year))
                
                # Description
                desc_input = linkedin_page.get_by_role("textbox", name="Description").first
                if not desc_input.is_visible():
                     desc_input = linkedin_page.get_by_label("Description").first
                     
                if desc_input.is_visible():
                    desc_input.click()
                    linkedin_page.wait_for_timeout(500)
                    linkedin_page.keyboard.type(description)
                    
                # Save
                logger.info("Clicking Save...")
                save_btn = linkedin_page.get_by_role("button", name="Save").first
                if save_btn.is_visible():
                    save_btn.click()
                    linkedin_page.wait_for_timeout(3000)
                    return "SUCCESS"
                else:
                    return "ERROR: Could not find the Save button."

            except Exception as e:
                logger.error(f"CDP UI Automation failed: {e}")
                return f"ERROR: Automation failed. Details: {e}"

    def get_about(self) -> str:
        logger.info(f"Connecting to Chrome via CDP at {self.cdp_url} to fetch About section")

        with sync_playwright() as p:
            try:
                browser = p.chromium.connect_over_cdp(self.cdp_url)
                linkedin_page = self._get_or_create_linkedin_page(browser)

                profile_id = os.getenv("LINKEDIN_PROFILE_ID", "me")
                logger.info(f"Navigating to LinkedIn Profile page for {profile_id}...")
                linkedin_page.goto(f"https://www.linkedin.com/in/{profile_id}/", wait_until="domcontentloaded")
                linkedin_page.wait_for_timeout(4000)

                linkedin_page.mouse.wheel(0, 1000)
                linkedin_page.wait_for_timeout(2000)

                logger.info("Clicking Edit About button...")
                edit_btn = linkedin_page.locator("a[aria-label*='Edit about'], a[aria-label*='Edit About'], button[aria-label*='Edit about']").first
                if edit_btn.is_visible():
                    edit_btn.click()
                    linkedin_page.wait_for_timeout(3000)
                else:
                    return "ERROR: Could not find the 'Edit about' button. Ensure you have an About section."

                logger.info("Extracting current summary...")
                summary_text = ""
                summary_input = linkedin_page.locator("textarea").first
                if summary_input.is_visible():
                    summary_text = summary_input.input_value()
                else:
                    # Tiptap fallback
                    desc_input = linkedin_page.locator("div[role='textbox'].tiptap").first
                    if not desc_input.is_visible():
                        desc_input = linkedin_page.get_by_role("textbox").first
                        
                    if desc_input.is_visible():
                        summary_text = desc_input.inner_text()
                    else:
                        return "ERROR: Could not find the summary input field."

                # Close the modal
                close_btn = linkedin_page.locator("button[aria-label='Dismiss']").first
                if close_btn.is_visible():
                    close_btn.click()
                    linkedin_page.wait_for_timeout(1000)

                # Confirm discard if prompted
                discard_btn = linkedin_page.locator("button:has-text('Discard')").first
                if discard_btn.is_visible():
                    discard_btn.click()
                    linkedin_page.wait_for_timeout(1000)

                return summary_text

            except Exception as e:
                logger.error(f"CDP UI Automation failed while fetching about: {e}")
                return f"ERROR: Automation failed. Details: {e}"

    def update_about(self, summary: str) -> str:
        logger.info(f"Connecting to Chrome via CDP at {self.cdp_url}")

        with sync_playwright() as p:
            try:
                browser = p.chromium.connect_over_cdp(self.cdp_url)
                
                linkedin_page = self._get_or_create_linkedin_page(browser)

                # Navigate to the profile page
                profile_id = os.getenv("LINKEDIN_PROFILE_ID", "me")
                logger.info(f"Navigating to LinkedIn Profile page for {profile_id}...")
                linkedin_page.goto(f"https://www.linkedin.com/in/{profile_id}/", wait_until="domcontentloaded")
                linkedin_page.wait_for_timeout(4000)

                # Scroll down to ensure About section loads
                linkedin_page.mouse.wheel(0, 1000)
                linkedin_page.wait_for_timeout(2000)

                # Click the Edit about button
                logger.info("Clicking Edit About button...")
                edit_btn = linkedin_page.locator("a[aria-label*='Edit about'], a[aria-label*='Edit About'], button[aria-label*='Edit about']").first
                if edit_btn.is_visible():
                    edit_btn.click()
                    linkedin_page.wait_for_timeout(3000)
                else:
                    return "ERROR: Could not find the 'Edit about' button on the profile page. Please ensure you have an About section."

                # Fill out the summary
                logger.info("Filling out summary...")
                # The about section might be a textarea or a Tiptap editor
                summary_input = linkedin_page.locator("textarea").first
                if summary_input.is_visible():
                    summary_input.click()
                    linkedin_page.wait_for_timeout(500)
                    summary_input.fill(summary)
                    linkedin_page.wait_for_timeout(1000)
                else:
                    # Tiptap fallback
                    desc_input = linkedin_page.locator("div[role='textbox'].tiptap").first
                    if not desc_input.is_visible():
                        desc_input = linkedin_page.get_by_role("textbox").first
                        
                    if desc_input.is_visible():
                        desc_input.click()
                        linkedin_page.wait_for_timeout(500)
                        linkedin_page.keyboard.press("Meta+A")
                        linkedin_page.wait_for_timeout(200)
                        linkedin_page.keyboard.press("Backspace")
                        linkedin_page.wait_for_timeout(200)
                        linkedin_page.keyboard.type(summary)
                    else:
                        return "ERROR: Could not find the summary input field."

                # Save
                logger.info("Clicking Save...")
                try:
                    save_btn = linkedin_page.locator("button:has-text('Save'):visible").first
                    save_btn.click()
                    linkedin_page.wait_for_timeout(3000)
                    return "SUCCESS"
                except Exception as e:
                    return f"ERROR: Could not find the Save button. Details: {e}"

            except Exception as e:
                logger.error(f"CDP UI Automation failed: {e}")
                return f"ERROR: Automation failed. Details: {e}"

    def export_pdf(self, output_filename: str) -> str:
        logger.info(f"Connecting to Chrome via CDP at {self.cdp_url} to export PDF")

        with sync_playwright() as p:
            try:
                browser = p.chromium.connect_over_cdp(self.cdp_url)
                linkedin_page = self._get_or_create_linkedin_page(browser)

                # Navigate to the profile page
                profile_id = os.getenv("LINKEDIN_PROFILE_ID", "me")
                logger.info(f"Navigating to LinkedIn Profile page for {profile_id}...")
                linkedin_page.goto(f"https://www.linkedin.com/in/{profile_id}/", wait_until="domcontentloaded")
                linkedin_page.wait_for_timeout(4000)

                # Scroll to the top of the page to avoid sticky notification headers overlapping the buttons
                logger.info("Scrolling to top of the page...")
                linkedin_page.evaluate("window.scrollTo(0, 0)")
                linkedin_page.wait_for_timeout(1000)

                # Click the More button natively via JS to completely bypass any sticky headers or scrolling issues
                logger.info("Clicking 'More' button...")
                more_btn = linkedin_page.locator("button[aria-label='More']").first
                if more_btn.is_visible():
                    more_btn.evaluate("node => node.click()")
                    linkedin_page.wait_for_timeout(2000)
                else:
                    return "ERROR: Could not find the 'More' button."

                # Intercept the download and click Save to PDF
                logger.info("Clicking 'Save to PDF' and waiting for download...")
                with linkedin_page.expect_download(timeout=30000) as download_info:
                    save_pdf_btn = linkedin_page.locator("div[role='menuitem'], div[data-tabindex='0']").filter(has_text="Save to PDF").first
                    if not save_pdf_btn.is_visible():
                         save_pdf_btn = linkedin_page.get_by_text("Save to PDF").first
                         
                    if save_pdf_btn.is_visible():
                        save_pdf_btn.evaluate("node => node.click()")
                    else:
                        return "ERROR: Could not find 'Save to PDF' option."

                download = download_info.value
                download.save_as(output_filename)
                logger.info(f"PDF successfully saved to {output_filename}")
                return "SUCCESS"

            except Exception as e:
                logger.error(f"CDP UI Automation failed while exporting PDF: {e}")
                return f"ERROR: Automation failed. Details: {e}"
