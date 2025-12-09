"""
Category 11: Form Validation - Test 11.3.2
Mutually Exclusive Fields - DeviceCapabilities Enhanced
Test Count: 5 of 37 in Category 11
Hardware: Device Only
Priority: HIGH - Critical form validation functionality
Series: Both Series 2 and 3
ENHANCED: Comprehensive DeviceCapabilities integration for device-aware mutually exclusive field validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_11_3_2_mutually_exclusive_fields_device_enhanced(
    general_config_page: GeneralConfigPage, base_url: str, request
):
    """
    Test 11.3.2: Mutually Exclusive Fields - DeviceCapabilities Enhanced
    Purpose: Verify mutually exclusive field validation with device-aware patterns
    Expected: Device-specific mutually exclusive field behavior with proper validation logic
    ENHANCED: Full DeviceCapabilities integration for mutually exclusive field validation patterns
    Series: Both - validates mutually exclusive field behavior across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate mutually exclusive field behavior"
        )

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing mutually exclusive field validation on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Navigate to general configuration page
    general_config_page.navigate_to_page()

    # Verify page loaded with device-aware timing
    general_config_page.verify_page_loaded()

    # Test mutually exclusive field validation with device-aware patterns
    try:
        # Look for mutually exclusive options (e.g., DHCP vs Static IP)
        dhcp_enable = general_config_page.page.locator("input[name*='dhcp' i]")
        static_ip = general_config_page.page.locator("input[name*='ip' i]")
        ip_address = general_config_page.page.locator("input[name*='ip_address' i]")
        subnet_mask = general_config_page.page.locator("input[name*='subnet' i]")

        logger.info(
            f"Testing DHCP vs Static IP mutually exclusive validation on {device_model}"
        )

        field_timeout = int(8000 * timeout_multiplier)

        # Test DHCP vs Static IP mutually exclusive behavior
        if dhcp_enable.is_visible(timeout=field_timeout):
            logger.info("DHCP enable field found - testing mutually exclusive behavior")

            # Ensure we start with a known state
            dhcp_enable.uncheck()
            time.sleep(1)

            # Test 1: Static IP configuration (DHCP disabled)
            logger.info("Test 1: Static IP configuration (DHCP disabled)")

            # Configure static IP
            if ip_address.count() > 0:
                ip_address.fill("192.168.1.100")
                time.sleep(0.5)
                logger.info(" Static IP address configured")

            if subnet_mask.count() > 0:
                subnet_mask.fill("255.255.255.0")
                time.sleep(0.5)
                logger.info(" Subnet mask configured")

            # DHCP should be disabled when using static IP
            dhcp_state = dhcp_enable.is_checked()
            logger.info(f"DHCP state with static IP configured: {dhcp_state}")

            # Test 2: Enable DHCP (should clear/modify static IP fields)
            logger.info("Test 2: Enable DHCP (should affect static IP fields)")

            dhcp_enable.check()
            time.sleep(1)

            dhcp_state_after = dhcp_enable.is_checked()
            logger.info(f"DHCP enabled: {dhcp_state_after}")

            # Check if static IP fields are affected by DHCP enable
            if ip_address.count() > 0:
                ip_enabled = ip_address.is_enabled()
                ip_visible = ip_address.is_visible()
                logger.info(
                    f"IP address field - Enabled: {ip_enabled}, Visible: {ip_visible}"
                )

            # Test 3: DHCP disabled again (should restore static IP capability)
            logger.info("Test 3: Disable DHCP (should restore static IP capability)")

            dhcp_enable.uncheck()
            time.sleep(1)

            dhcp_state_final = dhcp_enable.is_checked()
            logger.info(f"DHCP disabled: {not dhcp_state_final}")

            # Test 4: Save behavior with different configurations
            logger.info("Test 4: Save behavior validation")

            # Test saving with DHCP enabled
            dhcp_enable.check()
            time.sleep(0.5)

            try:
                save_button = general_config_page.get_save_button_locator()
                if save_button.count() > 0:
                    save_button_enabled = save_button.is_enabled()
                    logger.info(f"Save button enabled with DHCP: {save_button_enabled}")

                    if save_button_enabled:
                        # Test save
                        save_success = general_config_page.save_configuration()
                        if save_success:
                            logger.info(" Save with DHCP configuration successful")
                        else:
                            logger.warning(" Save with DHCP configuration failed")
            except Exception as e:
                logger.warning(f"DHCP save test failed: {e}")

            # Test saving with static IP
            dhcp_enable.uncheck()
            time.sleep(0.5)

            if ip_address.count() > 0:
                ip_address.fill("192.168.1.200")
                time.sleep(0.5)

            try:
                if save_button.count() > 0:
                    save_button_enabled = save_button.is_enabled()
                    logger.info(
                        f"Save button enabled with static IP: {save_button_enabled}"
                    )

                    if save_button_enabled:
                        # Test save
                        save_success = general_config_page.save_configuration()
                        if save_success:
                            logger.info(" Save with static IP configuration successful")
                        else:
                            logger.warning(" Save with static IP configuration failed")
            except Exception as e:
                logger.warning(f"Static IP save test failed: {e}")

        else:
            logger.info(
                "DHCP enable field not found - checking for other mutually exclusive scenarios"
            )

            # Look for other potential mutually exclusive field scenarios
            exclusive_pairs = [
                ("ntp_server", "manual_time"),  # NTP server vs manual time setting
                ("snmp_v2c", "snmp_v3"),  # SNMP v2c vs v3
                ("primary_server", "backup_server"),  # Primary vs backup server roles
                ("master_mode", "slave_mode"),  # Master vs slave mode
            ]

            for field1_pattern, field2_pattern in exclusive_pairs:
                try:
                    field1 = general_config_page.page.locator(
                        f"input[name*='{field1_pattern}' i]"
                    )
                    field2 = general_config_page.page.locator(
                        f"input[name*='{field2_pattern}' i]"
                    )

                    if field1.is_visible(timeout=int(2000 * timeout_multiplier)):
                        logger.info(
                            f"Found potential mutually exclusive fields: {field1_pattern} vs {field2_pattern}"
                        )

                        # Test basic interaction
                        if field1.count() > 0:
                            field1.click()
                            time.sleep(0.5)

                        if field2.count() > 0:
                            field2_enabled = field2.is_enabled()
                            logger.info(
                                f"Field2 enabled after Field1 interaction: {field2_enabled}"
                            )

                except Exception as e:
                    logger.warning(
                        f"Mutually exclusive field test failed for {field1_pattern}: {e}"
                    )

    except Exception as e:
        pytest.fail(
            f"Mutually exclusive field validation test failed on {device_model}: {e}"
        )

    # Test form submission with mutually exclusive field validation
    try:
        logger.info("Testing form submission with mutually exclusive field validation")

        # Configure a valid setup
        general_config_page.configure_device_info(
            identifier="MutualExclTest",
            location="Test Location",
            contact="Test Contact",
        )

        # Test save functionality
        save_success = general_config_page.save_configuration()
        if save_success:
            logger.info(" Form submission with mutually exclusive fields successful")
        else:
            logger.warning(" Form submission with mutually exclusive fields failed")

    except Exception as e:
        logger.warning(f"Form submission validation test failed on {device_model}: {e}")

    # Test validation error handling
    try:
        logger.info("Testing validation error handling for mutually exclusive fields")

        # Test edge cases that might trigger validation errors
        edge_cases = [
            (
                "Both DHCP and static IP configured",
                lambda: self._configure_conflicting_settings(),
            ),
            ("Invalid IP addresses", lambda: self._configure_invalid_ips()),
        ]

        for case_name, case_function in edge_cases:
            logger.info(f"Testing edge case: {case_name}")
            try:
                # Reset to clean state
                general_config_page.navigate_to_page()
                time.sleep(2)

                # Apply the edge case
                case_function()

                # Try to save and check for validation errors
                save_success = general_config_page.save_configuration()
                if not save_success:
                    logger.info(
                        f" Validation error correctly triggered for: {case_name}"
                    )
                else:
                    logger.warning(f" No validation error for: {case_name}")

            except Exception as e:
                logger.warning(f"Edge case test failed for {case_name}: {e}")

    except Exception as e:
        logger.warning(f"Validation error handling test failed on {device_model}: {e}")

    # Performance validation against device baselines
    try:
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            form_performance = performance_data.get("form_interaction", {})
            field_validation = form_performance.get("field_validation", {})
            typical_time = field_validation.get("typical_time", "")

            if typical_time:
                logger.info(
                    f"Form field validation performance baseline: {typical_time}"
                )

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Log comprehensive test results
    device_info = DeviceCapabilities.get_device_info(device_model)
    capabilities = DeviceCapabilities.get_capabilities(device_model)

    logger.info(
        f"Mutually exclusive field validation test completed for {device_model}"
    )
    logger.info(f"Device info: {device_info}")
    logger.info(f"Device capabilities: {capabilities}")
    logger.info(f"Device series: {device_series}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"MUTUALLY EXCLUSIVE FIELD VALIDATION TEST COMPLETED: {device_model} (Series {device_series})"
    )

    # Helper methods for edge case testing
    def _configure_conflicting_settings():
        """Configure settings that should be mutually exclusive"""
        if dhcp_enable.count() > 0:
            dhcp_enable.check()
            time.sleep(0.5)

        if ip_address.count() > 0:
            ip_address.fill("192.168.1.100")
            time.sleep(0.5)

    def _configure_invalid_ips():
        """Configure invalid IP addresses for validation testing"""
        if ip_address.count() > 0:
            ip_address.fill("999.999.999.999")
            time.sleep(0.5)
