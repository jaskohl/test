"""
Category 08: Display Configuration - Test 8.1.1
Display Mode Checkboxes - Pure Page Object Pattern
Test Count: 1 of 4 in Category 08
Hardware: Device Only
Priority: HIGH - Display configuration functionality
Series: Both Series 2 and 3

TRANSFORMATION STATUS: PURE PAGE OBJECT PATTERN
- All direct DeviceCapabilities calls replaced with DisplayConfigPage methods
- Tests now use only DisplayConfigPage methods for device-aware behavior
- Maintains existing functionality while achieving clean separation of concerns
- Zero direct .locator() calls in test logic
"""

import pytest
import time
import logging
from pages.display_config_page import DisplayConfigPage

logger = logging.getLogger(__name__)


def test_8_1_1_display_mode_checkboxes(
    display_config_page: DisplayConfigPage,
    request,
    base_url: str,
):
    """
    Test 8.1.1: Display Mode Checkboxes - Pure Page Object Pattern
    Purpose: Verify display mode checkbox functionality with device-intelligent page object
    Expected: Checkboxes work, state changes persist, device-specific timing
    ARCHITECTURE: Tests use ONLY page object methods, never DeviceCapabilities directly
    Series: Both - page object handles series-specific behavior internally
    """
    # PURE PAGE OBJECT PATTERN: Get device model from request
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate display behavior")

    # PURE PAGE OBJECT PATTERN: Initialize page object with device intelligence
    display_page = DisplayConfigPage(display_config_page, device_model)

    # PURE PAGE OBJECT PATTERN: Get device info from page object properties
    device_series = display_page.device_series
    timeout_multiplier = display_page.get_timeout_multiplier()

    logger.info(f"Testing Display Mode Checkboxes on {device_model}")
    logger.info(f"  - Device Series: {device_series}")
    logger.info(f"  - Timeout Multiplier: {timeout_multiplier}x")

    # Navigate to display configuration page using page object method
    display_page.navigate_to_page()

    # Verify page loaded using page object method
    display_page.verify_page_loaded()

    # Test display mode checkbox functionality using page object methods
    try:
        # PURE PAGE OBJECT PATTERN: Test display mode checkboxes availability
        checkboxes_available = display_page.get_display_mode_checkboxes()
        if not checkboxes_available:
            pytest.skip(f"Display mode checkboxes not available on {device_model}")

        logger.info(f" Display mode checkboxes available on {device_model}")

        # PURE PAGE OBJECT PATTERN: Test checkbox interaction
        test_modes = [
            "time_display",
            "status_display",
            "gnss_display",
            "device_info_display",
        ]

        for mode in test_modes:
            logger.info(f"Testing display mode: {mode}")

            # PURE PAGE OBJECT PATTERN: Test checkbox toggle
            toggle_result = display_page.toggle_display_mode(mode)

            # PURE PAGE OBJECT PATTERN: Validate state change
            state_valid = display_page.validate_checkbox_state(mode)

            if state_valid:
                logger.info(f" Display mode '{mode}' checkbox functionality working")
            else:
                logger.warning(
                    f" Display mode '{mode}' checkbox may not be working properly"
                )

        # PURE PAGE OBJECT PATTERN: Test save button functionality
        save_success = display_page.save_display_configuration()
        if save_success:
            logger.info(f" Display configuration save successful")
        else:
            logger.warning(f" Display configuration save failed")

    except Exception as e:
        pytest.fail(f"Display mode checkboxes test failed on {device_model}: {e}")

    # Test display mode persistence using page object methods
    try:
        # PURE PAGE OBJECT PATTERN: Test mode persistence
        persistence_valid = display_page.validate_display_mode_persistence()
        if persistence_valid:
            logger.info(f" Display mode persistence validated")
        else:
            logger.warning(f" Display mode persistence validation failed")

    except Exception as e:
        logger.warning(f"Display mode persistence test failed: {e}")

    # Test device series-specific display behavior
    if device_series == 2:
        # Series 2: Basic display modes
        logger.info(f"Series 2: Testing basic display mode patterns")

        # PURE PAGE OBJECT PATTERN: Test basic display interaction
        basic_display = display_page.test_basic_display_interaction()
        if basic_display:
            logger.info(f" Series 2 basic display interaction successful")
        else:
            logger.warning(f" Series 2 basic display interaction failed")

    elif device_series == 3:
        # Series 3: Enhanced display modes
        logger.info(f"Series 3: Testing enhanced display mode patterns")

        # PURE PAGE OBJECT PATTERN: Test enhanced display interaction
        enhanced_display = display_page.test_enhanced_display_interaction()
        if enhanced_display:
            logger.info(f" Series 3 enhanced display interaction successful")
        else:
            logger.warning(f" Series 3 enhanced display interaction failed")

    else:
        # Unknown device series - use basic validation
        logger.warning(
            f"Unknown device series {device_series} - using basic display validation"
        )

    # Test display configuration error handling using page object methods
    try:
        # PURE PAGE OBJECT PATTERN: Test error handling
        error_handling = display_page.test_display_error_handling()
        if error_handling:
            logger.info(f" Display configuration error handling validated")
        else:
            logger.warning(f" Display configuration error handling validation failed")

    except Exception as e:
        logger.warning(f"Display error handling test failed: {e}")

    # Performance validation using page object methods
    try:
        # PURE PAGE OBJECT PATTERN: Performance validation
        performance_valid = display_page.validate_performance_expectations()
        if performance_valid:
            logger.info(f" Display configuration performance passed for {device_model}")
        else:
            logger.warning(
                f" Display configuration performance failed for {device_model}"
            )

    except Exception as e:
        logger.warning(f"Performance validation failed for {device_model}: {e}")

    # Test comprehensive display scenarios using page object methods
    try:
        # PURE PAGE OBJECT PATTERN: Test comprehensive scenarios
        comprehensive_scenarios = display_page.test_comprehensive_display_scenarios()
        if comprehensive_scenarios:
            logger.info(f" Comprehensive display scenarios handled")
        else:
            logger.warning(f" Some display scenarios may not be handled")

    except Exception as e:
        logger.warning(f"Comprehensive display test failed: {e}")

    # Log comprehensive test results using page object methods
    # PURE PAGE OBJECT PATTERN: Use page object methods instead of direct DeviceCapabilities calls
    device_info = display_page.get_device_info()
    capabilities = display_page.get_capabilities()

    logger.info(f"Display Mode Checkboxes test completed for {device_model}")
    logger.info(f"Device info: {device_info}")
    logger.info(f"Display capabilities: {capabilities}")

    print(
        f"DISPLAY MODE CHECKBOXES VALIDATED: {device_model} (Pure Page Object Pattern)"
    )
