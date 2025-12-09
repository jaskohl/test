"""
Test 23.1.1: IP address boundary values
Category 23 - Boundary & Input Testing - COMPLETE
Test Count: 3 tests
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 23

Extracted from: tests/test_23_boundary.py
Source Class: TestBoundaryValues
"""

import pytest
import time
from playwright.sync_api import Page


def test_23_1_1_ip_address_boundary_values(unlocked_config_page: Page, base_url: str):
    """Test 23.1.1: IP address field boundary values"""
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")
    time.sleep(1)
    ip_field = unlocked_config_page.locator("input[name='ipaddr']")
    if ip_field.is_visible():
        # Test boundary values
        test_ips = [
            "0.0.0.0",  # Minimum
            "1.1.1.1",  # Valid
            "255.255.255.255",  # Maximum
            "192.168.1.1",  # Typical
        ]
        for ip in test_ips:
            ip_field.fill(ip)
            time.sleep(0.2)
            assert ip_field.input_value() == ip
        # Test invalid values
        invalid_ips = [
            "256.1.1.1",  # > 255
            "-1.1.1.1",  # Negative
            "999.999.999.999",  # Way over
        ]
        for ip in invalid_ips:
            ip_field.fill(ip)
            time.sleep(0.2)
            # Should show validation error or reject input
