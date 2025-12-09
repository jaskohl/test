"""
Test 23.1.2: Numeric field boundaries (domain number 0-255)
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


def test_23_1_2_numeric_field_boundaries(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 23.1.2: Numeric field boundaries (domain number 0-255)"""
    # FIXED: Use DeviceCapabilities.get_series() instead of device_series parameter
    from pages.device_capabilities import DeviceCapabilities

    # Get device model from the request fixture
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot determine PTP capabilities")

    # Check if this is a Series 3 device using DeviceCapabilities
    device_series_num = DeviceCapabilities.get_series(device_model)
    if device_series_num != 3:
        pytest.skip("PTP is Series 3 exclusive")

    unlocked_config_page.goto(f"{base_url}/ptp", wait_until="domcontentloaded")

    # Get available PTP interfaces for this device model
    available_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)
    if not available_interfaces:
        pytest.skip(f"No PTP interfaces available on device model {device_model}")

    # Use first available interface for testing
    test_interface = available_interfaces[0]
    domain = unlocked_config_page.locator(
        f"input[name='domain_number_{test_interface}']"
    )

    if domain.is_visible():
        # Test boundaries
        test_values = [
            ("0", True),  # Minimum valid
            ("127", True),  # Middle
            ("255", True),  # Maximum valid
            ("-1", False),  # Below minimum
            ("256", False),  # Above maximum
            ("999", False),  # Way over
        ]
        for value, should_accept in test_values:
            domain.fill(value)
            time.sleep(0.2)
            if should_accept:
                assert domain.input_value() == value
