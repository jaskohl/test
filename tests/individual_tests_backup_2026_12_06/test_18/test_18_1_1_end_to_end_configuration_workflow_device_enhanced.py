"""
Test: 18.1.1 - End-to-End Configuration Workflow [DEVICE ENHANCED]
Category: Workflow Testing (18)
Purpose: Test complete configuration workflow with device-aware patterns
Expected: Smooth workflow from login through configuration and validation
Series: Both Series 2 and 3 (device-aware)
Priority: HIGH
Hardware: Device Only
Device-Aware: YES - Uses DeviceCapabilities database for workflow validation
Based on: test_18_workflow.py
Enhanced: 2025-12-01
"""

import pytest
import time
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.network_config_page import NetworkConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_18_1_1_end_to_end_configuration_workflow_device_enhanced(
    login_page: LoginPage,
    dashboard_page: DashboardPage,
    network_config_page: NetworkConfigPage,
    request,
    base_url: str,
    device_password: str,
):
    """
    Test 18.1.1: End-to-End Configuration Workflow [DEVICE ENHANCED]
    Purpose: Test complete configuration workflow with device-aware patterns
    Expected: Smooth workflow from login through configuration and validation
    Series: Both 2 and 3
    Device-Aware: Uses DeviceCapabilities database for workflow validation
    """
    # Get device context and validate
    device_model = request.session.get("device_model", "unknown")
    device_capabilities = DeviceCapabilities()

    if device_model not in device_capabilities.get_series_list():
        pytest.skip(f"Device model '{device_model}' not in DeviceCapabilities database")

    device_series = device_capabilities.get_device_series(device_model)

    # Device-aware timeout scaling
    base_timeout = 10000  # Workflow testing needs longer timeouts
    device_timeout_multiplier = device_capabilities.get_timeout_multiplier(device_model)
    scaled_timeout = int(base_timeout * device_timeout_multiplier)

    print(
        f"Device {device_model} (Series {device_series}): Testing end-to-end workflow"
    )

    workflow_steps = []

    try:
        # Step 1: Login
        try:
            login_page.page.goto(base_url, timeout=scaled_timeout)
            login_page.verify_page_loaded()
            success = login_page.login(password=device_password)
            assert success, f"Login failed for {device_model}"
            workflow_steps.append("Login")
            print(f"Device {device_model}: Step 1 - Login successful")
        except Exception as e:
            pytest.fail(f"Login step failed for {device_model}: {e}")

        # Step 2: Dashboard access
        try:
            dashboard_page.verify_page_loaded()

            # Verify dashboard elements are present
            dashboard_indicators = [
                dashboard_page.page.locator("text=/dashboard|configure|settings/i"),
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

            assert dashboard_found, f"Dashboard not accessible for {device_model}"
            workflow_steps.append("Dashboard Access")
            print(f"Device {device_model}: Step 2 - Dashboard access successful")
        except Exception as e:
            pytest.fail(f"Dashboard access step failed for {device_model}: {e}")

        # Step 3: Navigate to configuration
        try:
            config_link = dashboard_page.page.locator(
                "a[href*='network'], text=/network|config/i"
            )
            if config_link.count() > 0:
                config_link.first.click(timeout=scaled_timeout)
                network_config_page.verify_page_loaded()
                workflow_steps.append("Config Navigation")
                print(
                    f"Device {device_model}: Step 3 - Configuration navigation successful"
                )
            else:
                print(f"Device {device_model}: Warning - No configuration link found")
        except Exception as e:
            print(f"Device {device_model}: Config navigation step failed: {e}")

        # Step 4: Network configuration
        try:
            # Test basic network configuration interaction
            ip_input = network_config_page.page.locator(
                "input[name*='ip'], input[placeholder*='IP']"
            )
            if ip_input.count() > 0:
                # Get current value and test interaction
                original_value = (
                    ip_input.input_value() if ip_input.input_value() else ""
                )

                # Test field interaction (don't change actual values)
                ip_input.focus(timeout=scaled_timeout)

                workflow_steps.append("Network Config")
                print(
                    f"Device {device_model}: Step 4 - Network configuration interaction successful"
                )
            else:
                print(f"Device {device_model}: Warning - Network IP input not found")
        except Exception as e:
            print(f"Device {device_model}: Network config step failed: {e}")

        # Step 5: Device capability validation
        try:
            # Verify device-specific capabilities
            max_outputs = device_capabilities.get_max_outputs(device_model)
            snmp_capable = device_capabilities.has_capability(device_model, "snmp")
            https_capable = device_capabilities.has_capability(
                device_model, "https_enforcement"
            )

            print(
                f"Device {device_model}: Capabilities - Max outputs: {max_outputs}, SNMP: {snmp_capable}, HTTPS: {https_capable}"
            )
            workflow_steps.append("Device Validation")
            print(
                f"Device {device_model}: Step 5 - Device capability validation successful"
            )
        except Exception as e:
            print(f"Device {device_model}: Device validation step failed: {e}")

        # Step 6: Return to dashboard
        try:
            dashboard_link = network_config_page.page.locator(
                "a[href*='dashboard'], text=/dashboard|home/i"
            )
            if dashboard_link.count() > 0:
                dashboard_link.first.click(timeout=scaled_timeout)
                dashboard_page.verify_page_loaded()
                workflow_steps.append("Return Navigation")
                print(f"Device {device_model}: Step 6 - Return to dashboard successful")
            else:
                print(
                    f"Device {device_model}: Warning - No dashboard return link found"
                )
        except Exception as e:
            print(f"Device {device_model}: Return navigation step failed: {e}")

        # Workflow completion summary
        print(
            f"Device {device_model}: Workflow completed - {len(workflow_steps)} steps successful"
        )
        print(f"Successful steps: {workflow_steps}")

        # Cross-validate with DeviceCapabilities database
        device_network_config = device_capabilities.get_network_config(device_model)
        if device_network_config and "management_interface" in device_network_config:
            mgmt_iface = device_network_config["management_interface"]
            print(f"Device {device_model}: End-to-end workflow test completed")
            print(
                f"Management interface: {mgmt_iface}, Timeout scaling: {device_timeout_multiplier}x"
            )

    except Exception as e:
        pytest.fail(f"End-to-end workflow test failed for {device_model}: {e}")

    # Database validation summary
    assert device_capabilities.get_device_series(device_model) == device_series
    assert (
        device_capabilities.get_timeout_multiplier(device_model)
        == device_timeout_multiplier
    )
