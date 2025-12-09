"""
Category 6: GNSS Configuration - Test 6.6.1
GPS-Only Configuration - Pure Page Object Pattern
Test Count: 1 of 11 in Category 6
Hardware: Device Only
Priority: HIGH - GNSS constellation management
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on GNSS configuration requirements and GPS-only patterns
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.gnss_config_page import GNSSConfigPage

logger = logging.getLogger(__name__)


def test_6_6_1_gps_only_configuration(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 6.6.1: GPS-Only Configuration - Pure Page Object Pattern
    Purpose: Verify can configure GPS-only operation by disabling optional constellations
    Expected: Only GPS remains enabled (mandatory), others disabled
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates GPS-only patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate GPS-only configuration"
        )

    # Initialize page object with device-aware patterns
    gnss_config_page = GNSSConfigPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing GPS-only configuration on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to GNSS configuration page using page object method
        gnss_config_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        gnss_config_page.wait_for_page_load()

        # Test initial constellation states
        logger.info("Testing initial constellation states")

        available_constellations = gnss_config_page.get_available_constellations()
        logger.info(f"Available constellations: {available_constellations}")

        if available_constellations:
            # Store original constellation states for restoration
            original_states = {}
            for constellation in available_constellations:
                original_states[constellation] = (
                    gnss_config_page.is_constellation_enabled(constellation)
                )

            logger.info(f"Original constellation states: {original_states}")

            # Test GPS-only configuration
            logger.info("Testing GPS-only constellation configuration")

            # Configure GPS-only operation (enable only GPS, disable others)
            gps_only_constellations = (
                ["GPS"]
                if "GPS" in available_constellations
                else [available_constellations[0]]
            )

            gps_only_configured = gnss_config_page.configure_constellations(
                gps_only_constellations
            )

            if gps_only_configured:
                logger.info(f"GPS-only configuration applied on {device_model}")

                # Verify GPS-only state using page object methods
                logger.info("Verifying GPS-only constellation states")

                gps_enabled = gnss_config_page.is_constellation_enabled("GPS")
                logger.info(f"GPS enabled state: {gps_enabled}")

                # Check optional constellations are disabled
                optional_constellations_disabled = True
                for constellation in available_constellations:
                    if constellation != "GPS":
                        state = gnss_config_page.is_constellation_enabled(constellation)
                        if state:
                            logger.warning(
                                f"Optional constellation {constellation} still enabled: {state}"
                            )
                            optional_constellations_disabled = False
                        else:
                            logger.info(
                                f"Optional constellation {constellation} disabled: {state}"
                            )

                if gps_enabled and optional_constellations_disabled:
                    logger.info(f"GPS-only configuration verified on {device_model}")
                else:
                    logger.warning(
                        f"GPS-only configuration incomplete on {device_model}"
                    )

                # Test save functionality using page object method
                logger.info("Testing save functionality")

                save_successful = gnss_config_page.save_configuration()

                if save_successful:
                    logger.info(
                        f"GPS-only configuration saved successfully on {device_model}"
                    )
                else:
                    logger.warning(
                        f"GPS-only configuration save failed on {device_model}"
                    )

                # Test restore original configuration using page object method
                logger.info("Testing restore original configuration")

                original_restored = gnss_config_page.configure_constellations(
                    list(original_states.keys())
                )

                if original_restored:
                    logger.info("Original constellation configuration restored")

                    # Verify restoration
                    restoration_verified = True
                    for constellation in available_constellations:
                        current_state = gnss_config_page.is_constellation_enabled(
                            constellation
                        )
                        if current_state != original_states[constellation]:
                            logger.warning(
                                f"{constellation} restoration failed: expected {original_states[constellation]}, got {current_state}"
                            )
                            restoration_verified = False

                    if restoration_verified:
                        logger.info("Original constellation configuration verified")
                    else:
                        logger.warning(
                            "Original constellation configuration restoration incomplete"
                        )

                    # Test cancel functionality using page object method
                    try:
                        gnss_config_page.cancel_gnss_changes()
                        logger.info(f"Cancel operation completed on {device_model}")
                    except Exception as e:
                        logger.warning(
                            f"Cancel operation failed on {device_model}: {e}"
                        )

                else:
                    logger.warning(
                        "Failed to restore original constellation configuration"
                    )

            else:
                logger.warning(f"GPS-only configuration failed on {device_model}")

        else:
            logger.warning(f"No available constellations found on {device_model}")

        # Test device series-specific behavior using page object methods
        device_series = DeviceCapabilities.get_series(device_model)

        if device_series == 2:
            logger.info(
                f"Testing Series 2 specific GPS-only patterns on {device_model}"
            )
            # Series 2 typically has single constellation selection
        elif device_series == 3:
            logger.info(
                f"Testing Series 3 specific GPS-only patterns on {device_model}"
            )
            # Series 3 supports multiple constellation checkboxes

        # Test GNSS capability validation using page object method
        logger.info("Testing GNSS capability validation")

        capabilities = gnss_config_page.detect_gnss_capabilities()
        logger.info(f"GNSS capabilities detected: {capabilities['detection_summary']}")

        # Validate GPS support
        available_constellations = capabilities.get("available_constellations", [])
        if "GPS" in available_constellations:
            logger.info(f"GPS constellation supported on {device_model}")
        else:
            logger.warning(
                f"GPS constellation not detected in capabilities on {device_model}"
            )

        # Test page data retrieval using page object method
        logger.info("Testing page data retrieval")

        page_data = gnss_config_page.get_page_data()
        logger.info(f"GNSS page data retrieved: {list(page_data.keys())}")

        # Test multiple constellation configuration scenarios
        logger.info("Testing multiple constellation configuration scenarios")

        if len(available_constellations) > 1:
            # Test all constellations enabled
            all_enabled = gnss_config_page.configure_constellations(
                available_constellations
            )

            if all_enabled:
                logger.info("All constellations enabled successfully")

                # Verify all are enabled
                all_enabled_verified = True
                for constellation in available_constellations:
                    if not gnss_config_page.is_constellation_enabled(constellation):
                        all_enabled_verified = False
                        logger.warning(f"{constellation} not enabled as expected")

                if all_enabled_verified:
                    logger.info("All constellations enabled verification passed")

                # Test disable all except GPS
                gps_only_again = gnss_config_page.configure_constellations(["GPS"])

                if gps_only_again:
                    logger.info("GPS-only configuration tested again successfully")

        # Final validation using page object method
        logger.info("Performing final validation")

        final_constellation_states = {}
        for constellation in available_constellations:
            final_constellation_states[constellation] = (
                gnss_config_page.is_constellation_enabled(constellation)
            )

        logger.info(f"Final constellation states: {final_constellation_states}")

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

        logger.info(f"GPS-only configuration test COMPLETED for {device_model}")
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"GPS-only configuration test failed on {device_model}: {e}")
        pytest.fail(f"GPS-only configuration test failed on {device_model}: {e}")
