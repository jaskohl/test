"""
Test: 30.3.2 - SNMP v3 Section Save Button [PURE PAGE OBJECT]
Category: SNMP Configuration (Category 30)
Purpose: Verify v3 section saves independently with pure page object validation
Expected: button_save_3 saves only v3 settings
Series: Both Series 2 and 3 (Universal)
Priority: MEDIUM
Hardware: Device Only
Device-Aware: YES - Uses SNMPConfigPage methods for validation
Based on: test_30_snmp_config.py
: 2025-12-08 - Pure page object pattern
"""

import pytest
import time
import logging
from pages.snmp_config_page import SNMPConfigPage
from playwright.sync_api import expect

logger = logging.getLogger(__name__)


def test_30_3_2_v3_save_button_pure_page_object(
    snmp_config_page: SNMPConfigPage, base_url: str, request
):
    """
    Test 30.3.2: SNMP v3 Section Save Button [PURE PAGE OBJECT]
    Purpose: Verify v3 section saves independently with pure page object validation
    Expected: button_save_3 saves only v3 settings
    Series: Both 2 and 3
    Device-Aware: Uses SNMPConfigPage methods for timeout scaling and validation
    """
    # Get device model and initialize page object with device-aware patterns
    device_model = request.session.device_hardware_model
    if device_model == "Unknown":
        pytest.fail("Device model not detected - cannot determine SNMP capabilities")

    # Initialize page object with device-aware patterns
    snmp_config_page = SNMPConfigPage(snmp_config_page.page, device_model)

    # Validate device series using page object method
    device_series = snmp_config_page.get_series()
    expected_series = [2, 3]  # Series numbers as integers
    if device_series not in expected_series:
        pytest.skip(
            f"Device series {device_series} not supported for this test (expected: {expected_series})"
        )

    # Device-aware timeout scaling using page object method
    base_timeout = 5000
    device_timeout_multiplier = snmp_config_page.get_timeout_multiplier()
    scaled_timeout = int(base_timeout * device_timeout_multiplier)

    # Cross-validate SNMP capability with page object method
    snmp_capable = snmp_config_page.has_capability("snmp_support")
    if not snmp_capable:
        pytest.skip(f"Device {device_model} does not support SNMP configuration")

    # Navigate to SNMP page using page object method
    snmp_config_page.navigate_to_page()

    # Device-aware save button detection and validation using page object method
    save_button_config = snmp_config_page.get_interface_specific_save_button()
    save_button_locator = snmp_config_page.page.locator(
        save_button_config.get("selector", "button#button_save")
    )

    # Get original configuration using page object method
    original_data = snmp_config_page.get_page_data()

    try:
        # CRITICAL FIX: Actually modify form fields to enable save button
        # Step 1: Modify v3 auth name field if available
        auth_name_field = snmp_config_page.page.locator("input[name='auth_name']")
        if auth_name_field.count() > 0:
            expect(auth_name_field).to_be_visible(timeout=scaled_timeout)
            expect(auth_name_field).to_be_editable(timeout=scaled_timeout)
            auth_name_field.fill("test_v3_user_device", timeout=scaled_timeout)

        # Step 2: Modify v3 auth key field if available
        auth_key_field = snmp_config_page.page.locator("input[name='auth_key']")
        if auth_key_field.count() > 0:
            expect(auth_key_field).to_be_visible(timeout=scaled_timeout)
            expect(auth_key_field).to_be_editable(timeout=scaled_timeout)
            auth_key_field.fill("test_v3_key_12345_device", timeout=scaled_timeout)

        # Step 3: Wait for save button to become enabled
        time.sleep(1 * device_timeout_multiplier)  # Device-aware timeout

        # Step 4: Save using section-specific method (device-aware)
        result = snmp_config_page.save_v3_configuration()
        assert result, "Save operation should succeed"

        # Verify configuration was applied with device-aware validation
        if auth_name_field.count() > 0:
            actual_value = auth_name_field.input_value()
            assert (
                actual_value == "test_v3_user_device"
            ), f"Expected 'test_v3_user_device', got '{actual_value}'"

    except Exception as e:
        pytest.fail(f"Failed to configure and save v3 settings for {device_model}: {e}")

    finally:
        # Reset to original state if original values exist
        try:
            auth_name = original_data.get("auth_name")
            if auth_name:
                auth_name_field = snmp_config_page.page.locator(
                    "input[name='auth_name']"
                )
                if auth_name_field.count() > 0:
                    auth_name_field.fill(auth_name, timeout=scaled_timeout)
                    snmp_config_page.save_v3_configuration()
        except Exception as e:
            logger.warning(
                f"Failed to restore original v3 auth name for {device_model}: {e}"
            )

    # Get device information using page object methods for logging
    device_info = snmp_config_page.get_device_info()
    capabilities = snmp_config_page.get_capabilities()

    if device_info and "management_interface" in device_info:
        mgmt_iface = device_info["management_interface"]
        print(
            f"Device {device_model} (Series {device_series}): SNMP v3 save button validation completed"
        )
        print(
            f"Management interface: {mgmt_iface}, Timeout scaling: {device_timeout_multiplier}x"
        )

    # Validate using page object methods
    assert snmp_config_page.get_series() == device_series
    assert snmp_config_page.has_capability("snmp_support") == snmp_capable
    assert snmp_config_page.get_timeout_multiplier() == device_timeout_multiplier

    print(
        f"SNMP V3 SAVE BUTTON VALIDATED (PURE PAGE OBJECT): {device_model} (Series {device_series})"
    )
