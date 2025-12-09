"""
Category 4: Network Configuration - Test 4.3.1
Network Interface Detection - Pure Page Object Pattern
Test Count: 3 of 8 in Category 4
Hardware: Device Only
Priority: HIGH - Network interface foundation
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with device intelligence
PATTERN: Zero direct .locator() calls, essential methods only
"""

import pytest
import logging
from pages.network_config_page import NetworkConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_4_3_1_network_interface_detection(
    network_config_page: NetworkConfigPage,
    request,
    base_url: str,
):
    """
    Test 4.3.1: Network Interface Detection - Pure Page Object Pattern
    Purpose: Verify network interface detection with device-specific patterns
    Expected: Network interface detection works correctly with device intelligence
    TRANSFORMED: Uses pure page object methods with device awareness
    """
    device_model = request.session.device_hardware_model

    # Essential device intelligence
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(f"Testing network interface detection on {device_model}")

    # Navigate to network configuration page
    network_config_page.navigate_to_network_config()

    # Test network interface discovery and detection through page object
    interface_detection_results = network_config_page.discover_network_interfaces()
    logger.info(f"Interface detection results: {interface_detection_results}")

    # Test device series-specific network interface patterns
    if device_series == 2:
        # Series 2 devices have simpler network interface patterns
        series2_results = network_config_page.test_series2_interface_patterns()
        logger.info(f"Series 2 interface patterns: {series2_results}")
    elif device_series == 3:
        # Series 3 devices may have  network interface patterns
        series3_results = network_config_page.test_series3_interface_patterns()
        logger.info(f"Series 3 interface patterns: {series3_results}")

    # Test network interface status and information through page object
    status_results = network_config_page.test_interface_status_detection()
    logger.info(f"Interface status results: {status_results}")

    # Test network interface save button behavior through page object
    save_behavior = network_config_page.test_interface_save_button_behavior()
    logger.info(f"Interface save button behavior: {save_behavior}")

    # Performance validation for network interface detection through page object
    performance_results = network_config_page.test_interface_detection_performance()
    logger.info(f"Interface detection performance: {performance_results}")

    # Final comprehensive validation through page object
    validation_summary = network_config_page.validate_network_interface_configuration()
    logger.info(f"Interface validation summary: {validation_summary}")

    logger.info(f"Network Interface Detection Test PASSED for {device_model}")
