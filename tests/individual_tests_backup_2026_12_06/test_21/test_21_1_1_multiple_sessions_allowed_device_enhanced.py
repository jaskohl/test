"""
Test 21.1.1: Multiple Sessions Allowed (Device-Enhanced)
Category 21: Session & Concurrency Testing - COMPLETE
Test Count: 3 tests
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 21

Enhanced Version with DeviceCapabilities Integration
"""

import pytest
import time
from playwright.sync_api import Page
from pages.device_capabilities import DeviceCapabilities


def test_21_1_1_multiple_sessions_allowed_device_enhanced(
    browser, base_url: str, request
):
    """Test 21.1.1: Multiple browser sessions can access device with device-aware patterns"""
    # Device detection and validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate behavior")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Capability validation
    supported_features = DeviceCapabilities.get_capabilities(device_model)

    print(f"\n=== Device-Enhanced Session Concurrency Test ===")
    print(f"Device Model: {device_model}")
    print(f"Device Series: {device_series}")
    print(f"Timeout Multiplier: {timeout_multiplier}")
    print(f"Supported Features: {supported_features}")

    # Create two contexts (simulating two users) with device-aware timing
    context1 = browser.new_context()
    context2 = browser.new_context()
    page1 = context1.new_page()
    page2 = context2.new_page()

    try:
        # Login with both sessions using device-aware timeout patterns
        for i, page in enumerate([page1, page2], 1):
            print(f"\n--- Session {i} Login Process ---")

            # Navigate with device-aware timeout
            page.goto(
                base_url,
                wait_until="domcontentloaded",
                timeout=int(30000 * timeout_multiplier),
            )
            time.sleep(1 * timeout_multiplier)

            # Password field interaction with device-aware timing
            password_field = page.get_by_placeholder("Password")
            password_field.wait_for(timeout=int(5000 * timeout_multiplier))

            # Get device password from fixture with device series awareness
            device_password = request.getfixturevalue("device_password")
            password_field.fill(device_password)

            # Submit with device-aware timeout
            submit_btn = page.locator("button[type='submit']")
            submit_btn.click()

            # Wait for login completion with series-specific timing
            login_wait_time = 12 * timeout_multiplier if device_series == "3" else 10
            time.sleep(login_wait_time)

            # Verify login success with device-aware validation
            assert (
                "Kronos" in page.title()
            ), f"Session {i}: Login failed - not on Kronos page"
            print(f"Session {i}: Successfully logged in")

        # Verify both sessions are active with device-aware checks
        print(f"\n=== Verifying Both Sessions Active ===")
        for i, page in enumerate([page1, page2], 1):
            page_title = page.title()
            assert (
                "Kronos" in page_title
            ), f"Session {i}: Lost session or invalid title: {page_title}"
            print(f"Session {i}: Session verified active - Title: {page_title}")

        # Series-specific validation
        if device_series == "3":
            print("Series 3: Extended timeout validation applied")
        else:
            print("Series 2: Standard timeout validation applied")

        print(f"\n=== Multiple Sessions Test PASSED ===")
        print(f"Both browser contexts successfully accessed device concurrently")

    except Exception as e:
        print(f"\n=== Multiple Sessions Test FAILED ===")
        print(f"Error: {str(e)}")
        raise

    finally:
        # Clean up contexts with device-aware timing
        context1.close()
        context2.close()
        time.sleep(1 * timeout_multiplier)
