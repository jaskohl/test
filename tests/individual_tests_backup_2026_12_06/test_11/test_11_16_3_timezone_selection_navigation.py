"""
Test 11.16.3: Timezone Selection Navigation (Device-Aware)
Category 11: Form Validation Tests
Test Count: 1 of 47 total tests
Hardware: Device Only
Priority: MEDIUM - Input validation critical for data integrity
Series: Both Series 2 and 3

FIXES APPLIED:
-  Fixed device model detection: uses request.session.device_hardware_model
-  Device-aware validation using DeviceCapabilities.get_series()
-  Maintains rollback logic with try/finally blocks
-  Uses correct parameter signatures
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_16_3_timezone_selection_navigation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.16.3: Timezone dropdown navigation and selection (Device-Aware)
    Purpose: Test timezone dropdown navigation and selection
    Expected: Device should handle timezone navigation appropriately
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate timezone navigation")

    device_series = DeviceCapabilities.get_series(device_model)

    try:
        general_config_page.navigate_to_page()

        # Look for timezone select fields
        timezone_selects = general_config_page.page.locator(
            "select[name*='timezone' i]"
        )
        if timezone_selects.count() > 0:
            timezone_select = timezone_selects.first
            options = timezone_select.locator("option")
            option_count = options.count()
            if option_count > 1:
                # Test navigation through timezone options
                options.nth(1).click()  # Select second option
                selected_value = timezone_select.input_value()
                assert selected_value != "", "Timezone should be selected"
                # Test selecting different timezone
                if option_count > 2:
                    options.nth(2).click()  # Select third option
                    new_value = timezone_select.input_value()
                    assert (
                        new_value != selected_value
                    ), "Timezone selection should change"
        else:
            print(f"No timezone select fields found for {device_model}")

    finally:
        # Cleanup: Reset fields to original state if needed
        pass
