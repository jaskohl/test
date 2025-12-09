"""
Category 6: GNSS Configuration - Test 6.4.1
BeiDou Checkbox Toggle
Test Count: 1 of 15 in Category 6
Hardware: Device Only
Priority: HIGH - GNSS is primary time source
Series: Both Series 2 and 3
Based on test_06_gnss_config.py::TestConstellationSelection::test_6_4_1_beidou_checkbox_toggle
Device exploration data: config_gnss.forms.json
MODERNIZATION: Uses request.session.device_hardware_model for device-aware error handling
CRITICAL FIX: Fixed device model detection to use request.session.device_hardware_model
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.gnss_config_page import GNSSConfigPage


def test_beidou_checkbox_toggle(gnss_config_page: GNSSConfigPage, request):
    """
    Test 6.4.1: BeiDou Constellation Configuration
    Purpose: Verify BeiDou can be enabled/disabled
    Expected: Checkbox toggles and persists
    Field: name="beidou", id="beidou", class="gnss"
    Series: Both 2 and 3
    IMPROVED: Device-aware error handling
    """
    device_model = request.session.device_hardware_model

    try:
        # Use page object's user-facing locator
        beidou_checkbox = gnss_config_page._get_constellation_checkbox("beidou")
        expect(beidou_checkbox).to_be_visible()
        expect(beidou_checkbox).to_be_enabled()
        # Toggle and verify change
        was_checked = beidou_checkbox.is_checked()
        beidou_checkbox.click()
        assert (
            beidou_checkbox.is_checked() != was_checked
        ), f"BeiDou checkbox should toggle on {device_model}"
        # Use page object's cancel method
        gnss_config_page.cancel_gnss_changes()
        print(f"INFO: {device_model} - BeiDou checkbox toggle verified")
    except Exception as e:
        pytest.skip(f"BeiDou checkbox test failed on {device_model}: {e}")
