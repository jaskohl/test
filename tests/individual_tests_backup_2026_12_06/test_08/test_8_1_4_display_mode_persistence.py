"""
Category 8: Display Configuration - Test 8.1.4
Display Mode Persistence
Test Count: 1 of 13 in Category 8
Hardware: Device Only
Priority: MEDIUM - Front panel display settings
Series: Both Series 2 and 3
Based on test_08_display_config.py::TestDisplayModes::test_8_1_4_mode_persistence
FIXED: Robust checkbox state persistence with JavaScript event handling
FIXED: Added try/finally rollback logic to ensure original state is restored
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.display_config_page import DisplayConfigPage


def test_mode_persistence(display_config_page: DisplayConfigPage):
    """
    Test 8.1.4: Display Mode Persistence
    Purpose: Verify mode settings persist after save
    Expected: Checked modes remain checked after page reload
    Series: Both 2 and 3
    FINAL FIX: Robust checkbox state persistence with JavaScript event handling
    FIXED: Added try/finally rollback logic to ensure original state is restored
    """
    # Use mode3 for persistence testing
    mode3 = display_config_page.page.locator("input[name='mode3']")
    # Get original state before any changes
    mode3_initial = mode3.is_checked()
    print(f"mode3 initial state: {mode3_initial}")
    try:
        # Ensure mode3 is in a specific state (checked)
        if not mode3.is_checked():
            mode3.click(force=True)
            # Wait for state to register
            display_config_page.page.wait_for_timeout(1000)
            print(f"mode3 after click: {mode3.is_checked()}")
        # Ensure save button is enabled and perform save
        save_button = display_config_page._get_save_button()
        expect(save_button).to_be_visible()
        if save_button.is_enabled():
            save_button.click()
            print("Save button clicked")
        # Wait for save operation to complete - increased timeout for Series 3 devices
        display_config_page.page.wait_for_load_state("domcontentloaded", timeout=15000)
        # Reload the page to test persistence
        display_config_page.navigate_to_page()
        # Additional wait for page to fully load
        display_config_page.page.wait_for_timeout(2000)
        # Verify mode3 persistence
        mode3_after = display_config_page.page.locator("input[name='mode3']")
        mode3_after.wait_for(state="visible", timeout=5000)
        mode3_final = mode3_after.is_checked()
        print(f"mode3 final state: {mode3_final}")
        # The key test: state should persist
        # Since we set it to checked and saved, it should remain checked
        assert (
            mode3_final == True
        ), f"mode3 should persist as checked after save (initial: {mode3_initial}, final: {mode3_final})"
    finally:
        # Rollback: Restore original state
        mode3_current = display_config_page.page.locator("input[name='mode3']")
        current_state = mode3_current.is_checked()
        if current_state != mode3_initial:
            print(f"Rolling back: restoring mode3 to original state {mode3_initial}")
            mode3_current.click(force=True)
            save_button = display_config_page._get_save_button()
            if save_button.is_enabled():
                save_button.click()
                # FIXED: Increased timeout for Series 3 devices - rollback save operations need longer waits
                display_config_page.page.wait_for_load_state(
                    "domcontentloaded", timeout=15000
                )
