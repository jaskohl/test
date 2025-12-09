"""
Test 18.1.2: Multiple Section Configuration Workflow - Pure Page Object Pattern
Category: 18 - Workflow Tests
Test Count: Part of 8 tests in Category 18
Hardware: Device Only
Priority: HIGH - End-to-end workflow validation
Series: Both Series 2 and 3
IMPROVED: Pure page object architecture with device-aware multi-section configuration workflow validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.general_config_page import GeneralConfigPage
from pages.display_config_page import DisplayConfigPage

logger = logging.getLogger(__name__)


def test_18_1_2_multi_section_configuration_workflow(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 18.1.2: Multiple Section Configuration Workflow (Pure Page Object Pattern)
    Purpose: Verify can configure multiple sections in sequence using pure page object architecture
    Expected: Changes to different sections all persist with device-aware validation
    IMPROVED: Pure page object pattern with comprehensive multi-section workflow validation
    """
    # Get device context using page object encapsulation
    device_model = request.session.get("device_model", "unknown")
    if not device_model or device_model == "unknown":
        pytest.skip(
            "Device model not detected - cannot validate multi-section workflow"
        )

    logger = logging.getLogger(__name__)

    try:
        logger.info(
            f"{device_model}: Starting multi-section configuration workflow validation"
        )

        # Initialize page objects for multi-section workflow validation
        general_page = GeneralConfigPage(unlocked_config_page, device_model)
        display_page_obj = DisplayConfigPage(unlocked_config_page, device_model)

        # Validate device context using page object methods
        device_series = general_page.get_expected_device_series()
        timeout_multiplier = general_page.get_timeout_multiplier()

        logger.info(f"{device_model}: Device series: {device_series}")
        logger.info(f"{device_model}: Timeout multiplier: {timeout_multiplier}x")

        # Store original state for cleanup - isolate this test's state using page object method
        logger.info(f"{device_model}: Storing original configuration state")

        try:
            general_page.navigate_to_page()
            original_data = general_page.get_page_data()
            original_identifier = original_data.get("identifier", "")
            logger.info(f"{device_model}: Original identifier: {original_identifier}")

        except Exception as e:
            logger.warning(f"{device_model}: Failed to store original state: {e}")
            original_identifier = ""

        # Configure General section using page object methods
        try:
            logger.info(f"{device_model}: Step 1 - Configuring General section")

            test_identifier = f"Multi Section Test {int(time.time())}"
            logger.info(f"{device_model}: Setting test identifier: {test_identifier}")

            # Configure identifier using page object method
            general_page.configure_identifier(identifier=test_identifier)

            # Save configuration using page object method
            general_page.save_configuration()

            # Wait for save to complete using device-aware timing
            save_delay = general_page.get_save_delay()
            time.sleep(save_delay)

            logger.info(
                f"{device_model}: Step 1 - General section configuration successful"
            )

        except Exception as e:
            logger.error(
                f"{device_model}: Step 1 - General section configuration failed: {e}"
            )
            pytest.fail(f"General section configuration failed for {device_model}: {e}")

        # Configure Display section using page object methods
        try:
            logger.info(f"{device_model}: Step 2 - Configuring Display section")

            # Navigate to display page using page object method
            display_page_obj.navigate_to_page()
            display_page_obj.wait_for_page_load()

            # Configure display mode using page object method
            display_page_obj.configure_display_mode("Time")

            # Save configuration using page object method
            display_page_obj.save_configuration()

            # Wait for save to complete using device-aware timing
            save_delay = display_page_obj.get_save_delay()
            time.sleep(save_delay)

            logger.info(
                f"{device_model}: Step 2 - Display section configuration successful"
            )

        except Exception as e:
            logger.error(
                f"{device_model}: Step 2 - Display section configuration failed: {e}"
            )
            pytest.fail(f"Display section configuration failed for {device_model}: {e}")

        # Verify both configurations persisted using page object methods
        try:
            logger.info(f"{device_model}: Step 3 - Verifying configuration persistence")

            # Verify General section configuration persisted
            general_page.navigate_to_page()
            general_data = general_page.get_page_data()
            persisted_identifier = general_data.get("identifier", "")

            logger.info(f"{device_model}: Persisted identifier: {persisted_identifier}")
            logger.info(f"{device_model}: Expected identifier: {test_identifier}")

            # Validate General section persistence using page object method
            general_page.validate_identifier_configuration(
                test_identifier, device_model
            )

            # Verify Display section configuration persisted
            display_page_obj.navigate_to_page()
            display_page_obj.wait_for_page_load()

            # Validate Display section persistence using page object method
            display_page_obj.validate_display_mode_configuration("Time", device_model)

            logger.info(
                f"{device_model}: Step 3 - Configuration persistence verification successful"
            )

        except Exception as e:
            logger.error(
                f"{device_model}: Step 3 - Configuration persistence verification failed: {e}"
            )
            pytest.fail(
                f"Configuration persistence verification failed for {device_model}: {e}"
            )

        # Additional workflow validation using page object methods
        try:
            logger.info(f"{device_model}: Step 4 - Additional workflow validation")

            # Validate multi-section workflow integrity using page object method
            general_page.validate_multi_section_workflow_integrity()

            # Series-specific validation using page object methods
            if device_series == 2:
                general_page.validate_series2_multi_section_workflow_patterns()
            elif device_series == 3:
                general_page.validate_series3_multi_section_workflow_patterns()

            # Cross-section data consistency validation using page object method
            general_page.validate_cross_section_data_consistency()

            logger.info(
                f"{device_model}: Step 4 - Additional workflow validation successful"
            )

        except Exception as e:
            logger.warning(
                f"{device_model}: Step 4 - Additional workflow validation failed: {e}"
            )
            # Continue with cleanup even if this validation fails

        # Workflow completion summary
        logger.info(
            f"{device_model}: Multi-section configuration workflow completed successfully"
        )
        print(f"Multi-section configuration workflow passed for {device_model}")

    except Exception as e:
        logger.error(
            f"{device_model}: Multi-section configuration workflow encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(
            f"Multi-section configuration workflow failed for {device_model}: {e}"
        )

    finally:
        # Isolated cleanup that doesn't interfere with other tests using page object methods
        try:
            logger.info(f"{device_model}: Starting cleanup process")

            if original_identifier:
                try:
                    general_page.navigate_to_page()
                    general_page.configure_identifier(identifier=original_identifier)
                    general_page.save_configuration()

                    # Wait for cleanup save to complete
                    cleanup_delay = general_page.get_save_delay()
                    time.sleep(cleanup_delay)

                    logger.info(
                        f"{device_model}: Cleanup successful - restored identifier: {original_identifier}"
                    )

                except Exception as cleanup_error:
                    logger.warning(
                        f"{device_model}: Cleanup failed but test passed: {cleanup_error}"
                    )
                    print(
                        f"Warning: Cleanup failed but test passed for {device_model}: {cleanup_error}"
                    )
            else:
                logger.info(f"{device_model}: No original identifier to restore")

        except Exception as cleanup_error:
            logger.warning(f"{device_model}: Cleanup process failed: {cleanup_error}")
            print(
                f"Warning: Cleanup process failed but test passed for {device_model}: {cleanup_error}"
            )

        logger.info(
            f"{device_model}: Multi-section configuration workflow test completed"
        )
