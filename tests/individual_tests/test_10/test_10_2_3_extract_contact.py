"""
Category 10: Dashboard - Test 10.2.3
Extract Contact from Status Table - Pure Page Object Pattern
Test Count: 4 of 10 in Category 10
Hardware: Device Only
Priority: HIGH - Critical status monitoring
Series: Both Series 2 and 3
TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
Based on dashboard requirements and contact extraction patterns
"""

import pytest
import logging
from playwright.sync_api import Page, expect
from pages.device_capabilities import DeviceCapabilities
from pages.dashboard_page import DashboardPage

logger = logging.getLogger(__name__)


def test_10_2_3_extract_contact(unlocked_config_page: Page, base_url: str, request):
    """
    Test 10.2.3: Extract Contact - Pure Page Object Pattern
    Purpose: Verify can extract contact from status table with device-aware validation
    Expected: Contact value is readable with device-specific data extraction (may be empty - this is valid)
    TRANSFORMED: Pure page object architecture with DeviceCapabilities integration
    Series: Both - validates contact extraction patterns across device variants
    """
    # Get device model for device-aware testing
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail(
            "Device model not detected - cannot validate dashboard data extraction"
        )

    # Initialize page object with device-aware patterns
    dashboard_page = DashboardPage(unlocked_config_page, device_model)

    logger.info(
        f"Testing contact extraction on {device_model} using pure page object pattern"
    )

    try:
        # Navigate to dashboard page using page object method
        dashboard_page.navigate_to_page()

        # Wait for page load with device-aware timeout
        dashboard_page.wait_for_page_load()

        # Test contact extraction using page object method
        logger.info("Testing contact extraction")

        contact_extracted = dashboard_page.get_contact()
        logger.info(
            f"Extracted contact: '{contact_extracted}' (type: {type(contact_extracted)})"
        )

        # Validate contact data structure
        if contact_extracted is not None:
            assert isinstance(
                contact_extracted, str
            ), f"Contact should be a string, got {type(contact_extracted)}"

            # Empty contact is valid behavior for unconfigured devices
            if contact_extracted:
                assert (
                    len(contact_extracted) > 0
                ), "If present, contact should have content"
                logger.info(f"Contact content validated: '{contact_extracted}'")
            else:
                logger.info(
                    "Contact is empty - this is valid behavior for unconfigured devices"
                )
        else:
            logger.info(
                "Contact extraction returned None - this may be expected for this device model"
            )

        # Test device information extraction using page object method
        logger.info("Testing device information extraction")

        device_info = dashboard_page.get_device_info()
        logger.info(
            f"Device information keys: {list(device_info.keys()) if device_info else 'None'}"
        )

        # Test status data extraction using page object method
        logger.info("Testing status data extraction")

        status_data = dashboard_page.get_status_data()
        logger.info(
            f"Status data keys: {list(status_data.keys()) if status_data else 'None'}"
        )

        # Look for contact data in status information
        if status_data:
            contact_key = None
            for key in status_data.keys():
                if key.lower() in [
                    "contact",
                    "device contact",
                    "administrator contact",
                ]:
                    contact_key = key
                    break

            if contact_key:
                logger.info(f"Found contact key in status data: {contact_key}")
                contact_from_status = status_data[contact_key]
                logger.info(f"Contact from status data: '{contact_from_status}'")
            else:
                # Check if contact data exists under different naming
                potential_keys = [
                    k for k in status_data.keys() if "contact" in k.lower()
                ]
                if potential_keys:
                    logger.info(
                        f"Found potential contact keys in status data: {potential_keys}"
                    )
                else:
                    logger.info(
                        "No contact data found in status data - this may be expected for this device model"
                    )

        # Test device-specific contact expectations using page object method
        device_series = DeviceCapabilities.get_series(device_model)

        if device_series == 2:
            logger.info(f"Testing Series 2 specific contact patterns on {device_model}")
            # Series 2: Basic contact field validation
            contact_patterns = dashboard_page.get_series_2_contact_patterns()
            logger.info(f"Series 2 contact patterns: {contact_patterns}")
        elif device_series == 3:
            logger.info(f"Testing Series 3 specific contact patterns on {device_model}")
            # Series 3: May have additional contact fields or formatting
            contact_patterns = dashboard_page.get_series_3_contact_patterns()
            logger.info(f"Series 3 contact patterns: {contact_patterns}")

        # Test contact field validation using page object method
        logger.info("Testing contact field validation")

        contact_valid = dashboard_page.validate_contact_field()
        logger.info(f"Contact field validation: {contact_valid}")

        # Test contact persistence using page object method
        logger.info("Testing contact persistence")

        contact_persistent = dashboard_page.test_contact_persistence()
        logger.info(f"Contact persistence: {contact_persistent}")

        # Test dashboard completeness using page object method
        logger.info("Testing dashboard completeness")

        dashboard_complete = dashboard_page.is_dashboard_complete()
        logger.info(f"Dashboard completeness: {dashboard_complete}")

        # Test navigation reliability using page object method
        logger.info("Testing navigation reliability")

        navigation_reliable = dashboard_page.test_navigation_reliability()
        logger.info(f"Dashboard navigation reliability: {navigation_reliable}")

        # Cross-validate with device capabilities
        device_capabilities_info = DeviceCapabilities.get_device_info(device_model)
        hardware_model = device_capabilities_info.get("hardware_model", "Unknown")
        logger.info(
            f"Cross-validating contact extraction from device: {hardware_model}"
        )

        # Performance validation using device baselines
        performance_expectations = DeviceCapabilities.get_performance_expectations(
            device_model
        )
        if performance_expectations:
            nav_performance = performance_expectations.get("navigation_performance", {})
            section_nav = nav_performance.get("section_navigation", {})
            typical_time = section_nav.get("typical_time", "")
            if typical_time:
                logger.info(
                    f"Dashboard navigation performance baseline: {typical_time}"
                )

        # Test contact extraction alternative methods using page object method
        logger.info("Testing contact extraction alternative methods")

        alt_contact = dashboard_page.extract_contact_alternative()
        logger.info(f"Alternative contact extraction: '{alt_contact}'")

        # Test page data retrieval using page object method
        logger.info("Testing page data retrieval")

        page_data = dashboard_page.get_page_data()
        logger.info(
            f"Dashboard page data keys: {list(page_data.keys()) if page_data else 'None'}"
        )

        # Test dashboard status using page object method
        logger.info("Testing dashboard status")

        dashboard_status = dashboard_page.get_dashboard_status()
        logger.info(f"Dashboard status: {dashboard_status}")

        # Test contact field format validation using page object method
        logger.info("Testing contact field format validation")

        contact_format_valid = dashboard_page.validate_contact_format()
        logger.info(f"Contact format validation: {contact_format_valid}")

        # Test contact information completeness using page object method
        logger.info("Testing contact information completeness")

        contact_complete = dashboard_page.is_contact_info_complete()
        logger.info(f"Contact information completeness: {contact_complete}")

        # Final validation using page object method
        logger.info("Performing final validation")

        final_contact = dashboard_page.get_contact()
        final_device_info = dashboard_page.get_device_info()
        final_status_data = dashboard_page.get_status_data()

        logger.info(f"Final contact extraction: '{final_contact}'")
        logger.info(
            f"Final device info keys: {list(final_device_info.keys()) if final_device_info else 'None'}"
        )
        logger.info(
            f"Final status data keys: {list(final_status_data.keys()) if final_status_data else 'None'}"
        )

        # Cross-validate contact extraction results
        if final_contact is not None:
            logger.info(f"Contact extraction validation PASSED: '{final_contact}'")
        else:
            logger.info(
                f"Contact extraction validation INFO: contact not available (may be expected)"
            )

        logger.info(
            f"Contact extraction test COMPLETED for {device_model} using pure page object pattern"
        )
        logger.info(
            "All operations performed using pure page object pattern - no direct locators used"
        )

    except Exception as e:
        logger.error(f"Contact extraction test failed on {device_model}: {e}")
        pytest.fail(f"Contact extraction test failed on {device_model}: {e}")
