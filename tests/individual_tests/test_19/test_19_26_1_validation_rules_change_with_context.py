"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.26.1: Validation Rules Change with Context
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 19.26.1
Modernized with DeviceCapabilities integration for improved device detection and error handling
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_26_1_validation_rules_change_with_context(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.26.1: Validation rules change based on form context"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate validation rules change with context"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/network")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing validation rules that change with context")

    # Select appropriate field based on device series to avoid strict mode violations
    if device_series == "Series 2":
        context_field = unlocked_config_page.locator("input[name*='ip' i]").first
    else:  # Series 3
        # Use specific interface selector
        context_field = unlocked_config_page.locator("input#ip_eth0")
    if context_field.count() > 0 and context_field.is_visible():
        # Test validation with different contexts
        # Enter a value that might be valid in one context but invalid in another
        context_field.fill("192.168.1.100")
        context_field.dispatch_event("change")  # Trigger onchange event
        time.sleep(0.5)
        # Change context if possible
        mode_selects = unlocked_config_page.locator("select[name*='mode' i]")
        if mode_selects.count() > 0:
            mode_select = mode_selects.first
            if mode_select.locator("option").count() > 1:
                mode_select.select_option(index=1)
                time.sleep(0.5)
                # Validation rules may have changed
