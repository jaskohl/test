"""
Test 2.2.1: All Sidebar Navigation Links Functional - Device-Aware
Purpose: Verify all sidebar links navigate to correct pages based on device model
Expected: Each link leads to its corresponding configuration page

Category: 2 - Configuration Section Navigation
Test Type: Unit Test
Priority: HIGH
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect
from conftest import wait_for_satellite_loading
from pages.device_capabilities import DeviceCapabilities


def test_2_2_1_sidebar_navigation_links(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 2.2.1: All Sidebar Navigation Links Functional - Device-Aware
    Purpose: Verify all sidebar links navigate to correct pages based on device model
    Expected: Each link leads to its corresponding configuration page
    MODERNIZED: Uses DeviceCapabilities for device-aware navigation testing
    - PTP navigation only appears on Series 3 devices
    - Extended timeout for devices with known navigation issues
    - Device-specific validation patterns based on model capabilities
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate navigation")

    device_series = DeviceCapabilities.get_series(device_model)
    ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)

    # MODERNIZED: Use DeviceCapabilities for device-aware navigation sections
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
        print(f"Device {device_model}: PTP-supported navigation enabled")
    else:
        sections = base_sections
        print(f"Device {device_model}: PTP not supported - navigation excludes PTP")

    # Navigate to dashboard first to ensure sidebar is fully visible
    unlocked_config_page.goto(f"{base_url}/")
    wait_for_satellite_loading(unlocked_config_page)

    # MODERNIZED: Device-aware PTP panel expansion for Series 3 devices
    if device_series == 3:
        print(f"Series 3 device {device_model} detected - expanding PTP panels")
        try:
            # Import and use PTP page object for panel expansion
            from pages.ptp_config_page import PTPConfigPage

            ptp_page = PTPConfigPage(unlocked_config_page)
            ptp_page.expand_all_ptp_panels()
            print(f"PTP panels expanded successfully for {device_model}")
        except Exception as e:
            print(f"Warning: PTP panel expansion failed for {device_model}: {e}")
            # Continue anyway - navigation may still work

    for section_name, expected_path in sections.items():
        # Use href-based locator to target sidebar specifically
        sidebar_link = unlocked_config_page.locator("aside.main-sidebar a").filter(
            has_text=section_name
        )

        # Fallback: Try mobile navigation if sidebar not found
        if sidebar_link.count() == 0:
            sidebar_link = unlocked_config_page.locator("#navbar-collapse a").filter(
                has_text=section_name
            )

        # Last resort: Use href attribute matching
        if sidebar_link.count() == 0:
            sidebar_link = unlocked_config_page.locator("a").filter(
                has=unlocked_config_page.locator(
                    f"[href*='{expected_path.lstrip('/')}']"
                )
            )

        # Ensure we found the link
        assert (
            sidebar_link.count() > 0
        ), f"Could not find {section_name} link in sidebar for {device_model}"

        # Verify the link is clickable and has correct href
        expect(sidebar_link).to_be_visible(timeout=5000)

        # Verify href attribute matches expected path
        href_attr = sidebar_link.get_attribute("href")
        expected_href = expected_path.lstrip("/")
        assert expected_href in href_attr or href_attr.endswith(
            expected_href
        ), f"Link href '{href_attr}' should contain '{expected_href}' for {device_model}"

        print(f"Device {device_model}: Clicking {section_name} sidebar link...")

        # MODERNIZED: Device-aware timeout based on known performance characteristics
        known_issues = DeviceCapabilities.get_known_issues(device_model)
        navigation_timeout = 30000  # Default 30s

        if any("timeout" in issue.lower() for issue in known_issues):
            navigation_timeout = (
                45000  # Extended timeout for devices with timeout issues
            )
            print(
                f"Device {device_model}: Using extended timeout due to known navigation issues"
            )

        # Click the sidebar link with device-aware timeout
        sidebar_link.click(timeout=navigation_timeout)

        # Verify navigation occurred
        assert (
            expected_path in unlocked_config_page.url
        ), f"Device {device_model}: Clicking {section_name} should navigate to {expected_path}"

        print(
            f"Device {device_model}: Successfully navigated to {section_name} ({expected_path})"
        )

        # Navigate back to dashboard and wait for satellite loading to complete
        unlocked_config_page.goto(f"{base_url}/")
        wait_for_satellite_loading(unlocked_config_page)
