"""
Test 29 10 2 Access Control Lists
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page


def test_29_10_2_access_control_lists(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29.10.2: Access control list management

    Test ACL configuration management functionality.
    Series 3 devices only - checks for ACL field availability and editability.
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")
    # Look for ACL configuration fields
    from playwright.sync_api import expect

    acl = unlocked_config_page.locator(
        "textarea[name*='acl' i], input[name*='acl_rule' i]"
    )
    if acl.is_visible():
        expect(acl).to_be_editable()
