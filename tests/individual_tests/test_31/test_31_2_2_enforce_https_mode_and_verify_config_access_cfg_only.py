"""
Test 31 2 2 Enforce Https Mode And Verify Config Access Cfg Only
Category: 31 - Tests\Test 31 Https Enforcement Scenarios
Extracted from: tests\test_31_https_enforcement_scenarios.py
Source Class: TestHTTPSEnforcementScenarios
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect


def test_31_2_2_enforce_https_mode_and_verify_config_access_cfg_only(
    access_config_page,
    device_ip: str,
    device_capabilities: dict,
):
    """
    Test 31.2.2: HTTPS Enforcement Mode Configuration and Config Access - CFG_ONLY Mode
    Purpose: Configure HTTPS enforcement mode to CFG_ONLY and verify config access uses HTTPS
    Expected: Configuration accessible via HTTPS when enforcement is set to CFG_ONLY
    """
    import time

    try:
        # Check if this is a Series 3 device - HTTPS enforcement typically applies to Series 3
        if not device_capabilities.get("series") == "3":
            pytest.skip("HTTPS enforcement tests apply to Series 3 devices")

        print(f"Testing config access for HTTPS enforcement mode: CFG_ONLY")
        # Configure the target HTTPS enforcement mode
        print(f"Ensuring HTTPS enforcement is set to: CFG_ONLY")
        success = access_config_page.configure_https_enforcement("CFG_ONLY")
        if not success:
            pytest.fail("Failed to configure HTTPS enforcement mode to CFG_ONLY")
        # Save the configuration
        save_success = access_config_page.save_configuration()
        if not save_success:
            pytest.fail("Failed to save HTTPS enforcement configuration")
        # Calculate expected protocol for config based on enforcement mode
        expected_config_protocol = "https"  # Config requires HTTPS in CFG_ONLY
        print(
            f"Expected config protocol for mode 'CFG_ONLY': {expected_config_protocol}"
        )
        # Wait for configuration to take effect
        time.sleep(3)
        # Test config access with the expected protocol
        config_url = f"{expected_config_protocol}://{device_ip}/login"
        print(f"Attempting to access config with URL: {config_url}")
        # Navigate to config using the expected protocol
        try:
            # For CFG_ONLY mode, test that HTTPS works for config
            access_config_page.page.goto(
                config_url, timeout=30000, wait_until="domcontentloaded"
            )
            assert access_config_page.page.url.startswith(
                "https://"
            ), "Configuration should be accessible via HTTPS for 'CFG_ONLY' mode"
            print(f" Configuration correctly accessible via HTTPS for mode 'CFG_ONLY'")
        except Exception as e:
            pytest.fail(
                f"Failed to access configuration with expected protocol for mode 'CFG_ONLY': {e}"
            )
    except Exception as e:
        pytest.fail(
            f"HTTPS enforcement config access test failed for mode 'CFG_ONLY': {e}"
        )
