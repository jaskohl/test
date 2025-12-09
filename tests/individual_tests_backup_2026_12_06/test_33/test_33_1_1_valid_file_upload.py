"""
Test 33 1 1 Valid File Upload
Category: 33 - Tests\Test 33 Upload Configuration
Extracted from: tests\grouped\test_33_upload_config.py
Source Class: TestFileUploadValidation
Source Method: test_33_1_1_valid_file_upload
Individual test file for better test isolation and debugging.
UPDATED: Now uses actual firmware files from files/ directory
"""

import pytest
import os
from pathlib import Path
from playwright.sync_api import Page, expect
from pages.upload_config_page import UploadConfigPage


def test_33_1_1_valid_file_upload(upload_config_page: UploadConfigPage):
    """
    Test 33.1.1: Valid File Upload
    Purpose: Verify valid firmware/configuration file upload and processing
    Expected: .fwu files accepted, upload completes, and file is processed by device
    Series: Both Series 2 and 3
    Note: Device only accepts .fwu, .pem, .pub files
    """
    # Determine firmware file based on device series or use default
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
    print(f"Using firmware file: {firmware_file_path} (Size: {file_size} bytes)")

    try:
        # Verify file upload field exists
        file_input = upload_config_page.page.locator(
            "input[type='file'][name='file[]']"
        )
        expect(file_input).to_be_visible()

        # Attempt upload through page object method using real firmware file
        upload_result = upload_config_page.upload_file(firmware_file_path)

        # Verify upload completed (method returns True on success)
        assert (
            upload_result is True
        ), "upload_file() should return True for successful file upload"

        # Verify file was processed - check for upload confirmation message
        success_indicators = [
            upload_config_page.page.locator(
                "text=/upload.*successful|file.*uploaded|success/i"
            ),
            upload_config_page.page.locator("[class*='success'], [class*='complete']"),
            upload_config_page.page.locator("text=/complete|finished|done/i"),
        ]

        upload_confirmed = any(
            indicator.count() > 0 for indicator in success_indicators
        )
        assert (
            upload_confirmed
        ), "Upload success should be indicated by message or UI element"

        print(
            f"Valid FWU upload test passed using real firmware file: {firmware_file_path}"
        )

    except Exception as e:
        print(f"Upload test completed with validation: {e}")
        # Don't clean up firmware files - they're real files
        raise
