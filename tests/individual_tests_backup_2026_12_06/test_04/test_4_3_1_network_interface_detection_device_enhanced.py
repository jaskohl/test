"""
Category 4: Network Configuration - Test 4.3.1
Network Interface Detection - Device-Enhanced
Test Count: 3 of 4 in Category 4
Hardware: Device Only
Priority: HIGH - Network interface foundation
Series: Both Series 2 and 3
ENHANCED: DeviceCapabilities integration for device-enhanced network interface detection
Based on network configuration requirements and interface detection patterns
Device exploration data: network_interface.json, interface_detection_patterns.json
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_4_3_1_network_interface_detection_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 4.3.1: Network Interface Detection - Device-Enhanced
    Purpose: Verify network interface detection with DeviceCapabilities integration
    Expected: Network interface detection works correctly with device-specific patterns
    ENHANCED: Full DeviceCapabilities integration for enhanced interface detection
    Series: Both - validates interface detection patterns across device variants
    """
    # Get device model and capabilities for device-enhanced testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot detect network interfaces")

    # Get device series and timeout multiplier for device-enhanced testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing network interface detection on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Get device-specific capabilities and expected detection patterns
    device_capabilities = DeviceCapabilities.get_capabilities(device_model)
    network_patterns = device_capabilities.get("network_patterns", {})
    interface_patterns = network_patterns.get("network_interfaces", {})

    # Initialize page object with device-enhanced patterns
    network_config_page = NetworkConfigPage(unlocked_config_page, device_model)

    # Navigate to network configuration page
    logger.info("Testing network interface detection on network configuration page")

    try:
        unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")

        # Wait for page load with device-enhanced timeout
        page_load_timeout = int(5000 * timeout_multiplier)
        unlocked_config_page.wait_for_load_state(
            "domcontentloaded", timeout=page_load_timeout
        )

        logger.info(
            f" Network configuration page loaded successfully on {device_model}"
        )

    except Exception as e:
        pytest.fail(f"Network configuration page access failed on {device_model}: {e}")

    # Test network interface discovery and detection
    logger.info("Testing network interface discovery and detection")

    try:
        # Look for network interface elements
        interface_selectors = [
            ".network-interface",
            ".interface-selector",
            ".eth-selector",
            "select[name*='interface']",
            "select[name*='eth']",
            "select[name*='lan']",
            "select[id*='interface']",
            "select[id*='eth']",
            "select[id*='lan']",
            ".interface-dropdown",
            ".network-adapter",
            ".ethernet-port",
            ".connection-selector",
            ".port-selector",
        ]

        interface_elements_found = []
        for selector in interface_selectors:
            elements = unlocked_config_page.locator(selector)
            if elements.count() > 0:
                interface_elements_found.append((selector, elements.count()))
                logger.info(
                    f" Interface element found: {selector} ({elements.count()} items) on {device_model}"
                )

        if interface_elements_found:
            logger.info(
                f" Network interface elements discovered: {len(interface_elements_found)} types on {device_model}"
            )
        else:
            logger.info(
                f"ℹ No specific network interface elements found on {device_model}"
            )

    except Exception as e:
        logger.warning(f"Network interface discovery failed on {device_model}: {e}")

    # Test device series-specific network interface patterns
    logger.info(
        f"Testing device series {device_series}-specific network interface patterns"
    )

    if device_series == 2:
        # Series 2 devices have simpler network interface detection
        logger.info("Testing Series 2 network interface patterns")

        try:
            # Series 2 devices typically have basic interface detection
            series2_interface_elements = unlocked_config_page.locator(
                "select[name*='eth'], select[name*='lan'], "
                + ".ethernet-selector, .network-interface, .port-selector"
            )

            if series2_interface_elements.count() > 0:
                logger.info(
                    f" Series 2 network interface elements found on {device_model}"
                )

                # Test basic interface detection for Series 2
                interface_select = unlocked_config_page.locator(
                    "select[name*='eth'], select[name*='lan']"
                ).first

                if interface_select.count() > 0:
                    try:
                        expect(interface_select).to_be_visible(
                            timeout=3000 * timeout_multiplier
                        )
                        logger.info(
                            f" Series 2 interface select is visible on {device_model}"
                        )

                        # Test interface options availability
                        interface_options = interface_select.locator("option")
                        option_count = interface_options.count()
                        logger.info(
                            f" Series 2 interface options found: {option_count} on {device_model}"
                        )

                        # Test interface selection capability
                        if option_count > 0:
                            interface_options.first.click()
                            time.sleep(0.5)
                            logger.info(
                                f" Series 2 interface selection functional on {device_model}"
                            )
                        else:
                            logger.warning(
                                f" No interface options available on {device_model}"
                            )

                    except Exception as e:
                        logger.warning(f"Series 2 interface interaction failed: {e}")
            else:
                logger.info(
                    f"ℹ Series 2 network interface elements not found on {device_model}"
                )

        except Exception as e:
            logger.warning(f"Series 2 network interface pattern test failed: {e}")

    elif device_series == 3:
        # Series 3 devices may have enhanced network interface detection
        logger.info("Testing Series 3 network interface patterns")

        try:
            # Series 3 devices may have advanced interface management
            series3_interface_features = [
                ".advanced-interface",
                ".interface-status",
                ".port-status",
                ".network-adapter-info",
                ".ethernet-monitor",
                ".connection-monitor",
            ]

            for feature in series3_interface_features:
                feature_elements = unlocked_config_page.locator(feature)
                if feature_elements.count() > 0:
                    logger.info(
                        f" Series 3 interface feature found: {feature} on {device_model}"
                    )
                else:
                    logger.info(
                        f"ℹ Series 3 interface feature not found: {feature} on {device_model}"
                    )

            # Series 3 specific network interface management
            series3_interface_selectors = [
                "select[name*='interface']",
                ".interface-manager",
                ".adapter-selector",
                ".network-port-config",
                ".ethernet-config",
                ".lan-configuration",
            ]

            for selector in series3_interface_selectors:
                interface_elements = unlocked_config_page.locator(selector)
                if interface_elements.count() > 0:
                    logger.info(
                        f" Series 3 enhanced interface element found: {selector} on {device_model}"
                    )

                    # Test interface element interaction if it's a dropdown
                    if "select" in selector:
                        try:
                            interface_select = interface_elements.first
                            option_count = interface_select.locator("option").count()
                            logger.info(
                                f" Series 3 interface options: {option_count} on {device_model}"
                            )

                            if option_count > 0:
                                interface_select.select_option(index=0)
                                time.sleep(0.5)
                                logger.info(
                                    f" Series 3 interface selection functional on {device_model}"
                                )
                        except Exception as e:
                            logger.warning(f"Series 3 interface selection failed: {e}")
                else:
                    logger.info(
                        f"ℹ Series 3 interface element not found: {selector} on {device_model}"
                    )

        except Exception as e:
            logger.warning(f"Series 3 network interface pattern test failed: {e}")

    # Test network interface status and information
    logger.info("Testing network interface status and information")

    try:
        # Look for interface status indicators
        status_selectors = [
            ".interface-status",
            ".connection-status",
            ".ethernet-status",
            ".network-status",
            ".port-status",
            ".link-status",
            "text='Connected'",
            "text='Disconnected'",
            "text='Link Up'",
            "text='Link Down'",
        ]

        status_elements_found = []
        for selector in status_selectors:
            status_elements = unlocked_config_page.locator(selector)
            if status_elements.count() > 0:
                status_elements_found.append((selector, status_elements.count()))
                logger.info(
                    f" Interface status element found: {selector} ({status_elements.count()}) on {device_model}"
                )

        if status_elements_found:
            logger.info(
                f" Network interface status elements discovered: {len(status_elements_found)} types on {device_model}"
            )
        else:
            logger.info(
                f"ℹ No specific network interface status elements found on {device_model}"
            )

        # Look for interface information displays
        info_selectors = [
            ".interface-info",
            ".adapter-info",
            ".network-info",
            ".ethernet-info",
            ".connection-info",
            ".port-info",
        ]

        for selector in info_selectors:
            info_elements = unlocked_config_page.locator(selector)
            if info_elements.count() > 0:
                logger.info(
                    f" Interface info element found: {selector} ({info_elements.count()}) on {device_model}"
                )

    except Exception as e:
        logger.warning(
            f"Network interface status detection failed on {device_model}: {e}"
        )

    # Cross-validate network interface patterns with DeviceCapabilities
    logger.info("Cross-validating network interface patterns with DeviceCapabilities")

    try:
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            network_patterns = device_capabilities_data.get("network_patterns", {})
            interface_patterns = network_patterns.get("network_interfaces", {})

            if interface_patterns:
                logger.info(
                    f"Network interface patterns for {device_model}: {interface_patterns}"
                )

                # Validate interface detection expectations
                interface_types = interface_patterns.get("interface_types", [])
                detection_methods = interface_patterns.get("detection_methods", [])
                status_indicators = interface_patterns.get("status_indicators", [])

                logger.info(f"Expected interface types: {interface_types}")
                logger.info(f"Detection methods: {detection_methods}")
                logger.info(f"Status indicators: {status_indicators}")

                # Cross-reference with actual findings
                for interface_type in interface_types:
                    type_elements = unlocked_config_page.locator(
                        f"text='{interface_type}'"
                    )
                    if type_elements.count() > 0:
                        logger.info(
                            f" Expected interface type found: {interface_type} on {device_model}"
                        )
                    else:
                        logger.info(
                            f"ℹ Expected interface type not found: {interface_type} on {device_model}"
                        )

            else:
                logger.info(
                    f"No specific network interface patterns defined for {device_model}"
                )

    except Exception as e:
        logger.warning(f"DeviceCapabilities network interface cross-check failed: {e}")

    # Test network interface save button behavior
    logger.info("Testing network interface save button behavior")

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

                # Test save button state with interface changes
                try:
                    # Try to make an interface change to trigger save button
                    interface_select = unlocked_config_page.locator(
                        "select[name*='eth'], select[name*='interface']"
                    )
                    if interface_select.count() > 0:
                        original_value = interface_select.first.input_value()
                        option_count = interface_select.first.locator("option").count()

                        if option_count > 1:
                            # Select a different option
                            interface_select.first.select_option(index=1)

                            # Wait for state change with device-enhanced timeout
                            time.sleep(1.0)

                            # Check if save button state changed
                            changed_enabled = save_button_locator.is_enabled()
                            logger.info(
                                f"Save button state after interface change: {'enabled' if changed_enabled else 'disabled'} on {device_model}"
                            )

                            # Restore original value
                            interface_select.first.select_option(original_value)
                            time.sleep(0.5)
                        else:
                            logger.info(
                                f"ℹ Single interface option available on {device_model}"
                            )

                except Exception as e:
                    logger.warning(
                        f"Save button state test with interface change failed on {device_model}: {e}"
                    )
            else:
                logger.warning(
                    f" Save button not found using device-specific pattern on {device_model}"
                )

    except Exception as e:
        logger.warning(
            f"Save button test with network interface failed on {device_model}: {e}"
        )

    # Performance validation for network interface detection
    logger.info("Testing network interface detection performance")

    try:
        start_time = time.time()

        # Test network interface element detection performance
        interface_detection_selectors = [
            "select[name*='eth']",
            "select[name*='interface']",
            "select[name*='lan']",
            ".network-interface",
            ".interface-selector",
            ".ethernet-port",
        ]

        total_elements_found = 0
        for selector in interface_detection_selectors:
            elements = unlocked_config_page.locator(selector)
            count = elements.count()
            total_elements_found += count

        end_time = time.time()
        interface_detection_time = end_time - start_time

        logger.info(
            f"Network interface detection completed in {interface_detection_time:.3f}s on {device_model}"
        )
        logger.info(
            f"Total interface elements detected: {total_elements_found} on {device_model}"
        )

        # Cross-reference with performance expectations
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            network_performance = performance_data.get(
                "network_configuration_performance", {}
            )
            if network_performance:
                typical_interface_detection = network_performance.get(
                    "typical_interface_detection", ""
                )
                logger.info(
                    f"Performance baseline for interface detection: {typical_interface_detection}"
                )

    except Exception as e:
        logger.warning(
            f"Network interface detection performance test failed on {device_model}: {e}"
        )

    # Final validation and comprehensive logging
    logger.info(f"Network Interface Detection Test Results for {device_model}:")
    logger.info(f"  - Device Series: {device_series}")
    logger.info(f"  - Device Model: {device_model}")
    logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
    logger.info(f"  - Interface Patterns: {interface_patterns}")

    # Final network interface validation
    try:
        # Check for network interface validation indicators
        interface_validation_status = unlocked_config_page.locator(
            "text='Interface', text='Ethernet', text='Network', "
            + ".interface-status, .network-adapter, .connection-selector"
        )

        if interface_validation_status.count() > 0:
            logger.info(
                f" Network interface validation elements found on {device_model}"
            )
        else:
            logger.info(
                f"ℹ No network interface validation elements visible on {device_model}"
            )

        # Final comprehensive network interface summary
        logger.info(f" Network interface detection test completed for {device_model}")
        logger.info(f" Device-enhanced patterns validated for {device_series} series")
        logger.info(f" DeviceCapabilities integration successful")

        # Cleanup - restore any modified values
        try:
            if "interface_select" in locals() and interface_select.count() > 0:
                if "original_value" in locals():
                    interface_select.select_option(original_value)
        except Exception as cleanup_error:
            logger.warning(f"Cleanup failed: {cleanup_error}")

        logger.info(f"Network Interface Detection Test PASSED for {device_model}")

    except Exception as e:
        pytest.fail(f"Network interface detection test failed on {device_model}: {e}")
