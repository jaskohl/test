"""
Test 19.5.1: Profile Changes Field States
Category 19: Dynamic UI Behavior & Element Validation - IMPROVED
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_5_1_profile_changes_field_states(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.5.1: PTP profile changes field readonly states"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate PTP profile field state changes"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    if device_series != "Series 3":
        pytest.skip("PTP is Series 3 exclusive")

    # IMPROVED: Device-aware timeout with timeout multiplier
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    timeout = int(60000 * timeout_multiplier)

    unlocked_config_page.goto(
        f"{base_url}/ptp", timeout=timeout
    )  # Extended timeout for Series 3
    print(
        f"[Device: {device_model}] Testing PTP profile changes with {timeout}ms timeout"
    )

    # Wait for PTP page content to fully load (Series 3 panels collapsed by default)
    time.sleep(2)
    # Wait for loading mask to clear if present
    loading_mask = unlocked_config_page.locator(".page-loading-mask, #loading-mask")
    if loading_mask.is_visible(timeout=5000):
        expect(loading_mask).to_be_hidden(timeout=15000)
    # Use interface-specific selector for eth1 (matches device exploration: ptp_interfaces: ["eth1", "eth2", "eth3", "eth4"])
    profile = unlocked_config_page.locator("select#eth1_profile")
    if profile.is_visible():
        profile.select_option(label="Custom")
        time.sleep(0.5)
        # Fields should become editable
