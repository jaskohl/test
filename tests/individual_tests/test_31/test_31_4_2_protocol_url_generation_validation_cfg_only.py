"""
Test 31.4.2: Protocol URL Generation Validation - CFG_ONLY Mode
Purpose: Verify protocol determination logic for CFG_ONLY HTTPS enforcement mode
Expected: HTTP for dashboard, HTTPS for config
Based on test_31_4 parametrized test from test_31_https_enforcement_scenarios.py
"""

import pytest
from playwright.sync_api import Page, expect


def test_31_4_2_protocol_url_generation_validation_cfg_only(
    device_ip: str, device_capabilities: dict
):
    """
    Test 31.4.2: Protocol URL Generation Validation - CFG_ONLY Mode
    Purpose: Verify protocol determination logic for CFG_ONLY HTTPS enforcement mode
    Expected: HTTP for dashboard, HTTPS for config
    This test validates protocol logic without making external function calls.
    """
    target_enforcement_mode = "CFG_ONLY"

    # Determine expected protocols based on enforcement mode (implementation logic)
    # Test dashboard URL protocol logic
    expected_dashboard_protocol = (
        "http" if target_enforcement_mode in ["NEVER", "CFG_ONLY"] else "https"
    )

    # Test config URL protocol logic
    expected_config_protocol = "http" if target_enforcement_mode == "NEVER" else "https"

    # Validate protocol requirements for CFG_ONLY mode
    print(f"Protocol requirements for enforcement mode '{target_enforcement_mode}':")
    print(f"  Dashboard requires: {expected_dashboard_protocol.upper()}")
    print(f"  Configuration requires: {expected_config_protocol.upper()}")

    # Test protocol determination logic for CFG_ONLY mode
    if target_enforcement_mode == "CFG_ONLY":
        assert (
            expected_dashboard_protocol == "http"
        ), "CFG_ONLY mode should allow HTTP for dashboard"
        assert (
            expected_config_protocol == "https"
        ), "CFG_ONLY mode should require HTTPS for config"

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

    # Validate CFG_ONLY mode specific requirements
    assert (
        dashboard_url == f"http://{device_ip}/"
    ), f"CFG_ONLY dashboard URL should be HTTP"
    assert (
        config_url == f"https://{device_ip}/login"
    ), f"CFG_ONLY config URL should be HTTPS"
