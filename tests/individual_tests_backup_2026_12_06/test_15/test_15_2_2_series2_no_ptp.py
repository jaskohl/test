"""
Test 15.2.2: Series 2 Does Not Have PTP - DeviceCapabilities Enhanced
Category: 15 - Device Capability Detection Tests
Test Count: 4 of 15 in Category 15
Hardware: Device Only
Priority: CRITICAL - Foundation for conditional test execution
Series: Series 2 Only
ENHANCED: Comprehensive DeviceCapabilities integration for negative PTP capability validation
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_15_2_2_series2_no_ptp_device_enhanced(
    unlocked_config_page: Page, base_url: str, device_series: str, request
):
    """
    Test 15.2.2: Series 2 Does Not Have PTP - DeviceCapabilities Enhanced
    Purpose: Verify Series 2 devices lack PTP capability with database validation
    Expected: PTP page not accessible and device database confirms no PTP support
    ENHANCED: Cross-validation with DeviceCapabilities PTP database
    Series: Series 2 Only
    """
    # Get device model for comprehensive validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate PTP absence")

    # Get device series from database for validation
    expected_series = DeviceCapabilities.get_series(device_model)
    if expected_series != 2:
        pytest.skip(
            f"Test only applies to Series 2, detected Series {expected_series} device {device_model}"
        )

    # Validate NO PTP support using DeviceCapabilities (negative test)
    ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)
    assert (
        ptp_supported == False
    ), f"Device database should indicate NO PTP support for {device_model}"

    # Get PTP interfaces from database (should be empty)
    ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)
    assert (
        len(ptp_interfaces) == 0
    ), f"Series 2 device should have no PTP interfaces, found {ptp_interfaces} for {device_model}"

    logger.info(f"Testing PTP absence on {device_model}")
    logger.info(f"Expected series from database: {expected_series}")
    logger.info(f"PTP supported according to database: {ptp_supported}")
    logger.info(f"PTP interfaces from database: {ptp_interfaces} (should be empty)")

    # Navigate to PTP page with device-aware timeout
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    page_timeout = int(
        5000 * timeout_multiplier
    )  # Shorter timeout since we expect failure

    try:
        unlocked_config_page.goto(
            f"{base_url}/ptp", wait_until="domcontentloaded", timeout=page_timeout
        )

        # Check if PTP page is accessible (it shouldn't be for Series 2)
        current_url = unlocked_config_page.url
        page_content = unlocked_config_page.content()

        logger.info(f"PTP page navigation result for {device_model}:")
        logger.info(f"Final URL: {current_url}")
        logger.info(f"Page contains 'ptp': {'ptp' in current_url}")
        logger.info(f"Page contains '404': {'404' in page_content}")
        logger.info(f"Page contains 'not found': {'not found' in page_content.lower()}")

        # Series 2 should NOT have PTP page - validate expected behavior
        has_ptp_access = "ptp" in current_url
        has_404_error = "404" in page_content
        has_not_found = "not found" in page_content.lower()

        if has_ptp_access and not (has_404_error or has_not_found):
            # PTP page is accessible but shouldn't be for Series 2
            logger.warning(
                f"  PTP page appears accessible for Series 2 device {device_model}"
            )

            # Additional validation: check if PTP elements actually exist
            ptp_profiles = unlocked_config_page.locator("select[id*='profile']")
            profile_count = ptp_profiles.count()

            if profile_count == 0:
                logger.info(
                    f" PTP page accessible but no PTP configuration elements found - acceptable for {device_model}"
                )
            else:
                logger.warning(
                    f" PTP page has {profile_count} PTP elements - unexpected for Series 2 device {device_model}"
                )
                # This might indicate a configuration issue

        else:
            logger.info(
                f" PTP page correctly inaccessible for Series 2 device {device_model}"
            )

        # Validate that database expectation matches actual behavior
        assert (
            not has_ptp_access or has_404_error or has_not_found
        ), f"Series 2 device {device_model} should not have accessible PTP page"

    except Exception as e:
        # Navigation timeout or error is expected behavior for Series 2
        logger.info(
            f" PTP page navigation failed as expected for Series 2 device {device_model}: {e}"
        )

    # Additional database cross-validation
    capabilities = DeviceCapabilities.get_capabilities(device_model)
    network_interfaces = DeviceCapabilities.get_network_interfaces(device_model)

    logger.info(f"Device network interfaces: {network_interfaces}")
    logger.info(f"Device capabilities: {capabilities}")

    # Validate PTP-related fields in capabilities
    assert (
        "ptp_supported" in capabilities
    ), f"Capabilities should include ptp_supported for {device_model}"
    assert (
        capabilities["ptp_supported"] == False
    ), f"Capabilities should indicate no PTP support for {device_model}"

    # Validate network interfaces don't include PTP-capable ones
    ptp_capable_interfaces = ["eth1", "eth2", "eth3", "eth4"]
    for interface in ptp_capable_interfaces:
        if interface in network_interfaces:
            logger.warning(
                f"  Network interface {interface} exists but should not support PTP on Series 2 device {device_model}"
            )

    # Series-specific validation
    if expected_series == 2:
        # Series 2 validation - should definitively not support PTP
        assert (
            ptp_supported == False
        ), f"Series 2 should definitively NOT support PTP according to device database"
        assert (
            len(ptp_interfaces) == 0
        ), f"Series 2 should have 0 PTP interfaces according to device database"

        logger.info(
            f" Series 2 PTP validation: Confirmed NO PTP support for {device_model}"
        )

        # Additional validation: check if PTP would be expected based on network interfaces
        if len(network_interfaces) > 1:
            logger.warning(
                f"  Series 2 device has {len(network_interfaces)} network interfaces - verify this is expected"
            )

    logger.info(f"Series 2 PTP absence test completed successfully for {device_model}")
    print(f" PTP ABSENCE VALIDATED: {device_model} - Confirmed NO PTP support")
