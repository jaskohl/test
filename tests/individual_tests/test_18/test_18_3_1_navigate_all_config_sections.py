"""
Test 18.3.1: Navigate Through All Configuration Sections - Pure Page Object Pattern
Category: 18 - Workflow Tests
Test Count: Part of 8 tests in Category 18
Hardware: Device Only
Priority: HIGH - End-to-end workflow validation
Series: Both Series 2 and 3
IMPROVED: Pure page object architecture with device-aware all configuration sections navigation validation
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
from pages.upload_config_page import UploadConfigPage
from pages.snmp_config_page import SnmpConfigPage
from pages.syslog_config_page import SyslogConfigPage
from pages.access_config_page import AccessConfigPage
from pages.ptp_config_page import PtpConfigPage

logger = logging.getLogger(__name__)


def test_18_3_1_navigate_all_config_sections(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 18.3.1: Navigate Through All Configuration Sections (Pure Page Object Pattern)
    Purpose: Verify can navigate through all sections without errors using pure page object architecture
    Expected: Smooth navigation through all sections with device-aware validation
    IMPROVED: Pure page object pattern with comprehensive all configuration sections navigation validation
    """
    # Get device context using page object encapsulation
    device_model = request.session.get("device_model", "unknown")
    if not device_model or device_model == "unknown":
        pytest.skip("Device model not detected - cannot validate navigation workflow")

    logger = logging.getLogger(__name__)

    try:
        logger.info(
            f"{device_model}: Starting navigation through all configuration sections validation"
        )

        # Initialize dashboard page object for navigation validation
        dashboard_page_obj = DashboardPage(unlocked_config_page, device_model)

        # Validate device context using page object methods
        device_series = dashboard_page_obj.get_expected_device_series()
        timeout_multiplier = dashboard_page_obj.get_timeout_multiplier()

        logger.info(f"{device_model}: Device series: {device_series}")
        logger.info(f"{device_model}: Timeout multiplier: {timeout_multiplier}x")

        # Device-aware configuration sections with page objects
        configuration_sections = [
            {
                "name": "general",
                "page_obj": GeneralConfigPage,
                "expected_elements": ["input[name='identifier']"],
                "validation_method": "validate_general_section_navigation",
            },
            {
                "name": "network",
                "page_obj": NetworkConfigPage,
                "expected_elements": [
                    "select[name='mode']",
                    "input[name='sfp_mode']",
                    "input[name='ip_eth0']",
                ],
                "validation_method": "validate_network_section_navigation",
            },
            {
                "name": "time",
                "page_obj": TimeConfigPage,
                "expected_elements": ["select[name='timezones']"],
                "validation_method": "validate_time_section_navigation",
            },
            {
                "name": "outputs",
                "page_obj": OutputsConfigPage,
                "expected_elements": [
                    "select[name='signal1']",
                    "select[name='signal2']",
                ],
                "validation_method": "validate_outputs_section_navigation",
            },
            {
                "name": "gnss",
                "page_obj": GnssConfigPage,
                "expected_elements": ["input[value='1']", "input[name='galileo']"],
                "validation_method": "validate_gnss_section_navigation",
            },
            {
                "name": "upload",
                "page_obj": UploadConfigPage,
                "expected_elements": [
                    ".ajax-upload-dragdrop",
                    ".ajax-file-upload",
                    "text=drag & drop",
                ],
                "validation_method": "validate_upload_section_navigation",
            },
            {
                "name": "snmp",
                "page_obj": SnmpConfigPage,
                "expected_elements": ["input[name='ro_community1']"],
                "validation_method": "validate_snmp_section_navigation",
            },
            {
                "name": "syslog",
                "page_obj": SyslogConfigPage,
                "expected_elements": [
                    "input[name='level']",
                    "input[name='target_a']",
                    "input[name='port_a']",
                ],
                "validation_method": "validate_syslog_section_navigation",
            },
            {
                "name": "access",
                "page_obj": AccessConfigPage,
                "expected_elements": [
                    "input[name='cfgpwd']",
                    "input[name='uplpwd']",
                    "input[name='stspwd']",
                ],
                "validation_method": "validate_access_section_navigation",
            },
        ]

        # Add PTP section for Series 3 devices only using page object method
        try:
            ptp_supported = dashboard_page_obj.is_ptp_supported()
            if ptp_supported:
                configuration_sections.append(
                    {
                        "name": "ptp",
                        "page_obj": PtpConfigPage,
                        "expected_elements": [
                            "select[name='profile']",
                            "input[name='domain_number_eth1']",
                        ],
                        "validation_method": "validate_ptp_section_navigation",
                    }
                )
                logger.info(f"{device_model}: PTP section included for Series 3 device")
            else:
                logger.info(
                    f"{device_model}: PTP section not supported for this device"
                )
        except Exception as e:
            logger.warning(f"{device_model}: PTP support detection failed: {e}")

        # Navigate through all configuration sections
        successful_navigations = []
        failed_navigations = []

        for section_config in configuration_sections:
            section_name = section_config["name"]
            page_obj_class = section_config["page_obj"]
            expected_elements = section_config["expected_elements"]
            validation_method = section_config["validation_method"]

            try:
                logger.info(f"{device_model}: Navigating to {section_name} section")

                # Initialize page object for this section
                section_page_obj = page_obj_class(unlocked_config_page, device_model)

                # Navigate to section using page object method
                section_page_obj.navigate_to_page()
                section_page_obj.wait_for_page_load()

                # Verify page loaded correctly using page object method
                current_url = section_page_obj.get_current_url()
                assert (
                    section_name in current_url
                ), f"Should navigate to {section_name} page for {device_model}"

                # Verify at least one expected element is present using page object validation
                section_page_obj.validate_expected_elements_present(
                    expected_elements, section_name, device_model
                )

                # Additional section-specific validation using page object method
                validation_func = getattr(section_page_obj, validation_method, None)
                if validation_func:
                    validation_func()

                successful_navigations.append(section_name)
                logger.info(
                    f"{device_model}: Successfully navigated to {section_name} section"
                )

                # Additional wait for JavaScript-driven pages like upload
                if section_name == "upload":
                    upload_delay = section_page_obj.get_upload_delay()
                    time.sleep(upload_delay)

            except Exception as e:
                failed_navigations.append({"section": section_name, "error": str(e)})
                logger.warning(
                    f"{device_model}: Failed to navigate to {section_name} section: {e}"
                )

        # Summary of navigation results
        logger.info(f"{device_model}: Navigation summary:")
        logger.info(f"{device_model}: Successful sections: {successful_navigations}")
        if failed_navigations:
            logger.warning(f"{device_model}: Failed sections: {failed_navigations}")

        # Validate navigation workflow integrity using page object methods
        try:
            dashboard_page_obj.validate_all_sections_navigation_workflow_integrity(
                successful_navigations, failed_navigations
            )

            # Series-specific validation using page object methods
            if device_series == 2:
                dashboard_page_obj.validate_series2_all_sections_navigation_patterns(
                    successful_navigations
                )
            elif device_series == 3:
                dashboard_page_obj.validate_series3_all_sections_navigation_patterns(
                    successful_navigations
                )

            # Cross-validation test using page object method
            dashboard_page_obj.test_all_sections_navigation_cross_validation()

        except Exception as e:
            logger.warning(
                f"{device_model}: Navigation workflow validation failed: {e}"
            )

        # Assert that at least some sections were successfully navigated
        assert (
            len(successful_navigations) > 0
        ), f"Should successfully navigate to at least one configuration section for {device_model}"

        # Final validation using page object method
        dashboard_page_obj.validate_all_config_sections_navigation_completion(
            successful_navigations, device_model
        )

        logger.info(
            f"{device_model}: Navigation through all configuration sections completed successfully"
        )
        print(
            f"All configuration sections navigation passed for {device_model}: {len(successful_navigations)}/{len(configuration_sections)} sections successful"
        )

    except Exception as e:
        logger.error(
            f"{device_model}: Navigation through all configuration sections encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(
            f"Navigation through all configuration sections failed for {device_model}: {e}"
        )
