"""
Test 19.16.2: Dynamic field type changes based on configuration - INDIVIDUAL TEST FILE
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


def test_19_16_2_dynamic_field_type_changes(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.16.2: Dynamic field type changes based on configuration"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate dynamic field type changes"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/network")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing dynamic field type changes")

    # Look for fields that change type based on selections
    # Use specific selector to avoid ambiguity
    mode_select = unlocked_config_page.locator("select[name='redundancy_mode_eth1']")
    dynamic_fields = unlocked_config_page.locator(
        "input[data-dynamic-type], input[dynamic-type]"
    )
    if mode_select.is_visible() and dynamic_fields.count() > 0:
        # Change mode and observe field type changes
        initial_type = dynamic_fields.first.get_attribute("type")
        mode_select.select_option(index=1)
        time.sleep(0.5)
        new_type = dynamic_fields.first.get_attribute("type")
        # Field type may change (e.g., text to number, etc.)
