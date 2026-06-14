import sys
from unittest.mock import patch
from linkedin_cv_updater.main import main

def test_main_cli():
    with patch("linkedin_cv_updater.main.mcp.run") as mock_run:
        with patch.object(sys, "argv", ["linkedin-cv-updater"]):
            main()
            mock_run.assert_called_once()
