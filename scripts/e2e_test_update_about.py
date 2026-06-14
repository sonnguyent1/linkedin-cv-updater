import sys
from linkedin_cv_updater.tools.update_about import update_linkedin_about, AboutUpdate

def test_update_about():
    print("Generating JavaScript Snippet...")
    
    test_about = AboutUpdate(
        summary="I am an AI engineer passionate about building next-gen automation solutions. (Updated via E2E test)"
    )
    
    print("\n--- E2E Test Output ---")
    result = update_linkedin_about(test_about)
    print(result)
    print("-----------------------\n")
    
    if "✅ Successfully" not in result:
        sys.exit(1)

if __name__ == "__main__":
    test_update_about()
