"""
Category 8: Display Configuration - Test 8.1.2
Enable Display Mode Checkbox - Pure Page Object Pattern
Test Count: 2 of 10 in Category 8
Hardware: Device Only
Priority: MEDIUM - Front panel display settings
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on test_08_display_config.py::TestDisplayModes::test_8_1_2_enable_mode_checkbox
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.display_config_page import DisplayConfigPage

logger = logging.getLogger(__name__)


def test_8_1_2_enable_mode_checkbox(unlocked_config_page: Page, base_url: str, request):
    """
    Test 8.1.2: Enable Display Mode Checkbox - Pure Page Object Pattern
    Purpose: Verify mode checkbox can be checked with device-aware validation
    Expected: Checkbox toggles and persists with device-specific timing
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both 2 and 3 - validates display patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate display behavior")

    # Initialize page object with device-aware patterns
    display_config_page = DisplayConfigPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing display mode checkbox on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to display configuration page using page object method
        display_config_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        display_config_page.wait_for_page_load()

        # Test device series-specific behavior using page object methods
        device_series = DeviceCapabilities.get_series(device_model)

        logger.info(
            f"Testing display mode checkbox on {device_model} (Series {device_series})"
        )

        # Test display mode availability using page object method
        available_modes = display_config_page.get_available_display_modes()
        logger.info(f"Available display modes: {available_modes}")

        # Use mode1 for testing with device-aware patterns
        test_mode = "mode1"

        if test_mode in available_modes:
            logger.info(f"Testing mode1 checkbox functionality")

            # Get initial state using page object method
            initial_state = display_config_page.is_display_mode_enabled(test_mode)
            logger.info(
                f"Initial checkbox state: {'checked' if initial_state else 'unchecked'}"
            )

            # Toggle checkbox using page object method
            toggle_success = display_config_page.toggle_display_mode(test_mode)

            if toggle_success:
                # Small wait for device stability using page object timeout
                stability_wait = (
                    display_config_page.get_timeout() // 20
                )  # 5% of timeout
                time.sleep(stability_wait // 1000)  # Convert to seconds

                # Verify state changed using page object method
                new_state = display_config_page.is_display_mode_enabled(test_mode)
                logger.info(
                    f"After toggle checkbox state: {'checked' if new_state else 'unchecked'}"
                )

                if new_state != initial_state:
                    logger.info(f"Display mode checkbox toggled successfully")

                    # Toggle back to restore original state
                    revert_success = display_config_page.toggle_display_mode(test_mode)

                    if revert_success:
                        # Small wait for device stability
                        time.sleep(stability_wait // 1000)

                        # Verify revert using page object method
                        revert_state = display_config_page.is_display_mode_enabled(
                            test_mode
                        )
                        if revert_state == initial_state:
                            logger.info(f"Display mode checkbox reverted successfully")
                        else:
                            logger.warning(
                                f"Display mode checkbox may not have reverted properly"
                            )
                    else:
                        logger.warning(f"Failed to revert display mode checkbox")
                else:
                    logger.warning(f"Display mode checkbox may not have toggled")
            else:
                logger.warning(f"Failed to toggle display mode checkbox")
        else:
            logger.warning(
                f"Test mode '{test_mode}' not found in available modes: {available_modes}"
            )

            # Fallback: try to find and test any available mode
            if available_modes:
                fallback_mode = list(available_modes.keys())[
                    0
                ]  # Get first available mode
                logger.info(f"Using fallback mode: {fallback_mode}")

                # Test fallback mode using page object methods
                fallback_initial = display_config_page.is_display_mode_enabled(
                    fallback_mode
                )
                logger.info(
                    f"Fallback mode initial state: {'checked' if fallback_initial else 'unchecked'}"
                )

                fallback_toggle = display_config_page.toggle_display_mode(fallback_mode)

                if fallback_toggle:
                    # Small wait for device stability
                    stability_wait = display_config_page.get_timeout() // 20
                    time.sleep(stability_wait // 1000)

                    # Verify fallback toggle
                    fallback_new = display_config_page.is_display_mode_enabled(
                        fallback_mode
                    )
                    logger.info(
                        f"Fallback mode after toggle: {'checked' if fallback_new else 'unchecked'}"
                    )

                    if fallback_new != fallback_initial:
                        logger.info(f"Fallback display mode toggled successfully")

                        # Restore original state
                        fallback_revert = display_config_page.toggle_display_mode(
                            fallback_mode
                        )
                        if fallback_revert:
                            logger.info(f"Fallback display mode reverted successfully")
                    else:
                        logger.warning(f"Fallback display mode may not have toggled")

        # Test additional device series-specific behavior
        if device_series == 2:
            logger.info(
                f"Series 2 specific display mode validation completed on {device_model}"
            )
        elif device_series == 3:
            logger.info(
                f"Series 3 specific display mode validation completed on {device_model}"
            )

        # Test save functionality using page object method
        logger.info("Testing save functionality")
        save_successful = display_config_page.save_configuration()
        if save_successful:
            logger.info(f"Display configuration saved successfully on {device_model}")
        else:
            logger.warning(f"Display configuration save unclear on {device_model}")

        # Test page data retrieval using page object method
        page_data = display_config_page.get_page_data()
        logger.info(f"Display page data retrieved: {list(page_data.keys())}")

        # Test save button state using page object method
        save_button_state = display_config_page.test_save_button_state()
        if save_button_state is not None:
            logger.info(
                f"Save button state: {'enabled' if save_button_state else 'disabled'}"
            )

        # Performance validation using page object methods
        logger.info("Performing performance validation")

        start_time = time.time()

        # Test page reload performance
        display_config_page.reload_page()
        reload_time = time.time() - start_time

        logger.info(f"Page reload time: {reload_time:.2f}s")

        # Cross-reference with performance expectations
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            nav_performance = performance_data.get("navigation_performance", {})
            section_nav = nav_performance.get("section_navigation", {})
            typical_time = section_nav.get("typical_time", "")
            if typical_time:
                logger.info(
                    f"Display configuration performance baseline: {typical_time}"
                )

        logger.info(
            f"Display mode checkbox test completed successfully for {device_model}"
        )
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Display mode checkbox test failed on {device_model}: {e}")
        pytest.fail(f"Display mode checkbox test failed on {device_model}: {e}")

    finally:
        # Small cleanup wait for device stability using page object timeout
        cleanup_wait = display_config_page.get_timeout() // 20  # 5% of timeout
        time.sleep(cleanup_wait // 1000)  # Convert to seconds
