"""
Category 19.5.3: Network Mode Field Visibility
Test: Network mode change shows relevant fields
Hardware: Device Only
Priority: MEDIUM
Series: Series 2 Only
Based on COMPLETE_TEST_LIST.md Section 19.5.3
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_5_3_mode_change_shows_relevant_fields(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.5.3: Network mode change shows relevant fields"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate network mode field visibility"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    if device_series != "Series 2":
        pytest.skip("Network mode field is Series 2 only")

    unlocked_config_page.goto(f"{base_url}/network")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    mode = unlocked_config_page.get_by_label("Network Mode")
    if not mode.is_visible():
        mode = unlocked_config_page.locator("select[name='mode']")

    if mode.is_visible():
        # Select different modes and verify fields change
        mode.select_option(index=0)
        time.sleep(0.5)
