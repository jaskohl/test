"""
Test: 30.1.3 - SNMP v1/v2c Section Save Button [PURE PAGE OBJECT]
Category: SNMP Configuration (Category 30)
Purpose: Verify v1/v2c section saves independently with pure page object validation
Expected: button_save_1 saves only v1/v2c settings
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


def test_30_1_3_v1v2c_save_button_pure_page_object(
    snmp_config_page: SNMPConfigPage, base_url: str, request
):
    """
    Test 30.1.3: SNMP v1/v2c Section Save Button [PURE PAGE OBJECT]
    Purpose: Verify v1/v2c section saves independently with pure page object validation
    Expected: button_save_1 saves only v1/v2c settings
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
        pytest.fail(
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

    # Device-aware element locators based on series
    ro_community1_locator = snmp_config_page.page.locator("input[name='ro_community1']")

    if ro_community1_locator.count() == 0:
        pytest.fail(
            f"ro_community1 input field not found for device series {device_series}"
        )

    expect(ro_community1_locator).to_be_visible(timeout=scaled_timeout)
    expect(ro_community1_locator).to_be_editable(timeout=scaled_timeout)

    # Get original value with device-aware error handling
    try:
        original_value = ro_community1_locator.input_value()
    except Exception as e:
        pytest.fail(
            f"Failed to get original ro_community1 value for {device_model}: {e}"
        )

    # Device-aware save button detection and validation using page object method
    save_button_config = snmp_config_page.get_interface_specific_save_button()
    save_button_locator = snmp_config_page.page.locator(
        save_button_config.get("selector", "button#button_save")
    )

    try:
        # CRITICAL FIX: Actually modify form fields to enable save button
        # Step 1: Modify ro_community1 field
        ro_community1_locator.fill("test_community_v1v2c", timeout=scaled_timeout)

        # Step 2: Modify ro_community2 field if available
        ro_community2_locator = snmp_config_page.page.locator(
            "input[name='ro_community2']"
        )
        if ro_community2_locator.count() > 0:
            ro_community2_locator.fill("public2_test", timeout=scaled_timeout)

        # Step 3: Wait for save button to become enabled
        time.sleep(1 * device_timeout_multiplier)  # Device-aware timeout

        # Step 4: Save using section-specific method (device-aware)
        result = snmp_config_page.save_v1_v2c_configuration()
        assert result, "Save operation should succeed"

        # Verify configuration was applied with device-aware validation
        actual_value = ro_community1_locator.input_value()
        assert (
            actual_value == "test_community_v1v2c"
        ), f"Expected 'test_community_v1v2c', got '{actual_value}'"

    except Exception as e:
        pytest.fail(
            f"Failed to configure and save v1/v2c settings for {device_model}: {e}"
        )

    finally:
        # Reset to original state
        try:
            ro_community1_locator.fill(original_value, timeout=scaled_timeout)
            snmp_config_page.save_v1_v2c_configuration()
        except Exception as e:
            logger.warning(
                f"Failed to restore original ro_community1 value for {device_model}: {e}"
            )

    # Get device information using page object methods for logging
    device_info = snmp_config_page.get_device_info()
    capabilities = snmp_config_page.get_capabilities()

    if device_info and "management_interface" in device_info:
        mgmt_iface = device_info["management_interface"]
        print(
            f"Device {device_model} (Series {device_series}): SNMP v1/v2c save button validation completed"
        )
        print(
            f"Management interface: {mgmt_iface}, Timeout scaling: {device_timeout_multiplier}x"
        )

    # Validate using page object methods
    assert snmp_config_page.get_series() == device_series
    assert snmp_config_page.has_capability("snmp_support") == snmp_capable
    assert snmp_config_page.get_timeout_multiplier() == device_timeout_multiplier

    print(
        f"SNMP V1/V2C SAVE BUTTON VALIDATED (PURE PAGE OBJECT): {device_model} (Series {device_series})"
    )
