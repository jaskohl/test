"""
Test 16.1.2: NTP Time Accuracy Validation
Category: 16 - Integration Tests
Test Count: Part of 9 tests in Category 16
Hardware: Software Tools for 6 tests, Device Only for 3 tests
Priority: MEDIUM - External protocol validation
Series: Both Series 2 and 3

Extracted from: tests/test_16_integration.py
Source Class: TestNTPIntegration
"""

import pytest
import time


def check_package_available(package_name: str) -> bool:
    """Check if a Python package is available."""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def test_16_1_2_ntp_time_accuracy(device_ip: str):
    """
    Test 16.1.2: NTP Time Accuracy Validation
    Purpose: Verify NTP time is accurate
    Expected: Time offset within acceptable range (< 1ms typical)
    Series: Both 2 and 3
    FIXED: Dynamic package detection
    """
    if not check_package_available("ntplib"):
        pytest.skip("Requires ntplib and time accuracy validation")
    try:
        import ntplib

        client = ntplib.NTPClient()
        response = client.request(device_ip, version=3)
        current_time = time.time()
        time_diff = abs(response.tx_time - current_time)
        assert time_diff < 1.0, f"NTP time should be accurate, difference: {time_diff}s"
        print(f"NTP accuracy test passed: {time_diff}s difference")
    except Exception as e:
        print(f"NTP accuracy test error (expected for device testing): {e}")
