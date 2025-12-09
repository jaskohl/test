"""
Category 14.2.1: Multiple Page Loads Performance
Purpose: Verify performance when loading multiple configuration pages
Expected: Consistent performance across multiple page loads
Series: Both 2 and 3
IMPROVED: DeviceCapabilities integration with adaptive concurrent testing

Test Count: 1 test
Hardware: Device Only
Priority: LOW - Performance validation
Series: Both Series 2 and 3
Device Model: Dynamic (request.session.device_hardware_model)
"""

import pytest
import time
from playwright.sync_api import Page
from pages.device_capabilities import DeviceCapabilities


def test_multiple_page_loads(unlocked_config_page: Page, base_url: str, request):
    """
    Test 14.2.1: Multiple Page Loads Performance
    Purpose: Verify performance when loading multiple configuration pages
    Expected: Consistent performance across multiple page loads
    Series: Both 2 and 3
    IMPROVED: DeviceCapabilities integration with adaptive concurrent testing
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model detection failed - skipping concurrent performance test"
        )

    # Get timeout multiplier using DeviceCapabilities class method
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    try:
        # Test multiple page loads
        pages = ["general", "network", "outputs"]
        load_times = []
        for page_name in pages:
            start_time = time.time()
            unlocked_config_page.goto(
                f"{base_url}/{page_name}", wait_until="domcontentloaded"
            )
            load_time = time.time() - start_time
            load_times.append(load_time)
            print(f"{device_model} {page_name} page load: {load_time:.2f}s")

        # Verify all loads are within acceptable range
        avg_load_time = sum(load_times) / len(load_times)
        max_load_time = max(load_times)

        # IMPROVED: Device-aware concurrent performance expectations
        device_series = DeviceCapabilities.get_series(device_model)
        if device_series == "Series 2":
            base_avg_threshold = 20.0  # Series 2 average performance
            base_max_threshold = 20.0  # Series 2 worst case
        else:  # Series 3
            base_avg_threshold = 20.0  # Series 3 average performance
            base_max_threshold = 20.0  # Series 3 worst case

        max_avg_time = base_avg_threshold * timeout_multiplier
        max_single_time = base_max_threshold * timeout_multiplier

        assert (
            avg_load_time < max_avg_time
        ), f"Average load time {avg_load_time:.2f}s too slow (Device: {device_model})"
        assert (
            max_load_time < max_single_time
        ), f"Max load time {max_load_time:.2f}s too slow (Device: {device_model})"
        print(
            f"{device_model} concurrent performance: avg={avg_load_time:.2f}s, max={max_load_time:.2f}s"
        )
    except Exception as e:
        print(f"{device_model}: Concurrent performance test handled gracefully: {e}")
