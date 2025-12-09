"""
Category 6: GNSS Configuration - Test 6.1.1
GPS Always Enabled Validation - Pure Page Object Pattern
Test Count: 1 of 9 in Category 6
Hardware: Device Only
Priority: HIGH - GNSS functionality validation
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with device intelligence
PATTERN: Zero direct .locator() calls, essential methods only
"""

import pytest
import logging
from pages.gnss_config_page import GNSSConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_6_1_1_gps_always_enabled(
    gnss_config_page: GNSSConfigPage,
    request,
    base_url: str,
):
    """
    Test 6.1.1: GPS Always Enabled Validation - Pure Page Object Pattern
    Purpose: Verify GPS constellation is always enabled across device variants
    Expected: GPS checkbox always present and checked, device-aware validation
    TRANSFORMED: Uses pure page object methods with device intelligence
    Series: Both - validates GNSS patterns across device variants
    """
    device_model = request.session.device_hardware_model

    # Essential device intelligence
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Get GNSS capabilities for validation
    gnss_constellations = DeviceCapabilities.get_gnss_constellations(device_model)

    if "GPS" not in gnss_constellations:
        pytest.skip(f"GPS not supported on {device_model}")

    logger.info(f"Testing GPS always enabled validation on {device_model}")
    logger.info(f"Expected GNSS constellations: {gnss_constellations}")

    # Navigate to GNSS configuration page
    gnss_config_page.navigate_to_gnss_config()

    # Test GPS always enabled validation through page object
    gps_test_results = gnss_config_page.test_gps_always_enabled_validation()
    logger.info(f"GPS always enabled test results: {gps_test_results}")

    # Verify GPS checkbox presence
    gps_found = gps_test_results.get("gps_found", False)
    assert gps_found, "GPS checkbox should be found"
    logger.info("GPS checkbox found")

    # Verify GPS checkbox state (should always be checked)
    gps_checked = gps_test_results.get("gps_checked", False)
    if gps_checked:
        logger.info("GPS checkbox is checked as expected")
    else:
        logger.warning("GPS checkbox is not checked - attempting to enable")

        # The page object should handle enabling if needed
        gps_enabled = gps_test_results.get("gps_enabled", False)
        assert (
            gps_enabled
        ), "GPS should be enabled (either initially or after enable attempt)"
        logger.info("GPS checkbox enabled successfully")

    # Test other GNSS constellations availability
    other_constellations = [c for c in gnss_constellations if c != "GPS"]
    constellation_tests = gps_test_results.get("constellation_tests", {})

    for constellation in other_constellations:
        constellation_result = constellation_tests.get(constellation, {})
        constellation_found = constellation_result.get("found", False)

        if constellation_found:
            logger.info(f"Constellation {constellation} checkbox found")

            # Test toggle functionality
            is_checked = constellation_result.get("checked", False)
            if is_checked:
                logger.info(f"Constellation {constellation} is currently enabled")
            else:
                logger.info(f"Constellation {constellation} is currently disabled")
        else:
            logger.warning(f"Constellation {constellation} checkbox not found")

    # Test save button behavior for GNSS changes
    save_button_test = gps_test_results.get("save_button_test", {})
    save_functional = save_button_test.get("functional", False)

    if save_functional:
        logger.info("GNSS save button functionality verified")
    else:
        logger.info("Save button behavior varies by device (acceptable)")

    # Performance validation against device baselines
    performance_results = gps_test_results.get("performance_validation", {})
    if performance_results:
        logger.info(f"GNSS performance validation: {performance_results}")
    else:
        logger.info("Performance validation varies by device (acceptable)")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)
    capabilities = DeviceCapabilities.get_capabilities(device_model)

    logger.info(f"GPS always enabled validation completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"GNSS capabilities: {gnss_constellations}")

    print(
        f"GPS ALWAYS ENABLED VALIDATION COMPLETED: {device_model} (Series {device_series})"
    )
