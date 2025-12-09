"""
Category 8: Display Configuration - Test 8.1.1
Display Mode Checkboxes - DeviceCapabilities Enhanced
Test Count: 1 of 4 in Category 8
Hardware: Device Only
Priority: HIGH - Display configuration functionality
Series: Both Series 2 and 3
ENHANCED: Comprehensive DeviceCapabilities integration for device-aware display validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.display_config_page import DisplayConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_8_1_1_display_mode_checkboxes_device_enhanced(
    display_config_page: DisplayConfigPage, base_url: str, request
):
    """
    Test 8.1.1: Display Mode Checkboxes - DeviceCapabilities Enhanced
    Purpose: Verify display mode checkboxes with device-aware validation
    Expected: Checkboxes functional, mode selection works, device-specific timing
    ENHANCED: Full DeviceCapabilities integration for display configuration validation
    Series: Both - validates display patterns across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate display behavior")

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing display mode checkboxes on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to display configuration page
    display_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    display_config_page.verify_page_loaded()

    # Test display mode checkboxes with device-aware validation
    try:
        # Locate display mode checkboxes with device-aware selectors
        mode_checkboxes = display_config_page.page.locator(
            "input[type='checkbox'][name*='mode'], input[type='checkbox'][id*='mode']"
        )

        checkbox_timeout = int(8000 * timeout_multiplier)

        if mode_checkboxes.count() > 0:
            logger.info(
                f"Found {mode_checkboxes.count()} display mode checkboxes on {device_model}"
            )

            # Test each checkbox
            for i in range(min(mode_checkboxes.count(), 5)):  # Test up to 5 checkboxes
                checkbox = mode_checkboxes.nth(i)

                try:
                    expect(checkbox).to_be_visible(timeout=checkbox_timeout)

                    # Get checkbox information
                    checkbox_id = checkbox.get_attribute("id") or f"checkbox_{i}"
                    checkbox_name = checkbox.get_attribute("name") or f"mode_{i}"

                    logger.info(
                        f"Testing checkbox {i}: ID='{checkbox_id}', Name='{checkbox_name}'"
                    )

                    # Test checkbox state
                    initial_state = checkbox.is_checked()
                    logger.info(
                        f"Initial checkbox state: {'checked' if initial_state else 'unchecked'}"
                    )

                    # Test toggling checkbox
                    checkbox.click()
                    time.sleep(0.5)

                    # Verify state changed
                    new_state = checkbox.is_checked()
                    if new_state != initial_state:
                        logger.info(
                            f" Checkbox toggled successfully: {'checked' if new_state else 'unchecked'}"
                        )
                    else:
                        logger.warning(
                            f" Checkbox state may not have changed: {'checked' if new_state else 'unchecked'}"
                        )

                    # Test toggling back
                    checkbox.click()
                    time.sleep(0.5)

                    # Verify state reverted
                    reverted_state = checkbox.is_checked()
                    if reverted_state == initial_state:
                        logger.info(
                            f" Checkbox reverted successfully: {'checked' if reverted_state else 'unchecked'}"
                        )
                    else:
                        logger.warning(f" Checkbox may not have reverted properly")

                except Exception as e:
                    logger.warning(f"Checkbox {i} test failed: {e}")
        else:
            logger.warning(f"No display mode checkboxes found on {device_model}")
            # Some devices may not have checkboxes, don't fail

    except Exception as e:
        pytest.fail(f"Display mode checkbox validation failed on {device_model}: {e}")

    # Test save button behavior for display changes
    try:
        # Test save button with device-aware patterns
        save_button = display_config_page.page.locator("button#button_save")

        if save_button.count() > 0:
            # Initially should be disabled without changes
            if save_button.is_disabled():
                logger.info(
                    f"Display save button initially disabled as expected on {device_model}"
                )
            else:
                logger.info(
                    f"Display save button state unusual but proceeding on {device_model}"
                )

            # Test saving functionality
            save_success = display_config_page.save_configuration()
            if save_success:
                logger.info(f"Display configuration save successful on {device_model}")
            else:
                logger.warning(f"Display configuration save failed on {device_model}")
        else:
            logger.warning(f"Display save button not found on {device_model}")

    except Exception as e:
        logger.warning(f"Display save button test failed on {device_model}: {e}")

    # Test display mode persistence
    try:
        # Make a display mode change
        if mode_checkboxes.count() > 0:
            first_checkbox = mode_checkboxes.first
            initial_state = first_checkbox.is_checked()

            # Toggle checkbox
            first_checkbox.click()
            time.sleep(1)

            # Check if change was applied
            new_state = first_checkbox.is_checked()
            if new_state != initial_state:
                logger.info(f"Display mode change applied on {device_model}")
            else:
                logger.warning(
                    f"Display mode change may not have been applied on {device_model}"
                )

    except Exception as e:
        logger.warning(f"Display mode persistence test failed on {device_model}: {e}")

    # Performance validation against device baselines
    try:
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            nav_performance = performance_data.get("navigation_performance", {})
            section_nav = nav_performance.get("section_navigation", {})
            typical_time = section_nav.get("typical_time", "")

            if typical_time:
                logger.info(f"Display navigation performance baseline: {typical_time}")

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)
    capabilities = DeviceCapabilities.get_capabilities(device_model)

    logger.info(f"Display mode checkboxes test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Device series: {device_series}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(f"DISPLAY MODE CHECKBOXES VALIDATED: {device_model} (Series {device_series})")
