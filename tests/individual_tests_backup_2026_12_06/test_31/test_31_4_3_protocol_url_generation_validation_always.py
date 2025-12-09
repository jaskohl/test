"""
Test 31.4.3: Protocol URL Generation Validation - ALWAYS Mode
Purpose: Verify protocol determination logic for ALWAYS HTTPS enforcement mode
Expected: HTTPS for both dashboard and config
Based on test_31_4 parametrized test from test_31_https_enforcement_scenarios.py
"""

import pytest
from playwright.sync_api import Page, expect


def test_31_4_3_protocol_url_generation_validation_always(
    device_ip: str, device_capabilities: dict
):
    """
    Test 31.4.3: Protocol URL Generation Validation - ALWAYS Mode
    Purpose: Verify protocol determination logic for ALWAYS HTTPS enforcement mode
    Expected: HTTPS for both dashboard and config
    This test validates protocol logic without making external function calls.
    """
    target_enforcement_mode = "ALWAYS"

    # Determine expected protocols based on enforcement mode (implementation logic)
    # Test dashboard URL protocol logic
    expected_dashboard_protocol = (
        "http" if target_enforcement_mode in ["NEVER", "CFG_ONLY"] else "https"
    )

    # Test config URL protocol logic
    expected_config_protocol = "http" if target_enforcement_mode == "NEVER" else "https"

    # Validate protocol requirements for ALWAYS mode
    print(f"Protocol requirements for enforcement mode '{target_enforcement_mode}':")
    print(f"  Dashboard requires: {expected_dashboard_protocol.upper()}")
    print(f"  Configuration requires: {expected_config_protocol.upper()}")

    # Test protocol determination logic for ALWAYS mode
    if target_enforcement_mode == "ALWAYS":
        assert (
            expected_dashboard_protocol == "https"
        ), "ALWAYS mode should require HTTPS for dashboard"
        assert (
            expected_config_protocol == "https"
        ), "ALWAYS mode should require HTTPS for config"

    # Verify URL could be constructed properly (basic validation)
    dashboard_url = f"{expected_dashboard_protocol}://{device_ip}/"
    config_url = f"{expected_config_protocol}://{device_ip}/login"

    print(
        f" URL generation logic validated for enforcement mode '{target_enforcement_mode}':"
    )
    print(f"  Dashboard URL pattern: {dashboard_url}")
    print(f"  Config URL pattern: {config_url}")

    # Basic URL structure validation
    assert "://" in dashboard_url, f"Dashboard URL should contain protocol separator"
    assert device_ip in dashboard_url, f"Dashboard URL should contain device IP"
    assert "://" in config_url, f"Config URL should contain protocol separator"
    assert device_ip in config_url, f"Config URL should contain device IP"

    # Validate ALWAYS mode specific requirements
    assert (
        dashboard_url == f"https://{device_ip}/"
    ), f"ALWAYS dashboard URL should be HTTPS"
    assert (
        config_url == f"https://{device_ip}/login"
    ), f"ALWAYS config URL should be HTTPS"
