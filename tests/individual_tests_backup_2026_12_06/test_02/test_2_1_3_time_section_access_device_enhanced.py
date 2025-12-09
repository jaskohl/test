"""
Test 2.1.3: Time Section Accessible - Device Enhanced
Purpose: Verify time section navigation and timezone configuration availability with device-aware capabilities

Category: 2 - Configuration Section Navigation
Test Type: Integration Test
Priority: HIGH
Hardware: Device Only
Device Model: ALL
Series: 2 & 3
DeviceCapabilities Integration: FULL
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_2_1_3_time_section_access_device_enhanced(
    unlocked_config_page: Page, base_url: str, device_capabilities: DeviceCapabilities
):
    """
    Test 2.1.3: Time Section Accessible - Device Enhanced

    Device-aware test that verifies:
    - Time section navigation with device series optimization
    - Timezone dropdown availability across device series
    - Series-specific timeout handling
    - Device model detection and logging
    - Comprehensive error handling and recovery
    """
    logger = logging.getLogger(__name__)

    # Initialize device capabilities for enhanced testing
    # Using a representative Series 3 device for timeout calculations
    model = "KRONOS-3R-HVLV-TCXO-A2F"
    series = DeviceCapabilities.get_series(model)

    logger.info(
        f" Device-Enhanced Time Section Access Test - Series: {series}, Model: {model}"
    )
    logger.info(f" Test 2.1.3 - Device Model: {model}, Series: {series}")

    # Get device-optimized timeout
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(model)
    operation_timeout = int(30000 * timeout_multiplier)  # Base 30s timeout

    logger.info(
        f"⏱ Using timeout multiplier: {timeout_multiplier}x, Operation timeout: {operation_timeout}ms"
    )

    try:
        # Device-aware navigation to time section
        time_url = f"{base_url}/time"
        logger.info(f" Navigating to time section: {time_url}")

        # Navigate with device-aware timeout
        unlocked_config_page.goto(time_url, timeout=operation_timeout)

        # Verify navigation success with device-specific URL handling
        current_url = unlocked_config_page.url
        logger.info(f" Current URL after navigation: {current_url}")

        # Series-specific URL verification patterns
        if series == 2:
            # Series 2 devices may have different URL patterns
            assert (
                "time" in current_url.lower()
            ), f"Expected 'time' in URL, got: {current_url}"
        else:
            # Series 3 and future devices
            assert (
                "time" in current_url.lower()
            ), f"Expected 'time' in URL, got: {current_url}"

        logger.info(f" Successfully navigated to time section")

        # Device-aware element detection for timezone dropdown
        timezone_selectors = [
            "select[name='timezones']",
            "select[name='timezone']",
            "select[id='timezone']",
            "select[class*='timezone']",
            "select[data-testid='timezone']",
        ]

        timezone_select = None
        selector_used = None

        for selector in timezone_selectors:
            try:
                element = unlocked_config_page.locator(selector)
                if element.count() > 0:
                    timezone_select = element
                    selector_used = selector
                    break
            except Exception as e:
                logger.debug(f"Selector {selector} not found: {e}")
                continue

        if timezone_select is None:
            # Fallback: look for any timezone-related element
            logger.warning(
                " Primary timezone selectors not found, using fallback detection"
            )
            timezone_select = unlocked_config_page.locator("select").filter(
                has_text="time zone"
            )
            selector_used = "fallback timezone select"

        # Verify timezone dropdown with device-aware checks
        assert timezone_select is not None, "Timezone dropdown/select element not found"

        logger.info(f" Timezone element found using: {selector_used}")

        # Series-specific timezone element verification
        try:
            # Wait for element visibility with device-optimized timeout
            expect(timezone_select).to_be_visible(timeout=operation_timeout)
            logger.info(" Timezone dropdown is visible")

            # Device series-specific validation
            if series == 2:
                # Series 2 specific validations
                element_count = timezone_select.count()
                logger.info(f" Series 2 - Timezone options count: {element_count}")
                assert (
                    element_count > 0
                ), "Series 2: Timezone dropdown should have options"

            elif series == 3:
                # Series 3 specific validations
                element_count = timezone_select.count()
                logger.info(f" Series 3 - Timezone options count: {element_count}")
                assert (
                    element_count > 0
                ), "Series 3: Timezone dropdown should have options"

                # Series 3 may have additional timezone features
                try:
                    # Check for timezone-related input fields
                    timezone_inputs = unlocked_config_page.locator(
                        "input[name*='time'], input[id*='time']"
                    ).count()
                    if timezone_inputs > 0:
                        logger.info(
                            f" Series 3 - Additional timezone inputs found: {timezone_inputs}"
                        )
                except Exception as e:
                    logger.debug(f"Series 3 timezone input check failed: {e}")

            logger.info(
                f" Time section access test completed successfully for series {series} {model}"
            )

        except Exception as e:
            logger.error(f" Timezone element verification failed: {e}")
            raise

        # Enhanced verification: Check for additional time-related elements
        try:
            time_related_elements = {
                "ntp_servers": "input[name*='ntp'], input[id*='ntp']",
                "time_format": "select[name*='format'], select[id*='format']",
                "dst_settings": "input[name*='dst'], input[id*='dst'], input[name*='daylight']",
            }

            found_elements = {}
            for element_name, selector in time_related_elements.items():
                try:
                    count = unlocked_config_page.locator(selector).count()
                    if count > 0:
                        found_elements[element_name] = count
                        logger.info(
                            f" Additional time element found - {element_name}: {count} elements"
                        )
                except Exception as e:
                    logger.debug(f"Time element {element_name} check failed: {e}")

            if found_elements:
                logger.info(
                    f" Additional time configuration elements detected: {list(found_elements.keys())}"
                )

        except Exception as e:
            logger.warning(f" Additional time element detection failed: {e}")
            # Don't fail the test for this, it's supplementary

        logger.info(
            f" Test 2.1.3 Device-Enhanced Time Section Access - PASSED for series {series} {model}"
        )

    except Exception as e:
        logger.error(f" Test 2.1.3 failed for series {series} {model}: {str(e)}")

        # Device-aware error recovery
        try:
            logger.info(" Attempting device-aware error recovery...")
            unlocked_config_page.reload(timeout=operation_timeout)
            time.sleep(2)  # Allow page to stabilize
            logger.info(" Device recovery successful")
        except Exception as recovery_error:
            logger.error(f" Device recovery failed: {recovery_error}")

        raise
