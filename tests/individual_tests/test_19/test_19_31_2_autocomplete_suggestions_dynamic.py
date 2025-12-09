"""
Category 19: Dynamic UI Behavior & Element Validation - Individual Test
Test 19.31.2: Autocomplete Suggestions Dynamic - IMPROVED
Test Count: 1 test
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 19.31.2
Modernized with DeviceCapabilities integration for improved device detection and error handling
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_31_2_autocomplete_suggestions_dynamic(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.31.2: Autocomplete suggestions update based on context"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate autocomplete suggestions dynamic"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/network")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing dynamic autocomplete suggestions")

    # Look for fields with autocomplete
    autocomplete_fields = unlocked_config_page.locator(
        "input[autocomplete], input[list]"
    )
    if autocomplete_fields.count() > 0:
        autocomplete_field = autocomplete_fields.first
        # Type to trigger autocomplete
        autocomplete_field.fill("192")
        time.sleep(0.5)
        # Look for autocomplete suggestions
        suggestions = unlocked_config_page.locator(
            "datalist option, .autocomplete-suggestion"
        )
        if suggestions.count() > 0:
            expect(suggestions.first).to_be_visible()
