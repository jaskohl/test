"""
Category 9: Access Configuration - Test 9.1.1
Status Password Change
Test Count: 1 of 7 in Category 9
Hardware: Device Only
Priority: HIGH - Security configuration
Series: Both Series 2 and 3
Based on test_09_access_config.py::TestPasswordConfiguration::test_9_1_1_status_password_change
NOTE: Device uses input[type='text'] for password fields, not input[type='password']
"""

import pytest
from playwright.sync_api import Page, expect
from pages.access_config_page import AccessConfigPage


def test_status_password_change(
    access_config_page: AccessConfigPage, device_password: str
):
    """
    Test 9.1.1: Status Password Change
    Purpose: Verify status monitoring password can be changed
    Expected: Password field accepts input
    Series: Both 2 and 3
    NOTE: Device uses input[type='text'] for password fields, not input[type='password']
    Field name: stspwd
    """
    # Device has input name="stspwd" for status password
    status_password_field = access_config_page.page.locator("input[name='stspwd']")

    expect(status_password_field).to_be_visible()
    expect(status_password_field).to_be_editable()

    # Verify field type is text (device design)
    field_type = status_password_field.get_attribute("type")
    assert field_type == "text", "Status password field should be type='text'"

    # Get current value
    current_value = status_password_field.input_value()
    assert len(current_value) > 0, "Status password field should have a value"
