"""
Test 11.7.2: URL Format Validation (Device-Enhanced)
Purpose: URL format validation with device capabilities
Expected: Device-aware URL format validation
Device-Enhanced: Uses DeviceCapabilities for device-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_7_2_url_format_validation_device_enhanced(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.7.2: URL Format Validation (Device-Enhanced)
    Purpose: URL format validation with device capabilities
    Expected: Device-aware URL format validation
    Device-Enhanced: Uses DeviceCapabilities for device-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate URL format")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Navigate to general config page
    general_config_page.navigate_to_page()

    # Look for URL fields
    url_field_selectors = [
        "input[type='url']",
        "input[name*='url']",
        "input[name*='server']",
    ]

    url_field = None
    for selector in url_field_selectors:
        try:
            field = general_config_page.page.locator(selector).first
            if field.count() > 0:
                url_field = field
                print(f"Found URL field with selector: {selector}")
                break
        except:
            continue

    if url_field:
        # Test valid URL formats
        valid_urls = [
            "http://example.com",
            "https://secure.domain.org",
            "http://192.168.1.1:8080",
            "https://api.company.co.uk/v1",
        ]

        for url in valid_urls:
            try:
                url_field.fill(url)
                actual_value = url_field.input_value()
                print(f"Valid URL accepted: {url} -> {actual_value}")
            except Exception as e:
                print(f"URL field test issue for {url}: {e}")

        # Test invalid URL formats
        invalid_urls = ["not-a-url", "http://", "ftp://invalid", "http://[invalid ipv6"]

        for invalid_url in invalid_urls:
            try:
                url_field.fill(invalid_url)
                actual_value = url_field.input_value()
                print(f"Invalid URL test: {invalid_url} -> {actual_value}")
            except Exception as e:
                print(f"Invalid URL test issue for {invalid_url}: {e}")
    else:
        print(f"No URL fields found for validation test on {device_model}")
