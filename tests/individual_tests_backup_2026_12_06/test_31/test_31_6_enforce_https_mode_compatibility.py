"""
Test 31.6: HTTPS Enforcement Mode Compatibility
Category: 31 - HTTPS Enforcement Scenarios
Extracted from: tests/grouped/test_31_https_enforcement_scenarios.py
Source Method: TestHTTPSEnforcementConfigurationValidation.test_31_6_enforce_https_mode_compatibility
Individual test file for better test isolation and debugging.
"""

import pytest


@pytest.mark.parametrize("target_mode", ["NEVER", "CFG_ONLY", "ALWAYS"])
def test_31_6_enforce_https_mode_compatibility(
    access_config_page, target_mode: str, device_capabilities: dict
):
    """
    Test 31.6: HTTPS Enforcement Mode Compatibility
    Purpose: Verify device correctly reports compatibility with different HTTPS modes
    Expected: Device allows configuration of any valid HTTPS enforcement mode
    WARNING: This test reads current configuration but does not modify it.
    Series: Both Series 2 and 3
    """
    # Verify the target mode is supported by the device
    available_modes = access_config_page.get_available_https_modes()
    mode_values = [mode["value"] for mode in available_modes]
    assert (
        target_mode in mode_values
    ), f"Device should support HTTPS enforcement mode '{target_mode}'"
    # Verify the mode has a proper description
    mode_info = next(
        (mode for mode in available_modes if mode["value"] == target_mode), None
    )
    assert mode_info is not None, f"Should find information for mode '{target_mode}'"
    assert "text" in mode_info, f"Mode '{target_mode}' should have text description"
    assert (
        len(mode_info["text"]) > 0
    ), f"Mode '{target_mode}' should have non-empty description"
    print(f"HTTPS enforcement mode '{target_mode}' is supported: '{mode_info['text']}'")
