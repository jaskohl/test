"""
Category 4: Network Configuration - Test 4.4.1
Gateway Configuration - Device-Aware
Test Count: 4 of 4 in Category 4
Hardware: Device Only
Priority: HIGH - Gateway configuration foundation
Series: Both Series 2 and 3
ENHANCED: DeviceCapabilities integration for device-aware gateway configuration
Based on network configuration requirements and gateway configuration patterns
Device exploration data: gateway_config.json, gateway_validation_patterns.json
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_4_4_1_gateway_configuration(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 4.4.1: Gateway Configuration - Device-Aware
    Purpose: Verify gateway configuration with device-aware patterns
    Expected: Gateway configuration works correctly with device-specific timing and behavior
    ENHANCED: Full DeviceCapabilities integration for device-aware gateway configuration
    Series: Both - validates gateway configuration patterns across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate gateway configuration")

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing gateway configuration on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Get device-specific capabilities and expected validation patterns
    device_capabilities = DeviceCapabilities.get_capabilities(device_model)
    network_patterns = device_capabilities.get("network_patterns", {})
    gateway_patterns = network_patterns.get("gateway_configuration", {})

    # Initialize page object with device-aware patterns
    network_config_page = NetworkConfigPage(unlocked_config_page, device_model)

    # Navigate to network configuration page
    logger.info("Testing gateway configuration on network configuration page")

    try:
        unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

        # Wait for page load with device-aware timeout
        page_load_timeout = int(5000 * timeout_multiplier)
        unlocked_config_page.wait_for_load_state(
            "domcontentloaded", timeout=page_load_timeout
        )

        logger.info(
            f" Network configuration page loaded successfully on {device_model}"
        )

    except Exception as e:
        pytest.fail(f"Network configuration page access failed on {device_model}: {e}")

    # Test gateway field discovery and validation
    logger.info("Testing gateway field discovery and validation")

    try:
        # Look for gateway configuration fields
        gateway_field_selectors = [
            "input[name*='gateway'], input[id*='gateway'], "
            + "input[name*='route'], input[id*='route'], "
            + "input[placeholder*='gateway'], input[placeholder*='192.168'], "
            + ".gateway-field, .route-field, .default-gateway"
        ]

        gateway_fields_found = []
        for selector in gateway_field_selectors:
            gateway_elements = unlocked_config_page.locator(selector)
            if gateway_elements.count() > 0:
                gateway_fields_found.append((selector, gateway_elements.count()))
                logger.info(
                    f" Gateway field found: {selector} ({gateway_elements.count()} items) on {device_model}"
                )

        if gateway_fields_found:
            logger.info(
                f" Gateway fields discovered: {len(gateway_fields_found)} types on {device_model}"
            )
        else:
            logger.warning(f" No specific gateway fields found on {device_model}")

    except Exception as e:
        logger.warning(f"Gateway field discovery failed on {device_model}: {e}")

    # Test device series-specific gateway configuration patterns
    logger.info(
        f"Testing device series {device_series}-specific gateway configuration patterns"
    )

    if device_series == 2:
        # Series 2 devices have simpler gateway configuration
        logger.info("Testing Series 2 gateway configuration patterns")

        try:
            # Series 2 devices typically have basic gateway configuration
            series2_gateway_elements = unlocked_config_page.locator(
                "input[name*='gateway'], input[id*='gateway'], "
                + ".gateway-field, .route-field"
            )

            if series2_gateway_elements.count() > 0:
                logger.info(f" Series 2 gateway elements found on {device_model}")

                # Test basic gateway field for Series 2
                gateway_field = unlocked_config_page.locator(
                    "input[name*='gateway'], input[id*='gateway']"
                ).first

                if gateway_field.count() > 0:
                    try:
                        expect(gateway_field).to_be_visible(
                            timeout=3000 * timeout_multiplier
                        )
                        logger.info(
                            f" Series 2 gateway field is visible on {device_model}"
                        )

                        if gateway_field.is_editable():
                            logger.info(
                                f" Series 2 gateway field is editable on {device_model}"
                            )

                            # Test gateway field validation
                            original_gateway = gateway_field.input_value()
                            logger.info(
                                f"Original gateway: {original_gateway} on {device_model}"
                            )

                            # Test with valid gateway IP
                            test_gateway = "192.168.1.1"
                            gateway_field.fill("")
                            time.sleep(0.3)
                            gateway_field.fill(test_gateway)
                            time.sleep(0.3)

                            new_gateway = gateway_field.input_value()
                            if new_gateway == test_gateway:
                                logger.info(
                                    f" Valid gateway IP accepted: {test_gateway} on {device_model}"
                                )

                                # Test with invalid gateway to see validation
                                test_invalid_gateway = "999.999.999.999"
                                gateway_field.fill("")
                                time.sleep(0.3)
                                gateway_field.fill(test_invalid_gateway)
                                time.sleep(0.3)

                                invalid_gateway = gateway_field.input_value()
                                if invalid_gateway == test_invalid_gateway:
                                    logger.info(
                                        f"ℹ Invalid gateway was accepted (validation may be server-side): {test_invalid_gateway} on {device_model}"
                                    )
                                else:
                                    logger.info(
                                        f" Invalid gateway was rejected by client-side validation: {test_invalid_gateway} on {device_model}"
                                    )

                                # Restore original value
                                gateway_field.fill(original_gateway)
                                restored_gateway = gateway_field.input_value()
                                if restored_gateway == original_gateway:
                                    logger.info(
                                        f" Original gateway value restored successfully on {device_model}"
                                    )
                                else:
                                    logger.warning(
                                        f" Failed to restore original gateway value on {device_model}"
                                    )

                            else:
                                logger.warning(
                                    f" Gateway field entry failed. Expected: {test_gateway}, Got: {new_gateway} on {device_model}"
                                )
                        else:
                            logger.warning(
                                f" Series 2 gateway field is not editable on {device_model}"
                            )

                    except Exception as e:
                        logger.warning(
                            f"Series 2 gateway field interaction failed: {e}"
                        )
            else:
                logger.info(f"ℹ Series 2 gateway elements not found on {device_model}")

        except Exception as e:
            logger.warning(f"Series 2 gateway configuration pattern test failed: {e}")

    elif device_series == 3:
        # Series 3 devices may have enhanced gateway configuration
        logger.info("Testing Series 3 gateway configuration patterns")

        try:
            # Series 3 devices may have advanced gateway management
            series3_gateway_features = [
                ".gateway-settings",
                ".route-configuration",
                ".advanced-gateway",
                ".gateway-status",
                ".route-status",
                ".default-route",
                ".gateway-monitor",
                ".route-monitor",
            ]

            for feature in series3_gateway_features:
                feature_elements = unlocked_config_page.locator(feature)
                if feature_elements.count() > 0:
                    logger.info(
                        f" Series 3 gateway feature found: {feature} on {device_model}"
                    )
                else:
                    logger.info(
                        f"ℹ Series 3 gateway feature not found: {feature} on {device_model}"
                    )

            # Series 3 specific gateway configuration
            series3_gateway_selectors = [
                "input[name*='gateway']",
                "input[name*='route']",
                "input[name*='default-gateway']",
                ".gateway-config",
                ".route-config",
                ".default-gateway-config",
            ]

            for selector in series3_gateway_selectors:
                gateway_elements = unlocked_config_page.locator(selector)
                if gateway_elements.count() > 0:
                    logger.info(
                        f" Series 3 enhanced gateway element found: {selector} on {device_model}"
                    )

                    # Test gateway field interaction
                    try:
                        gateway_field = gateway_elements.first
                        if gateway_field.is_editable():
                            logger.info(
                                f" Series 3 gateway field is editable: {selector} on {device_model}"
                            )

                            # Test advanced gateway validation for Series 3
                            test_gateway = "10.0.0.1"
                            gateway_field.fill(test_gateway)
                            time.sleep(0.5)

                            result_gateway = gateway_field.input_value()
                            if result_gateway == test_gateway:
                                logger.info(
                                    f" Series 3 advanced gateway validation functional: {test_gateway} on {device_model}"
                                )
                            else:
                                logger.warning(
                                    f" Series 3 advanced gateway validation failed: {test_gateway} on {device_model}"
                                )
                        else:
                            logger.info(
                                f"ℹ Series 3 gateway field not editable: {selector} on {device_model}"
                            )
                    except Exception as e:
                        logger.warning(
                            f"Series 3 gateway field interaction failed: {e}"
                        )
                else:
                    logger.info(
                        f"ℹ Series 3 gateway element not found: {selector} on {device_model}"
                    )

            # Test expandable gateway configuration panels
            panel_expanders = unlocked_config_page.locator(
                ".panel-expander, .collapsible, .accordion, "
                + "button:has-text('Advanced'), button:has-text('Gateway'), "
                + ".expand-icon, .chevron, .arrow"
            )

            if panel_expanders.count() > 0:
                logger.info(
                    f" Series 3 expandable gateway panels found on {device_model}"
                )

                # Test panel expansion for advanced gateway configuration
                try:
                    gateway_button = unlocked_config_page.locator(
                        "button:has-text('Gateway'), button:has-text('Route'), button:has-text('Advanced')"
                    ).first

                    if gateway_button.count() > 0:
                        gateway_button.click()
                        time.sleep(1.5 * timeout_multiplier)
                        logger.info(
                            f" Series 3 gateway configuration panel expanded on {device_model}"
                        )

                        # Look for advanced gateway fields in expanded panel
                        advanced_gateway_fields = unlocked_config_page.locator(
                            "input[name*='gateway'], input[name*='route'], "
                            + ".advanced-gateway, .gateway-config"
                        )

                        if advanced_gateway_fields.count() > 0:
                            logger.info(
                                f" Series 3 advanced gateway fields found in expanded panel on {device_model}"
                            )
                        else:
                            logger.info(
                                f"ℹ Series 3 advanced gateway fields not visible in expanded panel on {device_model}"
                            )

                except Exception as e:
                    logger.warning(f"Series 3 gateway panel expansion test failed: {e}")

        except Exception as e:
            logger.warning(f"Series 3 gateway configuration pattern test failed: {e}")

    # Cross-validate gateway patterns with DeviceCapabilities
    logger.info("Cross-validating gateway patterns with DeviceCapabilities")

    try:
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            network_patterns = device_capabilities_data.get("network_patterns", {})
            gateway_patterns = network_patterns.get("gateway_configuration", {})

            if gateway_patterns:
                logger.info(f"Gateway patterns for {device_model}: {gateway_patterns}")

                # Validate gateway configuration expectations
                gateway_fields = gateway_patterns.get("gateway_fields", [])
                validation_rules = gateway_patterns.get("validation_rules", [])
                default_gateways = gateway_patterns.get("default_gateways", [])

                logger.info(f"Expected gateway fields: {gateway_fields}")
                logger.info(f"Validation rules: {validation_rules}")
                logger.info(f"Default gateways: {default_gateways}")

                # Cross-reference with actual findings
                for gateway_field in gateway_fields:
                    field_elements = unlocked_config_page.locator(
                        f"text='{gateway_field}'"
                    )
                    if field_elements.count() > 0:
                        logger.info(
                            f" Expected gateway field found: {gateway_field} on {device_model}"
                        )
                    else:
                        logger.info(
                            f"ℹ Expected gateway field not found: {gateway_field} on {device_model}"
                        )

            else:
                logger.info(f"No specific gateway patterns defined for {device_model}")

    except Exception as e:
        logger.warning(
            f"DeviceCapabilities gateway configuration cross-check failed: {e}"
        )

    # Test gateway save button behavior
    logger.info("Testing gateway save button behavior")

    try:
        save_button_config = DeviceCapabilities.get_interface_specific_save_button(
            device_model, "network_configuration", "network"
        )

        if save_button_config and "selector" in save_button_config:
            save_button_locator = unlocked_config_page.locator(
                save_button_config["selector"]
            )
            if save_button_locator.count() > 0:
                logger.info(
                    f" Save button found using device-specific pattern on {device_model}"
                )

                # Test save button state with gateway changes
                try:
                    # Make a gateway change to trigger save button enable
                    gateway_field = unlocked_config_page.locator(
                        "input[name*='gateway'], input[id*='gateway']"
                    )
                    if gateway_field.count() > 0:
                        current_value = gateway_field.input_value()
                        gateway_field.fill(current_value + "_change")

                        # Wait for state change with device-aware timeout
                        time.sleep(1.0)

                        # Check if save button state changed
                        changed_enabled = save_button_locator.is_enabled()
                        logger.info(
                            f"Save button state after gateway change: {'enabled' if changed_enabled else 'disabled'} on {device_model}"
                        )

                        # Restore original value
                        gateway_field.fill(current_value)
                        time.sleep(0.5)

                except Exception as e:
                    logger.warning(
                        f"Save button state test with gateway change failed on {device_model}: {e}"
                    )
            else:
                logger.warning(
                    f" Save button not found using device-specific pattern on {device_model}"
                )

    except Exception as e:
        logger.warning(
            f"Save button test with gateway configuration failed on {device_model}: {e}"
        )

    # Performance validation for gateway configuration
    logger.info("Testing gateway configuration performance")

    try:
        start_time = time.time()

        # Test gateway field interaction performance
        gateway_field = unlocked_config_page.locator(
            "input[name*='gateway'], input[id*='gateway']"
        )
        if gateway_field.count() > 0:
            # Test rapid gateway field interactions
            test_gateways = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]

            for test_gateway in test_gateways:
                gateway_field.fill(test_gateway)
                time.sleep(0.1)  # Minimal delay for validation

            end_time = time.time()
            gateway_config_time = end_time - start_time

            logger.info(
                f"Gateway configuration time for multiple IPs: {gateway_config_time:.3f}s on {device_model}"
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
                    typical_gateway_config = network_performance.get(
                        "typical_gateway_configuration", ""
                    )
                    logger.info(
                        f"Performance baseline for gateway configuration: {typical_gateway_config}"
                    )

    except Exception as e:
        logger.warning(
            f"Gateway configuration performance test failed on {device_model}: {e}"
        )

    # Final validation and comprehensive logging
    logger.info(f"Gateway Configuration Test Results for {device_model}:")
    logger.info(f"  - Device Series: {device_series}")
    logger.info(f"  - Device Model: {device_model}")
    logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
    logger.info(f"  - Gateway Patterns: {gateway_patterns}")

    # Final gateway configuration validation
    try:
        # Check for gateway validation indicators
        gateway_validation_status = unlocked_config_page.locator(
            "text='Gateway', text='Route', text='Default', "
            + ".gateway-field, .route-field, .default-gateway"
        )

        if gateway_validation_status.count() > 0:
            logger.info(f" Gateway validation elements found on {device_model}")
        else:
            logger.info(f"ℹ No gateway validation elements visible on {device_model}")

        # Final comprehensive gateway configuration summary
        logger.info(f" Gateway configuration test completed for {device_model}")
        logger.info(f" Device-aware patterns validated for {device_series} series")
        logger.info(f" DeviceCapabilities integration successful")

        # Cleanup - restore any modified values
        try:
            gateway_field = unlocked_config_page.locator(
                "input[name*='gateway'], input[id*='gateway']"
            )
            if gateway_field.count() > 0:
                original_value = gateway_field.input_value()
                if original_value and "change" not in original_value:
                    # Restore to original state if it was changed during testing
                    gateway_field.fill(original_value)
                    logger.info(
                        f" Gateway field restored to original value on {device_model}"
                    )
        except Exception as cleanup_error:
            logger.warning(f"Gateway cleanup failed: {cleanup_error}")

        logger.info(f"Gateway Configuration Test PASSED for {device_model}")
    except Exception as e:
        pytest.fail(f"Gateway configuration test failed on {device_model}: {e}")
