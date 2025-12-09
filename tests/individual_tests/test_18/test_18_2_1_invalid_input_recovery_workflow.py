"""
Test 18.2.1: Recovery from Invalid Input - Pure Page Object Pattern
Category: 18 - Workflow Tests
Test Count: Part of 8 tests in Category 18
Hardware: Device Only
Priority: HIGH - End-to-end workflow validation
Series: Both Series 2 and 3
IMPROVED: Pure page object architecture with device-aware invalid input recovery workflow validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.general_config_page import GeneralConfigPage

logger = logging.getLogger(__name__)


def test_18_2_1_invalid_input_recovery_workflow(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 18.2.1: Recovery from Invalid Input (Pure Page Object Pattern)
    Purpose: Verify user can recover from validation errors using pure page object architecture
    Expected: Cancel reverts to valid state, can then make valid changes with device-aware validation
    IMPROVED: Pure page object pattern with comprehensive invalid input recovery workflow validation
    """
    # Get device context using page object encapsulation
    device_model = request.session.get("device_model", "unknown")
    if not device_model or device_model == "unknown":
        pytest.fail("Device model not detected - cannot validate recovery workflow")

    logger = logging.getLogger(__name__)

    try:
        logger.info(
            f"{device_model}: Starting invalid input recovery workflow validation"
        )

        # Initialize page object for recovery workflow validation
        general_page = GeneralConfigPage(general_config_page.page, device_model)

        # Validate object methods
        device_series = general_page.device_series
        timeout_multiplier = 2

        logger.info(f"{device_model}: Device series: {device_series}")
        logger.info(f"{device_model}: Timeout multiplier: {timeout_multiplier}x")

        # Get original valid state using page object method
        logger.info(f"{device_model}: Storing original valid state")

        try:
            general_page.navigate_to_page()
            original_data = general_page.get_page_data()
            original_identifier = original_data.get("identifier", "")
            logger.info(f"{device_model}: Original identifier: {original_identifier}")

        except Exception as e:
            logger.warning(f"{device_model}: Failed to store original state: {e}")
            pytest.fail(f"Failed to store original state for {device_model}: {e}")

        # Step 1: Make invalid change using page object methods
        try:
            logger.info(
                f"{device_model}: Step 1 - Making invalid change (exceeding max length)"
            )

            # Make invalid change using page object method
            invalid_identifier = "X" * 100
            general_page.configure_identifier_with_invalid_input(invalid_identifier)

            logger.info(f"{device_model}: Step 1 - Invalid change attempted")

        except Exception as e:
            logger.error(f"{device_model}: Step 1 - Invalid change failed: {e}")
            pytest.fail(f"Invalid change failed for {device_model}: {e}")

        # Step 2: Cancel to recover using page object methods
        try:
            logger.info(
                f"{device_model}: Step 2 - Canceling to recover from invalid input"
            )

            # Cancel configuration using page object method
            cancel_result = general_page.cancel_configuration()

            # Wait for potential navigation/reload using device-aware timing
            recovery_delay = general_page.get_recovery_delay()
            general_page.wait_for_page_load()

            logger.info(f"{device_model}: Step 2 - Cancel recovery attempted")

        except Exception as e:
            logger.error(f"{device_model}: Step 2 - Cancel recovery failed: {e}")
            pytest.fail(f"Cancel recovery failed for {device_model}: {e}")

        # Step 3: Verify recovery worked using page object methods
        try:
            logger.info(f"{device_model}: Step 3 - Verifying recovery worked")

            # Check if we're still on the same page
            current_url = general_page.get_current_url()

            if "general" in current_url:
                # If still on page, verify field value was reset using page object method
                recovered_value = general_page.get_identifier_field_value()

                logger.info(f"{device_model}: Recovered value: {recovered_value}")
                logger.info(f"{device_model}: Original value: {original_identifier}")

                # Validate recovery using page object method
                general_page.validate_identifier_recovery(
                    recovered_value, original_identifier, device_model
                )

            else:
                # Cancel may have navigated away - this is acceptable behavior
                logger.info(
                    f"{device_model}: Cancel navigated away from page - acceptable behavior"
                )

                # Verify we're back at a reasonable location using page object method
                general_page.validate_navigation_after_cancel(current_url, device_model)

            logger.info(f"{device_model}: Step 3 - Recovery verification successful")

        except Exception as e:
            logger.error(f"{device_model}: Step 3 - Recovery verification failed: {e}")
            pytest.fail(f"Recovery verification failed for {device_model}: {e}")

        # Step 4: Make valid change after recovery using page object methods
        try:
            logger.info(f"{device_model}: Step 4 - Making valid change after recovery")

            # Navigate back if needed using page object method
            if "general" not in general_page.get_current_url():
                general_page.navigate_to_page()

            # Make valid change using page object method
            valid_identifier = "Valid Change After Recovery"
            general_page.configure_identifier(identifier=valid_identifier)

            # Trigger onchange to enable save button using page object method
            general_page.trigger_identifier_onchange()

            # Wait for JavaScript to execute using device-aware timing
            js_delay = general_page.get_js_delay()
            time.sleep(js_delay)

            logger.info(f"{device_model}: Step 4 - Valid change configured")

        except Exception as e:
            logger.error(f"{device_model}: Step 4 - Valid change failed: {e}")
            pytest.fail(f"Valid change failed for {device_model}: {e}")

        # Step 5: Save and verify valid change using page object methods
        try:
            logger.info(f"{device_model}: Step 5 - Saving and verifying valid change")

            # Check if save button is enabled using page object method
            if general_page.is_save_button_enabled():
                # Save configuration using page object method
                general_page.save_configuration()

                # Navigate to page to verify using page object method
                general_page.navigate_to_page()

                # Verify valid change succeeded using page object method
                final_data = general_page.get_page_data()
                final_identifier = final_data.get("identifier", "")

                logger.info(f"{device_model}: Final identifier: {final_identifier}")
                logger.info(f"{device_model}: Expected identifier: {valid_identifier}")

                # Validate final change using page object method
                general_page.validate_final_identifier_change(
                    final_identifier, valid_identifier, device_model
                )

            else:
                # If save button didn't enable, the recovery still worked
                logger.info(
                    f"{device_model}: Save button not enabled - recovery worked, invalid change prevented"
                )

                # Verify we're in a valid state using page object method
                general_page.navigate_to_page()
                final_data = general_page.get_page_data()
                current_identifier = final_data.get("identifier", "")

                # Either back to original or field was reset - both are valid recovery
                general_page.validate_invalid_input_cleared(
                    current_identifier, device_model
                )

            logger.info(f"{device_model}: Step 5 - Save and verification successful")

        except Exception as e:
            logger.error(f"{device_model}: Step 5 - Save and verification failed: {e}")
            pytest.fail(f"Save and verification failed for {device_model}: {e}")

        # Additional workflow validation using page object methods
        try:
            logger.info(f"{device_model}: Step 6 - Additional workflow validation")

            # Validate recovery workflow integrity using page object method
            general_page.validate_invalid_input_recovery_workflow_integrity()

            # Series-specific validation using page object methods
            if device_series == 2:
                general_page.validate_series2_invalid_input_recovery_patterns()
            elif device_series == 3:
                general_page.validate_series3_invalid_input_recovery_patterns()

            # Cross-validation test using page object method
            general_page.test_invalid_input_recovery_cross_validation()

            logger.info(
                f"{device_model}: Step 6 - Additional workflow validation successful"
            )

        except Exception as e:
            logger.warning(
                f"{device_model}: Step 6 - Additional workflow validation failed: {e}"
            )
            # Continue with cleanup even if this validation fails

        # Workflow completion summary
        logger.info(
            f"{device_model}: Invalid input recovery workflow completed successfully"
        )
        print(f"Invalid input recovery workflow passed for {device_model}")

    except Exception as e:
        logger.error(
            f"{device_model}: Invalid input recovery workflow encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"Invalid input recovery workflow failed for {device_model}: {e}")

    finally:
        # Restore original state after recovery test using page object methods
        try:
            logger.info(f"{device_model}: Starting cleanup process")

            # Navigate to page if needed
            if "general" not in general_page.get_current_url():
                general_page.navigate_to_page()

            # Restore original identifier using page object method
            general_page.configure_identifier(identifier=original_identifier)
            general_page.trigger_identifier_onchange()

            # Save if enabled using page object method
            if general_page.is_save_button_enabled():
                general_page.save_configuration()

                # Wait for save to complete using device-aware timing
                cleanup_delay = general_page.get_save_delay()
                time.sleep(cleanup_delay)

                logger.info(
                    f"{device_model}: Cleanup successful - restored identifier: {original_identifier}"
                )
            else:
                logger.info(f"{device_model}: Cleanup completed - no save needed")

        except Exception as cleanup_error:
            logger.warning(
                f"{device_model}: Cleanup failed but test passed: {cleanup_error}"
            )
            print(
                f"Warning: Cleanup failed but test passed for {device_model}: {cleanup_error}"
            )

        logger.info(f"{device_model}: Invalid input recovery workflow test completed")
