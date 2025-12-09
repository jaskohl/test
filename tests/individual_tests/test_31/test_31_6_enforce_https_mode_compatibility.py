"""
Test 31.6: HTTPS Enforcement Mode Compatibility (Device )
Category: 31 - HTTPS Enforcement Scenarios
Extracted from: tests/grouped/test_31_https_enforcement_scenarios.py
Source Method: TestHTTPSEnforcementConfigurationValidation.test_31_6_enforce_https_mode_compatibility
Individual test file for better test isolation and debugging.
: DeviceCapabilities integration with device-aware compatibility validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.access_config_page import AccessConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("target_mode", ["NEVER", "CFG_ONLY", "ALWAYS"])
def test_31_6_enforce_https_mode_compatibility(
    access_config_page: AccessConfigPage, target_mode: str, base_url: str, request
):
    """
    Test 31.6: HTTPS Enforcement Mode Compatibility (Device )
    Purpose: Verify device correctly reports compatibility with different HTTPS modes with device-aware patterns
    Expected: Device allows configuration of any valid HTTPS enforcement mode
    : DeviceCapabilities integration with device-aware validation
    WARNING: This test reads current configuration but does not modify it.
    Series: Both Series 2 and 3
    """
    # : Use request.session.device_hardware_model for device detection
    device_model = request.session.device_hardware_model
    if device_model == "Unknown":
        pytest.fail("Device model not detected - cannot determine HTTPS capabilities")

    device_series = DeviceCapabilities.get_series(device_model)

    try:
        # : Check if this is a Series 3 device - HTTPS enforcement typically applies to Series 3
        if device_series != "Series 3":
            pytest.skip("HTTPS enforcement tests apply to Series 3 devices")

        # : Apply timeout multiplier for device-aware testing
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
        logger.info(
            f"Testing HTTPS mode compatibility for '{target_mode}' on {device_model} with {timeout_multiplier}x timeout multiplier"
        )

        # Navigate to access configuration page with device-aware timeout
        access_config_page.page.goto(f"{base_url}/access")
        time.sleep(1 * timeout_multiplier)

        # : Verify device has HTTPS enforcement capability
        has_https_capability = DeviceCapabilities.has_capability(
            device_model, "https_enforcement"
        )
        if not has_https_capability:
            pytest.skip(f"Device {device_model} does not support HTTPS enforcement")

        # : Verify the target mode is supported by the device with device-aware validation
        available_modes = access_config_page.get_available_https_modes()
        mode_values = [mode["value"] for mode in available_modes]
        assert (
            target_mode in mode_values
        ), f"Device {device_model} should support HTTPS enforcement mode '{target_mode}'"

        # : Verify the mode has a proper description with device context
        mode_info = next(
            (mode for mode in available_modes if mode["value"] == target_mode), None
        )
        assert (
            mode_info is not None
        ), f"Should find information for mode '{target_mode}' on {device_model}"
        assert "text" in mode_info, f"Mode '{target_mode}' should have text description"
        assert (
            len(mode_info["text"]) > 0
        ), f"Mode '{target_mode}' should have non-empty description for {device_model}"

        # : Log device-specific compatibility information
        logger.info(
            f"HTTPS enforcement mode '{target_mode}' is supported on {device_model}: '{mode_info['text']}'"
        )

        # : Cross-validate with DeviceCapabilities save button patterns
        save_button_pattern = DeviceCapabilities.get_interface_specific_save_button(
            device_model, "access_configuration", None
        )
        logger.info(
            f"Device save button pattern for {device_model}: {save_button_pattern}"
        )

        # : Validate series-specific behavior for HTTPS enforcement
        if device_series == "Series 3":
            # Series 3 should have full HTTPS enforcement capabilities
            assert (
                len(available_modes) >= 3
            ), f"Series 3 device should support multiple HTTPS modes"
            logger.info(
                f"Series 3 device {device_model} supports {len(available_modes)} HTTPS enforcement modes"
            )
        elif device_series == "Series 2":
            # Series 2 may have limited HTTPS enforcement support
            logger.info(
                f"Series 2 device {device_model} has limited HTTPS enforcement support"
            )

    except Exception as e:
        pytest.fail(
            f"HTTPS enforcement mode compatibility test failed for mode '{target_mode}' on {device_model}: {e}"
        )
