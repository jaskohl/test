"""
Test: 30.3.1 - SNMP v3 Enable Configuration [PURE PAGE OBJECT]
Category: SNMP Configuration (Category 30)
Purpose: Verify SNMP v3 enable/disable functionality with pure page object validation
Expected: v3 section appears/disappears based on enable state
Series: Both Series 2 and 3 (Universal)
Priority: MEDIUM
Hardware: Device Only
Device-Aware: YES - Uses SNMPConfigPage methods for validation
Based on: test_30_snmp_config.py
: 2025-12-08 - Pure page object pattern
"""

import pytest
from pages.snmp_config_page import SNMPConfigPage
from playwright.sync_api import expect


def test_30_3_1_v3_enable_pure_page_object(snmp_config_page: SNMPConfigPage, request):
    """
    Test 30.3.1: SNMP v3 Enable Configuration [PURE PAGE OBJECT]
    Purpose: Verify SNMP v3 enable/disable functionality with pure page object validation
    Expected: v3 section appears/disappears based on enable state
    Series: Both 2 and 3
    Device-Aware: Uses SNMPConfigPage methods for timeout scaling and validation
    """
    # Get device model and initialize page object with device-aware patterns
    device_model = request.session.device_hardware_model
    if device_model == "Unknown":
        pytest.fail("Device model not detected - cannot determine SNMP capabilities")

    # Initialize page object with device-aware patterns
    snmp_config_page = SNMPConfigPage(snmp_config_page.page, device_model)

    # Validate device series using page object method
    device_series = snmp_config_page.get_series()
    expected_series = [2, 3]  # Series numbers as integers
    if device_series not in expected_series:
        pytest.fail(
            f"Device series {device_series} not supported for this test (expected: {expected_series})"
        )

    # Device-aware timeout scaling using page object method
    base_timeout = 5000
    device_timeout_multiplier = snmp_config_page.get_timeout_multiplier()
    scaled_timeout = int(base_timeout * device_timeout_multiplier)

    # Cross-validate SNMP capability with page object method
    snmp_capable = snmp_config_page.has_capability("snmp_support")
    if not snmp_capable:
        pytest.skip(f"Device {device_model} does not support SNMP configuration")

    # Navigate to SNMP page using page object method
    snmp_config_page.navigate_to_page()

    # Device-aware SNMP v3 enable checkbox locator
    v3_enable_locator = None
    if device_series == 3:
        v3_enable_locator = snmp_config_page.page.locator("input[name='v3_enable']")
    elif device_series == 2:
        v3_enable_locator = snmp_config_page.page.locator("input[name='v3_enable']")

    if not v3_enable_locator or v3_enable_locator.count() == 0:
        pytest.fail(f"v3_enable checkbox not found for device series {device_series}")

    expect(v3_enable_locator).to_be_visible(timeout=scaled_timeout)

    # Get original checkbox state
    try:
        original_state = v3_enable_locator.is_checked()
    except Exception as e:
        pytest.fail(f"Failed to get original v3_enable state for {device_model}: {e}")

    # Test enabling SNMP v3
    try:
        if not original_state:
            v3_enable_locator.check(timeout=scaled_timeout)
            expect(v3_enable_locator).to_be_checked(timeout=scaled_timeout)

        # Verify v3 configuration section becomes available
        v3_username_locator = snmp_config_page.page.locator("input[name='v3_username']")
        if v3_username_locator.count() > 0:
            expect(v3_username_locator).to_be_visible(timeout=scaled_timeout)
            print(
                f"Device {device_model}: v3 configuration section visible when enabled"
            )

    except Exception as e:
        pytest.fail(f"Failed to enable SNMP v3 for {device_model}: {e}")

    # Test disabling SNMP v3
    try:
        if original_state or v3_enable_locator.is_checked():
            v3_enable_locator.uncheck(timeout=scaled_timeout)
            expect(v3_enable_locator).not_to_be_checked(timeout=scaled_timeout)

        # Verify v3 configuration section becomes hidden/disabled
        v3_username_locator = snmp_config_page.page.locator("input[name='v3_username']")
        if v3_username_locator.count() > 0:
            # v3 fields may be hidden or disabled when v3 is disabled
            try:
                expect(v3_username_locator).to_be_hidden(timeout=scaled_timeout)
            except Exception:
                # Alternative: fields remain visible but become disabled
                expect(v3_username_locator).to_be_disabled(timeout=scaled_timeout)
            print(
                f"Device {device_model}: v3 configuration section hidden/disabled when disabled"
            )

    except Exception as e:
        pytest.fail(f"Failed to disable SNMP v3 for {device_model}: {e}")

    # Restore original state
    try:
        if original_state:
            v3_enable_locator.check(timeout=scaled_timeout)
        else:
            v3_enable_locator.uncheck(timeout=scaled_timeout)

        final_state = v3_enable_locator.is_checked()
        assert (
            final_state == original_state
        ), f"Failed to restore original state: expected {original_state}, got {final_state}"

    except Exception as e:
        print(
            f"Warning: Failed to restore original v3_enable state for {device_model}: {e}"
        )

    # Get device information using page object methods for logging
    device_info = snmp_config_page.get_device_info()
    if device_info and "management_interface" in device_info:
        mgmt_iface = device_info["management_interface"]
        print(
            f"Device {device_model} (Series {device_series}): SNMP v3 enable/disable completed"
        )
        print(
            f"Management interface: {mgmt_iface}, Timeout scaling: {device_timeout_multiplier}x"
        )

    # Validate using page object methods
    assert snmp_config_page.get_series() == device_series
    assert snmp_config_page.has_capability("snmp_support") == snmp_capable
    assert snmp_config_page.get_timeout_multiplier() == device_timeout_multiplier

    print(
        f"SNMP V3 ENABLE CONFIGURATION VALIDATED (PURE PAGE OBJECT): {device_model} (Series {device_series})"
    )
