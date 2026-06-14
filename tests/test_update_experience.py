import pytest
from linkedin_cv_updater.tools.update_experience import ExperienceUpdate, update_linkedin_experience

def test_update_linkedin_experience_success(mocker):
    """
    Test that the experience tool correctly parses input and passes it to LinkedinClient.add_experience.
    """
    input_data = ExperienceUpdate(
        title="Lead Engineer",
        company_name="Antigravity IDE Integration",
        start_month=1,
        start_year=2023,
        end_month=None,
        end_year=None,
        description="- Increased workflow efficiency by 20%\\n- Integrated 3 new MCP servers",
        location="Remote"
    )
    
    # Mock the LinkedinClient instance and its add_experience method
    mock_client_instance = mocker.Mock()
    mock_client_instance.add_experience.return_value = "SUCCESS"
    
    # Mock the LinkedinClient class to return our mock instance
    mocker.patch("linkedin_cv_updater.tools.update_experience.LinkedinClient", return_value=mock_client_instance)
    
    result = update_linkedin_experience(input_data)
    
    # Verify the client method was called with the correct mapped parameters
    mock_client_instance.add_experience.assert_called_once_with(
        title="Lead Engineer",
        company_name="Antigravity IDE Integration",
        start_month=1,
        start_year=2023,
        end_month=None,
        end_year=None,
        description="- Increased workflow efficiency by 20%\\n- Integrated 3 new MCP servers",
        location="Remote"
    )
    
    assert "✅ Successfully added" in result
    assert "Lead Engineer" in result

def test_update_linkedin_experience_failure(mocker):
    input_data = ExperienceUpdate(
        title="Engineer",
        company_name="Test Co",
        start_month=1,
        start_year=2023,
        description="test"
    )
    
    mock_client_instance = mocker.Mock()
    mock_client_instance.add_experience.return_value = "ERROR: Could not find Add experience button."
    mocker.patch("linkedin_cv_updater.tools.update_experience.LinkedinClient", return_value=mock_client_instance)
    
    result = update_linkedin_experience(input_data)
    
    assert "❌ Failed to update profile" in result
    assert "Could not find Add experience button" in result
