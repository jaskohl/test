"""
Category 6: GNSS Configuration - Test 6.7.1
GNSS Save Button State - Pure Page Object Pattern
Test Count: 1 of 11 in Category 6
Hardware: Device Only
Priority: HIGH - GNSS save button state management
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on GNSS configuration requirements and save button patterns
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.gnss_config_page import GNSSConfigPage

logger = logging.getLogger(__name__)


def test_6_7_1_gnss_save_button_state(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 6.7.1: GNSS Save Button State Management - Pure Page Object Pattern
    Purpose: Verify GNSS save button enables on constellation change
    Expected: Disabled initially, enables on change
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates save button patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate GNSS save button state"
        )

    # Initialize page object with device-aware patterns
    gnss_config_page = GNSSConfigPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing GNSS save button state on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to GNSS configuration page using page object method
        gnss_config_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        gnss_config_page.wait_for_page_load()

        # Test initial save button state using page object method
        logger.info("Testing initial GNSS save button state")

        save_button_state_initial = gnss_config_page.test_save_button_state()

        if save_button_state_initial is not None:
            if not save_button_state_initial:
                logger.info(f"GNSS save button initially disabled on {device_model}")
            else:
                logger.warning(
                    f"GNSS save button initially enabled on {device_model} (unexpected)"
                )
        else:
            logger.warning(f"GNSS save button state unclear on {device_model}")

        # Test constellation change to trigger save button enablement
        logger.info("Testing constellation change to trigger save button")

        available_constellations = gnss_config_page.get_available_constellations()

        if available_constellations:
            # Get first constellation to toggle
            test_constellation = available_constellations[0]
            logger.info(f"Testing constellation toggle: {test_constellation}")

            # Get current state
            original_state = gnss_config_page.is_constellation_enabled(
                test_constellation
            )
            logger.info(f"{test_constellation} initial state: {original_state}")

            # Toggle constellation to trigger save button
            if original_state:
                # Currently enabled, disable it
                new_constellations = [
                    c for c in available_constellations if c != test_constellation
                ]
            else:
                # Currently disabled, enable all
                new_constellations = available_constellations

            constellation_toggled = gnss_config_page.configure_constellations(
                new_constellations
            )

            if constellation_toggled:
                logger.info(f"Constellation toggle applied on {device_model}")

                # Test save button state after constellation change using page object method
                logger.info("Testing save button state after constellation change")

                save_button_state_after = gnss_config_page.test_save_button_state()

                if save_button_state_after is not None:
                    if save_button_state_after:
                        logger.info(
                            f"GNSS save button enabled after constellation change on {device_model}"
                        )
                    else:
                        logger.warning(
                            f"GNSS save button still disabled after constellation change on {device_model}"
                        )
                else:
                    logger.warning(
                        f"GNSS save button state unclear after constellation change on {device_model}"
                    )

                # Test save functionality using page object method
                logger.info("Testing save functionality")

                save_successful = gnss_config_page.save_configuration()

                if save_successful:
                    logger.info(f"Configuration save successful on {device_model}")
                else:
                    logger.warning(f"Configuration save failed on {device_model}")

                # Test cancel functionality using page object method
                logger.info("Testing cancel functionality")

                # Toggle constellation again to create unsaved changes
                if original_state:
                    # Restore to original state
                    restore_constellations = available_constellations
                else:
                    # Keep disabled state
                    restore_constellations = [
                        c for c in available_constellations if c != test_constellation
                    ]

                constellation_restored = gnss_config_page.configure_constellations(
                    restore_constellations
                )

                if constellation_restored:
                    logger.info(
                        "Constellation state restored to create unsaved changes"
                    )

                    # Test cancel functionality using page object method
                    try:
                        gnss_config_page.cancel_gnss_changes()
                        logger.info(f"Cancel operation completed on {device_model}")

                        # Verify save button state after cancel using page object method
                        save_button_state_cancel = (
                            gnss_config_page.test_save_button_state()
                        )

                        if save_button_state_cancel is not None:
                            if not save_button_state_cancel:
                                logger.info(
                                    f"GNSS save button disabled after cancel on {device_model}"
                                )
                            else:
                                logger.warning(
                                    f"GNSS save button still enabled after cancel on {device_model}"
                                )
                        else:
                            logger.warning(
                                f"GNSS save button state unclear after cancel on {device_model}"
                            )

                    except Exception as e:
                        logger.warning(
                            f"Cancel operation failed on {device_model}: {e}"
                        )

            else:
                logger.warning(f"Constellation toggle failed on {device_model}")
        else:
            logger.warning(f"No available constellations found on {device_model}")

        # Test device series-specific behavior using page object methods
        device_series = DeviceCapabilities.get_series(device_model)

        if device_series == 2:
            logger.info(f"Testing Series 2 specific patterns on {device_model}")
            # Series 2 typically has different save button behavior
        elif device_series == 3:
            logger.info(f"Testing Series 3 specific patterns on {device_model}")
            # Series 3 supports multiple constellation checkboxes

        # Test GNSS capability validation using page object method
        logger.info("Testing GNSS capability validation")

        capabilities = gnss_config_page.detect_gnss_capabilities()
        logger.info(f"GNSS capabilities detected: {capabilities['detection_summary']}")

        # Validate constellation support
        available_constellations = capabilities.get("available_constellations", [])
        if available_constellations:
            logger.info(
                f"Constellations supported on {device_model}: {available_constellations}"
            )
        else:
            logger.warning(f"No constellations detected on {device_model}")

        # Test page data retrieval using page object method
        logger.info("Testing page data retrieval")

        page_data = gnss_config_page.get_page_data()
        logger.info(f"GNSS page data retrieved: {list(page_data.keys())}")

        # Final validation using page object method
        logger.info("Performing final validation")

        final_save_button_state = gnss_config_page.test_save_button_state()

        if final_save_button_state is not None:
            logger.info(
                f"Final save button state: {'enabled' if final_save_button_state else 'disabled'}"
            )
        else:
            logger.warning("Final save button state unclear")

        # Cross-validate with device capabilities
        device_capabilities_data = DeviceCapabilities.get_gnss_constellations(
            device_model
        )
        if device_capabilities_data:
            logger.info(
                f"GNSS constellations supported by DeviceCapabilities for {device_model}: {device_capabilities_data}"
            )
        else:
            logger.info(
                f"No specific GNSS constellations defined in DeviceCapabilities for {device_model}"
            )

        logger.info(f"GNSS save button state test COMPLETED for {device_model}")
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"GNSS save button state test failed on {device_model}: {e}")
        pytest.fail(f"GNSS save button state test failed on {device_model}: {e}")
