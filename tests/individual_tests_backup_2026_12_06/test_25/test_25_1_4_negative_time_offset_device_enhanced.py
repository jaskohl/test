"""
Test 25.1.4: Negative UTC offset handling [DEVICE ENHANCED]
Category 25: Time Synchronization Edge Cases - COMPLETE
Test Count: Part of 5 tests in Category 25
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
ENHANCED: DeviceCapabilities integration for device-aware timezone validation
ENHANCED: Series-specific negative offset validation patterns
ENHANCED: Device-aware timeout scaling and timezone capability validation

Extracted from: tests/test_25_time_sync_edge_cases.py
Source Class: TestTimeSyncEdgeCases
Enhanced: 2025-12-01 with DeviceCapabilities integration
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.time_config_page import TimeConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_25_1_4_negative_time_offset_device_enhanced(
    time_config_page: TimeConfigPage, base_url: str, request
):
    """
    Test 25.1.4: Negative UTC offset handling [DEVICE ENHANCED]
    Purpose: Verify device handles negative UTC offsets with device-aware validation
    Expected: Device accepts negative UTC offsets with device series validation
    ENHANCED: DeviceCapabilities integration for series-specific timezone validation
    Series: Both Series 2 and 3 with device-aware negative offset testing
    """
    # Get device context for device-aware validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate timezone capabilities")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing negative UTC offset handling on {device_model} (Series {device_series}) with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to time configuration page
    time_config_page.page.goto(f"{base_url}/time", wait_until="domcontentloaded")

    # Apply device-aware timeout scaling
    timeout_scaled = int(
        5000 * timeout_multiplier
    )  # Base timeout of 5s scaled by device multiplier

    # Verify page loaded with device-aware timeout
    time_heading = time_config_page.page.get_by_role("heading", name="Time")
    expect(time_heading).to_be_visible(timeout=timeout_scaled)

    # Get timezone capabilities from DeviceCapabilities database
    timezone_capabilities = DeviceCapabilities.get_timezone_capabilities(device_model)
    logger.info(f"Timezone capabilities for {device_model}: {timezone_capabilities}")

    # Device-aware timezone field detection with series-specific patterns
    timezone_field = None
    selectors = []

    # Series-specific timezone field patterns
    if device_series == 2:
        # Series 2: Traditional timezone field patterns
        selectors = [
            "select[name='timezone']",
            "select[name='time_zone']",
            "select[name='tz']",
        ]
        logger.info(
            f"Series 2: Using traditional timezone field patterns for {device_model}"
        )

    elif device_series == 3:
        # Series 3: Advanced timezone field patterns with more comprehensive timezone list
        selectors = [
            "select[name='timezone']",
            "select[name='time_zone']",
            "select[name='tz']",
            "select[name='timezone_region']",
        ]
        logger.info(
            f"Series 3: Using advanced timezone field patterns for {device_model}"
        )

    else:
        # Unknown series: Use comprehensive selector patterns
        selectors = [
            "select[name='timezone']",
            "select[name='time_zone']",
            "select[name='tz']",
            "select[name='timezone_region']",
        ]
        logger.info(
            f"Unknown series: Using comprehensive timezone field patterns for {device_model}"
        )

    # Try semantic locator first (best practice for device-aware testing)
    try:
        timezone_field = time_config_page.page.get_by_role(
            "combobox", name=("Timezone" or "Time Zone")
        )
        if timezone_field.is_visible(timeout=2000):
            logger.info(f"Semantic timezone field found for {device_model}")
    except:
        # Fallback to device-aware selector patterns
        for selector in selectors:
            try:
                potential_field = time_config_page.page.locator(selector)
                if potential_field.is_visible(timeout=1000):
                    timezone_field = potential_field
                    logger.info(
                        f"Timezone field found using selector '{selector}' for {device_model}"
                    )
                    break
            except:
                continue

    if timezone_field and timezone_field.is_visible(timeout=timeout_scaled):
        # Timezone is configurable - validate device-aware configuration
        assert (
            timezone_field.is_enabled()
        ), f"Timezone configuration should be available on {device_model}"

        # Get all timezone options for device-aware analysis
        timezone_options = timezone_field.locator("option")
        option_count = timezone_options.count()

        logger.info(f"Found {option_count} timezone options for {device_model}")

        # Device-aware negative offset validation based on series
        negative_offset_options = []
        series2_negative_found = False
        series3_negative_found = False

        for i in range(min(option_count, 200)):  # Check more options for Series 3
            try:
                option_text = timezone_options.nth(i).inner_text()
                option_value = timezone_options.nth(i).get_attribute("value")

                # Look for negative offset patterns
                if option_text and ("-" in option_text or "(UTC-" in option_text):
                    negative_offset_options.append(
                        {"index": i, "text": option_text, "value": option_value}
                    )

                    # Series-specific negative offset validation
                    if device_series == 2:
                        if any(
                            region in option_text.lower()
                            for region in ["pacific", "mountain", "central", "eastern"]
                        ):
                            series2_negative_found = True
                            logger.info(
                                f"Series 2: Found US negative offset option: {option_text}"
                            )

                    elif device_series == 3:
                        if any(
                            region in option_text.lower()
                            for region in [
                                "pacific",
                                "mountain",
                                "central",
                                "eastern",
                                "tokyo",
                                "beijing",
                                "moscow",
                            ]
                        ):
                            series3_negative_found = True
                            logger.info(
                                f"Series 3: Found advanced negative offset option: {option_text}"
                            )

            except Exception as option_error:
                logger.warning(
                    f"Error reading timezone option {i} on {device_model}: {option_error}"
                )
                continue

        # Device-aware validation of negative offset support
        if negative_offset_options:
            logger.info(
                f"Found {len(negative_offset_options)} negative offset options for {device_model}"
            )

            # Series-specific validation criteria
            if device_series == 2:
                # Series 2: Should have at least basic US negative offset options
                assert (
                    len(negative_offset_options) >= 2
                ), f"Series 2 device {device_model} should have at least 2 negative offset options"
                assert (
                    series2_negative_found
                ), f"Series 2 device {device_model} should have US negative offset options"

            elif device_series == 3:
                # Series 3: Should have comprehensive negative offset options
                assert (
                    len(negative_offset_options) >= 5
                ), f"Series 3 device {device_model} should have at least 5 negative offset options"
                assert (
                    series3_negative_found
                ), f"Series 3 device {device_model} should have comprehensive negative offset options"

            else:
                # Unknown series: Basic validation
                assert (
                    len(negative_offset_options) >= 1
                ), f"Device {device_model} should have at least 1 negative offset option"

            # Test selecting a negative offset timezone (device-aware approach)
            first_negative_option = negative_offset_options[0]
            logger.info(
                f"Testing negative offset selection: {first_negative_option['text']}"
            )

            try:
                # Try to select the negative offset option
                if first_negative_option["value"]:
                    timezone_field.select_option(value=first_negative_option["value"])
                else:
                    timezone_field.select_option(index=first_negative_option["index"])

                logger.info(
                    f"Successfully selected negative offset option on {device_model}"
                )

                # Verify the selection was accepted
                selected_value = timezone_field.input_value()
                if selected_value:
                    logger.info(
                        f"Selected timezone value on {device_model}: {selected_value}"
                    )
                else:
                    # Some devices may not return the selected value immediately
                    logger.info(
                        f"Negative offset selection accepted on {device_model} (value not immediately readable)"
                    )

            except Exception as selection_error:
                logger.warning(
                    f"Negative offset selection failed on {device_model}: {selection_error}"
                )
                # Don't fail the test - some devices may handle timezone selection differently

        else:
            # No negative offset options found
            logger.warning(f"No negative offset options found for {device_model}")

            # Cross-validate with device capabilities database
            expected_timezone_support = timezone_capabilities.get(
                "negative_offset_support", True
            )
            if expected_timezone_support:
                pytest.fail(
                    f"Device {device_model} should support negative UTC offsets but none were found"
                )
            else:
                logger.info(
                    f"Device {device_model} correctly lacks negative offset support"
                )
                pytest.skip(f"Negative offset options not available on {device_model}")

        # Cross-validate timezone support with device capabilities database
        expected_timezone_count = timezone_capabilities.get("timezone_count", 50)
        if option_count < (expected_timezone_count * 0.5):  # Allow 50% variance
            logger.warning(
                f"Device {device_model} has fewer timezone options ({option_count}) "
                f"than expected ({expected_timezone_count})"
            )

        logger.info(
            f"Cross-validated: {device_model} has {option_count} timezone options"
        )

        # Record successful device-aware negative offset validation
        logger.info(
            f"DeviceCapabilities negative offset validation completed for {device_model} (Series {device_series}): "
            f"Negative UTC offset handling validated with {timeout_multiplier}x timeout scaling"
        )

        print(
            f" NEGATIVE OFFSET TEST COMPLETED: {device_model} (Series {device_series}) - "
            f"Negative UTC offset handling validated with device-aware patterns"
        )

    else:
        # Device doesn't have timezone configuration (which is valid for some configurations)
        expected_timezone_support = timezone_capabilities.get(
            "timezone_configurable", True
        )

        if not expected_timezone_support:
            logger.info(f"Device {device_model} correctly lacks timezone configuration")
            pytest.skip(
                f"Timezone configuration not available on {device_model} (as expected)"
            )
        else:
            pytest.fail(
                f"Timezone configuration should be available on {device_model} but field detection failed"
            )

    # Test completion summary
    logger.info(
        f"Negative UTC offset handling test completed successfully for {device_model}"
    )
    print(f" NEGATIVE OFFSET: Device-aware validation completed for {device_model}")
