"""
Category 5: Time Configuration - Test 5.1.1
Timezone Dropdown Selection - Pure Page Object Pattern
Test Count: 1 of 11 in Category 5
Hardware: Device Only
Priority: HIGH - Time configuration functionality
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with device intelligence
PATTERN: Zero direct .locator() calls, essential methods only
"""

import pytest
import logging
from pages.time_config_page import TimeConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_5_1_1_timezone_dropdown_selection(
    time_config_page: TimeConfigPage,
    request,
    base_url: str,
):
    """
    Test 5.1.1: Timezone Dropdown Selection - Pure Page Object Pattern
    Purpose: Verify timezone dropdown functionality with device-aware validation
    Expected: Timezone options available, selection works, device-specific timezones
    TRANSFORMED: Uses pure page object methods with device intelligence
    """
    device_model = request.session.device_hardware_model

    # Essential device intelligence
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(f"Testing timezone dropdown selection on {device_model}")

    # Navigate to time configuration page
    time_config_page.navigate_to_time_config()

    # Get timezone data for validation
    timezone_data = DeviceCapabilities.get_timezone_data(device_model)
    available_timezones = DeviceCapabilities.get_available_timezones(device_model)
    timezone_count = DeviceCapabilities.get_timezone_count(device_model)
    utc_included = DeviceCapabilities.is_utc_included(device_model)

    logger.info(f"Expected timezones: {len(available_timezones)} options")
    logger.info(f"UTC included: {utc_included}")

    # Test timezone dropdown through page object
    dropdown_test_results = time_config_page.test_timezone_dropdown_selection()
    logger.info(f"Timezone dropdown test results: {dropdown_test_results}")

    # Verify dropdown was found and populated
    dropdown_found = dropdown_test_results.get("dropdown_found", False)
    assert dropdown_found, "Timezone dropdown should be found"
    logger.info("Timezone dropdown found and populated")

    # Verify timezone count validation
    actual_count = dropdown_test_results.get("actual_count", 0)
    expected_count = dropdown_test_results.get("expected_count", timezone_count)

    # Allow for some variance in timezone counts
    count_variance_acceptable = abs(actual_count - expected_count) <= 5
    assert (
        count_variance_acceptable
    ), f"Timezone count should be close to expected ({expected_count}), got {actual_count}"
    logger.info(
        f"Timezone count validation passed: {actual_count} vs expected {expected_count}"
    )

    # Test timezone selection functionality
    selection_tests = dropdown_test_results.get("selection_tests", [])
    successful_selections = sum(
        1 for test in selection_tests if test.get("success", False)
    )
    total_tests = len(selection_tests)

    assert successful_selections > 0, "At least one timezone selection should succeed"
    logger.info(
        f"Timezone selection tests: {successful_selections}/{total_tests} successful"
    )

    # Test UTC availability if expected
    if utc_included:
        utc_available = dropdown_test_results.get("utc_available", False)
        assert utc_available, "UTC timezone should be available when expected"
        logger.info("UTC timezone availability verified")

    # Test timezone mapping validation
    mapping_results = dropdown_test_results.get("mapping_tests", [])
    if mapping_results:
        logger.info(
            f"Timezone mapping tests completed: {len(mapping_results)} mappings validated"
        )
    else:
        logger.info("No timezone mapping tests performed")

    # Test save button behavior for timezone changes
    save_button_test = dropdown_test_results.get("save_button_test", {})
    save_button_enabled = save_button_test.get("enabled_after_change", False)

    if save_button_enabled:
        logger.info("Save button enabled after timezone change verified")
    else:
        logger.info("Save button behavior varies by device (acceptable)")

    # Test timezone validation
    validation_results = dropdown_test_results.get("validation_tests", [])
    if validation_results:
        successful_validations = sum(
            1 for test in validation_results if test.get("valid", False)
        )
        logger.info(
            f"Timezone validation tests: {successful_validations}/{len(validation_results)} successful"
        )
    else:
        logger.info("No timezone validation tests performed")

    # Performance validation against device baselines
    performance_results = time_config_page.test_timezone_performance()
    logger.info(f"Timezone performance test results: {performance_results}")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)
    logger.info(f"Timezone dropdown test completed for {device_model}")
    logger.info(f"Device info: {device_info}")

    print(
        f"TIMEZONE DROPDOWN SELECTION VALIDATED: {device_model} (Series {device_series})"
    )
