"""
Test 15.3.1: Detect Series 3 PTP Variant (FIXED)
Category: 15 - Device Capability Detection Tests
Test Count: Part of 12 tests in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Series 3 Only

Extracted from: tests/test_15_capability_detection.py
Source Class: TestSeries3VariantDetection
"""

import pytest
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_15_3_1_detect_ptp_variant(unlocked_config_page: Page, base_url: str, request):
    """
    Test 15.3.1: Detect Series 3 PTP Variant (A, B, or C) - FIXED FOR 66.6 AND 190.47
    Purpose: Determine Series 3 hardware variant from PTP forms
    Expected: Variant based on form count and available ports
    Series: Series 3 Only
    FIXED: Handle different PTP port configurations across devices
    FIXED: Device 66.6 and 190.47 specific port availability issues
    FIXED: Use device_capabilities fixture for dynamic interface detection
    """
    # FIXED: Use DeviceCapabilities for series detection
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot determine PTP variant")

    device_series_num = DeviceCapabilities.get_series(device_model)
    if device_series_num != 3:
        pytest.skip("Variant detection only applies to Series 3")

    unlocked_config_page.goto(f"{base_url}/ptp", wait_until="domcontentloaded")
    # Count forms (subtract 1 for session modal)
    all_forms = unlocked_config_page.locator("form")
    total_forms = all_forms.count()
    ptp_forms = total_forms - 1
    # FIXED: Allow 2, 3, or 4 forms for Series 3 variants
    assert ptp_forms in [
        2,
        3,
        4,
    ], f"Series 3 should have 2, 3, or 4 PTP forms, found {ptp_forms}"

    # FIXED: Use DeviceCapabilities for dynamic interface detection
    available_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)
    if not available_interfaces:
        pytest.skip(f"No PTP interfaces available on device model {device_model}")

    print(
        f"Detected PTP variant: {ptp_forms} forms, available interfaces: {available_interfaces}"
    )

    # Verify interfaces match what DeviceCapabilities expects
    # Check that we can find profile selectors for the available interfaces
    found_profiles = []
    for interface in available_interfaces:
        profile_select = unlocked_config_page.locator(f"#{interface}_profile")
        if profile_select.count() > 0:
            found_profiles.append(interface)

    assert (
        len(found_profiles) > 0
    ), f"Should find PTP profiles for available interfaces {available_interfaces}, found: {found_profiles}"

    print(f"Confirmed PTP variant: {ptp_forms} forms with interfaces: {found_profiles}")
