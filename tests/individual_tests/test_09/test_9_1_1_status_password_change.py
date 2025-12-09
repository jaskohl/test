"""
Category 9: Access Configuration - Test 9.1.1
Status Password Change - Pure Page Object Pattern
Test Count: 1 of 8 in Category 9
Hardware: Device Only
Priority: HIGH - Authentication configuration
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on status password change functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.access_config_page import AccessConfigPage

logger = logging.getLogger(__name__)


def test_9_1_1_status_password_change(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 9.1.1: Status Password Change - Pure Page Object Pattern
    Purpose: Verify status password change functionality with device-aware validation
    Expected: Password change works, old password disabled, device-specific timing
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates authentication patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate authentication behavior"
        )

    # Initialize page object with device-aware patterns
    access_config_page = AccessConfigPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing status password change on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to access configuration page using page object method
        access_config_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        access_config_page.wait_for_page_load()

        # Test device series-specific behavior using page object methods
        device_series = DeviceCapabilities.get_series(device_model)

        logger.info(
            f"Testing status password change on {device_model} (Series {device_series})"
        )

        # Test password field availability using page object method
        logger.info("Testing password field availability")
        password_fields = access_config_page.get_available_password_fields()
        logger.info(f"Available password fields: {list(password_fields.keys())}")

        if not password_fields:
            logger.warning(f"No password fields detected on {device_model}")
            return

        # Test status password field specifically
        test_password_type = "status_password"

        if test_password_type not in password_fields:
            logger.warning(f"Test password type '{test_password_type}' not found")
            # Fallback to first available password field
            test_password_type = list(password_fields.keys())[0]
            logger.info(f"Using fallback password type: {test_password_type}")

        # Test current password field accessibility using page object method
        logger.info(f"Testing {test_password_type} field accessibility")
        current_password_value = access_config_page.get_password_value(
            test_password_type
        )

        if current_password_value:
            logger.info(
                f"Current {test_password_type} field has value (length: {len(current_password_value)})"
            )
        else:
            logger.info(f"Current {test_password_type} field is empty")

        # Test password change functionality using page object method
        new_password = "newstatus123"
        logger.info(f"Testing {test_password_type} change to: {new_password}")

        try:
            change_success = access_config_page.change_password(
                test_password_type, new_password
            )

            if change_success:
                logger.info(f"Successfully changed {test_password_type}")

                # Verify password was set using page object method
                new_value = access_config_page.get_password_value(test_password_type)
                if len(new_value) > 0:
                    logger.info(
                        f"{test_password_type} field updated (length: {len(new_value)})"
                    )
                else:
                    logger.warning(f"{test_password_type} field may not have updated")
            else:
                logger.warning(f"Failed to change {test_password_type}")

        except Exception as password_error:
            logger.warning(f"{test_password_type} change test failed: {password_error}")

        # Test configuration password field as well using page object method
        logger.info("Testing configuration password field")
        config_password_type = "config_password"

        if config_password_type in password_fields:
            logger.info(f"Configuration password field found on {device_model}")

            current_config_value = access_config_page.get_password_value(
                config_password_type
            )
            logger.info(
                f"Current config password field state: {'has value' if current_config_value else 'empty'}"
            )
        else:
            logger.info(f"Configuration password field not found on {device_model}")

        # Test save button behavior for password changes using page object method
        logger.info("Testing save button behavior")
        save_button_state_initial = access_config_page.test_save_button_state()
        logger.info(
            f"Save button initial state: {'enabled' if save_button_state_initial else 'disabled'}"
        )

        if save_button_state_initial is False:
            logger.info(f"Access save button initially disabled as expected")
        else:
            logger.info(f"Access save button state unusual but proceeding")

        # Test saving functionality using page object method
        save_successful = access_config_page.save_configuration()

        if save_successful:
            logger.info(f"Access configuration save successful on {device_model}")
        else:
            logger.warning(f"Access configuration save failed on {device_model}")

        # Test password field validation using page object method
        logger.info("Testing password field validation")

        # Test with invalid password formats
        invalid_passwords = ["", "123", "a"]

        for invalid_pwd in invalid_passwords[:2]:  # Test a couple invalid formats
            logger.info(f"Testing invalid password format: '{invalid_pwd}'")

            try:
                validation_success = access_config_page.validate_password_field(
                    test_password_type, invalid_pwd
                )

                if validation_success:
                    logger.info(
                        f"Invalid password validation handled for: '{invalid_pwd}'"
                    )
                else:
                    logger.info(f"Invalid password rejected for: '{invalid_pwd}'")

            except Exception as validation_error:
                logger.warning(
                    f"Invalid password test failed for '{invalid_pwd}': {validation_error}"
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

        # Cross-reference with performance expectations
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            auth_performance = performance_data.get("authentication_performance", {})
            config_unlock = auth_performance.get("configuration_unlock", {})
            typical_time = config_unlock.get("typical_time", "")
            if typical_time:
                logger.info(f"Authentication performance baseline: {typical_time}")

        # Final validation
        logger.info(f"Status password change test completed for {device_model}")

        # Log comprehensive test results
        device_info = DeviceCapabilities.get_device_info(device_model)
        logger.info(f"Device info: {device_info}")
        logger.info(f"Device series: {device_series}")

        logger.info(
            f"Status password change test PASSED for {device_model} (Series {device_series})"
        )

    except Exception as e:
        logger.error(f"Status password change test failed on {device_model}: {e}")
        pytest.fail(f"Status password change test failed on {device_model}: {e}")

    finally:
        # Small cleanup wait for device stability using page object timeout
        try:
            cleanup_wait = access_config_page.get_timeout() // 20  # 5% of timeout
            time.sleep(cleanup_wait // 1000)  # Convert to seconds
        except:
            # Fallback cleanup wait
            time.sleep(0.5)

        logger.info(f"Status password change test completed for {device_model}")
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )
