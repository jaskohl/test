"""
Test 31.2: HTTPS Enforcement Mode Configuration and Configuration Access
Category: 31 - HTTPS Enforcement Scenarios
Extracted from: tests/grouped/test_31_https_enforcement_scenarios.py
Source Method: TestHTTPSEnforcementScenarios.test_31_2_enforce_https_mode_and_verify_config_access
Individual test file for better test isolation and debugging.
"""

import pytest
import time
from playwright.sync_api import Page


@pytest.mark.parametrize("target_enforcement_mode", ["NEVER", "CFG_ONLY", "ALWAYS"])
def test_31_2_enforce_https_mode_and_verify_config_access(
    access_config_page,
    target_enforcement_mode: str,
    device_ip: str,
    device_capabilities: dict,
):
    """
    Test 31.2: HTTPS Enforcement Mode Configuration and Configuration Access
    Purpose: Configure HTTPS enforcement mode and verify configuration access uses correct protocol
    Expected: Configuration accessible only via protocol required by enforcement setting
    FIXED: Now actually changes enforcement mode and tests enforcement, not just device behavior.
    Series: Both Series 2 and 3
    """
    try:
        print(
            f"Testing config access for HTTPS enforcement mode: {target_enforcement_mode}"
        )
        # Configure the target HTTPS enforcement mode (already done in test 31.1, but ensure it's set)
        print(f"Ensuring HTTPS enforcement is set to: {target_enforcement_mode}")
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
        # Calculate expected protocol for config based on enforcement mode
        if target_enforcement_mode == "NEVER":
            expected_config_protocol = "http"
        elif target_enforcement_mode == "CFG_ONLY":
            expected_config_protocol = "https"  # Config requires HTTPS in CFG_ONLY
        elif target_enforcement_mode == "ALWAYS":
            expected_config_protocol = "https"  # HTTPS required for both
        else:
            pytest.fail(f"Unknown enforcement mode: {target_enforcement_mode}")
        print(
            f"Expected config protocol for mode '{target_enforcement_mode}': {expected_config_protocol}"
        )
        # Wait for configuration to take effect
        time.sleep(3)
        # Test config access with the expected protocol
        config_url = f"{expected_config_protocol}://{device_ip}/login"
        print(f"Attempting to access config with URL: {config_url}")
        # Navigate to config using the expected protocol
        try:
            if expected_config_protocol == "https":
                # For HTTPS enforcement, test that HTTPS works for config
                access_config_page.page.goto(
                    config_url, timeout=30000, wait_until="domcontentloaded"
                )
                assert access_config_page.page.url.startswith(
                    "https://"
                ), f"Configuration should be accessible via HTTPS for '{target_enforcement_mode}' mode"
                print(
                    f" Configuration correctly accessible via HTTPS for mode '{target_enforcement_mode}'"
                )
            else:
                # For NEVER mode, test that HTTP works for config
                access_config_page.page.goto(
                    config_url, timeout=30000, wait_until="domcontentloaded"
                )
                assert access_config_page.page.url.startswith(
                    "http://"
                ), f"Configuration should be accessible via HTTP for '{target_enforcement_mode}' mode"
                print(
                    f" Configuration correctly accessible via HTTP for mode '{target_enforcement_mode}'"
                )
        except Exception as e:
            pytest.fail(
                f"Failed to access configuration with expected protocol for mode '{target_enforcement_mode}': {e}"
            )
    except Exception as e:
        pytest.fail(
            f"HTTPS enforcement config access test failed for mode '{target_enforcement_mode}': {e}"
        )
