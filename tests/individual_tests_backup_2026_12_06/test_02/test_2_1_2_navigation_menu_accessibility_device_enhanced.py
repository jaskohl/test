"""
Category 2: Navigation - Test 2.1.2
Navigation Menu Accessibility - DeviceCapabilities Enhanced
Test Count: 2 of 4 in Category 2
Hardware: Device Only
Priority: MEDIUM - Navigation foundation
Series: Both Series 2 and 3
ENHANCED: DeviceCapabilities integration for device-aware navigation patterns
Based on navigation workflow requirements and device exploration data
Device exploration data: navigation_menus.json, page_structure.json
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.login_page import LoginPage

logger = logging.getLogger(__name__)


def test_2_1_2_navigation_menu_accessibility_device_enhanced(
    unlocked_config_page: Page, base_url: str, device_password: str, request
):
    """
    Test 2.1.2: Navigation Menu Accessibility - DeviceCapabilities Enhanced
    Purpose: Verify navigation menu accessibility and device-aware menu structure
    Expected: Menu accessible with device-specific sections and timing
    ENHANCED: Full DeviceCapabilities integration for device-aware navigation validation
    Series: Both - validates navigation patterns across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate navigation accessibility"
        )

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing navigation menu accessibility on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Get device-specific behavior patterns
    behavior_data = DeviceCapabilities.get_behavior_data(device_model)
    navigation_workflow = behavior_data.get("navigation_workflow", {})

    # Initialize page objects with device-aware patterns
    login_page = LoginPage(unlocked_config_page, device_model)

    # FIX 2: Use BasePage method for proper dashboard context management
    from pages.base import BasePage

    base_page = BasePage(unlocked_config_page, device_model)

    # Ensure we're on dashboard before testing navigation menus
    print(f"Ensuring dashboard context for navigation menu testing...")
    dashboard_ready = base_page.ensure_dashboard_context(base_url)
    assert (
        dashboard_ready
    ), f"Failed to ensure dashboard context for navigation testing on {device_model}"
    print(f" Dashboard context confirmed for {device_model}")

    # Test navigation menu presence with device-aware validation
    navigation_menus = [
        ("General", "Configuration"),
        ("Network", "Network"),
        ("Time", "Time"),
        ("GNSS", "GNSS"),
        ("Outputs", "Outputs"),
        ("Display", "Display"),
        ("Access", "Access"),
    ]

    found_menus = []
    missing_menus = []

    for menu_name, menu_text in navigation_menus:
        try:
            # Search for menu link by text and role
            menu_link = unlocked_config_page.get_by_role("link", name=menu_text)
            if menu_link.count() > 0 and menu_link.is_visible():
                found_menus.append(menu_name)
                logger.info(f" {menu_name} menu accessible on {device_model}")
            else:
                # Alternative search patterns
                menu_link = unlocked_config_page.locator("a").filter(has_text=menu_text)
                if menu_link.count() > 0 and menu_link.is_visible():
                    found_menus.append(menu_name)
                    logger.info(
                        f" {menu_name} menu accessible (alt pattern) on {device_model}"
                    )
                else:
                    missing_menus.append(menu_name)
                    logger.warning(f" {menu_name} menu not found on {device_model}")
        except Exception as e:
            missing_menus.append(menu_name)
            logger.warning(f" {menu_name} menu search failed: {e}")

    # Validate Series-specific menu variations
    if device_series == 2:
        # Series 2 devices typically have fewer menu options
        expected_core_menus = [
            "General",
            "Network",
            "Time",
            "GNSS",
            "Outputs",
            "Display",
            "Access",
        ]
        series2_specific = [
            "General",
            "Network",
            "Time",
            "GNSS",
            "Outputs",
            "Display",
            "Access",
        ]

        for expected_menu in expected_core_menus:
            if expected_menu in found_menus:
                logger.info(
                    f" Series 2 core menu {expected_menu} found on {device_model}"
                )
            else:
                logger.warning(
                    f" Series 2 core menu {expected_menu} missing on {device_model}"
                )

    elif device_series == 3:
        # Series 3 devices have expanded menu options including SNMP, Syslog, PTP
        expected_series3_menus = [
            "General",
            "Network",
            "Time",
            "GNSS",
            "Outputs",
            "Display",
            "Access",
        ]
        extended_menus = [
            ("SNMP", "SNMP"),  # Series 3 may have SNMP menu
            ("Syslog", "Syslog"),  # Series 3 may have Syslog menu
            ("PTP", "PTP"),  # Series 3 may have PTP menu
        ]

        for menu_name, menu_text in extended_menus:
            try:
                menu_link = unlocked_config_page.get_by_role("link", name=menu_text)
                if menu_link.count() > 0 and menu_link.is_visible():
                    logger.info(
                        f" Series 3 extended menu {menu_name} available on {device_model}"
                    )
                    found_menus.append(menu_name)
                else:
                    logger.info(
                        f"ℹ Series 3 menu {menu_name} not available on {device_model} (may be conditional)"
                    )
            except Exception as e:
                logger.warning(f"Extended menu {menu_name} search failed: {e}")

    # Test menu accessibility timing with device-aware expectations
    start_time = time.time()

    # Try to access each found menu to verify functionality
    accessible_menus = 0
    for menu_name, menu_text in navigation_menus:
        if menu_name in found_menus:
            try:
                menu_link = unlocked_config_page.get_by_role("link", name=menu_text)
                if menu_link.count() > 0:
                    menu_link.click()

                    # Wait for page load with device-aware timeout
                    page_load_timeout = int(5000 * timeout_multiplier)
                    unlocked_config_page.wait_for_load_state(
                        "domcontentloaded", timeout=page_load_timeout
                    )

                    accessible_menus += 1
                    logger.info(
                        f" {menu_name} menu accessible and clickable on {device_model}"
                    )

                    # Return to dashboard for next menu test
                    unlocked_config_page.goto(base_url, wait_until="domcontentloaded")
                    stability_timeout = int(2000 * timeout_multiplier)
                    unlocked_config_page.wait_for_load_state(
                        "domcontentloaded", timeout=stability_timeout
                    )

            except Exception as e:
                logger.warning(f" {menu_name} menu click failed: {e}")

    navigation_duration = time.time() - start_time

    # Validate navigation performance expectations
    performance_data = DeviceCapabilities.get_performance_expectations(device_model)
    if performance_data:
        navigation_performance = performance_data.get("navigation_performance", {})
        if navigation_performance:
            typical_time = navigation_performance.get("typical_page_transition", "")
            logger.info(f"Navigation performance baseline: {typical_time}")

    # Test responsive menu behavior with device-specific patterns
    try:
        # Check for menu toggle/collapse behavior (especially on Series 3)
        if device_series == 3:
            # Series 3 devices may have collapsible navigation
            menu_toggle = unlocked_config_page.locator(
                "button[aria-label*='menu'], button[aria-label*='Menu']"
            )
            if menu_toggle.count() > 0:
                logger.info(f" Menu toggle found for Series 3 device {device_model}")
                # Test menu toggle functionality
                menu_toggle.click()
                time.sleep(0.5 * timeout_multiplier)
                logger.info(f" Menu toggle responsive on {device_model}")
            else:
                logger.info(f"ℹ No collapsible menu toggle on {device_model}")

        # Series 2 typically has simpler navigation structure
        elif device_series == 2:
            logger.info(f"ℹ Series 2 simple navigation structure on {device_model}")

    except Exception as e:
        logger.warning(f"Menu toggle test failed on {device_model}: {e}")

    # Cross-validate with DeviceCapabilities expected navigation patterns
    device_capabilities = DeviceCapabilities.get_capabilities(device_model)
    expected_features = device_capabilities.get("features", [])

    # Check if menu accessibility matches device capabilities
    if "network_config" in expected_features:
        if "Network" in found_menus:
            logger.info(
                f" Network menu accessibility matches device capabilities for {device_model}"
            )
        else:
            logger.warning(
                f" Network menu missing despite network_config capability for {device_model}"
            )

    if "gnss_config" in expected_features:
        if "GNSS" in found_menus:
            logger.info(
                f" GNSS menu accessibility matches device capabilities for {device_model}"
            )
        else:
            logger.warning(
                f" GNSS menu missing despite gnss_config capability for {device_model}"
            )

    # Final validation and logging
    total_expected_menus = len(navigation_menus)
    accessibility_rate = (accessible_menus / total_expected_menus) * 100

    logger.info(f"Navigation Menu Accessibility Test Results for {device_model}:")
    logger.info(f"  - Device Series: {device_series}")
    logger.info(f"  - Total Menus Found: {len(found_menus)}/{total_expected_menus}")
    logger.info(f"  - Accessible Menus: {accessible_menus}/{len(found_menus)}")
    logger.info(f"  - Accessibility Rate: {accessibility_rate:.1f}%")
    logger.info(f"  - Navigation Duration: {navigation_duration:.2f}s")
    logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")

    # Final validation - ensure minimum accessibility
    if accessible_menus >= (total_expected_menus * 0.7):  # 70% minimum
        logger.info(f" Navigation menu accessibility PASSED for {device_model}")
        print(
            f"NAVIGATION MENU ACCESSIBILITY SUCCESSFUL: {device_model} (Series {device_series})"
        )
    else:
        pytest.fail(
            f"Navigation menu accessibility FAILED - only {accessible_menus}/{total_expected_menus} menus accessible on {device_model}"
        )
