"""
Test 33 1 3 File Size Limit Enforcement
Category: 33 - Tests\Test 33 Upload Configuration
Extracted from: tests\grouped\test_33_upload_config.py
Source Class: TestFileUploadValidation
Source Method: test_33_1_3_file_size_limit_enforcement
Individual test file for better test isolation and debugging.
"""

import pytest
import tempfile
import os
from playwright.sync_api import Page
from pages.upload_config_page import UploadConfigPage


def test_33_1_3_file_size_limit_enforcement(upload_config_page: UploadConfigPage):
    """
    Test 33.1.3: File Size Limit Enforcement
    Purpose: Verify file size limits are enforced
    Expected: Oversized files rejected with size-related error
    Series: Both Series 2 and 3
    """
    # Create a large file that exceeds typical device limits (assume ~5MB limit)
    large_content = "x" * (6 * 1024 * 1024)  # 6MB of data

    # Create the oversized file with .fwu extension to pass basic type validation
    large_file_path = upload_config_page.create_test_file(large_content, "fwu")
    assert os.path.exists(large_file_path), "Large test file should be created"

    # Verify file size is actually large
    file_size = os.path.getsize(large_file_path)
    assert file_size > 5 * 1024 * 1024, f"File should be >5MB, got {file_size} bytes"

    try:
        # Check file size validation through page object (if method exists)
        if hasattr(upload_config_page, "check_file_size_validation"):
            size_validation_result = upload_config_page.check_file_size_validation(
                large_file_path
            )
            assert (
                size_validation_result is False
            ), "File size validation should reject oversized files"
        else:
            # Fallback: Try to upload and check for rejection
            file_input = upload_config_page.page.locator(
                "input[type='file'][name='file[]']"
            )
            file_input.set_input_files(large_file_path)

            # Wait for size validation to trigger
            upload_config_page.page.wait_for_timeout(2000)

            # Check for size-related error messages
            size_error_indicators = [
                upload_config_page.page.locator(
                    "text=/too.*large|size.*limit|file.*too.*big/i"
                ),
                upload_config_page.page.locator("text=/exceeds.*limit|over.*size/i"),
                upload_config_page.page.locator("text=/maximum.*size|size.*maximum/i"),
            ]

            size_limit_enforced = any(
                indicator.count() > 0 for indicator in size_error_indicators
            )
            assert (
                size_limit_enforced
            ), "Oversized file should trigger size limit error message"

        print("File size limit enforcement test passed")

    finally:
        # Clean up test file
        if os.path.exists(large_file_path):
            os.unlink(large_file_path)
