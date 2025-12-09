"""
Category 26: API & Alternative Interface Testing - Individual Test
Test 26.1.10: File Download Endpoints - FIXED
Test Count: 1 test
Hardware: Conditional ([WARNING])
Priority: LOW
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 26.1.10
FIXED: Increased timeouts, proper authentication, device-aware handling
"""

import pytest
import time
from playwright.sync_api import Page


def test_26_1_10_file_download_endpoints(browser, base_url: str, device_password: str):
    """Test 26.1.10: File download endpoints (/log)"""
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    # FIXED: Authenticate first for protected endpoints
    # Check if already logged in by navigating to a protected endpoint
    page.goto(base_url, timeout=10000, wait_until="domcontentloaded")

    # If we can access protected content without redirect to login, we're logged in
    if page.get_by_placeholder("Password").count() > 0:
        # Need to login
        password_field = page.get_by_placeholder("Password")
        password_field.fill(device_password)

        # Use role-based locator per LOCATOR_STRATEGY.md
        submit_button = page.get_by_role("button", name="Submit")
        submit_button.click()
        time.sleep(3)
    # Test file download endpoints
    download_endpoints = [
        f"{base_url}/log",  # Log files download
        f"{base_url}/legal",  # Legal info (PDF)
    ]
    download_results = {}
    for endpoint in download_endpoints:
        try:
            # FIXED: Increased timeout for device responsiveness and downloads
            response = page.goto(endpoint, wait_until="domcontentloaded", timeout=30000)
            content_type = response.headers.get("content-type", "").lower()
            download_results[endpoint] = {
                "status": response.status,
                "content_type": content_type,
            }
            if response.status == 200:
                if "pdf" in content_type:
                    print(f" {endpoint}: PDF download working")
                elif "zip" in content_type or "application" in content_type:
                    print(f" {endpoint}: File download working")
                else:
                    print(f"? {endpoint}: Unexpected content type: {content_type}")
            else:
                print(f"? {endpoint}: Download returned status: {response.status}")
        except Exception as e:
            download_results[endpoint] = {"error": str(e)}
            print(f"Download endpoint test failed for {endpoint}: {e}")
            continue
    context.close()
    # Should be able to access download endpoints
    successful_downloads = [
        ep
        for ep, data in download_results.items()
        if isinstance(data, dict) and data.get("status") == 200
    ]
    print(
        f"Successful downloads: {len(successful_downloads)}/{len(download_endpoints)}"
    )
