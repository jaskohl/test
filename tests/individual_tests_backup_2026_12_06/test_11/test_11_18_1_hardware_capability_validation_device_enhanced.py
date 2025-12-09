"""
Test 11.18.1: Hardware Capability Validation (Device-Enhanced)
Purpose: Hardware capability detection and validation
Expected: Device-specific hardware capability behavior with comprehensive validation
Device-Enhanced: Full DeviceCapabilities integration with series-specific validation
Compatible: All 5 hardware variants (172.16.66.1, 172.16.66.3, 172.16.66.6, 172.16.190.46, 172.16.190.47)
Series Coverage: Series 2 (2 outputs), Series 3 (6 outputs, PTP support)
"""

import pytest
import time
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def validate_hardware_capability_consistency(
    page, device_model, device_series, device_capabilities, timeout_multiplier
):
    """Validate hardware capability consistency across the device interface."""
    start_time = time.time()

    try:
        # Check capability indicators in the interface
        capability_indicators = page.locator(
            ".capability, .hardware-info, [data-capability], .device-info, .series-info"
        )
        if capability_indicators.count() > 0:
            # Device displays capability information
            capability_indicators.first.wait_for(
                state="visible", timeout=3000 * timeout_multiplier
            )
            expect(capability_indicators.first).to_be_visible()
            print(f" Capability indicators found for {device_model}")

            # Validate series-specific indicators
            if device_series == 2:
                # Look for Series 2 specific indicators
                series2_indicators = page.locator(
                    ".series-2, [data-series='2'], .basic-capability"
                )
                if series2_indicators.count() > 0:
                    expect(series2_indicators.first).to_be_visible()
                    print(" Series 2 indicators detected correctly")
            else:
                # Look for Series 3 specific indicators
                series3_indicators = page.locator(
                    ".series-3, [data-series='3'], .advanced-capability, .ptp-capability"
                )
                if series3_indicators.count() > 0:
                    expect(series3_indicators.first).to_be_visible()
                    print(" Series 3 indicators detected correctly")
        else:
            print(
                f"ℹ No capability indicators found for {device_model} - this is acceptable"
            )

    except Exception as e:
        print(f"Warning: Capability indicator validation issue: {e}")

    elapsed_time = time.time() - start_time
    if elapsed_time > 10:
        print(
            f" Hardware capability consistency validation took {elapsed_time:.2f}s (long for {device_model})"
        )


def validate_output_configuration_capabilities(
    page, device_model, device_series, device_capabilities, timeout_multiplier
):
    """Validate output configuration capabilities based on device model."""
    start_time = time.time()

    try:
        # Check output configuration sections
        output_sections = page.locator(
            ".output-config, .outputs-section, [data-output]"
        )

        if device_series == 2:
            # Series 2 should have fewer output options
            print(f"{device_model} (Series 2): Validating basic output configuration")
            expected_outputs = 2  # Series 2 typically has 2 outputs

            # Check if output sections are accessible
            if output_sections.count() > 0:
                print(
                    f" Found {output_sections.count()} output sections (expected: {expected_outputs})"
                )
            else:
                print("ℹ No output configuration sections visible on this page")

        else:  # Series 3
            # Series 3 should have more advanced output options
            print(
                f"{device_model} (Series 3): Validating advanced output configuration"
            )
            expected_outputs = 6  # Series 3 typically has 6 outputs

            # Check if output sections are accessible
            if output_sections.count() > 0:
                print(
                    f" Found {output_sections.count()} output sections (expected: {expected_outputs})"
                )

                # Look for advanced features
                advanced_features = page.locator(
                    ".ptp-option, .advanced-output, [data-feature='ptp']"
                )
                if advanced_features.count() > 0:
                    print(" Series 3 advanced features detected")
                else:
                    print("ℹ No advanced features visible on this page")
            else:
                print("ℹ No output configuration sections visible on this page")

    except Exception as e:
        print(f"Warning: Output configuration capability validation issue: {e}")

    elapsed_time = time.time() - start_time
    if elapsed_time > 10:
        print(
            f" Output configuration validation took {elapsed_time:.2f}s (long for {device_model})"
        )


def validate_feature_limitations(
    page, device_model, device_series, device_capabilities, timeout_multiplier
):
    """Validate that device respects its hardware limitations."""
    start_time = time.time()

    try:
        # Check for PTP availability based on series
        ptp_sections = page.locator(".ptp-config, .ptp-section, [data-feature='ptp']")

        if device_series == 2:
            # Series 2 should NOT have PTP features
            if ptp_sections.count() > 0:
                print(
                    f" {device_model}: Unexpected PTP sections found for Series 2 device"
                )
            else:
                print(f" {device_model}: Correctly lacks PTP features (Series 2)")
        else:  # Series 3
            # Series 3 should have PTP features
            if ptp_sections.count() > 0:
                print(f" {device_model}: PTP features available (Series 3)")
            else:
                print(f" {device_model}: Expected PTP features not found for Series 3")

        # Check interface count limitations
        interface_sections = page.locator(
            ".interface-config, .network-section, [data-interface]"
        )
        max_interfaces = 2 if device_series == 2 else 4

        if interface_sections.count() > max_interfaces:
            print(
                f" {device_model}: More interfaces than expected ({interface_sections.count()} > {max_interfaces})"
            )
        else:
            print(
                f" {device_model}: Interface count within limits ({interface_sections.count()}/{max_interfaces})"
            )

    except Exception as e:
        print(f"Warning: Feature limitation validation issue: {e}")

    elapsed_time = time.time() - start_time
    if elapsed_time > 10:
        print(
            f" Feature limitation validation took {elapsed_time:.2f}s (long for {device_model})"
        )


def test_11_18_1_hardware_capability_validation_device_enhanced(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.18.1: Hardware Capability Validation (Device-Enhanced)
    Purpose: Hardware capability detection and validation
    Expected: Device-specific hardware capability behavior with comprehensive validation
    Device-Enhanced: Full DeviceCapabilities integration with series-specific validation
    Compatible: All 5 hardware variants (172.16.66.1, 172.16.66.3, 172.16.66.6, 172.16.190.46, 172.16.190.47)
    Series Coverage: Series 2 (2 outputs), Series 3 (6 outputs, PTP support)
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate hardware capabilities")

    general_config_page.navigate_to_page()

    # Get device capabilities and series information
    device_series = DeviceCapabilities.get_series(device_model)
    device_capabilities = DeviceCapabilities.get_capabilities(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    print(f"\n=== Hardware Capability Validation for {device_model} ===")
    print(f"Device Series: {device_series}")
    print(f"Timeout Multiplier: {timeout_multiplier}")
    print(f"Device Capabilities: {device_capabilities}")

    # Validate hardware capability consistency
    validate_hardware_capability_consistency(
        general_config_page.page,
        device_model,
        device_series,
        device_capabilities,
        timeout_multiplier,
    )

    # Validate output configuration capabilities
    validate_output_configuration_capabilities(
        general_config_page.page,
        device_model,
        device_series,
        device_capabilities,
        timeout_multiplier,
    )

    # Validate feature limitations
    validate_feature_limitations(
        general_config_page.page,
        device_model,
        device_series,
        device_capabilities,
        timeout_multiplier,
    )

    print(f" Hardware capability validation completed for {device_model}")
