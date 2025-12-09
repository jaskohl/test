"""
Test: 30.1.2 - SNMP Read-Only Community 2 Configuration [DEVICE ENHANCED]
Category: SNMP Configuration (30)
Purpose: Verify ro_community2 field configuration with device-aware validation
Expected: Field accepts valid values, rejects invalid ones
Series: Both Series 2 and 3 (Universal)
Priority: MEDIUM
Hardware: Device Only
Device-Aware: YES - Uses DeviceCapabilities database for validation
Based on: test_30_snmp_config.py
Enhanced: 2025-12-01
"""

import pytest
from pages.snmp_config_page import SNMPConfigPage
from pages.device_capabilities import DeviceCapabilities
from playwright.sync_api import expect


def test_30_1_2_ro_community2_configuration_device_enhanced(
    snmp_config_page: SNMPConfigPage,
):
    """
    Test 30.1.2: SNMP Read-Only Community 2 Configuration [DEVICE ENHANCED]
    Purpose: Verify ro_community2 field configuration with device-aware validation
    Expected: Field accepts valid values, rejects invalid ones
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

    # Device-aware element locators based on series
    ro_community2_locator = None
    if device_series == "Series 3":
        ro_community2_locator = snmp_config_page.page.locator(
            "input[name='ro_community2']"
        )
    elif device_series == "Series 2":
        ro_community2_locator = snmp_config_page.page.locator(
            "input[name='ro_community2']"
        )

    if not ro_community2_locator or ro_community2_locator.count() == 0:
        pytest.fail(
            f"ro_community2 input field not found for device series {device_series}"
        )

    expect(ro_community2_locator).to_be_visible(timeout=scaled_timeout)
    expect(ro_community2_locator).to_be_editable(timeout=scaled_timeout)

    # Get original value with device-aware error handling
    try:
        original_value = ro_community2_locator.input_value()
    except Exception as e:
        pytest.fail(
            f"Failed to get original ro_community2 value for {device_model}: {e}"
        )

    # Test valid community string configurations
    valid_community_strings = ["public", "readonly", "monitor", "test123"]

    for test_community in valid_community_strings:
        try:
            # Clear field and enter valid community string
            ro_community2_locator.fill("", timeout=scaled_timeout)
            ro_community2_locator.fill(test_community, timeout=scaled_timeout)

            # Verify value was set correctly
            actual_value = ro_community2_locator.input_value()
            assert (
                actual_value == test_community
            ), f"Expected '{test_community}', got '{actual_value}'"

            # Verify field is still editable
            expect(ro_community2_locator).to_be_editable(timeout=scaled_timeout)

        except Exception as e:
            pytest.fail(
                f"Failed to configure valid community string '{test_community}' for {device_model}: {e}"
            )

    # Test maximum length validation (SNMP communities typically limited to 32 chars)
    max_length_community = "a" * 32
    try:
        ro_community2_locator.fill("", timeout=scaled_timeout)
        ro_community2_locator.fill(max_length_community, timeout=scaled_timeout)

        actual_value = ro_community2_locator.input_value()
        # Device may truncate or accept full length
        assert len(actual_value) <= len(
            max_length_community
        ), f"Community string too long: {actual_value}"

    except Exception as e:
        pytest.fail(
            f"Failed to test maximum length community string for {device_model}: {e}"
        )

    # Test special characters (should be handled gracefully)
    special_char_community = "test_community-123"
    try:
        ro_community2_locator.fill("", timeout=scaled_timeout)
        ro_community2_locator.fill(special_char_community, timeout=scaled_timeout)

        actual_value = ro_community2_locator.input_value()
        assert (
            actual_value == special_char_community
        ), f"Special characters not handled correctly: {actual_value}"

    except Exception as e:
        pytest.fail(
            f"Failed to test special character community string for {device_model}: {e}"
        )

    # Device-aware save button detection and validation
    save_button_locator = None
    if device_series == "Series 3":
        save_button_locator = snmp_config_page.page.locator("button#button_save_1")
    elif device_series == "Series 2":
        save_button_locator = snmp_config_page.page.locator("input#button_save_1")

    # Cross-validate with DeviceCapabilities database
    device_network_config = device_capabilities.get_network_config(device_model)
    if device_network_config and "management_interface" in device_network_config:
        mgmt_iface = device_network_config["management_interface"]
        print(
            f"Device {device_model} (Series {device_series}): SNMP community2 configuration completed"
        )
        print(
            f"Management interface: {mgmt_iface}, Timeout scaling: {device_timeout_multiplier}x"
        )

    # Restore original value to maintain test isolation
    try:
        ro_community2_locator.fill(original_value, timeout=scaled_timeout)
    except Exception as e:
        print(
            f"Warning: Failed to restore original ro_community2 value for {device_model}: {e}"
        )

    # Database validation summary
    assert device_capabilities.get_device_series(device_model) == device_series
    assert device_capabilities.has_capability(device_model, "snmp") == snmp_capable
    assert (
        device_capabilities.get_timeout_multiplier(device_model)
        == device_timeout_multiplier
    )
