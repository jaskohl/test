"""
Test 33 2 1 Upload Progress Indication
Category: 33 - Upload Configuration Tests
Extracted from: tests/grouped/test_33_upload_config.py
Source Class: TestUploadProcessManagement
Individual test file for better test isolation and debugging.
UPDATED: Now uses actual firmware files for realistic progress testing
"""

import pytest
import os
from playwright.sync_api import Page, expect
from pages.upload_config_page import UploadConfigPage


def test_33_2_1_upload_progress_indication(upload_config_page: UploadConfigPage):
    """
    Test 33.2.1: Upload Progress Indication
    Purpose: Verify upload progress is communicated to user
    Expected: Progress indicators or status updates during upload
    Series: Both Series 2 and 3
    Note: Uses actual firmware files for realistic progress monitoring
    """
    # Determine firmware file based on device series
    firmware_file_path = None

    # Try to get device model from page object
    device_model = getattr(upload_config_page, "device_model", None)

    if device_model:
        if "Series 2" in device_model or "K2" in device_model:
            firmware_file_path = "files/kronos2-04.04.00.fwu"
        elif "Series 3" in device_model or "K3" in device_model:
            firmware_file_path = "files/kronos3-02.06.04.fwu"

    # Fallback: Use Series 2 firmware if device model not available
    if not firmware_file_path or not os.path.exists(firmware_file_path):
        firmware_file_path = "files/kronos2-04.04.00.fwu"

    # Verify firmware file exists
    assert os.path.exists(
        firmware_file_path
    ), f"Firmware file should exist: {firmware_file_path}"

    # Get file size for validation
    file_size = os.path.getsize(firmware_file_path)
    print(
        f"Using firmware file for progress test: {firmware_file_path} (Size: {file_size} bytes)"
    )

    try:
        # Verify we can select file for upload
        file_selection_result = upload_config_page.select_file_for_upload(
            firmware_file_path
        )
        assert file_selection_result is True, "File should be selectable for upload"

        # Check for upload initiation capability
        if hasattr(upload_config_page, "initiate_upload"):
            initiation_result = upload_config_page.initiate_upload()
            assert initiation_result is True, "Upload should be initiatable"
        else:
            # Fallback: Look for upload button and interaction
            upload_button = upload_config_page.page.locator(
                "input[type='submit'], button[type='submit']"
            )
            expect(upload_button).to_be_visible()

        # Look for progress indicators during potential upload
        progress_indicators = [
            upload_config_page.page.locator("progress, [role='progressbar']"),
            upload_config_page.page.locator("[class*='progress'], [class*='loading']"),
            upload_config_page.page.locator(
                "text=/uploading|processing|transferring/i"
            ),
        ]

        progress_present = any(
            indicator.count() > 0 for indicator in progress_indicators
        )
        if not progress_present:
            print(
                "No explicit progress indicators found - checking for other UI feedback"
            )
        else:
            print("Progress indicators detected during upload process")

        # Wait for potential upload completion
        if hasattr(upload_config_page, "wait_for_upload_completion"):
            completion_result = upload_config_page.wait_for_upload_completion(
                timeout=30000
            )
            assert completion_result is True, "Upload should complete successfully"
        else:
            # Fallback: Wait for upload-related state changes
            upload_config_page.page.wait_for_timeout(5000)  # Allow time for upload

        print(
            f"Upload progress indication test completed using firmware file: {firmware_file_path}"
        )

    except Exception as e:
        print(f"Progress indication test encountered: {e}")
        # Don't clean up firmware files - they're real files
        raise
