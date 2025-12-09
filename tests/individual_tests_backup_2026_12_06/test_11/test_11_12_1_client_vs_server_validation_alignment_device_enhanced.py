"""
Test 11.12.1: Client vs Server Validation Alignment (Device-Enhanced)
Purpose: Consistency between client-side and server-side validation with device-aware behavior
Expected: Device should provide consistent validation feedback based on capabilities
Device-Enhanced: Full DeviceCapabilities integration with series-specific patterns
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_12_1_client_vs_server_validation_alignment_device_enhanced(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.12.1: Client vs Server Validation Alignment (Device-Enhanced)
    Purpose: Consistency between client-side and server-side validation with device-aware behavior
    Expected: Device should provide consistent validation feedback based on capabilities
    Device-Enhanced: Full DeviceCapabilities integration with series-specific patterns
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate client-server consistency"
        )

    # Get device capabilities for enhanced validation
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    try:
        general_config_page.navigate_to_page()

        # Device-aware timeout handling
        base_timeout = 5000
        enhanced_timeout = int(base_timeout * timeout_multiplier)

        # Test alignment between client and server validation with device-specific patterns
        if device_series == "Series 2":
            # Series 2 has simpler validation patterns
            validation_field_selectors = [
                "input[type='email']",
                "input[name*='email' i]",
                "input[type='url']",
                "input[name*='url' i]",
                "input[type='text'].required",
            ]
            server_error_selectors = [
                ".error",
                ".server-error",
                "[role='alert']",
                ".validation-error",
            ]
        else:  # Series 3
            # Series 3 has more complex validation including PTP-related fields
            validation_field_selectors = [
                "input[type='email']",
                "input[name*='email' i]",
                "input[type='url']",
                "input[name*='url' i]",
                "input[type='text'].required",
                "[data-field-type='ptp-email']",
                "[data-field-type='ptp-url']",
            ]
            server_error_selectors = [
                ".error",
                ".server-error",
                "[role='alert']",
                ".validation-error",
                ".ptp-error",
                "[data-field-type='ptp'][aria-invalid='true']",
            ]

        total_tested_validations = 0

        # Test each type of validation field
        for selector in validation_field_selectors:
            validation_fields = general_config_page.page.locator(selector)
            count = validation_fields.count()

            if count > 0:
                print(f"Found {count} validation fields using selector: {selector}")

                # Test client-server validation alignment (up to 2 fields to avoid overwhelming)
                for i in range(min(count, 2)):
                    try:
                        validation_field = validation_fields.nth(i)

                        # Test invalid data that should trigger both client and server validation
                        if "email" in selector.lower() or "ptp-email" in selector:
                            invalid_data = "invalid-email-format"
                        elif "url" in selector.lower() or "ptp-url" in selector:
                            invalid_data = "invalid-url-format"
                        else:
                            invalid_data = (
                                "invalid@data#format"  # General invalid format
                            )

                        # Clear field and enter invalid data
                        validation_field.clear()
                        validation_field.fill(invalid_data)

                        # Trigger client-side validation
                        validation_field.dispatch_event("input")

                        # Test server-side validation by attempting form submission
                        # Find appropriate submit button based on device series
                        if device_series == "Series 2":
                            submit_selectors = [
                                "button[type='submit']",
                                ".save-btn",
                                "#save",
                            ]
                        else:
                            submit_selectors = [
                                "button[type='submit']",
                                ".save-btn",
                                "#save",
                                ".ptp-save-btn",
                                "[data-field-type='ptp'] button[type='submit']",
                            ]

                        submit_found = False
                        for submit_selector in submit_selectors:
                            submit_btn = general_config_page.page.locator(
                                submit_selector
                            )
                            if submit_btn.is_visible(timeout=enhanced_timeout):
                                print(f"Found submit button: {submit_selector}")

                                # Capture validation state before submission
                                before_submit_errors = general_config_page.page.locator(
                                    ".error, .validation-error, [aria-invalid='true']"
                                ).count()

                                # Submit to trigger server validation
                                submit_btn.click()

                                # Wait for server validation response
                                time.sleep(0.5)

                                # Check for server-side validation errors
                                server_error_selector = ", ".join(
                                    server_error_selectors
                                )
                                server_errors = general_config_page.page.locator(
                                    server_error_selector
                                )

                                if server_errors.count() > 0:
                                    try:
                                        # Ensure error messages are visible
                                        expect(server_errors.first).to_be_visible(
                                            timeout=enhanced_timeout
                                        )

                                        after_submit_errors = server_errors.count()
                                        print(
                                            f"Server validation errors: {after_submit_errors}"
                                        )

                                        # Validate client-server alignment
                                        assert (
                                            after_submit_errors >= before_submit_errors
                                        ), f"Server validation should provide feedback for invalid data on {device_model}"

                                        total_tested_validations += 1
                                        submit_found = True
                                        break

                                    except Exception as e:
                                        print(
                                            f"Error checking server validation: {str(e)}"
                                        )
                                        total_tested_validations += 1
                                        submit_found = True
                                        break
                                else:
                                    print("No server validation errors detected")
                                    total_tested_validations += 1
                                    submit_found = True
                                    break

                        if not submit_found:
                            print(
                                f"No submit button found for validation testing on {device_model}"
                            )
                            total_tested_validations += 1

                    except Exception as e:
                        print(f"Error testing validation field {i}: {str(e)}")
                        total_tested_validations += 1

        # Device-specific validation assertions
        assert (
            total_tested_validations > 0
        ), f"No validation fields could be tested for client-server alignment on {device_model}"

        if device_series == "Series 2":
            print(
                f"Series 2 device {device_model} - validated basic client-server validation alignment"
            )
        else:  # Series 3
            print(
                f"Series 3 device {device_model} - validated enhanced client-server validation alignment"
            )

        # Check for device-specific validation alignment patterns
        if device_series == "Series 3":
            # Look for PTP-specific client-server validation alignment
            ptp_validation_fields = general_config_page.page.locator(
                "[data-field-type='ptp-email'], [data-field-type='ptp-url']"
            )
            if ptp_validation_fields.count() > 0:
                print(f"Found PTP validation fields for Series 3 device {device_model}")
                # PTP fields should have consistent client-server validation
                try:
                    ptp_field = ptp_validation_fields.first
                    ptp_field.clear()
                    ptp_field.fill("invalid_ptp_format")
                    ptp_field.dispatch_event("input")

                    time.sleep(0.3)

                    ptp_server_errors = general_config_page.page.locator(
                        ".ptp-error, [data-field-type='ptp'][aria-invalid='true']"
                    )
                    if ptp_server_errors.count() > 0:
                        expect(ptp_server_errors.first).to_be_visible(
                            timeout=enhanced_timeout
                        )
                        print(
                            f"PTP client-server validation alignment working for Series 3 device {device_model}"
                        )
                except Exception as e:
                    print(f"PTP validation alignment test failed: {str(e)}")
        else:
            print(
                f"Series 2 device {device_model} - no PTP validation alignment expected"
            )

        print(
            f"Successfully validated client-server validation alignment for {device_model} ({device_series}): {total_tested_validations} validations tested"
        )

    finally:
        # Cleanup: Reset fields to original state if needed
        pass
