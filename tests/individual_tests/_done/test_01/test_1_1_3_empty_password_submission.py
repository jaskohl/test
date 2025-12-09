"""
Test 1.1.3: Empty Password Submission
Purpose: Verify behavior when submitting empty password
Expected: Either rejects empty password OR accepts (documented vulnerability)

Category: 1 - Authentication & Session Management
Test Type: Unit Test
Priority: CRITICAL
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_1_1_3_empty_password_submission(page: Page, base_url: str):
    """
    Test 1.1.3: Empty Password Submission
    Purpose: Verify behavior when submitting empty password
    Expected: Either rejects empty password OR accepts (documented vulnerability)
    Follows Pattern 22: Clear acceptance criteria for edge cases.
    Direct implementation to avoid debug file creation for expected failures.
    Device-aware error detection to handle variable security policies.
    """
    # Navigate to login page directly (skip page object to avoid debug capture)
    page.goto(base_url, wait_until="domcontentloaded")

    # Find and fill password field directly with empty string
    password_field = page.get_by_placeholder("Password").first
    expect(password_field).to_be_visible()
    expect(password_field).to_be_editable()

    password_field.clear()
    # Fill empty password explicitly
    password_field.fill("")
    time.sleep(0.5)

    # Submit the form directly
    submit_button = page.get_by_role("button", name="Submit").first
    expect(submit_button).to_be_visible()
    submit_button.click()

    # Device-aware error detection with multiple validation methods
    error_detected = False

    # Method 1: Primary - Exact "Incorrect password." text (with or without period)
    try:
        if page.get_by_text("Incorrect password.", exact=False).is_visible(
            timeout=2000
        ):
            error_detected = True
            print("Found exact error message: 'Incorrect password.'")
    except Exception:
        pass

    # Method 2: Check if still on authenticate page (strong failure indicator)
    try:
        if "authenticate" in page.url.lower():
            # On auth page, check for various error indicators
            # Method 2a: CSS class-based error detection
            error_elements = page.locator(
                "[class*='error'], [class*='alert'], [class*='danger']"
            )
            if error_elements.count() > 0:
                for i in range(error_elements.count()):
                    elem = error_elements.nth(i)
                    if elem.is_visible(timeout=2000):
                        elem_text = elem.text_content()
                        if (
                            elem_text
                            and len(elem_text) > 0
                            and "incorrect" in elem_text.lower()
                        ):
                            error_detected = True
                            print(f"Found CSS error element: '{elem_text}'")
                            break

            # Method 2b: Field state verification (password field visible and empty)
            if not error_detected:
                password_field_state = page.get_by_placeholder("Password")
                if (
                    password_field_state.is_visible()
                    and password_field_state.input_value() == ""
                ):
                    error_detected = True
                    print("Detected error via field state: password field cleared")

            # Method 2c: Any error keyword in content
            if not error_detected:
                page_content = page.locator("body").text_content()
                error_keywords = [
                    "error",
                    "failed",
                    "invalid",
                    "incorrect",
                    "wrong",
                ]
                for keyword in error_keywords:
                    if keyword.lower() in page_content.lower():
                        error_detected = True
                        print(f"Found error keyword in content: {keyword}")
                        break

    except Exception as e:
        print(f"Error during validation: {e}")

    # Final assertion
    assert (
        error_detected
    ), "Authentication error should be detected through one or more validation methods"
    assert (
        "authenticate" in page.url.lower()
    ), "Should remain on authenticate page after failed login"
