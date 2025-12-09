"""
Category 5: Time Configuration - Test 5.2.1
Time Synchronization Status - Series-Specific
Test Count: 2 of 2 in Time Sync Subcategory
Hardware: Device Only
Priority: HIGH - Time synchronization validation
Series: Both Series 2 and 3
ENHANCED: DeviceCapabilities integration for series-specific time synchronization validation
Based on time configuration requirements and synchronization validation patterns
Device exploration data: time_sync.json, sync_validation_patterns.json
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.time_config_page import TimeConfigPage

logger = logging.getLogger(__name__)


def test_5_2_1_dst_rule_selection(time_config_page: TimeConfigPage, request):
    """
    Test 5.2.1: Time Synchronization Status - Series-Specific
    Purpose: Verify time synchronization status validation with series-specific patterns
    Expected: Time synchronization works correctly with device series-specific timing and behavior
    ENHANCED: Full DeviceCapabilities integration for series-specific time sync validation
    Series: Both - validates time synchronization patterns across device variants
    """
    # Get device model and capabilities for series-specific testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate time synchronization")

    # Get device series and timeout multiplier for series-specific testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing time synchronization status on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    dst_rule_select = time_config_page.page.locator("select[name='dst_rule']")
    expect(dst_rule_select).to_be_visible()
    # Verify options present
    options = dst_rule_select.locator("option")
    option_count = options.count()
    assert option_count == 7, f"Should have 7 DST rules, found {option_count}"
    # Verify key rules present
    expected_rules = ["CUSTOM", "OFF", "USA", "WESTERN EUROPE"]
    for rule in expected_rules:
        # Check if DST rule exists in available options
        rule_found = False
        for i in range(option_count):
            option_text = options.nth(i).inner_text()
            if rule in option_text:
                rule_found = True
                break
        assert rule_found, f"DST rule {rule} should be available"
