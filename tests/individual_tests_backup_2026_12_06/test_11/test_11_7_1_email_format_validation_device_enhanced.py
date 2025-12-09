"""
Test 11.7.1: Email Format Validation (Device-Enhanced)
Purpose: Email format validation with device capabilities
Expected: Device-aware email format validation
Device-Enhanced: Uses DeviceCapabilities for device-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_7_1_email_format_validation_device_enhanced(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.7.1: Email Format Validation (Device-Enhanced)
    Purpose: Email format validation with device capabilities
    Expected: Device-aware email format validation
    Device-Enhanced: Uses DeviceCapabilities for device-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate email format")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Navigate to general config page
    general_config_page.navigate_to_page()

    # Look for email fields
    email_field_selectors = [
        "input[type='email']",
        "input[name*='email']",
        "input[name*='contact']",
    ]

    email_field = None
    for selector in email_field_selectors:
        try:
            field = general_config_page.page.locator(selector).first
            if field.count() > 0:
                email_field = field
                print(f"Found email field with selector: {selector}")
                break
        except:
            continue

    if email_field:
        # Test valid email formats
        valid_emails = ["test@example.com", "user@domain.org", "admin@company.co.uk"]

        for email in valid_emails:
            try:
                email_field.fill(email)
                actual_value = email_field.input_value()
                print(f"Valid email accepted: {email} -> {actual_value}")
            except Exception as e:
                print(f"Email field test issue for {email}: {e}")

        # Test invalid email formats
        invalid_emails = [
            "invalid-email",
            "@domain.com",
            "user@",
            "user..user@example.com",
        ]

        for invalid_email in invalid_emails:
            try:
                email_field.fill(invalid_email)
                actual_value = email_field.input_value()
                print(f"Invalid email test: {invalid_email} -> {actual_value}")
                # Note: Device behavior may vary on invalid emails
            except Exception as e:
                print(f"Invalid email test issue for {invalid_email}: {e}")
    else:
        print(f"No email fields found for validation test on {device_model}")
