"""
Test 31.7: Device HTTPS Policy Detection
Category: 31 - HTTPS Enforcement Scenarios
Extracted from: tests/grouped/test_31_https_enforcement_scenarios.py
Source Method: TestHTTPSEnforcementDeviceCompliance.test_31_7_device_https_policy_detection
Individual test file for better test isolation and debugging.
"""

import pytest


def test_31_7_device_https_policy_detection(
    device_capabilities: dict, access_config_page
):
    """
    Test 31.7: Device HTTPS Policy Detection
    Purpose: Verify device capabilities correctly detect and report HTTPS enforcement
    Expected: Device capabilities include HTTPS enforcement information
    This test validates capability detection rather than enforcement behavior.
    Series: Both Series 2 and 3
    """
    # Verify device capabilities include HTTPS enforcement detection
    assert (
        "https_enforcement" in device_capabilities
    ), "Device capabilities should include HTTPS enforcement detection"
    https_mode = device_capabilities.get("https_enforcement", "UNKNOWN")
    assert (
        https_mode != "UNKNOWN"
    ), "Device should successfully detect HTTPS enforcement mode (not UNKNOWN)"
    assert https_mode in [
        "NEVER",
        "CFG_ONLY",
        "ALWAYS",
    ], f"Detected HTTPS mode '{https_mode}' should be valid"
    # Verify protocol settings based on enforcement
    dashboard_protocol = device_capabilities.get("dashboard_protocol")
    config_protocol = device_capabilities.get("config_protocol")
    assert dashboard_protocol in [
        "http",
        "https",
    ], f"Dashboard protocol '{dashboard_protocol}' should be valid"
    assert config_protocol in [
        "http",
        "https",
    ], f"Config protocol '{config_protocol}' should be valid"
    print("Device HTTPS policy detection:")
    print(f"  Enforcement mode: {https_mode}")
    print(f"  Dashboard protocol: {dashboard_protocol}")
    print(f"  Config protocol: {config_protocol}")
