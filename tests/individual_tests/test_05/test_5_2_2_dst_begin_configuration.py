"""
Test: 5.2.2 - DST Begin Date Configuration (Pure Page Object Pattern)
Category: Time Configuration - Test 5.2.2
Test Count: 7 of 11 in Category 5
Purpose: Verify DST begin date fields (week, day, month, time)
Expected: All 4 fields configurable
Series: Both Series 2 and 3
Priority: HIGH
Hardware: Device Only
TRANSFORMED: Pure page object architecture with device intelligence
PATTERN: Zero direct .locator() calls, essential methods only
"""

import pytest
import logging
from pages.time_config_page import TimeConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_5_2_2_dst_begin_configuration(
    time_config_page: TimeConfigPage,
    request,
    base_url: str,
):
    """
    Test 5.2.2: DST Begin Date Configuration - Pure Page Object Pattern
    Purpose: Verify DST begin date fields (week, day, month, time)
    Expected: All 4 fields configurable
    TRANSFORMED: Uses pure page object methods with device intelligence
    Series: Both 2 and 3
    """
    device_model = request.session.device_hardware_model

    # Essential device intelligence
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Validate device capabilities
    has_dst_config = DeviceCapabilities.has_capability(device_model, "dst_begin_config")
    if not has_dst_config:
        pytest.skip(f"Device {device_model} does not support DST begin configuration")

    logger.info(f"Testing DST begin date configuration on {device_model}")

    # Navigate to time configuration page
    time_config_page.navigate_to_time_config()

    # Test DST begin configuration through page object
    dst_begin_test_results = time_config_page.test_dst_begin_configuration()
    logger.info(f"DST begin configuration test results: {dst_begin_test_results}")

    # Verify all DST begin fields were found
    fields_found = dst_begin_test_results.get("fields_found", {})
    week_found = fields_found.get("week_found", False)
    day_found = fields_found.get("day_found", False)
    month_found = fields_found.get("month_found", False)
    time_found = fields_found.get("time_found", False)

    assert week_found, "DST begin week field should be found"
    assert day_found, "DST begin day field should be found"
    assert month_found, "DST begin month field should be found"
    assert time_found, "DST begin time field should be found"
    logger.info("All DST begin date fields found")

    # Verify field visibility and editability
    field_visibility = dst_begin_test_results.get("field_visibility", {})
    assert all(field_visibility.values()), "All DST begin fields should be visible"
    logger.info("All DST begin fields are visible")

    # Verify field configuration tests
    field_configurations = dst_begin_test_results.get("field_configurations", {})
    week_configured = field_configurations.get("week_configured", False)
    day_configured = field_configurations.get("day_configured", False)
    month_configured = field_configurations.get("month_configured", False)
    time_configured = field_configurations.get("time_configured", False)

    assert week_configured, "DST begin week field should be configurable"
    assert day_configured, "DST begin day field should be configurable"
    assert month_configured, "DST begin month field should be configurable"
    assert time_configured, "DST begin time field should be configurable"
    logger.info("All DST begin fields are configurable")

    # Verify specific test values were applied
    test_values = dst_begin_test_results.get("test_values", {})
    week_value = test_values.get("week_value", "")
    day_value = test_values.get("day_value", "")
    month_value = test_values.get("month_value", "")
    time_value = test_values.get("time_value", "")

    expected_week = "2"  # 2nd week
    expected_day = "0"  # Sunday
    expected_month = "3"  # March
    expected_time = "2:00"

    assert (
        week_value == expected_week
    ), f"DST begin week should be '{expected_week}', got '{week_value}'"
    assert (
        day_value == expected_day
    ), f"DST begin day should be '{expected_day}', got '{day_value}'"
    assert (
        month_value == expected_month
    ), f"DST begin month should be '{expected_month}', got '{month_value}'"
    assert (
        time_value == expected_time
    ), f"DST begin time should be '{expected_time}', got '{time_value}'"
    logger.info("DST begin configuration values applied successfully")

    # Device capabilities validation passed
    logger.info("Device capabilities validation passed for DST begin configuration")

    # Device series-specific validation
    if device_series == 2:
        logger.info("Series 2 DST begin configuration validation completed")
    elif device_series == 3:
        logger.info("Series 3 DST begin configuration validation completed")

    logger.info(f"DST begin date configuration test completed for {device_model}")
