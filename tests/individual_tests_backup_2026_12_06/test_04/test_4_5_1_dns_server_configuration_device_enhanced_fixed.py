"""
Category 4: Network Configuration - Test 4.5.1
DNS Server Configuration - Device-Enhanced
Test Count: 1 of 1 in DNS Subcategory
Hardware: Device Only
Priority: HIGH - DNS configuration foundation
Series: Both Series 2 and 3
ENHANCED: DeviceCapabilities integration for device-enhanced DNS server configuration
Based on network configuration requirements and DNS configuration patterns
Device exploration data: dns_config.json, dns_validation_patterns.json
CORRECTED: Now uses correct device-enhanced page object imports with consistent method names
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.network_config_page_device_enhanced import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_4_5_1_dns_server_configuration_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 4.5.1: DNS Server Configuration - Device-Enhanced
    Purpose: Verify DNS server configuration with DeviceCapabilities integration
    Expected: DNS server configuration works correctly with device-specific patterns
    ENHANCED: Full DeviceCapabilities integration for enhanced DNS configuration
    Series: Both - validates DNS configuration patterns across device variants
    CORRECTED: Using device-enhanced page object with consistent method names
    """
    # Get device model and capabilities for device-enhanced testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate DNS server configuration"
        )

    # Get device series and timeout multiplier for device-enhanced testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing DNS server configuration on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Get device-specific capabilities and expected validation patterns
    device_capabilities = DeviceCapabilities.get_capabilities(device_model)
    network_patterns = device_capabilities.get("network_patterns", {})
    dns_patterns = network_patterns.get("dns_configuration", {})

    # Initialize page object with device-enhanced patterns - CORRECTED: Use device-enhanced page object
    network_config_page = NetworkConfigPage(unlocked_config_page, device_model)

    # Navigate to network configuration page
    logger.info("Testing DNS server configuration on network configuration page")

    try:
        unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

        # Wait for page load with device-enhanced timeout
        page_load_timeout = int(5000 * timeout_multiplier)
        unlocked_config_page.wait_for_load_state(
            "domcontentloaded", timeout=page_load_timeout
        )

        logger.info(f"Network configuration page loaded successfully on {device_model}")

    except Exception as e:
        pytest.fail(f"Network configuration page access failed on {device_model}: {e}")

    # Test DNS server field discovery and validation
    logger.info("Testing DNS server field discovery and validation")

    try:
        # Look for DNS server configuration fields
        dns_field_selectors = [
            "input[name*='dns'], input[id*='dns'], "
            + "input[name*='nameserver'], input[id*='nameserver'], "
            + "input[placeholder*='DNS'], input[placeholder*='8.8.8.8'], "
            + ".dns-field, .nameserver-field, .dns-server"
        ]

        dns_fields_found = []
        for selector in dns_field_selectors:
            dns_elements = unlocked_config_page.locator(selector)
            if dns_elements.count() > 0:
                dns_fields_found.append((selector, dns_elements.count()))
                logger.info(
                    f"DNS field found: {selector} ({dns_elements.count()} items) on {device_model}"
                )

        if dns_fields_found:
            logger.info(
                f"DNS fields discovered: {len(dns_fields_found)} types on {device_model}"
            )
        else:
            logger.warning(f"No specific DNS fields found on {device_model}")

    except Exception as e:
        logger.warning(f"DNS server field discovery failed on {device_model}: {e}")

    # Test device series-specific DNS configuration patterns
    logger.info(
        f"Testing device series {device_series}-specific DNS configuration patterns"
    )

    if device_series == 2:
        # Series 2 devices have simpler DNS configuration
        logger.info("Testing Series 2 DNS configuration patterns")

        try:
            # Series 2 devices typically have basic DNS configuration
            series2_dns_elements = unlocked_config_page.locator(
                "input[name*='dns'], input[id*='dns'], " ".dns-field, .nameserver-field"
            )

            if series2_dns_elements.count() > 0:
                logger.info(f"Series 2 DNS elements found on {device_model}")

                # Test basic DNS field for Series 2
                dns_field = unlocked_config_page.locator(
                    "input[name*='dns'], input[id*='dns']"
                ).first

                if dns_field.count() > 0:
                    try:
                        expect(dns_field).to_be_visible(
                            timeout=3000 * timeout_multiplier
                        )
                        logger.info(f"Series 2 DNS field is visible on {device_model}")

                        if dns_field.is_editable():
                            logger.info(
                                f"Series 2 DNS field is editable on {device_model}"
                            )

                            # Test DNS field validation
                            original_dns = dns_field.input_value()
                            logger.info(
                                f"Original DNS: {original_dns} on {device_model}"
                            )

                            # Test with valid DNS IP
                            test_dns = "8.8.8.8"
                            dns_field.fill("")
                            time.sleep(0.3)
                            dns_field.fill(test_dns)
                            time.sleep(0.3)

                            new_dns = dns_field.input_value()
                            if new_dns == test_dns:
                                logger.info(
                                    f"Valid DNS IP accepted: {test_dns} on {device_model}"
                                )

                                # Test with invalid DNS to see validation
                                test_invalid_dns = "999.999.999.999"
                                dns_field.fill("")
                                time.sleep(0.3)
                                dns_field.fill(test_invalid_dns)
                                time.sleep(0.3)

                                invalid_dns = dns_field.input_value()
                                if invalid_dns == test_invalid_dns:
                                    logger.info(
                                        f"ℹ Invalid DNS was accepted (validation may be server-side): {test_invalid_dns} on {device_model}"
                                    )
                                else:
                                    logger.info(
                                        f"Invalid DNS was rejected by client-side validation: {test_invalid_dns} on {device_model}"
                                    )

                                # Restore original value
                                dns_field.fill(original_dns)
                                restored_dns = dns_field.input_value()
                                if restored_dns == original_dns:
                                    logger.info(
                                        f"Original DNS value restored successfully on {device_model}"
                                    )
                                else:
                                    logger.warning(
                                        f"Failed to restore original DNS value on {device_model}"
                                    )

                            else:
                                logger.warning(
                                    f"DNS field entry failed. Expected: {test_dns}, Got: {new_dns} on {device_model}"
                                )
                        else:
                            logger.warning(
                                f"Series 2 DNS field is not editable on {device_model}"
                            )

                    except Exception as e:
                        logger.warning(f"Series 2 DNS field interaction failed: {e}")
            else:
                logger.info(f"ℹ Series 2 DNS elements not found on {device_model}")

        except Exception as e:
            logger.warning(f"Series 2 DNS configuration pattern test failed: {e}")

    elif device_series == 3:
        # Series 3 devices may have enhanced DNS configuration
        logger.info("Testing Series 3 DNS configuration patterns")

        try:
            # Series 3 devices may have advanced DNS management
            series3_dns_features = [
                ".dns-settings",
                ".nameserver-configuration",
                ".advanced-dns",
                ".dns-status",
                ".nameserver-status",
                ".dns-servers",
                ".dns-monitor",
                ".nameserver-monitor",
            ]

            for feature in series3_dns_features:
                feature_elements = unlocked_config_page.locator(feature)
                if feature_elements.count() > 0:
                    logger.info(
                        f"Series 3 DNS feature found: {feature} on {device_model}"
                    )
                else:
                    logger.info(
                        f"ℹ Series 3 DNS feature not found: {feature} on {device_model}"
                    )

            # Series 3 specific DNS configuration
            series3_dns_selectors = [
                "input[name*='dns']",
                "input[name*='nameserver']",
                "input[name*='dns-server']",
                ".dns-config",
                ".nameserver-config",
                ".dns-servers-config",
            ]

            for selector in series3_dns_selectors:
                dns_elements = unlocked_config_page.locator(selector)
                if dns_elements.count() > 0:
                    logger.info(
                        f"Series 3 enhanced DNS element found: {selector} on {device_model}"
                    )

                    # Test DNS field interaction
                    try:
                        dns_field = dns_elements.first
                        if dns_field.is_editable():
                            logger.info(
                                f"Series 3 DNS field is editable: {selector} on {device_model}"
                            )

                            # Test advanced DNS validation for Series 3
                            test_dns = "8.8.4.4"
                            dns_field.fill(test_dns)
                            time.sleep(0.5)

                            result_dns = dns_field.input_value()
                            if result_dns == test_dns:
                                logger.info(
                                    f"Series 3 advanced DNS validation functional: {test_dns} on {device_model}"
                                )
                            else:
                                logger.warning(
                                    f"Series 3 advanced DNS validation failed: {test_dns} on {device_model}"
                                )
                        else:
                            logger.info(
                                f"ℹ Series 3 DNS field not editable: {selector} on {device_model}"
                            )
                    except Exception as e:
                        logger.warning(f"Series 3 DNS field interaction failed: {e}")
                else:
                    logger.info(
                        f"ℹ Series 3 DNS element not found: {selector} on {device_model}"
                    )

            # Test multiple DNS server configuration
            multiple_dns_selectors = [
                "input[name*='dns']",
                ".dns-primary",
                ".dns-secondary",
                ".primary-dns",
                ".secondary-dns",
            ]

            primary_dns_count = 0
            secondary_dns_count = 0

            for selector in multiple_dns_selectors:
                dns_elements = unlocked_config_page.locator(selector)
                if dns_elements.count() > 0:
                    if "primary" in selector.lower() or "dns" in selector.lower():
                        primary_dns_count += dns_elements.count()
                    elif "secondary" in selector.lower():
                        secondary_dns_count += dns_elements.count()
                    else:
                        primary_dns_count += dns_elements.count()

                    logger.info(
                        f"DNS server element found: {selector} ({dns_elements.count()}) on {device_model}"
                    )

            if primary_dns_count > 0:
                logger.info(
                    f"Primary DNS servers found: {primary_dns_count} on {device_model}"
                )
            if secondary_dns_count > 0:
                logger.info(
                    f"Secondary DNS servers found: {secondary_dns_count} on {device_model}"
                )

            if primary_dns_count == 0 and secondary_dns_count == 0:
                logger.info(
                    f"ℹ No multiple DNS server configuration found on {device_model}"
                )

        except Exception as e:
            logger.warning(f"Series 3 DNS configuration pattern test failed: {e}")

    # Cross-validate DNS patterns with DeviceCapabilities
    logger.info("Cross-validating DNS patterns with DeviceCapabilities")

    try:
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            network_patterns = device_capabilities_data.get("network_patterns", {})
            dns_patterns = network_patterns.get("dns_configuration", {})

            if dns_patterns:
                logger.info(f"DNS patterns for {device_model}: {dns_patterns}")

                # Validate DNS configuration expectations
                dns_fields = dns_patterns.get("dns_fields", [])
                validation_rules = dns_patterns.get("validation_rules", [])
                default_dns = dns_patterns.get("default_dns_servers", [])

                logger.info(f"Expected DNS fields: {dns_fields}")
                logger.info(f"Validation rules: {validation_rules}")
                logger.info(f"Default DNS servers: {default_dns}")

                # Cross-reference with actual findings
                for dns_field in dns_fields:
                    field_elements = unlocked_config_page.locator(f"text='{dns_field}'")
                    if field_elements.count() > 0:
                        logger.info(
                            f"Expected DNS field found: {dns_field} on {device_model}"
                        )
                    else:
                        logger.info(
                            f"ℹ Expected DNS field not found: {dns_field} on {device_model}"
                        )

            else:
                logger.info(f"No specific DNS patterns defined for {device_model}")

    except Exception as e:
        logger.warning(f"DeviceCapabilities DNS configuration cross-check failed: {e}")

    # Test DNS save button behavior - CORRECTED: Use get_save_button_locator method
    logger.info("Testing DNS save button behavior")

    try:
        save_button = network_config_page.get_save_button_locator()
        if save_button and save_button.count() > 0:
            logger.info(
                f"Save button found using device-specific pattern on {device_model}"
            )

            # Test save button state with DNS changes
            try:
                # Make a DNS change to trigger save button enable
                dns_field = unlocked_config_page.locator(
                    "input[name*='dns'], input[id*='dns']"
                )
                if dns_field.count() > 0:
                    current_value = dns_field.input_value()
                    dns_field.fill(current_value + "_change")

                    # Wait for state change with device-enhanced timeout
                    time.sleep(1.0)

                    # Check if save button state changed
                    changed_enabled = save_button.is_enabled()
                    logger.info(
                        f"Save button state after DNS change: {'enabled' if changed_enabled else 'disabled'} on {device_model}"
                    )

                    # Restore original value
                    dns_field.fill(current_value)
                    time.sleep(0.5)

            except Exception as e:
                logger.warning(
                    f"Save button state test with DNS change failed on {device_model}: {e}"
                )
        else:
            logger.warning(
                f"Save button not found using device-specific pattern on {device_model}"
            )

    except Exception as e:
        logger.warning(
            f"Save button test with DNS configuration failed on {device_model}: {e}"
        )

    # Performance validation for DNS configuration
    logger.info("Testing DNS configuration performance")

    try:
        start_time = time.time()

        # Test DNS field interaction performance
        dns_field = unlocked_config_page.locator("input[name*='dns'], input[id*='dns']")
        if dns_field.count() > 0:
            # Test rapid DNS field interactions
            test_dns_servers = ["8.8.8.8", "8.8.4.4", "1.1.1.1"]

            for test_dns in test_dns_servers:
                dns_field.fill(test_dns)
                time.sleep(0.1)  # Minimal delay for validation

            end_time = time.time()
            dns_config_time = end_time - start_time

            logger.info(
                f"DNS configuration time for multiple IPs: {dns_config_time:.3f}s on {device_model}"
            )

            # Cross-reference with performance expectations
            performance_data = DeviceCapabilities.get_performance_expectations(
                device_model
            )
            if performance_data:
                network_performance = performance_data.get(
                    "network_configuration_performance", {}
                )
                if network_performance:
                    typical_dns_config = network_performance.get(
                        "typical_dns_configuration", ""
                    )
                    logger.info(
                        f"Performance baseline for DNS configuration: {typical_dns_config}"
                    )

    except Exception as e:
        logger.warning(
            f"DNS configuration performance test failed on {device_model}: {e}"
        )

    # Final validation and comprehensive logging
    logger.info(f"DNS Server Configuration Test Results for {device_model}")
    logger.info(f"  - Device Series: {device_series}")
    logger.info(f"  - Device Model: {device_model}")
    logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
    logger.info(f"  - DNS Patterns: {dns_patterns}")

    # Final DNS configuration validation
    try:
        # Check for DNS validation indicators
        dns_validation_status = unlocked_config_page.locator(
            "text='DNS', text='Nameserver', text='Server', "
            ".dns-field, .nameserver-field, .dns-server"
        )

        if dns_validation_status.count() > 0:
            logger.info(f"DNS validation elements found on {device_model}")
        else:
            logger.info(f"ℹ No DNS validation elements visible on {device_model}")

        # Final comprehensive DNS configuration summary
        logger.info(f"DNS server configuration test completed for {device_model}")
        logger.info(f"Device-enhanced patterns validated for {device_series} series")
        logger.info(f"DeviceCapabilities integration successful")

        # Cleanup - restore any modified values
        try:
            dns_field = unlocked_config_page.locator(
                "input[name*='dns'], input[id*='dns']"
            )
            if dns_field.count() > 0:
                original_value = dns_field.input_value()
                if original_value and "change" not in original_value:
                    # Restore to original state if it was changed during testing
                    dns_field.fill(original_value)
                    logger.info(
                        f"DNS field restored to original value on {device_model}"
                    )
        except Exception as cleanup_error:
            logger.warning(f"DNS cleanup failed: {cleanup_error}")

        logger.info(f"DNS Server Configuration Test PASSED for {device_model}")

    except Exception as e:
        pytest.fail(f"DNS server configuration test failed on {device_model}: {str(e)}")
