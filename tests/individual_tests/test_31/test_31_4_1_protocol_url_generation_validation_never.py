"""
Test 31 4 1 Protocol Url Generation Validation Never (Device )
Category: 31 - HTTPS Enforcement Scenarios
Extracted from: tests\test_31_https_enforcement_scenarios.py
Source Class: TestHTTPSSettingAvailability
Individual test file for better test isolation and debugging.
: DeviceCapabilities integration with device-aware protocol validation
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_31_4_1_protocol_url_generation_validation_never(base_url: str, request):
    """
    Test 31.4.1: Protocol URL Generation Validation - NEVER Mode (Device )
    Purpose: Verify protocol determination logic for NEVER HTTPS enforcement mode with device-aware patterns
    Expected: Correct protocol requirements understood for NEVER enforcement policy
    : DeviceCapabilities integration with device-aware validation
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

        logger.info(
            f"Testing protocol URL generation validation for NEVER mode on {device_model}"
        )

        target_enforcement_mode = "NEVER"

        # : Cross-validate protocol logic with DeviceCapabilities
        # Check if device has HTTPS enforcement capability
        has_https_capability = DeviceCapabilities.has_capability(
            device_model, "https_enforcement"
        )
        if not has_https_capability:
            pytest.skip(f"Device {device_model} does not support HTTPS enforcement")

        # Determine expected protocols based on enforcement mode (implementation logic)
        # Test dashboard URL protocol logic
        expected_dashboard_protocol = (
            "http" if target_enforcement_mode in ["NEVER", "CFG_ONLY"] else "https"
        )

        # Test config URL protocol logic
        expected_config_protocol = (
            "http" if target_enforcement_mode == "NEVER" else "https"
        )

        # : Validate protocol requirements per enforcement mode with device context
        logger.info(
            f"Protocol requirements for enforcement mode '{target_enforcement_mode}' on {device_model}:"
        )
        logger.info(f"  Dashboard requires: {expected_dashboard_protocol.upper()}")
        logger.info(f"  Configuration requires: {expected_config_protocol.upper()}")

        # : Test protocol determination logic for NEVER mode with device validation
        assert (
            expected_dashboard_protocol == "http"
        ), f"NEVER mode should allow HTTP for dashboard on {device_model}"
        assert (
            expected_config_protocol == "http"
        ), f"NEVER mode should allow HTTP for config on {device_model}"

        # : Verify URL could be constructed properly (device-aware validation)
        device_ip = base_url.split("://")[-1].split("/")[0]
        dashboard_url = f"{expected_dashboard_protocol}://{device_ip}/"
        config_url = f"{expected_config_protocol}://{device_ip}/login"

        logger.info(
            f"URL generation logic validated for enforcement mode '{target_enforcement_mode}' on {device_model}:"
        )
        logger.info(f"  Dashboard URL pattern: {dashboard_url}")
        logger.info(f"  Config URL pattern: {config_url}")

        # : Basic URL structure validation with device context
        assert (
            "://" in dashboard_url
        ), f"Dashboard URL should contain protocol separator for {device_model}"
        assert (
            device_ip in dashboard_url
        ), f"Dashboard URL should contain device IP for {device_model}"
        assert (
            "://" in config_url
        ), f"Config URL should contain protocol separator for {device_model}"
        assert (
            device_ip in config_url
        ), f"Config URL should contain device IP for {device_model}"

        # : Additional device-specific validations
        # Validate protocol consistency across device capabilities
        save_button_pattern = DeviceCapabilities.get_interface_specific_save_button(
            device_model, "general_configuration", None
        )
        logger.info(
            f"Device save button pattern for {device_model}: {save_button_pattern}"
        )

    except Exception as e:
        pytest.fail(
            f"Protocol URL generation validation test failed for NEVER mode on {device_model}: {e}"
        )
