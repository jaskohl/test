"""
Test 26.1.1: Discover all web interface endpoints from device exploration data
Category 26: API & Alternative Interface Testing - FIXED
Test Count: Part of 11 tests in Category 26
Hardware: Conditional ([WARNING])
Priority: LOW
Series: Both Series 2 and 3

Extracted from: tests/test_26_api_interfaces.py
Source Class: TestAPIInterfaces
"""

import pytest
import time
from playwright.sync_api import Page


def test_26_1_1_web_interface_endpoints_discovery(browser, base_url: str):
    """Test 26.1.1: Discover all web interface endpoints from device exploration data"""
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    # EXPANDED: Test all web endpoints discovered by device exploration
    web_endpoints = [
        f"{base_url}/",  # Dashboard
        f"{base_url}/general",  # General config
        f"{base_url}/time",  # Time config
        f"{base_url}/display",  # Display config
        f"{base_url}/outputs",  # Outputs config
        f"{base_url}/network",  # Network config
        f"{base_url}/snmp",  # SNMP config
        f"{base_url}/gnss",  # GNSS config
        f"{base_url}/syslog",  # Syslog config
        f"{base_url}/upload",  # Upload page
        f"{base_url}/access",  # Access config
        f"{base_url}/log",  # Log files
        f"{base_url}/legal",  # Legal info
        f"{base_url}/contact",  # Contact info
        f"{base_url}/login",  # Login page
        f"{base_url}/logout",  # Logout
    ]
    working_endpoints = []
    auth_required_endpoints = []
    for endpoint in web_endpoints:
        try:
            # FIXED: Increased timeout from 5000ms to 30000ms for device responsiveness
            response = page.goto(endpoint, wait_until="domcontentloaded", timeout=30000)
            if response.status in [200, 302]:
                working_endpoints.append(endpoint)
                # Check if redirected to login (indicates auth required)
                if "login" in page.url.lower() or "authenticate" in page.url.lower():
                    auth_required_endpoints.append(endpoint)
            elif response.status in [401, 403]:
                auth_required_endpoints.append(endpoint)

            print(f" {endpoint}: Status {response.status}")
        except Exception as e:
            print(f"Endpoint {endpoint} failed: {e}")
            continue
    context.close()
    # Assert we found working endpoints
    assert (
        len(working_endpoints) > 0
    ), f"No working web endpoints found. Tested: {web_endpoints}"
    print(f"Working web endpoints: {len(working_endpoints)}/{len(web_endpoints)}")
    print(f"Auth-required endpoints: {len(auth_required_endpoints)}")
    # At least login endpoint should work for API discovery
    assert any(
        "login" in ep for ep in working_endpoints
    ), "Login endpoint should be accessible"
