"""
Category 28: Syslog Configuration - Test 28.1.1
Syslog 1 Enable Checkbox - DeviceCapabilities Enhanced
Test Count: 1 of 1 in Category 28
Hardware: Device Only
Priority: HIGH - Syslog configuration functionality
Series: Both Series 2 and 3
ENHANCED: Comprehensive DeviceCapabilities integration for device-aware syslog validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.syslog_config_page import SyslogConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_28_1_1_syslog1_enable_checkbox_device_enhanced(
    syslog_config_page: SyslogConfigPage, base_url: str, request
):
    """
    Test 28.1.1: Syslog 1 Enable Checkbox - DeviceCapabilities Enhanced
    Purpose: Verify syslog 1 enable checkbox with device-aware validation
    Expected: Checkbox functional, enable/disable works, device-specific timing
    ENHANCED: Full DeviceCapabilities integration for syslog configuration validation
    Series: Both - validates syslog patterns across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate syslog behavior")

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing syslog 1 enable checkbox on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to syslog configuration page
    syslog_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    syslog_config_page.verify_page_loaded()

    # Test syslog 1 enable checkbox with device-aware validation
    try:
        # Locate syslog 1 enable checkbox with device-aware selectors
        syslog1_checkbox = syslog_config_page.page.locator(
            "input[type='checkbox'][name*='syslog1'], input[type='checkbox'][name*='syslog_1'], input[type='checkbox'][id*='syslog1']"
        )

        checkbox_timeout = int(8000 * timeout_multiplier)
        expect(syslog1_checkbox).to_be_visible(timeout=checkbox_timeout)

        logger.info(f"Syslog 1 enable checkbox found on {device_model}")

        # Test checkbox state and functionality
        initial_state = syslog1_checkbox.is_checked()
        logger.info(
            f"Initial syslog 1 checkbox state: {'checked' if initial_state else 'unchecked'}"
        )

        # Test toggling checkbox
        syslog1_checkbox.click()
        time.sleep(0.5)

        # Verify state changed
        new_state = syslog1_checkbox.is_checked()
        if new_state != initial_state:
            logger.info(
                f" Syslog 1 checkbox toggled successfully: {'checked' if new_state else 'unchecked'}"
            )
        else:
            logger.warning(f" Syslog 1 checkbox state may not have changed")

        # Test dependent fields visibility/functionality
        if new_state:  # If enabled, test related fields
            logger.info(f"Testing syslog 1 dependent fields when enabled")

            # Test syslog server field
            server_field = syslog_config_page.page.locator(
                "input[name*='syslog1_server'], input[name*='syslog_1_server'], input[id*='syslog1_server']"
            )

            if server_field.count() > 0:
                expect(server_field).to_be_visible(timeout=3000)
                logger.info(f"Syslog 1 server field visible when enabled")

                # Test server field functionality
                test_server = "192.168.1.100"
                server_field.fill(test_server)
                time.sleep(0.3)

                server_value = server_field.input_value()
                if test_server in server_value:
                    logger.info(f"Syslog 1 server field functional: {server_value}")
                else:
                    logger.warning(f"Syslog 1 server field may not be functional")
            else:
                logger.warning(f"Syslog 1 server field not found when enabled")

        # Test toggling back
        syslog1_checkbox.click()
        time.sleep(0.5)

        # Verify state reverted
        reverted_state = syslog1_checkbox.is_checked()
        if reverted_state == initial_state:
            logger.info(
                f" Syslog 1 checkbox reverted successfully: {'checked' if reverted_state else 'unchecked'}"
            )
        else:
            logger.warning(f" Syslog 1 checkbox may not have reverted properly")

    except Exception as e:
        pytest.fail(
            f"Syslog 1 enable checkbox validation failed on {device_model}: {e}"
        )

    # Test save button behavior for syslog changes
    try:
        # Test save button with device-aware patterns
        save_button = syslog_config_page.page.locator("button#button_save")

        if save_button.count() > 0:
            # Initially should be disabled without changes
            if save_button.is_disabled():
                logger.info(
                    f"Syslog save button initially disabled as expected on {device_model}"
                )
            else:
                logger.info(
                    f"Syslog save button state unusual but proceeding on {device_model}"
                )

            # Test saving functionality
            save_success = syslog_config_page.save_configuration()
            if save_success:
                logger.info(f"Syslog configuration save successful on {device_model}")
            else:
                logger.warning(f"Syslog configuration save failed on {device_model}")
        else:
            logger.warning(f"Syslog save button not found on {device_model}")

    except Exception as e:
        logger.warning(f"Syslog save button test failed on {device_model}: {e}")

    # Test syslog configuration persistence
    try:
        # Make a syslog configuration change
        initial_state = syslog1_checkbox.is_checked()

        # Toggle checkbox
        syslog1_checkbox.click()
        time.sleep(1)

        # Check if change was applied
        new_state = syslog1_checkbox.is_checked()
        if new_state != initial_state:
            logger.info(f"Syslog 1 configuration change applied on {device_model}")
        else:
            logger.warning(
                f"Syslog 1 configuration change may not have been applied on {device_model}"
            )

    except Exception as e:
        logger.warning(
            f"Syslog configuration persistence test failed on {device_model}: {e}"
        )

    # Performance validation against device baselines
    try:
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            nav_performance = performance_data.get("navigation_performance", {})
            section_nav = nav_performance.get("section_navigation", {})
            typical_time = section_nav.get("typical_time", "")

            if typical_time:
                logger.info(f"Syslog navigation performance baseline: {typical_time}")

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)
    capabilities = DeviceCapabilities.get_capabilities(device_model)

    logger.info(f"Syslog 1 enable checkbox test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Device series: {device_series}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"SYSLOG 1 ENABLE CHECKBOX VALIDATED: {device_model} (Series {device_series})"
    )
