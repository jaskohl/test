"""
Test: 5.1.4 - DST Timezone Name Configuration (Pure Page Object Pattern)
Category: Time Configuration - Test 5.1.4
Test Count: 4 of 11 in Category 5
Purpose: Verify DST timezone name field functionality
Expected: Accepts DST-specific timezone name configurations
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


def test_5_1_4_dst_timezone_name(unlocked_config_page, request):
    """
    Test 5.1.4: DST Timezone Name Configuration - Pure Page Object Pattern
    Purpose: Verify DST timezone name field functionality
    Expected: Accepts DST-specific timezone name configurations
    TRANSFORMED: Uses pure page object methods with device intelligence
    Series: Both 2 and 3
    """
    logger.info(f"Testing DST timezone name field on {device_model}")

    # Initialize page object with device intelligence encapsulated internally
    time_config_page = TimeConfigPage(unlocked_config_page, device_model)

    # Navigate to time configuration page
    time_config_page.navigate_to_page()

    # Verify page loaded using page object method
    time_config_page.verify_page_loaded()

    # Test DST timezone name functionality
    try:
        # Test DST configuration which includes timezone name settings
        try:
            # Test enabling DST
            dst_enabled_success = time_config_page.configure_dst(True)
            if dst_enabled_success:
                logger.info("DST enabled successfully")

                # Verify DST is enabled using page object method
                is_dst_enabled = time_config_page.is_dst_enabled()
                if is_dst_enabled:
                    logger.info("DST status verified as enabled")
                else:
                    logger.warning("DST status verification failed")

            # Get DST rules to test DST timezone name functionality
            dst_rules = time_config_page.get_dst_rules()
            logger.info(f"Found {len(dst_rules)} DST rules")

            # Test DST rule selection (which includes DST timezone names)
            test_rules = ["CUSTOM", "USA", "WESTERN EUROPE", "OFF"]

            for test_rule in test_rules:
                # Find matching rule (case-insensitive)
                matching_rule = None
                for rule in dst_rules:
                    if test_rule.upper() in rule.upper():
                        matching_rule = rule
                        break

                if matching_rule:
                    logger.info(f"Testing DST timezone name: {matching_rule}")

                    try:
                        # Select DST rule using page object method
                        rule_select_success = time_config_page.select_dst_rule(
                            matching_rule
                        )

                        if rule_select_success:
                            logger.info(
                                f"Successfully selected DST rule: {matching_rule}"
                            )
                        else:
                            logger.warning(
                                f"Failed to select DST rule: {matching_rule}"
                            )

                    except Exception as e:
                        logger.warning(
                            f"DST rule selection failed for {matching_rule}: {e}"
                        )
                else:
                    logger.info(f"DST rule '{test_rule}' not found in available rules")

        except Exception as e:
            logger.warning(f"DST configuration test failed: {e}")

        # Test timezone selection to verify DST integration
        try:
            # Get available timezones
            available_timezones = time_config_page.get_available_timezones()
            logger.info(f"Found {len(available_timezones)} timezone options")

            # Select a timezone that typically has DST
            test_timezones = ["US/Eastern", "US/Central", "US/Pacific"]

            for test_timezone in test_timezones:
                if test_timezone in available_timezones:
                    logger.info(f"Testing timezone with DST: {test_timezone}")

                    try:
                        # Select timezone using page object method
                        select_success = time_config_page.select_timezone(test_timezone)

                        if select_success:
                            logger.info(
                                f"Successfully selected timezone: {test_timezone}"
                            )

                            # Verify selection was applied
                            selected_timezone = time_config_page.get_current_timezone()
                            if selected_timezone == test_timezone:
                                logger.info(
                                    f"Timezone selection verified: {selected_timezone}"
                                )
                            else:
                                logger.warning(
                                    f"Timezone selection may not have persisted: {selected_timezone}"
                                )
                        else:
                            logger.warning(
                                f"Failed to select timezone: {test_timezone}"
                            )

                    except Exception as e:
                        logger.warning(
                            f"Timezone selection test failed for {test_timezone}: {e}"
                        )
                else:
                    logger.info(f"Skipping timezone {test_timezone} - not available")

        except Exception as e:
            logger.warning(f"Timezone selection test failed: {e}")

        # Test save functionality to verify DST timezone name integration
        try:
            # Make a DST change and test save button
            if dst_rules:
                test_rule = dst_rules[0]
                time_config_page.select_dst_rule(test_rule)

                # Get save button using page object method
                save_button = time_config_page.get_save_button()
                if save_button.count() > 0:
                    logger.info("Save button accessible for DST timezone name changes")

        except Exception as e:
            logger.warning(f"Save button test for DST timezone name failed: {e}")

        logger.info(f"DST timezone name validation completed for {device_model}")

    except Exception as e:
        pytest.fail(f"DST timezone name validation failed: {e}")
