"""
Login page object for Kronos device test automation.

Handles authentication functionality including:
- Password input (status monitoring authentication)
- Login form submission
- Enhanced authentication error handling with multiple detection methods
- Session management

Field: name="sts_password", id="sts_password", placeholder="Password"
Button: type="submit"
Enhanced error detection with 5 different methods based on systemPatterns.md Pattern 23
"""

from playwright.sync_api import Page, expect
from .base import BasePage
from .device_capabilities import DeviceCapabilities
from typing import Dict, Optional
import time


class LoginPage(BasePage):
    """
    Page object for Kronos device login functionality.

    Handles status monitoring authentication using exact selectors with enhanced error detection.

    """

    def __init__(self, page: Page):
        super().__init__(page)

    def verify_page_loaded(self):
        """Verify login page has loaded successfully."""
        try:
            # Device has password field with placeholder
            password_field = self.page.get_by_placeholder("Password")
            expect(password_field).to_be_visible()
        except Exception as e:
            print(f"Warning: Login page verification failed: {e}")

    def get_page_data(self) -> Dict[str, str]:
        """
        Extract data from the login page.

        Returns:
            Dictionary with login page data
        """
        page_data = {}

        try:
            # Check for error messages
            error_patterns = [
                "Login failed",
                "Authentication error",
                "Invalid credentials",
                "Session expired",
            ]

            for indicator in error_patterns:
                try:
                    element = self.page.get_by_text(indicator, exact=False)
                    if element.is_visible():
                        page_data["status_message"] = indicator
                        break
                except:
                    continue

        except Exception as e:
            print(f"Error getting login page data: {e}")

        return page_data

    def login(self, password: str = "novatech", **kwargs) -> bool:
        """
        Perform login using device-specific selectors.

        Args:
            password: Password for authentication (default: novatech)
            **kwargs: Additional login parameters (unused, kept for compatibility)

        Returns:
            True if login successful, False otherwise
        """
        try:
            self.start_performance_tracking("login")

            # PRIMARY: Use placeholder (device has this)
            password_field = self.page.get_by_placeholder("Password").first
            if not password_field.is_visible():
                # FALLBACK: Use name selector as device-specific fallback
                # Note: Using name selector - device has name="sts_password"
                password_field = self.page.locator("input[name='sts_password']").first

            expect(password_field).to_be_visible()
            expect(password_field).to_be_editable()

            # Clear any existing password and fill new password
            password_field.clear()
            password_field.fill(password)

            # wait for a moment to ensure input is registered
            time.sleep(0.5)

            # PRIMARY: Submit button by role
            submit_button = self.page.get_by_role("button", name="Submit").first
            expect(submit_button).to_be_visible()
            # Click submit
            submit_button.click()

            # Wait a moment for the page to respond
            time.sleep(1)

            # IMPORTANT: Check for authentication errors FIRST
            # This is the key fix - check for error messages immediately after submit
            auth_errors = self.check_for_authentication_errors()
            if auth_errors:
                print(f"Authentication failed: {auth_errors}")
                self.end_performance_tracking("login")
                return False

            # ENHANCED: Longer satellite loading wait for all devices
            self.wait_for_satellite_loading(
                timeout=15000
            )  # 15 seconds (increased from 3)

            # Verify login success with enhanced verification
            login_successful = self._verify_login_success()

            self.end_performance_tracking("login")

            if login_successful:
                return True
            else:
                print("Login verification failed")
                return False
        except Exception as e:
            print(f"Login error: {e}")
            self.end_performance_tracking("login")
            return False

    def _verify_login_success(self) -> bool:
        """
        Verify that login was successful by checking for dashboard indicators.

        ENHANCED: Device-aware verification that works for both Series 2 and Series 3 devices.
        Uses universal dashboard indicators that are consistent across device series.

        Returns:
            True if login appears successful, False otherwise
        """
        try:
            # Check if we're no longer on login page
            current_url = self.page.url
            if "authenticate" in current_url.lower():
                return False
        except Exception as e:
            print(f"Error verifying login page: {e}")
            return False

        # ENHANCED: Longer timeout for all devices to handle slower initialization
        max_wait_time = 15000  # 15 seconds (increased from 5 seconds)
        check_interval = 500  # Check every 0.5 seconds

        start_time = time.time()

        while (time.time() - start_time) * 1000 < max_wait_time:
            try:
                # FIRST: Check for and wait for loading mask removal
                # Use more specific selectors to avoid strict mode violations
                loading_selectors = [
                    ".page_loading_mask",
                    '[class*="loading"][class*="mask"]',
                    ".pageLoadingMask",
                ]

                loading_visible = False
                for selector in loading_selectors:
                    try:
                        mask = self.page.locator(
                            selector
                        ).first  # Use .first to avoid strict mode
                        if mask.is_visible():
                            loading_visible = True
                            break
                    except Exception:
                        continue

                if loading_visible:
                    time.sleep(0.5)
                    continue

                # SECOND: Universal dashboard indicators (work for both Series 2 and 3)
                universal_indicators = [
                    "#Main_Header",  # Main header element
                    ".main-header",  # Header CSS class
                    "h3:has-text('Time')",  # Time section header
                    "h3:has-text('Status')",  # Status section header
                    "h3:has-text('General')",  # General section header
                    "table",  # Must have tables (4 for both series)
                ]

                for selector in universal_indicators:
                    element = self.page.locator(selector)
                    if element.is_visible():
                        print(f"Found universal dashboard indicator: {selector}")
                        return True

                # THIRD: Configure button detection (generic patterns for both series)
                configure_selectors = [
                    'a[href="login"]:has-text("Configure")',  # Generic configure link
                    'a[href*="login"]',  # Any login link
                    'a[title*="locked"]',  # Locked title (Series 3 specific but safe)
                ]

                for selector in configure_selectors:
                    element = self.page.locator(selector)
                    if element.is_visible():
                        print(f"Found configure link: {selector}")
                        return True

                # FOURTH: Body content check with device-neutral keywords
                try:
                    body = self.page.locator("body")
                    if body.is_visible():
                        content = body.text_content()
                        if content:
                            content = content.strip()
                            # Device-neutral keywords that appear on all dashboard pages
                            required_keywords = ["kronos", "time", "status"]
                            keyword_count = sum(
                                1
                                for keyword in required_keywords
                                if keyword in content.lower()
                            )

                            if (
                                len(content) > 200 and keyword_count >= 2
                            ):  # Substantial content with 2+ keywords
                                print(
                                    f"Found substantial dashboard content ({len(content)} chars, {keyword_count} keywords)"
                                )
                                return True
                except Exception as e:
                    print(f"Error checking body content: {e}")

                # FIFTH: Table count verification (both series should have 4 tables minimum)
                try:
                    table_count = self.page.locator("table").count()
                    if table_count >= 4:  # Both series have 4 tables minimum
                        print(f"Found {table_count} tables (dashboard loaded)")
                        return True
                except Exception as e:
                    print(f"Error checking table count: {e}")

            except Exception as e:
                print(f"Error during verification check: {e}")

            time.sleep(check_interval / 1000)  # Convert to seconds

        print("No success indicators found after checking all device selectors")
        return False

    def navigate_to_page(self):
        """Navigate to login page."""
        try:
            # Navigate to root (redirects to login if not authenticated)
            current_url = self.page.url

            if "authenticate" not in current_url.lower():
                self.page.goto("/", wait_until="domcontentloaded")

            self.wait_for_page_load()

        except Exception as e:
            print(f"Error navigating to login page: {e}")

    def check_for_authentication_errors(self) -> Dict[str, str]:
        """
        Check for authentication errors using multiple detection methods


        Enhanced detection methods (5 layers):
        1. Exact device error messages
        2. Error CSS classes and visual indicators
        3. URL-based error detection
        4. Field state verification
        5. Content scanning for error keywords

        Confirmed device error message: "Incorrect password."

        Returns:
            Dictionary with error information if errors found, empty dict if no errors
        """
        errors = {}

        try:
            # Method 1: Check if we're still on auth page after submission (primary indicator)
            current_url = self.page.url
            if "authenticate" in current_url.lower():
                # Still on login page - check for error messages

                # Method 2: Check for exact device error message "Incorrect password." (with period)
                device_error_patterns = [
                    "Incorrect password.",  # Exact message
                    "Incorrect password",  # Fallback without period
                    "Authentication failed",  # Generic patterns
                    "Invalid password",
                    "Login failed",
                    "Access denied",
                ]

                for pattern in device_error_patterns:
                    try:
                        error_element = self.page.get_by_text(pattern, exact=False)
                        if error_element.is_visible():
                            errors["auth_error"] = "Authentication error displayed"
                            errors["error_text"] = error_element.inner_text()
                            errors["detection_method"] = "exact_device_message"
                            # Log exact match for debugging
                            print(
                                f"FOUND AUTHENTICATION ERROR: '{errors['error_text']}'"
                            )
                            return errors
                    except Exception as e:
                        print(f"Error checking pattern '{pattern}': {e}")
                        continue

                # Method 3: Check for error CSS classes (fallback)
                try:
                    error_elements = self.page.locator(
                        "[class*='error'], [class*='alert'], [class*='danger']"
                    )
                    if error_elements.count() > 0:
                        for i in range(error_elements.count()):
                            elem = error_elements.nth(i)
                            if elem.is_visible():
                                elem_text = elem.inner_text().strip()
                                if (
                                    elem_text and len(elem_text) > 0
                                ):  # Only if there's actual text content
                                    errors["auth_error"] = "Error element visible"
                                    errors["error_text"] = elem_text
                                    errors["detection_method"] = "css_class_fallback"
                                    print(f"FOUND CSS ERROR: '{elem_text}'")
                                    return errors
                except Exception as e:
                    print(f"Error checking CSS classes: {e}")

                # Method 4: Check if password field is still visible (suggests failed login)
                try:
                    password_field = self.page.get_by_placeholder("Password")
                    if password_field.is_visible():
                        # Password field visible suggests login failed
                        # Check if field appears to have been reset (cleared)
                        field_value = password_field.input_value()
                        if field_value == "":
                            errors["auth_error"] = (
                                "Password field cleared (indicates failed login)"
                            )
                            errors["detection_method"] = "field_state"
                            print("Password field cleared - likely failed login")
                            return errors
                except Exception as e:
                    print(f"Error checking password field state: {e}")

                # Method 5: Check for any error-related elements by content
                try:
                    # Look for elements containing error-related keywords
                    error_keywords = [
                        "error",
                        "failed",
                        "invalid",
                        "incorrect",
                        "wrong",
                    ]
                    page_content = self.page.content()
                    for keyword in error_keywords:
                        if keyword.lower() in page_content.lower():
                            errors["auth_error"] = f"Error keyword detected: {keyword}"
                            errors["detection_method"] = "content_scan"
                            errors["keyword"] = keyword
                            print(f"Found error keyword in page content: {keyword}")
                            return errors
                except Exception as e:
                    print(f"Error scanning page content: {e}")

            else:
                # Not on auth page - likely successful login
                return errors  # Return empty dict = no errors

        except Exception as e:
            print(f"Error checking for authentication errors: {e}")
            errors["debug_error"] = str(e)

        print("No authentication errors detected")
        return errors

    # Wrapper methods for test compatibility - Fix missing get_password_field and get_login_button
    def get_password_field(self):
        """
        Wrapper method for test compatibility - get password field locator.

        Returns:
            Locator for the password field element
        """
        try:
            # PRIMARY: Use placeholder (device has this)
            password_field = self.page.get_by_placeholder("Password")
            if password_field.count() > 0:
                return password_field.first

            # FALLBACK: Use name selector as device-specific fallback
            return self.page.locator("input[name='sts_password']").first

        except Exception as e:
            print(f"Error getting password field: {e}")
            # Return empty locator as fallback
            return self.page.locator("input[type='password']").first

    def get_login_button(self):
        """
        Wrapper method for test compatibility - get login button locator.

        Returns:
            Locator for the login/submit button element
        """
        try:
            # PRIMARY: Submit button by role
            submit_button = self.page.get_by_role("button", name="Submit")
            if submit_button.count() > 0:
                return submit_button.first

            # FALLBACK: Use type selector
            return self.page.locator("input[type='submit']").first

        except Exception as e:
            print(f"Error getting login button: {e}")
            # Return empty locator as fallback
            return self.page.locator("button").first
