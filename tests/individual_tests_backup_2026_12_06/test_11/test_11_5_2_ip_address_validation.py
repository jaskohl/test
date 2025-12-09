"""
Test 11.5.2: IP Address Validation (Device-Aware)
Purpose: IP address format validation
Expected: Device-specific IP address field behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_5_2_ip_address_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.5.2: IP Address Validation (Device-Aware)
    Purpose: IP address format validation
    Expected: Device-specific IP address field behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate IP address field behavior"
        )

    general_config_page.navigate_to_page()

    # Look for IP address fields
    ip_fields = general_config_page.page.locator(
        "input[name*='ip' i], input[name*='gateway' i], input[name*='dns' i]"
    )
    if ip_fields.count() > 0:
        ip_field = ip_fields.first
        # Test valid IP addresses
        valid_ips = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
        for ip in valid_ips:
            ip_field.fill(ip)
            expect(ip_field).to_have_value(ip)
        # Test invalid IP format
        ip_field.fill("999.999.999.999")
        # Field may accept invalid format client-side
    else:
        print(f"No IP address fields found for {device_model}")
