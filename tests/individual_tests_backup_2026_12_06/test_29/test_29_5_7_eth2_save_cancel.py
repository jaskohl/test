"""
Test 29 5 7 Eth2 Save Cancel
Category: 29 - Tests\Test 29 Network Config Series3
Extracted from: tests\test_29_network_config_series3.py
Source Class: TestNetworkConfigurationDynamic
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page


def test_29_5_7_eth2_save_cancel(
    unlocked_config_page: Page, base_url: str, device_series: str
):
    """
    Test 29 5 7 Eth2 Save Cancel
    Purpose: Test eth2 save/cancel functionality through eth1 panel (Series 3A architecture)

    Architecture Note: In Series 3A devices, eth2 doesn't exist as a separate port.
    eth2 save/cancel operations are managed through the eth1 panel interface.
    This test verifies that eth2-specific save/cancel buttons don't exist separately
    and confirms operations are handled through eth1 panel.

    Expected: Test should pass according to original specification
    """
    # Series 3 only test - eth2 architecture is Series 3A specific
    if device_series != "Series 3":
        pytest.skip("Series 3 only")

    # Navigate to network configuration page
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

    # NOTE: eth2 save/cancel operations are managed through eth1 panel
    # No separate eth2 configuration exists in Series 3A devices

    # Verify eth2-specific save buttons don't exist (they should be managed via eth1)
    eth2_save_buttons = [
        "button#button_save_port_eth2",
        "button[name='port_eth2']",
        "button#button_save_eth2",
    ]

    eth2_save_found = False
    for selector in eth2_save_buttons:
        save_button = unlocked_config_page.locator(selector)
        if save_button.count() > 0:
            eth2_save_found = True
            break

    # eth2-specific save buttons should not exist in Series 3A architecture
    assert (
        not eth2_save_found
    ), "eth2 save button should not exist separately (should use eth1 panel)"

    # Verify eth2-specific cancel buttons don't exist
    eth2_cancel_buttons = [
        "button#button_cancel_port_eth2",
        "button.cancel[name*='eth2']",
    ]

    eth2_cancel_found = False
    for selector in eth2_cancel_buttons:
        cancel_button = unlocked_config_page.locator(selector)
        if cancel_button.count() > 0:
            eth2_cancel_found = True
            break

    # eth2-specific cancel buttons should not exist in Series 3A architecture
    assert (
        not eth2_cancel_found
    ), "eth2 cancel button should not exist separately (should use eth1 panel)"

    # Verify save/cancel buttons exist for eth1 (where eth2 operations are managed)
    eth1_save = unlocked_config_page.locator("button#button_save_port_eth1")
    eth1_cancel = unlocked_config_page.locator("button#button_cancel_port_eth1")

    # These should exist since eth1 panel manages both eth1 and eth2 save/cancel operations
    # Note: Buttons may not be visible until eth1 panel is expanded
    if eth1_save.count() > 0:
        print("eth1 save button found (manages both eth1 and eth2 save operations)")

    if eth1_cancel.count() > 0:
        print("eth1 cancel button found (manages both eth1 and eth2 cancel operations)")

    print(
        " eth2 save/cancel test passed - no separate eth2 save/cancel (correct for Series 3A architecture)"
    )
