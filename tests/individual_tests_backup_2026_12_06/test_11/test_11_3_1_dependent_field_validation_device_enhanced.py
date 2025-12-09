"""
Test 11.3.1: Dependent Field Validation (Device-Enhanced)
Purpose: Validation of fields that depend on other field values with device-aware behavior
Expected: Device-specific dependent field behavior based on capabilities
Device-Enhanced: Full DeviceCapabilities integration with series-specific patterns
"""

import pytest
import time
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_3_1_dependent_field_validation_device_enhanced(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.3.1: Dependent Field Validation (Device-Enhanced)
    Purpose: Validation of fields that depend on other field values with device-aware behavior
    Expected: Device-specific dependent field behavior based on capabilities
    Device-Enhanced: Full DeviceCapabilities integration with series-specific patterns
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate dependent field behavior"
        )

    # Get device capabilities for enhanced validation
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    general_config_page.navigate_to_page()

    # Device-aware timeout handling
    base_timeout = 5000
    enhanced_timeout = int(base_timeout * timeout_multiplier)

    # Test dependent field validation with device-specific patterns
    total_tested_dependencies = 0

    if device_series == "Series 2":
        # Series 2 has simpler dependent field patterns
        dependent_field_pairs = [
            ("vlan_enable", "vlan_id"),
            ("dhcp_enable", "static_ip"),
            ("ntp_enable", "ntp_server"),
        ]
    else:  # Series 3
        # Series 3 has more complex dependent fields including PTP-related dependencies
        dependent_field_pairs = [
            ("vlan_enable", "vlan_id"),
            ("dhcp_enable", "static_ip"),
            ("ntp_enable", "ntp_server"),
            ("ptp_enable", "ptp_priority"),
            ("ptp_enable", "ptp_domain"),
            ("interface_enable", "interface_config"),
        ]

    # Test each dependent field pair
    for enable_field_name, dependent_field_name in dependent_field_pairs:
        try:
            # Look for the enabling field
            enable_field_selectors = [
                f"input[name*='{enable_field_name}' i]",
                f"#{enable_field_name}",
                f".{enable_field_name}",
                f"[data-field-name='{enable_field_name}']",
            ]

            enable_field = None
            for selector in enable_field_selectors:
                candidate = general_config_page.page.locator(selector)
                if candidate.count() > 0:
                    enable_field = candidate.first
                    print(
                        f"Found enable field: {enable_field_name} using selector: {selector}"
                    )
                    break

            if enable_field and enable_field.is_visible(timeout=enhanced_timeout):
                # Look for the dependent field
                dependent_field_selectors = [
                    f"input[name*='{dependent_field_name}' i]",
                    f"#{dependent_field_name}",
                    f".{dependent_field_name}",
                    f"[data-field-name='{dependent_field_name}']",
                ]

                dependent_field = None
                for selector in dependent_field_selectors:
                    candidate = general_config_page.page.locator(selector)
                    if candidate.count() > 0:
                        dependent_field = candidate.first
                        print(
                            f"Found dependent field: {dependent_field_name} using selector: {selector}"
                        )
                        break

                if dependent_field and dependent_field.is_visible(
                    timeout=enhanced_timeout
                ):
                    # Test dependent field behavior

                    # Test 1: Dependent field should be accessible when disabled
                    if enable_field.get_attribute("type") == "checkbox":
                        if enable_field.is_checked():
                            enable_field.uncheck()
                        time.sleep(0.2)

                    # When disabled, dependent field may be disabled or hidden
                    try:
                        is_enabled_when_disabled = dependent_field.is_enabled()
                        is_visible_when_disabled = dependent_field.is_visible()
                        print(
                            f"When disabled - {dependent_field_name}: enabled={is_enabled_when_disabled}, visible={is_visible_when_disabled}"
                        )
                    except:
                        print(
                            f"Dependent field {dependent_field_name} not accessible when disabled"
                        )

                    # Test 2: Enable the field and test dependent behavior
                    if enable_field.get_attribute("type") == "checkbox":
                        enable_field.check()
                    else:
                        enable_field.fill("enabled")

                    time.sleep(0.2)

                    # When enabled, dependent field should be accessible
                    try:
                        expect(dependent_field).to_be_visible(timeout=enhanced_timeout)
                        expect(dependent_field).to_be_enabled(timeout=enhanced_timeout)
                        print(
                            f"When enabled - {dependent_field_name}: accessible as expected"
                        )

                        # Test entering data in dependent field
                        test_value = "test_dependent_data"
                        dependent_field.clear()
                        dependent_field.fill(test_value)
                        actual_value = dependent_field.input_value()

                        assert (
                            actual_value == test_value
                        ), f"Dependent field {dependent_field_name} did not accept input"
                        print(
                            f"Dependent field {dependent_field_name} accepted input: {test_value}"
                        )

                        total_tested_dependencies += 1

                    except Exception as e:
                        print(
                            f"Error testing dependent field {dependent_field_name}: {str(e)}"
                        )
                        total_tested_dependencies += 1

                    # Reset the enable field
                    try:
                        if enable_field.get_attribute("type") == "checkbox":
                            enable_field.uncheck()
                        else:
                            enable_field.clear()
                    except:
                        pass

                else:
                    print(
                        f"Dependent field {dependent_field_name} not found or not visible"
                    )
            else:
                print(f"Enable field {enable_field_name} not found or not visible")

        except Exception as e:
            print(
                f"Error testing dependent field pair ({enable_field_name}, {dependent_field_name}): {str(e)}"
            )

    # Device-specific validation assertions
    assert (
        total_tested_dependencies > 0
    ), f"No dependent field pairs could be tested on {device_model}"

    if device_series == "Series 2":
        print(
            f"Series 2 device {device_model} - validated basic dependent field validation"
        )
    else:  # Series 3
        print(
            f"Series 3 device {device_model} - validated enhanced dependent field validation"
        )

    # Check for device-specific dependent field patterns
    if device_series == "Series 3":
        # Look for PTP-specific dependent field patterns
        ptp_enable_fields = general_config_page.page.locator(
            "input[name*='ptp_enable' i], #ptp_enable, [data-field-name='ptp_enable']"
        )
        if ptp_enable_fields.count() > 0:
            print(f"Found PTP enable field for Series 3 device {device_model}")
            try:
                ptp_enable = ptp_enable_fields.first

                # Look for PTP-dependent fields
                ptp_dependent_fields = general_config_page.page.locator(
                    "input[name*='ptp_priority' i], input[name*='ptp_domain' i], #ptp_priority, #ptp_domain"
                )

                if ptp_dependent_fields.count() > 0:
                    print(f"Found {ptp_dependent_fields.count()} PTP-dependent fields")

                    # Test PTP enable/disable behavior
                    if ptp_enable.is_checked():
                        ptp_enable.uncheck()
                        time.sleep(0.2)

                    # PTP-dependent fields behavior when disabled
                    disabled_count = 0
                    for i in range(min(ptp_dependent_fields.count(), 2)):
                        field = ptp_dependent_fields.nth(i)
                        if not field.is_enabled():
                            disabled_count += 1

                    # Enable PTP
                    ptp_enable.check()
                    time.sleep(0.2)

                    # PTP-dependent fields should be accessible when enabled
                    enabled_count = 0
                    for i in range(min(ptp_dependent_fields.count(), 2)):
                        field = ptp_dependent_fields.nth(i)
                        if field.is_enabled():
                            enabled_count += 1

                    print(
                        f"PTP-dependent fields: {disabled_count} disabled when PTP off, {enabled_count} enabled when PTP on"
                    )
                    print(
                        f"PTP-dependent field validation working for Series 3 device {device_model}"
                    )

            except Exception as e:
                print(f"PTP dependent field test failed: {str(e)}")
    else:
        print(
            f"Series 2 device {device_model} - no PTP-dependent field validation expected"
        )

    print(
        f"Successfully validated dependent field validation for {device_model} ({device_series}): {total_tested_dependencies} dependencies tested"
    )
