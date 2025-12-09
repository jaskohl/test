"""
Category 9: Access Configuration - Test 9.3.1
All Password Fields Present
Test Count: 1 of 7 in Category 9
Hardware: Device Only
Priority: HIGH - Security configuration
Series: Both Series 2 and 3
Based on test_09_access_config.py::TestPasswordValidation::test_9_3_1_password_fields_exist
NOTE: Device has 3 password fields, all type='text'
"""

import pytest
from playwright.sync_api import Page, expect
from pages.access_config_page import AccessConfigPage


def test_password_fields_exist(access_config_page: AccessConfigPage):
    """
    Test 9.3.1: All Password Fields Present
    Purpose: Verify all 3 password fields exist
    Expected: cfgpwd, uplpwd, stspwd fields present
    Series: Both 2 and 3
    NOTE: Device has 3 password fields, all type='text'
    """
    # Verify all 3 password fields exist
    password_fields = [
        ("cfgpwd", "Configuration password"),
        ("uplpwd", "Upload password"),
        ("stspwd", "Status password"),
    ]

    for field_name, description in password_fields:
        field = access_config_page.page.locator(f"input[name='{field_name}']")
        expect(field).to_be_visible()

        # Verify it's a text input
        field_type = field.get_attribute("type")
        assert field_type == "text", f"{description} should be type='text'"
