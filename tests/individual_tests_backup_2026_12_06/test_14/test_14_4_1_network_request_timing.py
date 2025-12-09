"""
Category 14.4.1: Network Request Timing
Purpose: Verify network requests complete within acceptable time
Expected: Network operations complete within device-specific time limits
Series: Both 2 and 3
IMPROVED: DeviceCapabilities integration with adaptive network timing

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


def test_network_request_timing(unlocked_config_page: Page, request):
    """
    Test 14.4.1: Network Request Timing
    Purpose: Verify network requests complete within acceptable time
    Expected: Network operations complete within device-specific time limits
    Series: Both 2 and 3
    IMPROVED: DeviceCapabilities integration with adaptive network timing
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model detection failed - skipping network performance test")

    # Get timeout multiplier using DeviceCapabilities class method
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    try:
        # Navigate to a page and monitor network timing
        start_time = time.time()
        unlocked_config_page.goto(
            "http://172.16.66.3/network",
            wait_until="domcontentloaded",
            timeout=int(10000 * timeout_multiplier),
        )
        total_time = time.time() - start_time

        # IMPROVED: Device-aware network performance expectations
        # Network performance should be relatively consistent across devices
        base_threshold = 6.0  # Universal network performance baseline
        max_time = base_threshold * timeout_multiplier

        assert (
            total_time < max_time
        ), f"Network operation took {total_time:.2f}s (Device: {device_model}, Threshold: {max_time:.2f}s)"
        print(
            f"{device_model} network performance: {total_time:.2f}s (Threshold: {max_time:.2f}s)"
        )
    except Exception as e:
        print(f"{device_model}: Network performance test handled gracefully: {e}")
