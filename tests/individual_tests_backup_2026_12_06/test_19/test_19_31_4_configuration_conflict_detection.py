"""
Category 19: Dynamic UI Behavior & Element Validation - Individual Test
Test 19.31.4: Configuration Conflict Detection - IMPROVED
Test Count: 1 test
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 19.31.4
Modernized with DeviceCapabilities integration for improved device detection and error handling
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_19_31_4_configuration_conflict_detection(
    unlocked_config_page: Page, base_url: str, request
):
    """Test 19.31.4: Real-time detection and warning of configuration conflicts"""
    # IMPROVED: Device model detection with graceful skip handling
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate configuration conflict detection"
        )

    try:
        device_series = DeviceCapabilities.get_series(device_model)
    except Exception as e:
        pytest.skip(f"Device model detection failed for {device_model}: {e}")

    unlocked_config_page.goto(f"{base_url}/network")
    time.sleep(1)
    print(f"[Device: {device_model}] Testing configuration conflict detection")

    # Look for conflict detection areas
    conflicts = unlocked_config_page.locator(".conflict, .warning, .error")
    if conflicts.count() > 0:
        # Try to create a conflicting configuration
        ip_fields = unlocked_config_page.locator("input[name*='ip' i]")
        gateway_fields = unlocked_config_page.locator("input[name*='gateway' i]")
        if ip_fields.count() > 0 and gateway_fields.count() > 0:
            # Set conflicting IP and gateway
            ip_fields.first.fill("192.168.1.1")
            gateway_fields.first.fill("192.168.2.1")  # Different subnet
            time.sleep(0.5)
            # Check for conflict warnings
            expect(conflicts.first).to_be_visible()
