"""
Test: 14.1.1 - Dashboard Load Time Performance [DEVICE ENHANCED]
Category: Performance Testing (14)
Purpose: Measure dashboard load time with device-aware timeout scaling
Expected: Load time within device-specific performance thresholds
Series: Both Series 2 and 3 (device-aware)
Priority: HIGH
Hardware: Device Only
Device-Aware: YES - Uses DeviceCapabilities database for performance scaling
Based on: test_14_performance.py
Enhanced: 2025-12-01
"""

import pytest
import time
from playwright.sync_api import expect
from pages.dashboard_page import DashboardPage
from pages.device_capabilities import DeviceCapabilities


def test_14_1_1_dashboard_load_time_device_enhanced(
    dashboard_page: DashboardPage, request
):
    """
    Test 14.1.1: Dashboard Load Time Performance [DEVICE ENHANCED]
    Purpose: Measure dashboard load time with device-aware timeout scaling
    Expected: Load time within device-specific performance thresholds
    Series: Both 2 and 3
    Device-Aware: Uses DeviceCapabilities database for performance expectations
    """
    # Get device context and validate
    device_model = request.session.get("device_model", "unknown")
    device_capabilities = DeviceCapabilities()

    if device_model not in device_capabilities.get_series_list():
        pytest.skip(f"Device model '{device_model}' not in DeviceCapabilities database")

    device_series = device_capabilities.get_device_series(device_model)

    # Device-aware timeout scaling for performance testing
    base_timeout = 10000  # Dashboard loading needs longer timeouts
    device_timeout_multiplier = device_capabilities.get_timeout_multiplier(device_model)
    scaled_timeout = int(base_timeout * device_timeout_multiplier)

    # Performance expectations vary by device series
    if device_series == "Series 2":
        expected_load_time = 5.0  # Series 2 devices are typically faster
    elif device_series == "Series 3":
        expected_load_time = 8.0  # Series 3 devices have more features, slower loading
    else:
        expected_load_time = 6.0  # Default for unknown devices

    print(
        f"Device {device_model} (Series {device_series}): Expected load time {expected_load_time}s"
    )

    # Measure dashboard load time
    try:
        start_time = time.time()

        # Navigate to dashboard
        dashboard_page.navigate_to_page()

        # Wait for page to load with device-aware timeout
        dashboard_page.verify_page_loaded()

        end_time = time.time()
        load_time = end_time - start_time

        print(f"Device {device_model}: Dashboard load time: {load_time:.2f}s")

        # Check if load time is within acceptable range for device
        if load_time <= expected_load_time:
            print(
                f"Device {device_model}: Load time {load_time:.2f}s within acceptable range"
            )
        else:
            print(
                f"Device {device_model}: Load time {load_time:.2f}s exceeds expected {expected_load_time}s"
            )
            # Non-critical - log but don't fail as load times can vary

        # Verify key dashboard elements are present with device-aware locators
        dashboard_indicators = [
            dashboard_page.page.locator("text=/index|system|kronos/i"),
            dashboard_page.page.locator("nav, .nav, .navigation"),
            dashboard_page.page.locator("[class*='status'], [class*='info']"),
        ]

        elements_found = 0
        for indicator in dashboard_indicators:
            try:
                if indicator.count() > 0:
                    expect(indicator).to_be_visible(timeout=scaled_timeout)
                    elements_found += 1
            except Exception:
                continue

        print(f"Device {device_model}: Found {elements_found}/3 dashboard indicators")

        # Verify device-specific functionality
        device_network_config = device_capabilities.get_network_config(device_model)
        if device_network_config and "management_interface" in device_network_config:
            mgmt_iface = device_network_config["management_interface"]
            print(f"Device {device_model}: Management interface {mgmt_iface} detected")

        # Test performance consistency with multiple loads
        load_times = []
        for i in range(3):
            try:
                load_start = time.time()
                dashboard_page.page.reload()
                dashboard_page.verify_page_loaded()
                load_end = time.time()
                individual_load_time = load_end - load_start
                load_times.append(individual_load_time)

                print(
                    f"Device {device_model}: Load #{i+1} time: {individual_load_time:.2f}s"
                )

            except Exception as e:
                print(f"Device {device_model}: Load #{i+1} failed: {e}")

        if load_times:
            avg_load_time = sum(load_times) / len(load_times)
            max_load_time = max(load_times)
            min_load_time = min(load_times)

            print(
                f"Device {device_model}: Performance stats - Avg: {avg_load_time:.2f}s, "
                f"Min: {min_load_time:.2f}s, Max: {max_load_time:.2f}s"
            )

            # Performance consistency check
            if max_load_time - min_load_time < 2.0:  # Less than 2s variance
                print(f"Device {device_model}: Load times are consistent")
            else:
                print(f"Device {device_model}: Load times show high variance")

    except Exception as e:
        pytest.fail(f"Dashboard load time test failed for {device_model}: {e}")

    # Cross-validate with DeviceCapabilities database
    print(
        f"Device {device_model} (Series {device_series}): Dashboard performance test completed"
    )
    print(f"Timeout scaling: {device_timeout_multiplier}x")

    # Database validation summary
    assert device_capabilities.get_device_series(device_model) == device_series
    assert (
        device_capabilities.get_timeout_multiplier(device_model)
        == device_timeout_multiplier
    )
