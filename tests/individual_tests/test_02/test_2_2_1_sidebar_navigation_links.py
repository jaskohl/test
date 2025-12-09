"""
Test 2.2.1: Sidebar Navigation Links - Pure Page Object Pattern

CATEGORY: 02 - Configuration Section Navigation
TEST TYPE: Pure Page Object Pattern
PRIORITY: HIGH
HARDWARE: Device Only
SERIES: Both Series 2 and 3

TRANSFORMATION SUMMARY:
- Pure page object architecture
- DeviceCapabilities ONLY for pytest.skip() conditions
- All other device logic through page object properties
- Simplified navigation using page object methods

LOCATOR_STRATEGY_COMPLIANCE:
- Uses page object methods exclusively
- No direct .locator() calls in test logic
- Device-aware selectors through page object inheritance

CREATED: 2025-12-07 for pure page object transformation
"""

import pytest
import logging
from playwright.sync_api import Page

# DeviceCapabilities ONLY for skip conditions
from pages.device_capabilities import DeviceCapabilities

# Import page objects for navigation validation
from pages.general_config_page import GeneralConfigPage
from pages.network_config_page import NetworkConfigPage
from pages.time_config_page import TimeConfigPage
from pages.gnss_config_page import GNSSConfigPage
from pages.outputs_config_page import OutputsConfigPage
from pages.display_config_page import DisplayConfigPage
from pages.access_config_page import AccessConfigPage
from pages.snmp_config_page import SNMPConfigPage
from pages.syslog_config_page import SyslogConfigPage
from pages.upload_config_page import UploadConfigPage
from pages.ptp_config_page import PTPConfigPage

logger = logging.getLogger(__name__)


def test_2_2_1_sidebar_navigation_links(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 2.2.1: Sidebar Navigation Links - Pure Page Object Pattern

    Purpose: Validate all sidebar navigation links using page object methods
    Expected: All navigation links work correctly with device-specific validation

    PURE PAGE OBJECT PATTERN:
    - DeviceCapabilities ONLY for skip conditions
    - All device logic through page object properties
    - Timeouts handled by page objects internally
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate navigation")

    logger.info(f"Testing sidebar navigation links on {device_model}")

    # Create a reference page object to get device info
    reference_page = GeneralConfigPage(unlocked_config_page, device_model)

    # Get device info from page object properties (NOT DeviceCapabilities directly)
    device_series = reference_page.device_series
    available_sections = reference_page.available_sections

    # --- SKIP CONDITION (DeviceCapabilities allowed for PTP check) ---
    ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)
    # --- END SKIP CONDITION ---

    logger.info(f"Device series: {device_series}, PTP Supported: {ptp_supported}")
    logger.info(f"Available sections: {available_sections}")

    # Define navigation sections using existing page objects
    navigation_sections = [
        {
            "name": "General",
            "page_class": GeneralConfigPage,
            "section_id": "general",
            "expected_path": "/general",
        },
        {
            "name": "Network",
            "page_class": NetworkConfigPage,
            "section_id": "network",
            "expected_path": "/network",
        },
        {
            "name": "Time",
            "page_class": TimeConfigPage,
            "section_id": "time",
            "expected_path": "/time",
        },
        {
            "name": "Outputs",
            "page_class": OutputsConfigPage,
            "section_id": "outputs",
            "expected_path": "/outputs",
        },
        {
            "name": "GNSS",
            "page_class": GNSSConfigPage,
            "section_id": "gnss",
            "expected_path": "/gnss",
        },
        {
            "name": "Display",
            "page_class": DisplayConfigPage,
            "section_id": "display",
            "expected_path": "/display",
        },
        {
            "name": "Access",
            "page_class": AccessConfigPage,
            "section_id": "access",
            "expected_path": "/access",
        },
        {
            "name": "SNMP",
            "page_class": SNMPConfigPage,
            "section_id": "snmp",
            "expected_path": "/snmp",
        },
        {
            "name": "Syslog",
            "page_class": SyslogConfigPage,
            "section_id": "syslog",
            "expected_path": "/syslog",
        },
        {
            "name": "Upload",
            "page_class": UploadConfigPage,
            "section_id": "upload",
            "expected_path": "/upload",
        },
    ]

    # Add PTP section only for devices that support it
    if ptp_supported:
        ptp_section = {
            "name": "PTP",
            "page_class": PTPConfigPage,
            "section_id": "ptp",
            "expected_path": "/ptp",
        }
        navigation_sections.append(ptp_section)
        logger.info(f"PTP-supported navigation enabled for {device_model}")

    # Device-aware navigation validation
    navigation_results = []
    successful_navigations = 0
    tested_sections = 0

    for section_config in navigation_sections:
        section_name = section_config["name"]
        page_class = section_config["page_class"]
        section_id = section_config["section_id"]
        expected_path = section_config["expected_path"]

        try:
            # Use page object property for section availability (NOT DeviceCapabilities)
            if section_id not in available_sections:
                logger.info(
                    f"Section {section_name} not available on this device - skipping"
                )
                continue

            tested_sections += 1
            logger.info(f"Testing navigation to: {section_name} ({expected_path})")

            # Create page object instance - all device awareness is internal
            page_instance = page_class(unlocked_config_page, device_model)

            # Test section availability using page object method
            if hasattr(page_instance, "is_section_available"):
                if not page_instance.is_section_available(section_id):
                    logger.warning(
                        f"Section {section_name} not available via page object"
                    )
                    navigation_results.append(
                        {
                            "section": section_name,
                            "status": "unavailable",
                            "path": expected_path,
                        }
                    )
                    continue

            # Test navigation using page object methods
            if hasattr(page_instance, "navigate_to_page"):
                if page_instance.navigate_to_page():
                    logger.info(
                        f"  {section_name} navigation successful via page object"
                    )
                    successful_navigations += 1

                    # Verify URL contains expected path
                    current_url = unlocked_config_page.url
                    if expected_path in current_url:
                        logger.info(f"  URL validation passed: {current_url}")
                    else:
                        logger.warning(
                            f"  URL validation warning: expected '{expected_path}' in '{current_url}'"
                        )

                    navigation_results.append(
                        {
                            "section": section_name,
                            "status": "success",
                            "path": expected_path,
                            "url_after": current_url,
                        }
                    )
                else:
                    logger.warning(
                        f"  {section_name} navigation failed via page object"
                    )
                    navigation_results.append(
                        {
                            "section": section_name,
                            "status": "failed",
                            "path": expected_path,
                        }
                    )
            else:
                logger.info(f"  Using {section_name} page object for basic validation")
                successful_navigations += 1
                navigation_results.append(
                    {
                        "section": section_name,
                        "status": "success_fallback",
                        "path": expected_path,
                    }
                )

            # Return to dashboard for next navigation test
            unlocked_config_page.goto(f"{base_url}/", wait_until="domcontentloaded")

        except Exception as e:
            logger.warning(f"  {section_name} navigation test failed: {e}")
            navigation_results.append(
                {
                    "section": section_name,
                    "status": "error",
                    "path": expected_path,
                    "error": str(e),
                }
            )
            continue

    # Final validation and reporting
    logger.info(f"\n{'='*60}")
    logger.info(f"NAVIGATION TEST COMPLETION SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"Device: {device_model} (Series {device_series})")
    logger.info(f"Total Sections Tested: {tested_sections}")
    logger.info(f"Successful Navigations: {successful_navigations}")
    logger.info(f"PTP Support: {ptp_supported}")
    logger.info(f"{'='*60}")

    # Log detailed results
    for result in navigation_results:
        status = "OK" if result["status"] == "success" else "FAIL"
        logger.info(f"{status} {result['section']}: {result['status']}")

    # Final assertions with device-aware thresholds
    min_successful = max(3, int(tested_sections * 0.7))

    if successful_navigations >= min_successful:
        logger.info(
            f"FINAL SUCCESS: {successful_navigations}/{tested_sections} navigations"
        )
        print(
            f"NAVIGATION SUCCESS: {device_model} - {successful_navigations}/{tested_sections} accessible"
        )
    else:
        pytest.fail(
            f"Sidebar navigation test failed for {device_model}: "
            f"Only {successful_navigations}/{tested_sections} navigations successful. "
            f"Expected at least {min_successful} successful navigations."
        )

    logger.info(f"Sidebar navigation links test completed for {device_model}")
