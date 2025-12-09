"""
Test 1.2.2: Invalid Password Unlock Error
Purpose: Verify error on invalid configuration password
Expected: Error message, configuration remains locked

Category: 1 - Authentication & Session Management
Test Type: Unit Test
Priority: CRITICAL
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_1_2_2_invalid_password_unlock_error(logged_in_page: Page, base_url: str):
    """
    Test 1.2.2: Invalid Password Unlock Error
    Purpose: Verify error on invalid configuration password
    Expected: Error message, configuration remains locked
    Direct implementation to avoid debug file creation for expected failures.
    Device-aware error detection for configuration unlock failures.
    """
    # Navigate to configuration unlock form
    logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")
    configure_button = logged_in_page.locator("a[title*='locked']").filter(
        has_text="Configure"
    )
    if configure_button.is_visible():
        configure_button.click()
        time.sleep(1)

    # Perform direct authentication attempt (skip page object method to avoid debug capture)
    password_field = logged_in_page.locator("input[name='cfg_password']")
    password_field.wait_for(state="visible")
    password_field.fill("wrong_password_67890")

    # Submit the form
    submit_button = logged_in_page.get_by_role("button", name="Submit")
    submit_button.click()

    # Wait for error response
    time.sleep(1)

    # Device-aware error detection for config unlock
    config_error_detected = False

    # Method 1: Primary - Exact "Incorrect password." text
    try:
        if logged_in_page.get_by_text("Incorrect password.", exact=False).is_visible(
            timeout=2000
        ):
            config_error_detected = True
            print("Config unlock: Found exact error message")
    except Exception:
        pass

    # Method 2: Check if still on login/config page (failure indicator)
    try:
        if (
            "login" in logged_in_page.url.lower()
            or "authenticate" in logged_in_page.url.lower()
        ):
            # On login page after config access attempt - check for error elements
            # Method 2a: CSS class-based error detection
            error_elements = logged_in_page.locator(
                "[class*='error'], [class*='alert'], [class*='danger']"
            )
            if error_elements.count() > 0:
                for i in range(error_elements.count()):
                    elem = error_elements.nth(i)
                    if elem.is_visible(timeout=2000):
                        elem_text = elem.text_content()
                        if elem_text and len(elem_text) > 0:
                            config_error_detected = True
                            print(
                                f"Config unlock: Found CSS error element: '{elem_text}'"
                            )
                            break

            # Method 2b: Check if password field is still visible (unlock failed)
            if not config_error_detected:
                cfg_password_field = logged_in_page.locator(
                    "input[name='cfg_password']"
                )
                if cfg_password_field.is_visible():
                    config_error_detected = True
                    print("Config unlock: Password field still visible - unlock failed")

            # Method 2c: Check for any error keywords in page content
            if not config_error_detected:
                page_content = logged_in_page.locator("body").text_content()
                error_keywords = [
                    "error",
                    "failed",
                    "invalid",
                    "incorrect",
                    "wrong",
                    "denied",
                ]
                for keyword in error_keywords:
                    if keyword.lower() in page_content.lower():
                        config_error_detected = True
                        print(f"Config unlock: Found error keyword: {keyword}")
                        break

    except Exception as e:
        print(f"Config unlock error detection failed: {e}")

    # Final assertions for configuration unlock failure
    assert (
        config_error_detected
    ), "Configuration unlock error should be detectable through one or more methods"
    assert (
        "login" in logged_in_page.url.lower()
        or "authenticate" in logged_in_page.url.lower()
    ), "Should remain on login/authenticate page after unlock failure"

    # Verify configuration remains locked (no config sections visible)
    general_link = logged_in_page.get_by_role("link", name="General")
    assert (
        not general_link.is_visible()
    ), "Configuration should remain locked after failed unlock attempt"
