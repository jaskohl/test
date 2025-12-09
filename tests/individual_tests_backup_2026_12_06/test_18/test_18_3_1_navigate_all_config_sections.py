"""
Test 18.3.1: Navigate Through All Configuration Sections
Category: 18 - Workflow Tests
Test Count: Part of 8 tests in Category 18
Hardware: Device Only
Priority: HIGH - End-to-end workflow validation
Series: Both Series 2 and 3

Extracted from: tests/test_18_workflow.py
Source Class: TestNavigationWorkflow
"""

import pytest
import time
from playwright.sync_api import Page
from pages.device_capabilities import DeviceCapabilities


def test_18_3_1_navigate_all_config_sections(
    unlocked_config_page: Page, base_url: str, request
):
    """
    Test 18.3.1: Navigate Through All Configuration Sections (Device-Aware)
    Purpose: Verify can navigate through all sections without errors
    Expected: Smooth navigation, no authentication required
    Device-Aware: Uses device model for model-specific validation and timeout handling
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate navigation workflow")

    device_series = DeviceCapabilities.get_series(device_model)

    # Device-aware element expectations - FIXED: Using actual user-facing locators from device exploration
    base_sections = [
        ("general", ["input[name='identifier']"]),
        (
            "network",
            [
                "select[name='mode']",
                "input[name='sfp_mode']",
                "input[name='ip_eth0']",
            ],
        ),  # Series 2 or Series 3
        ("time", ["select[name='timezones']"]),
        (
            "outputs",
            ["select[name='signal1']", "select[name='signal2']"],
        ),  # FIXED: Using actual elements from device exploration
        (
            "gnss",
            ["input[value='1']", "input[name='galileo']"],
        ),  # GPS checkbox or Galileo
        (
            "upload",
            [
                ".ajax-upload-dragdrop",  # Always visible upload container
                ".ajax-file-upload",  # Upload widget button container
                "text=drag & drop",  # Visible instruction text
            ],
        ),  # DEVICE-AWARE: Check for visible upload UI elements instead of hidden file input
        ("snmp", ["input[name='ro_community1']"]),
        (
            "syslog",
            [
                "input[name='level']",
                "input[name='target_a']",
                "input[name='port_a']",
            ],
        ),  # Form inputs always present
        (
            "access",
            [
                "input[name='cfgpwd']",
                "input[name='uplpwd']",
                "input[name='stspwd']",
            ],
        ),  # Use name attributes instead of type
        (
            "contact",
            ["a[href*='novatech']", "a[href*='913']"],
        ),  # Contact page has static links, not form fields
    ]

    # Add PTP section for Series 3 devices only
    ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)
    if ptp_supported:
        base_sections.append(
            ("ptp", ["select[name='profile']", "input[name='domain_number_eth1']"])
        )

    for section_path, expected_elements in base_sections:
        unlocked_config_page.goto(
            f"{base_url}/{section_path}", wait_until="domcontentloaded"
        )
        # Additional wait for JavaScript-driven pages like upload
        if section_path == "upload":
            time.sleep(1)  # Allow upload widget initialization

        # Verify page loaded
        assert (
            section_path in unlocked_config_page.url
        ), f"Should navigate to {section_path} page for {device_model}"

        # Verify at least one expected element is present (device-aware)
        found_element = False
        for element_selector in expected_elements:
            element = unlocked_config_page.locator(element_selector)
            if element.count() > 0:
                found_element = True
                break
        assert (
            found_element
        ), f"Should find at least one expected element on {section_path} page for {device_model}"
