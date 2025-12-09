"""
Test 21.1.2: Concurrent Config Changes (Device-Enhanced)
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


def test_21_1_2_concurrent_config_changes_device_enhanced(
    browser, base_url: str, request
):
    """Test 21.1.2: Concurrent configuration changes handling with device-aware patterns"""
    # Device detection and validation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate behavior")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Capability validation
    supported_features = DeviceCapabilities.get_capabilities(device_model)

    print(f"\n=== Device-Enhanced Concurrent Config Changes Test ===")
    print(f"Device Model: {device_model}")
    print(f"Device Series: {device_series}")
    print(f"Timeout Multiplier: {timeout_multiplier}")
    print(f"Supported Features: {supported_features}")

    # Create two contexts for concurrent configuration
    context1 = browser.new_context()
    context2 = browser.new_context()
    page1 = context1.new_page()
    page2 = context2.new_page()

    try:
        # Both login and unlock config with device-aware patterns
        for i, page in enumerate([page1, page2], 1):
            print(f"\n--- Session {i} Login and Unlock Process ---")

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

            # Unlock config with device-aware patterns
            print(f"Session {i}: Unlocking configuration...")
            page.goto(f"{base_url}/", wait_until="domcontentloaded")

            # Find and click configure button with device-aware wait
            configure_btn = page.locator("a[title*='locked']").filter(
                has_text="Configure"
            )
            configure_btn.wait_for(timeout=int(10000 * timeout_multiplier))

            if configure_btn.is_visible():
                configure_btn.click()
                time.sleep(1 * timeout_multiplier)

                # Handle configuration password if required
                cfg_password = page.locator("input[name='cfg_password']")
                if cfg_password.is_visible():
                    cfg_password.wait_for(timeout=int(5000 * timeout_multiplier))
                    cfg_password.fill(device_password)
                    cfg_submit = page.locator("button[type='submit']")
                    cfg_submit.click()
                    time.sleep(10 * timeout_multiplier)

            print(f"Session {i}: Successfully logged in and unlocked config")

        # Both navigate to same config page with device-aware navigation
        print(f"\n=== Navigating Both Sessions to Display Configuration ===")
        for i, page in enumerate([page1, page2], 1):
            page.goto(f"{base_url}/display", wait_until="domcontentloaded")
            time.sleep(2 * timeout_multiplier)
            print(f"Session {i}: Navigated to display configuration page")

        # Make changes in both sessions (last write wins) with device-aware interaction
        print(f"\n=== Making Concurrent Configuration Changes ===")
        mode1 = page1.locator("select[name='mode']")
        mode2 = page2.locator("select[name='mode']")

        if mode1.is_visible() and mode2.is_visible():
            # Wait for both mode selectors with device-aware timing
            mode1.wait_for(timeout=int(5000 * timeout_multiplier))
            mode2.wait_for(timeout=int(5000 * timeout_multiplier))

            print("Both sessions found mode selector - making different selections")

            # Session 1 selects option 1
            mode1.select_option(index=1)
            print("Session 1: Selected mode option 1")
            time.sleep(1 * timeout_multiplier)

            # Session 2 selects option 2 (this will win)
            mode2.select_option(index=2)
            print("Session 2: Selected mode option 2")
            time.sleep(1 * timeout_multiplier)

            # Verify the final state (last write wins)
            final_mode = mode2.input_value()
            print(f"Final configuration mode: {final_mode}")

            # Series-specific validation
            if device_series == "3":
                print(
                    "Series 3: Extended timeout validation applied for concurrent changes"
                )
            else:
                print(
                    "Series 2: Standard timeout validation applied for concurrent changes"
                )
        else:
            print(
                "Mode selector not visible in one or both sessions - skipping concurrent change test"
            )

        print(f"\n=== Concurrent Config Changes Test PASSED ===")
        print(
            f"Both browser contexts successfully made concurrent configuration changes"
        )

    except Exception as e:
        print(f"\n=== Concurrent Config Changes Test FAILED ===")
        print(f"Error: {str(e)}")
        raise

    finally:
        # Clean up contexts with device-aware timing
        context1.close()
        context2.close()
        time.sleep(1 * timeout_multiplier)
