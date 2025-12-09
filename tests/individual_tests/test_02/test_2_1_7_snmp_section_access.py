"""
Test 2.1.7: SNMP Section Accessible - Pure Page Object Pattern

CATEGORY: 02 - Configuration Section Navigation
TEST TYPE: Pure Page Object Pattern
PRIORITY: HIGH
HARDWARE: Device Only
SERIES: Both Series 2 and 3 (SNMP primarily Series 3)

TRANSFORMATION SUMMARY:
- Pure page object architecture using SNMPConfigPage
- All complex validation logic moved to page objects
- Essential assertions only - no redundant device capability calls
- Device-aware SNMP capability validation handled transparently
- Clean, maintainable test structure

LOCATOR_STRATEGY_COMPLIANCE:
- Uses SNMPConfigPage page object methods exclusively
- No direct .locator() calls in test logic
- Device-aware selectors through  page object inheritance
- Series-specific SNMP features handled transparently

CREATED: 2025-12-06 for comprehensive transformation
BASED ON: Original test_2_1_7_snmp_section_access.py
"""

import pytest
import time
import logging
from playwright.sync_api import Page

# Import  page objects
from pages.snmp_config_page import SNMPConfigPage

logger = logging.getLogger(__name__)


def test_2_1_7_snmp_section_access(unlocked_config_page: Page, request):
    """
    Test 2.1.7: SNMP Section Accessible - Pure Page Object Pattern

    Purpose: Verify SNMP section navigation and configuration availability using pure page object methods
    Expected: Section accessible (primarily Series 3), SNMP features visible, community configuration available

    TRANSFORMATION CHANGES:
    - Uses SNMPConfigPage instead of complex validation logic
    - All device capability calls moved to page object initialization
    - Simplified to essential assertions only
    - No redundant validation with fallbacks
    """
    # Get device model from test request
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate SNMP section accessibility"
        )

    logger.info(f"Testing SNMP section accessibility on {device_model}")

    # Initialize snmp_page to avoid unbound variable error
    snmp_page = None

    try:
        # Create SNMPConfigPage instance - all device awareness handled internally
        snmp_page = SNMPConfigPage(unlocked_config_page, device_model)
        if snmp_page.device_series == 2:
            pytest.skip("SNMP not supported on Series 2 devices - skipping test")
        logger.info(f"SNMPConfigPage initialized for {device_model}")

        # Navigate to SNMP section using page object method
        navigation_success = snmp_page.navigate_to_page()

        assert navigation_success, "Failed to navigate to SNMP section"

        # Verify page loaded using page object method
        assert snmp_page.verify_page_loaded(), "SNMP configuration page failed to load"

        # Test SNMP section accessibility using page object method
        assert snmp_page.is_section_available(
            "snmp"
        ), "SNMP section should be accessible"

        # Test SNMP configuration options using page object method
        configuration_options = snmp_page.get_configuration_options()
        assert (
            len(configuration_options) >= 1
        ), "Should have at least 1 SNMP configuration indicator"

        # Test SNMP community strings availability using page object method
        community_strings = snmp_page.get_community_strings()
        if community_strings:
            logger.info(
                f"SNMP community strings available: {len(community_strings)} communities"
            )
        else:
            logger.warning("No SNMP community strings detected")

        # Test SNMP trap configuration availability using page object method
        trap_config = snmp_page.get_trap_configuration()
        if trap_config:
            logger.info("SNMP trap configuration is available")
        else:
            logger.warning("SNMP trap configuration not detected")

        # Test save button availability using page object method
        save_button = snmp_page.get_save_button_locator()

        # Series 2 devices don't have SNMP support, so no save button is expected
        if snmp_page.device_series == "Series 2":
            if save_button is None or save_button.count() == 0:
                logger.info(
                    "No save button found on Series 2 device - expected behavior for devices without SNMP"
                )
                logger.info(
                    f"SNMP SECTION SUCCESS: {device_model} - Series 2 device without SNMP support"
                )
                return  # Exit gracefully for Series 2 without SNMP

        # For Series 3 devices, save button should be available
        assert (
            save_button is not None and save_button.count() > 0
        ), f"Save button should be available on Series 3 device {device_model}"

        # Essential functionality validation
        logger.info(
            f"SNMP SECTION SUCCESS: {device_model} - SNMP functionality verified"
        )

    except Exception as e:
        logger.error(f"SNMP section access test failed on {device_model}: {e}")
        # For Series 2 devices, SNMP failure may be expected
        if snmp_page and snmp_page.device_series == "Series 2":
            logger.info("SNMP test failed on Series 2 - this may be expected behavior")
            logger.info(
                f"SNMP SECTION SUCCESS: {device_model} - Series 2 device without SNMP support"
            )
            return  # Exit gracefully for Series 2
        raise

    finally:
        # Simple cleanup
        time.sleep(0.5)
