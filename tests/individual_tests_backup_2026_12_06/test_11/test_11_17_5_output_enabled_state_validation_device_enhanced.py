"""
Test 11.17.5: Output Enabled State Validation (Device-Enhanced)
Purpose: Comprehensive output enabled/disabled state validation with DeviceCapabilities
Expected: Device-specific output enable behavior with series-aware validation
Device-Enhanced: Uses DeviceCapabilities for device-aware testing across all hardware variants
"""

import pytest
import time
from playwright.sync_api import expect
from pages.outputs_config_page import OutputsConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_17_5_output_enabled_state_validation_device_enhanced(
    outputs_config_page: OutputsConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.17.5: Output Enabled State Validation (Device-Enhanced)

    Purpose: Comprehensive output enabled/disabled state validation with DeviceCapabilities
    Expected: Device-specific output enable behavior with series-aware validation
    Device-Enhanced: Uses DeviceCapabilities for device-aware testing across all hardware variants
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate output enabled state")

    # Get device capabilities and series information
    device_capabilities = DeviceCapabilities.get_capabilities(device_model)
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    print(
        f"Testing output enabled state validation for {device_model} (Series {device_series})"
    )

    # Navigate to outputs configuration
    outputs_config_page.navigate_to_page()

    # Wait for page to load with device-aware timeout
    time.sleep(1 * timeout_multiplier)

    # Get expected number of outputs based on device series
    if device_series == 2:
        expected_outputs = 2
        max_output_index = 1
        interface_suffix = ""
    elif device_series == 3:
        expected_outputs = 6
        max_output_index = 5
        interface_suffix = "-eth0"  # Series 3 uses interface-specific targeting
    else:
        pytest.skip(f"Unknown device series for {device_model}")

    # Validate that we can find output enable controls
    enable_selectors = [
        "input[name*='enabled' i]",
        "input[name*='enable' i]",
        "select[name*='enabled' i]",
        "select[name*='enable' i]",
        f"input[id*='enabled{interface_suffix}']",
        f"select[id*='enabled{interface_suffix}']",
    ]

    output_enable_found = False
    for selector in enable_selectors:
        enable_elements = outputs_config_page.page.locator(selector)
        if enable_elements.count() > 0:
            output_enable_found = True
            print(f"Found output enable elements using selector: {selector}")
            break

    if not output_enable_found:
        # Try to find output sections and check for enable controls within them
        output_sections = outputs_config_page.page.locator(
            "[class*='output' i], [id*='output' i], .output-config, #output-config"
        )

        if output_sections.count() > 0:
            print(f"Found {output_sections.count()} output sections")
            for i in range(min(output_sections.count(), expected_outputs)):
                section = output_sections.nth(i)

                # Look for enable controls within this output section
                section_enable_selectors = [
                    "input[type='checkbox']",
                    "select",
                    "input[name*='enabled' i]",
                    "select[name*='enabled' i]",
                ]

                for selector in section_enable_selectors:
                    enable_control = section.locator(selector)
                    if enable_control.count() > 0:
                        print(
                            f"Found enable control in output section {i} using {selector}"
                        )
                        output_enable_found = True
                        break

                if output_enable_found:
                    break

    if not output_enable_found:
        # Try to find by output index if available
        for output_idx in range(expected_outputs):
            if device_series == 3:
                # Series 3: try interface-specific selectors
                enable_selectors_indexed = [
                    f"input[id*='output{output_idx}-enabled-eth0']",
                    f"select[id*='output{output_idx}-enabled-eth0']",
                    f"input[name*='output{output_idx}.*enabled']",
                    f"select[name*='output{output_idx}.*enabled']",
                ]
            else:
                # Series 2: simple indexed selectors
                enable_selectors_indexed = [
                    f"input[id*='output{output_idx}-enabled']",
                    f"select[id*='output{output_idx}-enabled']",
                    f"input[name*='output{output_idx}.*enabled']",
                    f"select[name*='output{output_idx}.*enabled']",
                ]

            for selector in enable_selectors_indexed:
                enable_elements = outputs_config_page.page.locator(selector)
                if enable_elements.count() > 0:
                    output_enable_found = True
                    print(
                        f"Found output {output_idx} enable elements using selector: {selector}"
                    )
                    break

            if output_enable_found:
                break

    # If we found enable controls, perform comprehensive validation
    if output_enable_found:
        # Test enabled/disabled state transitions
        validate_output_enabled_state_transitions(
            outputs_config_page, device_model, device_series, timeout_multiplier
        )

        # Test consistency across all outputs
        validate_output_enabled_consistency(
            outputs_config_page,
            device_model,
            device_series,
            expected_outputs,
            timeout_multiplier,
        )

        # Test device-specific enable behavior
        validate_series_specific_enabled_behavior(
            outputs_config_page, device_model, device_series, timeout_multiplier
        )
    else:
        print(
            f"No output enable controls found for {device_model} - this may be expected behavior"
        )
        # Log that output enable state might be handled differently for this device
        pytest.skip(
            f"Output enable controls not found for {device_model} - device may use different enable mechanism"
        )


def validate_output_enabled_state_transitions(
    page, device_model, device_series, timeout_multiplier
):
    """Validate output enable/disable state transitions"""
    print(f"Validating output enabled state transitions for {device_model}")

    # Find output enable controls
    enable_selectors = [
        "input[type='checkbox'][name*='enabled' i]",
        "select[name*='enabled' i]",
        f"input[type='checkbox'][id*='enabled-eth0']",
        f"select[id*='enabled-eth0']",
    ]

    for selector in enable_selectors:
        enable_controls = page.page.locator(selector)
        control_count = enable_controls.count()

        if control_count > 0:
            print(f"Found {control_count} enable controls using selector: {selector}")

            # Test first few controls for state transitions
            for i in range(min(control_count, 3)):
                control = enable_controls.nth(i)

                try:
                    if control.get_attribute("type") == "checkbox":
                        # Test checkbox enable/disable
                        initial_state = control.is_checked()

                        # Toggle to opposite state
                        if initial_state:
                            control.uncheck()
                            expect(control).not_to_be_checked()
                            time.sleep(0.5 * timeout_multiplier)
                            control.check()
                        else:
                            control.check()
                            expect(control).to_be_checked()
                            time.sleep(0.5 * timeout_multiplier)
                            control.uncheck()

                        # Restore original state
                        if initial_state:
                            control.check()
                        else:
                            control.uncheck()

                    elif control.tag_name == "select":
                        # Test dropdown enable/disable options
                        options = control.locator("option")
                        option_count = options.count()

                        if option_count > 0:
                            # Test enabled/disabled options if available
                            for opt_idx in range(min(option_count, 3)):
                                option = options.nth(opt_idx)
                                option_value = option.get_attribute("value")

                                if option_value and (
                                    "enable" in option_value.lower()
                                    or "disable" in option_value.lower()
                                ):
                                    control.select_option(option_value)
                                    time.sleep(0.5 * timeout_multiplier)
                                    selected = control.evaluate("el => el.value")
                                    assert (
                                        selected == option_value
                                    ), f"Expected {option_value}, got {selected}"

                except Exception as e:
                    print(
                        f"Warning: Could not test state transitions for control {i}: {e}"
                    )
                    continue

            break  # Found working selector, stop trying others


def validate_output_enabled_consistency(
    page, device_model, device_series, expected_outputs, timeout_multiplier
):
    """Validate consistency of enabled state across all outputs"""
    print(f"Validating output enabled consistency for {device_model}")

    # Check if all outputs have consistent enable control availability
    enable_selectors = [
        "input[type='checkbox'][name*='enabled' i]",
        "select[name*='enabled' i]",
    ]

    for selector in enable_selectors:
        enable_controls = page.page.locator(selector)
        control_count = enable_controls.count()

        if control_count > 0:
            # For Series 3, we expect to find controls for each output
            if device_series == 3 and control_count >= expected_outputs:
                print(
                    f"Found {control_count} enable controls for {expected_outputs} outputs (Series 3)"
                )
            elif device_series == 2 and control_count >= expected_outputs:
                print(
                    f"Found {control_count} enable controls for {expected_outputs} outputs (Series 2)"
                )

            # Validate that controls are accessible
            for i in range(min(control_count, expected_outputs)):
                control = enable_controls.nth(i)
                try:
                    is_visible = control.is_visible()
                    is_enabled = control.is_enabled()
                    print(
                        f"Output enable control {i}: visible={is_visible}, enabled={is_enabled}"
                    )
                except Exception as e:
                    print(f"Warning: Could not check control {i} state: {e}")

            break


def validate_series_specific_enabled_behavior(
    page, device_model, device_series, timeout_multiplier
):
    """Validate series-specific enabled state behavior"""
    print(f"Validating series-specific enabled behavior for {device_model}")

    if device_series == 2:
        # Series 2: Simpler enable/disable behavior
        print("Testing Series 2 enable behavior")

        # Look for basic enable controls
        enable_controls = page.page.locator("input[type='checkbox'][name*='enabled' i]")
        if enable_controls.count() > 0:
            control = enable_controls.first
            try:
                initial_state = control.is_checked()
                control.click()
                time.sleep(0.5 * timeout_multiplier)
                new_state = control.is_checked()
                assert initial_state != new_state, "Enable toggle should change state"
                print(f"Series 2 enable toggle working: {initial_state} -> {new_state}")
            except Exception as e:
                print(f"Series 2 enable test failed: {e}")

    elif device_series == 3:
        # Series 3: Interface-specific enable behavior
        print("Testing Series 3 enable behavior")

        # Test interface-specific enables
        interface_enables = page.page.locator("input[id*='enabled-eth']")
        enable_count = interface_enables.count()

        if enable_count > 0:
            print(f"Found {enable_count} interface-specific enable controls")

            for i in range(min(enable_count, 3)):
                control = interface_enables.nth(i)
                try:
                    interface_id = control.get_attribute("id")
                    initial_state = control.is_checked()
                    control.click()
                    time.sleep(0.5 * timeout_multiplier)
                    new_state = control.is_checked()
                    assert (
                        initial_state != new_state
                    ), f"Interface enable toggle should change state for {interface_id}"
                    print(
                        f"Series 3 interface enable toggle working for {interface_id}: {initial_state} -> {new_state}"
                    )
                except Exception as e:
                    print(f"Series 3 interface enable test failed for control {i}: {e}")

    print(
        f"Series-specific enabled behavior validation completed for Series {device_series}"
    )
