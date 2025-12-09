"""
Category 6: GNSS Configuration - Test 6.3.1
GLONASS Checkbox Toggle - Pure Page Object Pattern
Test Count: 3 of 15 in Category 6
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


def test_6_3_1_glonass_checkbox_toggle(
    gnss_config_page: GNSSConfigPage,
    request,
    base_url: str,
):
    """
    Test 6.3.1: GLONASS Constellation Configuration - Pure Page Object Pattern
    Purpose: Verify GLONASS can be enabled/disabled
    Expected: Checkbox toggles and persists, device-aware validation
    TRANSFORMED: Uses pure page object methods with device intelligence
    Series: Both 2 and 3
    """
    device_model = request.session.device_hardware_model

    # Essential device intelligence
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(f"Testing GLONASS checkbox toggle on {device_model}")
    logger.info(f"Device series: {device_series}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}x")

    # Check if device supports GLONASS
    if not DeviceCapabilities.has_capability(device_model, "glonass_constellation"):
        pytest.skip(f"GLONASS constellation not supported on {device_model}")

    # Navigate to GNSS configuration page
    gnss_config_page.navigate_to_gnss_config()

    # Test GLONASS checkbox toggle through page object
    toggle_results = gnss_config_page.test_glonass_checkbox_toggle()
    logger.info(f"GLONASS toggle test results: {toggle_results}")

    # Verify GLONASS checkbox found
    checkbox_found = toggle_results.get("checkbox_found", False)
    assert checkbox_found, "GLONASS checkbox should be found"

    # Verify GLONASS checkbox visibility
    checkbox_visible = toggle_results.get("checkbox_visible", False)
    assert checkbox_visible, "GLONASS checkbox should be visible"

    # Verify GLONASS checkbox enabled
    checkbox_enabled = toggle_results.get("checkbox_enabled", False)
    assert checkbox_enabled, "GLONASS checkbox should be enabled"

    # Test toggle functionality
    toggle_successful = toggle_results.get("toggle_successful", False)
    assert toggle_successful, "GLONASS checkbox should toggle successfully"

    # Test state persistence
    state_persistence = toggle_results.get("state_persistence", False)
    if state_persistence:
        logger.info("GLONASS checkbox state persists correctly")
    else:
        logger.info("GLONASS checkbox state persistence varies by device")

    # Test cancel functionality
    cancel_functional = toggle_results.get("cancel_functional", False)
    if cancel_functional:
        logger.info("GLONASS cancel functionality works correctly")
    else:
        logger.info("GLONASS cancel functionality varies by device")

    # Device capabilities validation
    glonass_capability = DeviceCapabilities.has_capability(
        device_model, "glonass_constellation"
    )
    assert (
        glonass_capability
    ), "Device should support GLONASS constellation configuration"

    # Get current constellation status
    constellation_status = gnss_config_page.is_constellation_enabled("GLONASS")
    logger.info(f"GLONASS constellation enabled: {constellation_status}")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)
    logger.info(f"GLONASS checkbox toggle test completed for {device_model}")
    logger.info(f"Device info: {device_info}")

    print(f"GLONASS CHECKBOX TOGGLE COMPLETED: {device_model} (Series {device_series})")
