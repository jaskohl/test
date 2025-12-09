"""
Test 21.2.1: Session Survives Page Refresh (Device-Enhanced)
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


def test_21_2_1_session_survives_page_refresh_device_enhanced(
    logged_in_page: Page, base_url: str, request
):
    """Test 21.2.1: Session persists across page refresh with device-aware patterns"""
    # Device detection and validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate behavior")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Capability validation
    supported_features = DeviceCapabilities.get_capabilities(device_model)

    print(f"\n=== Device-Enhanced Session Persistence Test ===")
    print(f"Device Model: {device_model}")
    print(f"Device Series: {device_series}")
    print(f"Timeout Multiplier: {timeout_multiplier}")
    print(f"Supported Features: {supported_features}")

    try:
        # Navigate to main page with device-aware timing
        print(f"\n=== Initial Navigation ===")
        logged_in_page.goto(
            f"{base_url}/",
            wait_until="domcontentloaded",
            timeout=int(30000 * timeout_multiplier),
        )

        # Verify initial login state with device-aware checks
        initial_title = logged_in_page.title()
        initial_url = logged_in_page.url
        print(f"Initial page title: {initial_title}")
        print(f"Initial URL: {initial_url}")

        assert (
            "Kronos" in initial_title
        ), f"Initial login failed - not on Kronos page: {initial_title}"
        assert (
            "authenticate" not in initial_url.lower()
        ), f"Still on auth page: {initial_url}"

        print("Initial session verification PASSED")

        # Perform page refresh with device-aware timing
        print(f"\n=== Page Refresh Process ===")
        refresh_start_time = time.time()

        # Execute refresh with device-aware timeout
        logged_in_page.reload(timeout=int(30000 * timeout_multiplier))

        # Wait for refresh completion with series-specific timing
        refresh_wait_time = 2 * timeout_multiplier if device_series == "3" else 1.5
        time.sleep(refresh_wait_time)

        refresh_end_time = time.time()
        refresh_duration = refresh_end_time - refresh_start_time

        print(f"Page refresh completed in {refresh_duration:.2f} seconds")

        # Verify session persistence after refresh with device-aware checks
        print(f"\n=== Post-Refresh Session Verification ===")
        post_refresh_title = logged_in_page.title()
        post_refresh_url = logged_in_page.url

        print(f"Post-refresh page title: {post_refresh_title}")
        print(f"Post-refresh URL: {post_refresh_url}")

        # Assert session survived refresh
        assert (
            "Kronos" in post_refresh_title
        ), f"Session lost after refresh - not on Kronos page: {post_refresh_title}"
        assert (
            "authenticate" not in post_refresh_url.lower()
        ), f"Redirected to auth page after refresh: {post_refresh_url}"

        # Additional device-aware session validation
        print(f"\n=== Advanced Session Validation ===")

        # Check for key page elements that indicate valid session
        try:
            # Look for navigation elements that should be present when logged in
            nav_elements = logged_in_page.locator(
                "nav, .navigation, [class*='nav'], [id*='nav']"
            ).first
            if nav_elements.is_visible(timeout=int(5000 * timeout_multiplier)):
                print("Navigation elements found - session valid")
            else:
                print("Navigation elements not found - checking alternative indicators")

                # Alternative session validation - look for configuration links
                config_links = logged_in_page.locator(
                    "a[href*='config'], a[href*='general'], a[href*='network']"
                )
                if config_links.count() > 0:
                    print(
                        f"Found {config_links.count()} configuration links - session valid"
                    )
                else:
                    print(
                        "No clear session indicators found - but title and URL are valid"
                    )

        except Exception as e:
            print(f"Advanced session validation encountered issue: {e}")
            print("Falling back to basic title/URL validation")

        # Series-specific session persistence validation
        if device_series == "3":
            print("Series 3: Extended session persistence validation applied")
            # Series 3 may have different session management behavior
            additional_wait = 1 * timeout_multiplier
            time.sleep(additional_wait)
            print(
                f"Applied additional {additional_wait}s wait for Series 3 session stability"
            )
        else:
            print("Series 2: Standard session persistence validation applied")

        # Final validation - ensure we're still on the expected page
        final_title = logged_in_page.title()
        final_url = logged_in_page.url

        print(f"\n=== Final Session State ===")
        print(f"Final page title: {final_title}")
        print(f"Final URL: {final_url}")

        # Verify we haven't been redirected to login
        assert (
            "Kronos" in final_title
        ), f"Session invalid - not on Kronos page: {final_title}"
        assert (
            "authenticate" not in final_url.lower()
        ), f"Session expired - redirected to auth: {final_url}"

        print(f"\n=== Session Persistence Test PASSED ===")
        print(f"Session successfully survived page refresh on {device_series} device")

    except Exception as e:
        print(f"\n=== Session Persistence Test FAILED ===")
        print(f"Error: {str(e)}")
        raise
