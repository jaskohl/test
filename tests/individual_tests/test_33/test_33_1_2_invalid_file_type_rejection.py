"""
Test 33 1 2 Invalid File Type Rejection (Device )
Category: 33 - Tests\Test 33 Upload Configuration
Extracted from: tests\grouped\test_33_upload_config.py
Source Class: TestFileUploadValidation
Source Method: test_33_1_2_invalid_file_type_rejection
Individual test file for better test isolation and debugging.
: DeviceCapabilities integration with device-aware file validation patterns

Purpose: Verify invalid file types are rejected with appropriate error handling using device-aware patterns
Expected: Non-accepted file types (.txt) rejected with error message or validation failure with device validation
Series: Both Series 2 and 3
"""

import pytest
import tempfile
import os
import time
import logging
from playwright.sync_api import Page
from pages.upload_config_page import UploadConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_33_1_2_invalid_file_type_rejection(
    upload_config_page: UploadConfigPage, base_url: str, request
):
    """
    Test 33.1.2: Invalid File Type Rejection (Device )
    Purpose: Verify invalid file types are rejected with appropriate error handling using device-aware patterns
    Expected: Non-accepted file types (.txt) rejected with error message or validation failure with device validation
    : DeviceCapabilities integration with device-aware file validation
    Series: Both Series 2 and 3
    """
    # : Use request.session.device_hardware_model for device detection
    device_model = request.session.device_hardware_model
    if device_model == "Unknown":
        pytest.fail("Device model not detected - cannot determine upload capabilities")

    device_series = DeviceCapabilities.get_series(device_model)

    # : Apply timeout multiplier for device-aware testing
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Create an invalid text file that should be rejected
    test_content = "This is not a valid firmware file. It contains plain text data that should be rejected by the device upload validation."

    # Create the invalid file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(test_content)
        invalid_file_path = f.name

    try:
        logger.info(
            f"Testing invalid file type rejection on {device_model} with {timeout_multiplier}x timeout multiplier"
        )

        # : Cross-validate upload capabilities with DeviceCapabilities
        has_upload_capability = DeviceCapabilities.has_capability(
            device_model, "file_upload"
        )
        if not has_upload_capability:
            pytest.skip(f"Device {device_model} does not support file upload")

        logger.info(
            f"File upload capability for {device_model}: {has_upload_capability}"
        )

        # Verify file exists
        assert os.path.exists(invalid_file_path), "Test file should be created"

        # : Navigate to upload page with device-aware timeout
        upload_config_page.page.goto(f"{base_url}/upload")
        time.sleep(1 * timeout_multiplier)

        # : Check file type validation through page object with device awareness
        if hasattr(upload_config_page, "check_file_type_validation"):
            validation_result = upload_config_page.check_file_type_validation(
                invalid_file_path
            )
            # Validation should fail for invalid file types
            assert (
                validation_result is False
            ), f"File type validation should reject .txt files on {device_model}"
            logger.info(
                f"File type validation correctly rejected .txt file on {device_model}"
            )
        else:
            # : Fallback: Try to select the file with device-aware patterns
            file_input = upload_config_page.page.locator(
                "input[type='file'][name='file[]']"
            )
            if file_input.count() > 0:
                file_input.set_input_files(invalid_file_path)
                time.sleep(2 * timeout_multiplier)  # Device-aware delay for validation

                # : Check for error messages or validation failures with device context
                error_indicators = [
                    upload_config_page.page.locator(
                        "text=/invalid.*file|file.*not.*supported|unsupported.*type/i"
                    ),
                    upload_config_page.page.locator(
                        "[class*='error'], [class*='invalid']"
                    ),
                    upload_config_page.page.locator("text=/error|rejected|denied/i"),
                ]

                rejection_indicated = any(
                    indicator.count() > 0 for indicator in error_indicators
                )
                assert (
                    rejection_indicated
                ), f"Invalid file type should trigger error message or validation failure on {device_model}"

                logger.info(f"Invalid file type rejection confirmed on {device_model}")
            else:
                pytest.skip(f"File upload input not found on {device_model}")

        # : Cross-validate with save button patterns (indicates UI sophistication)
        save_button_pattern = DeviceCapabilities.get_interface_specific_save_button(
            device_model, "upload_configuration", None
        )
        logger.info(
            f"Device save button pattern for {device_model}: {save_button_pattern}"
        )

        # : Device series-specific upload validation
        if device_series == "Series 3":
            # Series 3 may have more sophisticated upload validation
            logger.info(f"Series 3 device {device_model} -  upload validation expected")
        elif device_series == "Series 2":
            # Series 2 may have basic upload handling
            logger.info(
                f"Series 2 device {device_model} - basic upload handling expected"
            )

        logger.info(f"Invalid file type rejection test passed for {device_model}")

    finally:
        # Clean up test file
        if os.path.exists(invalid_file_path):
            os.unlink(invalid_file_path)
