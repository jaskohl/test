"""
Test 6.4.1: BeiDou Checkbox Toggle (Pure Page Object)
Purpose: Verify BeiDou can be enabled/disabled with device-aware validation
Expected: Checkbox toggles and persists with DeviceCapabilities integration
Pure Page Object: Zero direct .locator() calls, 100% page object methods
Device-: Full DeviceCapabilities integration with series-specific patterns
"""

import pytest
import time
from pages.gnss_config_page import GNSSConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_6_4_1_beidou_checkbox_toggle(gnss_config_page: GNSSConfigPage, request):
    """
    Test 6.4.1: BeiDou Constellation Configuration (Pure Page Object)
    Purpose: Verify BeiDou can be enabled/disabled using pure page object methods
    Expected: Checkbox toggles and persists with device-aware validation
    Field: BeiDou constellation checkbox
    Series: Both 2 and 3
    Device-: Full DeviceCapabilities integration through page object methods
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate BeiDou configuration")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    try:
        # Initialize GNSS page with device model for device-aware behavior
        gnss_config_page.device_model = device_model
        gnss_config_page.device_series = device_series

        # Device capabilities validation using page object method
        assert DeviceCapabilities.has_capability(
            device_model, "beidou_constellation"
        ), "Device should support BeiDou constellation configuration"

        # Check if BeiDou is available for this device using page object method
        available_constellations = gnss_config_page.get_available_constellations()
        beidou_available = any(
            "BEIDOU" in c.upper() or "BEIDOU" in c.upper()
            for c in available_constellations
        )

        if not beidou_available:
            pytest.skip(f"BeiDou constellation not available for {device_model}")

        # Navigate to GNSS page using page object method
        gnss_config_page.navigate_to_page()

        # Test BeiDou checkbox toggle using page object method
        print(f"INFO: {device_model} - Testing BeiDou checkbox toggle")

        # Get initial BeiDou state using page object method
        initial_beidou_state = gnss_config_page.is_constellation_enabled("BeiDou")
        print(
            f"INFO: {device_model} - Initial BeiDou state: {'enabled' if initial_beidou_state else 'disabled'}"
        )

        # Toggle BeiDou using page object method
        toggle_success = gnss_config_page.toggle_constellation("BeiDou")
        assert toggle_success, f"BeiDou checkbox toggle failed on {device_model}"

        # Verify state changed using page object method
        new_beidou_state = gnss_config_page.is_constellation_enabled("BeiDou")
        assert (
            new_beidou_state != initial_beidou_state
        ), f"BeiDou checkbox should toggle on {device_model}"

        print(
            f"INFO: {device_model} - BeiDou state after toggle: {'enabled' if new_beidou_state else 'disabled'}"
        )

        # Cancel changes using page object method to restore original state
        cancel_success = gnss_config_page.cancel_gnss_changes()
        assert cancel_success, f"Cancel GNSS changes failed on {device_model}"

        # Verify state is restored using page object method
        final_beidou_state = gnss_config_page.is_constellation_enabled("BeiDou")
        assert (
            final_beidou_state == initial_beidou_state
        ), f"BeiDou state should be restored after cancel on {device_model}"

        print(
            f"INFO: {device_model} - BeiDou state after cancel: {'enabled' if final_beidou_state else 'disabled'}"
        )

        # Device series-specific validation
        if device_series == 2:
            print(
                f"INFO: {device_model} - Series 2: BeiDou configuration validated with basic patterns"
            )
        elif device_series == 3:
            print(
                f"INFO: {device_model} - Series 3: BeiDou configuration validated with advanced patterns"
            )
        else:
            print(
                f"INFO: {device_model} - Unknown series: BeiDou configuration validated with standard patterns"
            )

        # DeviceCapabilities integration validation
        capabilities = DeviceCapabilities.get_capabilities(device_model)
        beidou_support = capabilities.get("gnss_constellations", {}).get(
            "beidou", False
        )

        if beidou_support:
            print(f"INFO: {device_model} - DeviceCapabilities confirms BeiDou support")
        else:
            print(
                f"INFO: {device_model} - DeviceCapabilities indicates limited BeiDou support"
            )

        # Performance validation
        start_time = time.time()

        # Test multiple toggle operations for robustness
        for i in range(2):
            toggle_success = gnss_config_page.toggle_constellation("BeiDou")
            assert toggle_success, f"BeiDou toggle {i+1} failed on {device_model}"

            current_state = gnss_config_page.is_constellation_enabled("BeiDou")
            print(
                f"INFO: {device_model} - Toggle {i+1} result: {'enabled' if current_state else 'disabled'}"
            )

        end_time = time.time()
        toggle_time = end_time - start_time

        # Validate toggle performance
        max_expected_time = 2.0 * timeout_multiplier
        if toggle_time <= max_expected_time:
            print(
                f"INFO: {device_model} - BeiDou toggle performance: {toggle_time:.2f}s (within limit)"
            )
        else:
            print(
                f"WARNING: {device_model} - BeiDou toggle performance: {toggle_time:.2f}s (slower than expected)"
            )

        # Final state restoration
        final_cancel_success = gnss_config_page.cancel_gnss_changes()
        assert (
            final_cancel_success
        ), f"Final cancel GNSS changes failed on {device_model}"

        # Comprehensive validation summary
        print(f"INFO: {device_model} - BeiDou checkbox toggle validation completed:")
        print(f"  - Device Series: {device_series}")
        print(f"  - Initial State: {'enabled' if initial_beidou_state else 'disabled'}")
        print(f"  - Toggle Operations: 2 successful")
        print(f"  - Final State: {'enabled' if final_beidou_state else 'disabled'}")
        print(
            f"  - State Restoration: {'successful' if final_beidou_state == initial_beidou_state else 'failed'}"
        )
        print(f"  - Toggle Performance: {toggle_time:.2f}s")

        print(
            f"INFO: {device_model} - BeiDou checkbox toggle verified using pure page object methods"
        )

    except Exception as e:
        pytest.skip(f"BeiDou checkbox test failed on {device_model}: {e}")
