"""
Category 14: Performance Tests
Test: 14.1.1 - Dashboard Page Load Time
Purpose: Verify dashboard loads within acceptable performance thresholds
Expected: Load time within device-specific performance expectations
Hardware: Device Only
Priority: LOW - Performance validation
Series: Both Series 2 and 3

IMPROVED: DeviceCapabilities integration with adaptive timeouts
Uses request.session.device_hardware_model for model-specific logic
Integrates device_capabilities.get_timeout_multiplier() for adaptive timeouts
"""

import pytest
import time
from playwright.sync_api import Page
from pages.device_capabilities import DeviceCapabilities


def test_14_1_1_dashboard_load_time(logged_in_page: Page, base_url: str, request):
    """
    Test 14.1.1: Dashboard Page Load Time
    Purpose: Verify dashboard loads within acceptable performance thresholds
    Expected: Load time within device-specific performance expectations
    Series: Both 2 and 3
    IMPROVED: DeviceCapabilities integration with adaptive timeouts
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model detection failed - skipping dashboard performance test"
        )

    # Get timeout multiplier using DeviceCapabilities class method
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Navigate to dashboard
    start_time = time.time()
    logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")
    load_time = time.time() - start_time

    # IMPROVED: Device-aware performance thresholds with timeout multiplier
    # Base thresholds adjusted for known device performance characteristics
    device_series = DeviceCapabilities.get_series(device_model)
    if device_series == "Series 2":
        base_threshold = 20.0  # Series 2 baseline performance
    else:  # Series 3
        base_threshold = 6.0  # Series 3 baseline performance (faster devices)

    max_time = base_threshold * timeout_multiplier

    assert (
        load_time < max_time
    ), f"Dashboard took {load_time:.2f}s (Device: {device_model}, Threshold: {max_time:.2f}s)"
    print(
        f"Dashboard load time: {load_time:.2f}s (Device: {device_model}, Threshold: {max_time:.2f}s)"
    )
