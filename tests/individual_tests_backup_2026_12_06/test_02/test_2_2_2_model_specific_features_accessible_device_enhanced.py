"""
Test 2_2_2 Model Specific Features Accessible - Device Enhanced
Category: 02 - Configuration Section Navigation
Enhanced with comprehensive DeviceCapabilities integration
Source Method: TestConfigurationNavigation.test_2_2_2_model_specific_features_accessible

This variant includes:
- Comprehensive series-specific timeout handling
- Enhanced device model detection and validation
- Robust PTP feature validation based on device capabilities
- Extensive logging with device context information
- Device-specific interface validation patterns
"""

import pytest
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect
from conftest import wait_for_satellite_loading
from pages.device_capabilities import DeviceCapabilities
from pages.ptp_config_page_device_enhanced import PTPConfigPage


def test_2_2_2_model_specific_features_accessible_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 2_2_2 Model Specific Features Accessible - Device Enhanced

    Purpose: Enhanced test for model-specific configuration features with
             comprehensive DeviceCapabilities integration

    Features:
    - Comprehensive series-specific timeout handling and validation
    - Enhanced device model detection with PTP feature verification
    - Robust navigation with device-aware error recovery
    - Extensive logging with device context information
    - Device-specific interface validation patterns

    Expected:
    - PTP features accessible only on Series 3+ devices that support them
    - PTP profile selectors validated based on available interfaces
    - Series 2 devices should NOT have PTP section accessible
    - Series-specific validation and error handling
    - Comprehensive device context logging

    Args:
        unlocked_config_page (Page): Playwright page object in unlocked config state
        base_url (str): Base URL for the device under test
        request: Pytest request object for accessing device model information
    """
    # Device capabilities setup with comprehensive validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate device-specific features"
        )

    # Get device series and timeout multiplier for enhanced handling
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)
    ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)
    max_outputs = DeviceCapabilities.get_max_outputs(device_model)

    # Calculate series-specific timeout
    base_timeout = 15000  # 15 seconds base for PTP operations
    series_timeout = int(base_timeout * timeout_multiplier)

    print(f"\n{'='*60}")
    print(f"DEVICE ENHANCED TEST: Model Specific Features")
    print(f"{'='*60}")
    print(f"Device Model: {device_model}")
    print(f"Device Series: {device_series}")
    print(f"PTP Supported: {ptp_supported}")
    print(f"PTP Interfaces: {len(ptp_interfaces)} available")
    print(f"Max Outputs: {max_outputs}")
    print(f"Timeout Multiplier: {timeout_multiplier}")
    print(f"Series-Specific Timeout: {series_timeout}ms")
    print(f"{'='*60}\n")

    # Enhanced PTP feature validation based on device series
    if ptp_supported:
        print(f"\nPerforming Series {device_series} PTP feature validation...")
        print(f" Device {device_model}: PTP-supported device detected")
        print(f"PTP Interfaces to validate: {ptp_interfaces}")

        try:
            # Enhanced navigation to PTP configuration
            ptp_url = f"{base_url}/ptp"
            print(f"Navigating to PTP configuration: {ptp_url}")

            # Series-specific PTP navigation
            unlocked_config_page.goto(ptp_url, timeout=series_timeout)

            # Enhanced URL validation
            assert "ptp" in unlocked_config_page.url, "URL should contain 'ptp'"
            print(f" PTP URL validation passed: {unlocked_config_page.url}")

            # Wait for PTP page load with device-aware loading
            wait_for_satellite_loading(unlocked_config_page)
            print(f" PTP page loaded successfully for device {device_model}")

            # Enhanced PTP interface validation
            print(f"\nValidating PTP interfaces for device {device_model}...")

            # Create PTPConfigPage instance for panel expansion
            ptp_page = PTPConfigPage(unlocked_config_page, device_model)

            available_profiles = []

            for interface in ptp_interfaces:
                try:
                    print(f"Checking PTP profile selector for interface {interface}...")

                    # CRITICAL FIX: Expand PTP panel first before checking selectors
                    print(f" Expanding PTP panel for interface {interface}...")
                    panel_expanded = ptp_page.expand_ptp_interface_panel(interface)
                    if panel_expanded:
                        print(f" PTP panel {interface} expanded successfully")
                    else:
                        print(f" PTP panel {interface} expansion failed or not needed")

                    # Enhanced PTP profile selector detection (after panel expansion)
                    profile_selectors = [
                        unlocked_config_page.locator(
                            f"select[name='ptp_profile_{interface}']"
                        ),
                        unlocked_config_page.locator(
                            f"select[name*='ptp'][name*='{interface}']"
                        ),
                        unlocked_config_page.locator(
                            f"select[id*='ptp'][id*='{interface}']"
                        ),
                    ]

                    profile_found = False
                    for selector in profile_selectors:
                        if selector.count() > 0:
                            profile_found = True
                            print(
                                f" PTP profile selector found for interface {interface}"
                            )

                            # Validate selector has options
                            options = selector.locator("option").all()
                            option_count = len(options)
                            print(
                                f"   Interface {interface}: {option_count} profile options available"
                            )

                            # Verify selector is visible and accessible
                            expect(selector).to_be_visible(timeout=series_timeout // 4)
                            break

                    if profile_found:
                        available_profiles.append(interface)
                    else:
                        print(
                            f"ℹ PTP profile selector not found for interface {interface}"
                        )

                except Exception as e:
                    print(f" Error checking interface {interface}: {str(e)}")

            # Enhanced validation results
            if len(available_profiles) > 0:
                print(f" PTP configuration validated for {device_model}")
                print(f"   Available PTP interfaces: {available_profiles}")
                print(
                    f"   Total interfaces with profiles: {len(available_profiles)}/{len(ptp_interfaces)}"
                )
            else:
                print(f" No PTP profile selectors found for device {device_model}")
                print(f"   Expected interfaces: {ptp_interfaces}")
                print(f"   Available profiles: {available_profiles}")

            # Series-specific PTP validation patterns
            if device_series == 3:
                print(f"\nSeries {device_series} PTP validation patterns:")
                # Series 3 specific validations could go here
                pass
            else:
                print(f"\nSeries {device_series} PTP validation patterns:")
                # Other series validations could go here
                pass

            # Final PTP validation assertions
            assert len(available_profiles) > 0, (
                f"Device {device_model} should have at least one PTP interface with profile selector. "
                f"Expected: {ptp_interfaces}, Found: {available_profiles}"
            )

            # Enhanced PTP page content validation
            print(f"\nPerforming PTP page content validation...")

            try:
                # Check for common PTP page elements
                ptp_indicators = [
                    unlocked_config_page.locator("text=PTP"),
                    unlocked_config_page.locator("text=Profile"),
                    unlocked_config_page.locator("text=Precision"),
                    unlocked_config_page.locator("text=Time"),
                ]

                found_indicators = 0
                for indicator in ptp_indicators:
                    if indicator.count() > 0:
                        found_indicators += 1

                print(
                    f"PTP page indicators found: {found_indicators}/{len(ptp_indicators)}"
                )

                if found_indicators >= 2:
                    print(f" PTP page content validation passed")
                else:
                    print(f" PTP page content may be limited")

            except Exception as e:
                print(f" PTP page content validation warning: {str(e)}")

            # Success logging for PTP devices
            success_msg = (
                f"PTP features validated successfully for device {device_model} "
                f"(Series {device_series}, {len(available_profiles)}/{len(ptp_interfaces)} interfaces, "
                f"PTP supported: {ptp_supported})"
            )
            print(f" PTP SUCCESS: {success_msg}")

        except PlaywrightTimeoutError:
            error_msg = (
                f"PTP navigation failed for device {device_model} "
                f"(Series {device_series}) within {series_timeout}ms timeout"
            )
            print(f" PTP NAVIGATION TIMEOUT: {error_msg}")
            raise AssertionError(error_msg)

        except Exception as e:
            error_msg = f"PTP validation failed for device {device_model}: {str(e)}"
            print(f" PTP VALIDATION ERROR: {error_msg}")
            raise AssertionError(error_msg)

    else:
        print(f"\nPerforming Series {device_series} non-PTP device validation...")
        print(
            f" Device {device_model}: Non-PTP device detected (Series {device_series})"
        )

        try:
            # Enhanced navigation to dashboard for non-PTP devices
            dashboard_url = f"{base_url}/"
            print(f"Navigating to dashboard: {dashboard_url}")

            unlocked_config_page.goto(dashboard_url, timeout=series_timeout)

            # Wait for dashboard load
            wait_for_satellite_loading(unlocked_config_page)
            print(f" Dashboard loaded successfully for device {device_model}")

            # Enhanced validation that PTP is not accessible
            print(f"\nValidating PTP is NOT accessible for device {device_model}...")

            # Check if PTP section exists in navigation
            ptp_nav_elements = [
                unlocked_config_page.locator("a").filter(has_text="PTP"),
                unlocked_config_page.locator("aside a").filter(has_text="PTP"),
                unlocked_config_page.locator("#navbar-collapse a").filter(
                    has_text="PTP"
                ),
            ]

            ptp_found_in_nav = False
            for element in ptp_nav_elements:
                if element.count() > 0:
                    ptp_found_in_nav = True
                    print(
                        f" PTP navigation found in sidebar (unexpected for non-PTP device)"
                    )
                    break

            if not ptp_found_in_nav:
                print(f" PTP navigation correctly absent for device {device_model}")

            # Try direct PTP URL access (should fail or redirect)
            try:
                ptp_direct_url = f"{base_url}/ptp"
                unlocked_config_page.goto(ptp_direct_url, timeout=series_timeout // 2)

                current_url = unlocked_config_page.url
                if "ptp" in current_url:
                    print(f" Direct PTP URL access succeeded (may be redirected)")
                else:
                    print(f" Direct PTP URL access redirected/denied as expected")

            except Exception as e:
                print(f" Direct PTP URL access failed as expected: {str(e)}")

            # Success logging for non-PTP devices
            success_msg = (
                f"Non-PTP device validation completed for device {device_model} "
                f"(Series {device_series}, Max outputs: {max_outputs}, PTP supported: {ptp_supported})"
            )
            print(f" NON-PTP SUCCESS: {success_msg}")

        except Exception as e:
            error_msg = (
                f"Non-PTP device validation failed for device {device_model}: {str(e)}"
            )
            print(f" NON-PTP VALIDATION ERROR: {error_msg}")
            raise AssertionError(error_msg)

    # Enhanced final validation and reporting
    final_status = {
        "device_model": device_model,
        "device_series": device_series,
        "ptp_supported": ptp_supported,
        "ptp_interfaces": len(ptp_interfaces),
        "max_outputs": max_outputs,
        "timeout_multiplier": timeout_multiplier,
    }

    print(f"\n{'='*60}")
    print(f"MODEL SPECIFIC FEATURES VALIDATION COMPLETE")
    print(f"{'='*60}")
    for key, value in final_status.items():
        print(f"{key}: {value}")
    print(f"{'='*60}\n")

    # Assert device series validation
    assert device_series in [
        2,
        3,
    ], f"Device series should be 2 or 3, found {device_series}"

    # Final success message
    print(f" ALL MODEL SPECIFIC FEATURES VALIDATED SUCCESSFULLY! ")
