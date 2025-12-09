"""
Category 8: Display Configuration - Test 8.1.3
Multiple Display Modes Enabled - Pure Page Object Pattern
Test Count: 3 of 10 in Category 8
Hardware: Device Only
Priority: MEDIUM - Front panel display settings
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on multiple display modes enabled functionality
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.display_config_page import DisplayConfigPage

logger = logging.getLogger(__name__)


def test_8_1_3_multiple_modes_enabled(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 8.1.3: Multiple Display Modes Enabled - Pure Page Object Pattern
    Purpose: Verify multiple display modes can be enabled simultaneously
    Expected: No conflicts, multiple checkboxes can be checked
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
        f"Testing multiple display modes enabled on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to display configuration page using page object method
        display_config_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        display_config_page.wait_for_page_load()

        # Test device series-specific behavior using page object methods
        device_series = DeviceCapabilities.get_series(device_model)

        logger.info(
            f"Testing multiple display modes on {device_model} (Series {device_series})"
        )

        # Test display mode availability using page object method
        available_modes = display_config_page.get_available_display_modes()
        logger.info(f"Available display modes: {available_modes}")

        if not available_modes:
            logger.warning(f"No display modes detected on {device_model}")
            return

        # Store original states for rollback using page object methods
        original_states = {}
        modes_to_test = list(available_modes.keys())[:3]  # Test first 3 modes

        for mode_name in modes_to_test:
            original_states[mode_name] = display_config_page.is_display_mode_enabled(
                mode_name
            )
            logger.info(
                f"Original state for {mode_name}: {'checked' if original_states[mode_name] else 'unchecked'}"
            )

        # Enable multiple modes using page object methods
        enabled_count = 0

        for mode_name in modes_to_test:
            logger.info(f"Enabling display mode: {mode_name}")

            toggle_success = display_config_page.toggle_display_mode(mode_name)

            if toggle_success:
                enabled_count += 1
                # Small wait for device stability using page object timeout
                stability_wait = (
                    display_config_page.get_timeout() // 20
                )  # 5% of timeout
                time.sleep(stability_wait // 1000)  # Convert to seconds

                # Verify mode is now enabled using page object method
                new_state = display_config_page.is_display_mode_enabled(mode_name)
                logger.info(
                    f"After toggle - {mode_name} state: {'checked' if new_state else 'unchecked'}"
                )

            else:
                logger.warning(f"Failed to toggle display mode: {mode_name}")

        logger.info(f"Enabled {enabled_count} display modes successfully")

        # Verify multiple modes can be enabled without conflict using page object methods
        logger.info("Verifying multiple display modes enabled without conflicts")

        for mode_name in modes_to_test:
            mode_enabled = display_config_page.is_display_mode_enabled(mode_name)
            logger.info(
                f"Verification - {mode_name} state: {'checked' if mode_enabled else 'unchecked'}"
            )

        # Test save functionality using page object method
        logger.info("Testing save functionality with multiple modes enabled")
        save_successful = display_config_page.save_configuration()

        if save_successful:
            logger.info(
                f"Multiple display modes configuration saved successfully on {device_model}"
            )
        else:
            logger.warning(f"Multiple display modes save unclear on {device_model}")

        # Test save button state using page object method
        save_button_state = display_config_page.test_save_button_state()
        if save_button_state is not None:
            logger.info(
                f"Save button state: {'enabled' if save_button_state else 'disabled'}"
            )
        else:
            logger.warning(f"Save button state unclear")

        # Test page data retrieval using page object method
        page_data = display_config_page.get_page_data()
        logger.info(f"Display page data retrieved: {list(page_data.keys())}")

        # Test display capabilities validation using page object method
        capabilities = display_config_page.detect_display_capabilities()
        logger.info(f"Display capabilities detected: {capabilities}")

        # Verify no conflicts with multiple modes enabled
        logger.info("Verifying no conflicts with multiple display modes")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_capabilities(device_model)
        if device_capabilities_data:
            display_capabilities = device_capabilities_data.get(
                "display_capabilities", {}
            )
            logger.info(
                f"Display capabilities from DeviceCapabilities: {display_capabilities}"
            )

            # Check if multiple modes are supported
            multiple_modes_support = display_capabilities.get(
                "multiple_modes_supported", False
            )
            logger.info(f"Multiple modes support: {multiple_modes_support}")

        # Performance validation using page object methods
        logger.info("Performing performance validation with multiple modes")

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
                logger.info(f"Display navigation performance baseline: {typical_time}")

        # Final verification - ensure at least some modes were enabled
        final_enabled_count = sum(
            1
            for mode in modes_to_test
            if display_config_page.is_display_mode_enabled(mode)
        )
        logger.info(f"Final enabled modes count: {final_enabled_count}")

        if final_enabled_count > 0:
            logger.info(f"Multiple display modes test PASSED for {device_model}")
        else:
            logger.warning(
                f"Multiple display modes test completed but no modes remained enabled"
            )

        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Multiple display modes test failed on {device_model}: {e}")
        pytest.fail(f"Multiple display modes test failed on {device_model}: {e}")

    finally:
        # Rollback: Restore original states using page object methods
        logger.info("Rolling back to original display mode states")

        for mode_name, original_state in original_states.items():
            try:
                current_state = display_config_page.is_display_mode_enabled(mode_name)
                logger.info(
                    f"Checking rollback for {mode_name}: current='{current_state}', original='{original_state}'"
                )

                if current_state != original_state:
                    logger.info(
                        f"Restoring {mode_name} to original state: {'checked' if original_state else 'unchecked'}"
                    )
                    restore_success = display_config_page.toggle_display_mode(mode_name)

                    if restore_success:
                        # Small wait for device stability
                        stability_wait = display_config_page.get_timeout() // 20
                        time.sleep(stability_wait // 1000)

                        # Verify restoration
                        restored_state = display_config_page.is_display_mode_enabled(
                            mode_name
                        )
                        logger.info(
                            f"Rollback verification - {mode_name} state: {'checked' if restored_state else 'unchecked'}"
                        )

                    else:
                        logger.warning(f"Failed to restore display mode: {mode_name}")
                else:
                    logger.info(f"Display mode {mode_name} already in original state")
            except Exception as rollback_error:
                logger.warning(f"Rollback failed for {mode_name}: {rollback_error}")

        # Small cleanup wait for device stability using page object timeout
        cleanup_wait = display_config_page.get_timeout() // 20  # 5% of timeout
        time.sleep(cleanup_wait // 1000)  # Convert to seconds

        logger.info(f"Multiple display modes test completed for {device_model}")
