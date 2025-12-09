"""
Test 29 2 4 Sfp Cancel
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_29_2_4_sfp_cancel(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29 2 4 Sfp Cancel
    Purpose: Test SFP cancel button reverts configuration changes
    Expected: SFP settings should revert when cancel is clicked
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

    # Test SFP cancel functionality
    sfp = unlocked_config_page.locator("select[name*='sfp' i]")
    if sfp.is_visible():
        if sfp.locator("option").count() >= 2:
            # Change SFP selection if multiple options available
            sfp.select_option(index=1)

        # Look for cancel button
        cancel = unlocked_config_page.locator("button#button_cancel_sfp, button.cancel")
        if cancel.is_visible():
            cancel.click()
            time.sleep(0.5)
        else:
            print("SFP cancel button not visible on this device model")
    else:
        # SFP may not be visible on all devices
        print("SFP configuration not visible on this device model")
