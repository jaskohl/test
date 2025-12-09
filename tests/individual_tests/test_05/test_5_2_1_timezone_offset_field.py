"""
Category: 5 - Time Configuration - Test 5.1.2
Timezone Offset Field - Pure Page Object Pattern
Test Count: 1 of 32 in Category 5
Hardware: Device Only
Priority: HIGH - Critical time synchronization settings
Series: Both Series 2 and 3
IMPROVED: Pure page object architecture with device-aware timezone offset validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.time_config_page import TimeConfigPage
from pages.dashboard_page import DashboardPage

logger = logging.getLogger(__name__)


def test_5_2_1_timezone_offset_field(time_config_page: TimeConfigPage, request):
    """
    Test 5.1.2: Timezone Offset Field (Pure Page Object Pattern)
    Purpose: Verify timezone offset field accepts valid formats using pure page object architecture
    Expected: Accepts +/-HH:MM format with device-aware validation
    IMPROVED: Pure page object pattern with comprehensive timezone offset validation
    Series: Both 2 and 3
    """
    # Get device context using page object encapsulation
    device_model = request.session.get("device_model", "unknown")
    if not device_model or device_model == "unknown":
        pytest.skip("Device model not detected - cannot validate timezone offset field")

    logger = logging.getLogger(__name__)

    try:
        logger.info(f"{device_model}: Starting timezone offset field validation")

        # Initialize page objects for timezone offset validation
        time_page_obj = TimeConfigPage(time_config_page.page, device_model)
        dashboard_page_obj = DashboardPage(time_config_page.page, device_model)

        # Validate device context using page object methods
        device_series = time_page_obj.get_expected_device_series()
        timeout_multiplier = time_page_obj.get_timeout_multiplier()

        logger.info(f"{device_model}: Device series: {device_series}")
        logger.info(f"{device_model}: Timeout multiplier: {timeout_multiplier}x")

        # Test offset field with device-aware timeout using page object method
        logger.info(
            f"{device_model}: Testing timezone offset field visibility and editability"
        )

        # Verify offset field visibility and editability using page object method
        offset_field_visible = time_page_obj.verify_timezone_offset_field_visible()
        assert (
            offset_field_visible
        ), f"Timezone offset field should be visible for {device_model}"

        offset_field_editable = time_page_obj.verify_timezone_offset_field_editable()
        assert (
            offset_field_editable
        ), f"Timezone offset field should be editable for {device_model}"

        # Test valid offset format using page object method
        logger.info(f"{device_model}: Testing valid offset format (+05:00)")

        test_offset = "+05:00"
        offset_configured = time_page_obj.configure_timezone_offset(test_offset)
        assert (
            offset_configured
        ), f"Timezone offset configuration failed for {device_model}"

        # Verify offset configuration using page object method
        current_offset = time_page_obj.get_timezone_offset_value()
        assert (
            current_offset == test_offset
        ), f"Expected {test_offset}, got {current_offset} for {device_model}"

        logger.info(f"{device_model}: Offset field validation successful")

        # Device capabilities validation using page object method
        timezone_offset_capable = time_page_obj.has_timezone_offset_capability()
        assert (
            timezone_offset_capable
        ), f"Device should support timezone offset configuration for {device_model}"

        # Additional timezone offset validation using page object methods
        logger.info(f"{device_model}: Additional timezone offset validation")

        # Series-specific validation using page object methods
        if device_series == 2:
            time_page_obj.validate_series2_timezone_offset_patterns()
        elif device_series == 3:
            time_page_obj.validate_series3_timezone_offset_patterns()

        # Cross-validation test using page object method
        time_page_obj.test_timezone_offset_cross_validation()

        logger.info(
            f"{device_model}: Timezone offset field validation completed successfully"
        )
        print(f"Timezone offset field test passed for {device_model}")

    except Exception as e:
        logger.error(f"{device_model}: Timezone offset field validation failed: {e}")
        pytest.fail(f"Timezone offset field test failed for {device_model}: {e}")
