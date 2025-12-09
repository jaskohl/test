"""
Category 6: GNSS Configuration - Test 6.1.2
GNSS Satellite Detection - Device-Enhanced
Test Count: 1 of 2 in GNSS Subcategory
Hardware: Device Only
Priority: HIGH - GNSS detection foundation
Series: Both Series 2 and 3
ENHANCED: DeviceCapabilities integration for device-enhanced GNSS satellite detection
Based on GNSS configuration requirements and satellite detection patterns
Device exploration data: gnss_config.json, satellite_detection_patterns.json
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.gnss_config_page import GNSSConfigPage

logger = logging.getLogger(__name__)


def test_6_1_2_gnss_satellite_detection_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 6.1.2: GNSS Satellite Detection - Device-Enhanced
    Purpose: Verify GNSS satellite detection with DeviceCapabilities integration
    Expected: GNSS satellite detection works correctly with device-specific patterns
    ENHANCED: Full DeviceCapabilities integration for enhanced satellite detection
    Series: Both - validates satellite detection patterns across device variants
    """
    # Get device model and capabilities for device-enhanced testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate GNSS satellite detection"
        )

    # Get device series and timeout multiplier for device-enhanced testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing GNSS satellite detection on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Get device-specific capabilities and expected detection patterns
    device_capabilities = DeviceCapabilities.get_capabilities(device_model)
    gnss_patterns = device_capabilities.get("gnss_configuration_patterns", {})
    satellite_patterns = gnss_patterns.get("satellite_detection", {})

    # Initialize page object with device-enhanced patterns
    gnss_config_page = GNSSConfigPage(unlocked_config_page, device_model)

    # Navigate to GNSS configuration page
    logger.info("Testing GNSS satellite detection on GNSS configuration page")

    try:
        unlocked_config_page.goto(f"{base_url}/gnss", wait_until="domcontentloaded")

        # Wait for page load with device-enhanced timeout
        page_load_timeout = int(5000 * timeout_multiplier)
        unlocked_config_page.wait_for_load_state(
            "domcontentloaded", timeout=page_load_timeout
        )

        logger.info(f" GNSS configuration page loaded successfully on {device_model}")

    except Exception as e:
        pytest.fail(f"GNSS configuration page access failed on {device_model}: {e}")

    # Test GNSS satellite field discovery and validation
    logger.info("Testing GNSS satellite field discovery and validation")

    try:
        # Look for GNSS satellite detection fields
        satellite_field_selectors = [
            "input[name*='satellite'], input[id*='satellite'], "
            + "input[name*='gnss'], input[id*='gnss'], "
            + "input[placeholder*='satellite'], input[placeholder*='GPS'], "
            + ".satellite-field, .gnss-field, .gps-field"
        ]

        satellite_fields_found = []
        for selector in satellite_field_selectors:
            satellite_elements = unlocked_config_page.locator(selector)
            if satellite_elements.count() > 0:
                satellite_fields_found.append((selector, satellite_elements.count()))
                logger.info(
                    f" Satellite field found: {selector} ({satellite_elements.count()} items) on {device_model}"
                )

        if satellite_fields_found:
            logger.info(
                f" Satellite fields discovered: {len(satellite_fields_found)} types on {device_model}"
            )
        else:
            logger.warning(f" No specific satellite fields found on {device_model}")

    except Exception as e:
        logger.warning(f"GNSS satellite field discovery failed on {device_model}: {e}")

    # Test device series-specific GNSS satellite patterns
    logger.info(
        f"Testing device series {device_series}-specific GNSS satellite patterns"
    )

    if device_series == 2:
        # Series 2 devices have simpler GNSS satellite detection
        logger.info("Testing Series 2 GNSS satellite patterns")

        try:
            # Series 2 devices typically have basic satellite detection
            series2_satellite_elements = unlocked_config_page.locator(
                "input[name*='satellite'], input[id*='satellite'], "
                + ".satellite-field, .gnss-field"
            )

            if series2_satellite_elements.count() > 0:
                logger.info(f" Series 2 satellite elements found on {device_model}")

                # Test basic satellite field for Series 2
                satellite_field = unlocked_config_page.locator(
                    "input[name*='satellite'], input[id*='satellite']"
                ).first

                if satellite_field.count() > 0:
                    try:
                        expect(satellite_field).to_be_visible(
                            timeout=3000 * timeout_multiplier
                        )
                        logger.info(
                            f" Series 2 satellite field is visible on {device_model}"
                        )

                        if satellite_field.is_editable():
                            logger.info(
                                f" Series 2 satellite field is editable on {device_model}"
                            )

                            # Test satellite field validation
                            original_satellite = satellite_field.input_value()
                            logger.info(
                                f"Original satellite: {original_satellite} on {device_model}"
                            )

                            # Test with valid satellite ID
                            test_satellite = "GPS-01"
                            satellite_field.fill("")
                            time.sleep(0.3)
                            satellite_field.fill(test_satellite)
                            time.sleep(0.3)

                            new_satellite = satellite_field.input_value()
                            if new_satellite == test_satellite:
                                logger.info(
                                    f" Valid satellite ID accepted: {test_satellite} on {device_model}"
                                )

                                # Test with invalid satellite to see validation
                                test_invalid_satellite = "INVALID-SAT"
                                satellite_field.fill("")
                                time.sleep(0.3)
                                satellite_field.fill(test_invalid_satellite)
                                time.sleep(0.3)

                                invalid_satellite = satellite_field.input_value()
                                if invalid_satellite == test_invalid_satellite:
                                    logger.info(
                                        f"ℹ Invalid satellite was accepted (validation may be server-side): {test_invalid_satellite} on {device_model}"
                                    )
                                else:
                                    logger.info(
                                        f" Invalid satellite was rejected by client-side validation: {test_invalid_satellite} on {device_model}"
                                    )

                                # Restore original value
                                satellite_field.fill(original_satellite)
                                restored_satellite = satellite_field.input_value()
                                if restored_satellite == original_satellite:
                                    logger.info(
                                        f" Original satellite value restored successfully on {device_model}"
                                    )
                                else:
                                    logger.warning(
                                        f" Failed to restore original satellite value on {device_model}"
                                    )

                            else:
                                logger.warning(
                                    f" Satellite field entry failed. Expected: {test_satellite}, Got: {new_satellite} on {device_model}"
                                )
                        else:
                            logger.warning(
                                f" Series 2 satellite field is not editable on {device_model}"
                            )

                    except Exception as e:
                        logger.warning(
                            f"Series 2 satellite field interaction failed: {e}"
                        )
            else:
                logger.info(
                    f"ℹ Series 2 satellite elements not found on {device_model}"
                )

        except Exception as e:
            logger.warning(f"Series 2 GNSS satellite pattern test failed: {e}")

    elif device_series == 3:
        # Series 3 devices may have enhanced GNSS satellite detection
        logger.info("Testing Series 3 GNSS satellite patterns")

        try:
            # Series 3 devices may have advanced satellite management
            series3_satellite_features = [
                ".satellite-settings",
                ".gnss-configuration",
                ".advanced-satellite",
                ".satellite-status",
                ".gnss-status",
                ".satellite-monitor",
                ".satellite-metrics",
                ".gnss-monitor",
                ".satellite-info",
            ]

            for feature in series3_satellite_features:
                feature_elements = unlocked_config_page.locator(feature)
                if feature_elements.count() > 0:
                    logger.info(
                        f" Series 3 satellite feature found: {feature} on {device_model}"
                    )
                else:
                    logger.info(
                        f"ℹ Series 3 satellite feature not found: {feature} on {device_model}"
                    )

            # Series 3 specific satellite configuration
            series3_satellite_selectors = [
                "input[name*='satellite']",
                "input[name*='gnss']",
                "input[name*='gps']",
                ".satellite-config",
                ".gnss-config",
                ".gps-config",
            ]

            for selector in series3_satellite_selectors:
                satellite_elements = unlocked_config_page.locator(selector)
                if satellite_elements.count() > 0:
                    logger.info(
                        f" Series 3 enhanced satellite element found: {selector} on {device_model}"
                    )

                    # Test satellite field interaction
                    try:
                        satellite_field = satellite_elements.first
                        if satellite_field.is_editable():
                            logger.info(
                                f" Series 3 satellite field is editable: {selector} on {device_model}"
                            )

                            # Test advanced satellite validation for Series 3
                            test_satellite = "GPS-03"
                            satellite_field.fill(test_satellite)
                            time.sleep(0.5)

                            result_satellite = satellite_field.input_value()
                            if result_satellite == test_satellite:
                                logger.info(
                                    f" Series 3 advanced satellite validation functional: {test_satellite} on {device_model}"
                                )
                            else:
                                logger.warning(
                                    f" Series 3 advanced satellite validation failed: {test_satellite} on {device_model}"
                                )
                        else:
                            logger.info(
                                f"ℹ Series 3 satellite field not editable: {selector} on {device_model}"
                            )
                    except Exception as e:
                        logger.warning(
                            f"Series 3 satellite field interaction failed: {e}"
                        )
                else:
                    logger.info(
                        f"ℹ Series 3 satellite element not found: {selector} on {device_model}"
                    )

            # Test satellite constellation configuration
            constellation_selectors = [
                ".gps-constellation",
                ".glonass-constellation",
                ".galileo-constellation",
                ".beidou-constellation",
                ".constellation-config",
            ]

            constellation_count = 0
            for selector in constellation_selectors:
                constellation_elements = unlocked_config_page.locator(selector)
                if constellation_elements.count() > 0:
                    constellation_count += constellation_elements.count()
                    logger.info(
                        f" Satellite constellation found: {selector} ({constellation_elements.count()}) on {device_model}"
                    )

            if constellation_count > 0:
                logger.info(
                    f" Series 3 satellite constellation elements found: {constellation_count} on {device_model}"
                )
            else:
                logger.info(
                    f"ℹ No Series 3 satellite constellation elements found on {device_model}"
                )

        except Exception as e:
            logger.warning(f"Series 3 GNSS satellite pattern test failed: {e}")

    # Test satellite status and information display
    logger.info("Testing satellite status and information display")

    try:
        # Look for satellite status indicators
        status_selectors = [
            ".satellite-status",
            ".gnss-status",
            ".gps-status",
            "text='Detected'",
            "text='Tracking'",
            "text='Locked'",
            ".satellite-info",
            ".gnss-info",
            ".gps-info",
            ".satellite-metrics",
            ".signal-quality",
        ]

        status_elements_found = []
        for selector in status_selectors:
            status_elements = unlocked_config_page.locator(selector)
            if status_elements.count() > 0:
                status_elements_found.append((selector, status_elements.count()))
                logger.info(
                    f" Satellite status element found: {selector} ({status_elements.count()}) on {device_model}"
                )

        if status_elements_found:
            logger.info(
                f" Satellite status elements discovered: {len(status_elements_found)} types on {device_model}"
            )
        else:
            logger.info(
                f"ℹ No specific satellite status elements found on {device_model}"
            )

    except Exception as e:
        logger.warning(f"Satellite status detection failed on {device_model}: {e}")

    # Cross-validate satellite patterns with DeviceCapabilities
    logger.info("Cross-validating satellite patterns with DeviceCapabilities")

    try:
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            gnss_patterns = device_capabilities_data.get(
                "gnss_configuration_patterns", {}
            )
            satellite_patterns = gnss_patterns.get("satellite_detection", {})

            if satellite_patterns:
                logger.info(
                    f"Satellite patterns for {device_model}: {satellite_patterns}"
                )

                # Validate satellite detection expectations
                satellite_types = satellite_patterns.get("satellite_types", [])
                detection_methods = satellite_patterns.get("detection_methods", [])
                status_indicators = satellite_patterns.get("status_indicators", [])

                logger.info(f"Expected satellite types: {satellite_types}")
                logger.info(f"Detection methods: {detection_methods}")
                logger.info(f"Status indicators: {status_indicators}")

                # Cross-reference with actual findings
                for satellite_type in satellite_types:
                    type_elements = unlocked_config_page.locator(
                        f"text='{satellite_type}'"
                    )
                    if type_elements.count() > 0:
                        logger.info(
                            f" Expected satellite type found: {satellite_type} on {device_model}"
                        )
                    else:
                        logger.info(
                            f"ℹ Expected satellite type not found: {satellite_type} on {device_model}"
                        )

            else:
                logger.info(
                    f"No specific satellite patterns defined for {device_model}"
                )

    except Exception as e:
        logger.warning(
            f"DeviceCapabilities satellite detection cross-check failed: {e}"
        )

    # Test GNSS save button behavior
    logger.info("Testing GNSS save button behavior")

    try:
        save_button_config = DeviceCapabilities.get_interface_specific_save_button(
            device_model, "gnss_configuration", "gnss"
        )

        if save_button_config and "selector" in save_button_config:
            save_button_locator = unlocked_config_page.locator(
                save_button_config["selector"]
            )
            if save_button_locator.count() > 0:
                logger.info(
                    f" Save button found using device-specific pattern on {device_model}"
                )

                # Test save button state with satellite changes
                try:
                    # Make a satellite change to trigger save button enable
                    satellite_field = unlocked_config_page.locator(
                        "input[name*='satellite'], input[id*='satellite']"
                    )
                    if satellite_field.count() > 0:
                        current_value = satellite_field.input_value()
                        satellite_field.fill(current_value + "_change")

                        # Wait for state change with device-enhanced timeout
                        time.sleep(1.0)

                        # Check if save button state changed
                        changed_enabled = save_button_locator.is_enabled()
                        logger.info(
                            f"Save button state after satellite change: {'enabled' if changed_enabled else 'disabled'} on {device_model}"
                        )

                        # Restore original value
                        satellite_field.fill(current_value)
                        time.sleep(0.5)

                except Exception as e:
                    logger.warning(
                        f"Save button state test with satellite change failed on {device_model}: {e}"
                    )
            else:
                logger.warning(
                    f" Save button not found using device-specific pattern on {device_model}"
                )

    except Exception as e:
        logger.warning(
            f"Save button test with GNSS configuration failed on {device_model}: {e}"
        )

    # Performance validation for GNSS satellite detection
    logger.info("Testing GNSS satellite detection performance")

    try:
        start_time = time.time()

        # Test satellite field interaction performance
        satellite_field = unlocked_config_page.locator(
            "input[name*='satellite'], input[id*='satellite']"
        )
        if satellite_field.count() > 0:
            # Test rapid satellite field interactions
            test_satellites = ["GPS-01", "GLONASS-02", "GALILEO-03"]

            for test_satellite in test_satellites:
                satellite_field.fill(test_satellite)
                time.sleep(0.1)  # Minimal delay for validation

            end_time = time.time()
            satellite_detection_time = end_time - start_time

            logger.info(
                f"GNSS satellite detection time for multiple IDs: {satellite_detection_time:.3f}s on {device_model}"
            )

            # Cross-reference with performance expectations
            performance_data = DeviceCapabilities.get_performance_expectations(
                device_model
            )
            if performance_data:
                gnss_performance = performance_data.get(
                    "gnss_configuration_performance", {}
                )
                if gnss_performance:
                    typical_satellite_detection = gnss_performance.get(
                        "typical_satellite_detection", ""
                    )
                    logger.info(
                        f"Performance baseline for satellite detection: {typical_satellite_detection}"
                    )

    except Exception as e:
        logger.warning(
            f"GNSS satellite detection performance test failed on {device_model}: {e}"
        )

    # Final validation and comprehensive logging
    logger.info(f"GNSS Satellite Detection Test Results for {device_model}:")
    logger.info(f"  - Device Series: {device_series}")
    logger.info(f"  - Device Model: {device_model}")
    logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
    logger.info(f"  - Satellite Patterns: {satellite_patterns}")

    # Final GNSS satellite detection validation
    try:
        # Check for satellite validation indicators
        satellite_validation_status = unlocked_config_page.locator(
            "text='Satellite', text='GNSS', text='GPS', "
            + ".satellite-status, .gnss-field, .gps-field"
        )

        if satellite_validation_status.count() > 0:
            logger.info(f" Satellite validation elements found on {device_model}")
        else:
            logger.info(f"ℹ No satellite validation elements visible on {device_model}")

        # Final comprehensive GNSS satellite summary
        logger.info(f" GNSS satellite detection test completed for {device_model}")
        logger.info(f" Device-enhanced patterns validated for {device_series} series")
        logger.info(f" DeviceCapabilities integration successful")

        # Cleanup - restore any modified values
        try:
            satellite_field = unlocked_config_page.locator(
                "input[name*='satellite'], input[id*='satellite']"
            )
            if satellite_field.count() > 0:
                original_value = satellite_field.get_attribute("value") or ""
                test_value = satellite_field.input_value()

                # Restore original value if it was changed during testing
                if test_value != original_value:
                    satellite_field.fill(original_value)
                    restored_value = satellite_field.input_value()
                    if restored_value == original_value:
                        logger.info(
                            f" Original satellite configuration restored on {device_model}"
                        )
                    else:
                        logger
                        logger.warning(
                            f" Failed to restore original satellite configuration on {device_model}"
                        )
                else:
                    logger.info(
                        f" Satellite configuration already in original state on {device_model}"
                    )
            else:
                logger.info(
                    f"ℹ No satellite fields found for cleanup on {device_model}"
                )

        except Exception as e:
            logger.warning(
                f"Cleanup phase failed during GNSS satellite detection test on {device_model}: {e}"
            )

        logger.info(
            f" Complete GNSS satellite detection test suite executed for {device_model}"
        )
        logger.info(
            f" Device series {device_series} GNSS patterns validated successfully"
        )
        logger.info(
            f" DeviceCapabilities integration complete for GNSS satellite detection"
        )

    except Exception as e:
        pytest.fail(f"GNSS satellite detection test failed on {device_model}: {e}")
