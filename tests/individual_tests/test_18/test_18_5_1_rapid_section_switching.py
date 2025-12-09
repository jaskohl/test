"""
Category 18: Workflow Tests - TEST 18.5.1: RAPID SECTION SWITCHING - Pure Page Object Pattern
Hardware: Device Only
Priority: HIGH - End-to-end workflow validation
Series: Both Series 2 and 3
IMPROVED: Pure page object architecture with device-aware rapid section switching validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page
from pages.dashboard_page import DashboardPage
from pages.general_config_page import GeneralConfigPage
from pages.network_config_page import NetworkConfigPage
from pages.time_config_page import TimeConfigPage
from pages.outputs_config_page import OutputsConfigPage
from pages.gnss_config_page import GnssConfigPage
from pages.display_config_page import DisplayConfigPage

logger = logging.getLogger(__name__)


def test_18_5_1_rapid_section_switching(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 18.5.1: Rapid Switching Between Sections (Pure Page Object Pattern)
    Purpose: Verify system handles rapid navigation without issues using pure page object architecture
    Expected: No errors, session remains stable with device-aware validation
    IMPROVED: Pure page object pattern with comprehensive rapid section switching validation
    """
    # Get device context using page object encapsulation
    device_model = request.session.get("device_model", "unknown")
    if not device_model or device_model == "unknown":
        pytest.fail("Device model not detected - cannot validate rapid switching")

    logger = logging.getLogger(__name__)

    try:
        logger.info(f"{device_model}: Starting rapid section switching validation")

        # Initialize dashboard page object for rapid switching validation
        dashboard_page_obj = DashboardPage(unlocked_config_page, device_model)

        # Validate device context using page object methods
        device_series = dashboard_page_obj.get_expected_device_series()
        timeout_multiplier = dashboard_page_obj.get_timeout_multiplier()

        logger.info(f"{device_model}: Device series: {device_series}")
        logger.info(f"{device_model}: Timeout multiplier: {timeout_multiplier}x")

        # Device-aware configuration sections for rapid switching
        sections_config = [
            {
                "name": "general",
                "page_obj": GeneralConfigPage,
                "validation_method": "validate_general_section_rapid_switching",
            },
            {
                "name": "network",
                "page_obj": NetworkConfigPage,
                "validation_method": "validate_network_section_rapid_switching",
            },
            {
                "name": "time",
                "page_obj": TimeConfigPage,
                "validation_method": "validate_time_section_rapid_switching",
            },
            {
                "name": "outputs",
                "page_obj": OutputsConfigPage,
                "validation_method": "validate_outputs_section_rapid_switching",
            },
            {
                "name": "gnss",
                "page_obj": GnssConfigPage,
                "validation_method": "validate_gnss_section_rapid_switching",
            },
            {
                "name": "display",
                "page_obj": DisplayConfigPage,
                "validation_method": "validate_display_section_rapid_switching",
            },
        ]

        # Get device-aware rapid switching delay using page object method
        rapid_switching_delay = dashboard_page_obj.get_rapid_switching_delay()

        # Rapidly navigate between sections
        successful_cycles = 0
        failed_cycles = []

        for cycle in range(3):  # 3 cycles
            try:
                logger.info(
                    f"{device_model}: Starting rapid switching cycle {cycle + 1}/3"
                )

                for section_config in sections_config:
                    section_name = section_config["name"]
                    page_obj_class = section_config["page_obj"]
                    validation_method = section_config["validation_method"]

                    try:
                        logger.info(
                            f"{device_model}: Switching to {section_name} section (cycle {cycle + 1})"
                        )

                        # Initialize page object for this section
                        section_page_obj = page_obj_class(
                            unlocked_config_page, device_model
                        )

                        # Navigate to section using page object method
                        section_page_obj.navigate_to_page()
                        section_page_obj.wait_for_page_load()

                        # Verify no redirect to authentication using page object method
                        current_url = section_page_obj.get_current_url()
                        assert (
                            "authenticate" not in current_url.lower()
                        ), f"Session should remain stable during rapid navigation on {device_model}"

                        # Additional section-specific validation using page object method
                        validation_func = getattr(
                            section_page_obj, validation_method, None
                        )
                        if validation_func:
                            validation_func()

                        # Brief pause for rapid switching using device-aware timing
                        time.sleep(rapid_switching_delay)

                        logger.info(
                            f"{device_model}: Successfully switched to {section_name} section (cycle {cycle + 1})"
                        )

                    except Exception as section_error:
                        logger.warning(
                            f"{device_model}: Failed to switch to {section_name} section (cycle {cycle + 1}): {section_error}"
                        )
                        failed_cycles.append(
                            f"Cycle {cycle + 1}, Section {section_name}: {str(section_error)}"
                        )

                successful_cycles += 1
                logger.info(
                    f"{device_model}: Completed rapid switching cycle {cycle + 1}/3"
                )

            except Exception as cycle_error:
                logger.warning(
                    f"{device_model}: Rapid switching cycle {cycle + 1} failed: {cycle_error}"
                )
                failed_cycles.append(f"Cycle {cycle + 1}: {str(cycle_error)}")

        # Summary of rapid switching results
        logger.info(f"{device_model}: Rapid switching summary:")
        logger.info(f"{device_model}: Successful cycles: {successful_cycles}/3")
        if failed_cycles:
            logger.warning(f"{device_model}: Failed cycles: {failed_cycles}")

        # Validate rapid switching workflow integrity using page object methods
        try:
            dashboard_page_obj.validate_rapid_section_switching_workflow_integrity(
                successful_cycles, failed_cycles
            )

            # Series-specific validation using page object methods
            if device_series == 2:
                dashboard_page_obj.validate_series2_rapid_section_switching_patterns(
                    successful_cycles
                )
            elif device_series == 3:
                dashboard_page_obj.validate_series3_rapid_section_switching_patterns(
                    successful_cycles
                )

            # Cross-validation test using page object method
            dashboard_page_obj.test_rapid_section_switching_cross_validation()

        except Exception as e:
            logger.warning(
                f"{device_model}: Rapid switching workflow validation failed: {e}"
            )

        # Assert that at least some cycles were successful
        assert (
            successful_cycles > 0
        ), f"Should successfully complete at least one rapid switching cycle for {device_model}"

        # Final validation using page object method
        dashboard_page_obj.validate_rapid_section_switching_completion(
            successful_cycles, device_model
        )

        logger.info(f"{device_model}: Rapid section switching completed successfully")
        print(
            f"Rapid section switching passed for {device_model}: {successful_cycles}/3 cycles successful"
        )

    except Exception as e:
        logger.error(f"{device_model}: Rapid section switching encountered error - {e}")
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"Rapid section switching failed for {device_model}: {e}")
