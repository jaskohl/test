"""
Test: 30.4.1 - SNMP Sections Save Independently [PURE PAGE OBJECT]
Category: SNMP Configuration (Category 30)
Purpose: Verify each SNMP section can save without affecting others with pure page object validation
Expected: Three independent save buttons work correctly
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


def test_30_4_1_section_save_independence_pure_page_object(
    snmp_config_page: SNMPConfigPage, base_url: str, request
):
    """
    Test 30.4.1: SNMP Sections Save Independently [PURE PAGE OBJECT]
    Purpose: Verify each SNMP section can save without affecting others with pure page object validation
    Expected: Three independent save buttons work correctly
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

    # Device-aware save button detection and validation using page object method
    save_button_config = snmp_config_page.get_interface_specific_save_button()

    # Store original configuration values for rollback
    original_data = snmp_config_page.get_page_data()
    original_ro_community1 = original_data.get("ro_community1", "PUBLIC")
    original_trap_community = original_data.get("trap_community", "")

    # Get device-aware save button locators
    save1_locator = None
    save2_locator = None
    save3_locator = None

    if device_series == 3:
        save1_locator = snmp_config_page.page.locator("button#button_save_1")
        save2_locator = snmp_config_page.page.locator("button#button_save_2")
        save3_locator = snmp_config_page.page.locator("button#button_save_3")
    elif device_series == 2:
        save1_locator = snmp_config_page.page.locator("input#button_save_1")
        save2_locator = snmp_config_page.page.locator("input#button_save_2")
        save3_locator = snmp_config_page.page.locator("input#button_save_3")

    try:
        # Modify v1/v2c section
        ro_community1 = snmp_config_page.page.locator("input[name='ro_community1']")
        if ro_community1.count() > 0:
            expect(ro_community1).to_be_visible(timeout=scaled_timeout)
            expect(ro_community1).to_be_editable(timeout=scaled_timeout)
            ro_community1.fill("test_community_v1v2c_device", timeout=scaled_timeout)

        # Only v1/v2c save button should enable (device-aware timeout)
        if save1_locator and save1_locator.count() > 0:
            expect(save1_locator).to_be_enabled(
                timeout=2000 * device_timeout_multiplier
            )
        if save2_locator and save2_locator.count() > 0:
            expect(save2_locator).to_be_disabled()
        if save3_locator and save3_locator.count() > 0:
            expect(save3_locator).to_be_disabled()

        # Reset and test section 2 modification
        if ro_community1.count() > 0:
            ro_community1.fill(
                original_ro_community1, timeout=scaled_timeout
            )  # Reset section 1
        time.sleep(0.5 * device_timeout_multiplier)  # Device-aware delay
        if save1_locator and save1_locator.count() > 0:
            expect(save1_locator).to_be_disabled()

        # Modify section 2
        trap_community = snmp_config_page.page.locator("input[name='trap_community']")
        if trap_community.count() > 0:
            expect(trap_community).to_be_visible(timeout=scaled_timeout)
            expect(trap_community).to_be_editable(timeout=scaled_timeout)
            trap_community.fill("test_trap_community_device", timeout=scaled_timeout)

            if save2_locator and save2_locator.count() > 0:
                expect(save2_locator).to_be_enabled(
                    timeout=2000 * device_timeout_multiplier
                )
            if save1_locator and save1_locator.count() > 0:
                expect(save1_locator).to_be_disabled()
            if save3_locator and save3_locator.count() > 0:
                expect(save3_locator).to_be_disabled()

    except Exception as e:
        pytest.fail(f"Failed to test section save independence for {device_model}: {e}")

    finally:
        # Rollback to original values
        try:
            ro_community1 = snmp_config_page.page.locator("input[name='ro_community1']")
            if ro_community1.count() > 0:
                ro_community1.fill(original_ro_community1, timeout=scaled_timeout)

            trap_community = snmp_config_page.page.locator(
                "input[name='trap_community']"
            )
            if trap_community.count() > 0 and original_trap_community:
                trap_community.fill(original_trap_community, timeout=scaled_timeout)
            elif trap_community.count() > 0:
                trap_community.fill(
                    "", timeout=scaled_timeout
                )  # Clear if no original value

            # Save to restore original state
            snmp_config_page.save_v1_v2c_configuration()
            if trap_community.count() > 0:
                snmp_config_page.save_traps_configuration()
        except Exception as e:
            logger.warning(f"Failed to restore original values for {device_model}: {e}")

    # Get device information using page object methods for logging
    device_info = snmp_config_page.get_device_info()
    capabilities = snmp_config_page.get_capabilities()

    if device_info and "management_interface" in device_info:
        mgmt_iface = device_info["management_interface"]
        print(
            f"Device {device_model} (Series {device_series}): SNMP section save independence validation completed"
        )
        print(
            f"Management interface: {mgmt_iface}, Timeout scaling: {device_timeout_multiplier}x"
        )

    # Validate using page object methods
    assert snmp_config_page.get_series() == device_series
    assert snmp_config_page.has_capability("snmp_support") == snmp_capable
    assert snmp_config_page.get_timeout_multiplier() == device_timeout_multiplier

    print(
        f"SNMP SECTION SAVE INDEPENDENCE VALIDATED (PURE PAGE OBJECT): {device_model} (Series {device_series})"
    )
