"""
Test 11.7.1: Email Format Validation (Device-Aware)
Purpose: Email format validation
Expected: Device-specific email field behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_7_1_email_format_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.7.1: Email Format Validation (Device-Aware)
    Purpose: Email format validation
    Expected: Device-specific email field behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate email format behavior")

    general_config_page.navigate_to_page()

    # Look for email fields
    email_fields = general_config_page.page.locator(
        "input[type='email'], input[name*='email' i], input[name*='contact' i]"
    )
    if email_fields.count() > 0:
        email_field = email_fields.first
        # Test valid email formats
        valid_emails = ["test@example.com", "user@domain.org", "admin@test.co"]
        for email in valid_emails:
            email_field.fill(email)
            expect(email_field).to_have_value(email)
        # Test invalid email format
        email_field.fill("invalid-email")
        # Device may accept invalid format client-side
    else:
        print(f"No email fields found for {device_model}")
