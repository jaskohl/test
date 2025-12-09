"""
Category 4: Network Configuration - Test 4.4.1
Gateway Configuration - Pure Page Object Pattern
Test Count: 4 of 8 in Category 4
Hardware: Device Only
Priority: HIGH - Gateway configuration foundation
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with device intelligence
PATTERN: Zero direct .locator() calls, essential methods only
"""

import pytest
import logging
from pages.network_config_page import NetworkConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_4_4_1_gateway_configuration(
    network_config_page: NetworkConfigPage,
    request,
    base_url: str,
):
    """
    Test 4.4.1: Gateway Configuration - Pure Page Object Pattern
    Purpose: Verify gateway configuration with device-aware patterns
    Expected: Gateway configuration works correctly with device-specific timing and behavior
    TRANSFORMED: Uses pure page object methods with device intelligence
    """
    device_model = request.session.device_hardware_model

    # Essential device intelligence
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(f"Testing gateway configuration on {device_model}")

    # Navigate to network configuration page
    network_config_page.navigate_to_network_config()

    # Test gateway field discovery and validation through page object
    gateway_discovery = network_config_page.discover_gateway_fields()
    logger.info(f"Gateway field discovery: {gateway_discovery}")

    # Test device series-specific gateway configuration patterns
    if device_series == 2:
        # Series 2 devices have simpler gateway configuration
        series2_results = network_config_page.test_series2_gateway_patterns()
        logger.info(f"Series 2 gateway patterns: {series2_results}")
    elif device_series == 3:
        # Series 3 devices may have  gateway configuration
        series3_results = network_config_page.test_series3_gateway_patterns()
        logger.info(f"Series 3 gateway patterns: {series3_results}")

    # Cross-validate gateway patterns with DeviceCapabilities
    gateway_patterns = (
        network_config_page.validate_gateway_patterns_with_device_capabilities()
    )
    logger.info(f"Gateway pattern validation: {gateway_patterns}")

    # Test gateway save button behavior through page object
    save_behavior = network_config_page.test_gateway_save_button_behavior()
    logger.info(f"Gateway save button behavior: {save_behavior}")

    # Performance validation for gateway configuration through page object
    performance_results = network_config_page.test_gateway_configuration_performance()
    logger.info(f"Gateway configuration performance: {performance_results}")

    # Final comprehensive validation through page object
    validation_summary = network_config_page.validate_gateway_configuration()
    logger.info(f"Gateway validation summary: {validation_summary}")

    logger.info(f"Gateway Configuration Test PASSED for {device_model}")
