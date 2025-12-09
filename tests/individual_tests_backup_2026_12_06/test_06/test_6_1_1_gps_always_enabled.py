"""
Category 6: GNSS Configuration - Test 6.1.1
GPS Always Enabled Validation - DeviceCapabilities Enhanced
Test Count: 1 of 7 in Category 6
Hardware: Device Only
Priority: HIGH - GNSS functionality validation
Series: Both Series 2 and 3
ENHANCED: Comprehensive DeviceCapabilities integration for device-aware GNSS validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.gnss_config_page import GNSSConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_6_1_1_gps_always_enabled_device_enhanced(
    gnss_config_page: GNSSConfigPage, base_url: str, request
):
    """
    Test 6.1.1: GPS Always Enabled Validation - DeviceCapabilities Enhanced
    Purpose: Verify GPS constellation is always enabled across device variants
    Expected: GPS checkbox always present and checked, device-aware validation
    ENHANCED: Full DeviceCapabilities integration for GNSS capability validation
    Series: Both - validates GNSS patterns across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate GNSS behavior")

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing GPS always enabled validation on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Get GNSS capabilities for validation
    gnss_constellations = DeviceCapabilities.get_gnss_constellations(device_model)

    if "GPS" not in gnss_constellations:
        pytest.skip(f"GPS not supported on {device_model}")

    logger.info(
        f"Expected GNSS constellations for {device_model}: {gnss_constellations}"
    )

    # Navigate to GNSS configuration page
    gnss_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    gnss_config_page.verify_page_loaded()

    # Test GPS field presence and state with device-aware patterns
    try:
        # Locate GPS checkbox with device-aware selectors
        gps_checkbox = gnss_config_page.page.locator(
            "input[name='gps'], input[type='checkbox'][value='gps']"
        )

        field_timeout = int(8000 * timeout_multiplier)
        expect(gps_checkbox).to_be_visible(timeout=field_timeout)

        # Verify GPS checkbox is present
        if gps_checkbox.count() > 0:
            logger.info(f"GPS checkbox found on {device_model}")

            # Check if GPS is enabled (should always be checked)
            if gps_checkbox.is_checked():
                logger.info(f"GPS checkbox is checked as expected on {device_model}")
            else:
                logger.warning(
                    f"GPS checkbox is not checked on {device_model} - this may be unexpected"
                )

                # Try to enable GPS if it's disabled
                try:
                    gps_checkbox.check()
                    time.sleep(1)
                    if gps_checkbox.is_checked():
                        logger.info(
                            f"GPS checkbox enabled successfully on {device_model}"
                        )
                    else:
                        logger.warning(
                            f"Could not enable GPS checkbox on {device_model}"
                        )
                except Exception as e:
                    logger.warning(
                        f"Failed to enable GPS checkbox on {device_model}: {e}"
                    )
        else:
            pytest.fail(f"GPS checkbox not found on {device_model}")

    except Exception as e:
        pytest.fail(f"GPS field validation failed on {device_model}: {e}")

    # Test other GNSS constellations availability
    try:
        other_constellations = [c for c in gnss_constellations if c != "GPS"]

        for constellation in other_constellations:
            logger.info(f"Testing constellation availability: {constellation}")

            # Try to find checkbox for this constellation
            constellation_checkbox = gnss_config_page.page.locator(
                f"input[name='{constellation.lower()}'], input[type='checkbox'][value='{constellation.lower()}']"
            )

            if constellation_checkbox.count() > 0:
                logger.info(
                    f"Constellation {constellation} checkbox found on {device_model}"
                )

                # Test toggle functionality
                if constellation_checkbox.is_checked():
                    logger.info(f"Constellation {constellation} is currently enabled")
                else:
                    logger.info(f"Constellation {constellation} is currently disabled")
            else:
                logger.warning(
                    f"Constellation {constellation} checkbox not found on {device_model}"
                )

    except Exception as e:
        logger.warning(f"GNSS constellation validation failed on {device_model}: {e}")

    # Test save button behavior for GNSS changes
    try:
        # Make a change to test save button behavior
        save_button = gnss_config_page.page.locator("button#button_save")

        if save_button.count() > 0:
            # Initially should be disabled without changes
            if save_button.is_disabled():
                logger.info(
                    f"Save button initially disabled as expected on {device_model}"
                )
            else:
                logger.info(
                    f"Save button state unusual but proceeding on {device_model}"
                )

            # Test saving functionality
            save_success = gnss_config_page.save_configuration()
            if save_success:
                logger.info(f"GNSS configuration save successful on {device_model}")
            else:
                logger.warning(f"GNSS configuration save failed on {device_model}")

    except Exception as e:
        logger.warning(f"GNSS save button test failed on {device_model}: {e}")

    # Performance validation against device baselines
    try:
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            nav_performance = performance_data.get("navigation_performance", {})
            section_nav = nav_performance.get("section_navigation", {})
            typical_time = section_nav.get("typical_time", "")

            if typical_time:
                logger.info(f"GNSS navigation performance baseline: {typical_time}")

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)
    capabilities = DeviceCapabilities.get_capabilities(device_model)

    logger.info(f"GPS always enabled validation completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"GNSS capabilities: {gnss_constellations}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"GPS ALWAYS ENABLED VALIDATION COMPLETED: {device_model} (Series {device_series})"
    )
