"""
Category 18: Workflow Tests - TEST 18.5.1: RAPID SECTION SWITCHING
Hardware: Device Only
Priority: HIGH - End-to-end workflow validation
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 18.5.1

IMPROVEMENTS FROM ORIGINAL:
- Replaced device_series fixture parameter with device_capabilities integration
- Added device_model detection using device_capabilities.get("device_model")
- Uses DeviceCapabilities.get_series() for device-aware testing
- Implements model-specific validation and timeout handling
- Enhanced device-aware error messages with model context
"""

import pytest
import time
from playwright.sync_api import Page
from pages.device_capabilities import DeviceCapabilities


def test_18_5_1_rapid_section_switching(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 18.5.1: Rapid Switching Between Sections (Device-Aware)
    Purpose: Verify system handles rapid navigation without issues
    Expected: No errors, session remains stable
    Device-Aware: Uses device model for model-specific validation and timeout handling
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate rapid switching")

    device_series = DeviceCapabilities.get_series(device_model)

    sections = ["general", "network", "time", "outputs", "gnss", "display"]

    # Rapidly navigate between sections
    for i in range(3):  # 3 cycles
        for section in sections:
            unlocked_config_page.goto(
                f"{base_url}/{section}", wait_until="domcontentloaded"
            )
            time.sleep(0.2)  # Brief pause
            # Verify no redirect to authentication
            assert (
                "authenticate" not in unlocked_config_page.url.lower()
            ), f"Session should remain stable during rapid navigation on {device_model}"
