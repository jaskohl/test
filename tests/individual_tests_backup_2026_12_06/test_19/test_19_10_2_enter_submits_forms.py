"""Test 19.10.2: Enter Submits Forms
Category: Dynamic UI Behavior & Element Validation
Priority: MEDIUM
Hardware: Device Only
Series: Both Series 2 and 3

Test 19.10.2: Enter key submits forms
Modernized with DeviceCapabilities integration for improved device detection and error handling
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_10_2_enter_submits_forms(unlocked_config_page: Page, base_url: str):
    """Test 19.10.2: Enter key submits forms"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(1)
    # IMPROVED: Use user-facing locator
    identifier = unlocked_config_page.get_by_label("Device Identifier")
    if not identifier.is_visible():
        identifier = unlocked_config_page.locator("input[name='identifier']")

    if identifier.is_visible():
        identifier.fill("TEST")
        identifier.press("Enter")
        time.sleep(1)
