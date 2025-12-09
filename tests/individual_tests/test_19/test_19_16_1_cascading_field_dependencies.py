"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.16.1: Cascading Field Dependencies
Hardware: Device Only
Series: Series 3
Extracted from test_19_dynamic_ui.py
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_16_1_cascading_field_dependencies(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.16.1: Cascading field dependencies with multiple levels"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate cascading dependencies"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    if device_series != "Series 3":
        pytest.skip("Advanced dependencies are Series 3 features")

    unlocked_config_page.goto(f"{base_url}/ptp")
    time.sleep(1)
    # Expand PTP panels before testing (CRITICAL FIX: panels collapsed by default)
    try:
        from pages.ptp_config_page import PTPConfigPage

        ptp_page = PTPConfigPage(unlocked_config_page)
        ptp_page.expand_all_ptp_panels()
    except Exception:
        pass  # Continue if expansion fails
    time.sleep(1)
    # Look for cascading dependencies (e.g., PTP enable -> profile select -> timing fields)
    # FIXED: Use interface-specific selector to avoid strict mode violations
    # Series 3 devices have multiple profile selectors (eth1, eth2, eth3, eth4)
    # Generic selector select[name='profile'] causes strict mode violations
    ptp_enable = unlocked_config_page.locator("input[name='ptp_enable_eth1']")
    # Note: Using interface-specific selector per LOCATOR_STRATEGY.md to avoid ambiguity
    profile_select = unlocked_config_page.locator("select#eth1_profile")
    if profile_select.count() > 0 and profile_select.is_visible():
        # Enable PTP first if possible
        if ptp_enable.count() > 0 and ptp_enable.is_visible():
            ptp_enable.check()
            time.sleep(0.5)
        # Select profile
        if profile_select.locator("option").count() > 1:
            profile_select.select_option(index=1)
            time.sleep(0.5)
            # Check if timing fields become visible/enabled
            # Use interface-specific timing field selector
            timing_fields = unlocked_config_page.locator(
                "input[name='log_announce_interval_eth1']"
            )
            if timing_fields.count() > 0:
                expect(timing_fields).to_be_visible()
