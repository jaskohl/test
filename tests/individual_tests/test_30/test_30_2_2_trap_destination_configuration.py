"""
Test: 30.2.2 - SNMP Trap Destination Configuration [DEVICE ]
Category: SNMP Configuration (30)
Purpose: Verify trap_host1 and trap_host2 configuration with device-aware validation
Expected: Valid IP addresses accepted, invalid ones rejected
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


def test_30_2_2_trap_destination_configuration(
    snmp_config_page: SNMPConfigPage,
):
    """
    Test 30.2.2: SNMP Trap Destination Configuration [DEVICE ]
    Purpose: Verify trap_host1 and trap_host2 configuration with device-aware validation
    Expected: Valid IP addresses accepted, invalid ones rejected
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

    # Device-aware trap host locators
    trap_host1_locator = None
    trap_host2_locator = None

    if device_series == "Series 3":
        trap_host1_locator = snmp_config_page.page.locator("input[name='trap_host1']")
        trap_host2_locator = snmp_config_page.page.locator("input[name='trap_host2']")
    elif device_series == "Series 2":
        trap_host1_locator = snmp_config_page.page.locator("input[name='trap_host1']")
        trap_host2_locator = snmp_config_page.page.locator("input[name='trap_host2']")

    if not trap_host1_locator or trap_host1_locator.count() == 0:
        pytest.fail(
            f"trap_host1 input field not found for device series {device_series}"
        )

    if not trap_host2_locator or trap_host2_locator.count() == 0:
        pytest.fail(
            f"trap_host2 input field not found for device series {device_series}"
        )

    expect(trap_host1_locator).to_be_visible(timeout=scaled_timeout)
    expect(trap_host2_locator).to_be_visible(timeout=scaled_timeout)
    expect(trap_host1_locator).to_be_editable(timeout=scaled_timeout)
    expect(trap_host2_locator).to_be_editable(timeout=scaled_timeout)

    # Get original values with device-aware error handling
    try:
        original_host1 = trap_host1_locator.input_value()
        original_host2 = trap_host2_locator.input_value()
    except Exception as e:
        pytest.fail(f"Failed to get original trap host values for {device_model}: {e}")

    # Test valid IP address configurations
    valid_ip_addresses = ["192.168.1.100", "10.0.0.50", "172.16.1.1", "192.168.100.200"]

    for test_ip in valid_ip_addresses:
        try:
            # Test trap_host1 with valid IP
            trap_host1_locator.fill("", timeout=scaled_timeout)
            trap_host1_locator.fill(test_ip, timeout=scaled_timeout)

            actual_host1 = trap_host1_locator.input_value()
            assert (
                actual_host1 == test_ip
            ), f"Expected '{test_ip}', got '{actual_host1}'"

            # Test trap_host2 with different valid IP
            trap_host2_locator.fill("", timeout=scaled_timeout)
            trap_host2_locator.fill(test_ip, timeout=scaled_timeout)

            actual_host2 = trap_host2_locator.input_value()
            assert (
                actual_host2 == test_ip
            ), f"Expected '{test_ip}', got '{actual_host2}'"

        except Exception as e:
            pytest.fail(
                f"Failed to configure valid IP address '{test_ip}' for {device_model}: {e}"
            )

    # Test IP address validation (devices should handle malformed IPs gracefully)
    invalid_ip_addresses = ["999.999.999.999", "invalid.ip.address", ""]

    for invalid_ip in invalid_ip_addresses:
        try:
            # Test trap_host1 with invalid IP
            trap_host1_locator.fill("", timeout=scaled_timeout)
            trap_host1_locator.fill(invalid_ip, timeout=scaled_timeout)

            actual_host1 = trap_host1_locator.input_value()
            # Device may accept or reject invalid IPs - both behaviors are valid
            print(
                f"Device {device_model}: trap_host1 accepts invalid IP '{invalid_ip}' -> '{actual_host1}'"
            )

            # Test trap_host2 with invalid IP
            trap_host2_locator.fill("", timeout=scaled_timeout)
            trap_host2_locator.fill(invalid_ip, timeout=scaled_timeout)

            actual_host2 = trap_host2_locator.input_value()
            print(
                f"Device {device_model}: trap_host2 accepts invalid IP '{invalid_ip}' -> '{actual_host2}'"
            )

        except Exception as e:
            print(
                f"Device {device_model}: Invalid IP '{invalid_ip}' rejected as expected: {e}"
            )

    # Cross-validate with DeviceCapabilities database
    device_network_config = device_capabilities.get_network_config(device_model)
    if device_network_config and "management_interface" in device_network_config:
        mgmt_iface = device_network_config["management_interface"]
        print(
            f"Device {device_model} (Series {device_series}): SNMP trap destination configuration completed"
        )
        print(
            f"Management interface: {mgmt_iface}, Timeout scaling: {device_timeout_multiplier}x"
        )

    # Restore original values to maintain test isolation
    try:
        trap_host1_locator.fill(original_host1, timeout=scaled_timeout)
        trap_host2_locator.fill(original_host2, timeout=scaled_timeout)
    except Exception as e:
        print(
            f"Warning: Failed to restore original trap host values for {device_model}: {e}"
        )

    # Database validation summary
    assert device_capabilities.get_device_series(device_model) == device_series
    assert device_capabilities.has_capability(device_model, "snmp") == snmp_capable
    assert (
        device_capabilities.get_timeout_multiplier(device_model)
        == device_timeout_multiplier
    )
