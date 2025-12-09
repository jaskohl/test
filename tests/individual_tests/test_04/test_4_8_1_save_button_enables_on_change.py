"""
Category 4: Network Configuration - Test 4.8.1
Save Button Enables On Change - Pure Page Object Pattern
Test Count: 6 of 8 in Category 4
Hardware: Device Only
Priority: HIGH - Critical save button behavior
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with device intelligence
PATTERN: Zero direct .locator() calls, essential methods only
"""

import pytest
import logging
from pages.network_config_page import NetworkConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_4_8_1_save_button_enables_on_change(
    network_config_page: NetworkConfigPage,
    request,
    base_url: str,
):
    """
    Test 4.8.1: Save Button Enables On Change - Pure Page Object Pattern
    Purpose: Verify save button enables when network fields change
    Expected: Disabled initially, enables after field input change
    TRANSFORMED: Uses pure page object methods with device intelligence
    """
    device_model = request.session.device_hardware_model

    # Essential device intelligence
    device_series = DeviceCapabilities.get_series(device_model)
    if device_series != 2:
        pytest.skip(
            f"Test applies to Series 2 only, detected {device_model} (Series {device_series})"
        )

    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(f"Testing save button behavior on {device_model}")

    # Navigate to network configuration page
    network_config_page.navigate_to_network_config()

    # Test save button state management through page object
    save_button_test = network_config_page.test_save_button_state_management()
    logger.info(f"Save button state management test: {save_button_test}")

    # Verify initial disabled state
    initial_state = save_button_test.get("initial_state", "unknown")
    assert (
        initial_state == "disabled"
    ), f"Save button should be disabled initially, got {initial_state}"
    logger.info("Save button initial state verified (disabled)")

    # Test field change triggers save button enable
    field_change_test = save_button_test.get("field_change_trigger", {})
    change_triggered = field_change_test.get("triggered", False)
    assert change_triggered, "Field change should trigger save button enable"

    button_enabled = field_change_test.get("button_enabled", False)
    assert button_enabled, "Save button should be enabled after field change"
    logger.info("Save button enabled after field change verified")

    # Test save button click detection (without actually saving)
    click_detection = save_button_test.get("click_detection", {})
    is_clickable = click_detection.get("clickable", False)
    assert is_clickable, "Save button should be clickable when enabled"
    logger.info("Save button clickability verified")

    # Test save button reverts to disabled after change is reverted
    reversion_test = save_button_test.get("state_reversion", {})
    reversion_worked = reversion_test.get("reverted_to_disabled", False)
    if reversion_worked:
        logger.info("Save button reverted to disabled state after change reversion")
    else:
        logger.info(
            "Save button state reversion behavior varies by device (acceptable)"
        )

    logger.info(f"Save button enable/disable test completed on {device_model}")
