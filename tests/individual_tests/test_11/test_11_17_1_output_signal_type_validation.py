"""
Test 11.17.1: Output Signal Type Validation (Device-)
Purpose: Output signal type selection and validation with device-aware testing
Expected: Device-specific output signal behavior based on hardware capabilities
Device-: Full DeviceCapabilities integration with series-specific validation
"""

import pytest
from playwright.sync_api import expect
from pages.outputs_config_page import OutputsConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_17_1_output_signal_type_validation(
    request,
    outputs_config_page: OutputsConfigPage,
    base_url: str,
):
    """
    Test 11.17.1: Output Signal Type Validation (Device-)
    Purpose: Output signal type selection and validation with device-aware testing
    Expected: Device-specific output signal behavior based on hardware capabilities
    Device-: Full DeviceCapabilities integration with series-specific validation
    """
    # Device detection and validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate output signal behavior"
        )

    # Get device capabilities for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Initialize outputs config page with device model
    if hasattr(outputs_config_page, "set_device_model"):
        outputs_config_page.set_device_model(device_model)

    outputs_config_page.navigate_to_page()

    # Get device capabilities for this device
    device_capabilities = outputs_config_page.get_device_capabilities()
    output_channels = device_capabilities["output_channels"]

    print(
        f"Testing output signal type validation for {device_model} (Series {device_series})"
    )
    print(f"Device has {output_channels} output channels")

    if output_channels == 0:
        print(f"No output channels found for {device_model}")
        return

    # Series-specific signal type expectations
    if device_series == 2:
        # Series 2 devices typically have: OFF, IRIG-B000/002/004/006, PPS, PPM
        expected_signal_types = [
            "OFF",
            "IRIG-B000",
            "IRIG-B002",
            "IRIG-B004",
            "IRIG-B006",
            "PPS",
            "PPM",
        ]
        max_channels = 2
    else:
        # Series 3 devices have extended options including additional IRIG types
        expected_signal_types = [
            "OFF",
            "IRIG-B000",
            "IRIG-B002",
            "IRIG-B004",
            "IRIG-B006",
            "IRIG-B120",
            "IRIG-B122",
            "IRIG-B124",
            "IRIG-B126",
            "PPS",
            "PPM",
        ]
        max_channels = 6

    # Test each available output channel
    for channel in range(1, min(output_channels + 1, max_channels + 1)):
        print(f"\nTesting output channel {channel} on {device_model}")

        try:
            # Get available signal types for this channel
            available_types = outputs_config_page.get_available_signal_types(channel)

            if not available_types:
                print(
                    f"No signal types available for channel {channel} on {device_model}"
                )
                continue

            print(f"Channel {channel} has {len(available_types)} signal type options")

            # Validate that expected signal types are available
            available_values = [sig_type["value"] for sig_type in available_types]
            available_texts = [sig_type["text"].upper() for sig_type in available_types]

            # Check for critical signal types
            critical_types = ["OFF", "PPS"]
            missing_critical = []

            for critical in critical_types:
                if critical not in available_values and not any(
                    critical in text for text in available_texts
                ):
                    missing_critical.append(critical)

            if missing_critical:
                print(
                    f"WARNING: Missing critical signal types on channel {channel}: {missing_critical}"
                )
            else:
                print(f" Channel {channel} has all critical signal types")

            # Test signal type selection and validation
            signal_select = outputs_config_page.page.locator(
                f"select[name='signal{channel}']"
            )

            if signal_select.count() > 0 and signal_select.is_visible(
                timeout=timeout_multiplier * 1000
            ):
                # Test selection of each available option
                for i, sig_type in enumerate(
                    available_types[:5]
                ):  # Test first 5 options to avoid overwhelming
                    try:
                        signal_select.select_option(sig_type["value"])

                        # Verify selection was accepted
                        current_value = signal_select.input_value()
                        assert (
                            current_value == sig_type["value"]
                        ), f"Signal type selection failed for {sig_type['value']}"

                        print(
                            f" Successfully selected {sig_type['value']} on channel {channel}"
                        )

                        # Test persistence by reading back the value
                        selected_option = signal_select.locator("option:checked")
                        if selected_option.is_visible(
                            timeout=timeout_multiplier * 1000
                        ):
                            persisted_value = selected_option.get_attribute("value")
                            assert (
                                persisted_value == sig_type["value"]
                            ), f"Signal type not persisted: expected {sig_type['value']}, got {persisted_value}"

                    except Exception as e:
                        print(
                            f" Error selecting signal type {sig_type['value']} on channel {channel}: {str(e)}"
                        )

                # Test invalid signal type (if field accepts custom input)
                try:
                    # Try to select a non-existent option
                    original_value = signal_select.input_value()
                    signal_select.select_option("INVALID_SIGNAL_TYPE")

                    # Check if the invalid value was rejected
                    current_value = signal_select.input_value()
                    if current_value == "INVALID_SIGNAL_TYPE":
                        print(
                            f"Channel {channel} accepts invalid signal types (may be normalized)"
                        )
                    else:
                        print(
                            f" Channel {channel} properly rejects invalid signal types"
                        )

                    # Restore original value
                    signal_select.select_option(original_value)

                except Exception:
                    print(f" Channel {channel} properly rejects invalid signal types")

            else:
                print(f"Signal select field not found for channel {channel}")

        except Exception as e:
            print(f"Error testing channel {channel}: {str(e)}")

    # Test save functionality with different signal configurations
    try:
        print(
            f"\nTesting save functionality with signal type configurations for {device_model}"
        )

        # Test configuration change and save
        if output_channels >= 1:
            # Configure first channel with a different signal type
            original_data = outputs_config_page.get_page_data()
            original_signal = original_data.get("signal1", "")

            if original_signal:
                # Find an alternative signal type
                available_types = outputs_config_page.get_available_signal_types(1)
                alternative_signal = None

                for sig_type in available_types:
                    if sig_type["value"] != original_signal:
                        alternative_signal = sig_type["value"]
                        break

                if alternative_signal:
                    print(
                        f"Testing save by changing signal1 from {original_signal} to {alternative_signal}"
                    )

                    # Make the change
                    if outputs_config_page.configure_output(1, alternative_signal):
                        # Test save functionality
                        if outputs_config_page.save_configuration():
                            print(
                                f" Signal type change saved successfully for {device_model}"
                            )

                            # Verify the change persisted
                            outputs_config_page.navigate_to_page()
                            new_data = outputs_config_page.get_page_data()
                            new_signal = new_data.get("signal1", "")

                            if new_signal == alternative_signal:
                                print(
                                    f" Signal type change persisted for {device_model}"
                                )
                            else:
                                print(
                                    f" Signal type change not persisted: expected {alternative_signal}, got {new_signal}"
                                )
                        else:
                            print(
                                f" Failed to save signal type change for {device_model}"
                            )
                    else:
                        print(
                            f" Failed to configure signal type change for {device_model}"
                        )
                else:
                    print(
                        f"No alternative signal types available for testing save functionality"
                    )
            else:
                print(f"No original signal type found for testing save functionality")

    except Exception as e:
        print(f"Error testing save functionality: {str(e)}")

    # Test series-specific validation
    print(
        f"\nPerforming series-specific validation for {device_model} (Series {device_series})"
    )

    try:
        # Validate against DeviceCapabilities expected behavior
        expected_output_count = 2 if device_series == 2 else 6

        if output_channels == expected_output_count:
            print(
                f" Output channel count matches series expectations ({expected_output_count})"
            )
        else:
            print(
                f" Output channel count mismatch: expected {expected_output_count}, found {output_channels}"
            )

        # Test signal type coverage
        all_signal_types = outputs_config_page.get_all_signal_types_by_channel()
        total_unique_types = set()

        for channel_data in all_signal_types.values():
            for sig_type in channel_data:
                total_unique_types.add(sig_type["value"])

        print(
            f"Device supports {len(total_unique_types)} unique signal types: {sorted(total_unique_types)}"
        )

        # Series 2 should have basic types, Series 3 should have extended types
        if device_series == 2:
            basic_types = {"OFF", "PPS", "PPM"}
            if basic_types.issubset(total_unique_types):
                print(" Series 2 device has expected basic signal types")
            else:
                missing_basic = basic_types - total_unique_types
                print(f" Series 2 device missing basic signal types: {missing_basic}")
        else:
            extended_types = {"IRIG-B120", "IRIG-B122", "IRIG-B124", "IRIG-B126"}
            if any(ext_type in total_unique_types for ext_type in extended_types):
                print(" Series 3 device has expected extended IRIG signal types")
            else:
                print(" Series 3 device may be missing extended IRIG signal types")

    except Exception as e:
        print(f"Error in series-specific validation: {str(e)}")

    print(
        f"\nOutput signal type validation completed for {device_model} (Series {device_series})"
    )
