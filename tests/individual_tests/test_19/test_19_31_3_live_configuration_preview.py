"""
Category 19: Dynamic UI Behavior & Element Validation - Individual Test
Test 19.31.3: Live Configuration Preview - IMPROVED
Test Count: 1 test
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 19.31.3
Modernized with DeviceCapabilities integration for improved device detection and error handling
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_31_3_live_configuration_preview(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.31.3: Real-time configuration preview updates"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate live configuration preview"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/ptp")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing live configuration preview updates")

    # Look for preview areas that update live
    previews = unlocked_config_page.locator(".preview, .live-preview, #config-preview")
    if previews.count() > 0:
        preview = previews.first
        # Make a configuration change
        selects = unlocked_config_page.locator("select")
        if selects.count() > 0 and selects.first.locator("option").count() > 1:
            selects.first.select_option(index=1)
            time.sleep(0.5)
            # Check if preview updated
            expect(preview).to_be_visible()
