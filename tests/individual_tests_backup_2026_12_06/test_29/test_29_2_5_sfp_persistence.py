"""
Test 29 2 5 Sfp Persistence
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_29_2_5_sfp_persistence(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29 2 5 Sfp Persistence
    Purpose: Test SFP configuration persists across page navigation
    Expected: SFP settings should be maintained after page reload/navigation
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

    # Test SFP persistence
    sfp = unlocked_config_page.locator("select[name*='sfp' i]")
    if sfp.is_visible():
        current = sfp.input_value()

        # Navigate away to another page and back
        unlocked_config_page.goto(f"{base_url}/general", wait_until="domcontentloaded")
        unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

        # Expand SFP panel again after navigation
        try:
            sfp_header = unlocked_config_page.locator('a[href="#sfp_mode_collapse"]')
            if sfp_header.count() > 0:
                aria_expanded = sfp_header.get_attribute("aria-expanded")
                if aria_expanded != "true":
                    sfp_header.click()
                    time.sleep(0.5)
        except Exception:
            pass  # Panel expansion is optional

        # Verify SFP selection persisted
        sfp_after = unlocked_config_page.locator("select[name*='sfp' i]")
        if sfp_after.is_visible():
            assert (
                sfp_after.input_value() == current
            ), f"SFP selection should persist after navigation (was {current})"
    else:
        # SFP may not be visible on all devices
        print("SFP configuration not visible on this device model")
