import pytest
from linkedin_cv_updater.linkedin_client import LinkedinClient
import os

def test_add_experience_success(mocker):
    # Mock playwright.sync_api.sync_playwright
    mock_sync_playwright = mocker.patch("linkedin_cv_updater.linkedin_client.sync_playwright")
    
    # Setup mock hierarchy: sync_playwright -> p -> chromium -> browser -> context -> page
    mock_p = mock_sync_playwright.return_value.__enter__.return_value
    mock_browser = mock_p.chromium.connect_over_cdp.return_value
    mock_context = mocker.Mock()
    mock_context.pages = []
    mock_browser.contexts = [mock_context]
    mock_page = mock_context.new_page.return_value
    
    # Mock the locators and their methods
    mock_locator = mocker.MagicMock()
    mock_locator.is_visible.return_value = True
    mock_locator.all.return_value = [mock_locator]
    mock_page.get_by_role.return_value = mock_locator
    mock_page.get_by_label.return_value = mock_locator
    mock_page.get_by_text.return_value = mock_locator
    mock_page.locator.return_value = mock_locator
    type(mock_locator).first = mocker.PropertyMock(return_value=mock_locator)
    
    # Instantiate client and call add_experience
    client = LinkedinClient()
    result = client.add_experience(
        title="Software Engineer",
        company_name="Tech Corp",
        start_month=5,
        start_year=2020,
        end_month=None,
        end_year=None,
        description="- Built things",
        location="NY"
    )
    
    assert result == "SUCCESS"
    
    # Verify the page navigated to the correct URL
    mock_page.goto.assert_any_call("https://www.linkedin.com/in/me/details/experience/", wait_until="domcontentloaded")
    
    # Verify fill was called (title, company, etc.)
    assert mock_locator.fill.called

def test_update_about_success(mocker):
    mock_sync_playwright = mocker.patch("linkedin_cv_updater.linkedin_client.sync_playwright")
    
    mock_p = mock_sync_playwright.return_value.__enter__.return_value
    mock_browser = mock_p.chromium.connect_over_cdp.return_value
    mock_context = mocker.Mock()
    mock_context.pages = []
    mock_browser.contexts = [mock_context]
    mock_page = mock_context.new_page.return_value
    
    # Setup locators
    mock_locator = mocker.MagicMock()
    mock_locator.is_visible.return_value = True
    mock_locator.filter.return_value = mock_locator
    mock_locator.all.return_value = [mock_locator]
    mock_page.locator.return_value = mock_locator
    mock_page.get_by_role.return_value = mock_locator
    type(mock_locator).first = mocker.PropertyMock(return_value=mock_locator)
    
    client = LinkedinClient()
    
    # Patch environment for PROFILE_ID
    mocker.patch.dict(os.environ, {"LINKEDIN_PROFILE_ID": "test_user"})
    
    result = client.update_about(summary="New Summary")
    
    assert result == "SUCCESS"
    
    # Verify navigation to the profile page
    mock_page.goto.assert_any_call("https://www.linkedin.com/in/test_user/", wait_until="domcontentloaded")
    
    # Verify the summary was filled
    mock_locator.fill.assert_called_with("New Summary")

def test_add_experience_exception(mocker):
    mock_sync_playwright = mocker.patch("linkedin_cv_updater.linkedin_client.sync_playwright")
    mock_p = mock_sync_playwright.return_value.__enter__.return_value
    mock_p.chromium.connect_over_cdp.side_effect = Exception("CDP Error")
    client = LinkedinClient()
    result = client.add_experience(title="T", company_name="C", start_month=1, start_year=2020, description="D", end_month=None, end_year=None, location="L")
    assert "ERROR: Automation failed" in result

def test_update_about_exception(mocker):
    mock_sync_playwright = mocker.patch("linkedin_cv_updater.linkedin_client.sync_playwright")
    mock_p = mock_sync_playwright.return_value.__enter__.return_value
    mock_p.chromium.connect_over_cdp.side_effect = Exception("CDP Error")
    mocker.patch.dict("os.environ", {"LINKEDIN_PROFILE_ID": "test_user"})
    client = LinkedinClient()
    result = client.update_about(summary="S")
    assert "ERROR: Automation failed" in result

def test_get_about_success(mocker):
    mock_sync_playwright = mocker.patch("linkedin_cv_updater.linkedin_client.sync_playwright")
    
    mock_p = mock_sync_playwright.return_value.__enter__.return_value
    mock_browser = mock_p.chromium.connect_over_cdp.return_value
    mock_context = mocker.Mock()
    mock_context.pages = []
    mock_browser.contexts = [mock_context]
    mock_page = mock_context.new_page.return_value
    
    # Setup locators
    mock_locator = mocker.MagicMock()
    mock_locator.is_visible.return_value = True
    mock_locator.input_value.return_value = "This is my old summary."
    mock_page.locator.return_value = mock_locator
    type(mock_locator).first = mocker.PropertyMock(return_value=mock_locator)
    
    client = LinkedinClient()
    mocker.patch.dict("os.environ", {"LINKEDIN_PROFILE_ID": "test_user"})
    
    result = client.get_about()
    
    assert result == "This is my old summary."
    mock_page.goto.assert_any_call("https://www.linkedin.com/in/test_user/", wait_until="domcontentloaded")
