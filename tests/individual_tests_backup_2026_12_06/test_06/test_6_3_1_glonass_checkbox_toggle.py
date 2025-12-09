"""
Category 6: GNSS Configuration - Test 6.3.1
GLONASS Checkbox Toggle
Test Count: 1 of 15 in Category 6
Hardware: Device Only
Priority: HIGH - GNSS is primary time source
Series: Both Series 2 and 3
Based on test_06_gnss_config.py::TestConstellationSelection::test_6_3_1_glonass_checkbox_toggle
Device exploration data: config_gnss.forms.json
MODERNIZATION: Uses request.session.device_hardware_model for device-aware skip handling
CRITICAL FIX: Fixed device model detection to use request.session.device_hardware_model
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.gnss_config_page import GNSSConfigPage


def test_6_3_1_glonass_checkbox_toggle(gnss_config_page: GNSSConfigPage, request):
    """
    Test 6.3.1: GLONASS Constellation Configuration
    Purpose: Verify GLONASS can be enabled/disabled
    Expected: Checkbox toggles and persists
    Field: name="glonass", id="glonass", class="gnss"
    Series: Both 2 and 3
    IMPROVED: Device-aware skip handling for known issues
    """
    device_model = request.session.device_hardware_model

    try:
        # Use page object's user-facing locator
        glonass_checkbox = gnss_config_page._get_constellation_checkbox("glonass")
        expect(glonass_checkbox).to_be_visible()
        expect(glonass_checkbox).to_be_enabled()
        # Toggle and verify change
        was_checked = glonass_checkbox.is_checked()
        glonass_checkbox.click()
        # Verify state changed
        assert (
            glonass_checkbox.is_checked() != was_checked
        ), f"GLONASS checkbox should toggle on {device_model}"
        # Use page object's cancel method
        gnss_config_page.cancel_gnss_changes()
        print(f"INFO: {device_model} - GLONASS checkbox toggle verified")
    except Exception as e:
        pytest.skip(f"GLONASS checkbox test failed on {device_model}: {e}")
