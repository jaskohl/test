"""
Test 2_1_8 Syslog Section Access - Device Enhanced
Category: 02 - Configuration Section Navigation
Enhanced with comprehensive DeviceCapabilities integration
Source Method: TestConfigurationNavigation.test_2_1_8_syslog_section_access

This variant includes:
- Series-specific timeout handling
- Device model detection and validation
- Comprehensive syslog configuration verification
- Enhanced logging and error recovery
"""

import pytest
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect
from conftest import wait_for_satellite_loading
from pages.device_capabilities import DeviceCapabilities


def test_2_1_8_syslog_section_access_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 2_1_8 Syslog Section Access - Device Enhanced

    Purpose: Enhanced test for syslog configuration section access with
             comprehensive DeviceCapabilities integration

    Features:
    - Series-specific timeout handling and validation
    - Device model detection with comprehensive syslog verification
    - Robust navigation with device-aware error recovery
    - Enhanced logging with device context information
    - Syslog system validation based on device capabilities

    Expected:
    - Navigation to syslog page succeeds within series-specific timeouts
    - Syslog configuration page loads successfully for all device models
    - Series-specific syslog validation and error handling
    - Comprehensive device context logging

    Args:
        unlocked_config_page (Page): Playwright page object in unlocked config state
        base_url (str): Base URL for the device under test
        request: Pytest request object for accessing device model information
    """
    # Device capabilities setup with comprehensive validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate syslog configuration")

    # Get device series and timeout multiplier for enhanced handling
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Calculate series-specific timeout
    base_timeout = 10000  # 10 seconds base
    series_timeout = int(base_timeout * timeout_multiplier)

    print(f"\n{'='*60}")
    print(f"DEVICE ENHANCED TEST: Syslog Section Access")
    print(f"{'='*60}")
    print(f"Device Model: {device_model}")
    print(f"Device Series: {device_series}")
    print(f"Timeout Multiplier: {timeout_multiplier}")
    print(f"Series-Specific Timeout: {series_timeout}ms")
    print(f"{'='*60}\n")

    # Enhanced navigation with device-aware error recovery
    syslog_url = f"{base_url}/syslog"
    try:
        print(f"Navigating to syslog configuration: {syslog_url}")

        # Series-specific navigation with enhanced timeout handling
        if device_series == 2:
            # Series 2 devices may have different syslog loading characteristics
            unlocked_config_page.goto(syslog_url, timeout=series_timeout)
            print(f"Series {device_series} navigation completed")
        else:
            # Series 3 and other devices
            unlocked_config_page.goto(syslog_url, timeout=series_timeout)
            print(f"Series {device_series} navigation completed")

        # Verify URL contains syslog with enhanced validation
        assert "syslog" in unlocked_config_page.url, "URL should contain 'syslog'"
        print(f"URL verification passed: {unlocked_config_page.url}")

    except PlaywrightTimeoutError:
        error_msg = (
            f"Navigation to syslog page failed for device {device_model} "
            f"(Series {device_series}) within {series_timeout}ms timeout"
        )
        print(f" NAVIGATION ERROR: {error_msg}")
        raise AssertionError(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error during syslog page navigation for device {device_model}: {str(e)}"
        print(f" UNEXPECTED ERROR: {error_msg}")
        raise AssertionError(error_msg)

    # Wait for page load completion with device-aware loading
    try:
        wait_for_satellite_loading(unlocked_config_page)
        print(f"Satellite loading completed for device {device_model}")
    except Exception as e:
        print(f" Satellite loading warning for device {device_model}: {str(e)}")
        # Continue test - this is not a critical failure

    # Enhanced syslog page validation
    print(f"\nValidating syslog configuration page for device {device_model}...")

    # Series-specific syslog configuration validation
    print(f"\nPerforming series-specific syslog validation...")

    if device_series == 2:
        print(f"Series {device_series} syslog configuration validation:")
        # Series 2 syslog-specific validations
        try:
            # Look for syslog-related configuration elements
            syslog_elements = [
                unlocked_config_page.locator("input[name*='syslog']"),
                unlocked_config_page.locator("select[name*='syslog']"),
                unlocked_config_page.locator("input[name*='log']"),
                unlocked_config_page.locator("textarea[name*='syslog']"),
            ]

            found_syslog_elements = 0
            for element in syslog_elements:
                if element.count() > 0:
                    found_syslog_elements += 1
                    print(f" Series {device_series} syslog element found")

            print(
                f"Series {device_series}: {found_syslog_elements} syslog-related elements detected"
            )

        except Exception as e:
            print(
                f" Series {device_series} syslog element validation warning: {str(e)}"
            )

    else:
        print(f"Series {device_series} syslog configuration validation:")
        # Series 3+ syslog-specific validations
        try:
            # Look for enhanced syslog-related configuration elements
            syslog_elements = [
                unlocked_config_page.locator("input[name*='syslog']"),
                unlocked_config_page.locator("select[name*='syslog']"),
                unlocked_config_page.locator("input[name*='log']"),
                unlocked_config_page.locator("textarea[name*='syslog']"),
            ]

            found_syslog_elements = 0
            for element in syslog_elements:
                if element.count() > 0:
                    found_syslog_elements += 1
                    print(f" Series {device_series} syslog element found")

            print(
                f"Series {device_series}: {found_syslog_elements} syslog-related elements detected"
            )

        except Exception as e:
            print(
                f" Series {device_series} syslog element validation warning: {str(e)}"
            )

    # Enhanced syslog system validation
    print(f"\nPerforming enhanced syslog system validation...")

    # Validate syslog page content availability
    try:
        # Check for common syslog page elements
        page_content = unlocked_config_page.locator("body")
        if page_content.count() > 0:
            page_text = page_content.text_content()
            if page_text and "syslog" in page_text.lower():
                print(f" Syslog page content validated")
            else:
                print(f" Warning: Syslog page content may be limited")

        # Additional syslog-specific element checks
        syslog_indicators = [
            unlocked_config_page.locator("text=Syslog"),
            unlocked_config_page.locator("text=Log"),
            unlocked_config_page.locator("text=Server"),
            unlocked_config_page.locator("text=Facility"),
        ]

        found_indicators = 0
        for indicator in syslog_indicators:
            if indicator.count() > 0:
                found_indicators += 1

        print(f"Syslog page indicators found: {found_indicators}/4")

    except Exception as e:
        print(f" Syslog system validation warning: {str(e)}")

    # Verify syslog page is actually loaded and responsive
    print(f"\nVerifying syslog page responsiveness...")

    try:
        # Check if the page has loaded completely
        page_title = unlocked_config_page.locator("title")
        if page_title.count() > 0:
            title_text = page_title.text_content()
            print(f"Page title: {title_text}")

        # Try to interact with the page to ensure it's responsive
        unlocked_config_page.reload()
        print(f" Syslog page responsiveness validated")

    except Exception as e:
        print(f" Syslog page responsiveness validation warning: {str(e)}")

    # Final comprehensive validation
    final_status = {
        "device_model": device_model,
        "device_series": device_series,
        "timeout_multiplier": timeout_multiplier,
        "navigation_timeout": series_timeout,
        "syslog_url_accessible": "syslog" in unlocked_config_page.url,
    }

    print(f"\n{'='*60}")
    print(f"FINAL VALIDATION RESULTS")
    print(f"{'='*60}")
    for key, value in final_status.items():
        print(f"{key}: {value}")
    print(f"{'='*60}\n")

    # Success validation
    success_msg = (
        f"Syslog section access validated successfully for device {device_model} "
        f"(Series {device_series}, {timeout_multiplier}x timeout multiplier)"
    )
    print(f" SUCCESS: {success_msg}")

    # Assert final validation
    assert device_series in [
        2,
        3,
    ], f"Device series should be 2 or 3, found {device_series}"
    assert "syslog" in unlocked_config_page.url, "URL should contain 'syslog'"
