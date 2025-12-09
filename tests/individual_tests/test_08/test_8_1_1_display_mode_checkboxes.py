"""
Category 8: Display Configuration - Test 8.1.1
Display Mode Checkboxes - Pure Page Object Pattern
Test Count: 1 of 5 in Category 8
Hardware: Device Only
Priority: HIGH - Display configuration functionality
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on display configuration requirements and checkbox patterns
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.display_config_page import DisplayConfigPage

logger = logging.getLogger(__name__)


def test_8_1_1_display_mode_checkboxes(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 8.1.1: Display Mode Checkboxes - Pure Page Object Pattern
    Purpose: Verify display mode checkboxes with device-aware validation
    Expected: Checkboxes functional, mode selection works, device-specific timing
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates display patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate display mode checkboxes"
        )

    # Initialize page object with device-aware patterns
    display_config_page = DisplayConfigPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing display mode checkboxes on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to display configuration page using page object method
        display_config_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        display_config_page.wait_for_page_load()

        # Test display mode availability using page object method
        logger.info("Testing display mode availability")

        available_modes = display_config_page.get_available_display_modes()
        logger.info(f"Available display modes: {available_modes}")

        if available_modes:
            logger.info(
                f"Display modes found on {device_model}: {len(available_modes)} modes"
            )

            # Test display mode functionality using page object methods
            logger.info("Testing display mode functionality")

            # Test each available display mode
            for mode in available_modes[:5]:  # Test up to 5 modes
                logger.info(f"Testing display mode: {mode}")

                # Test mode enable/disable using page object method
                mode_enabled = display_config_page.is_display_mode_enabled(mode)
                logger.info(
                    f"Display mode {mode} initial state: {'enabled' if mode_enabled else 'disabled'}"
                )

                # Test toggling display mode using page object method
                toggle_success = display_config_page.toggle_display_mode(mode)

                if toggle_success:
                    logger.info(f"Display mode {mode} toggled successfully")

                    # Verify new state using page object method
                    new_state = display_config_page.is_display_mode_enabled(mode)

                    if new_state != mode_enabled:
                        logger.info(
                            f"Display mode {mode} state changed: {'enabled' if mode_enabled else 'disabled'} -> {'enabled' if new_state else 'disabled'}"
                        )
                    else:
                        logger.warning(
                            f"Display mode {mode} state may not have changed"
                        )

                    # Test toggling back using page object method
                    revert_success = display_config_page.toggle_display_mode(mode)

                    if revert_success:
                        logger.info(f"Display mode {mode} reverted successfully")

                        # Verify revert state using page object method
                        revert_state = display_config_page.is_display_mode_enabled(mode)

                        if revert_state == mode_enabled:
                            logger.info(
                                f"Display mode {mode} reverted to original state: {'enabled' if revert_state else 'disabled'}"
                            )
                        else:
                            logger.warning(
                                f"Display mode {mode} may not have reverted properly"
                            )
                    else:
                        logger.warning(f"Failed to revert display mode {mode}")
                else:
                    logger.warning(f"Failed to toggle display mode {mode}")

            # Test save functionality using page object method
            logger.info("Testing save functionality")

            save_successful = display_config_page.save_configuration()

            if save_successful:
                logger.info(
                    f"Display configuration saved successfully on {device_model}"
                )
            else:
                logger.warning(f"Display configuration save unclear on {device_model}")

        else:
            logger.warning(f"No display modes detected on {device_model}")

        # Test device series-specific behavior using page object methods
        device_series = DeviceCapabilities.get_series(device_model)

        if device_series == 2:
            logger.info(f"Testing Series 2 specific display patterns on {device_model}")
            # Series 2 typically has simpler display mode options
        elif device_series == 3:
            logger.info(f"Testing Series 3 specific display patterns on {device_model}")
            # Series 3 may have advanced display features

        # Test display configuration methods using page object method
        logger.info("Testing display configuration methods")

        # Test display mode detection
        detected_modes = display_config_page.detect_display_modes()
        logger.info(f"Detected display modes: {detected_modes}")

        # Test display settings configuration
        if available_modes:
            test_settings = display_config_page.configure_display_settings("standard")
            if test_settings:
                logger.info("Display settings configuration successful")
            else:
                logger.warning("Display settings configuration failed")

        # Test display mode persistence using page object method
        logger.info("Testing display mode persistence")

        if available_modes:
            test_mode = available_modes[0]
            original_state = display_config_page.is_display_mode_enabled(test_mode)

            # Toggle mode to create unsaved changes
            toggle_for_persistence = display_config_page.toggle_display_mode(test_mode)

            if toggle_for_persistence:
                logger.info(f"Display mode {test_mode} toggled for persistence test")

                # Save changes
                persistence_save = display_config_page.save_configuration()

                if persistence_save:
                    logger.info("Display mode changes saved for persistence test")

                    # Reload page to test persistence using page object method
                    display_config_page.reload_page()
                    display_config_page.wait_for_page_load()

                    # Verify mode persisted
                    persisted_state = display_config_page.is_display_mode_enabled(
                        test_mode
                    )
                    logger.info(
                        f"Display mode {test_mode} state after reload: {'enabled' if persisted_state else 'disabled'}"
                    )

                    if persisted_state != original_state:
                        logger.info(f"Display mode {test_mode} persistence verified")
                    else:
                        logger.warning(
                            f"Display mode {test_mode} may not have persisted"
                        )

                    # Restore original state
                    if persisted_state != original_state:
                        restore_toggle = display_config_page.toggle_display_mode(
                            test_mode
                        )
                        if restore_toggle:
                            logger.info(
                                f"Display mode {test_mode} restored to original state"
                            )
                        else:
                            logger.warning(
                                f"Failed to restore display mode {test_mode}"
                            )

        # Test page data retrieval using page object method
        logger.info("Testing page data retrieval")

        page_data = display_config_page.get_page_data()
        logger.info(f"Display page data retrieved: {list(page_data.keys())}")

        # Test save button state using page object method
        logger.info("Testing save button state")

        save_button_state = display_config_page.test_save_button_state()

        if save_button_state is not None:
            logger.info(
                f"Save button state: {'enabled' if save_button_state else 'disabled'}"
            )
        else:
            logger.warning("Save button state unclear")

        # Test display capabilities validation using page object method
        logger.info("Testing display capabilities validation")

        capabilities = display_config_page.detect_display_capabilities()
        logger.info(f"Display capabilities detected: {capabilities}")

        # Final validation using page object method
        logger.info("Performing final validation")

        final_available_modes = display_config_page.get_available_display_modes()
        logger.info(f"Final available display modes: {final_available_modes}")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            display_capabilities = device_capabilities_data.get(
                "display_capabilities", {}
            )
            logger.info(
                f"Display capabilities from DeviceCapabilities: {display_capabilities}"
            )
        else:
            logger.info(
                f"No specific display capabilities defined in DeviceCapabilities for {device_model}"
            )

        # Performance validation
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
                logger.info(f"Performance baseline: {typical_time}")

        logger.info(f"Display mode checkboxes test COMPLETED for {device_model}")
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Display mode checkboxes test failed on {device_model}: {e}")
        pytest.fail(f"Display mode checkboxes test failed on {device_model}: {e}")
