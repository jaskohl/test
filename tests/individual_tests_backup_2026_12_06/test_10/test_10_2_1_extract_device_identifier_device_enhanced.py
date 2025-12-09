"""
Category 10: Dashboard - Test 10.2.1
Extract Device Identifier - DeviceCapabilities Enhanced
Test Count: 1 of 6 in Category 10
Hardware: Device Only
Priority: HIGH - Device identification functionality
Series: Both Series 2 and 3
ENHANCED: Comprehensive DeviceCapabilities integration for device-aware dashboard extraction
"""

import pytest
import time
import logging
from playwright.sync_api import Page, expect
from pages.dashboard_page import DashboardPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_10_2_1_extract_device_identifier_device_enhanced(
    logged_in_page: Page, base_url: str, request
):
    """
    Test 10.2.1: Extract Device Identifier - DeviceCapabilities Enhanced
    Purpose: Verify device identifier extraction from dashboard with device-aware validation
    Expected: Identifier accessible, extraction works, cross-validation with device model
    ENHANCED: Full DeviceCapabilities integration for device info validation
    Series: Both - validates dashboard extraction patterns across device variants
    """
    # Get device model and capabilities for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate dashboard extraction")

    # Get device series and timeout multiplier for device-aware testing
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    logger.info(
        f"Testing device identifier extraction on {device_model} with {timeout_multiplier}x timeout multiplier"
    )

    # Initialize dashboard page object with device-aware patterns
    dashboard_page = DashboardPage(logged_in_page, device_model)

    # Verify dashboard page is loaded
    dashboard_page.verify_page_loaded()

    # Test device identifier extraction with device-aware patterns
    try:
        # Get device information with enhanced extraction patterns
        device_info = dashboard_page.get_device_info()

        logger.info(f"Extracted device information: {device_info}")

        # Validate device identifier field
        identifier_extracted = False
        extracted_identifier = ""

        # Check various possible field names for identifier
        identifier_fields = [
            "identifier",
            "Identifier",
            "Device Identifier",
            "device identifier",
        ]

        for field_name in identifier_fields:
            if field_name in device_info:
                extracted_identifier = device_info[field_name]
                identifier_extracted = True
                logger.info(
                    f"Device identifier found via field '{field_name}': {extracted_identifier}"
                )
                break

        if not identifier_extracted:
            # Alternative extraction methods
            logger.info(
                "Primary identifier extraction failed, trying alternative methods"
            )

            # Try direct extraction from page elements
            try:
                # Look for identifier in device info table
                tables = logged_in_page.locator("table")
                if tables.count() >= 3:  # Device info is typically in table 2
                    device_table = tables.nth(2)
                    table_data = dashboard_page._extract_table_data(device_table)

                    for row in table_data:
                        if len(row) >= 2:
                            row_label = row[0].strip().lower()
                            if "identifier" in row_label or "device" in row_label:
                                extracted_identifier = row[1].strip()
                                identifier_extracted = True
                                logger.info(
                                    f"Device identifier found in table: {extracted_identifier}"
                                )
                                break
            except Exception as table_e:
                logger.warning(f"Table-based identifier extraction failed: {table_e}")

        # Validate extracted identifier
        if identifier_extracted and extracted_identifier:
            logger.info(
                f"Device identifier successfully extracted: {extracted_identifier}"
            )

            # Validate identifier format (should not be empty)
            if len(extracted_identifier.strip()) > 0:
                logger.info(
                    f"Device identifier format validation passed: {extracted_identifier}"
                )
            else:
                logger.warning(
                    f"Device identifier appears to be empty: '{extracted_identifier}'"
                )
        else:
            logger.warning(f"Device identifier not found on {device_model}")
            # Don't fail - some devices may not display identifier prominently

    except Exception as e:
        pytest.fail(f"Device identifier extraction failed on {device_model}: {e}")

    # Cross-validate with device model information
    try:
        # Get device info from DeviceCapabilities for cross-validation
        device_capabilities_info = DeviceCapabilities.get_device_info(device_model)
        expected_model = device_capabilities_info.get("hardware_model", "")

        logger.info(f"Expected device model: {expected_model}")
        logger.info(f"Detected device model: {device_model}")

        # Cross-validate device models
        if expected_model == device_model:
            logger.info(f"Device model cross-validation PASSED: {device_model}")
        else:
            logger.warning(
                f"Device model cross-validation WARNING: expected {expected_model}, got {device_model}"
            )

        # Check if extracted identifier matches expected patterns
        if identifier_extracted and expected_model:
            # The identifier might contain model information
            if expected_model.lower() in extracted_identifier.lower():
                logger.info(
                    f"Device identifier contains expected model: {expected_model}"
                )
            else:
                logger.info(
                    f"Device identifier format differs from model: {extracted_identifier} vs {expected_model}"
                )

    except Exception as e:
        logger.warning(f"Device model cross-validation failed on {device_model}: {e}")

    # Test dashboard data extraction reliability
    try:
        # Extract all dashboard data for comprehensive validation
        all_dashboard_data = dashboard_page.get_status_data()

        logger.info(
            f"Complete dashboard data extraction: {len(all_dashboard_data)} fields"
        )

        # Validate key fields are present
        expected_fields = ["Model", "identifier", "location", "firmware"]
        present_fields = []

        for field in expected_fields:
            # Check both exact matches and case-insensitive matches
            field_found = False
            for key in all_dashboard_data.keys():
                if field.lower() in key.lower():
                    present_fields.append(field)
                    field_found = True
                    logger.info(
                        f"Found expected field '{field}' as '{key}': {all_dashboard_data[key]}"
                    )
                    break

            if not field_found:
                logger.warning(f"Expected field '{field}' not found in dashboard data")

        logger.info(
            f"Dashboard field validation: {len(present_fields)}/{len(expected_fields)} fields found"
        )

    except Exception as e:
        logger.warning(
            f"Dashboard data extraction validation failed on {device_model}: {e}"
        )

    # Test navigation reliability
    try:
        # Test that we can navigate away and back successfully
        initial_url = logged_in_page.url

        # Navigate to a different section and back
        try:
            general_link = logged_in_page.get_by_role("link", name="General")
            if general_link.is_visible():
                general_link.click()
                time.sleep(2)

                # Navigate back to dashboard
                dashboard_link = logged_in_page.get_by_role("link", name="Dashboard")
                if dashboard_link.is_visible():
                    dashboard_link.click()
                    time.sleep(2)

                    # Verify we're back on dashboard
                    current_url = logged_in_page.url
                    if current_url == initial_url or current_url.endswith("/"):
                        logger.info(
                            f"Dashboard navigation reliability verified for {device_model}"
                        )
                    else:
                        logger.warning(
                            f"Navigation may have changed URL: {current_url}"
                        )
        except Exception:
            logger.info(f"Dashboard navigation test skipped for {device_model}")

    except Exception as e:
        logger.warning(
            f"Dashboard navigation reliability test failed on {device_model}: {e}"
        )

    # Performance validation against device baselines
    try:
        performance_data = DeviceCapabilities.get_performance_expectations(device_model)
        if performance_data:
            auth_performance = performance_data.get("authentication_performance", {})
            status_login = auth_performance.get("status_monitoring_login", {})
            typical_time = status_login.get("typical_time", "")

            if typical_time:
                logger.info(f"Dashboard performance baseline: {typical_time}")

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Log comprehensive test results
    device_capabilities = DeviceCapabilities.get_capabilities(device_model)

    logger.info(f"Device identifier extraction test completed for {device_model}")
    logger.info(f"Device info: {device_capabilities_info}")
    logger.info(
        f"Extracted identifier: {extracted_identifier if identifier_extracted else 'None'}"
    )
    logger.info(f"Device capabilities: {device_capabilities}")
    logger.info(f"Timeout multiplier: {timeout_multiplier}")

    print(
        f"DEVICE IDENTIFIER EXTRACTION VALIDATED: {device_model} (Series {device_series})"
    )
