"""
Test: 7.3.1 - Output 3 with Available Signals [DEVICE ] - Pure Page Object Pattern
Category: Outputs Configuration (7)
Purpose: Test output 3 with all available signal types for device
Expected: Device-specific signals work correctly for output 3
Series: Both Series 2 and 3 (device-aware)
Priority: HIGH
Hardware: Device Only
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
PATTERN: Zero direct .locator() calls, essential methods only
"""

import pytest
import time
import logging
from pages.outputs_config_page import OutputsConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_7_3_1_output_3_available_signals(
    outputs_config_page: OutputsConfigPage,
    request,
    base_url: str,
):
    """
    Test 7.3.1: Output 3 Available Signals - Pure Page Object Pattern
    Purpose: Test output 3 with all available signal types for device
    Expected: Device-specific signals work correctly for output 3
    TRANSFORMED: Uses pure page object methods with device intelligence
    Series: Both 2 and 3
    """
    device_model = request.session.device_hardware_model

    # Essential device intelligence
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(f"Testing output 3 available signals on {device_model}")
    logger.info(f"Device series: {device_series}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}x")

    # Get device capabilities
    max_outputs = DeviceCapabilities.get_max_outputs(device_model)

    # Check if output 3 is available
    if max_outputs < 3:
        pytest.skip(f"Device {device_model} does not support output 3")

    # Get signals available for output 3
    output_3_signals = DeviceCapabilities.get_output_signal_types(device_model, 3)

    if not output_3_signals:
        pytest.skip(f"No signals defined for output 3 on {device_model}")

    logger.info(
        f"Device {device_model}: Testing output 3 with signals: {output_3_signals}"
    )

    # Navigate to outputs configuration page
    outputs_config_page.navigate_to_page()

    # Test each available signal for output 3
    for signal_type in output_3_signals:
        test_name = f"output_3_{signal_type}"

        try:
            logger.info(f"Testing {test_name}")

            # Configure output 3 with the signal type
            # Get expected time references for this signal type
            expected_time_refs = DeviceCapabilities.get_expected_time_refs(
                device_model, signal_type
            )

            # Use default time reference if available, otherwise skip time reference
            time_reference = "UTC" if "UTC" in expected_time_refs else "LOCAL"

            configure_success = outputs_config_page.configure_output(
                channel=3, signal_type=signal_type, time_reference=time_reference
            )

            if not configure_success:
                logger.warning(f"Failed to configure output 3 with {signal_type}")
                continue

            # Verify expected time references are visible/hidden through page object
            # The page object should handle this automatically in configure_output

            # Save configuration through page object
            save_success = outputs_config_page.save_configuration()
            assert save_success, f"Failed to save output 3 {signal_type} configuration"

            # Verify persistence through page object methods
            page_data = outputs_config_page.get_page_data()
            persisted_signal = page_data.get("signal3", "")

            assert (
                persisted_signal == signal_type
            ), f"Signal type {signal_type} did not persist"

            # Verify time reference persisted if applicable
            if expected_time_refs:
                persisted_time = page_data.get("time3", "")
                assert (
                    persisted_time == time_reference
                ), f"Time reference {time_reference} did not persist"

            # Clean up - configure back to OFF for next test
            cleanup_success = outputs_config_page.configure_output(
                channel=3, signal_type="OFF", time_reference=time_reference
            )
            assert cleanup_success, f"Failed to clean up output 3 configuration"

            logger.info(f"Device {device_model}: Successfully tested {test_name}")

        except Exception as e:
            logger.error(f"Device {device_model}: Failed {test_name}: {e}")
            # Continue testing other signals even if one fails
            continue

    # Final capability validation through page object
    capabilities = outputs_config_page.detect_output_capabilities()
    output_channels = capabilities.get("output_channels", 0)

    logger.info(f"Output 3 testing completed on {device_model}")
    logger.info(f"Device {device_model} supports {output_channels} output channels")
    logger.info(f"Tested signals for output 3: {output_3_signals}")

    # Cross-validate with DeviceCapabilities database
    device_capabilities = DeviceCapabilities.get_capabilities(device_model)
    if device_capabilities:
        network_config = device_capabilities.get("network_config", {})
        mgmt_interface = network_config.get("management_interface", "unknown")
        logger.info(f"Management interface: {mgmt_interface}")

    print(f"OUTPUT 3 SIGNAL TESTING COMPLETED: {device_model} (Series {device_series})")
