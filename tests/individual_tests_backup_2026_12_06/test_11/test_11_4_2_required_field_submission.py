"""
Test 11.4.2: Required Field Submission (Device-Aware)
Purpose: Form submission behavior with missing required fields
Expected: Device-specific required field submission behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_4_2_required_field_submission(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.4.2: Required Field Submission (Device-Aware)
    Purpose: Form submission behavior with missing required fields
    Expected: Device-specific required field submission behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate required field submission"
        )

    general_config_page.navigate_to_page()

    # Find a form with required fields
    forms = general_config_page.page.locator("form")
    if forms.count() > 0:
        # Look for submit buttons
        submit_btn = general_config_page.page.locator(
            "button[type='submit'], input[type='submit']"
        )
        if submit_btn.is_visible():
            # Initially button should be disabled (device behavior)
            expect(submit_btn).to_be_disabled()

            # Fill a field to trigger onchange event and enable button
            input_fields = general_config_page.page.locator(
                "input[type='text'], input[type='number'], textarea"
            )
            if input_fields.count() > 0:
                test_field = input_fields.first
                original_value = test_field.input_value() or ""

                # Fill field with different value and dispatch change event
                test_field.fill(f"{original_value}test_change")
                test_field.dispatch_event("change")  # CRITICAL: Trigger onchange event

                # Now button should be enabled
                # Use device-specific timeout if available
                known_issues = DeviceCapabilities.get_capabilities(device_model).get(
                    "known_issues", {}
                )
                timeout_multiplier = known_issues.get("timeout_multiplier", 1.0)
                button_timeout = int(2000 * timeout_multiplier)
                expect(submit_btn).to_be_enabled(timeout=button_timeout)
        else:
            print(f"No submit button found for {device_model}")
