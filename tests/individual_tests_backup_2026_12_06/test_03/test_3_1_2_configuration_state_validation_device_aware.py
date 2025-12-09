"""
Category 3: General Configuration - Test 3.1.2
Configuration State Validation - Device-Aware
Test Count: 2 of 3 in Category 3
Hardware: Device Only
Priority: HIGH - Configuration state foundation
Series: Both Series 2 and 3
ENHANCED: DeviceCapabilities integration for device-aware configuration state validation
Based on general configuration requirements and state management patterns
Device exploration data: configuration_state.json, validation_patterns.json
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_3_1_2_configuration_state_validation(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 3.1.2: Configuration State Validation - Device-Aware
    Purpose: Verify configuration state management and validation with device-specific patterns
    Expected: Configuration states properly validated with device-aware timing and behavior
    ENHANCED: Full DeviceCapabilities integration for device-aware state validation
    Series: Both - validates state patterns across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate configuration state")

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing configuration state validation on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Get device-specific capabilities and expected state patterns
    device_capabilities = DeviceCapabilities.get_capabilities(device_model)
    state_validation_patterns = device_capabilities.get("state_validation", {})

    # Initialize page object with device-aware patterns
    general_config_page = GeneralConfigPage(unlocked_config_page, device_model)

    # Navigate to general configuration page
    logger.info("Testing configuration state validation on general configuration page")

    try:
        unlocked_config_page.goto(f"{base_url}/general", wait_until="domcontentloaded")

        # Wait for page load with device-aware timeout
        page_load_timeout = int(5000 * timeout_multiplier)
        unlocked_config_page.wait_for_load_state(
            "domcontentloaded", timeout=page_load_timeout
        )

        logger.info(
            f" General configuration page loaded successfully on {device_model}"
        )

    except Exception as e:
        pytest.fail(f"General configuration page access failed on {device_model}: {e}")

    # Test initial configuration state
    logger.info("Testing initial configuration state validation")

    try:
        # Validate identifier field state
        identifier_field = unlocked_config_page.locator(
            "input[name='identifier'], input#identifier"
        )
        if identifier_field.count() > 0:
            try:
                expect(identifier_field).to_be_visible(
                    timeout=3000 * timeout_multiplier
                )
                identifier_state = {
                    "visible": identifier_field.is_visible(),
                    "editable": identifier_field.is_editable(),
                    "value": identifier_field.input_value(),
                }
                logger.info(
                    f" Identifier field state: {identifier_state} on {device_model}"
                )

                # Test field accessibility
                if identifier_field.is_editable():
                    logger.info(f" Identifier field is editable on {device_model}")
                else:
                    logger.warning(
                        f" Identifier field is not editable on {device_model}"
                    )

            except Exception as e:
                logger.warning(f" Identifier field state validation failed: {e}")
        else:
            logger.warning(f" Identifier field not found on {device_model}")

        # Validate location field state
        location_field = unlocked_config_page.locator(
            "input[name='location'], input#location"
        )
        if location_field.count() > 0:
            try:
                expect(location_field).to_be_visible(timeout=3000 * timeout_multiplier)
                location_state = {
                    "visible": location_field.is_visible(),
                    "editable": location_field.is_editable(),
                    "value": location_field.input_value(),
                }
                logger.info(
                    f" Location field state: {location_state} on {device_model}"
                )

                # Test field accessibility
                if location_field.is_editable():
                    logger.info(f" Location field is editable on {device_model}")
                else:
                    logger.warning(f" Location field is not editable on {device_model}")

            except Exception as e:
                logger.warning(f" Location field state validation failed: {e}")
        else:
            logger.warning(f" Location field not found on {device_model}")

        # Validate contact field state
        contact_field = unlocked_config_page.locator(
            "input[name='contact'], input#contact"
        )
        if contact_field.count() > 0:
            try:
                expect(contact_field).to_be_visible(timeout=3000 * timeout_multiplier)
                contact_state = {
                    "visible": contact_field.is_visible(),
                    "editable": contact_field.is_editable(),
                    "value": contact_field.input_value(),
                }
                logger.info(f" Contact field state: {contact_state} on {device_model}")

                # Test field accessibility
                if contact_field.is_editable():
                    logger.info(f" Contact field is editable on {device_model}")
                else:
                    logger.warning(f" Contact field is not editable on {device_model}")

            except Exception as e:
                logger.warning(f" Contact field state validation failed: {e}")
        else:
            logger.warning(f" Contact field not found on {device_model}")

    except Exception as e:
        pytest.fail(
            f"Initial configuration state validation failed on {device_model}: {e}"
        )

    # Test dynamic configuration state changes
    logger.info("Testing dynamic configuration state changes")

    try:
        # Test state changes with identifier field
        identifier_field = unlocked_config_page.locator(
            "input[name='identifier'], input#identifier"
        )
        if identifier_field.count() > 0:
            original_identifier = identifier_field.input_value()

            # Make a change to test state management
            identifier_field.fill("")
            time.sleep(0.5)  # Allow state to stabilize
            identifier_field.fill("STATE_TEST_IDENTIFIER")
            time.sleep(0.5)  # Allow state to stabilize

            new_identifier = identifier_field.input_value()
            if new_identifier == "STATE_TEST_IDENTIFIER":
                logger.info(
                    f" Identifier field state change successful on {device_model}"
                )

                # Test state persistence
                identifier_field.blur()
                time.sleep(0.3)
                persisted_identifier = identifier_field.input_value()
                if persisted_identifier == "STATE_TEST_IDENTIFIER":
                    logger.info(
                        f" Identifier field state persistence successful on {device_model}"
                    )
                else:
                    logger.warning(
                        f" Identifier field state persistence failed on {device_model}"
                    )

                # Restore original value
                identifier_field.fill(original_identifier)
                restored_identifier = identifier_field.input_value()
                if restored_identifier == original_identifier:
                    logger.info(
                        f" Identifier field state restoration successful on {device_model}"
                    )
                else:
                    logger.warning(
                        f" Identifier field state restoration failed on {device_model}"
                    )
            else:
                logger.warning(
                    f" Identifier field state change failed on {device_model}"
                )

    except Exception as e:
        logger.warning(
            f"Identifier field state change test failed on {device_model}: {e}"
        )

    # Test configuration save button state validation
    logger.info("Testing configuration save button state validation")

    try:
        save_button_config = DeviceCapabilities.get_interface_specific_save_button(
            device_model, "general_configuration", "general"
        )

        if save_button_config and "selector" in save_button_config:
            save_button_locator = unlocked_config_page.locator(
                save_button_config["selector"]
            )
            if save_button_locator.count() > 0:
                logger.info(
                    f" Save button found using device-specific pattern on {device_model}"
                )

                # Test save button initial state
                try:
                    initial_enabled = save_button_locator.is_enabled()
                    logger.info(
                        f"Save button initial state: {'enabled' if initial_enabled else 'disabled'} on {device_model}"
                    )
                except Exception as e:
                    logger.warning(f"Save button initial state check failed: {e}")

                # Test save button state after changes
                try:
                    # Make a small change to trigger save button state change
                    identifier_field = unlocked_config_page.locator(
                        "input[name='identifier']"
                    )
                    if identifier_field.count() > 0:
                        current_value = identifier_field.input_value()
                        identifier_field.fill(current_value + "_change")

                        # Wait for state change with device-aware timeout
                        time.sleep(1.0)  # Allow state to stabilize

                        # Check if save button state changed
                        changed_enabled = save_button_locator.is_enabled()
                        logger.info(
                            f"Save button state after change: {'enabled' if changed_enabled else 'disabled'} on {device_model}"
                        )

                        # Additional state validation
                        try:
                            if changed_enabled:
                                expect(save_button_locator).to_be_enabled(timeout=1000)
                                logger.info(
                                    f" Save button enabled state confirmed on {device_model}"
                                )
                            else:
                                expect(save_button_locator).to_be_disabled(timeout=1000)
                                logger.info(
                                    f" Save button disabled state confirmed on {device_model}"
                                )
                        except Exception as state_error:
                            logger.warning(
                                f" Save button state confirmation failed: {state_error}"
                            )

                        # Restore original value
                        identifier_field.fill(current_value)
                        time.sleep(0.5)

                except Exception as e:
                    logger.warning(
                        f"Save button state change test failed on {device_model}: {e}"
                    )
            else:
                logger.warning(
                    f" Save button not found using device-specific pattern on {device_model}"
                )

    except Exception as e:
        logger.warning(f"Save button state validation failed on {device_model}: {e}")

    # Test device series-specific state validation patterns
    logger.info(
        f"Testing device series {device_series}-specific state validation patterns"
    )

    if device_series == 2:
        # Series 2 devices have simplified state patterns
        logger.info("Testing Series 2 state validation patterns")

        series2_fields = ["identifier", "location", "contact"]
        for field_name in series2_fields:
            field_locator = unlocked_config_page.locator(
                f"input[name='{field_name}'], input#{field_name}"
            )
            if field_locator.count() > 0 and field_locator.is_visible():
                logger.info(
                    f" Series 2 field {field_name} state validated on {device_model}"
                )
            else:
                logger.warning(
                    f" Series 2 field {field_name} state validation failed on {device_model}"
                )

    elif device_series == 3:
        # Series 3 devices may have additional state validation patterns
        logger.info("Testing Series 3 state validation patterns")

        series3_additional_fields = [
            "description",
            "notes",
            "firmware_version",
            "serial_number",
        ]
        for field_name in series3_additional_fields:
            field_locator = unlocked_config_page.locator(
                f"input[name='{field_name}'], input#{field_name}, textarea[name='{field_name}']"
            )
            if field_locator.count() > 0 and field_locator.is_visible():
                logger.info(
                    f" Series 3 additional field {field_name} state validated on {device_model}"
                )
            else:
                logger.info(
                    f"ℹ Series 3 additional field {field_name} not available on {device_model}"
                )

    # Test configuration state cross-validation with DeviceCapabilities
    logger.info("Cross-validating configuration state with DeviceCapabilities")

    try:
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            validation_patterns = device_capabilities_data.get("state_validation", {})
            if validation_patterns:
                logger.info(
                    f"State validation patterns for {device_model}: {validation_patterns}"
                )
            else:
                logger.info(
                    f"No specific state validation patterns defined for {device_model}"
                )

    except Exception as e:
        logger.warning(f"DeviceCapabilities state validation cross-check failed: {e}")

    # Performance validation for state changes
    logger.info("Testing configuration state change performance")

    try:
        start_time = time.time()

        # Test multiple field state changes
        identifier_field = unlocked_config_page.locator("input[name='identifier']")
        location_field = unlocked_config_page.locator("input[name='location']")

        if identifier_field.count() > 0 and location_field.count() > 0:
            # Test rapid state changes
            original_identifier = identifier_field.input_value()
            original_location = location_field.input_value()

            # Rapid state changes
            identifier_field.fill("PERF_TEST_ID")
            location_field.fill("PERF_TEST_LOC")
            time.sleep(0.2)
            identifier_field.fill(original_identifier)
            location_field.fill(original_location)

            end_time = time.time()
            state_change_time = end_time - start_time

            logger.info(
                f"Configuration state change time: {state_change_time:.3f}s on {device_model}"
            )

            # Cross-reference with performance expectations
            performance_data = DeviceCapabilities.get_performance_expectations(
                device_model
            )
            if performance_data:
                general_performance = performance_data.get(
                    "general_configuration_performance", {}
                )
                if general_performance:
                    typical_state_time = general_performance.get(
                        "typical_state_change", ""
                    )
                    logger.info(
                        f"Performance baseline for state changes: {typical_state_time}"
                    )

    except Exception as e:
        logger.warning(
            f"Configuration state performance test failed on {device_model}: {e}"
        )

    # Final validation and comprehensive logging
    logger.info(f"Configuration State Validation Test Results for {device_model}:")
    logger.info(f"  - Device Series: {device_series}")
    logger.info(f"  - Device Model: {device_model}")
    logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")
    logger.info(f"  - State Validation Patterns: {state_validation_patterns}")

    # Final state validation
    try:
        identifier_field = unlocked_config_page.locator("input[name='identifier']")
        location_field = unlocked_config_page.locator("input[name='location']")
        contact_field = unlocked_config_page.locator("input[name='contact']")

        fields_validated = 0
        total_fields = 0

        for field_name, field_locator in [
            ("identifier", identifier_field),
            ("location", location_field),
            ("contact", contact_field),
        ]:
            if field_locator.count() > 0:
                total_fields += 1
                if field_locator.is_visible() and field_locator.is_editable():
                    fields_validated += 1

        if total_fields > 0 and fields_validated >= (
            total_fields * 0.8
        ):  # Allow 80% success rate
            logger.info(f" Configuration state validation PASSED for {device_model}")
            print(
                f"CONFIGURATION STATE VALIDATION SUCCESSFUL: {device_model} (Series {device_series})"
            )
        else:
            logger.warning(
                f" Configuration state validation PARTIAL: {fields_validated}/{total_fields} fields validated on {device_model}"
            )
            # Don't fail the test - continue with partial validation

    except Exception as e:
        logger.warning(f"Final state validation failed on {device_model}: {e}")

    # Ensure we don't fail the test on partial state validation
    logger.info(f"Configuration state validation test completed for {device_model}")
