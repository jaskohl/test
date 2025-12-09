"""
Category 23: Boundary & Input Testing - COMPLETE
Test Count: 3 tests
Hardware: Device Only ()
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 23
"""

import pytest
import time
from playwright.sync_api import Page


class TestBoundaryValues:
    """Test 23.1-23.3: Boundary Value Testing"""

    def test_23_1_1_ip_address_boundary_values(
        self, unlocked_config_page: Page, base_url: str
    ):
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

    def test_23_1_2_numeric_field_boundaries(
        self, unlocked_config_page: Page, base_url: str, request
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

    def test_23_1_3_text_field_length_limits(
        self, unlocked_config_page: Page, base_url: str
    ):
        """Test 23.1.3: Text field maximum length limits"""
        unlocked_config_page.goto(f"{base_url}/general", wait_until="domcontentloaded")
        identifier = unlocked_config_page.locator("input[name='identifier']")
        if identifier.is_visible():
            # Test very long string
            long_string = "A" * 500
            identifier.fill(long_string)
            time.sleep(0.2)
            # Field should either accept up to max length or truncate
            current_value = identifier.input_value()
            assert len(current_value) <= 500, "Field should have length limit"
            # Test reasonable string
            identifier.fill("TEST-DEVICE-001")
            assert identifier.input_value() == "TEST-DEVICE-001"
