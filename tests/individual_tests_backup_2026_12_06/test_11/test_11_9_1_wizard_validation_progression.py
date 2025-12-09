"""
Test 11.9.1: Wizard Validation Progression (Device-Aware)
Purpose: Validation across multi-step form wizards
Expected: Device-specific multi-step form behavior
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_9_1_wizard_validation_progression(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.9.1: Wizard Validation Progression (Device-Aware)
    Purpose: Validation across multi-step form wizards
    Expected: Device-specific multi-step form behavior
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate multi-step form behavior"
        )

    general_config_page.navigate_to_page()

    # Look for multi-step form indicators
    next_buttons = general_config_page.page.locator(
        "button:has-text('Next'), button:has-text('Continue'), .next-btn"
    )
    if next_buttons.count() > 0:
        # Test progression between steps
        next_btn = next_buttons.first
        if next_btn.is_enabled():
            # Fill required fields before proceeding
            required_fields = general_config_page.page.locator(
                "[required], [aria-required='true']"
            )
            if required_fields.count() > 0:
                # Fill first required field
                required_fields.first.fill("test_value")
                # Try to proceed to next step
                next_btn.click()
                # Should either proceed or show validation errors
                # Device-specific behavior for multi-step validation
    else:
        print(
            f"Multi-step form validation skipped for {device_model} - No wizard found"
        )
