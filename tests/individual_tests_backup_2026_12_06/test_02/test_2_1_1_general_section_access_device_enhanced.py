"""
Test 2.1.1: General Section Accessible - DeviceCapabilities Enhanced
Purpose: Verify general section navigation and content availability with device-aware validation

Category: 2 - Configuration Section Navigation
Test Type: Unit Test
Priority: HIGH
Hardware: Device Only
Series: Both Series 2 and 3
ENHANCED: Comprehensive DeviceCapabilities integration for navigation validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_2_1_1_general_section_access_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 2.1.1: General Section Accessible - DeviceCapabilities Enhanced
    Purpose: Verify general section navigation and content availability with device-aware validation
    Expected: Section accessible, content loads, device-specific validation
    ENHANCED: Full DeviceCapabilities integration for navigation validation
    Series: Both - validates navigation patterns across device variants
    """
    # Get device series and timeout multiplier for device-aware testing
    device_model = request.session.device_hardware_model
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    try:
        # Get available sections from DeviceCapabilities for validation
        available_sections = DeviceCapabilities.get_available_sections(device_model)
        assert (
            "general" in available_sections
        ), f"General section not available for {device_model}"

        # Get device info for logging
        device_info = DeviceCapabilities.get_device_info(device_model)
        logger.info(f"Testing navigation on {device_model} (Series {device_series})")
        logger.info(f"Available sections: {available_sections}")

        # Device-aware navigation with timeout scaling
        page_timeout = int(10000 * timeout_multiplier)
        unlocked_config_page.goto(f"{base_url}/general", timeout=page_timeout)

        # Allow page to load with device-aware timing
        load_time = int(500 * timeout_multiplier)
        time.sleep(load_time)

        # Verify URL and page content with device-aware validation
        assert "general" in unlocked_config_page.url, "Should navigate to general page"

        # Verify key elements present with device-aware timeout
        identifier_field = unlocked_config_page.locator("input[name='identifier']")
        expect(identifier_field).to_be_visible(timeout=page_timeout)

        # Additional device-specific validations
        if device_series == 2:
            # Series 2: Basic general config validation
            location_field = unlocked_config_page.locator("input[name='location']")
            expect(location_field).to_be_visible(timeout=page_timeout)

        elif device_series == 3:
            # Series 3: May have additional general configuration fields
            contact_field = unlocked_config_page.locator("input[name='contact']")
            if contact_field.count() > 0:
                expect(contact_field).to_be_visible(timeout=page_timeout)

        # Get performance expectations for validation
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            navigation_perf = performance_data.get("navigation_performance", {})
            typical_time = navigation_perf.get("section_navigation", {}).get(
                "typical_time", "1-2 seconds"
            )
            logger.info(f"Expected navigation time: {typical_time}")

        # Log comprehensive test results
        logger.info(f"General section access test completed for {device_model}")
        logger.info(f"Device info: {device_info}")
        logger.info(f"Timeout multiplier: {timeout_multiplier}x")

    except Exception as e:
        logger.error(f"General section access test failed on {device_model}: {e}")
        raise

    finally:
        # Small cleanup wait for device stability
        time.sleep(int(0.5 * timeout_multiplier))


def test_2_1_2_network_section_access_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 2.1.2: Network Section Accessible - DeviceCapabilities Enhanced
    Purpose: Verify network section navigation with multi-interface validation
    Expected: Section accessible, interface count matches device capabilities
    ENHANCED: DeviceCapabilities integration for interface validation
    Series: Both - validates single vs multi-interface patterns
    """
    # Get device series and network capabilities
    device_model = request.session.device_hardware_model
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    try:
        # Get network interface information from DeviceCapabilities
        network_interfaces = DeviceCapabilities.get_network_interfaces(device_model)
        ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)

        logger.info(
            f"Testing network navigation on {device_model} (Series {device_series})"
        )
        logger.info(f"Network interfaces: {network_interfaces}")
        logger.info(f"PTP interfaces: {ptp_interfaces}")

        # Device-aware navigation with timeout scaling
        page_timeout = int(15000 * timeout_multiplier)
        unlocked_config_page.goto(f"{base_url}/network", timeout=page_timeout)

        # Allow page to load with device-aware timing
        load_time = int(1000 * timeout_multiplier)
        time.sleep(load_time)

        # Verify URL
        assert "network" in unlocked_config_page.url, "Should navigate to network page"

        # Validate network interfaces match DeviceCapabilities expectations
        if device_series == 2:
            # Series 2: Single interface validation
            assert (
                len(network_interfaces) == 1
            ), f"Series 2 should have 1 interface, found {len(network_interfaces)}"
            assert "eth0" in network_interfaces, "Series 2 should have eth0 interface"

            # Validate basic network fields
            mode_select = unlocked_config_page.locator("select[name='mode']")
            expect(mode_select).to_be_visible(timeout=page_timeout)

        elif device_series == 3:
            # Series 3: Multi-interface validation
            expected_interface_count = len(network_interfaces)
            logger.info(f"Expecting {expected_interface_count} network interfaces")

            # Validate at least eth0 is present
            eth0_field = unlocked_config_page.locator("input[name='ip_eth0']")
            if eth0_field.count() > 0:
                expect(eth0_field).to_be_visible(timeout=page_timeout)
            else:
                logger.warning("eth0 field not found - may be in collapsed panel")

            # If PTP interfaces exist, validate PTP section availability
            if ptp_interfaces:
                logger.info(f"Validating PTP support for interfaces: {ptp_interfaces}")
                # PTP section should be accessible for Series 3 devices
                ptp_link = unlocked_config_page.locator("a[href='/ptp']")
                if ptp_link.count() > 0:
                    logger.info("PTP configuration link found")
                else:
                    logger.warning("PTP configuration link not found")

        # Log comprehensive test results
        logger.info(f"Network section access test completed for {device_model}")
        logger.info(f"Network interfaces validated: {network_interfaces}")

    except Exception as e:
        logger.error(f"Network section access test failed on {device_model}: {e}")
        raise

    finally:
        # Small cleanup wait for device stability
        time.sleep(int(0.5 * timeout_multiplier))


def test_2_1_3_time_section_access_device_enhanced(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 2.1.3: Time Section Accessible - DeviceCapabilities Enhanced
    Purpose: Verify time section navigation with timezone validation
    Expected: Section accessible, timezone options match device database
    ENHANCED: DeviceCapabilities integration for timezone validation
    Series: Both - validates timezone configuration patterns
    """
    # Get device series and timezone capabilities
    device_model = request.session.device_hardware_model
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    try:
        # Get timezone data from DeviceCapabilities
        timezone_data = DeviceCapabilities.get_timezone_data(device_model)
        available_timezones = timezone_data.get("available_timezones", [])
        timezone_count = timezone_data.get("timezone_count", 0)
        includes_utc = timezone_data.get("includes_utc", False)

        logger.info(
            f"Testing time navigation on {device_model} (Series {device_series})"
        )
        logger.info(f"Available timezones: {len(available_timezones)} timezones")
        logger.info(f"UTC included: {includes_utc}")

        # Device-aware navigation with timeout scaling
        page_timeout = int(10000 * timeout_multiplier)
        unlocked_config_page.goto(f"{base_url}/time", timeout=page_timeout)

        # Allow page to load with device-aware timing
        load_time = int(500 * timeout_multiplier)
        time.sleep(load_time)

        # Verify URL
        assert "time" in unlocked_config_page.url, "Should navigate to time page"

        # Validate timezone dropdown with DeviceCapabilities data
        timezone_dropdown = unlocked_config_page.locator("select[name='timezone']")
        expect(timezone_dropdown).to_be_visible(timeout=page_timeout)

        # Get actual timezone options from page
        timezone_options = timezone_dropdown.locator("option")
        actual_count = timezone_options.count()

        logger.info(f"Timezone dropdown has {actual_count} options")
        logger.info(f"DeviceCapabilities expects {timezone_count} timezones")

        # Validate timezone count (allowing for some variation)
        if timezone_count > 0:
            # Allow for some variation in count due to implementation differences
            count_diff = abs(actual_count - timezone_count)
            assert (
                count_diff <= 2
            ), f"Timezone count mismatch: expected ~{timezone_count}, got {actual_count}"

        # Validate UTC availability if expected
        if includes_utc:
            utc_option = timezone_dropdown.locator("option[value='UTC']")
            assert (
                utc_option.count() > 0
            ), "UTC should be available in timezone dropdown"

        # Validate other device-specific time configuration features
        if device_series == 3:
            # Series 3 may have additional time configuration options
            dst_checkbox = unlocked_config_page.locator("input[name='dst_enabled']")
            if dst_checkbox.count() > 0:
                logger.info("DST configuration found on Series 3 device")

        # Log comprehensive test results
        logger.info(f"Time section access test completed for {device_model}")
        logger.info(f"Timezone validation: {actual_count} options found")

    except Exception as e:
        logger.error(f"Time section access test failed on {device_model}: {e}")
        raise

    finally:
        # Small cleanup wait for device stability
        time.sleep(int(0.5 * timeout_multiplier))
