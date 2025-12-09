"""
Category 14.1.2: Configuration Page Load Time
Purpose: Verify configuration pages load within acceptable performance thresholds
Expected: Load time within device-specific performance expectations
Series: Both 2 and 3
IMPROVED: DeviceCapabilities integration with model-specific thresholds

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


def test_config_page_load_time(
    unlocked_config_page: Page,
    base_url: str,
    request: pytest.FixtureRequest,
    page: str = "general",
):
    """
    Test 14.1.2: Configuration Page Load Time
    Purpose: Verify configuration pages load within acceptable performance thresholds
    Expected: Load time within device-specific performance expectations
    Series: Both 2 and 3
    IMPROVED: DeviceCapabilities integration with model-specific thresholds
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model detection failed - skipping config page performance test"
        )

    # Get timeout multiplier using DeviceCapabilities class method
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Navigate to configuration page and measure load time
    start_time = time.time()
    unlocked_config_page.goto(f"{base_url}/{page}", wait_until="domcontentloaded")
    load_time = time.time() - start_time

    # IMPROVED: Device-aware thresholds with timeout multiplier
    # Configuration pages typically take longer due to more complex UI
    device_series = DeviceCapabilities.get_series(device_model)
    if device_series == "Series 2":
        base_threshold = 11.0  # Series 2 config page baseline
    else:  # Series 3
        base_threshold = 11.0  # Series 3 config page baseline

    max_time = base_threshold * timeout_multiplier

    assert (
        load_time < max_time
    ), f"/{page} took {load_time:.2f}s (Device: {device_model}, Threshold: {max_time:.2f}s)"
    print(
        f"{device_model} {page} page load time: {load_time:.2f}s (Threshold: {max_time:.2f}s)"
    )
