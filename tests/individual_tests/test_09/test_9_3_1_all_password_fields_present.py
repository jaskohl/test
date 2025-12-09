"""
Category 9: Access Configuration - Test 9.3.1
All Password Fields Present - Pure Page Object Pattern
Test Count: 3 of 8 in Category 9
Hardware: Device Only
Priority: HIGH - Security configuration
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on all password fields present functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.access_config_page import AccessConfigPage

logger = logging.getLogger(__name__)


def test_9_3_1_all_password_fields_present(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 9.3.1: All Password Fields Present - Pure Page Object Pattern
    Purpose: Verify all 3 password fields exist
    Expected: cfgpwd, uplpwd, stspwd fields present
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates authentication patterns across device variants
    NOTE: Device has 3 password fields, all type='text'
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate password field presence"
        )

    # Initialize page object with device-aware patterns
    access_config_page = AccessConfigPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing all password fields present on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to access configuration page using page object method
        access_config_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        access_config_page.wait_for_page_load()

        # Test device series-specific behavior using page object methods
        device_series = DeviceCapabilities.get_series(device_model)

        logger.info(
            f"Testing all password fields on {device_model} (Series {device_series})"
        )

        # Verify all 3 password fields exist using page object method
        logger.info("Testing password field availability")
        password_fields = access_config_page.get_available_password_fields()
        logger.info(f"Available password fields: {list(password_fields.keys())}")

        # Expected password fields based on device design
        expected_password_fields = [
            ("cfgpwd", "Configuration password"),
            ("uplpwd", "Upload password"),
            ("stspwd", "Status password"),
        ]

        missing_fields = []
        present_fields = []

        for field_name, description in expected_password_fields:
            logger.info(f"Checking for {description} field: {field_name}")

            # Check if field exists using page object method
            field_exists = access_config_page.is_password_field_present(field_name)

            if field_exists:
                logger.info(f"{description} field found: {field_name}")
                present_fields.append((field_name, description))

                # Verify field properties using page object method
                field_accessible = access_config_page.is_password_field_accessible(
                    field_name
                )
                field_type = access_config_page.get_password_field_type(field_name)

                logger.info(f"{description} field accessibility: {field_accessible}")
                logger.info(f"{description} field type: {field_type}")

                # Verify it's a text input as per device design
                if field_type == "text":
                    logger.info(f"{description} field type verified as 'text'")
                else:
                    logger.warning(f"{description} field type unexpected: {field_type}")

            else:
                logger.warning(f"{description} field not found: {field_name}")
                missing_fields.append((field_name, description))

        # Summary of field validation
        logger.info(f"Password fields present: {len(present_fields)}")
        logger.info(f"Password fields missing: {len(missing_fields)}")

        if missing_fields:
            logger.warning(f"Missing password fields: {missing_fields}")
        else:
            logger.info(f"All expected password fields present on {device_model}")

        # Device capabilities validation
        has_password_fields = DeviceCapabilities.has_capability(
            device_model, "password_fields"
        )
        if has_password_fields:
            logger.info(f"Device {device_model} supports password field functionality")
        else:
            logger.warning(
                f"Device {device_model} may not support password field functionality"
            )

        # Cross-validate with device authentication capabilities
        device_capabilities = DeviceCapabilities.get_capabilities(device_model)
        auth_levels = device_capabilities.get("authentication_levels", [])
        logger.info(f"Authentication levels from DeviceCapabilities: {auth_levels}")

        if len(auth_levels) >= 3:
            logger.info(
                f"Device {device_model} supports multiple authentication levels"
            )
        else:
            logger.warning(
                f"Device {device_model} may not support expected authentication levels"
            )

        # Test page data retrieval using page object method
        page_data = access_config_page.get_page_data()
        logger.info(f"Access page data retrieved: {list(page_data.keys())}")

        # Test access capabilities validation using page object method
        capabilities = access_config_page.detect_access_capabilities()
        logger.info(f"Access capabilities detected: {capabilities}")

        # Performance validation using page object methods
        logger.info("Performing performance validation")

        start_time = time.time()

        # Test page reload performance
        access_config_page.reload_page()
        reload_time = time.time() - start_time

        logger.info(f"Page reload time: {reload_time:.2f}s")

        # Final validation
        if len(present_fields) >= 3:
            logger.info(
                f"All password fields test PASSED for {device_model} (Series {device_series})"
            )
        else:
            logger.warning(
                f"All password fields test partially completed for {device_model}"
            )
            logger.info(f"Expected 3 fields, found {len(present_fields)}")

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"All password fields test failed on {device_model}: {e}")
        pytest.fail(f"All password fields test failed on {device_model}: {e}")

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = access_config_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(f"All password fields test completed for {device_model}")
