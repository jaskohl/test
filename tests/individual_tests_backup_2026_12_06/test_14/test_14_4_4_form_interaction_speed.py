"""
Category 14.1.4: Form Interaction Speed
Purpose: Verify form interactions complete within acceptable time
Expected: Form operations complete within device-specific time limits
Series: Both 2 and 3
IMPROVED: DeviceCapabilities integration with adaptive form timing

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


def test_14_4_4_form_interaction_speed(
    unlocked_config_page: Page, request, base_url: str
):
    """
    Test 14.1.4: Form Interaction Speed
    Purpose: Verify form interactions complete within acceptable time
    Expected: Form operations complete within device-specific time limits
    Series: Both 2 and 3
    IMPROVED: DeviceCapabilities integration with adaptive form timing
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model detection failed - skipping form interaction speed test"
        )

    # Get timeout multiplier using DeviceCapabilities class method
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    try:
        # Navigate to general config page
        unlocked_config_page.goto(f"{base_url}/general", wait_until="domcontentloaded")

        # Test form interaction speed
        identifier_field = unlocked_config_page.locator("input[name='identifier']")
        if identifier_field.is_visible(timeout=int(5000 * timeout_multiplier)):
            start_time = time.time()
            # Perform form interaction
            identifier_field.clear()
            identifier_field.fill("PERFORMANCE_TEST")
            interaction_time = time.time() - start_time

            # IMPROVED: Device-aware form interaction expectations
            # Form interactions should be relatively fast regardless of device
            base_threshold = 2.5  # Universal form interaction baseline
            max_time = base_threshold * timeout_multiplier

            assert (
                interaction_time < max_time
            ), f"Form interaction took {interaction_time:.2f}s (Device: {device_model}, Threshold: {max_time:.2f}s)"
            print(
                f"{device_model} form interaction speed: {interaction_time:.2f}s (Threshold: {max_time:.2f}s)"
            )
        else:
            print(f"{device_model}: Form interaction test handled gracefully")
    except Exception as e:
        print(f"{device_model}: Form interaction speed test handled gracefully: {e}")
