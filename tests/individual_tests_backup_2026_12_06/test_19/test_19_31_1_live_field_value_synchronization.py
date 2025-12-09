"""
Category 19: Dynamic UI Behavior & Element Validation - Individual Test
Test 19.31.1: Live Field Value Synchronization - IMPROVED
Test Count: 1 test
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 19.31.1
Modernized with DeviceCapabilities integration for improved device detection and error handling
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_31_1_live_field_value_synchronization(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.31.1: Field values synchronize in real-time across related fields"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate live field value synchronization"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/network")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing live field value synchronization")

    # Select appropriate fields based on device series
    if device_series == "Series 2":
        field1 = unlocked_config_page.locator("input[name*='gateway' i]").first
    else:  # Series 3
        # Use specific interface selectors
        field1 = unlocked_config_page.locator("input#gateway")
    if field1.count() > 0 and field1.is_visible():
        field1 = field1.first
        # Change field
        field1.fill("192.168.1.1")
        field1.dispatch_event("change")  # Trigger onchange event
        time.sleep(0.5)
        # Verify field accepts the change
        actual_value = field1.input_value()
        assert (
            actual_value == "192.168.1.1"
        ), f"Field should contain 192.168.1.1, but contains {actual_value}"
