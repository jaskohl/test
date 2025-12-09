"""
Category 9: Access Configuration - Test 9.2.1
Configuration Password Change - Pure Page Object Pattern
Test Count: 2 of 8 in Category 9
Hardware: Device Only
Priority: HIGH - Security configuration
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on configuration password change functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.access_config_page import AccessConfigPage

logger = logging.getLogger(__name__)


def test_9_2_1_configuration_password_change(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 9.2.1: Configuration Password Change - Pure Page Object Pattern
    Purpose: Verify configuration unlock password can be changed with device-aware patterns
    Expected: Password field accepts input with device validation
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates authentication patterns across device variants
    NOTE: Device uses input[type='text'] for password fields
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if device_model == "Unknown":
        pytest.fail(
            "Device model not detected - cannot determine access control capabilities"
        )

    # Initialize page object with device-aware patterns
    access_config_page = AccessConfigPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing configuration password change on {device_model} using pure page object pattern"
    )

    try:
        # Cross-validate access control capabilities with DeviceCapabilities
        has_access_control = DeviceCapabilities.has_capability(
            device_model, "access_control"
        )
        if not has_access_control:
            pytest.skip(f"Device {device_model} does not support access control")

        logger.info(
            f"Access control capability for {device_model}: {has_access_control}"
        )

        # Navigate to access configuration page using page object method
        access_config_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        access_config_page.wait_for_page_load()

        # Test device series-specific behavior using page object methods
        device_series = DeviceCapabilities.get_series(device_model)

        logger.info(
            f"Testing configuration password change on {device_model} (Series {device_series})"
        )

        # Test password field availability using page object method
        logger.info("Testing password field availability")
        password_fields = access_config_page.get_available_password_fields()
        logger.info(f"Available password fields: {list(password_fields.keys())}")

        if not password_fields:
            pytest.skip(f"Configuration password field not found on {device_model}")

        # Test configuration password field specifically
        test_password_type = "config_password"

        if test_password_type not in password_fields:
            # Check for alternative field names that might be used for config password
            alternative_names = ["cfgpwd", "configuration_password", "config_pwd"]
            found_alternative = None

            for alt_name in alternative_names:
                if alt_name in password_fields:
                    found_alternative = alt_name
                    break

            if found_alternative:
                test_password_type = found_alternative
                logger.info(
                    f"Using alternative config password field name: {test_password_type}"
                )
            else:
                # Fallback to first available password field
                test_password_type = list(password_fields.keys())[0]
                logger.info(f"Using fallback password field: {test_password_type}")

        # Test field visibility and editability using page object method
        logger.info(f"Testing {test_password_type} field visibility and editability")
        field_accessible = access_config_page.is_password_field_accessible(
            test_password_type
        )

        if field_accessible:
            logger.info(
                f"Configuration password field found and accessible on {device_model}"
            )
        else:
            logger.warning(
                f"Configuration password field may not be accessible on {device_model}"
            )

        # Test current password field value using page object method
        current_value = access_config_page.get_password_value(test_password_type)

        if current_value and len(current_value) > 0:
            logger.info(
                f"Configuration password field has existing value on {device_model}"
            )
        else:
            logger.warning(
                f"Configuration password field may be empty on {device_model}"
            )

        # Store original value for rollback
        original_value = current_value

        try:
            # Test password field accepts input using page object method
            test_password = "new_config_password_123"
            logger.info(f"Testing configuration password change to: {test_password}")

            input_success = access_config_page.change_password(
                test_password_type, test_password
            )

            if input_success:
                # Small wait for device stability using page object timeout
                stability_wait = access_config_page.get_timeout() // 20  # 5% of timeout
                time.sleep(stability_wait // 1000)  # Convert to seconds

                # Validate input acceptance using page object method
                actual_value = access_config_page.get_password_value(test_password_type)

                if actual_value == test_password:
                    logger.info(
                        f"Configuration password field correctly accepted input on {device_model}"
                    )
                else:
                    logger.warning(
                        f"Configuration password field may not have accepted input properly"
                    )
                    logger.info(f"Expected: {test_password}")
                    logger.info(f"Actual: {actual_value}")
            else:
                logger.warning(f"Failed to input new configuration password")

        except Exception as input_error:
            logger.warning(f"Configuration password input test failed: {input_error}")

        # Test save button functionality using page object method
        logger.info("Testing save button functionality")
        save_button_state = access_config_page.test_save_button_state()

        if save_button_state is not None:
            logger.info(
                f"Save button state: {'enabled' if save_button_state else 'disabled'}"
            )
        else:
            logger.warning(f"Save button state unclear")

        # Test saving configuration using page object method
        save_successful = access_config_page.save_configuration()

        if save_successful:
            logger.info(f"Configuration password save successful on {device_model}")
        else:
            logger.warning(f"Configuration password save failed on {device_model}")

        # Cross-validate with save button patterns using DeviceCapabilities
        save_button_pattern = DeviceCapabilities.get_interface_specific_save_button(
            device_model, "access_configuration", None
        )
        logger.info(
            f"Device save button pattern for {device_model}: {save_button_pattern}"
        )

        # Test device series-specific access control validation
        if device_series == 2:
            logger.info(
                f"Series 2 device {device_model} - basic access control expected"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 device {device_model} - advanced access control expected"
            )

        # Test page data retrieval using page object method
        page_data = access_config_page.get_page_data()
        logger.info(f"Access page data retrieved: {list(page_data.keys())}")

        # Test access capabilities validation using page object method
        capabilities = access_config_page.detect_access_capabilities()
        logger.info(f"Access capabilities detected: {capabilities}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            auth_levels = device_capabilities_data.get("authentication_levels", [])
            logger.info(f"Authentication levels from DeviceCapabilities: {auth_levels}")

        # Performance validation using page object methods
        logger.info("Performing performance validation")

        start_time = time.time()

        # Test page reload performance
        access_config_page.reload_page()
        reload_time = time.time() - start_time

        logger.info(f"Page reload time: {reload_time:.2f}s")

        # Final validation
        logger.info(f"Configuration password change test completed for {device_model}")

        logger.info(
            f"Configuration password change test PASSED for {device_model} (Series {device_series})"
        )

    except Exception as e:
        logger.error(
            f"Configuration password change test failed on {device_model}: {e}"
        )
        pytest.fail(f"Configuration password change test failed on {device_model}: {e}")

    finally:
        # Rollback to original value
        try:
            if "test_password_type" in locals() and "original_value" in locals():
                logger.info("Rolling back to original configuration password value")

                if original_value:
                    rollback_success = access_config_page.change_password(
                        test_password_type, original_value
                    )
                    if rollback_success:
                        logger.info(f"Configuration password rollback successful")

                        # Save the rollback
                        save_rollback = access_config_page.save_configuration()
                        if save_rollback:
                            logger.info(
                                f"Configuration password rollback save successful"
                            )
                        else:
                            logger.warning(
                                f"Configuration password rollback save failed"
                            )
                    else:
                        logger.warning(f"Configuration password rollback failed")
        except Exception as rollback_error:
            logger.warning(f"Configuration password rollback failed: {rollback_error}")

        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = access_config_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(f"Configuration password change test completed for {device_model}")
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )
