"""
Test 29 8 1 Dynamic Device Detection
Category: 29 - Network Configuration Series3
Extracted from: tests/grouped/test_29_network_config_series3.py
Source Class: TestDynamicDeviceDetection.test_29_8_1_dynamic_device_detection
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page


def test_29_8_1_dynamic_device_detection(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.8.1: Dynamic Device Detection

    Purpose: Test that the system correctly detects available network interfaces based on device model
    Args:
        unlocked_config_page: Playwright page object for the network configuration page
        base_url: Base URL for the application under test
        device_series: Device series information (should be "Series 3")
    Expected:
        - Test should skip on non-Series 3 devices
        - Device should have 5-7 forms available (different Series 3 variants)
        - Should have at least 2 available ethernet ports
        - Should correctly identify available ports based on device capabilities
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # FIXED: Count available forms to determine device type
    # Updated to expect 5-7 forms based on actual device exploration across variants
    forms = unlocked_config_page.locator("form").count() - 1  # Subtract session modal
    assert forms in [
        5,
        6,
        7,
    ]  # Different device variants (UPDATED to include 5, 6, 7)

    # Check what ports are available
    available_ports = []
    for port in ["eth0", "eth1", "eth2", "eth3", "eth4"]:
        if unlocked_config_page.locator(f"input[name='ip_{port}']").count() > 0:
            available_ports.append(port)
    assert len(available_ports) >= 2  # Should have at least 2 ethernet ports

    print(f"Detected {len(available_ports)} available ports: {available_ports}")
    print(f"Device has {forms} forms (correct for this Series 3 variant)")
