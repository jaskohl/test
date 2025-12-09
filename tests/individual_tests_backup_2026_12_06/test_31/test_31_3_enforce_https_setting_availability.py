"""
Test 31.3: HTTPS Enforcement Setting Availability
Category: 31 - HTTPS Enforcement Scenarios
Extracted from: tests/grouped/test_31_https_enforcement_scenarios.py
Source Method: TestHTTPSSettingAvailability.test_31_3_enforce_https_setting_availability
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect


def test_31_3_enforce_https_setting_availability(access_config_page):
    """
    Test 31.3: HTTPS Enforcement Setting Availability
    Purpose: Verify HTTPS enforcement setting exists and provides required options
    Expected: Access configuration page includes HTTPS enforcement selector with NEVER, CFG_ONLY, ALWAYS
    NOTE: This test validates UI availability but does not test enforcement behavior.
    FIXED: Moved outside parametrized class to avoid parameter conflicts
    Series: Both Series 2 and 3
    """
    # Verify the HTTPS enforcement selector exists and has the expected options
    enforce_select = access_config_page.page.locator("select[name='enforce_https']")
    expect(enforce_select).to_be_visible()
    # Check that the expected options are available
    available_modes = access_config_page.get_available_https_modes()
    # All three modes should be available
    mode_values = [mode["value"] for mode in available_modes]
    assert "NEVER" in mode_values, "HTTPS enforcement should support NEVER mode"
    assert "CFG_ONLY" in mode_values, "HTTPS enforcement should support CFG_ONLY mode"
    assert "ALWAYS" in mode_values, "HTTPS enforcement should support ALWAYS mode"
    print(
        f"Available HTTPS enforcement modes: {[mode['value'] for mode in available_modes]}"
    )
    # Verify that each mode has a meaningful description/text
    for mode in available_modes:
        assert mode["text"], f"Mode {mode['value']} should have a description"
        assert (
            len(mode["text"]) > 0
        ), f"Mode {mode['value']} description should not be empty"
