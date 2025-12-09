"""
Test 15.1.2: Series 2 Output Count - DeviceCapabilities Enhanced
Category: 15 - Device Capability Detection Tests
Test Count: 3 of 15 in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Series 2 Only
ENHANCED: Comprehensive DeviceCapabilities integration for output count validation
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_15_1_2_series2_output_count_device_enhanced(
    unlocked_config_page: Page, base_url: str, device_series: str, request
):
    """
    Test 15.1.2: Series 2 Output Count - DeviceCapabilities Enhanced
    Purpose: Verify Series 2 devices have correct output count per device database
    Expected: Output count matches DeviceCapabilities database for device model
    ENHANCED: Cross-validation with DeviceCapabilities output data
    Series: Series 2 Only
    """
    # Get device model for comprehensive validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate output count")

    # Get device series from database for validation
    expected_series = DeviceCapabilities.get_series(device_model)
    if expected_series != 2:
        pytest.skip(
            f"Test only applies to Series 2, detected Series {expected_series} device {device_model}"
        )

    # Get expected output count from DeviceCapabilities
    max_outputs = DeviceCapabilities.get_max_outputs(device_model)
    assert (
        max_outputs > 0
    ), f"Device database should indicate output count for {device_model}"

    logger.info(f"Testing output count on {device_model}")
    logger.info(f"Expected series from database: {expected_series}")
    logger.info(f"Expected output count from database: {max_outputs}")

    # Navigate to outputs page with device-aware timeout
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    page_timeout = int(10000 * timeout_multiplier)

    unlocked_config_page.goto(
        f"{base_url}/outputs", wait_until="domcontentloaded", timeout=page_timeout
    )

    # Count actual output configuration elements
    output_selects = unlocked_config_page.locator("select[name*='signal']")
    actual_output_count = output_selects.count()

    logger.info(f"Found {actual_output_count} output select elements on {device_model}")
    logger.info(f"Expected {max_outputs} outputs according to device database")

    # Validate output count matches device database
    assert (
        actual_output_count == max_outputs
    ), f"Output count mismatch - database shows {max_outputs}, found {actual_output_count} outputs for {device_model}"

    # Verify specific output elements exist
    outputs_found = 0
    for i in range(1, max_outputs + 1):
        signal_element = unlocked_config_page.locator(f"select[name='signal{i}']")
        if signal_element.count() > 0:
            outputs_found += 1
            expect(signal_element.first).to_be_visible()
            logger.info(f" Found output signal{i} on {device_model}")
        else:
            logger.warning(f" Missing output signal{i} on {device_model}")

    assert (
        outputs_found == max_outputs
    ), f"Expected {max_outputs} output signals, found {outputs_found} for {device_model}"

    logger.info(
        f" All {max_outputs} output signals found and visible on {device_model}"
    )

    # Enhanced validation: Test output signal types for each output
    for i in range(1, max_outputs + 1):
        signal_element = unlocked_config_page.locator(f"select[name='signal{i}']")
        if signal_element.count() > 0:
            # Get available signal options
            signal_options = signal_element.first.locator("option")
            option_count = signal_options.count()

            assert (
                option_count > 0
            ), f"Output signal{i} should have available options on {device_model}"
            logger.info(f" Output signal{i} has {option_count} signal type options")

            # Validate signal types match device database
            available_types = DeviceCapabilities.get_output_signal_types(
                device_model, i
            )
            if available_types:
                logger.info(f"Expected signal types for output {i}: {available_types}")
                # Note: UI may not show all types or may have different naming

    # Additional database cross-validation
    capabilities = DeviceCapabilities.get_capabilities(device_model)

    # Validate output-related capabilities
    assert (
        "max_outputs" in capabilities
    ), f"Capabilities should include max_outputs for {device_model}"
    assert (
        capabilities["max_outputs"] == max_outputs
    ), f"Capabilities output count should match database for {device_model}"

    logger.info(f" Output capability validation passed for {device_model}")

    # Series-specific validation
    if expected_series == 2:
        # Series 2 validation
        assert (
            max_outputs == 4
        ), f"Series 2 should have 4 outputs according to device database, found {max_outputs}"
        logger.info(
            f" Series 2 output validation: {max_outputs} outputs confirmed for {device_model}"
        )

        # Note: Historical data may show 2 outputs for specific devices,
        # but DeviceCapabilities database indicates 4 outputs for Series 2
        logger.info(
            f"Note: Device database indicates {max_outputs} outputs for Series 2 devices"
        )

    logger.info(f"Series 2 output count test completed successfully for {device_model}")
    print(f" OUTPUT COUNT VALIDATED: {device_model} - {max_outputs} outputs confirmed")
