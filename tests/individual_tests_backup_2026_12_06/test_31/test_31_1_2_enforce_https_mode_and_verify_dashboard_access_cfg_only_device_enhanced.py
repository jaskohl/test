"""
Test 31 1 2 Enforce Https Mode And Verify Dashboard Access Cfg Only (Device Enhanced)
Category: 31 - HTTPS Enforcement Scenarios
Extracted from: tests\test_31_https_enforcement_scenarios.py
Source Class: TestHTTPSEnforcementScenarios
Individual test file for better test isolation and debugging.
ENHANCED: DeviceCapabilities integration with timeout multipliers and device-aware patterns
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.access_config_page import AccessConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_31_1_2_enforce_https_mode_and_verify_dashboard_access_cfg_only_device_enhanced(
    access_config_page: AccessConfigPage, base_url: str, request
):
    """
    Test 31.1.2: HTTPS Enforcement Mode Configuration and Dashboard Access - CFG_ONLY Mode (Device Enhanced)
    Purpose: Configure HTTPS enforcement mode to CFG_ONLY and verify dashboard access uses HTTP with device-aware patterns
    Expected: Dashboard accessible via HTTP when enforcement is set to CFG_ONLY
    ENHANCED: DeviceCapabilities integration with timeout multipliers
    """
    # ENHANCED: Use request.session.device_hardware_model for device detection
    device_model = request.session.device_hardware_model
    if device_model == "Unknown":
        pytest.fail("Device model not detected - cannot determine HTTPS capabilities")

    device_series = DeviceCapabilities.get_series(device_model)

    try:
        # ENHANCED: Check if this is a Series 3 device - HTTPS enforcement typically applies to Series 3
        if device_series != "Series 3":
            pytest.skip("HTTPS enforcement tests apply to Series 3 devices")

        # ENHANCED: Apply timeout multiplier for device-aware testing
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
        logger.info(
            f"Testing HTTPS enforcement mode CFG_ONLY on {device_model} with {timeout_multiplier}x timeout multiplier"
        )

        print(f"Testing HTTPS enforcement mode: CFG_ONLY")
        # Configure the target HTTPS enforcement mode with device-aware navigation
        access_config_page.page.goto(f"{base_url}/access")
        time.sleep(1 * timeout_multiplier)

        print(f"Setting HTTPS enforcement to: CFG_ONLY")
        success = access_config_page.configure_https_enforcement("CFG_ONLY")
        if not success:
            pytest.fail("Failed to configure HTTPS enforcement mode to CFG_ONLY")

        # Save the configuration with device-aware timeout
        save_success = access_config_page.save_configuration()
        if not save_success:
            pytest.fail("Failed to save HTTPS enforcement configuration")

        # Calculate expected protocol for dashboard based on enforcement mode
        expected_dashboard_protocol = "http"  # Dashboard allows HTTP in CFG_ONLY
        logger.info(
            f"Expected dashboard protocol for mode 'CFG_ONLY': {expected_dashboard_protocol}"
        )

        # Wait for configuration to take effect (device-aware)
        time.sleep(3 * timeout_multiplier)

        # Test dashboard access with the expected protocol
        dashboard_url = f"{expected_dashboard_protocol}://{base_url.split('//')[-1]}/"
        logger.info(f"Attempting to access dashboard with URL: {dashboard_url}")

        # Navigate to dashboard using the expected protocol (device-aware timeout)
        try:
            # For CFG_ONLY mode, test that HTTP works for dashboard
            access_config_page.page.goto(
                dashboard_url,
                timeout=30000 * timeout_multiplier,
                wait_until="domcontentloaded",
            )

            # ENHANCED: Device-aware validation of protocol enforcement
            actual_protocol = (
                "https"
                if access_config_page.page.url.startswith("https://")
                else "http"
            )
            assert (
                actual_protocol == "http"
            ), f"Dashboard should be accessible via HTTP for 'CFG_ONLY' mode, got {actual_protocol}"

            logger.info(f"Dashboard correctly accessible via HTTP for mode 'CFG_ONLY'")
        except Exception as e:
            pytest.fail(
                f"Failed to access dashboard with expected protocol for mode 'CFG_ONLY': {e}"
            )
    except Exception as e:
        pytest.fail(
            f"HTTPS enforcement dashboard access test failed for mode 'CFG_ONLY': {e}"
        )
