"""
Test 19.16.4: Progressive disclosure of form sections - INDIVIDUAL TEST FILE
Category 19: Dynamic UI Behavior & Element Validation
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 19
Modernized with DeviceCapabilities integration for improved device detection and error handling
Extracted from tests/test_19_dynamic_ui.py as part of individual test file organization
Individual test files improve test organization, readability, and execution granularity
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_16_4_progressive_form_disclosure(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.16.4: Progressive disclosure of form sections"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate progressive form disclosure"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/ptp")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing progressive form disclosure")

    # Look for collapsible sections that expand progressively
    expand_buttons = unlocked_config_page.locator(
        "a[href*='collapse'], button[data-toggle='collapse']"
    )
    if expand_buttons.count() > 0:
        # Click to expand sections progressively
        for i in range(min(3, expand_buttons.count())):
            button = expand_buttons.nth(i)
            if button.is_visible():
                button.click()
                time.sleep(0.5)
                # Check if new fields become visible
                new_fields = unlocked_config_page.locator("input, select").all()
                # Progressive disclosure should reveal more options
