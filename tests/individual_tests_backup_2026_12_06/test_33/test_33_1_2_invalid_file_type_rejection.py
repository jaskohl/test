"""
Test 33 1 2 Invalid File Type Rejection
Category: 33 - Tests\Test 33 Upload Configuration
Extracted from: tests\grouped\test_33_upload_config.py
Source Class: TestFileUploadValidation
Source Method: test_33_1_2_invalid_file_type_rejection
Individual test file for better test isolation and debugging.
"""

import pytest
import tempfile
import os
from playwright.sync_api import Page
from pages.upload_config_page import UploadConfigPage


def test_33_1_2_invalid_file_type_rejection(upload_config_page: UploadConfigPage):
    """
    Test 33.1.2: Invalid File Type Rejection
    Purpose: Verify invalid file types are rejected with appropriate error handling
    Expected: Non-accepted file types (.txt) rejected with error message or validation failure
    Series: Both Series 2 and 3
    """
    # Create an invalid text file that should be rejected
    test_content = "This is not a valid firmware file. It contains plain text data that should be rejected by the device upload validation."

    # Create the invalid file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(test_content)
        invalid_file_path = f.name

    try:
        # Verify file exists
        assert os.path.exists(invalid_file_path), "Test file should be created"

        # Check file type validation through page object (if method exists)
        if hasattr(upload_config_page, "check_file_type_validation"):
            validation_result = upload_config_page.check_file_type_validation(
                invalid_file_path
            )
            # Validation should fail for invalid file types
            assert (
                validation_result is False
            ), "File type validation should reject .txt files"
        else:
            # Fallback: Try to select the file and check for rejection
            file_input = upload_config_page.page.locator(
                "input[type='file'][name='file[]']"
            )
            file_input.set_input_files(invalid_file_path)

            # Check for error messages or validation failures
            error_indicators = [
                upload_config_page.page.locator(
                    "text=/invalid.*file|file.*not.*supported|unsupported.*type/i"
                ),
                upload_config_page.page.locator("[class*='error'], [class*='invalid']"),
                upload_config_page.page.locator("text=/error|rejected|denied/i"),
            ]

            rejection_indicated = any(
                indicator.count() > 0 for indicator in error_indicators
            )
            assert (
                rejection_indicated
            ), "Invalid file type should trigger error message or validation failure"

        print("Invalid file type rejection test passed")

    finally:
        # Clean up test file
        if os.path.exists(invalid_file_path):
            os.unlink(invalid_file_path)
