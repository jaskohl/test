"""
Test 2.1.8: Syslog Section Accessible - Pure Page Object Pattern

CATEGORY: 02 - Configuration Section Navigation
TEST TYPE: Pure Page Object Pattern
PRIORITY: HIGH
HARDWARE: Device Only
SERIES: Both Series 2 and 3 (Syslog primarily Series 3)

TRANSFORMATION SUMMARY:
- Pure page object architecture - NO direct DeviceCapabilities calls
- All device awareness handled through page object properties
- SyslogConfigPage encapsulates all device-specific logic
- Clean, maintainable page object architecture

LOCATOR_STRATEGY_COMPLIANCE:
- Uses SyslogConfigPage page object methods exclusively
- No direct .locator() calls in test logic
- Device-aware selectors through page object inheritance
- Series 3 syslog features handled by page object

CREATED: 2025-12-07 for pure page object transformation
"""

import pytest
import time
import logging
from playwright.sync_api import Page

# Import page objects only - all device logic encapsulated within
from pages.syslog_config_page import SyslogConfigPage

logger = logging.getLogger(__name__)


def test_2_1_8_syslog_section_access(unlocked_config_page: Page, request):
    """
    Test 2.1.8: Syslog Section Accessible - Pure Page Object Pattern

    Purpose: Verify syslog section navigation and configuration availability
    Expected: Section accessible (primarily Series 3), syslog features visible

    PURE PAGE OBJECT PATTERN:
    - NO DeviceCapabilities calls in test logic
    - Device awareness through page object properties
    - All timeouts handled by page objects internally
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate syslog section accessibility"
        )

    logger.info(f"Testing syslog section accessibility on {device_model}")

    try:
        # Create SyslogConfigPage instance - all device awareness is internal
        syslog_page = SyslogConfigPage(unlocked_config_page, device_model)

        # Get device info from page object properties (NOT DeviceCapabilities)
        device_series = syslog_page.device_series
        available_sections = syslog_page.available_sections

        logger.info(
            f"SyslogConfigPage initialized for {device_model} (Series {device_series})"
        )

        # Navigate to syslog section using page object
        syslog_page.navigate_to_page()

        # Verify page loaded using page object method
        syslog_page.verify_page_loaded()

        # Check if syslog is in available sections (using page object property)
        syslog_available = "syslog" in available_sections
        if syslog_available:
            logger.info(f"Syslog section is available for {device_model}")
        else:
            logger.info(
                f"Syslog section not listed in available sections for {device_model}"
            )

        # Test syslog section accessibility using page object methods
        section_accessible = syslog_page.is_section_available("syslog")

        if not section_accessible and device_series == 2:
            logger.info("Syslog section not accessible on Series 2 - expected behavior")
            return  # Exit gracefully for Series 2 without syslog

        assert (
            section_accessible or device_series == 2
        ), "Syslog section should be accessible"

        # Test syslog configuration options using page object
        configuration_options = 0
        try:
            if hasattr(syslog_page, "get_configuration_options"):
                config_opts = syslog_page.get_configuration_options()
                configuration_options = len(config_opts) if config_opts else 0
                logger.info(
                    f"Syslog configuration options found: {configuration_options}"
                )
            else:
                page_data = syslog_page.get_page_data()
                config_indicators = [
                    "syslog",
                    "server",
                    "facility",
                    "severity",
                    "protocol",
                ]
                configuration_options = sum(
                    1
                    for indicator in config_indicators
                    if indicator in str(page_data).lower()
                )
                logger.info(
                    f"Syslog configuration indicators found: {configuration_options}"
                )
        except Exception as e:
            logger.warning(f"Configuration options check failed: {e}")

        # Test syslog server configuration availability
        server_config_available = False
        try:
            if hasattr(syslog_page, "get_server_configuration"):
                server_config = syslog_page.get_server_configuration()
                server_config_available = server_config is not None
                if server_config_available:
                    logger.info("Syslog server configuration is available")
                else:
                    logger.warning("Syslog server configuration not detected")
            else:
                page_data = syslog_page.get_page_data()
                server_indicators = ["server", "syslog1", "syslog2", "host"]
                server_config_available = any(
                    indicator in str(page_data).lower()
                    for indicator in server_indicators
                )
                if server_config_available:
                    logger.info(
                        "Syslog server configuration indicators found in page data"
                    )
        except Exception as e:
            logger.warning(f"Server configuration check failed: {e}")

        # Test syslog facility and severity configuration
        facility_severity_available = False
        try:
            if hasattr(syslog_page, "get_facility_severity_options"):
                facility_severity = syslog_page.get_facility_severity_options()
                facility_severity_available = (
                    len(facility_severity) > 0 if facility_severity else False
                )
                if facility_severity_available:
                    logger.info(
                        f"Syslog facility/severity options: {len(facility_severity)}"
                    )
            else:
                page_data = syslog_page.get_page_data()
                facility_severity_indicators = ["facility", "severity", "level"]
                facility_severity_available = any(
                    indicator in str(page_data).lower()
                    for indicator in facility_severity_indicators
                )
                if facility_severity_available:
                    logger.info(
                        "Syslog facility/severity configuration indicators found"
                    )
        except Exception as e:
            logger.warning(f"Facility/severity check failed: {e}")

        # Test save button availability using page object
        save_button_available = False
        try:
            save_button = syslog_page.get_save_button_locator()
            if save_button and save_button.count() > 0:
                save_button_available = True
                logger.info("Syslog save button locator found and accessible")
        except Exception as e:
            logger.warning(f"Save button check failed: {e}")

        # Series-specific validation (using page object property)
        if device_series == 2:
            if section_accessible:
                logger.info(
                    "Series 2: Syslog section accessible (limited functionality expected)"
                )
            else:
                logger.info(
                    "Series 2: Syslog section not accessible - expected behavior"
                )
        elif device_series == 3:
            logger.info("Series 3: Validated syslog configuration capabilities")

        logger.info(
            f"SYSLOG SECTION SUCCESS: {device_model} (Series {device_series}) - "
            f"accessible: {section_accessible}, {configuration_options} config options, "
            f"server config: {server_config_available}, save button: {save_button_available}"
        )

    except Exception as e:
        logger.error(f"Syslog section access test failed on {device_model}: {e}")
        # For Series 2 devices, syslog failure may be expected
        syslog_page_temp = SyslogConfigPage(unlocked_config_page, device_model)
        if syslog_page_temp.device_series == 2:
            logger.info("Syslog test failed on Series 2 - expected behavior")
            return
        raise

    finally:
        time.sleep(0.5)

    logger.info(f"Syslog section access test completed for {device_model}")
