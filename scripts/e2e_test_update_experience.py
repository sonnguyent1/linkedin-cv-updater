import logging
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from linkedin_cv_updater.tools.update_experience import update_linkedin_experience, ExperienceUpdate

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    print("Generating JavaScript Snippet...")
    
    test_experience = ExperienceUpdate(
        title="Senior AI Engineer (E2E Test)",
        company_name="Acme Corp",
        start_month=1,
        start_year=2025,
        description="Developing next-gen solutions using cutting-edge AI.",
        location="Remote"
    )
    
    result = update_linkedin_experience(test_experience)
    
    print("\n--- E2E Test Output ---")
    print(result)
    print("-----------------------")
