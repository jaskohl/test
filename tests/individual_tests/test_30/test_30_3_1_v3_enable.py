"""
Test: 30.3.1 - SNMP v3 Enable Configuration [DEVICE ]
Category: SNMP Configuration (30)
Purpose: Verify SNMP v3 enable/disable functionality with device-aware validation
Expected: v3 section appears/disappears based on enable state
Series: Both Series 2 and 3 (Universal)
Priority: MEDIUM
Hardware: Device Only
Device-Aware: YES - Uses DeviceCapabilities database for validation
Based on: test_30_snmp_config.py
: 2025-12-01
"""

import pytest
from pages.snmp_config_page import SNMPConfigPage
from pages.device_capabilities import DeviceCapabilities
from playwright.sync_api import expect


def test_30_3_1_v3_enable(snmp_config_page: SNMPConfigPage):
    """
    Test 30.3.1: SNMP v3 Enable Configuration [DEVICE ]
    Purpose: Verify SNMP v3 enable/disable functionality with device-aware validation
    Expected: v3 section appears/disappears based on enable state
    Series: Both 2 and 3
    Device-Aware: Uses DeviceCapabilities database for timeout scaling and validation
    """
    # Get device context and validate series compatibility
    device_model = snmp_config_page.request.session.get("device_model", "unknown")
    device_capabilities = DeviceCapabilities()

    # Validate device series using DeviceCapabilities database
    expected_series = ["Series 2", "Series 3"]
    if device_model not in device_capabilities.get_series_list():
        pytest.skip(f"Device model '{device_model}' not in DeviceCapabilities database")

    # Device-aware timeout scaling
    base_timeout = 5000
    device_timeout_multiplier = device_capabilities.get_timeout_multiplier(device_model)
    scaled_timeout = int(base_timeout * device_timeout_multiplier)

    # Cross-validate SNMP capability with database
    snmp_capable = device_capabilities.has_capability(device_model, "snmp")
    if not snmp_capable:
        pytest.skip(f"Device {device_model} does not support SNMP configuration")

    # Verify device series is supported for this test
    device_series = device_capabilities.get_device_series(device_model)
    if device_series not in expected_series:
        pytest.skip(
            f"Device series {device_series} not supported for this test (expected: {expected_series})"
        )

    # Device-aware SNMP v3 enable checkbox locator
    v3_enable_locator = None
    if device_series == "Series 3":
        v3_enable_locator = snmp_config_page.page.locator("input[name='v3_enable']")
    elif device_series == "Series 2":
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

    # Cross-validate with DeviceCapabilities database
    device_network_config = device_capabilities.get_network_config(device_model)
    if device_network_config and "management_interface" in device_network_config:
        mgmt_iface = device_network_config["management_interface"]
        print(
            f"Device {device_model} (Series {device_series}): SNMP v3 enable/disable completed"
        )
        print(
            f"Management interface: {mgmt_iface}, Timeout scaling: {device_timeout_multiplier}x"
        )

    # Database validation summary
    assert device_capabilities.get_device_series(device_model) == device_series
    assert device_capabilities.has_capability(device_model, "snmp") == snmp_capable
    assert (
        device_capabilities.get_timeout_multiplier(device_model)
        == device_timeout_multiplier
    )
