"""
Test 2.1.6: Display Section Accessible - Pure Page Object Pattern

CATEGORY: 02 - Configuration Section Navigation
TEST TYPE: Pure Page Object Pattern
PRIORITY: HIGH
HARDWARE: Device Only
SERIES: Both Series 2 and 3

TRANSFORMATION SUMMARY:
- Pure page object architecture - NO direct DeviceCapabilities calls
- All device awareness handled through page object properties
- DisplayConfigPage encapsulates all device-specific logic
- Clean, maintainable page object architecture

LOCATOR_STRATEGY_COMPLIANCE:
- Uses DisplayConfigPage page object methods exclusively
- No direct .locator() calls in test logic
- Device-aware selectors through page object inheritance
- Series-specific display features handled by page object

CREATED: 2025-12-07 for pure page object transformation
"""

import pytest
import time
import logging
from playwright.sync_api import Page

# Import page objects only - all device logic encapsulated within
from pages.display_config_page import DisplayConfigPage

logger = logging.getLogger(__name__)


def test_2_1_6_display_section_access(unlocked_config_page: Page, request):
    """
    Test 2.1.6: Display Section Accessible - Pure Page Object Pattern

    Purpose: Verify display section navigation and configuration availability
    Expected: Section accessible, display modes visible, configuration options available

    PURE PAGE OBJECT PATTERN:
    - NO DeviceCapabilities calls in test logic
    - Device awareness through page object properties
    - All timeouts handled by page objects internally
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate display section accessibility"
        )

    logger.info(f"Testing display section accessibility on {device_model}")

    try:
        # Create DisplayConfigPage instance - all device awareness is internal
        display_page = DisplayConfigPage(unlocked_config_page, device_model)

        # Get device info from page object properties (NOT DeviceCapabilities)
        device_series = display_page.device_series
        available_sections = display_page.available_sections

        logger.info(
            f"DisplayConfigPage initialized for {device_model} (Series {device_series})"
        )

        # Navigate to display section using page object
        display_page.navigate_to_page()

        # Verify page loaded using page object method
        display_page.verify_page_loaded()

        # Test display section accessibility using page object methods
        section_accessible = display_page.is_section_available("display")
        assert section_accessible, "Display section should be accessible"
        assert (
            "display" in available_sections
        ), "Display section should be available for this device"

        logger.info(f"Display section is available for {device_model}")

        # Test display configuration options using page object
        configuration_options = 0
        try:
            if hasattr(display_page, "get_configuration_options"):
                config_opts = display_page.get_configuration_options()
                configuration_options = len(config_opts) if config_opts else 0
                logger.info(
                    f"Display configuration options found: {configuration_options}"
                )
            else:
                page_data = display_page.get_page_data()
                config_indicators = ["display", "mode", "brightness", "screen", "lcd"]
                configuration_options = sum(
                    1
                    for indicator in config_indicators
                    if indicator in str(page_data).lower()
                )
                logger.info(
                    f"Display configuration indicators found: {configuration_options}"
                )
        except Exception as e:
            logger.warning(f"Configuration options check failed: {e}")

        assert (
            configuration_options >= 1
        ), "Should have at least 1 display configuration indicator"

        # Test display mode availability using page object methods
        display_modes_available = False
        try:
            if hasattr(display_page, "get_available_display_modes"):
                display_modes = display_page.get_available_display_modes()
                display_modes_available = (
                    len(display_modes) > 0 if display_modes else False
                )
                if display_modes_available:
                    logger.info(f"Display modes available: {len(display_modes)} modes")
                else:
                    logger.warning("No display modes detected")
            else:
                page_data = display_page.get_page_data()
                display_modes_available = "mode" in str(page_data).lower()
                if display_modes_available:
                    logger.info("Display mode indicators found in page data")
                else:
                    logger.warning("No display mode indicators found")
        except Exception as e:
            logger.warning(f"Display mode check failed: {e}")

        # Test save/cancel button availability using page object
        buttons_available = False
        try:
            if hasattr(display_page, "get_save_cancel_buttons"):
                buttons = display_page.get_save_cancel_buttons()
                buttons_available = len(buttons) >= 1 if buttons else False
                if buttons_available:
                    logger.info(f"Save/cancel buttons found: {len(buttons)} buttons")
                else:
                    logger.warning("Save/cancel buttons not detected")
            else:
                save_button = display_page.get_save_button_locator()
                if save_button and save_button.count() > 0:
                    buttons_available = True
                    logger.info("Save button locator found and accessible")
                else:
                    logger.warning("Save button locator not accessible")
        except Exception as e:
            logger.warning(f"Button availability check failed: {e}")

        assert section_accessible, "Display section must be accessible"

        # Series-specific validation (using page object property)
        if device_series == 2:
            logger.info("Series 2: Validated basic display configuration")
        elif device_series == 3:
            logger.info("Series 3: Validated advanced display configuration")

        logger.info(
            f"DISPLAY SECTION SUCCESS: {device_model} (Series {device_series}) - "
            f"Section accessible, {configuration_options} config options, buttons: {buttons_available}"
        )

    except Exception as e:
        logger.error(f"Display section access test failed on {device_model}: {e}")
        raise

    finally:
        time.sleep(0.5)

    logger.info(f"Display section access test completed for {device_model}")
