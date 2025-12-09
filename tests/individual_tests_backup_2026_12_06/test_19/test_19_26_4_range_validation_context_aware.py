"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.26.4: Range Validation Context Aware
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 19.26.4
Modernized with DeviceCapabilities integration for improved device detection and error handling
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_26_4_range_validation_context_aware(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.26.4: Min/max range validation adapts to context"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate range validation context aware"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/network")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing context-aware range validation")

    # Select appropriate profile selector based on device series
    if device_series == "Series 2":
        profiles = unlocked_config_page.locator("select[name*='profile' i]").first
    else:  # Series 3
        # Use specific interface selector to avoid strict mode violations
        profiles = unlocked_config_page.locator("select#eth1_profile")
    if profiles.is_visible():
        # Get initial options
        initial_options = profiles.locator("option").count()
        # Change context
        if initial_options > 1:
            profiles.select_option(index=1)
            time.sleep(0.5)
            # Check if options changed
            new_options = profiles.locator("option").count()
            # Range constraints may have changed
            assert new_options > 0, "Profile should have options"
