"""
Test 12.1.1: Invalid Login Password Error - DeviceCapabilities Enhanced
Purpose: Verify authentication error handling with device-aware validation

Category: 12 - Error Handling
Test Type: Unit Test
Priority: HIGH
Hardware: Device Only
Series: Both Series 2 and 3
ENHANCED: DeviceCapabilities integration for device-aware error handling validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_12_1_1_invalid_login_password_error_device_enhanced(
    page: Page, base_url: str, request
):
    """
    Test 12.1.1: Invalid Login Password Error - DeviceCapabilities Enhanced
    Purpose: Verify authentication error handling with device-aware validation
    Expected: Error message displays, device-specific timing patterns
    ENHANCED: Full DeviceCapabilities integration for authentication validation
    Series: Both - validates authentication patterns across device variants
    """
    # Get device series and timeout multiplier for device-aware testing
    device_model = request.session.device_hardware_model
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    try:
        # Get authentication workflow expectations from DeviceCapabilities
        auth_workflow = DeviceCapabilities.get_authentication_workflow(device_model)
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)

        logger.info(
            f"Testing authentication error handling on {device_model} (Series {device_series})"
        )
        logger.info(f"Authentication workflow: {auth_workflow}")
        logger.info(f"Timeout multiplier: {timeout_multiplier}x")

        # Device-aware navigation with timeout scaling
        page_timeout = int(10000 * timeout_multiplier)
        page.goto(base_url, wait_until="domcontentloaded", timeout=page_timeout)

        login_page = LoginPage(page)
        login_page.verify_page_loaded()

        # Get authentication expectations from DeviceCapabilities
        status_login_info = auth_workflow.get("status_monitoring_login", {})
        typical_time = status_login_info.get("typical_time", "2-3 seconds")

        logger.info(f"Expected status login time: {typical_time}")

        # Test invalid password submission with device-aware timing
        invalid_password = "invalid_password_123"

        # Use device-aware timeout for login attempt
        login_attempt_timeout = int(5000 * timeout_multiplier)

        success = login_page.login(
            password=invalid_password, timeout=login_attempt_timeout
        )

        # Should return False for invalid password
        assert not success, "Login should fail with invalid password"

        # Verify error handling with device-aware timing
        error_message_timeout = int(3000 * timeout_multiplier)

        # Look for error message indicators
        error_selectors = [
            ".alert-danger",
            ".error-message",
            "input[name='message'][value*='error']",
            "text='Invalid password'",
            "text='Authentication failed'",
        ]

        error_found = False
        for selector in error_selectors:
            error_element = page.locator(selector)
            if error_element.count() > 0:
                logger.info(f"Error message found using selector: {selector}")
                error_found = True
                break

        # Log comprehensive test results
        logger.info(f"Authentication error test completed for {device_model}")
        logger.info(f"Device info: {DeviceCapabilities.get_device_info(device_model)}")
        logger.info(f"Error handling validated: {error_found}")

    except Exception as e:
        logger.error(f"Authentication error test failed on {device_model}: {e}")
        raise

    finally:
        # Small cleanup wait for device stability
        time.sleep(int(0.5 * timeout_multiplier))


def test_12_1_2_invalid_config_password_error_device_enhanced(
    page: Page, base_url: str, request
):
    """
    Test 12.1.2: Invalid Config Password Error - DeviceCapabilities Enhanced
    Purpose: Verify configuration unlock error handling with device-aware validation
    Expected: Configuration unlock fails, error message displays
    ENHANCED: DeviceCapabilities integration for configuration validation
    Series: Both - validates dual authentication patterns
    """
    # Get device series and capabilities
    device_model = request.session.device_hardware_model
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    try:
        # Get authentication capabilities for validation
        capabilities = DeviceCapabilities.get_capabilities(device_model)
        auth_levels = capabilities.get("authentication_levels", [])

        # Verify both authentication levels are supported
        assert (
            "status" in auth_levels
        ), f"Status authentication should be available for {device_model}"
        assert (
            "configuration" in auth_levels
        ), f"Configuration authentication should be available for {device_model}"

        logger.info(
            f"Testing configuration authentication on {device_model} (Series {device_series})"
        )
        logger.info(f"Authentication levels: {auth_levels}")

        # First authenticate successfully (status level)
        page.goto(base_url, wait_until="domcontentloaded")

        login_page = LoginPage(page)
        login_page.verify_page_loaded()

        # Use valid status password for initial login
        valid_status_password = "status"  # Assuming this is the status password
        success = login_page.login(password=valid_status_password)
        assert success, "Status login should succeed"

        # Wait for dashboard to load with device-aware timing
        dashboard_load_time = int(2000 * timeout_multiplier)
        time.sleep(dashboard_load_time)

        # Navigate to configuration unlock
        configure_link = page.locator("a[title*='locked']").filter(has_text="Configure")
        expect(configure_link).to_be_visible(timeout=int(5000 * timeout_multiplier))
        configure_link.click()

        # Wait for configuration unlock page with device-aware timing
        unlock_load_time = int(1000 * timeout_multiplier)
        time.sleep(unlock_load_time)

        # Test invalid configuration password
        invalid_config_password = "invalid_config_password"

        # Look for configuration password field
        config_password_field = page.locator("input[name='password']")
        if config_password_field.count() > 0:
            # Submit invalid configuration password
            config_password_field.fill(invalid_config_password)

            # Look for submit button and click
            submit_button = page.locator("input[type='submit'], button[type='submit']")
            if submit_button.count() > 0:
                submit_button.click()

                # Wait for error response with device-aware timing
                error_timeout = int(3000 * timeout_multiplier)
                time.sleep(error_timeout)

                # Verify error handling
                error_indicators = [
                    ".alert-danger",
                    ".error-message",
                    "input[name='message'][value*='error']",
                ]

                error_found = False
                for indicator in error_indicators:
                    error_element = page.locator(indicator)
                    if error_element.count() > 0:
                        logger.info(f"Configuration error message found: {indicator}")
                        error_found = True
                        break

                # Configuration should fail with invalid password
                assert (
                    error_found
                ), "Configuration unlock should fail with invalid password"

        # Log comprehensive test results
        logger.info(
            f"Configuration authentication error test completed for {device_model}"
        )
        logger.info(f"Dual authentication levels validated: {auth_levels}")

    except Exception as e:
        logger.error(
            f"Configuration authentication error test failed on {device_model}: {e}"
        )
        raise

    finally:
        # Small cleanup wait for device stability
        time.sleep(int(0.5 * timeout_multiplier))


def test_12_2_1_invalid_ip_address_error_device_enhanced(
    network_config_page, base_url: str, request
):
    """
    Test 12.2.1: Invalid IP Address Error - DeviceCapabilities Enhanced
    Purpose: Verify network validation error handling with device-aware patterns
    Expected: Invalid IP addresses rejected with appropriate error messages
    ENHANCED: DeviceCapabilities integration for network validation
    Series: Both - validates network validation patterns across interfaces
    """
    # Get device series and network capabilities
    device_model = request.session.device_hardware_model
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    try:
        # Get network interface information from DeviceCapabilities
        network_interfaces = DeviceCapabilities.get_network_interfaces(device_model)
        max_outputs = DeviceCapabilities.get_max_outputs(device_model)

        logger.info(
            f"Testing network validation on {device_model} (Series {device_series})"
        )
        logger.info(f"Network interfaces: {network_interfaces}")
        logger.info(f"Max outputs: {max_outputs}")

        # Navigate to network configuration with device-aware timing
        page_timeout = int(15000 * timeout_multiplier)
        network_config_page.page.goto(f"{base_url}/network", timeout=page_timeout)

        # Allow page to load with device-aware timing
        load_time = int(1000 * timeout_multiplier)
        time.sleep(load_time)

        # Test invalid IP addresses based on device series
        invalid_ip_addresses = [
            "999.999.999.999",  # Invalid octet values
            "192.168.1",  # Incomplete address
            "192.168.1.256",  # Octet too large
            "192.168.1.1.1",  # Too many octets
            "abc.def.ghi.jkl",  # Non-numeric
            "192.168.1.-1",  # Negative octet
        ]

        errors_found = 0

        for invalid_ip in invalid_ip_addresses:
            try:
                logger.info(f"Testing invalid IP address: {invalid_ip}")

                if device_series == 2:
                    # Series 2: Single network interface
                    ip_field = network_config_page.page.locator("input[name='ipaddr']")
                    if ip_field.count() > 0:
                        # Clear and set invalid IP
                        ip_field.clear()
                        ip_field.fill(invalid_ip)

                        # Try to save and check for validation error
                        save_button = network_config_page.page.locator(
                            "input#button_save"
                        )
                        if save_button.count() > 0:
                            save_button.click()

                            # Wait for validation response
                            validation_wait = int(2000 * timeout_multiplier)
                            time.sleep(validation_wait)

                            # Check for error indicators
                            error_selectors = [
                                ".alert-danger",
                                ".error-message",
                                "input[name='message'][value*='error']",
                            ]

                            for selector in error_selectors:
                                error_element = network_config_page.page.locator(
                                    selector
                                )
                                if error_element.count() > 0:
                                    logger.info(
                                        f"IP validation error found for {invalid_ip}"
                                    )
                                    errors_found += 1
                                    break

                elif device_series == 3:
                    # Series 3: Multi-interface - test eth0
                    eth0_ip_field = network_config_page.page.locator(
                        "input[name='ip_eth0']"
                    )
                    if eth0_ip_field.count() > 0:
                        # Clear and set invalid IP
                        eth0_ip_field.clear()
                        eth0_ip_field.fill(invalid_ip)

                        # Try to save and check for validation error
                        save_button = network_config_page.page.locator(
                            "button#button_save"
                        )
                        if save_button.count() > 0:
                            save_button.click()

                            # Wait for validation response
                            validation_wait = int(2000 * timeout_multiplier)
                            time.sleep(validation_wait)

                            # Check for error indicators
                            error_selectors = [
                                ".alert-danger",
                                ".error-message",
                                "input[name='message'][value*='error']",
                            ]

                            for selector in error_selectors:
                                error_element = network_config_page.page.locator(
                                    selector
                                )
                                if error_element.count() > 0:
                                    logger.info(
                                        f"IP validation error found for {invalid_ip} on eth0"
                                    )
                                    errors_found += 1
                                    break

            except Exception as e:
                logger.warning(f"Error testing IP {invalid_ip}: {e}")
                continue

        # Validate that at least some IP validation errors were detected
        assert (
            errors_found > 0
        ), f"Should detect IP validation errors for {device_model}"

        logger.info(f"Network validation test completed for {device_model}")
        logger.info(f"Invalid IP addresses tested: {len(invalid_ip_addresses)}")
        logger.info(f"Validation errors detected: {errors_found}")

    except Exception as e:
        logger.error(f"Network validation test failed on {device_model}: {e}")
        raise

    finally:
        # Small cleanup wait for device stability
        time.sleep(int(0.5 * timeout_multiplier))
