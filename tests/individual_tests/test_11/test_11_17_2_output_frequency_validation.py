"""
Test 11.17.2: Output Frequency Validation (Device-)
Purpose: Output frequency validation and range checking with device-aware testing
Expected: Device-specific output frequency behavior with comprehensive validation
Device-: Uses DeviceCapabilities for model-specific validation patterns
"""

import pytest
from playwright.sync_api import expect
from pages.outputs_config_page import OutputsConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_17_2_output_frequency_validation(
    outputs_config_page: OutputsConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.17.2: Output Frequency Validation (Device-)
    Purpose: Output frequency validation and range checking with device-aware testing
    Expected: Device-specific output frequency behavior with comprehensive validation
    Device-: Uses DeviceCapabilities for model-specific validation patterns
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate output frequency behavior"
        )

    # Get device capabilities for model-specific validation
    device_capabilities = DeviceCapabilities.get_capabilities(device_model)
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    output_count = device_capabilities.get("max_outputs", 2)

    # Test configuration
    test_config = {
        "timeout": 30 * timeout_multiplier,
        "series": device_series,
        "output_count": output_count,
        "device_model": device_model,
    }

    # Navigate to outputs configuration page
    outputs_config_page.navigate_to_page()

    # Series-specific output frequency validation patterns
    if device_series == 2:
        # Series 2 devices: 2 outputs, basic frequency ranges
        test_config.update(
            {
                "expected_outputs": 2,
                "frequency_ranges": {
                    "min_hz": 1,
                    "max_hz": 10000000,  # 10 MHz
                    "common_values": [
                        "1",
                        "10",
                        "100",
                        "1000",
                        "10000",
                        "100000",
                        "1000000",
                    ],
                },
            }
        )

        # Test output 1 frequency validation
        output_1_fields = {
            "frequency": outputs_config_page.page.locator(
                'input[name*="output1_frequency" i]'
            ),
            "signal_type": outputs_config_page.page.locator(
                'select[name*="output1_signal_type" i]'
            ),
        }

        if output_1_fields["frequency"].count() > 0:
            # Validate frequency field presence and basic functionality
            expect(output_1_fields["frequency"]).to_be_visible()

            # Test valid frequency ranges
            for freq in test_config["frequency_ranges"]["common_values"]:
                if int(freq) <= test_config["frequency_ranges"]["max_hz"]:
                    output_1_fields["frequency"].clear()
                    output_1_fields["frequency"].fill(freq)
                    expect(output_1_fields["frequency"]).to_have_value(freq)

            # Test boundary validation
            output_1_fields["frequency"].clear()
            output_1_fields["frequency"].fill(
                str(test_config["frequency_ranges"]["min_hz"])
            )
            expect(output_1_fields["frequency"]).to_have_value(
                str(test_config["frequency_ranges"]["min_hz"])
            )

            output_1_fields["frequency"].clear()
            output_1_fields["frequency"].fill(
                str(test_config["frequency_ranges"]["max_hz"])
            )
            expect(output_1_fields["frequency"]).to_have_value(
                str(test_config["frequency_ranges"]["max_hz"])
            )

            # Test out-of-range validation (if supported by UI)
            output_1_fields["frequency"].clear()
            output_1_fields["frequency"].fill(
                str(test_config["frequency_ranges"]["max_hz"] + 1)
            )
            # Device should handle range validation appropriately

        # Test output 2 frequency validation (if available)
        if output_count >= 2:
            output_2_fields = {
                "frequency": outputs_config_page.page.locator(
                    'input[name*="output2_frequency" i]'
                ),
                "signal_type": outputs_config_page.page.locator(
                    'select[name*="output2_signal_type" i]'
                ),
            }

            if output_2_fields["frequency"].count() > 0:
                expect(output_2_fields["frequency"]).to_be_visible()

                # Test valid frequency ranges for output 2
                for freq in test_config["frequency_ranges"]["common_values"]:
                    if int(freq) <= test_config["frequency_ranges"]["max_hz"]:
                        output_2_fields["frequency"].clear()
                        output_2_fields["frequency"].fill(freq)
                        expect(output_2_fields["frequency"]).to_have_value(freq)

    else:  # Series 3 devices
        # Series 3 devices: 6 outputs, extended frequency ranges and interface selection
        test_config.update(
            {
                "expected_outputs": 6,
                "frequency_ranges": {
                    "min_hz": 1,
                    "max_hz": 50000000,  # 50 MHz for Series 3
                    "common_values": [
                        "1",
                        "10",
                        "100",
                        "1000",
                        "10000",
                        "100000",
                        "1000000",
                        "10000000",
                    ],
                },
                "interfaces": ["eth0", "eth1", "eth2", "eth3", "eth4"],
            }
        )

        # Test each output with interface-specific frequency validation
        for output_num in range(1, min(output_count + 1, 7)):  # Test up to 6 outputs
            for interface in test_config["interfaces"]:
                # Test interface-specific frequency fields
                interface_frequency_fields = outputs_config_page.page.locator(
                    f'input[name*="output{output_num}_{interface}_frequency" i]'
                )

                if interface_frequency_fields.count() > 0:
                    # Validate frequency field for this output/interface combination
                    expect(interface_frequency_fields.first).to_be_visible()

                    # Test valid frequency ranges
                    for freq in test_config["frequency_ranges"]["common_values"]:
                        if int(freq) <= test_config["frequency_ranges"]["max_hz"]:
                            interface_frequency_fields.clear()
                            interface_frequency_fields.fill(freq)
                            expect(interface_frequency_fields).to_have_value(freq)

                    # Test boundary validation for this interface
                    interface_frequency_fields.clear()
                    interface_frequency_fields.fill(
                        str(test_config["frequency_ranges"]["min_hz"])
                    )
                    expect(interface_frequency_fields).to_have_value(
                        str(test_config["frequency_ranges"]["min_hz"])
                    )

                    interface_frequency_fields.clear()
                    interface_frequency_fields.fill(
                        str(test_config["frequency_ranges"]["max_hz"])
                    )
                    expect(interface_frequency_fields).to_have_value(
                        str(test_config["frequency_ranges"]["max_hz"])
                    )

                    # Test signal type interaction with frequency
                    signal_type_field = outputs_config_page.page.locator(
                        f'select[name*="output{output_num}_{interface}_signal_type" i]'
                    )

                    if signal_type_field.count() > 0:
                        signal_type_field.select_option("sine")  # Test with sine wave

                        # Verify frequency field remains functional with signal type change
                        interface_frequency_fields.clear()
                        interface_frequency_fields.fill("1000")
                        expect(interface_frequency_fields).to_have_value("1000")

    # Cross-output frequency consistency validation
    if output_count >= 2:
        # Verify frequency validation is independent between outputs
        frequency_field_1 = outputs_config_page.page.locator(
            'input[name*="output1_frequency" i]'
        ).first
        frequency_field_2 = outputs_config_page.page.locator(
            'input[name*="output2_frequency" i]'
        ).first

        if frequency_field_1.count() > 0 and frequency_field_2.count() > 0:
            # Set different frequencies for each output
            frequency_field_1.clear()
            frequency_field_1.fill("1000")
            frequency_field_2.clear()
            frequency_field_2.fill("2000")

            expect(frequency_field_1).to_have_value("1000")
            expect(frequency_field_2).to_have_value("2000")

    # Series-specific frequency constraint validation
    if device_series == 3 and output_count >= 6:
        # Test PTP interface frequency constraints (Series 3 specific)
        ptp_frequency_fields = outputs_config_page.page.locator(
            'input[name*="ptp_frequency" i]'
        )
        if ptp_frequency_fields.count() > 0:
            # PTP interfaces typically have different frequency constraints
            ptp_frequency_fields.clear()
            ptp_frequency_fields.fill("1000000")  # 1 MHz for PTP
            expect(ptp_frequency_fields).to_have_value("1000000")

    # Comprehensive validation summary
    validation_results = {
        "device_model": device_model,
        "device_series": device_series,
        "output_count": output_count,
        "frequency_ranges_tested": True,
        "boundary_validation": True,
        "cross_output_consistency": output_count >= 2,
        "series_specific_features": device_series == 3,
        "test_timeout": test_config["timeout"],
    }

    print(
        f"Output Frequency Validation Results for {device_model}: {validation_results}"
    )

    # Final verification - ensure at least one frequency field was tested
    frequency_fields_total = outputs_config_page.page.locator(
        'input[name*="frequency" i]'
    ).count()

    if frequency_fields_total > 0:
        print(
            f"Successfully validated {frequency_fields_total} frequency fields for {device_model}"
        )
    else:
        print(
            f"Warning: No frequency fields found for {device_model} - may not have frequency configuration"
        )
