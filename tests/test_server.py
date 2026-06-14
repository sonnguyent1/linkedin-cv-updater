from linkedin_cv_updater.server import format_linkedin_content, extract_project_highlights

def test_format_linkedin_content():
    # Test with role
    result_role = format_linkedin_content(role_description="Did things")
    assert "Did things" in result_role
    assert "Extract key achievements" in result_role
    
    # Test with about
    result_about = format_linkedin_content(about_summary="My summary")
    assert "My summary" in result_about
    assert "multi-paragraph" in result_about
    
    # Test with both
    result_both = format_linkedin_content(role_description="R", about_summary="A")
    assert "R" in result_both
    assert "A" in result_both
    
def test_extract_project_highlights():
    result = extract_project_highlights(project_path="/test")
    assert "/test" in result
    assert "synthesize the technical challenges" in result.lower()
