"""
Category 9: Access Configuration - Test 9.2.1 (Device Enhanced)
Configuration Password Change
Test Count: 1 of 7 in Category 9
Hardware: Device Only
Priority: HIGH - Security configuration
Series: Both Series 2 and 3
Based on test_09_access_config.py::TestPasswordConfiguration::test_9_2_1_configuration_password_change
NOTE: Device uses input[type='text'] for password fields
ENHANCED: DeviceCapabilities integration with device-aware access control patterns
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.access_config_page import AccessConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_9_2_1_configuration_password_change_device_enhanced(
    access_config_page: AccessConfigPage, base_url: str, request
):
    """
    Test 9.2.1: Configuration Password Change (Device Enhanced)
    Purpose: Verify configuration unlock password can be changed with device-aware patterns
    Expected: Password field accepts input with device validation
    ENHANCED: DeviceCapabilities integration with device-aware access control
    Series: Both 2 and 3
    NOTE: Device uses input[type='text'] for password fields
    Field name: cfgpwd
    """
    # ENHANCED: Use request.session.device_hardware_model for device detection
    device_model = request.session.device_hardware_model
    if device_model == "Unknown":
        pytest.fail(
            "Device model not detected - cannot determine access control capabilities"
        )

    device_series = DeviceCapabilities.get_series(device_model)

    # ENHANCED: Apply timeout multiplier for device-aware testing
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    try:
        logger.info(
            f"Testing configuration password change on {device_model} with {timeout_multiplier}x timeout multiplier"
        )

        # ENHANCED: Cross-validate access control capabilities with DeviceCapabilities
        has_access_control = DeviceCapabilities.has_capability(
            device_model, "access_control"
        )
        if not has_access_control:
            pytest.skip(f"Device {device_model} does not support access control")

        logger.info(
            f"Access control capability for {device_model}: {has_access_control}"
        )

        # ENHANCED: Navigate to access configuration page with device-aware timeout
        access_config_page.page.goto(f"{base_url}/access")
        time.sleep(1 * timeout_multiplier)

        # ENHANCED: Device has input name="cfgpwd" for configuration password with device validation
        config_password_field = access_config_page.page.locator("input[name='cfgpwd']")

        if config_password_field.count() > 0:
            # ENHANCED: Field visibility and editability validation with device-aware timeout
            expect(config_password_field).to_be_visible(
                timeout=5000 * timeout_multiplier
            )
            expect(config_password_field).to_be_editable()
            logger.info(
                f"Configuration password field found and editable on {device_model}"
            )

            # ENHANCED: Verify field type is text (device design) with device context
            field_type = config_password_field.get_attribute("type")
            assert (
                field_type == "text"
            ), f"Config password field should be type='text' on {device_model}"
            logger.info(
                f"Configuration password field type verified as 'text' on {device_model}"
            )

            # ENHANCED: Get current value with device-aware validation
            current_value = config_password_field.input_value()
            assert (
                len(current_value) > 0
            ), f"Config password field should have a value on {device_model}"
            logger.info(
                f"Configuration password field has existing value on {device_model}"
            )

            # Store original value for rollback
            original_value = current_value

            try:
                # ENHANCED: Test password field accepts input with device-aware patterns
                test_password = "new_config_password_123"
                config_password_field.fill(test_password)
                time.sleep(0.5 * timeout_multiplier)  # Device-aware delay

                # ENHANCED: Validate input acceptance with device context
                actual_value = config_password_field.input_value()
                assert (
                    actual_value == test_password
                ), f"Config password field should accept input on {device_model}"
                logger.info(
                    f"Configuration password field correctly accepted input on {device_model}"
                )

            finally:
                # ENHANCED: Rollback to original value
                if original_value:
                    config_password_field.fill(original_value)

        else:
            pytest.skip(f"Configuration password field not found on {device_model}")

        # ENHANCED: Cross-validate with save button patterns (indicates UI sophistication)
        save_button_pattern = DeviceCapabilities.get_interface_specific_save_button(
            device_model, "access_configuration", None
        )
        logger.info(
            f"Device save button pattern for {device_model}: {save_button_pattern}"
        )

        # ENHANCED: Device series-specific access control validation
        if device_series == "Series 3":
            # Series 3 may have enhanced access control features
            logger.info(
                f"Series 3 device {device_model} - enhanced access control expected"
            )
        elif device_series == "Series 2":
            # Series 2 may have basic access control
            logger.info(
                f"Series 2 device {device_model} - basic access control expected"
            )

        logger.info(f"Configuration password change test passed for {device_model}")

    except Exception as e:
        pytest.fail(f"Configuration password change test failed on {device_model}: {e}")
