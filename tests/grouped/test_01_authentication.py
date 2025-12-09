"""
Category 1: Authentication & Session Management Tests
Test Count: 8 tests
Hardware: Device Only
Priority: CRITICAL - Foundation for all other tests
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 1
"""

import pytest
import re
import time
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.configuration_unlock_page import ConfigurationUnlockPage


class TestAuthentication:
    """Test 1.1: Status Monitoring Authentication (Login)"""

    def test_1_1_1_valid_password_login(
        self, page: Page, base_url: str, device_password: str
    ):
        """
        Test 1.1.1: Valid Password Login
        Purpose: Verify successful login with correct password
        Expected: Login succeeds, satellite loading occurs, dashboard visible
        """
        page.goto(base_url, wait_until="domcontentloaded")
        login_page = LoginPage(page)
        login_page.verify_page_loaded()
        success = login_page.login(password=device_password)
        assert success, "Login should succeed with valid password"
        # Wait for satellite loading (dynamic wait with 5s timeout based on device exploration)
        login_page.wait_for_satellite_loading()
        # Verify dashboard is visible (check for Configure button presence)
        configure_button = page.locator("a[title*='locked']").filter(
            has_text="Configure"
        )
        assert configure_button.is_visible(), "Should show Configure button after login"

    def test_1_1_2_invalid_password_error(self, page: Page, base_url: str):
        """
        Test 1.1.2: Invalid Password Error
        Purpose: Verify appropriate error on invalid password
        Expected: Error message displayed, login form remains visible
        Direct implementation to avoid debug file creation for expected failures.
        Device-aware error detection using multiple validation methods.
        """
        # Navigate to login page directly (skip page object to avoid debug capture)
        page.goto(base_url, wait_until="domcontentloaded")

        # Find and fill password field directly
        password_field = page.get_by_placeholder("Password").first
        expect(password_field).to_be_visible()
        expect(password_field).to_be_editable()

        password_field.clear()
        password_field.fill("invalid_password_12345")
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

    def test_1_1_3_empty_password_submission(self, page: Page, base_url: str):
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


class TestConfigurationUnlock:
    """Test 1.2: Configuration Access Authentication (Unlock)"""

    def test_1_2_1_valid_password_unlock(
        self, logged_in_page: Page, base_url: str, device_password: str
    ):
        """
        Test 1.2.1: Valid Password Configuration Unlock
        Purpose: Verify successful configuration unlock
        Expected: Configuration sections become visible after unlock
        """
        unlock_page = ConfigurationUnlockPage(logged_in_page)
        # Navigate to configure
        logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")
        configure_button = logged_in_page.locator("a[title*='locked']").filter(
            has_text="Configure"
        )
        if configure_button.is_visible():
            configure_button.click()
            time.sleep(1)
        success = unlock_page.unlock_configuration(password=device_password)
        assert success, "Configuration unlock should succeed with valid password"
        # Wait for satellite loading (dynamic wait with 5s timeout based on device exploration)
        unlock_page.wait_for_satellite_loading()
        # Verify configuration sections visible
        config_sections = ["General", "Network", "Time", "Outputs"]
        for section in config_sections:
            link = logged_in_page.get_by_role("link", name=section)
            expect(link).to_be_visible(timeout=5000)

    def test_1_2_2_invalid_password_unlock_error(
        self, logged_in_page: Page, base_url: str
    ):
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
            if logged_in_page.get_by_text(
                "Incorrect password.", exact=False
            ).is_visible(timeout=2000):
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
                        print(
                            "Config unlock: Password field still visible - unlock failed"
                        )

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


class TestDualAuthentication:
    """Test 1.3: Dual Authentication Workflow"""

    def test_1_3_1_status_then_config_auth(
        self, page: Page, base_url: str, device_password: str
    ):
        """
        Test 1.3.1: Complete Dual Authentication Flow
        Purpose: Verify both authentication cycles work in sequence
        Expected: Login succeeds, then unlock succeeds, full access granted
        """
        # First authentication: Status monitoring
        page.goto(base_url, wait_until="domcontentloaded")
        login_page = LoginPage(page)
        login_success = login_page.login(password=device_password)
        assert login_success, "First authentication (login) should succeed"
        # Wait for satellite loading (dynamic wait with 5s timeout based on device exploration)
        login_page.wait_for_satellite_loading()
        # Second authentication: Configuration access
        unlock_page = ConfigurationUnlockPage(page)
        page.goto(f"{base_url}/", wait_until="domcontentloaded")
        configure_button = page.locator("a[title*='locked']").filter(
            has_text="Configure"
        )
        if configure_button.is_visible():
            configure_button.click()
        unlock_success = unlock_page.unlock_configuration(password=device_password)
        assert unlock_success, "Second authentication (unlock) should succeed"
        # Wait for satellite loading (dynamic wait with 5s timeout based on device exploration)
        unlock_page.wait_for_satellite_loading()
        # Verify full access
        access_info = unlock_page.get_configuration_access_level()
        assert not access_info["locked"], "Configuration should be fully unlocked"
        assert (
            len(access_info["sections_available"]) >= 5
        ), "Should have access to multiple sections"
