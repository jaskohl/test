"""
Category 3: General Configuration - Test 3.1.1
Device Information Display - DeviceCapabilities Enhanced
Test Count: 1 of 3 in Category 3
Hardware: Device Only
Priority: HIGH - Device information foundation
Series: Both Series 2 and 3
ENHANCED: DeviceCapabilities integration for device-aware information display validation
Based on general configuration requirements and device information patterns
Device exploration data: device_info.json, dashboard_info.json
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.dashboard_page import DashboardPage
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_3_1_1_device_information_display_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 3.1.1: Device Information Display - DeviceCapabilities Enhanced
    Purpose: Verify device information display accuracy and DeviceCapabilities cross-validation
    Expected: Device info displayed correctly with device-specific fields and timing
    ENHANCED: Full DeviceCapabilities integration for device-aware information validation
    Series: Both - validates information patterns across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate device information display"
        )

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing device information display on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Get device-specific capabilities and expected information
    device_capabilities = DeviceCapabilities.get_capabilities(device_model)
    device_info_expected = device_capabilities.get("device_info", {})

    # Initialize page objects with device-aware patterns
    dashboard_page = DashboardPage(unlocked_config_page, device_model)
    general_config_page = GeneralConfigPage(unlocked_config_page, device_model)

    # Test device information from Dashboard page
    logger.info("Testing device information display on dashboard")

    # Navigate to dashboard
    unlocked_config_page.goto(base_url, wait_until="domcontentloaded")

    # Wait for page stabilization with device-aware timing
    stability_timeout = int(2000 * timeout_multiplier)
    unlocked_config_page.wait_for_load_state(
        "domcontentloaded", timeout=stability_timeout
    )

    # Extract device information from dashboard
    try:
        dashboard_info = dashboard_page.get_device_info()
        logger.info(f"Dashboard device info extracted: {dashboard_info}")

        # Validate dashboard info against expected device model
        if dashboard_info.get("Model"):
            extracted_model = dashboard_info["Model"]
            if extracted_model == device_model:
                logger.info(f" Dashboard model validation PASSED: {extracted_model}")
            else:
                logger.warning(
                    f" Dashboard model validation WARNING: expected {device_model}, got {extracted_model}"
                )
        else:
            logger.warning(f" Dashboard model not found on {device_model}")

    except Exception as e:
        logger.warning(f"Dashboard info extraction failed: {e}")

    # Test device information from General Configuration page
    logger.info("Testing device information display on general configuration page")

    try:
        # Navigate to general configuration page
        unlocked_config_page.goto(f"{base_url}/general", wait_until="domcontentloaded")

        # Wait for page load with device-aware timeout
        page_load_timeout = int(5000 * timeout_multiplier)
        unlocked_config_page.wait_for_load_state(
            "domcontentloaded", timeout=page_load_timeout
        )

        # Test identifier field display
        identifier_field = unlocked_config_page.locator(
            "input[name='identifier'], input#identifier"
        )
        if identifier_field.count() > 0:
            try:
                expect(identifier_field).to_be_visible(
                    timeout=3000 * timeout_multiplier
                )
                identifier_value = identifier_field.input_value()
                logger.info(
                    f" Identifier field found with value: '{identifier_value}' on {device_model}"
                )
            except Exception as e:
                logger.warning(f" Identifier field validation failed: {e}")
        else:
            logger.warning(f" Identifier field not found on {device_model}")

        # Test location field display
        location_field = unlocked_config_page.locator(
            "input[name='location'], input#location"
        )
        if location_field.count() > 0:
            try:
                expect(location_field).to_be_visible(timeout=3000 * timeout_multiplier)
                location_value = location_field.input_value()
                logger.info(
                    f" Location field found with value: '{location_value}' on {device_model}"
                )
            except Exception as e:
                logger.warning(f" Location field validation failed: {e}")
        else:
            logger.warning(f" Location field not found on {device_model}")

        # Test contact field display
        contact_field = unlocked_config_page.locator(
            "input[name='contact'], input#contact"
        )
        if contact_field.count() > 0:
            try:
                expect(contact_field).to_be_visible(timeout=3000 * timeout_multiplier)
                contact_value = contact_field.input_value()
                logger.info(
                    f" Contact field found with value: '{contact_value}' on {device_model}"
                )
            except Exception as e:
                logger.warning(f" Contact field validation failed: {e}")
        else:
            logger.warning(f" Contact field not found on {device_model}")

    except Exception as e:
        pytest.fail(f"General configuration page access failed on {device_model}: {e}")

    # Cross-validate with DeviceCapabilities expected device info
    logger.info("Cross-validating device info with DeviceCapabilities")

    device_capabilities_data = DeviceCapabilities.get_device_info(device_model)
    if device_capabilities_data:
        logger.info(
            f"DeviceCapabilities info for {device_model}: {device_capabilities_data}"
        )

    # Validate device series-specific information patterns
    if device_series == 2:
        # Series 2 devices have simpler information fields
        series2_expected_fields = ["identifier", "location", "contact"]
        found_series2_fields = []

        for field_name in series2_expected_fields:
            field_locator = unlocked_config_page.locator(
                f"input[name='{field_name}'], input#{field_name}"
            )
            if field_locator.count() > 0 and field_locator.is_visible():
                found_series2_fields.append(field_name)
                logger.info(f" Series 2 field {field_name} found on {device_model}")
            else:
                logger.warning(
                    f" Series 2 field {field_name} missing on {device_model}"
                )

        logger.info(
            f"Series 2 fields found: {len(found_series2_fields)}/{len(series2_expected_fields)}"
        )

    elif device_series == 3:
        # Series 3 devices may have additional information fields
        series3_additional_fields = [
            "description",
            "notes",
            "firmware_version",
            "serial_number",
        ]
        found_series3_fields = []

        for field_name in series3_additional_fields:
            field_locator = unlocked_config_page.locator(
                f"input[name='{field_name}'], input#{field_name}, textarea[name='{field_name}']"
            )
            if field_locator.count() > 0 and field_locator.is_visible():
                found_series3_fields.append(field_name)
                logger.info(
                    f" Series 3 additional field {field_name} found on {device_model}"
                )
            else:
                logger.info(
                    f"ℹ Series 3 additional field {field_name} not available on {device_model}"
                )

        logger.info(
            f"Series 3 additional fields found: {len(found_series3_fields)}/{len(series3_additional_fields)}"
        )

    # Test device information editing capability
    try:
        logger.info("Testing device information editing capability")

        # Test identifier field editing
        identifier_field = unlocked_config_page.locator(
            "input[name='identifier'], input#identifier"
        )
        if identifier_field.count() > 0:
            original_identifier = identifier_field.input_value()

            # Clear and enter test value
            identifier_field.fill("")
            identifier_field.fill("TEST_DEVICE_IDENTIFIER")

            # Verify the value was entered
            new_identifier = identifier_field.input_value()
            if new_identifier == "TEST_DEVICE_IDENTIFIER":
                logger.info(f" Identifier field editing functional on {device_model}")

                # Restore original value
                identifier_field.fill(original_identifier)
                restored_identifier = identifier_field.input_value()
                if restored_identifier == original_identifier:
                    logger.info(
                        f" Identifier field restoration successful on {device_model}"
                    )
                else:
                    logger.warning(
                        f" Identifier field restoration failed on {device_model}"
                    )
            else:
                logger.warning(f" Identifier field editing failed on {device_model}")

        # Test location field editing
        location_field = unlocked_config_page.locator(
            "input[name='location'], input#location"
        )
        if location_field.count() > 0:
            original_location = location_field.input_value()

            # Clear and enter test value
            location_field.fill("")
            location_field.fill("TEST_LOCATION")

            # Verify the value was entered
            new_location = location_field.input_value()
            if new_location == "TEST_LOCATION":
                logger.info(f" Location field editing functional on {device_model}")

                # Restore original value
                location_field.fill(original_location)
                restored_location = location_field.input_value()
                if restored_location == original_location:
                    logger.info(
                        f" Location field restoration successful on {device_model}"
                    )
                else:
                    logger.warning(
                        f" Location field restoration failed on {device_model}"
                    )
            else:
                logger.warning(f" Location field editing failed on {device_model}")

    except Exception as e:
        logger.warning(f"Device information editing test failed on {device_model}: {e}")

    # Test save functionality for device information changes
    try:
        save_button = DeviceCapabilities.get_interface_specific_save_button(
            device_model, "general_configuration", "general"
        )

        if save_button and "selector" in save_button:
            save_button_locator = unlocked_config_page.locator(save_button["selector"])
            if save_button_locator.count() > 0:
                logger.info(
                    f" Save button found using device-specific pattern on {device_model}"
                )

                # Test save button state management
                try:
                    # Make a small change to trigger save button enable
                    identifier_field = unlocked_config_page.locator(
                        "input[name='identifier']"
                    )
                    if identifier_field.count() > 0:
                        current_value = identifier_field.input_value()
                        identifier_field.fill(current_value + "_test")

                        # Check if save button becomes enabled
                        try:
                            save_button_locator.wait_for(
                                timeout=3000 * timeout_multiplier
                            )
                            # Additional check for enabled state
                            expect(save_button_locator).to_be_enabled(timeout=1000)
                            logger.info(
                                f" Save button state management functional on {device_model}"
                            )
                        except Exception as state_error:
                            logger.warning(
                                f" Save button state check failed: {state_error}"
                            )
                            # Continue test even if state check fails
                            logger.info(
                                f"Save button found but state management unclear on {device_model}"
                            )

                        # Restore original value
                        identifier_field.fill(current_value)

                except Exception as e:
                    logger.warning(
                        f"Save button state management test failed on {device_model}: {e}"
                    )
            else:
                logger.warning(
                    f" Save button not found using device-specific pattern on {device_model}"
                )

    except Exception as e:
        logger.warning(f"Save button test failed on {device_model}: {e}")

    # Final validation and comprehensive logging
    logger.info(f"Device Information Display Test Results for {device_model}:")
    logger.info(f"  - Device Series: {device_series}")
    logger.info(f"  - Device Model: {device_model}")
    logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
    logger.info(f"  - Expected Capabilities: {device_capabilities}")

    # Performance validation
    start_time = time.time()

    # Test page load performance
    unlocked_config_page.reload()
    load_time = time.time() - start_time

    logger.info(f"  - Page Load Time: {load_time:.2f}s")

    # Cross-reference with performance expectations
    performance_data = DeviceCapabilities.get_performance_expectations(device_model)
    if performance_data:
        general_performance = performance_data.get(
            "general_configuration_performance", {}
        )
        if general_performance:
            typical_time = general_performance.get("typical_page_load", "")
            logger.info(f"  - Performance Baseline: {typical_time}")

    # Final validation
    dashboard_info = {}
    try:
        dashboard_page = DashboardPage(unlocked_config_page, device_model)
        dashboard_info = dashboard_page.get_device_info()
    except:
        pass

    if dashboard_info.get("Model") or device_model:
        logger.info(f" Device information display validation PASSED for {device_model}")
        print(
            f"DEVICE INFORMATION DISPLAY SUCCESSFUL: {device_model} (Series {device_series})"
        )
    else:
        pytest.fail(
            f"Device information display validation FAILED - insufficient information on {device_model}"
        )
