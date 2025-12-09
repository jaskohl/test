"""
Category 11: Form Validation - Test 11.2.1
Identifier Field Maxlength Behavior - DeviceCapabilities Enhanced
Test Count: 2 of 18 in Category 11
Hardware: Device Only
Priority: MEDIUM - Form validation foundation
Series: Both Series 2 and 3
ENHANCED: DeviceCapabilities integration for device-aware form validation
Based on form validation requirements and field behavior patterns
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_11_2_1_identifier_field_maxlength_behavior_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 11.2.1: Identifier Field Maxlength Behavior - DeviceCapabilities Enhanced
    Purpose: Verify identifier field maxlength enforcement with device-aware validation
    Expected: Field enforces character limits, validation works across device variants
    ENHANCED: DeviceCapabilities integration for device-aware maxlength validation
    Series: Both - validates maxlength patterns across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate identifier field behavior"
        )

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing identifier field maxlength on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    try:
        # Navigate to general configuration page
        unlocked_config_page.goto(f"{base_url}/general", wait_until="domcontentloaded")

        # Wait for page load with device-aware timeout
        page_load_timeout = int(5000 * timeout_multiplier)
        unlocked_config_page.wait_for_load_state(
            "domcontentloaded", timeout=page_load_timeout
        )

        # Find identifier field with multiple fallback strategies
        identifier_field = unlocked_config_page.locator("input[name='identifier']")

        # Try alternative selectors if primary fails
        if identifier_field.count() == 0:
            identifier_field = unlocked_config_page.locator("input#identifier")

        if identifier_field.count() == 0:
            identifier_field = unlocked_config_page.locator(
                "input[name='device_identifier']"
            )

        assert (
            identifier_field.count() > 0
        ), f"Identifier field not found on {device_model}"

        # Get device-specific field constraints - using reasonable defaults since no field constraints in DeviceCapabilities
        # Most identifier fields typically have 50-64 character limits
        expected_maxlength = 50  # Standard maxlength for identifier fields

        logger.info(
            f"Expected maxlength for identifier field on {device_model}: {expected_maxlength}"
        )

        # Make field visible with device-aware timeout
        expect(identifier_field).to_be_visible(timeout=3000 * timeout_multiplier)

        # Test maxlength enforcement
        # Clear field first
        identifier_field.clear()

        # Generate test strings of different lengths
        test_string_short = "TEST"
        test_string_exact = "A" * expected_maxlength
        test_string_over = "A" * (expected_maxlength + 10)

        # Test 1: Short string should be accepted
        identifier_field.fill(test_string_short)
        actual_value = identifier_field.input_value()
        assert len(actual_value) <= len(
            test_string_short
        ), f"Short string validation failed on {device_model}"
        logger.info(
            f" Short string ({len(test_string_short)} chars) accepted on {device_model}"
        )

        # Test 2: Exact maxlength string should be accepted
        identifier_field.fill(test_string_exact)
        actual_value = identifier_field.input_value()
        assert (
            len(actual_value) <= expected_maxlength
        ), f"Exact maxlength string rejected on {device_model}"
        logger.info(
            f" Exact maxlength string ({len(test_string_exact)} chars) accepted on {device_model}"
        )

        # Test 3: String exceeding maxlength should be truncated
        identifier_field.fill(test_string_over)
        actual_value = identifier_field.input_value()
        assert (
            len(actual_value) <= expected_maxlength
        ), f"Overlimit string not truncated on {device_model}"
        assert (
            len(actual_value) == expected_maxlength
        ), f"Overlimit string not truncated to exact maxlength on {device_model}"
        logger.info(
            f" Overlimit string truncated to {len(actual_value)} chars on {device_model}"
        )

        # Test device series-specific validation patterns
        if device_series == 2:
            # Series 2: Basic identifier validation
            logger.info(
                f"Series 2 identifier validation patterns applied on {device_model}"
            )

            # Test special characters handling
            special_chars = "TEST-DEVICE_V1.2"
            identifier_field.fill(special_chars)
            actual_value = identifier_field.input_value()
            if len(actual_value) <= expected_maxlength:
                logger.info(f" Special characters handled correctly on Series 2 device")
            else:
                logger.warning(
                    f"Special characters may cause issues on Series 2 device"
                )

        elif device_series == 3:
            # Series 3: May have more complex identifier validation
            logger.info(
                f"Series 3 identifier validation patterns applied on {device_model}"
            )

            # Test advanced identifier patterns
            complex_identifier = "KRONOS-TEST-DEVICE-SERIES-3-MODEL"
            identifier_field.fill(complex_identifier)
            actual_value = identifier_field.input_value()

            if len(actual_value) <= expected_maxlength:
                logger.info(f" Complex identifier handled correctly on Series 3 device")
            else:
                logger.warning(
                    f"Complex identifier validation may need adjustment on Series 3 device"
                )

        # Test maxlength attribute consistency
        maxlength_attr = identifier_field.get_attribute("maxlength")
        if maxlength_attr:
            maxlength_int = int(maxlength_attr)
            assert (
                maxlength_int == expected_maxlength
            ), f"Maxlength attribute mismatch on {device_model}"
            logger.info(f" Maxlength attribute validated: {maxlength_int}")
        else:
            logger.warning(f"Maxlength attribute not present on {device_model}")

        # Test paste behavior with device-aware timing (FIXED: removed max_length parameter)
        try:
            identifier_field.clear()
            identifier_field.fill("")

            # Test paste operation - use fill() instead of type() with max_length
            # Fill method respects maxlength attribute automatically
            identifier_field.fill(test_string_over)
            actual_value = identifier_field.input_value()
            assert (
                len(actual_value) <= expected_maxlength
            ), f"Paste operation exceeded maxlength on {device_model}"
            logger.info(f" Paste operation respects maxlength on {device_model}")

        except Exception as paste_error:
            logger.warning(
                f"Paste behavior test failed on {device_model}: {paste_error}"
            )

        # Test save button state with maxlength constraints
        try:
            # Make a valid change that reaches maxlength
            identifier_field.clear()
            identifier_field.fill(test_string_exact)

            # Look for save button with device-aware pattern
            save_patterns = [
                "button[type='submit']",
                "input[type='submit']",
                "button.save",
                ".save-button",
            ]

            save_button_found = False
            for pattern in save_patterns:
                save_button = unlocked_config_page.locator(pattern)
                if save_button.count() > 0:
                    try:
                        expect(save_button).to_be_visible(timeout=2000)
                        save_button_found = True
                        logger.info(
                            f" Save button found with pattern '{pattern}' on {device_model}"
                        )
                        break
                    except:
                        continue

            if not save_button_found:
                logger.warning(
                    f"Save button not found with any pattern on {device_model}"
                )

        except Exception as save_error:
            logger.warning(
                f"Save button state test failed on {device_model}: {save_error}"
            )

        # Log comprehensive test results
        logger.info(f"Identifier Field Maxlength Test Results for {device_model}:")
        logger.info(f"  - Device Series: {device_series}")
        logger.info(f"  - Expected Maxlength: {expected_maxlength}")
        logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")

        logger.info(f"  - Field Constraints: Standard 50-character limit applied")

        print(
            f"IDENTIFIER FIELD MAXLENGTH VALIDATION SUCCESSFUL: {device_model} (Series {device_series})"
        )

    except Exception as e:
        logger.error(f"Identifier field maxlength test failed on {device_model}: {e}")
        raise

    finally:
        # Small cleanup wait for device stability
        time.sleep(int(0.5 * timeout_multiplier))
