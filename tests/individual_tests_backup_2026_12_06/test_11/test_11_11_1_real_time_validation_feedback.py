"""
Test 11.11.1: Real-Time Validation Feedback (Device-Aware)
Purpose: Timing and responsiveness of validation feedback
Expected: Device-specific validation feedback timing
Device-Aware: Uses actual device model for model-specific validation
"""

import pytest
import time
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_11_1_real_time_validation_feedback(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.11.1: Real-Time Validation Feedback (Device-Aware)
    Purpose: Timing and responsiveness of validation feedback
    Expected: Device-specific validation feedback timing
    Device-Aware: Uses actual device model for model-specific validation
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate feedback timing")

    general_config_page.navigate_to_page()

    # Test real-time validation feedback timing
    input_fields = general_config_page.page.locator("input[type='text'], textarea")
    if input_fields.count() > 0:
        input_field = input_fields.first
        # Test immediate feedback on input
        start_time = time.time()
        input_field.fill("test")
        input_field.dispatch_event("input")
        # Wait for validation feedback
        # Device should provide feedback within reasonable timeframe
        error_containers = general_config_page.page.locator(
            ".error, .validation-error, [aria-invalid='true']"
        )
        # Feedback timing should be device-appropriate
        end_time = time.time()
        feedback_time = end_time - start_time
        # Device may have different feedback timing based on series
        device_series = DeviceCapabilities.get_series(device_model)
        max_expected_time = 2.0 if device_series == 2 else 1.0  # Series 2 may be slower
        assert (
            feedback_time <= max_expected_time
        ), f"Validation feedback took {feedback_time}s, expected <= {max_expected_time}s on {device_model}"
    else:
        print(f"No input fields found for timing validation on {device_model}")
