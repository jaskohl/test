"""
Category 4: Network Configuration - Test 4.5.1
DNS Server Configuration - Pure Page Object Pattern
Test Count: 5 of 8 in Category 4
Hardware: Device Only
Priority: HIGH - DNS configuration foundation
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with device intelligence
PATTERN: Zero direct .locator() calls, essential methods only
"""

import pytest
import logging
from pages.network_config_page import NetworkConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_4_5_1_dns_server_configuration(
    network_config_page: NetworkConfigPage,
    request,
    base_url: str,
):
    """
    Test 4.5.1: DNS Server Configuration - Pure Page Object Pattern
    Purpose: Verify DNS server configuration with device-aware patterns
    Expected: DNS server configuration works correctly with device-specific patterns
    TRANSFORMED: Uses pure page object methods with device intelligence
    """
    device_model = request.session.device_hardware_model

    # Essential device intelligence
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(f"Testing DNS server configuration on {device_model}")

    # Navigate to network configuration page
    network_config_page.navigate_to_network_config()

    # Test DNS server field discovery and validation through page object
    dns_discovery = network_config_page.discover_dns_fields()
    logger.info(f"DNS field discovery: {dns_discovery}")

    # Test device series-specific DNS configuration patterns
    if device_series == 2:
        # Series 2 devices have simpler DNS configuration
        series2_results = network_config_page.test_series2_dns_patterns()
        logger.info(f"Series 2 DNS patterns: {series2_results}")
    elif device_series == 3:
        # Series 3 devices may have more complex DNS configuration
        series3_results = network_config_page.test_series3_dns_patterns()
        logger.info(f"Series 3 DNS patterns: {series3_results}")

    # Cross-validate DNS patterns with DeviceCapabilities
    dns_patterns = network_config_page.validate_dns_patterns_with_device_capabilities()
    logger.info(f"DNS pattern validation: {dns_patterns}")

    # Test DNS save button behavior through page object
    save_behavior = network_config_page.test_dns_save_button_behavior()
    logger.info(f"DNS save button behavior: {save_behavior}")

    # Performance validation for DNS configuration through page object
    performance_results = network_config_page.test_dns_configuration_performance()
    logger.info(f"DNS configuration performance: {performance_results}")

    # Final comprehensive validation through page object
    validation_summary = network_config_page.validate_dns_configuration()
    logger.info(f"DNS validation summary: {validation_summary}")

    logger.info(f"DNS Server Configuration Test PASSED for {device_model}")
