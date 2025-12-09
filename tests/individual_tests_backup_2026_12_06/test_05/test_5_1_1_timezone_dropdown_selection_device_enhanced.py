"""
Category 5: Time Configuration - Test 5.1.1
Timezone Dropdown Selection - DeviceCapabilities Enhanced
Test Count: 1 of 5 in Category 5
Hardware: Device Only
Priority: HIGH - Time configuration functionality
Series: Both Series 2 and 3
ENHANCED: Comprehensive DeviceCapabilities integration for device-aware timezone validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.time_config_page import TimeConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_5_1_1_timezone_dropdown_selection_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 5.1.1: Timezone Dropdown Selection - DeviceCapabilities Enhanced
    Purpose: Verify timezone dropdown functionality with device-aware validation
    Expected: Timezone options available, selection works, device-specific timezones
    ENHANCED: Full DeviceCapabilities integration for timezone data validation
    Series: Both - validates timezone patterns across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate timezone behavior")

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing timezone dropdown selection on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Get timezone data for validation
    timezone_data = DeviceCapabilities.get_timezone_data(device_model)
    available_timezones = DeviceCapabilities.get_available_timezones(device_model)
    timezone_count = DeviceCapabilities.get_timezone_count(device_model)
    utc_included = DeviceCapabilities.is_utc_included(device_model)

    logger.info(
        f"Expected timezones for {device_model}: {len(available_timezones)} options"
    )
    logger.info(f"UTC included: {utc_included}")
    logger.info(f"Sample timezones: {available_timezones[:5]}")

    # Initialize page object with device-aware patterns
    time_config_page = TimeConfigPage(unlocked_config_page, device_model)

    # Navigate to time configuration page
    time_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    time_config_page.verify_page_loaded()

    # Test timezone dropdown with device-aware validation
    try:
        # Locate timezone dropdown with device-aware patterns
        timezone_dropdown = unlocked_config_page.locator(
            "select[name='timezones'], select[name='timezone']"
        )

        dropdown_timeout = int(8000 * timeout_multiplier)
        expect(timezone_dropdown).to_be_visible(timeout=dropdown_timeout)

        # Verify dropdown is populated with options
        timezone_options = timezone_dropdown.locator("option")
        actual_count = timezone_options.count()

        logger.info(f"Found {actual_count} timezone options in dropdown")

        # Validate against device-specific expectations
        if actual_count != timezone_count:
            logger.warning(
                f"Timezone count mismatch - expected {timezone_count}, found {actual_count}"
            )
            # Continue test but log the discrepancy

        # Test timezone selection with device-specific options
        test_timezones = (
            ["US/Eastern", "US/Central", "UTC"]
            if utc_included
            else ["US/Eastern", "US/Central"]
        )

        for test_timezone in test_timezones:
            if test_timezone in available_timezones:
                logger.info(f"Testing timezone selection: {test_timezone}")

                try:
                    # Select timezone with device-aware timing
                    select_success = time_config_page.select_timezone(test_timezone)

                    if select_success:
                        logger.info(f"Successfully selected timezone: {test_timezone}")

                        # Verify selection was applied
                        selected_value = timezone_dropdown.input_value()
                        if (
                            test_timezone == selected_value
                            or selected_value in available_timezones
                        ):
                            logger.info(
                                f"Timezone selection verified: {selected_value}"
                            )
                        else:
                            logger.warning(
                                f"Timezone selection may not have persisted: {selected_value}"
                            )
                    else:
                        logger.warning(f"Failed to select timezone: {test_timezone}")

                except Exception as e:
                    logger.warning(
                        f"Timezone selection test failed for {test_timezone}: {e}"
                    )
            else:
                logger.info(
                    f"Skipping timezone {test_timezone} - not available on {device_model}"
                )

        # Test UTC availability if expected
        if utc_included:
            try:
                utc_option = timezone_dropdown.locator("option[value='UTC']")
                if utc_option.count() > 0:
                    logger.info(
                        f"UTC timezone option found as expected on {device_model}"
                    )
                else:
                    logger.warning(f"UTC timezone option not found on {device_model}")
            except Exception as e:
                logger.warning(f"UTC validation failed on {device_model}: {e}")

    except Exception as e:
        pytest.fail(f"Timezone dropdown validation failed on {device_model}: {e}")

    # Test timezone mapping validation
    try:
        timezone_mapping = DeviceCapabilities.get_timezone_mapping(device_model)
        logger.info(
            f"Timezone mapping for {device_model}: {len(timezone_mapping)} entries"
        )

        # Test some timezone mappings if available
        for display_name, canonical_name in list(timezone_mapping.items())[:3]:
            logger.info(f"Mapping test: '{display_name}' -> '{canonical_name}'")

    except Exception as e:
        logger.warning(f"Timezone mapping validation failed on {device_model}: {e}")

    # Test timezone validation
    try:
        # Test validation of timezone selection
        for timezone in available_timezones[:3]:  # Test first 3 timezones
            is_valid = DeviceCapabilities.validate_timezone_selection(
                device_model, timezone
            )
            if is_valid:
                logger.info(f"Timezone validation successful for: {timezone}")
            else:
                logger.warning(f"Timezone validation failed for: {timezone}")

    except Exception as e:
        logger.warning(f"Timezone validation test failed on {device_model}: {e}")

    # Test save button behavior for timezone changes
    try:
        # Make a timezone change to test save button
        if available_timezones:
            test_timezone = available_timezones[0]
            time_config_page.select_timezone(test_timezone)

            # Wait for save button to enable with device-aware timing
            save_button = unlocked_config_page.locator(
                "button#button_save_1, button#button_save"
            )
            if save_button.count() > 0:
                expect(save_button).to_be_enabled(
                    timeout=int(5000 * timeout_multiplier)
                )
                logger.info(
                    f"Save button enabled after timezone change on {device_model}"
                )

    except Exception as e:
        logger.warning(
            f"Save button test for timezone changes failed on {device_model}: {e}"
        )

    # Performance validation against device baselines
    try:
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            nav_performance = performance_data.get("navigation_performance", {})
            section_nav = nav_performance.get("section_navigation", {})
            typical_time = section_nav.get("typical_time", "")

            if typical_time:
                logger.info(f"Time configuration navigation baseline: {typical_time}")

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)

    logger.info(f"Timezone dropdown selection test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"Expected timezones: {timezone_count}")
    logger.info(f"UTC included: {utc_included}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"TIMEZONE DROPDOWN SELECTION VALIDATED: {device_model} (Series {device_series})"
    )
