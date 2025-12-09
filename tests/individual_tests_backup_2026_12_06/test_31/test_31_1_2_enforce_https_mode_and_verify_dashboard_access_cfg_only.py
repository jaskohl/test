"""
Test 31 1 2 Enforce Https Mode And Verify Dashboard Access Cfg Only
Category: 31 - Tests\Test 31 Https Enforcement Scenarios
Extracted from: tests\test_31_https_enforcement_scenarios.py
Source Class: TestHTTPSEnforcementScenarios
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect


def test_31_1_2_enforce_https_mode_and_verify_dashboard_access_cfg_only(
    access_config_page,
    device_ip: str,
    device_capabilities: dict,
):
    """
    Test 31.1.2: HTTPS Enforcement Mode Configuration and Dashboard Access - CFG_ONLY Mode
    Purpose: Configure HTTPS enforcement mode to CFG_ONLY and verify dashboard access uses HTTP
    Expected: Dashboard accessible via HTTP when enforcement is set to CFG_ONLY
    """
    import time

    try:
        # Check if this is a Series 3 device - HTTPS enforcement typically applies to Series 3
        if not device_capabilities.get("series") == "3":
            pytest.skip("HTTPS enforcement tests apply to Series 3 devices")

        print(f"Testing HTTPS enforcement mode: CFG_ONLY")
        # Configure the target HTTPS enforcement mode
        print(f"Setting HTTPS enforcement to: CFG_ONLY")
        success = access_config_page.configure_https_enforcement("CFG_ONLY")
        if not success:
            pytest.fail("Failed to configure HTTPS enforcement mode to CFG_ONLY")
        # Save the configuration
        save_success = access_config_page.save_configuration()
        if not save_success:
            pytest.fail("Failed to save HTTPS enforcement configuration")
        # Calculate expected protocol for dashboard based on enforcement mode
        expected_dashboard_protocol = "http"  # Dashboard allows HTTP in CFG_ONLY
        print(
            f"Expected dashboard protocol for mode 'CFG_ONLY': {expected_dashboard_protocol}"
        )
        # Wait for configuration to take effect
        time.sleep(3)
        # Test dashboard access with the expected protocol
        dashboard_url = f"{expected_dashboard_protocol}://{device_ip}/"
        print(f"Attempting to access dashboard with URL: {dashboard_url}")
        # Navigate to dashboard using the expected protocol
        try:
            # For CFG_ONLY mode, test that HTTP works for dashboard
            access_config_page.page.goto(
                dashboard_url, timeout=30000, wait_until="domcontentloaded"
            )
            assert access_config_page.page.url.startswith(
                "http://"
            ), "Dashboard should be accessible via HTTP for 'CFG_ONLY' mode"
            print(f" Dashboard correctly accessible via HTTP for mode 'CFG_ONLY'")
        except Exception as e:
            pytest.fail(
                f"Failed to access dashboard with expected protocol for mode 'CFG_ONLY': {e}"
            )
    except Exception as e:
        pytest.fail(
            f"HTTPS enforcement dashboard access test failed for mode 'CFG_ONLY': {e}"
        )
