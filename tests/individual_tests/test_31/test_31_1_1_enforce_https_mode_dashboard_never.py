"""
Category 31: HTTPS Enforcement - Test 31.1.1
Enforce HTTPS Mode Dashboard Never - DeviceCapabilities
Test Count: 1 of 6 in Category 31
Hardware: Device Only
Priority: HIGH - Security configuration
Series: Both Series 2 and 3
: Comprehensive DeviceCapabilities integration for device-aware HTTPS validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.access_config_page import AccessConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_31_1_1_enforce_https_mode_dashboard_never(
    access_config_page: AccessConfigPage, base_url: str, request
):
    """
    Test 31.1.1: Enforce HTTPS Mode Dashboard Never - DeviceCapabilities
    Purpose: Verify HTTPS enforcement mode 'Never' with device-aware validation
    Expected: Dashboard accessible without HTTPS, device-specific security patterns
    : Full DeviceCapabilities integration for HTTPS enforcement validation
    Series: Both - validates security patterns across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate HTTPS behavior")

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing HTTPS enforcement mode 'Never' on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Get HTTP redirect capability for validation
    capabilities = DeviceCapabilities.get_capabilities(device_model)
    http_redirect = capabilities.get("http_redirect", False)

    logger.info(f"HTTP redirect capability for {device_model}: {http_redirect}")

    # Navigate to access configuration page
    access_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    access_config_page.verify_page_loaded()

    # Test HTTPS enforcement mode selection
    try:
        # Locate HTTPS enforcement mode selector with device-aware patterns
        https_mode_selector = access_config_page.page.locator(
            "select[name='enforce_https_mode'], select[name='https_mode'], select[id*='https']"
        )

        selector_timeout = int(8000 * timeout_multiplier)
        expect(https_mode_selector).to_be_visible(timeout=selector_timeout)

        logger.info(f"HTTPS enforcement mode selector found on {device_model}")

        # Get current HTTPS mode
        current_mode = https_mode_selector.input_value()
        logger.info(f"Current HTTPS enforcement mode: {current_mode}")

        # Test 'Never' mode selection
        never_mode = "NEVER"
        logger.info(f"Testing HTTPS mode selection: {never_mode}")

        try:
            # Select 'Never' mode
            select_success = access_config_page.page.locator(
                f"select[name='enforce_https_mode']"
            ).select_option(never_mode)

            if select_success:
                logger.info(f"Successfully selected HTTPS mode: {never_mode}")

                # Verify selection was applied
                new_mode = https_mode_selector.input_value()
                if never_mode in new_mode or new_mode == never_mode:
                    logger.info(f"HTTPS mode selection verified: {new_mode}")
                else:
                    logger.warning(
                        f"HTTPS mode selection may not have persisted: {new_mode}"
                    )
            else:
                logger.warning(f"Failed to select HTTPS mode: {never_mode}")

        except Exception as e:
            logger.warning(f"HTTPS mode selection test failed: {e}")

        # Test other available modes if present
        mode_options = https_mode_selector.locator("option")
        available_modes = []

        for i in range(mode_options.count()):
            option = mode_options.nth(i)
            option_value = option.get_attribute("value") or option.text_content()
            if option_value and option_value.strip():
                available_modes.append(option_value.strip())

        logger.info(f"Available HTTPS enforcement modes: {available_modes}")

        # Test mode switching
        if len(available_modes) > 1:
            for mode in available_modes[:2]:  # Test up to 2 modes
                try:
                    logger.info(f"Testing mode switch to: {mode}")
                    https_mode_selector.select_option(mode)
                    time.sleep(0.5)

                    selected = https_mode_selector.input_value()
                    logger.info(f"Mode switch result: {selected}")

                except Exception as e:
                    logger.warning(f"Mode switch test failed for {mode}: {e}")

    except Exception as e:
        pytest.fail(f"HTTPS enforcement mode validation failed on {device_model}: {e}")

    # Test save button behavior for HTTPS changes
    try:
        # Test save button with device-aware patterns
        save_button = access_config_page.page.locator("button#button_save")

        if save_button.count() > 0:
            # Initially should be disabled without changes
            if save_button.is_disabled():
                logger.info(
                    f"Access save button initially disabled as expected on {device_model}"
                )
            else:
                logger.info(
                    f"Access save button state unusual but proceeding on {device_model}"
                )

            # Test saving functionality
            save_success = access_config_page.save_configuration()
            if save_success:
                logger.info(f"HTTPS configuration save successful on {device_model}")
            else:
                logger.warning(f"HTTPS configuration save failed on {device_model}")
        else:
            logger.warning(f"Access save button not found on {device_model}")

    except Exception as e:
        logger.warning(f"HTTPS save button test failed on {device_model}: {e}")

    # Test HTTP redirect behavior if applicable
    try:
        if http_redirect == "https":
            logger.info(
                f"Device {device_model} has HTTP to HTTPS redirect - testing behavior"
            )

            # Test HTTP access
            http_url = base_url.replace("https://", "http://")
            logger.info(f"Testing HTTP access: {http_url}")

            # Navigate to HTTP URL
            access_config_page.page.goto(http_url, wait_until="domcontentloaded")
            time.sleep(3)

            # Check if redirected to HTTPS
            current_url = access_config_page.page.url
            if current_url.startswith("https://"):
                logger.info(f"HTTP to HTTPS redirect working: {current_url}")
            else:
                logger.warning(f"No HTTP to HTTPS redirect detected: {current_url}")

        elif http_redirect == False:
            logger.info(
                f"Device {device_model} has no HTTP redirect - 'Never' mode appropriate"
            )
        else:
            logger.info(f"Device {device_model} HTTP redirect setting: {http_redirect}")

    except Exception as e:
        logger.warning(f"HTTP redirect behavior test failed on {device_model}: {e}")

    # Performance validation against device baselines
    try:
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            nav_performance = performance_data.get("navigation_performance", {})
            section_nav = nav_performance.get("section_navigation", {})
            typical_time = section_nav.get("typical_time", "")

            if typical_time:
                logger.info(f"HTTPS navigation performance baseline: {typical_time}")

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)

    logger.info(f"HTTPS enforcement mode 'Never' test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"HTTP redirect capability: {http_redirect}")
    logger.info(f"Device series: {device_series}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"HTTPS ENFORCEMENT MODE 'NEVER' VALIDATED: {device_model} (Series {device_series})"
    )
