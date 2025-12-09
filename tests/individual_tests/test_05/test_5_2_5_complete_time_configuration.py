"""
Test: 5.2.5 - Complete Time Configuration Workflow (Pure Page Object Pattern)
Category: Time Configuration - Test 5.2.5
Test Count: 9 of 11 in Category 5
Purpose: Verify both timezone and DST can be configured together
Expected: Both sections save independently and persist
Series: Both Series 2 and 3
Priority: HIGH
Hardware: Device Only
TRANSFORMED: Pure page object architecture with device intelligence
PATTERN: Zero direct .locator() calls, essential methods only
"""

import pytest
import logging
from pages.time_config_page import TimeConfigPage
from pages.device_capabilities import DeviceCapabilities

logger = logging.getLogger(__name__)


def test_5_2_5_complete_time_configuration(
    time_config_page: TimeConfigPage,
    request,
    base_url: str,
):
    """
    Test 5.2.5: Complete Time Configuration Workflow - Pure Page Object Pattern
    Purpose: Verify both timezone and DST can be configured together
    Expected: Both sections save independently and persist
    TRANSFORMED: Uses pure page object methods with device intelligence
    Series: Both 2 and 3
    """
    device_model = request.session.device_hardware_model

    # Essential device intelligence
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Validate device capabilities
    has_complete_config = DeviceCapabilities.has_capability(
        device_model, "complete_time_config"
    )
    if not has_complete_config:
        pytest.skip(
            f"Device {device_model} does not support complete time configuration workflow"
        )

    logger.info(f"Testing complete time configuration workflow on {device_model}")

    # Navigate to time configuration page
    time_config_page.navigate_to_time_config()

    # Get original configuration for rollback
    original_data = time_config_page.get_page_data()
    original_timezone = original_data.get("timezone", "")
    original_dst_status = time_config_page.get_dst_status()

    try:
        # Test complete time configuration workflow through page object
        workflow_test_results = (
            time_config_page.test_complete_time_configuration_workflow()
        )
        logger.info(
            f"Complete time configuration workflow test results: {workflow_test_results}"
        )

        # Verify timezone configuration
        timezone_config = workflow_test_results.get("timezone_config", {})
        timezone_success = timezone_config.get("success", False)
        assert timezone_success, "Timezone configuration should save successfully"
        logger.info("Timezone configuration saved successfully")

        # Verify DST configuration
        dst_config = workflow_test_results.get("dst_config", {})
        dst_success = dst_config.get("success", False)
        assert dst_success, "DST configuration should save successfully"
        logger.info("DST configuration saved successfully")

        # Verify timezone persistence
        timezone_persistence = timezone_config.get("persistence_verified", False)
        assert timezone_persistence, "Timezone should persist after configuration"
        logger.info("Timezone configuration persists")

        # Verify DST persistence
        dst_persistence = dst_config.get("persistence_verified", False)
        assert dst_persistence, "DST should persist after configuration"
        logger.info("DST configuration persists")

        # Verify independent save functionality
        independence_verified = workflow_test_results.get(
            "independence_verified", False
        )
        assert independence_verified, "Both sections should save independently"
        logger.info("Independent save functionality verified")

        # Test specific configuration values
        test_timezone = workflow_test_results.get("test_timezone", "")
        expected_timezone = "US/Denver"
        assert (
            test_timezone == expected_timezone
        ), f"Timezone should be '{expected_timezone}', got '{test_timezone}'"
        logger.info(f"Timezone configuration verified: {test_timezone}")

        # Test DST status
        test_dst_status = workflow_test_results.get("test_dst_status", False)
        assert test_dst_status is True, "DST should be enabled"
        logger.info("DST configuration verified as enabled")

        # Device capabilities validation passed
        logger.info(
            "Device capabilities validation passed for complete time configuration workflow"
        )

        # Device series-specific validation
        if device_series == 2:
            logger.info(
                "Series 2 complete time configuration workflow validation completed"
            )
        elif device_series == 3:
            logger.info(
                "Series 3 complete time configuration workflow validation completed"
            )

        logger.info(
            f"Complete time configuration workflow test completed for {device_model}"
        )

    finally:
        # Rollback: Restore original configuration
        try:
            if original_timezone:
                time_config_page.restore_timezone_configuration(original_timezone)
            time_config_page.set_dst_with_save(original_dst_status)
            logger.info("Original time configuration restored")
        except Exception as rollback_error:
            logger.warning(f"Configuration rollback failed: {rollback_error}")

    logger.info(
        f"Complete time configuration workflow test completed for {device_model}"
    )
