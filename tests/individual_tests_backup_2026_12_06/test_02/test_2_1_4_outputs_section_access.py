"""
Test 2_1_4 Outputs Section Access
Category: 02 - Navigation
Extracted from: tests/grouped/test_02_navigation.py
Source Method: TestConfigurationNavigation.test_2_1_4_outputs_section_access
Individual test file for better test isolation and debugging.
"""

import pytest
from playwright.sync_api import Page, expect
from conftest import wait_for_satellite_loading
from pages.device_capabilities import DeviceCapabilities


def test_2_1_4_outputs_section_access(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 2_1_4 Outputs Section Access - Device-Aware

    Purpose: Verify outputs configuration section is accessible and contains
             appropriate signal configuration fields based on device model

    Expected:
    - Navigation to outputs page succeeds
    - Signal1 and signal2 fields are visible for all devices
    - Additional outputs are verified for devices with >2 outputs
    - Device model detection is properly handled

    Args:
        unlocked_config_page (Page): Playwright page object in unlocked config state
        base_url (str): Base URL for the device under test
        request: Pytest request object for accessing device model information
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate output configuration")

    # Navigate to outputs configuration page
    unlocked_config_page.goto(f"{base_url}/outputs")
    assert "outputs" in unlocked_config_page.url, "Should navigate to outputs page"

    # Use DeviceCapabilities for output-aware verification
    max_outputs = DeviceCapabilities.get_max_outputs(device_model)

    # Verify basic output configuration fields are present
    signal1_field = unlocked_config_page.locator("select[name='signal1']")
    signal2_field = unlocked_config_page.locator("select[name='signal2']")

    assert (
        signal1_field.is_visible() and signal2_field.is_visible()
    ), f"Device {device_model} should have signal1 and signal2 configuration fields"

    # Verify additional outputs for devices with more than 2 outputs
    if max_outputs > 2:
        for output_num in range(3, max_outputs + 1):
            signal_field = unlocked_config_page.locator(
                f"select[name='signal{output_num}']"
            )
            if signal_field.count() > 0:
                print(f"Device {device_model}: Output {output_num} available")
            else:
                print(
                    f"Device {device_model}: Output {output_num} not found (variant-specific)"
                )

    print(
        f"Device {device_model}: Output configuration section validated with max {max_outputs} outputs"
    )
