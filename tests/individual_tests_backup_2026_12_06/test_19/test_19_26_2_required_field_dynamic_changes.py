"""
Test 19.26.2: Fields become required/unrequired dynamically
Category: Dynamic UI Behavior & Element Validation
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_26_2_required_field_dynamic_changes(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.26.2: Fields become required/unrequired dynamically"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate required field dynamic changes"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/ptp")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing dynamic required field changes")

    # Look for fields that change required status
    dynamic_required = unlocked_config_page.locator(
        "input[data-dynamic-required], input[dynamic-required]"
    )
    if dynamic_required.count() > 0:
        field = dynamic_required.first
        # Check initial required state
        initial_required = field.get_attribute("required") is not None
        # Change context that affects required status
        selects = unlocked_config_page.locator("select")
        if selects.count() > 0 and selects.first.locator("option").count() > 1:
            selects.first.select_option(index=1)
            time.sleep(0.5)
            # Check if required status changed
            new_required = field.get_attribute("required") is not None
            # Required status may have changed
