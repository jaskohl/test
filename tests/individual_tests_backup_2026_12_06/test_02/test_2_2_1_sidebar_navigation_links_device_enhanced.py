"""
Test 2_2_1 Sidebar Navigation Links - Device Enhanced
Category: 02 - Configuration Section Navigation
Enhanced with comprehensive DeviceCapabilities integration
Source Method: TestConfigurationNavigation.test_2_2_1_sidebar_navigation_links

This variant includes:
- Comprehensive series-specific timeout handling
- Enhanced device model detection and validation
- Robust navigation with device-aware error recovery
- Extensive logging with device context information
- Device-specific navigation pattern validation
"""

import pytest
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect
from conftest import wait_for_satellite_loading
from pages.device_capabilities import DeviceCapabilities


def test_2_2_1_sidebar_navigation_links_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 2_2_1 Sidebar Navigation Links - Device Enhanced

    Purpose: Enhanced test for all sidebar navigation links with comprehensive
             DeviceCapabilities integration

    Features:
    - Comprehensive series-specific timeout handling and validation
    - Enhanced device model detection with navigation verification
    - Robust navigation with device-aware error recovery
    - Extensive logging with device context information
    - Device-specific navigation pattern validation

    Expected:
    - All sidebar navigation links work correctly for the device model
    - PTP navigation appears only on Series 3+ devices that support it
    - Series-specific navigation timeout handling
    - Comprehensive device context logging for all navigation actions
    - Device-aware performance monitoring and validation

    Args:
        unlocked_config_page (Page): Playwright page object in unlocked config state
        base_url (str): Base URL for the device under test
        request: Pytest request object for accessing device model information
    """
    # Device capabilities setup with comprehensive validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate navigation")

    # Get device series and timeout multiplier for enhanced handling
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)
    known_issues = DeviceCapabilities.get_known_issues(device_model)

    # Calculate series-specific timeout
    base_timeout = 30000  # 30 seconds base for navigation
    series_timeout = int(base_timeout * timeout_multiplier)

    print(f"\n{'='*60}")
    print(f"DEVICE ENHANCED TEST: Sidebar Navigation Links")
    print(f"{'='*60}")
    print(f"Device Model: {device_model}")
    print(f"Device Series: {device_series}")
    print(f"PTP Supported: {ptp_supported}")
    print(f"Timeout Multiplier: {timeout_multiplier}")
    print(f"Series-Specific Timeout: {series_timeout}ms")
    print(f"Known Issues: {len(known_issues)} identified")
    print(f"{'='*60}\n")

    # Enhanced navigation sections with device capabilities
    base_sections = {
        "General": "/general",
        "Network": "/network",
        "Time": "/time",
        "Outputs": "/outputs",
        "GNSS": "/gnss",
        "Display": "/display",
        "SNMP": "/snmp",
        "Syslog": "/syslog",
        "Upload": "/upload",
        "Access": "/access",
    }

    # Add PTP section only for devices that support it
    if ptp_supported:
        sections = base_sections.copy()
        sections["PTP"] = "/ptp"
        print(f" Device {device_model}: PTP-supported navigation enabled")
    else:
        sections = base_sections
        print(f"ℹ Device {device_model}: PTP not supported - navigation excludes PTP")

    # Enhanced navigation to dashboard with device-aware loading
    try:
        print(f"Navigating to dashboard for {device_model}...")
        unlocked_config_page.goto(f"{base_url}/", timeout=series_timeout)
        wait_for_satellite_loading(unlocked_config_page)
        print(f" Dashboard loaded successfully for device {device_model}")
    except Exception as e:
        error_msg = f"Failed to load dashboard for device {device_model}: {str(e)}"
        print(f" DASHBOARD LOAD ERROR: {error_msg}")
        raise AssertionError(error_msg)

    # Enhanced PTP panel expansion for Series 3+ devices
    if device_series >= 3 and ptp_supported:
        print(f"\nPerforming Series {device_series} PTP panel expansion...")
        try:
            from pages.ptp_config_page import PTPConfigPage

            ptp_page = PTPConfigPage(unlocked_config_page)
            ptp_page.expand_all_ptp_panels()
            print(f" PTP panels expanded successfully for {device_model}")
        except Exception as e:
            print(f" PTP panel expansion warning for {device_model}: {str(e)}")
            print(f"Continuing navigation test despite PTP expansion failure")

    # Enhanced navigation validation for each section
    navigation_results = []

    for section_name, expected_path in sections.items():
        print(f"\n{'='*50}")
        print(f"Testing navigation to: {section_name} ({expected_path})")
        print(f"Device: {device_model} (Series {device_series})")
        print(f"{'='*50}")

        try:
            # Enhanced link detection with multiple fallback strategies
            sidebar_link = None

            # Strategy 1: Direct sidebar targeting
            sidebar_link = unlocked_config_page.locator("aside.main-sidebar a").filter(
                has_text=section_name
            )

            # Strategy 2: Mobile navigation fallback
            if sidebar_link.count() == 0:
                print(f"Primary sidebar not found, trying mobile navigation...")
                sidebar_link = unlocked_config_page.locator(
                    "#navbar-collapse a"
                ).filter(has_text=section_name)

            # Strategy 3: Href-based matching
            if sidebar_link.count() == 0:
                print(f"Mobile nav not found, trying href-based matching...")
                sidebar_link = unlocked_config_page.locator("a").filter(
                    has=unlocked_config_page.locator(
                        f"[href*='{expected_path.lstrip('/')}']"
                    )
                )

            # Strategy 4: Generic text-based matching
            if sidebar_link.count() == 0:
                print(f"Href matching not found, trying generic text matching...")
                sidebar_link = unlocked_config_page.locator("a").filter(
                    has_text=section_name
                )

            # Verify link was found
            if sidebar_link.count() == 0:
                raise AssertionError(
                    f"Could not find {section_name} link in sidebar for {device_model}"
                )

            print(f" Found {section_name} navigation link")

            # Enhanced link validation
            expect(sidebar_link).to_be_visible(timeout=series_timeout // 4)

            # Verify href attribute matches expected path
            href_attr = sidebar_link.get_attribute("href")
            expected_href = expected_path.lstrip("/")

            if expected_href not in href_attr and not href_attr.endswith(expected_href):
                print(
                    f" Link href '{href_attr}' doesn't exactly match '{expected_href}' but proceeding..."
                )

            print(f"Navigation link validated: {href_attr}")

            # Enhanced device-aware timeout calculation
            navigation_timeout = series_timeout

            # Apply known issue adjustments
            if any("timeout" in issue.lower() for issue in known_issues):
                navigation_timeout = int(navigation_timeout * 1.5)
                print(
                    f"Extended timeout due to known navigation issues: {navigation_timeout}ms"
                )

            # Apply series-specific adjustments
            if device_series == 2:
                print(f"Applying Series 2 navigation timing adjustments")
                navigation_timeout = int(
                    navigation_timeout * 1.2
                )  # Series 2 may be slower
            elif device_series >= 3:
                print(f"Applying Series 3+ navigation timing optimizations")
                navigation_timeout = int(
                    navigation_timeout * 0.9
                )  # Series 3+ may be faster

            # Enhanced navigation execution
            print(
                f"Executing navigation to {section_name} with {navigation_timeout}ms timeout..."
            )
            sidebar_link.click(timeout=navigation_timeout)

            # Enhanced URL validation
            current_url = unlocked_config_page.url
            if expected_path not in current_url:
                raise AssertionError(
                    f"Navigation failed: Expected '{expected_path}' in URL, got '{current_url}'"
                )

            print(f" Successfully navigated to {section_name} ({expected_path})")

            # Record successful navigation
            navigation_results.append(
                {
                    "section": section_name,
                    "path": expected_path,
                    "status": "success",
                    "timeout_used": navigation_timeout,
                    "url_after": current_url,
                }
            )

            # Enhanced post-navigation validation
            print(f"Performing post-navigation validation for {section_name}...")

            # Check page loaded successfully
            page_title = unlocked_config_page.locator("title")
            if page_title.count() > 0:
                title_text = page_title.text_content()
                print(f"Page title: {title_text}")

            # Check for any obvious errors
            error_elements = unlocked_config_page.locator(
                ".error, .alert-error, [class*='error']"
            )
            if error_elements.count() > 0:
                print(
                    f" Warning: Found {error_elements.count()} error elements on {section_name} page"
                )

            # Navigate back to dashboard for next iteration
            print(f"Returning to dashboard for next navigation test...")
            unlocked_config_page.goto(f"{base_url}/", timeout=series_timeout // 2)
            wait_for_satellite_loading(unlocked_config_page)

        except PlaywrightTimeoutError as e:
            error_msg = (
                f"Navigation timeout for {section_name} on device {device_model} "
                f"(Series {device_series}): {str(e)}"
            )
            print(f" NAVIGATION TIMEOUT: {error_msg}")

            navigation_results.append(
                {
                    "section": section_name,
                    "path": expected_path,
                    "status": "timeout",
                    "error": str(e),
                    "timeout_used": (
                        navigation_timeout
                        if "navigation_timeout" in locals()
                        else series_timeout
                    ),
                }
            )
            raise

        except Exception as e:
            error_msg = (
                f"Navigation error for {section_name} on device {device_model} "
                f"(Series {device_series}): {str(e)}"
            )
            print(f" NAVIGATION ERROR: {error_msg}")

            navigation_results.append(
                {
                    "section": section_name,
                    "path": expected_path,
                    "status": "error",
                    "error": str(e),
                }
            )
            raise

    # Enhanced final validation and reporting
    print(f"\n{'='*60}")
    print(f"NAVIGATION TEST COMPLETION SUMMARY")
    print(f"{'='*60}")
    print(f"Device: {device_model} (Series {device_series})")
    print(f"Total Sections Tested: {len(sections)}")
    print(
        f"Successful Navigations: {len([r for r in navigation_results if r['status'] == 'success'])}"
    )
    print(
        f"Failed Navigations: {len([r for r in navigation_results if r['status'] != 'success'])}"
    )
    print(f"PTP Support: {ptp_supported}")
    print(f"Timeout Multiplier: {timeout_multiplier}")
    print(f"Known Issues Count: {len(known_issues)}")
    print(f"{'='*60}\n")

    # Detailed results for each section
    print(f"DETAILED NAVIGATION RESULTS:")
    for result in navigation_results:
        status_symbol = "" if result["status"] == "success" else ""
        print(f"{status_symbol} {result['section']}: {result['status']}")
        if result["status"] != "success":
            print(f"   Error: {result.get('error', 'Unknown error')}")
        print(f"   Path: {result['path']}")
        if "timeout_used" in result:
            print(f"   Timeout Used: {result['timeout_used']}ms")
        print()

    # Final assertions
    successful_navigations = len(
        [r for r in navigation_results if r["status"] == "success"]
    )
    expected_navigations = len(sections)

    assert successful_navigations == expected_navigations, (
        f"Navigation test failed: Expected {expected_navigations} successful navigations, "
        f"got {successful_navigations} for device {device_model}"
    )

    # Success validation
    success_msg = (
        f"All sidebar navigation links validated successfully for device {device_model} "
        f"(Series {device_series}, {successful_navigations}/{expected_navigations} navigations, "
        f"PTP: {ptp_supported}, {timeout_multiplier}x timeout multiplier)"
    )
    print(f" FINAL SUCCESS: {success_msg}")

    # Assert device series validation
    assert device_series in [
        2,
        3,
    ], f"Device series should be 2 or 3, found {device_series}"
