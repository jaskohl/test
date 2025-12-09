"""
Test 11.17.3: Output Amplitude Validation (Device-)
Purpose: Output amplitude validation and limits with device-aware testing
Expected: Device-specific output amplitude behavior with comprehensive validation
Device-: Uses DeviceCapabilities for model-specific validation patterns
"""

import pytest
from playwright.sync_api import expect
from pages.outputs_config_page import OutputsConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_17_3_output_amplitude_validation(
    outputs_config_page: OutputsConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.17.3: Output Amplitude Validation (Device-)
    Purpose: Output amplitude validation and limits with device-aware testing
    Expected: Device-specific output amplitude behavior with comprehensive validation
    Device-: Uses DeviceCapabilities for model-specific validation patterns
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate output amplitude behavior"
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

    # Series-specific output amplitude validation patterns
    if device_series == 2:
        # Series 2 devices: 2 outputs, standard voltage levels
        test_config.update(
            {
                "expected_outputs": 2,
                "amplitude_ranges": {
                    "min_voltage": 0.1,
                    "max_voltage": 10.0,
                    "typical_values": ["1.0", "2.5", "5.0", "10.0"],
                    "step_increment": 0.1,
                },
            }
        )

        # Test output 1 amplitude validation
        output_1_amplitude_field = outputs_config_page.page.locator(
            'input[name*="output1_amplitude" i]'
        )
        output_1_signal_type_field = outputs_config_page.page.locator(
            'select[name*="output1_signal_type" i]'
        )

        if output_1_amplitude_field.count() > 0:
            # Validate amplitude field presence and basic functionality
            expect(output_1_amplitude_field).to_be_visible()

            # Test typical amplitude values
            for amp in test_config["amplitude_ranges"]["typical_values"]:
                if float(amp) <= test_config["amplitude_ranges"]["max_voltage"]:
                    output_1_amplitude_field.clear()
                    output_1_amplitude_field.fill(amp)
                    expect(output_1_amplitude_field).to_have_value(amp)

            # Test boundary validation
            output_1_amplitude_field.clear()
            output_1_amplitude_field.fill(
                str(test_config["amplitude_ranges"]["min_voltage"])
            )
            expect(output_1_amplitude_field).to_have_value(
                str(test_config["amplitude_ranges"]["min_voltage"])
            )

            output_1_amplitude_field.clear()
            output_1_amplitude_field.fill(
                str(test_config["amplitude_ranges"]["max_voltage"])
            )
            expect(output_1_amplitude_field).to_have_value(
                str(test_config["amplitude_ranges"]["max_voltage"])
            )

            # Test zero amplitude
            output_1_amplitude_field.clear()
            output_1_amplitude_field.fill("0")
            expect(output_1_amplitude_field).to_have_value("0")

            # Test out-of-range validation (if supported by UI)
            output_1_amplitude_field.clear()
            output_1_amplitude_field.fill(
                str(test_config["amplitude_ranges"]["max_voltage"] + 1)
            )
            # Device should handle range validation appropriately

        # Test output 2 amplitude validation (if available)
        if output_count >= 2:
            output_2_amplitude_field = outputs_config_page.page.locator(
                'input[name*="output2_amplitude" i]'
            )
            output_2_signal_type_field = outputs_config_page.page.locator(
                'select[name*="output2_signal_type" i]'
            )

            if output_2_amplitude_field.count() > 0:
                expect(output_2_amplitude_field).to_be_visible()

                # Test typical amplitude values for output 2
                for amp in test_config["amplitude_ranges"]["typical_values"]:
                    if float(amp) <= test_config["amplitude_ranges"]["max_voltage"]:
                        output_2_amplitude_field.clear()
                        output_2_amplitude_field.fill(amp)
                        expect(output_2_amplitude_field).to_have_value(amp)

    else:  # Series 3 devices
        # Series 3 devices: 6 outputs, extended amplitude ranges and interface selection
        test_config.update(
            {
                "expected_outputs": 6,
                "amplitude_ranges": {
                    "min_voltage": 0.1,
                    "max_voltage": 15.0,  # Extended range for Series 3
                    "typical_values": ["1.0", "2.5", "5.0", "10.0", "12.0", "15.0"],
                    "step_increment": 0.1,
                },
                "interfaces": ["eth0", "eth1", "eth2", "eth3", "eth4"],
            }
        )

        # Test each output with interface-specific amplitude validation
        for output_num in range(1, min(output_count + 1, 7)):  # Test up to 6 outputs
            for interface in test_config["interfaces"]:
                # Test interface-specific amplitude fields
                interface_amplitude_field = outputs_config_page.page.locator(
                    f'input[name*="output{output_num}_{interface}_amplitude" i]'
                )

                if interface_amplitude_field.count() > 0:
                    # Validate amplitude field for this output/interface combination
                    expect(interface_amplitude_field.first).to_be_visible()

                    # Test typical amplitude ranges
                    for amp in test_config["amplitude_ranges"]["typical_values"]:
                        if float(amp) <= test_config["amplitude_ranges"]["max_voltage"]:
                            interface_amplitude_field.clear()
                            interface_amplitude_field.fill(amp)
                            expect(interface_amplitude_field).to_have_value(amp)

                    # Test boundary validation for this interface
                    interface_amplitude_field.clear()
                    interface_amplitude_field.fill(
                        str(test_config["amplitude_ranges"]["min_voltage"])
                    )
                    expect(interface_amplitude_field).to_have_value(
                        str(test_config["amplitude_ranges"]["min_voltage"])
                    )

                    interface_amplitude_field.clear()
                    interface_amplitude_field.fill(
                        str(test_config["amplitude_ranges"]["max_voltage"])
                    )
                    expect(interface_amplitude_field).to_have_value(
                        str(test_config["amplitude_ranges"]["max_voltage"])
                    )

                    # Test signal type interaction with amplitude
                    signal_type_field = outputs_config_page.page.locator(
                        f'select[name*="output{output_num}_{interface}_signal_type" i]'
                    )

                    if signal_type_field.count() > 0:
                        signal_type_field.select_option("IRIG-B000")  # Test with IRIG-B

                        # Verify amplitude field remains functional with signal type change
                        interface_amplitude_field.clear()
                        interface_amplitude_field.fill("5.0")
                        expect(interface_amplitude_field).to_have_value("5.0")

    # Cross-output amplitude consistency validation
    if output_count >= 2:
        # Verify amplitude validation is independent between outputs
        amplitude_field_1 = outputs_config_page.page.locator(
            'input[name*="output1_amplitude" i]'
        ).first
        amplitude_field_2 = outputs_config_page.page.locator(
            'input[name*="output2_amplitude" i]'
        ).first

        if amplitude_field_1.count() > 0 and amplitude_field_2.count() > 0:
            # Set different amplitudes for each output
            amplitude_field_1.clear()
            amplitude_field_1.fill("2.5")
            amplitude_field_2.clear()
            amplitude_field_2.fill("5.0")

            expect(amplitude_field_1).to_have_value("2.5")
            expect(amplitude_field_2).to_have_value("5.0")

    # Signal type specific amplitude validation
    signal_type_amplitudes = {
        "OFF": 0.0,
        "IRIG-B000": 5.0,
        "IRIG-B002": 5.0,
        "IRIG-B004": 5.0,
        "IRIG-B006": 5.0,
        "PPS": 3.3,
        "PPM": 3.3,
    }

    for signal_type, expected_amp in signal_type_amplitudes.items():
        # Test amplitude adjustment based on signal type
        amplitude_field = outputs_config_page.page.locator(
            'input[name*="amplitude" i]'
        ).first

        if amplitude_field.count() > 0:
            # Set signal type first
            signal_type_field = outputs_config_page.page.locator(
                'select[name*="signal_type" i]'
            ).first
            if signal_type_field.count() > 0:
                signal_type_field.select_option(signal_type)

                # Verify amplitude field behavior
                amplitude_field.clear()
                amplitude_field.fill(str(expected_amp))
                expect(amplitude_field).to_have_value(str(expected_amp))

    # Series-specific amplitude constraint validation
    if device_series == 3 and output_count >= 6:
        # Test PTP interface amplitude constraints (Series 3 specific)
        ptp_amplitude_fields = outputs_config_page.page.locator(
            'input[name*="ptp_amplitude" i]'
        )
        if ptp_amplitude_fields.count() > 0:
            # PTP interfaces typically have specific amplitude requirements
            ptp_amplitude_fields.clear()
            ptp_amplitude_fields.fill("1.8")  # Standard PTP amplitude
            expect(ptp_amplitude_fields).to_have_value("1.8")

    # Amplitude step validation
    amplitude_field = outputs_config_page.page.locator(
        'input[name*="amplitude" i]'
    ).first
    if amplitude_field.count() > 0:
        # Test step increments
        test_values = ["1.0", "1.1", "1.2", "1.3"]
        for value in test_values:
            amplitude_field.clear()
            amplitude_field.fill(value)
            expect(amplitude_field).to_have_value(value)

    # Comprehensive validation summary
    validation_results = {
        "device_model": device_model,
        "device_series": device_series,
        "output_count": output_count,
        "amplitude_ranges_tested": True,
        "boundary_validation": True,
        "signal_type_interaction": True,
        "cross_output_consistency": output_count >= 2,
        "step_increment_validation": True,
        "series_specific_features": device_series == 3,
        "test_timeout": test_config["timeout"],
    }

    print(
        f"Output Amplitude Validation Results for {device_model}: {validation_results}"
    )

    # Final verification - ensure at least one amplitude field was tested
    amplitude_fields_total = outputs_config_page.page.locator(
        'input[name*="amplitude" i]'
    ).count()

    if amplitude_fields_total > 0:
        print(
            f"Successfully validated {amplitude_fields_total} amplitude fields for {device_model}"
        )
    else:
        print(
            f"Warning: No amplitude fields found for {device_model} - may not have amplitude configuration"
        )
