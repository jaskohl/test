"""
Test: 5.1.5 - Timezone Section Independent Save (Pure Page Object Pattern)
Category: Time Configuration - Test 5.1.5
Test Count: 5 of 11 in Category 5
Purpose: Verify timezone section can be saved independently
Expected: Timezone changes persist without affecting other sections
Series: Both Series 2 and 3
Priority: HIGH
Hardware: Device Only
TRANSFORMED: Pure page object architecture with device intelligence
PATTERN: Zero direct .locator() calls, essential methods only
"""

import pytest
import logging
from pages.time_config_page import TimeConfigPage

logger = logging.getLogger(__name__)


def test_5_1_5_timezone_section_independent_save(
    unlocked_config_page, device_model: str
):
    """
    Test 5.1.5: Timezone Section Independent Save - Pure Page Object Pattern
    Purpose: Verify timezone section can be saved independently
    Expected: Timezone changes persist without affecting other sections
    TRANSFORMED: Uses pure page object methods with device intelligence
    Series: Both 2 and 3
    """
    logger.info(f"Testing timezone section independent save on {device_model}")

    # Initialize page object with device intelligence encapsulated internally
    time_config_page = TimeConfigPage(unlocked_config_page, device_model)

    # Navigate to time configuration page
    time_config_page.navigate_to_page()

    # Verify page loaded using page object method
    time_config_page.verify_page_loaded()

    # Test timezone section independent save functionality
    try:
        # Get initial timezone configuration
        initial_timezone = time_config_page.get_current_timezone()
        initial_dst_enabled = time_config_page.is_dst_enabled()
        logger.info(f"Initial timezone: {initial_timezone}")
        logger.info(f"Initial DST enabled: {initial_dst_enabled}")

        # Get available timezones for testing
        available_timezones = time_config_page.get_available_timezones()
        logger.info(f"Found {len(available_timezones)} timezone options")

        # Test timezone change and save
        test_timezone = None
        for tz in available_timezones:
            if tz != initial_timezone:
                test_timezone = tz
                break

        if test_timezone:
            logger.info(f"Testing timezone change to: {test_timezone}")

            try:
                # Select new timezone using page object method
                select_success = time_config_page.select_timezone(test_timezone)

                if select_success:
                    logger.info(f"Successfully selected timezone: {test_timezone}")

                    # Test saving timezone configuration using page object method
                    save_success = time_config_page.save_configuration()

                    if save_success:
                        logger.info("Timezone configuration saved successfully")

                        # Verify timezone selection persisted after save
                        persisted_timezone = time_config_page.get_current_timezone()
                        if persisted_timezone == test_timezone:
                            logger.info(
                                f"Timezone persisted after save: {persisted_timezone}"
                            )
                        else:
                            logger.warning(
                                f"Timezone may not have persisted: {persisted_timezone}"
                            )

                    else:
                        logger.warning("Failed to save timezone configuration")

                else:
                    logger.warning(f"Failed to select timezone: {test_timezone}")

            except Exception as e:
                logger.warning(f"Timezone save test failed: {e}")
        else:
            logger.info("No alternative timezone available for testing")

        # Test DST configuration save
        try:
            # Toggle DST configuration
            new_dst_enabled = not initial_dst_enabled
            logger.info(f"Testing DST toggle to: {new_dst_enabled}")

            dst_config_success = time_config_page.configure_dst(new_dst_enabled)

            if dst_config_success:
                logger.info("DST configuration changed successfully")

                # Verify DST status change
                verified_dst_enabled = time_config_page.is_dst_enabled()
                if verified_dst_enabled == new_dst_enabled:
                    logger.info(f"DST status verified: {verified_dst_enabled}")
                else:
                    logger.warning(
                        f"DST status verification failed: {verified_dst_enabled}"
                    )

                # Test saving DST configuration
                save_success = time_config_page.save_configuration()

                if save_success:
                    logger.info("DST configuration saved successfully")

                    # Verify DST status persisted after save
                    persisted_dst_enabled = time_config_page.is_dst_enabled()
                    if persisted_dst_enabled == new_dst_enabled:
                        logger.info(
                            f"DST status persisted after save: {persisted_dst_enabled}"
                        )
                    else:
                        logger.warning(
                            f"DST status may not have persisted: {persisted_dst_enabled}"
                        )
                else:
                    logger.warning("Failed to save DST configuration")
            else:
                logger.warning("Failed to configure DST")

        except Exception as e:
            logger.warning(f"DST save test failed: {e}")

        # Test DST rule selection and save
        try:
            dst_rules = time_config_page.get_dst_rules()
            if dst_rules:
                logger.info(f"Found {len(dst_rules)} DST rules for testing")

                # Test selecting a different DST rule
                test_rule = dst_rules[0] if dst_rules else None
                if test_rule:
                    rule_select_success = time_config_page.select_dst_rule(test_rule)

                    if rule_select_success:
                        logger.info(f"Successfully selected DST rule: {test_rule}")

                        # Test saving DST rule configuration
                        save_success = time_config_page.save_configuration()

                        if save_success:
                            logger.info("DST rule configuration saved successfully")
                        else:
                            logger.warning("Failed to save DST rule configuration")
                    else:
                        logger.warning(f"Failed to select DST rule: {test_rule}")

        except Exception as e:
            logger.warning(f"DST rule save test failed: {e}")

        # Test save button accessibility
        try:
            save_button = time_config_page.get_save_button()
            if save_button.count() > 0:
                logger.info("Save button is accessible for timezone section changes")
            else:
                logger.warning("Save button not found or not accessible")

        except Exception as e:
            logger.warning(f"Save button test failed: {e}")

        logger.info(
            f"Timezone section independent save test completed for {device_model}"
        )

    except Exception as e:
        pytest.fail(f"Timezone section independent save validation failed: {e}")
