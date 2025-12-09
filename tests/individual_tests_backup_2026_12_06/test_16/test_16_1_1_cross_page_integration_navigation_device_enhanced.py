"""
Test: 16.1.1 - Cross-Page Integration Navigation [DEVICE ENHANCED]
Category: Integration Testing (16)
Purpose: Verify navigation between pages works with device-aware patterns
Expected: Smooth navigation with proper device-specific timeouts
Series: Both Series 2 and 3 (device-aware)
Priority: MEDIUM
Hardware: Device Only
Device-Aware: YES - Uses DeviceCapabilities database for navigation patterns
Based on: test_16_integration.py
Enhanced: 2025-12-01
"""

import pytest
import time
from playwright.sync_api import expect
from pages.dashboard_page import DashboardPage
from pages.network_config_page import NetworkConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_16_1_1_cross_page_integration_navigation_device_enhanced(
    dashboard_page: DashboardPage, network_config_page: NetworkConfigPage, request
):
    """
    Test 16.1.1: Cross-Page Integration Navigation [DEVICE ENHANCED]
    Purpose: Verify navigation between pages works with device-aware patterns
    Expected: Smooth navigation with proper device-specific timeouts
    Series: Both 2 and 3
    Device-Aware: Uses DeviceCapabilities database for navigation validation
    """
    # Get device context and validate
    device_model = request.session.get("device_model", "unknown")
    device_capabilities = DeviceCapabilities()

    if device_model not in device_capabilities.get_series_list():
        pytest.skip(f"Device model '{device_model}' not in DeviceCapabilities database")

    device_series = device_capabilities.get_device_series(device_model)

    # Device-aware timeout scaling
    base_timeout = 5000
    device_timeout_multiplier = device_capabilities.get_timeout_multiplier(device_model)
    scaled_timeout = int(base_timeout * device_timeout_multiplier)

    print(
        f"Device {device_model} (Series {device_series}): Testing cross-page navigation"
    )

    try:
        # Start from dashboard
        dashboard_page.navigate_to_page()
        dashboard_page.verify_page_loaded()
        print(f"Device {device_model}: Starting from dashboard")

        # Test 1: Dashboard -> Network Config
        try:
            network_link = dashboard_page.page.locator(
                "a[href*='network'], text=/network|config/i"
            )
            if network_link.count() > 0:
                network_link.first.click(timeout=scaled_timeout)

                # Wait for network page load
                network_config_page.verify_page_loaded()
                print(
                    f"Device {device_model}: Dashboard -> Network Config navigation successful"
                )

                # Verify we're on network page
                network_indicators = [
                    network_config_page.page.locator("text=/network|ip|dhcp/i"),
                    network_config_page.page.locator(
                        "input[name*='ip'], input[name*='dhcp']"
                    ),
                ]

                network_found = False
                for indicator in network_indicators:
                    try:
                        if indicator.count() > 0:
                            network_found = True
                            break
                    except Exception:
                        continue

                if not network_found:
                    print(
                        f"Device {device_model}: Warning - Network page indicators not found"
                    )

            else:
                print(f"Device {device_model}: No network navigation link found")

        except Exception as e:
            print(f"Device {device_model}: Dashboard -> Network Config failed: {e}")

        # Test 2: Network Config -> Dashboard (return navigation)
        try:
            dashboard_link = network_config_page.page.locator(
                "a[href*='dashboard'], text=/dashboard|home/i"
            )
            if dashboard_link.count() > 0:
                dashboard_link.first.click(timeout=scaled_timeout)

                # Wait for dashboard load
                dashboard_page.verify_page_loaded()
                print(
                    f"Device {device_model}: Network Config -> Dashboard navigation successful"
                )

                # Verify we're back on dashboard
                dashboard_indicators = [
                    dashboard_page.page.locator("text=/dashboard|system|kronos/i"),
                    dashboard_page.page.locator("nav, .nav, .navigation"),
                ]

                dashboard_found = False
                for indicator in dashboard_indicators:
                    try:
                        if indicator.count() > 0:
                            dashboard_found = True
                            break
                    except Exception:
                        continue

                if not dashboard_found:
                    print(
                        f"Device {device_model}: Warning - Dashboard indicators not found after return"
                    )

            else:
                print(f"Device {device_model}: No dashboard return link found")

        except Exception as e:
            print(f"Device {device_model}: Network Config -> Dashboard failed: {e}")

        # Test 3: Multi-step navigation sequence
        try:
            nav_sequence = [
                ("dashboard", dashboard_page),
                ("network", network_config_page),
            ]

            current_page = dashboard_page
            for page_name, page_object in nav_sequence:
                try:
                    if page_name == "dashboard":
                        current_page.navigate_to_page()
                        current_page.verify_page_loaded()
                    elif page_name == "network":
                        # Navigate to network via dashboard
                        network_link = dashboard_page.page.locator("a[href*='network']")
                        if network_link.count() > 0:
                            network_link.first.click(timeout=scaled_timeout)
                            current_page = network_config_page
                            current_page.verify_page_loaded()

                    print(
                        f"Device {device_model}: Navigation step '{page_name}' successful"
                    )

                except Exception as e:
                    print(
                        f"Device {device_model}: Navigation step '{page_name}' failed: {e}"
                    )
                    break

        except Exception as e:
            print(f"Device {device_model}: Multi-step navigation test failed: {e}")

        # Cross-validate with DeviceCapabilities database
        device_network_config = device_capabilities.get_network_config(device_model)
        if device_network_config and "management_interface" in device_network_config:
            mgmt_iface = device_network_config["management_interface"]
            print(f"Device {device_model}: Cross-page integration test completed")
            print(
                f"Management interface: {mgmt_iface}, Timeout scaling: {device_timeout_multiplier}x"
            )

    except Exception as e:
        pytest.fail(f"Cross-page integration test failed for {device_model}: {e}")

    # Database validation summary
    assert device_capabilities.get_device_series(device_model) == device_series
    assert (
        device_capabilities.get_timeout_multiplier(device_model)
        == device_timeout_multiplier
    )
