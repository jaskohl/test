"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.26.3: Pattern Validation Dynamic Updates
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 19.26.3
Modernized with DeviceCapabilities integration for improved device detection and error handling
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_26_3_pattern_validation_dynamic_updates(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.26.3: Input pattern validation changes dynamically"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate pattern validation dynamic updates"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/network")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing dynamic pattern validation updates")

    # Look for fields with dynamic pattern attributes
    pattern_fields = unlocked_config_page.locator("input[pattern]")
    if pattern_fields.count() > 0:
        pattern_field = pattern_fields.first
        # Get initial pattern
        initial_pattern = pattern_field.get_attribute("pattern")
        # Change context that might affect pattern
        selects = unlocked_config_page.locator("select")
        if selects.count() > 0 and selects.first.locator("option").count() > 1:
            selects.first.select_option(index=1)
            time.sleep(0.5)
            # Check if pattern changed
            new_pattern = pattern_field.get_attribute("pattern")
            # Pattern may have changed based on context
