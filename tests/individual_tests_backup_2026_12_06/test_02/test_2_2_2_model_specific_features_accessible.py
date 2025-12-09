"""
Test 2.2.2: Model-Specific Features Accessible - Device-Aware
Purpose: Verify device-specific configuration sections are accessible
Expected: PTP only on Series 3 devices, with model-specific interface counts

Category: 2 - Configuration Section Navigation
Test Type: Unit Test
Priority: HIGH
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities


def test_2_2_2_model_specific_features_accessible(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 2.2.2: Model-Specific Features Accessible - Device-Aware
    Purpose: Verify device-specific configuration sections are accessible
    Expected: PTP only on Series 3 devices, with model-specific interface counts
    MODERNIZED: Uses DeviceCapabilities for precise feature detection
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate device-specific features"
        )

    ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)
    ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)

    if ptp_supported:
        # Series 3 devices should have PTP configuration
        unlocked_config_page.goto(f"{base_url}/ptp")
        assert (
            "ptp" in unlocked_config_page.url
        ), f"Device {device_model} should have PTP section"

        # Verify PTP profile selector based on available interfaces
        available_profiles = []
        for interface in ptp_interfaces:
            try:
                profile_select = unlocked_config_page.locator(
                    f"select[name='ptp_profile_{interface}']"
                )
                if profile_select.count() > 0:
                    available_profiles.append(interface)
                    print(
                        f"Device {device_model}: PTP profile selector found for interface {interface}"
                    )
            except Exception:
                print(
                    f"Device {device_model}: No PTP profile selector for interface {interface}"
                )

        # Verify at least one PTP interface has a profile selector available
        assert (
            len(available_profiles) > 0
        ), f"Device {device_model} should have at least one PTP interface with profile selector"

        print(
            f"Device {device_model}: PTP configuration validated with {len(available_profiles)} interface(s)"
        )

    else:
        # Series 2 devices should NOT have PTP section
        unlocked_config_page.goto(f"{base_url}/")
        # Verify PTP section is not accessible for Series 2
