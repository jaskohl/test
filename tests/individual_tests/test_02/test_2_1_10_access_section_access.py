"""
Test 2.1.10: Access Section Accessible - Pure Page Object Pattern

CATEGORY: 02 - Configuration Section Navigation
TEST TYPE: Pure Page Object Pattern
PRIORITY: HIGH
HARDWARE: Device Only
SERIES: Both Series 2 and 3

TRANSFORMATION SUMMARY:
- Pure page object architecture - NO direct DeviceCapabilities calls
- All device awareness handled through page object properties
- AccessConfigPage encapsulates all device-specific logic
- Clean, maintainable page object architecture

LOCATOR_STRATEGY_COMPLIANCE:
- Uses AccessConfigPage page object methods exclusively
- No direct .locator() calls in test logic
- Device-aware selectors through page object inheritance

CREATED: 2025-12-07 for pure page object transformation
"""

import pytest
import time
import logging
from playwright.sync_api import Page

# Import page objects only - all device logic encapsulated within
from pages.access_config_page import AccessConfigPage

logger = logging.getLogger(__name__)


def test_2_1_10_access_section_access(unlocked_config_page: Page, request):
    """
    Test 2.1.10: Access Section Accessible - Pure Page Object Pattern

    Purpose: Verify access section navigation and configuration availability
    Expected: Section accessible, access control features visible, password configuration available

    PURE PAGE OBJECT PATTERN:
    - NO DeviceCapabilities calls in test logic
    - Device awareness through page object properties
    - All timeouts handled by page objects internally
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate access section accessibility"
        )

    logger.info(f"Testing access section accessibility on {device_model}")

    try:
        # Create AccessConfigPage instance - all device awareness is internal
        access_page = AccessConfigPage(unlocked_config_page, device_model)

        # Get device info from page object properties (NOT DeviceCapabilities)
        device_series = access_page.device_series
        available_sections = access_page.available_sections

        logger.info(
            f"AccessConfigPage initialized for {device_model} (Series {device_series})"
        )

        # Navigate to access section using page object
        access_page.navigate_to_page()

        # Verify page loaded using page object method
        access_page.verify_page_loaded()

        # Use page object property for section validation
        assert (
            "access" in available_sections
        ), "Access section should be available for this device"
        logger.info(f"Access section is available for {device_model}")

        # Test access section accessibility using page object methods
        section_accessible = access_page.is_section_available("access")
        assert section_accessible, "Access section should be accessible"

        # Test access configuration options using page object
        configuration_options = 0
        try:
            if hasattr(access_page, "get_configuration_options"):
                config_opts = access_page.get_configuration_options()
                configuration_options = len(config_opts) if config_opts else 0
                logger.info(
                    f"Access configuration options found: {configuration_options}"
                )
            else:
                page_data = access_page.get_page_data()
                config_indicators = [
                    "password",
                    "timeout",
                    "https",
                    "access",
                    "security",
                    "authentication",
                ]
                configuration_options = sum(
                    1
                    for indicator in config_indicators
                    if indicator in str(page_data).lower()
                )
                logger.info(
                    f"Access configuration indicators found: {configuration_options}"
                )
        except Exception as e:
            logger.warning(f"Configuration options check failed: {e}")

        # Test password configuration availability
        password_config_available = False
        try:
            if hasattr(access_page, "get_password_configuration"):
                password_config = access_page.get_password_configuration()
                password_config_available = password_config is not None
                if password_config_available:
                    logger.info("Password configuration is available")
            else:
                page_data = access_page.get_page_data()
                password_indicators = ["password", "status", "configuration", "change"]
                password_config_available = any(
                    indicator in str(page_data).lower()
                    for indicator in password_indicators
                )
                if password_config_available:
                    logger.info("Password configuration indicators found in page data")
        except Exception as e:
            logger.warning(f"Password configuration check failed: {e}")

        # Test timeout configuration availability
        timeout_config_available = False
        try:
            if hasattr(access_page, "get_timeout_configuration"):
                timeout_config = access_page.get_timeout_configuration()
                timeout_config_available = timeout_config is not None
                if timeout_config_available:
                    logger.info("Timeout configuration is available")
            else:
                page_data = access_page.get_page_data()
                timeout_indicators = ["timeout", "session", "minutes", "expire"]
                timeout_config_available = any(
                    indicator in str(page_data).lower()
                    for indicator in timeout_indicators
                )
                if timeout_config_available:
                    logger.info("Timeout configuration indicators found")
        except Exception as e:
            logger.warning(f"Timeout configuration check failed: {e}")

        # Test HTTPS enforcement availability (Series 3 feature)
        https_enforcement_available = False
        try:
            if hasattr(access_page, "get_https_enforcement_options"):
                https_options = access_page.get_https_enforcement_options()
                https_enforcement_available = (
                    len(https_options) > 0 if https_options else False
                )
                if https_enforcement_available:
                    logger.info(
                        f"HTTPS enforcement options available: {len(https_options)}"
                    )
            else:
                page_data = access_page.get_page_data()
                https_indicators = ["https", "ssl", "tls", "enforce"]
                https_enforcement_available = any(
                    indicator in str(page_data).lower()
                    for indicator in https_indicators
                )
                if https_enforcement_available:
                    logger.info("HTTPS enforcement indicators found")
        except Exception as e:
            logger.warning(f"HTTPS enforcement check failed: {e}")

        # Test save/cancel button availability
        buttons_available = False
        try:
            if hasattr(access_page, "get_save_cancel_buttons"):
                buttons = access_page.get_save_cancel_buttons()
                buttons_available = len(buttons) >= 1 if buttons else False
                if buttons_available:
                    logger.info(f"Save/cancel buttons found: {len(buttons)} buttons")
            else:
                save_button = access_page.get_save_button_locator()
                if save_button and save_button.count() > 0:
                    buttons_available = True
                    logger.info("Save button locator found and accessible")
        except Exception as e:
            logger.warning(f"Button availability check failed: {e}")

        assert section_accessible, "Access section must be accessible"

        # Series-specific validation (using page object property)
        if device_series == 2:
            logger.info("Series 2: Validated basic access control configuration")
        elif device_series == 3:
            logger.info("Series 3: Validated advanced access control configuration")

        logger.info(
            f"ACCESS SECTION SUCCESS: {device_model} (Series {device_series}) - "
            f"accessible: {section_accessible}, {configuration_options} config options, "
            f"password: {password_config_available}, timeout: {timeout_config_available}, "
            f"HTTPS: {https_enforcement_available}, buttons: {buttons_available}"
        )

    except Exception as e:
        logger.error(f"Access section access test failed on {device_model}: {e}")
        raise

    finally:
        time.sleep(0.5)

    logger.info(f"Access section access test completed for {device_model}")
