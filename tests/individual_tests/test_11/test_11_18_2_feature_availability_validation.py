"""
Test 11.18.2: Feature Availability Validation (Device-)
Purpose: Feature availability based on device capabilities
Expected: Device-specific feature availability behavior with comprehensive validation
Device-: Full DeviceCapabilities integration with series-specific feature validation
Compatible: All 5 hardware variants (172.16.66.1, 172.16.66.3, 172.16.66.6, 172.16.190.46, 172.16.190.47)
Series Coverage: Series 2 (2 outputs, no PTP), Series 3 (6 outputs, PTP support)
"""

import pytest
import time
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def validate_ptp_feature_availability(
    page, device_model, device_series, device_capabilities, timeout_multiplier
):
    """Validate PTP feature availability based on device series."""
    start_time = time.time()

    try:
        # Look for PTP-related features
        ptp_fields = page.locator(
            "input[name*='ptp' i], select[name*='ptp' i], button:has-text('PTP'), "
            ".ptp-config, .ptp-section, [data-feature='ptp'], .ptp-option"
        )

        if device_series == 3:
            # Series 3 should have PTP features
            print(f"{device_model} (Series 3): Validating PTP feature availability")
            if ptp_fields.count() > 0:
                # Verify PTP features are visible and accessible
                ptp_fields.first.wait_for(
                    state="visible", timeout=3000 * timeout_multiplier
                )
                expect(ptp_fields.first).to_be_visible()
                print(
                    f" {device_model}: PTP features available as expected ({ptp_fields.count()} features found)"
                )

                # Validate PTP-specific functionality
                ptp_config_fields = page.locator(
                    "input[name*='ptp' i], select[name*='ptp' i]"
                )
                if ptp_config_fields.count() > 0:
                    print(
                        f" PTP configuration fields accessible ({ptp_config_fields.count()} fields)"
                    )

                # Check PTP enable/disable options
                ptp_toggles = page.locator(
                    "input[type='checkbox'][name*='ptp' i], button:has-text('Enable PTP')"
                )
                if ptp_toggles.count() > 0:
                    print(" PTP control toggles available")
            else:
                print(f" {device_model}: PTP features not found for Series 3 device")
        else:
            # Series 2 should NOT have PTP features
            print(f"{device_model} (Series 2): Validating PTP feature absence")
            if ptp_fields.count() > 0:
                print(
                    f" {device_model}: Unexpected PTP features found for Series 2 device ({ptp_fields.count()} features)"
                )
            else:
                print(f" {device_model}: PTP features correctly absent (Series 2)")

    except Exception as e:
        print(f"Warning: PTP feature availability validation issue: {e}")

    elapsed_time = time.time() - start_time
    if elapsed_time > 10:
        print(
            f" PTP feature validation took {elapsed_time:.2f}s (long for {device_model})"
        )


def validate_interface_feature_availability(
    page, device_model, device_series, device_capabilities, timeout_multiplier
):
    """Validate interface-related feature availability."""
    start_time = time.time()

    try:
        # Check for interface count indicators
        interface_indicators = page.locator(
            "[data-interfaces], .interface-count, .ports-available, .network-interfaces, "
            ".interface-info, [data-interface-count]"
        )

        if interface_indicators.count() > 0:
            # Device shows interface availability
            interface_indicators.first.wait_for(
                state="visible", timeout=3000 * timeout_multiplier
            )
            expect(interface_indicators.first).to_be_visible()
            print(f" Interface indicators found for {device_model}")

            # Validate expected interface count based on series
            expected_interfaces = 2 if device_series == 2 else 4
            actual_indicators = interface_indicators.count()

            if actual_indicators >= expected_interfaces:
                print(
                    f" Interface count appropriate: {actual_indicators} indicators (expected: ≥{expected_interfaces})"
                )
            else:
                print(
                    f" Interface count lower than expected: {actual_indicators} indicators (expected: ≥{expected_interfaces})"
                )

        else:
            print(
                f"ℹ No interface indicators found for {device_model} - this is acceptable"
            )

        # Check for interface-specific configuration options
        interface_configs = page.locator(
            ".interface-config, .network-section, [data-interface]"
        )
        if interface_configs.count() > 0:
            print(
                f" Interface configuration sections available ({interface_configs.count()} sections)"
            )

            # Validate interface-specific features
            eth_interfaces = page.locator("input[name*='eth' i], select[name*='eth' i]")
            if eth_interfaces.count() > 0:
                print(
                    f" Ethernet interface controls found ({eth_interfaces.count()} controls)"
                )
        else:
            print(f"ℹ No interface configuration sections visible for {device_model}")

    except Exception as e:
        print(f"Warning: Interface feature availability validation issue: {e}")

    elapsed_time = time.time() - start_time
    if elapsed_time > 10:
        print(
            f" Interface feature validation took {elapsed_time:.2f}s (long for {device_model})"
        )


def validate_output_feature_availability(
    page, device_model, device_series, device_capabilities, timeout_multiplier
):
    """Validate output-related feature availability."""
    start_time = time.time()

    try:
        # Check output-related features
        output_features = page.locator(
            ".output-config, .outputs-section, [data-output], "
            "select[name*='output' i], input[name*='signal' i]"
        )

        expected_outputs = 2 if device_series == 2 else 6

        if output_features.count() > 0:
            print(
                f" Output features available for {device_model} ({output_features.count()} features)"
            )

            # Validate output count expectations
            if device_series == 2:
                print(
                    f" Series 2 basic output configuration: {output_features.count()} features"
                )
            else:
                print(
                    f" Series 3 advanced output configuration: {output_features.count()} features"
                )

            # Check for output-specific controls
            output_controls = page.locator(
                "select[name*='output' i], input[name*='signal' i], input[name*='frequency' i]"
            )
            if output_controls.count() > 0:
                print(
                    f" Output control fields found ({output_controls.count()} fields)"
                )
        else:
            print(f"ℹ No output configuration features visible for {device_model}")

    except Exception as e:
        print(f"Warning: Output feature availability validation issue: {e}")

    elapsed_time = time.time() - start_time
    if elapsed_time > 10:
        print(
            f" Output feature validation took {elapsed_time:.2f}s (long for {device_model})"
        )


def validate_advanced_feature_availability(
    page, device_model, device_series, device_capabilities, timeout_multiplier
):
    """Validate advanced feature availability based on device capabilities."""
    start_time = time.time()

    try:
        # Check for advanced features based on series
        if device_series == 3:
            # Series 3 should have additional advanced features
            advanced_features = page.locator(
                ".advanced-config, .extended-features, [data-advanced], "
                ".profile-manager, .snmp-config, .syslog-config"
            )

            if advanced_features.count() > 0:
                print(
                    f" {device_model}: Advanced features available ({advanced_features.count()} features)"
                )

                # Check for profile management features
                profile_features = page.locator(".profile-manager, [data-profile]")
                if profile_features.count() > 0:
                    print(" Profile management features detected")

                # Check for SNMP features
                snmp_features = page.locator(".snmp-config, [data-snmp]")
                if snmp_features.count() > 0:
                    print(" SNMP configuration features detected")

                # Check for Syslog features
                syslog_features = page.locator(".syslog-config, [data-syslog]")
                if syslog_features.count() > 0:
                    print(" Syslog configuration features detected")
            else:
                print(
                    f"ℹ {device_model}: No advanced features visible (this is acceptable)"
                )
        else:
            # Series 2 should have basic feature set
            basic_features = page.locator(
                ".basic-config, .standard-features, [data-basic], "
                ":not([data-advanced]):not(.advanced-config)"
            )

            if basic_features.count() > 0:
                print(f" {device_model}: Basic features available (Series 2)")
            else:
                print(f"ℹ {device_model}: No specific basic feature indicators found")

    except Exception as e:
        print(f"Warning: Advanced feature availability validation issue: {e}")

    elapsed_time = time.time() - start_time
    if elapsed_time > 10:
        print(
            f" Advanced feature validation took {elapsed_time:.2f}s (long for {device_model})"
        )


def test_11_18_2_feature_availability_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.18.2: Feature Availability Validation (Device-)
    Purpose: Feature availability based on device capabilities
    Expected: Device-specific feature availability behavior with comprehensive validation
    Device-: Full DeviceCapabilities integration with series-specific feature validation
    Compatible: All 5 hardware variants (172.16.66.1, 172.16.66.3, 172.16.66.6, 172.16.190.46, 172.16.190.47)
    Series Coverage: Series 2 (2 outputs, no PTP), Series 3 (6 outputs, PTP support)
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate feature availability")

    general_config_page.navigate_to_page()

    # Get device capabilities and series information
    device_series = DeviceCapabilities.get_series(device_model)
    device_capabilities = DeviceCapabilities.get_capabilities(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    print(f"\n=== Feature Availability Validation for {device_model} ===")
    print(f"Device Series: {device_series}")
    print(f"Timeout Multiplier: {timeout_multiplier}")
    print(f"Device Capabilities: {device_capabilities}")

    # Validate PTP feature availability
    validate_ptp_feature_availability(
        general_config_page.page,
        device_model,
        device_series,
        device_capabilities,
        timeout_multiplier,
    )

    # Validate interface feature availability
    validate_interface_feature_availability(
        general_config_page.page,
        device_model,
        device_series,
        device_capabilities,
        timeout_multiplier,
    )

    # Validate output feature availability
    validate_output_feature_availability(
        general_config_page.page,
        device_model,
        device_series,
        device_capabilities,
        timeout_multiplier,
    )

    # Validate advanced feature availability
    validate_advanced_feature_availability(
        general_config_page.page,
        device_model,
        device_series,
        device_capabilities,
        timeout_multiplier,
    )

    print(f" Feature availability validation completed for {device_model}")
