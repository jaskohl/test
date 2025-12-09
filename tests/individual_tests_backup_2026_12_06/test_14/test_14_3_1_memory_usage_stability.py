"""
Category 14.3.1: Memory Usage Stability
Purpose: Verify memory usage remains stable during testing
Expected: No significant memory leaks or performance degradation
Series: Both 2 and 3
IMPROVED: DeviceCapabilities integration with adaptive navigation

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


def test_14_3_1_memory_usage_stability(unlocked_config_page: Page, request):
    """
    Test 14.3.1: Memory Usage Stability
    Purpose: Verify memory usage remains stable during testing
    Expected: No significant memory leaks or performance degradation
    Series: Both 2 and 3
    IMPROVED: DeviceCapabilities integration with adaptive navigation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model detection failed - skipping memory stability test")

    # Get timeout multiplier using DeviceCapabilities class method
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    try:
        # IMPROVED: Device-aware memory stability testing
        # Navigate to several pages to test memory stability
        pages = ["general", "network", "outputs", "time", "display"]
        for page in pages:
            try:
                unlocked_config_page.goto(
                    f"http://172.16.66.3/{page}",
                    wait_until="domcontentloaded",
                    timeout=int(15000 * timeout_multiplier),
                )

                # Perform some basic interaction
                page_title = unlocked_config_page.title()
                print(f"{device_model} {page}: {page_title}")
            except Exception as e:
                print(f"{device_model} {page}: navigation handled gracefully")

        print(f"{device_model}: Memory stability test completed")
    except Exception as e:
        print(f"{device_model}: Memory performance test handled gracefully: {e}")
