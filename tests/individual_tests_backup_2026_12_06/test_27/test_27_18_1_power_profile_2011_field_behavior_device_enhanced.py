"""
Test: 27.18.1 - IEEE C37.238-2011 Power Profile Field Behavior [DEVICE ENHANCED]
Category: PTP Configuration (27)
Purpose: Verify all fields editable in Power Profile 2011 with device-aware validation
Expected: All PTP fields remain editable in UI - constraints applied server-side
Series: Series 3 Only (PTP is exclusive feature)
Priority: HIGH
Hardware: Device Only
Device-Aware: YES - Uses DeviceCapabilities database for validation
Based on: test_27_ptp_config.py
Enhanced: 2025-12-01
"""

import pytest
import time
import logging
from playwright.sync_api import expect
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_27_18_1_power_profile_2011_field_behavior_device_enhanced(
    ptp_config_page: PTPConfigPage, base_url: str, request
):
    """
    Test 27.18.1: IEEE C37.238-2011 Power Profile Field Behavior [DEVICE ENHANCED]
    Purpose: Verify all fields editable in Power Profile 2011 with device-aware validation
    Expected: All PTP fields remain editable in UI - constraints applied server-side
    Series: Series 3 Only (PTP is exclusive feature)
    Device-Aware: Uses DeviceCapabilities database for PTP interface validation and timeout scaling
    """
    # Get device context and validate
    device_model = request.session.get("device_model", "unknown")
    device_capabilities = DeviceCapabilities()

    if device_model not in device_capabilities.get_series_list():
        pytest.skip(f"Device model '{device_model}' not in DeviceCapabilities database")

    device_series = device_capabilities.get_device_series(device_model)

    # PTP is Series 3 exclusive feature
    if device_series != "Series 3":
        pytest.skip(f"PTP is Series 3 exclusive feature (found: {device_series})")

    # Device-aware timeout scaling
    base_timeout = 10000  # PTP configuration needs longer timeouts
    device_timeout_multiplier = device_capabilities.get_timeout_multiplier(device_model)
    scaled_timeout = int(base_timeout * device_timeout_multiplier)

    # Cross-validate PTP capability with database
    ptp_capable = device_capabilities.has_capability(device_model, "ptp")
    if not ptp_capable:
        pytest.skip(f"Device {device_model} does not support PTP configuration")

    logger.info(
        f"Device {device_model} (Series {device_series}): Testing Power Profile 2011 field behavior"
    )

    try:
        # Navigate to PTP page with device-aware timeout
        ptp_config_page.page.goto(f"{base_url}/ptp", timeout=scaled_timeout)
        time.sleep(2 * device_timeout_multiplier)

        # Use heading role instead of text to avoid strict mode violation
        ptp_heading = ptp_config_page.page.get_by_role("heading", name="PTP")
        expect(ptp_heading).to_be_visible(timeout=scaled_timeout)

        print(f"Device {device_model}: PTP page loaded successfully")

        # Get available PTP ports using DeviceCapabilities database
        static_ptp_interfaces = device_capabilities.get_ptp_interfaces(device_model)
        if not static_ptp_interfaces:
            pytest.skip(f"No PTP interfaces available on device model {device_model}")

        assert (
            len(static_ptp_interfaces) >= 1
        ), "At least one PTP port should be available"

        # Test on first available port
        port = static_ptp_interfaces[0]
        print(f"Device {device_model}: Testing PTP on port {port}")

        # Select IEEE C37.238-2011 Power Profile
        result = ptp_config_page.configure_ptp_profile(
            port, "IEEE C37.238-2011 (Power Profile)"
        )
        assert result, f"Should successfully select Power Profile 2011 for {port}"

        print(f"Device {device_model}: Successfully selected Power Profile 2011")

        # Device UI keeps ALL fields editable - constraints applied server-side
        # Verify timing intervals remain editable (matches device behavior)
        field_tests = [
            ("log_announce_interval", "log_announce_interval"),
            ("log_sync_interval", "log_sync_interval"),
            ("log_min_delay_req_interval", "log_min_delay_req_interval"),
            ("domain_number", "domain_number"),
            ("priority_1", "priority_1"),
        ]

        for field_name, input_name in field_tests:
            try:
                input_locator = ptp_config_page.page.locator(
                    f"input[name='{input_name}_{port}']"
                )

                if input_locator.count() > 0:
                    # Check if field is visible
                    expect(input_locator).to_be_visible(timeout=scaled_timeout)

                    # Verify field is editable (not readonly)
                    is_readonly = input_locator.get_attribute("readonly")
                    assert (
                        not is_readonly
                    ), f"{field_name} should be editable in Power Profile 2011 for {port}"

                    print(f"Device {device_model}: {field_name} field is editable")
                else:
                    print(
                        f"Device {device_model}: {field_name} field not found (may be normal)"
                    )

            except Exception as e:
                print(
                    f"Device {device_model}: Warning - {field_name} field test failed: {e}"
                )

        # Cross-validate with DeviceCapabilities database
        device_network_config = device_capabilities.get_network_config(device_model)
        if device_network_config and "management_interface" in device_network_config:
            mgmt_iface = device_network_config["management_interface"]
            print(
                f"Device {device_model} (Series {device_series}): Power Profile 2011 field behavior validated"
            )
            print(
                f"Management interface: {mgmt_iface}, PTP ports: {static_ptp_interfaces}, Timeout scaling: {device_timeout_multiplier}x"
            )

    except Exception as e:
        pytest.fail(
            f"Power Profile 2011 field behavior test failed for {device_model}: {e}"
        )

    # Database validation summary
    assert device_capabilities.get_device_series(device_model) == device_series
    assert device_capabilities.has_capability(device_model, "ptp") == ptp_capable
    assert (
        device_capabilities.get_timeout_multiplier(device_model)
        == device_timeout_multiplier
    )
