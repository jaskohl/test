"""
Test 2.1.11: PTP Section Access - Pure Page Object Pattern

CATEGORY: 02 - Configuration Section Navigation
TEST TYPE: Pure Page Object Pattern
PRIORITY: HIGH
HARDWARE: Device Only
SERIES: Series 3 only (PTP not available on Series 2)

TRANSFORMATION SUMMARY:
- Pure page object architecture
- DeviceCapabilities ONLY for pytest.skip() conditions (per hybrid pattern)
- All other device logic through page object properties
- PTPConfigPage encapsulates device-specific logic

LOCATOR_STRATEGY_COMPLIANCE:
- Uses PTPConfigPage page object methods exclusively
- No direct .locator() calls in test logic
- Device-aware selectors through page object inheritance

CREATED: 2025-12-07 for pure page object transformation
"""

import pytest
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from conftest import wait_for_satellite_loading

# DeviceCapabilities ONLY for skip conditions
from pages.device_capabilities import DeviceCapabilities

# Page objects for all other device logic
from pages.ptp_config_page import PTPConfigPage

import logging

logger = logging.getLogger(__name__)


def test_2_1_11_ptp_section_access(unlocked_config_page: Page, base_url: str, request):
    """
    Test 2.1.11: PTP Section Access - Pure Page Object Pattern

    Purpose: Verify PTP configuration section access
    Expected: Series 3 devices navigate to PTP page; Series 2 skipped

    PURE PAGE OBJECT PATTERN:
    - DeviceCapabilities ONLY for skip conditions
    - All other device logic through page object properties
    - Timeouts handled by page objects internally
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate PTP configuration")

    # --- SKIP CONDITION (DeviceCapabilities allowed here) ---
    device_series = DeviceCapabilities.get_series(device_model)
    ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)

    if device_series == 2 or not ptp_supported:
        pytest.skip(
            f"PTP not supported on {device_model} (Series {device_series}) - "
            "PTP is only available on Series 3 devices"
        )
    # --- END SKIP CONDITION ---

    logger.info(f"Testing PTP section access on {device_model}")
    print(f"\n{'='*60}")
    print(f"DEVICE TEST: PTP Section Access")
    print(f"Device Model: {device_model}")
    print(f"Device Series: {device_series}")
    print(f"PTP Supported: {ptp_supported}")
    print(f"{'='*60}\n")

    # Create PTPConfigPage instance - all device logic encapsulated within
    ptp_page = PTPConfigPage(unlocked_config_page, device_model)

    # Get device info from page object properties (NOT DeviceCapabilities)
    ptp_interfaces = (
        ptp_page.get_ptp_interfaces() if hasattr(ptp_page, "get_ptp_interfaces") else []
    )

    # Get timeout from page object (page object uses DeviceCapabilities internally)
    series_timeout = ptp_page.DEFAULT_TIMEOUT

    print(f"PTP Interfaces: {ptp_interfaces}")
    print(f"Series-Specific Timeout: {series_timeout}ms")

    # Navigate to PTP page
    ptp_url = f"{base_url}/ptp"
    try:
        unlocked_config_page.goto(ptp_url, timeout=series_timeout)
        assert "ptp" in unlocked_config_page.url, "URL should contain 'ptp'"
        print(f"PTP URL verification passed: {unlocked_config_page.url}")

    except PlaywrightTimeoutError:
        error_msg = (
            f"Navigation to PTP page failed for device {device_model} "
            f"(Series {device_series}) within {series_timeout}ms timeout"
        )
        print(f"PTP NAVIGATION ERROR: {error_msg}")
        raise AssertionError(error_msg)

    # Wait for page load completion
    try:
        wait_for_satellite_loading(unlocked_config_page)
    except Exception as e:
        print(f"Satellite loading warning for device {device_model}: {str(e)}")

    # Expand all PTP panels (critical for Series 3 PTP access)
    try:
        if hasattr(ptp_page, "expand_all_ptp_panels"):
            panel_expansion_success = ptp_page.expand_all_ptp_panels()
            if panel_expansion_success:
                print(f"PTP panels expanded successfully for {device_model}")
            else:
                print(f"PTP panel expansion failed or not needed for {device_model}")
    except Exception as e:
        print(f"PTP panel expansion warning: {str(e)}")

    # Use PTPConfigPage's verify_page_loaded method for comprehensive validation
    try:
        print(f"Validating PTP page loaded using PTPConfigPage.verify_page_loaded()...")
        ptp_page.verify_page_loaded()
        print(f"PTP config page verification successful for {device_model}")
    except Exception as e:
        print(f"PTP config page verification failed: {e}")
        raise

    # Final validation assertions (using page object property for device_series)
    page_device_series = ptp_page.device_series
    print(f"\nPerforming final validation...")

    assert (
        page_device_series >= 3
    ), f"PTP should only be tested on Series 3+, found {page_device_series}"
    assert "ptp" in unlocked_config_page.url, "URL should contain 'ptp'"

    print(f"\n{'='*60}")
    print(f"PTP SECTION ACCESS TEST COMPLETED SUCCESSFULLY")
    print(f"Device: {device_model} (Series {page_device_series})")
    print(f"Test Result: PASSED")
    print(f"{'='*60}\n")

    logger.info(f"PTP section access test completed for {device_model}")
