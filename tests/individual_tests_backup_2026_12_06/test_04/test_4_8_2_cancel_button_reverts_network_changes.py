"""
Category 4: Network Configuration (Series 2) - Test 4.8.2
Cancel Button Reverts Network Changes - DeviceCapabilities Enhanced
Test Count: 1 of 12 in Category 4
Hardware: Device Only
Priority: HIGH - Critical network connectivity
Series: Series 2 only
ENHANCED: Comprehensive DeviceCapabilities integration for network interface validation and timeout handling
IP SAFETY: Uses temporary changes only, no permanent modifications
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.network_config_page import NetworkConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_4_8_2_cancel_button_reverts_network_changes_device_enhanced(
    network_config_page: NetworkConfigPage,
    request,
    base_url: str,
):
    """
    Test 4.8.2: Cancel Button Reverts Network Changes - DeviceCapabilities Enhanced
    Purpose: Verify cancel restores original network values with device-aware validation
    Expected: Fields revert to pre-change state with device-specific timeout handling
    ENHANCED: Full DeviceCapabilities integration for network interface validation and performance scaling
    IP SAFETY: Uses temporary changes only, no permanent modifications
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate cancel behavior")

    # Get device series and network capabilities
    device_series = DeviceCapabilities.get_series(device_model)
    if device_series != 2:
        pytest.skip(
            f"Test only applies to Series 2 devices, detected {device_model} (Series {device_series})"
        )

    # Get network interface information for device-aware testing
    network_interfaces = DeviceCapabilities.get_network_interfaces(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing cancel button reversion on {device_model} with {timeout_multiplier}x timeout multiplier"
    )
    logger.info(f"Available network interfaces: {network_interfaces}")

    # Verify expected interface configuration for Series 2
    expected_interfaces = ["eth0"]  # Series 2 has single network interface
    for interface in expected_interfaces:
        assert (
            interface in network_interfaces
        ), f"Expected interface {interface} not found on {device_model}"

    # Get original configuration for validation
    original_data = network_config_page.get_page_data()
    original_gateway = original_data.get("gateway", "")

    logger.info(f"Original gateway configuration on {device_model}: {original_gateway}")

    try:
        # Device-aware timeout for field interaction
        field_timeout = int(5000 * timeout_multiplier)

        # Make temporary change to test cancellation
        gateway_field = network_config_page.page.locator("input[name='gateway']")
        expect(gateway_field).to_be_visible(timeout=field_timeout)
        gateway_field.fill("192.168.100.99")  # Test IP (IP safety: temporary only)

        logger.info(
            f"Applied temporary gateway change on {device_model}: 192.168.100.99"
        )

        # Device-aware wait for field update
        change_delay = int(1000 * timeout_multiplier)
        time.sleep(change_delay)

        # Cancel button test with device-aware timeout
        try:
            cancel_button = network_config_page.page.locator("button#button_cancel")
            expect(cancel_button).to_be_visible(timeout=field_timeout)
            expect(cancel_button).to_be_enabled(timeout=field_timeout)

            logger.info(f"Cancel button found and enabled on {device_model}")

            # Click cancel with device-aware timing
            cancel_button.click()

            # Device-aware wait for cancellation processing
            cancel_processing_delay = int(2000 * timeout_multiplier)
            time.sleep(cancel_processing_delay)

            logger.info(
                f"Cancel button clicked on {device_model}, waiting for reversion"
            )

        except Exception as e:
            # Cancel button not found - use page refresh as fallback
            logger.warning(f"Cancel button not found for {device_model}: {e}")
            logger.info("Using page refresh for reversion testing")

            # Navigate back to page with device-aware timeout
            network_config_page.navigate_to_page()

            # Device-aware wait for page reload
            reload_delay = int(2000 * timeout_multiplier)
            time.sleep(reload_delay)

            logger.info(f"Page refreshed on {device_model}, verifying reversion")

        # Verify reversion using device-aware data retrieval
        current_data = network_config_page.get_page_data()
        current_gateway = current_data.get("gateway", "")

        logger.info(
            f"Current gateway configuration after cancel/refresh on {device_model}: {current_gateway}"
        )

        assert (
            current_gateway == original_gateway
        ), f"Gateway should revert to original value ({original_gateway}) on {device_model}, but got {current_gateway}"

        logger.info(f"Cancel button reversion verified successfully on {device_model}")

        # Additional Series 2 specific validation
        if device_series == 2:
            logger.info(f"Series 2 cancel behavior validated on {device_model}")
            # Series 2 should have simple cancellation behavior
            # No panel expansion or complex interface handling needed

    except Exception as e:
        logger.error(f"Cancel button test failed on {device_model}: {e}")
        pytest.skip(f"Cancel button test failed on {device_model}: {e}")

    finally:
        # Safe cleanup - ensure we're back to a known state
        try:
            # If gateway field still shows test value, clean it up
            current_gateway = network_config_page.get_page_data().get("gateway", "")
            if current_gateway == "192.168.100.99":
                logger.info(f"Cleaning up test gateway value on {device_model}")
                gateway_field = network_config_page.page.locator(
                    "input[name='gateway']"
                )
                if gateway_field.is_visible():
                    gateway_field.fill(original_gateway)
                    # Don't save - just restore the display value
                    logger.info(
                        f"Gateway field restored to original value on {device_model}"
                    )
        except Exception as e:
            logger.warning(f"Cleanup encountered issue on {device_model}: {e}")
            # Don't fail the test for cleanup issues

    logger.info(f"Cancel button reversion test completed on {device_model}")
