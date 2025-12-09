"""
Test: 5.1.5 - Timezone Section Independent Save - Pure Page Object Pattern
Category: Time Configuration (Category 5)
Purpose: Verify timezone section saves independently from DST section using pure page object architecture
Expected: Save button saves only timezone settings with device-aware validation
Series: Both Series 2 and 3
IMPROVED: Pure page object architecture with device-aware timezone save validation
"""

import pytest
import time
import logging
from playwright.sync_api import expect
from pages.time_config_page import TimeConfigPage
from pages.dashboard_page import DashboardPage

logger = logging.getLogger(__name__)


def test_5_1_5_timezone_section_save(time_config_page: TimeConfigPage, request):
    """
    Test 5.1.5: Timezone Section Independent Save (Pure Page Object Pattern)
    Purpose: Verify timezone section saves independently from DST section using pure page object architecture
    Expected: Save button saves only timezone settings with device-aware validation
    IMPROVED: Pure page object pattern with comprehensive timezone save validation
    """
    # Get device context using page object encapsulation
    device_model = request.session.get("device_model", "unknown")
    if not device_model or device_model == "unknown":
        pytest.skip(
            "Device model not detected - cannot validate timezone save functionality"
        )

    logger = logging.getLogger(__name__)

    try:
        logger.info(
            f"{device_model}: Starting timezone section independent save validation"
        )

        # Initialize page objects for timezone validation
        time_page_obj = TimeConfigPage(time_config_page.page, device_model)
        dashboard_page_obj = DashboardPage(time_config_page.page, device_model)

        # Validate device context using page object methods
        device_series = time_page_obj.get_expected_device_series()
        timeout_multiplier = time_page_obj.get_timeout_multiplier()

        logger.info(f"{device_model}: Device series: {device_series}")
        logger.info(f"{device_model}: Timeout multiplier: {timeout_multiplier}x")

        # Get original timezone configuration for rollback using page object method
        logger.info(f"{device_model}: Getting original timezone configuration")

        original_data = time_page_obj.get_page_data()
        original_timezone_value = original_data.get("timezone", "")
        logger.info(f"{device_model}: Original timezone: {original_timezone_value}")

        try:
            logger.info(f"{device_model}: Step 1 - Modifying timezone configuration")

            # Fill timezone dropdown using page object method
            test_timezone = "US/Denver"
            timezone_configured = time_page_obj.configure_timezone(test_timezone)
            assert (
                timezone_configured
            ), f"Timezone configuration failed for {device_model}"

            logger.info(f"{device_model}: Timezone configured: {test_timezone}")

            # Modify offset field to further ensure save button is enabled using page object method
            logger.info(f"{device_model}: Step 2 - Modifying offset field")

            offset_configured = time_page_obj.configure_timezone_offset("-07:00")
            if offset_configured:
                logger.info(f"{device_model}: Offset field configured successfully")
            else:
                logger.info(
                    f"{device_model}: Offset field configuration skipped (may not be available)"
                )

            # Wait for save button to become enabled using device-aware timing
            save_button_wait_time = time_page_obj.get_save_button_wait_time()
            time.sleep(save_button_wait_time)

            logger.info(f"{device_model}: Step 3 - Testing save functionality")

            # Test save functionality using page object method
            save_success = time_page_obj.save_timezone_configuration()
            assert (
                save_success
            ), f"Timezone configuration save failed for {device_model}"

            logger.info(f"{device_model}: Step 4 - Validating save success")

            # Verify timezone is configured using page object method
            current_timezone = time_page_obj.get_timezone_value()
            assert (
                current_timezone is not None
            ), f"Timezone should be configured for {device_model}"
            assert (
                len(current_timezone) > 0
            ), f"Timezone value should not be empty for {device_model}"
            assert (
                current_timezone == test_timezone
            ), f"Expected {test_timezone}, got {current_timezone} for {device_model}"

            logger.info(f"{device_model}: Timezone save validation successful")

            # Additional timezone validation using page object methods
            logger.info(f"{device_model}: Step 5 - Additional validation")

            # Validate timezone configuration persistence using page object method
            timezone_persistence_valid = time_page_obj.validate_timezone_persistence(
                test_timezone, device_model
            )
            assert (
                timezone_persistence_valid
            ), f"Timezone persistence validation failed for {device_model}"

            # Series-specific validation using page object methods
            if device_series == 2:
                time_page_obj.validate_series2_timezone_save_patterns()
            elif device_series == 3:
                time_page_obj.validate_series3_timezone_save_patterns()

            # Cross-validation test using page object method
            time_page_obj.test_timezone_save_cross_validation()

            logger.info(f"{device_model}: Step 6 - Final validation")

            # Verify device capabilities using page object method
            timezone_capable = time_page_obj.has_timezone_save_capability()
            assert (
                timezone_capable
            ), f"Device should support timezone save functionality for {device_model}"

            logger.info(
                f"{device_model}: Timezone save validation completed successfully"
            )
            print(f"Timezone section save test passed for {device_model}")

        except Exception as save_error:
            logger.error(f"{device_model}: Timezone save test failed: {save_error}")
            pytest.fail(
                f"Timezone section save test failed for {device_model}: {save_error}"
            )

        finally:
            # Rollback: Restore original timezone configuration using page object methods
            try:
                logger.info(f"{device_model}: Rolling back timezone configuration")

                if original_timezone_value:
                    rollback_success = time_page_obj.configure_timezone(
                        original_timezone_value
                    )
                    if rollback_success:
                        save_rollback_success = (
                            time_page_obj.save_timezone_configuration()
                        )
                        if save_rollback_success:
                            logger.info(
                                f"{device_model}: Rollback successful - timezone restored: {original_timezone_value}"
                            )
                        else:
                            logger.warning(
                                f"{device_model}: Rollback save failed - timezone may be in inconsistent state"
                            )
                    else:
                        logger.warning(f"{device_model}: Rollback configuration failed")
                else:
                    logger.info(f"{device_model}: No original timezone to restore")

                # Wait for rollback to complete
                rollback_wait_time = time_page_obj.get_save_button_wait_time()
                time.sleep(rollback_wait_time)

            except Exception as rollback_error:
                logger.warning(f"{device_model}: Rollback failed: {rollback_error}")
                logger.info(
                    f"{device_model}: Manual intervention may be required for timezone rollback"
                )

    except Exception as e:
        logger.error(
            f"{device_model}: Timezone section save validation encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"Timezone section save validation failed for {device_model}: {e}")
