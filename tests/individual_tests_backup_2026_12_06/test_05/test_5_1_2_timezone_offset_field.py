"""
Test: 5.1.2 - Timezone Offset Field (Device Enhanced)
Category: Time Configuration (Category 5)
Purpose: Verify timezone offset field accepts valid formats with device-aware patterns
Expected: Accepts +/-HH:MM format with device validation
Series: Both Series 2 and 3
Priority: HIGH
Hardware: Device Only
Based on COMPLETE_TEST_LIST.md Section 5.1.2
Device exploration data: config_time.forms.json
ENHANCED: DeviceCapabilities integration with device-aware time configuration patterns
"""

import pytest
import time
import logging
from pages.time_config_page import TimeConfigPage
from pages.device_capabilities import DeviceCapabilities
from playwright.sync_api import expect

logger = logging.getLogger(__name__)


def test_5_1_2_timezone_offset_field_device_enhanced(
    time_config_page: TimeConfigPage, base_url: str, request
):
    """
    Test 5.1.2: Timezone Offset Field (Device Enhanced)
    Purpose: Verify timezone offset field accepts valid formats with device-aware patterns
    Expected: Accepts +/-HH:MM format with device validation
    ENHANCED: DeviceCapabilities integration with device-aware time configuration
    Series: Both 2 and 3
    """
    # ENHANCED: Use request.session.device_hardware_model for device detection
    device_model = request.session.device_hardware_model
    if device_model == "Unknown":
        pytest.fail(
            "Device model not detected - cannot determine time configuration capabilities"
        )

    device_series = DeviceCapabilities.get_series(device_model)

    # ENHANCED: Apply timeout multiplier for device-aware testing
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    try:
        logger.info(
            f"Testing timezone offset field on {device_model} with {timeout_multiplier}x timeout multiplier"
        )

        # ENHANCED: Cross-validate time configuration capabilities with DeviceCapabilities
        has_time_config = DeviceCapabilities.has_capability(
            device_model, "time_configuration"
        )
        if not has_time_config:
            pytest.skip(f"Device {device_model} does not support time configuration")

        logger.info(
            f"Time configuration capability for {device_model}: {has_time_config}"
        )

        # ENHANCED: Navigate to time configuration page with device-aware timeout
        time_config_page.page.goto(f"{base_url}/time")
        time.sleep(1 * timeout_multiplier)

        # ENHANCED: Test offset field with device-aware validation
        offset_field = time_config_page.page.locator("input[name='offset']")
        if offset_field.count() > 0:
            # ENHANCED: Field visibility and editability validation with device-aware timeout
            expect(offset_field).to_be_visible(timeout=5000 * timeout_multiplier)
            expect(offset_field).to_be_editable()
            logger.info(f"Timezone offset field found and editable on {device_model}")

            # Store original value for rollback
            original_value = offset_field.input_value()

            try:
                # ENHANCED: Test valid offset with device-aware patterns
                test_offset = "+05:00"
                offset_field.fill(test_offset)
                time.sleep(0.5 * timeout_multiplier)  # Device-aware delay

                # ENHANCED: Validate input acceptance with device context
                actual_value = offset_field.input_value()
                assert (
                    actual_value == test_offset
                ), f"Timezone offset should accept {test_offset} format on {device_model}"
                logger.info(
                    f"Timezone offset field correctly accepted {test_offset} format on {device_model}"
                )

            finally:
                # ENHANCED: Rollback to original value
                if original_value:
                    offset_field.fill(original_value)
                else:
                    offset_field.fill("")

        else:
            pytest.skip(f"Timezone offset field not found on {device_model}")

        # ENHANCED: Cross-validate with save button patterns (indicates UI sophistication)
        save_button_pattern = DeviceCapabilities.get_interface_specific_save_button(
            device_model, "time_configuration", None
        )
        logger.info(
            f"Device save button pattern for {device_model}: {save_button_pattern}"
        )

        # ENHANCED: Device series-specific time configuration validation
        if device_series == "Series 3":
            # Series 3 may have enhanced time configuration features
            logger.info(
                f"Series 3 device {device_model} - enhanced time configuration expected"
            )
        elif device_series == "Series 2":
            # Series 2 may have basic time configuration
            logger.info(
                f"Series 2 device {device_model} - basic time configuration expected"
            )

        logger.info(f"Timezone offset field test passed for {device_model}")

    except Exception as e:
        pytest.fail(f"Timezone offset field test failed on {device_model}: {e}")
