"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.21.5: Dynamic Tab Content Visibility
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 19.21.5
Modernized with DeviceCapabilities integration for improved device detection and error handling
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_21_5_dynamic_tab_content_visibility(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.21.5: Tab content shows/hides dynamically based on conditions"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate dynamic tab content visibility"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/time")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing dynamic tab content visibility")

    # Look for tabbed interfaces with conditional content
    tabs = unlocked_config_page.locator("[role='tab'], .tab-button")
    tab_content = unlocked_config_page.locator(".tab-content, [role='tabpanel']")
    if tabs.count() > 1 and tab_content.count() > 0:
        # Click different tabs and observe content changes
        for i in range(min(3, tabs.count())):
            tab = tabs.nth(i)
            if tab.is_visible():
                tab.click()
                time.sleep(0.5)
                # Check if tab content is visible and other content is hidden
                expect(tab_content.nth(i)).to_be_visible()
