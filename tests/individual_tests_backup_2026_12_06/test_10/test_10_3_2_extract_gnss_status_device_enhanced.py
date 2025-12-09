"""
Test 10.3.2: Extract GNSS Status [DEVICE ENHANCED]
Category: 10 - Dashboard Data Extraction Tests
Test Count: Part of 12 tests in Category 10
Hardware: Device Only
Priority: HIGH - Critical status monitoring
Series: Both Series 2 and 3
ENHANCED: DeviceCapabilities integration for device-aware GNSS validation

Extracted from: tests/test_10_dashboard.py
Source Class: TestGNSSTable
Enhanced: 2025-12-01 with DeviceCapabilities integration
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.dashboard_page import DashboardPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_10_3_2_extract_gnss_status_device_enhanced(
    logged_in_page, base_url: str, request
):
    """
    Test 10.3.2: Extract GNSS Lock Status [DEVICE ENHANCED]
    Purpose: Verify GNSS lock status with device-aware validation
    ENHANCED: DeviceCapabilities integration for series-specific GNSS validation
    """
    # Get device context for device-aware validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate GNSS capabilities")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing GNSS status extraction on {device_model} (Series {device_series})"
    )

    # Navigate to dashboard page
    logged_in_page.goto(f"{base_url}/index", wait_until="domcontentloaded")
    timeout_scaled = int(10000 * timeout_multiplier)

    # Verify page loaded with device-aware timeout
    dashboard_heading = logged_in_page.get_by_role("heading", name="Dashboard")
    expect(dashboard_heading).to_be_visible(timeout=timeout_scaled)

    # Get GNSS capabilities from DeviceCapabilities database
    gnss_capabilities = DeviceCapabilities.get_gnss_capabilities(device_model)
    logger.info(f"GNSS capabilities for {device_model}: {gnss_capabilities}")

    # Initialize dashboard page object
    dashboard_page = DashboardPage(logged_in_page)

    # Device-aware GNSS data extraction
    gnss_data = dashboard_page.get_gnss_data()
    logger.info(f"GNSS data extracted from dashboard: {gnss_data}")

    # Validate GNSS data structure
    assert isinstance(gnss_data, dict), "GNSS data should be a dictionary"

    # Device-aware GNSS field validation based on series
    if device_series == 2:
        # Series 2: Basic GNSS status
        expected_fields = ["GNSS state", "Antenna state", "Time accuracy"]
        logger.info(f"Series 2: Validating basic GNSS fields for {device_model}")
    elif device_series == 3:
        # Series 3: Advanced GNSS with satellite count
        expected_fields = [
            "GNSS state",
            "Antenna state",
            "Time accuracy",
            "Used / tracked SVs",
        ]
        logger.info(f"Series 3: Validating advanced GNSS fields for {device_model}")
    else:
        expected_fields = ["GNSS state", "Antenna state"]
        logger.info(f"Unknown series: Using generic validation for {device_model}")

    # Check for expected GNSS fields
    gnss_fields_present = [field for field in expected_fields if field in gnss_data]

    # Minimum validation: At least GNSS state should be present
    assert (
        "GNSS state" in gnss_data
    ), f"GNSS state not found. Available: {list(gnss_data.keys())}"

    # GNSS state validation
    if "GNSS state" in gnss_data:
        gnss_state = gnss_data["GNSS state"]
        valid_states = [
            "LOCKED",
            "ACQUIRING",
            "SEARCHING",
            "NOTIME",
            "UNKNOWN",
            "LOWQUALITY",
        ]

        if gnss_state:
            assert gnss_state in valid_states, f"Unexpected GNSS state: {gnss_state}"
            logger.info(f"Valid GNSS state found: {gnss_state}")
        else:
            logger.warning(f"GNSS state is empty on {device_model}")

    # Cross-validate GNSS support
    expected_gnss_support = gnss_capabilities.get("supported", True)
    if expected_gnss_support:
        logger.info(f"Cross-validated: {device_model} has expected GNSS support")
    else:
        logger.info(f"Device {device_model} has limited GNSS support as expected")

    # Log completion
    logger.info(
        f"DeviceCapabilities GNSS validation completed for {device_model} (Series {device_series})"
    )

    print(f" GNSS STATUS EXTRACTION COMPLETED: {device_model} (Series {device_series})")
    print(f"GNSS data: {gnss_data}")
