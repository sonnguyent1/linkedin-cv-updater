import pytest
from linkedin_cv_updater.tools.update_about import AboutUpdate, update_linkedin_about

def test_update_linkedin_about_success(mocker):
    """
    Test that the about tool correctly parses input and passes it to LinkedinClient.update_about.
    """
    input_data = AboutUpdate(
        summary="A highly motivated engineer.\\n\\nPassionate about AI."
    )
    
    mock_client_instance = mocker.Mock()
    mock_client_instance.update_about.return_value = "SUCCESS"
    mocker.patch("linkedin_cv_updater.tools.update_about.LinkedinClient", return_value=mock_client_instance)
    
    result = update_linkedin_about(input_data)
    
    mock_client_instance.update_about.assert_called_once_with(
        summary="A highly motivated engineer.\\n\\nPassionate about AI."
    )
    
    assert "✅ Successfully updated" in result

def test_update_linkedin_about_failure(mocker):
    input_data = AboutUpdate(
        summary="Failed summary"
    )
    
    mock_client_instance = mocker.Mock()
    mock_client_instance.update_about.return_value = "ERROR: Could not find the Save button."
    mocker.patch("linkedin_cv_updater.tools.update_about.LinkedinClient", return_value=mock_client_instance)
    
    result = update_linkedin_about(input_data)
    
    assert "❌ Failed to update profile" in result
    assert "Could not find the Save button" in result
