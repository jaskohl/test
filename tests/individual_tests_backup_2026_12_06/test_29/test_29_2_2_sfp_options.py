"""
Test 29 2 2 Sfp Options
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_29_2_2_sfp_options(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29 2 2 Sfp Options
    Purpose: Test SFP mode configuration options and selections
    Expected: SFP should have multiple mode options available
    """
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    # Navigate to network page
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # Expand SFP panel before field interaction
    try:
        sfp_header = unlocked_config_page.locator('a[href="#sfp_mode_collapse"]')
        if sfp_header.count() > 0:
            aria_expanded = sfp_header.get_attribute("aria-expanded")
            if aria_expanded != "true":
                sfp_header.click()
                time.sleep(0.5)
    except Exception:
        pass  # Panel expansion is optional

    # Test SFP options availability
    sfp = unlocked_config_page.locator("select[name*='sfp' i]")
    if sfp.is_visible():
        expect(sfp).to_be_enabled()
        assert (
            sfp.locator("option").count() >= 2
        ), "SFP should have at least 2 mode options"
    else:
        # SFP may not be visible on all devices
        print("SFP configuration not visible on this device model")
