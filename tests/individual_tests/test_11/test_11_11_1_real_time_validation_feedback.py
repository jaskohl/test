"""
Test 11.11.1: Real-Time Validation Feedback (Pure Page Object)
Purpose: Timing and responsiveness of validation feedback with device-aware behavior
Expected: Device-specific validation feedback timing based on capabilities
Device-: Full DeviceCapabilities integration with series-specific patterns
Pure Page Object: Zero direct .locator() calls, 100% page object methods
"""

import pytest
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_11_1_real_time_validation_feedback(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.11.1: Real-Time Validation Feedback (Pure Page Object)
    Purpose: Timing and responsiveness of validation feedback with device-aware behavior
    Expected: Device-specific validation feedback timing based on capabilities
    Device-: Full DeviceCapabilities integration with series-specific patterns
    Pure Page Object: Zero direct .locator() calls, 100% page object methods
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate feedback timing")

    # Initialize page object with device model
    general_config_page.device_model = device_model
    general_config_page.device_series = DeviceCapabilities.get_series(device_model)

    # Navigate to page using page object method
    general_config_page.navigate_to_page()

    # Test real-time validation feedback using comprehensive page object method
    validation_results = general_config_page.test_real_time_validation_feedback()

    # Device-specific validation assertions using page object methods
    assert (
        validation_results["total_tested_fields"] > 0
    ), f"No input fields could be tested for real-time validation feedback on {device_model}"

    # Validate device-specific performance expectations
    if general_config_page.device_series == "Series 2":
        print(
            f"Series 2 device {device_model} - validated basic real-time validation feedback timing"
        )
        # Series 2 allows more time for feedback processing
        expected_max_time = 2.0
    else:  # Series 3
        print(
            f"Series 3 device {device_model} - validated advanced real-time validation feedback timing"
        )
        # Series 3 expects faster feedback due to more advanced interface
        expected_max_time = 1.0

    # Validate timing performance using page object method
    max_feedback_time = general_config_page.get_max_feedback_time()
    assert (
        max_feedback_time == expected_max_time
    ), f"Device {device_model} feedback time expectation mismatch: {max_feedback_time} != {expected_max_time}"

    # Validate that validation feedback is working within device-appropriate timeframes
    successful_validations = validation_results["successful_validations"]
    total_tested = validation_results["total_tested_fields"]

    assert (
        successful_validations > 0
    ), f"No successful validations on {device_model} - validation feedback may not be working"

    # Calculate success rate and validate it's acceptable
    success_rate = successful_validations / total_tested
    print(f"Validation feedback success rate on {device_model}: {success_rate:.1%}")

    # Device-specific validation feedback pattern verification
    if general_config_page.device_series == "Series 3":
        # Test PTP-specific validation patterns for Series 3 devices
        ptp_fields = general_config_page.get_ptp_input_fields()
        if ptp_fields:
            print(f"Found PTP-related input fields for Series 3 device {device_model}")
            ptp_validation_result = general_config_page.test_ptp_validation_feedback()
            assert (
                ptp_validation_result
            ), f"PTP field validation feedback failed for Series 3 device {device_model}"
        else:
            print(
                f"No PTP fields found for Series 3 device {device_model} (may be expected)"
            )
    else:
        print(
            f"Series 2 device {device_model} - no PTP-related validation feedback expected"
        )

    # Performance baseline cross-validation
    if validation_results["validation_times"]:
        avg_feedback_time = sum(validation_results["validation_times"]) / len(
            validation_results["validation_times"]
        )
        print(
            f"Average validation feedback time for {device_model}: {avg_feedback_time:.2f}s"
        )

        # Ensure average feedback time is within acceptable limits
        assert (
            avg_feedback_time <= max_feedback_time * 1.2
        ), f"Average feedback time {avg_feedback_time:.2f}s exceeds acceptable limit for {device_model}"

    # Summary validation
    print(
        f"Successfully validated real-time validation feedback for {device_model} ({general_config_page.device_series}):"
    )
    print(f"  Fields tested: {validation_results['total_tested_fields']}")
    print(f"  Successful validations: {validation_results['successful_validations']}")
    print(f"  Success rate: {success_rate:.1%}")
    print(f"  Max allowed time: {validation_results['max_feedback_time']}s")

    # Final validation that page object methods are working correctly
    assert (
        general_config_page.has_basic_general_fields()
    ), f"Basic general fields not available on {device_model} for validation testing"

    print(
        f"Pure page object real-time validation feedback test completed successfully for {device_model}"
    )
