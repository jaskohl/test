"""
Test 31.8: Protocol Policy Consistency Check
Category: 31 - HTTPS Enforcement Scenarios
Extracted from: tests/grouped/test_31_https_enforcement_scenarios.py
Source Method: TestHTTPSEnforcementDeviceCompliance.test_31_8_protocol_policy_consistency_check
Individual test file for better test isolation and debugging.
"""

import pytest


def test_31_8_protocol_policy_consistency_check(device_capabilities: dict):
    """
    Test 31.8: Protocol Policy Consistency Check
    Purpose: Verify device protocol settings are internally consistent
    Expected: Protocol settings align with detected HTTPS enforcement mode
    This test validates logical consistency of detected settings.
    Series: Both Series 2 and 3
    """
    https_mode = device_capabilities.get("https_enforcement", "UNKNOWN")
    dashboard_protocol = device_capabilities.get("dashboard_protocol", "https")
    config_protocol = device_capabilities.get("config_protocol", "https")
    # Check consistency based on HTTPS enforcement mode
    if https_mode == "NEVER":
        # Both protocols should allow HTTP
        assert (
            dashboard_protocol == "http"
        ), "NEVER mode should allow HTTP for dashboard"
        assert config_protocol == "http", "NEVER mode should allow HTTP for config"
    elif https_mode == "CFG_ONLY":
        # HTTP for dashboard, HTTPS for config
        assert (
            dashboard_protocol == "http"
        ), "CFG_ONLY mode should allow HTTP for dashboard"
        assert (
            config_protocol == "https"
        ), "CFG_ONLY mode should require HTTPS for config"
    elif https_mode == "ALWAYS":
        # HTTPS for both
        assert (
            dashboard_protocol == "https"
        ), "ALWAYS mode should require HTTPS for dashboard"
        assert config_protocol == "https", "ALWAYS mode should require HTTPS for config"
    print(f"Protocol policy consistency validated for mode '{https_mode}':")
    print(f"  Dashboard: {dashboard_protocol} ")
    print(f"  Config: {config_protocol} ")
