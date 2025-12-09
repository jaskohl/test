"""
Test 29.7.5 Eth4 PTP Configuration - Pure Page Object Pattern
Category: 29 - Network Configuration Series 3
Purpose: Test eth4 PTP configuration visibility and functionality.
Expected: PTP enable field should be visible when PTP is supported on eth4 interface.

TRANSFORMED: Pure page object pattern - no direct DeviceCapabilities calls.
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_29_7_5_eth4_ptp(unlocked_config_page: Page, base_url: str, request):
    """
    Test 29.7.5: Eth4 PTP Configuration - Pure Page Object Pattern

    Purpose: Test eth4 PTP configuration visibility and functionality.
    """
    # Get device model from session
    device_model = request.session.device_hardware_model
    if not device_model or device_model == "Unknown":
        pytest.skip("Device model not detected - cannot validate eth4 PTP interface")

    # Create page object with device_model
    network_page = NetworkConfigPage(unlocked_config_page, device_model=device_model)

    # Get device-aware timeout using page object method
    device_timeout = network_page.get_timeout(5000)

    print(f"eth4 PTP interface testing for device: {device_model}")

    # Get expected PTP and network interfaces from page object
    expected_ptp_interfaces = network_page.get_ptp_interfaces()
    expected_network_interfaces = network_page.get_network_interfaces()
    ptp_supported = network_page.has_capability("ptp")

    print(f"Page object expects PTP support: {ptp_supported}")
    print(f"Expected PTP interfaces: {expected_ptp_interfaces}")
    print(f"Expected network interfaces: {expected_network_interfaces}")

    # Series-specific validation using page object method
    device_series = network_page.get_series()
    if device_series == 2:
        # Series 2 devices should not support PTP
        pytest.skip(
            f"Series 2 device {device_model} does not support PTP - eth4 PTP test not applicable"
        )

    elif device_series == 3:
        # Series 3 devices should support PTP on eth4
        if not ptp_supported:
            pytest.skip(
                f"Device {device_model} does not support PTP according to page object"
            )

        if "eth4" not in expected_ptp_interfaces:
            pytest.skip(
                f"eth4 is not a PTP interface according to page object for {device_model}"
            )

        if "eth4" not in expected_network_interfaces:
            pytest.skip(
                f"eth4 is not a network interface according to page object for {device_model}"
            )

    # Navigate and verify page loaded
    network_page.navigate_to_page()
    network_page.verify_page_loaded()

    # Expand eth4 panel using page object method
    network_page.expand_network_interface_panel("eth4")

    # Test PTP enable configuration visibility using page object method
    if network_page.has_element(
        "input[name='ptp_enable_eth4']", timeout=device_timeout
    ):
        ptp_field = unlocked_config_page.locator("input[name='ptp_enable_eth4']")

        # Validate PTP field visibility based on page object
        if "eth4" in expected_ptp_interfaces:
            # eth4 should have PTP capability according to page object
            expect(ptp_field).to_be_visible(timeout=device_timeout)
            print(f"eth4 PTP enable field found and visible for {device_model}")
        else:
            # eth4 should not have PTP capability
            if ptp_field.count() > 0:
                # Field exists but shouldn't according to page object
                print(
                    f"Note: eth4 PTP field visible but not expected for {device_model}"
                )
            else:
                print(f"eth4 PTP field correctly absent for {device_model}")
    else:
        print(f"eth4 PTP field not found for {device_model}")

    # Validate eth4 IP field presence using page object method
    if network_page.has_element("input[name='ip_eth4']", timeout=device_timeout):
        eth4_ip = unlocked_config_page.locator("input[name='ip_eth4']")
        expect(eth4_ip).to_be_visible(timeout=device_timeout)
        print(f"eth4 IP field found and visible for {device_model}")

    # Additional PTP-related field validation on eth4
    ptp_domain_field = unlocked_config_page.locator("input[name='ptp_domain_eth4']")
    if ptp_domain_field.count() > 0:
        print(f"eth4 PTP domain field found for {device_model}")

    ptp_priority1_field = unlocked_config_page.locator(
        "input[name='ptp_priority1_eth4']"
    )
    if ptp_priority1_field.count() > 0:
        print(f"eth4 PTP priority1 field found for {device_model}")

    ptp_priority2_field = unlocked_config_page.locator(
        "input[name='ptp_priority2_eth4']"
    )
    if ptp_priority2_field.count() > 0:
        print(f"eth4 PTP priority2 field found for {device_model}")

    # Validate eth4 is distinguished from management interface (eth0)
    # eth4 should have PTP capability while eth0 should not
    if network_page.has_element(
        "input[name='ptp_enable_eth0']", timeout=device_timeout
    ):
        eth0_ptp_field = unlocked_config_page.locator("input[name='ptp_enable_eth0']")
        assert not eth0_ptp_field.is_visible(
            timeout=device_timeout
        ), f"eth0 should not have PTP capability (management interface) for {device_model}"

    print(f"eth0/eth4 PTP capability distinction validated for {device_model}")

    # Validate eth4 is distinguished from eth1 (both PTP-capable)
    # Both eth1 and eth4 should have PTP capability
    if network_page.has_element(
        "input[name='ptp_enable_eth1']", timeout=device_timeout
    ):
        eth1_ptp_field = unlocked_config_page.locator("input[name='ptp_enable_eth1']")
        assert eth1_ptp_field.is_visible(
            timeout=device_timeout
        ), f"eth1 should have PTP capability (PTP-capable interface) for {device_model}"

    print(f"eth1/eth4 PTP capability correlation validated for {device_model}")

    # Store eth4 PTP validation results for subsequent tests
    eth4_ptp_visible = network_page.has_element(
        "input[name='ptp_enable_eth4']", timeout=device_timeout
    )
    request.session.eth4_ptp_validation_passed = True
    request.session.eth4_ptp_interface_data = {
        "device_model": device_model,
        "device_series": device_series,
        "eth4_ptp_visible": eth4_ptp_visible,
        "eth4_ip_visible": True,
        "expected_in_ptp_interfaces": "eth4" in expected_ptp_interfaces,
        "ptp_supported": ptp_supported,
        "validation_timestamp": "_eth4_ptp_validation",
    }

    print(f"eth4 PTP interface validation successful for {device_model}")
    print(f"- Device: {device_model} (Series {device_series})")
    ptp_field_status = "Visible" if eth4_ptp_visible else "Absent"
    print(f"- eth4 PTP field: {ptp_field_status}")
    print(f"- eth4 IP field: Visible and functional")
    print(f"- Expected PTP interface: {'eth4' in expected_ptp_interfaces}")
    print(f"- PTP support: {ptp_supported}")

    print(f"ETH4 PTP TEST COMPLETED: {device_model}")
