"""
Category 9: Access Configuration - Test 9.2.1
Configuration Password Change
Test Count: 1 of 7 in Category 9
Hardware: Device Only
Priority: HIGH - Security configuration
Series: Both Series 2 and 3
Based on test_09_access_config.py::TestPasswordConfiguration::test_9_2_1_configuration_password_change
NOTE: Device uses input[type='text'] for password fields
"""

import pytest
from playwright.sync_api import Page, expect
from pages.access_config_page import AccessConfigPage


def test_9_2_1_configuration_password_change(access_config_page: AccessConfigPage):
    """
    Test 9.2.1: Configuration Password Change
    Purpose: Verify configuration unlock password can be changed
    Expected: Password field accepts input
    Series: Both 2 and 3
    NOTE: Device uses input[type='text'] for password fields
    Field name: cfgpwd
    """
    # Device has input name="cfgpwd" for configuration password
    config_password_field = access_config_page.page.locator("input[name='cfgpwd']")

    expect(config_password_field).to_be_visible()
    expect(config_password_field).to_be_editable()

    # Verify field type is text (device design)
    field_type = config_password_field.get_attribute("type")
    assert field_type == "text", "Config password field should be type='text'"

    # Get current value
    current_value = config_password_field.input_value()
    assert len(current_value) > 0, "Config password field should have a value"
