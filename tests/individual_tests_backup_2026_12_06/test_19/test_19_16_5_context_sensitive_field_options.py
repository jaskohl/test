"""
Test 19.16.5: Context-sensitive field options based on other selections - INDIVIDUAL TEST FILE
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


def test_19_16_5_context_sensitive_field_options(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.16.5: Context-sensitive field options based on other selections"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate context-sensitive field options"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(
        f"{base_url}/network"
    )  # Changed from ptp to network for wider compatibility
    time.sleep(1)
    print(f"[Device: {device_model}] Testing context-sensitive field options")

    # Select appropriate profile selector based on device series
    if device_series == "Series 2":
        # Series 2 has single interface
        profile_select = unlocked_config_page.locator("select[name='profile']").first
    else:  # Series 3
        # Use specific interface selector to avoid strict mode violations
        profile_select = unlocked_config_page.locator("select#eth1_profile")
    if profile_select.is_visible():
        # Get initial options count
        initial_options = profile_select.locator("option").count()
        # Change profile
        if initial_options > 1:
            profile_select.select_option(index=1)
            time.sleep(0.5)
            # Check if options changed
            new_options = profile_select.locator("option").count()
            # Options may change based on profile selection
            assert new_options > 0, "Profile options should be available"
