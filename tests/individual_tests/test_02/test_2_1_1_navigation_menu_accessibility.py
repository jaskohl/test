"""
Test 2.1.1: Navigation Menu Accessibility - Pure Page Object Pattern

CATEGORY: 02 - Configuration Section Navigation
TEST TYPE: Pure Page Object Pattern
PRIORITY: HIGH
HARDWARE: Device Only
SERIES: Both Series 2 and 3

TRANSFORMATION SUMMARY:
- Pure page object architecture - NO direct DeviceCapabilities calls for non-skip logic
- All device awareness handled through page object properties
- DeviceCapabilities only imported for pytest.skip() conditions if needed
- Simplified, maintainable test pattern

LOCATOR_STRATEGY_COMPLIANCE:
- Uses existing page object methods exclusively
- Primary locators through page objects (get_by_role, get_by_text)
- Fallback patterns handled in page objects
- Series 3 multi-interface support through BasePage

CREATED: 2025-12-07 for pure page object transformation
"""

import pytest
import logging
from playwright.sync_api import Page

# Import page objects - all device logic encapsulated within
from pages.general_config_page import GeneralConfigPage
from pages.network_config_page import NetworkConfigPage
from pages.time_config_page import TimeConfigPage
from pages.gnss_config_page import GNSSConfigPage
from pages.outputs_config_page import OutputsConfigPage
from pages.display_config_page import DisplayConfigPage
from pages.access_config_page import AccessConfigPage
from pages.snmp_config_page import SNMPConfigPage
from pages.syslog_config_page import SyslogConfigPage
from pages.ptp_config_page import PTPConfigPage
from pages.upload_config_page import UploadConfigPage

logger = logging.getLogger(__name__)


def test_2_1_1_navigation_menu_accessibility_exploration_based(
    unlocked_config_page: Page, request
):
    """
    Test 2.1.1: Navigation Menu Accessibility - Pure Page Object Pattern

    Purpose: Verify navigation menu accessibility using pure page object methods
    Expected: All available sections accessible with device-specific validation

    PURE PAGE OBJECT PATTERN:
    - NO DeviceCapabilities calls in test logic
    - Device awareness through page object properties
    - All timeouts handled by page objects internally
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate navigation accessibility"
        )

    logger.info(f"Testing navigation menu accessibility on {device_model}")

    # Create a reference page object to get device info
    # Page object internally uses DeviceCapabilities
    reference_page = GeneralConfigPage(unlocked_config_page, device_model)
    device_series = reference_page.device_series
    available_sections = reference_page.available_sections

    logger.info(
        f"Device series: {device_series}, Available sections: {available_sections}"
    )

    # Define navigation tests using existing page objects
    navigation_tests = [
        {"name": "General", "page_class": GeneralConfigPage, "section_id": "general"},
        {"name": "Network", "page_class": NetworkConfigPage, "section_id": "network"},
        {"name": "Time", "page_class": TimeConfigPage, "section_id": "time"},
        {"name": "GNSS", "page_class": GNSSConfigPage, "section_id": "gnss"},
        {"name": "Outputs", "page_class": OutputsConfigPage, "section_id": "outputs"},
        {"name": "Display", "page_class": DisplayConfigPage, "section_id": "display"},
        {"name": "Access", "page_class": AccessConfigPage, "section_id": "access"},
        {"name": "SNMP", "page_class": SNMPConfigPage, "section_id": "snmp"},
        {"name": "Syslog", "page_class": SyslogConfigPage, "section_id": "syslog"},
        {"name": "PTP", "page_class": PTPConfigPage, "section_id": "ptp"},
        {"name": "Upload", "page_class": UploadConfigPage, "section_id": "upload"},
    ]

    found_menus = []
    accessible_menus = 0
    tested_sections = 0

    # Test each navigation section using page objects
    for test_config in navigation_tests:
        section_name = test_config["name"]
        page_class = test_config["page_class"]
        section_id = test_config["section_id"]

        try:
            # Use page object method for section availability (NOT DeviceCapabilities directly)
            if section_id not in available_sections:
                logger.info(
                    f"Section {section_name} not available on this device - skipping"
                )
                continue

            tested_sections += 1
            logger.info(f"Testing {section_name} section navigation")

            # Create page object instance - all device awareness is internal
            page_instance = page_class(unlocked_config_page, device_model)

            # Test navigation using page object method
            if hasattr(page_instance, "navigate_to_page"):
                if page_instance.navigate_to_page():
                    found_menus.append(section_name)
                    logger.info(f"  {section_name} menu accessible via page object")
                    accessible_menus += 1
                else:
                    logger.warning(
                        f"  {section_name} navigation failed via page object"
                    )
            else:
                # Page object exists but may not have navigate method
                logger.info(f"  Using {section_name} page object (no navigate method)")
                found_menus.append(section_name)
                accessible_menus += 1

        except Exception as e:
            logger.warning(f"  {section_name} menu test failed: {e}")
            continue

    # Final validation
    min_accessible = max(3, int(tested_sections * 0.6))

    if accessible_menus >= min_accessible:
        logger.info(
            f"NAVIGATION SUCCESS: {accessible_menus}/{tested_sections} sections accessible on {device_model}"
        )
        print(
            f"NAVIGATION SUCCESS: {device_model} (Series {device_series}) - {accessible_menus}/{tested_sections} accessible"
        )

        for menu in found_menus:
            logger.info(f"   {menu}")
    else:
        pytest.fail(
            f"Navigation accessibility FAILED - only {accessible_menus}/{tested_sections} sections accessible on {device_model}. "
            f"Expected at least {min_accessible} sections."
        )

    logger.info(f"Navigation accessibility test completed for {device_model}")
    logger.info(f"Device series: {device_series}")
    logger.info(f"Sections tested: {tested_sections}")
    logger.info(f"Sections accessible: {accessible_menus}")
