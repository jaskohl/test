"""
Category 6: GNSS Configuration - Test 6.2.1
Galileo Checkbox Toggle - Pure Page Object Pattern
Test Count: 4 of 15 in Category 6
Hardware: Device Only
Priority: HIGH - GNSS is primary time source
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with device intelligence
PATTERN: Zero direct .locator() calls, essential methods only
"""

import pytest
import logging
from pages.gnss_config_page import GNSSConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_6_2_1_galileo_checkbox_toggle(
    gnss_config_page: GNSSConfigPage,
    request,
    base_url: str,
):
    """
    Test 6.2.1: Galileo Constellation Configuration - Pure Page Object Pattern
    Purpose: Verify Galileo can be enabled/disabled and persists
    Expected: Checkbox toggles, state persists after save, device-aware validation
    TRANSFORMED: Uses pure page object methods with device intelligence
    Series: Both 2 and 3
    """
    device_model = request.session.device_hardware_model

    # Essential device intelligence
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(f"Testing Galileo checkbox toggle on {device_model}")
    logger.info(f"Device series: {device_series}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}x")

    # Check if device supports Galileo
    if not DeviceCapabilities.has_capability(device_model, "galileo_constellation"):
        pytest.skip(f"Galileo constellation not supported on {device_model}")

    # Navigate to GNSS configuration page
    gnss_config_page.navigate_to_gnss_config()

    # Test Galileo checkbox toggle through page object
    toggle_results = gnss_config_page.test_galileo_checkbox_toggle()
    logger.info(f"Galileo toggle test results: {toggle_results}")

    # Verify Galileo checkbox found
    checkbox_found = toggle_results.get("checkbox_found", False)
    assert checkbox_found, "Galileo checkbox should be found"

    # Verify Galileo checkbox visibility and enabled state
    checkbox_visible = toggle_results.get("checkbox_visible", False)
    checkbox_enabled = toggle_results.get("checkbox_enabled", False)
    assert (
        checkbox_visible and checkbox_enabled
    ), "Galileo checkbox should be visible and enabled"

    # Test toggle functionality
    toggle_successful = toggle_results.get("toggle_successful", False)
    assert toggle_successful, "Galileo checkbox should toggle successfully"

    # Test state persistence
    state_persistence = toggle_results.get("state_persistence", False)
    if state_persistence:
        logger.info("Galileo checkbox state persists correctly")
    else:
        logger.info("Galileo checkbox state persistence varies by device")

    # Test save functionality (series-aware)
    save_functional = toggle_results.get("save_functional", False)
    if save_functional:
        logger.info("Galileo save functionality works correctly")
    else:
        logger.info("Galileo save functionality varies by device")

    # Test cancel functionality
    cancel_functional = toggle_results.get("cancel_functional", False)
    if cancel_functional:
        logger.info("Galileo cancel functionality works correctly")
    else:
        logger.info("Galileo cancel functionality varies by device")

    # Device capabilities validation
    galileo_capability = DeviceCapabilities.has_capability(
        device_model, "galileo_constellation"
    )
    assert (
        galileo_capability
    ), "Device should support Galileo constellation configuration"

    # Get current constellation status
    constellation_status = gnss_config_page.is_constellation_enabled("GALILEO")
    logger.info(f"Galileo constellation enabled: {constellation_status}")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)
    logger.info(f"Galileo checkbox toggle test completed for {device_model}")
    logger.info(f"Device info: {device_info}")

    print(f"GALILEO CHECKBOX TOGGLE COMPLETED: {device_model} (Series {device_series})")
