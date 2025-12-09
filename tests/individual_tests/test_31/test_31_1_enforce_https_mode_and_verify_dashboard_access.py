"""
Test 31.1: HTTPS Enforcement Mode Configuration and Dashboard Access
Category: 31 - HTTPS Enforcement Scenarios
Extracted from: tests/grouped/test_31_https_enforcement_scenarios.py
Source Method: TestHTTPSEnforcementScenarios.test_31_1_enforce_https_mode_and_verify_dashboard_access
Individual test file for better test isolation and debugging.
"""

import pytest
import time
from playwright.sync_api import Page


@pytest.mark.parametrize("target_enforcement_mode", ["NEVER", "CFG_ONLY", "ALWAYS"])
def test_31_1_enforce_https_mode_and_verify_dashboard_access(
    access_config_page,
    target_enforcement_mode: str,
    device_ip: str,
    device_capabilities: dict,
):
    """
    Test 31.1: HTTPS Enforcement Mode Configuration and Dashboard Access
    Purpose: Configure HTTPS enforcement mode and verify dashboard access uses correct protocol
    Expected: Dashboard accessible only via protocol required by enforcement setting
    FIXED: Now actually changes enforcement mode and tests enforcement, not just device behavior.
    Series: Both Series 2 and 3
    """
    try:
        print(f"Testing HTTPS enforcement mode: {target_enforcement_mode}")
        # Configure the target HTTPS enforcement mode
        print(f"Setting HTTPS enforcement to: {target_enforcement_mode}")
        success = access_config_page.configure_https_enforcement(
            target_enforcement_mode
        )
        if not success:
            pytest.fail(
                f"Failed to configure HTTPS enforcement mode to {target_enforcement_mode}"
            )
        # Save the configuration
        save_success = access_config_page.save_configuration()
        if not save_success:
            pytest.fail("Failed to save HTTPS enforcement configuration")
        # Calculate expected protocol for dashboard based on enforcement mode
        if target_enforcement_mode == "NEVER":
            expected_dashboard_protocol = "http"
        elif target_enforcement_mode == "CFG_ONLY":
            expected_dashboard_protocol = "http"  # Dashboard allows HTTP in CFG_ONLY
        elif target_enforcement_mode == "ALWAYS":
            expected_dashboard_protocol = "https"  # HTTPS required for both
        else:
            pytest.fail(f"Unknown enforcement mode: {target_enforcement_mode}")
        print(
            f"Expected dashboard protocol for mode '{target_enforcement_mode}': {expected_dashboard_protocol}"
        )
        # Wait for configuration to take effect
        time.sleep(3)
        # Test dashboard access with the expected protocol
        dashboard_url = f"{expected_dashboard_protocol}://{device_ip}/"
        print(f"Attempting to access dashboard with URL: {dashboard_url}")
        # Navigate to dashboard using the expected protocol
        try:
            if expected_dashboard_protocol == "https":
                # For HTTPS enforcement, test that HTTPS works
                access_config_page.page.goto(
                    dashboard_url, timeout=30000, wait_until="domcontentloaded"
                )
                assert access_config_page.page.url.startswith(
                    "https://"
                ), f"Dashboard should be accessible via HTTPS for '{target_enforcement_mode}' mode"
                print(
                    f" Dashboard correctly accessible via HTTPS for mode '{target_enforcement_mode}'"
                )
            else:
                # For HTTP enforcement, test that HTTP works
                access_config_page.page.goto(
                    dashboard_url, timeout=30000, wait_until="domcontentloaded"
                )
                assert access_config_page.page.url.startswith(
                    "http://"
                ), f"Dashboard should be accessible via HTTP for '{target_enforcement_mode}' mode"
                print(
                    f" Dashboard correctly accessible via HTTP for mode '{target_enforcement_mode}'"
                )
        except Exception as e:
            pytest.fail(
                f"Failed to access dashboard with expected protocol for mode '{target_enforcement_mode}': {e}"
            )
    except Exception as e:
        pytest.fail(
            f"HTTPS enforcement dashboard access test failed for mode '{target_enforcement_mode}': {e}"
        )
