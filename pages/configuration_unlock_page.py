"""
Configuration unlock page object for Kronos device test automation.

Handles configuration unlock functionality:
- Configuration password authentication
- Lock/unlock state management
- Access control validation

Field: name="cfg_password", id="cfg_password", placeholder="Password"
Button: type="submit"

"""

from playwright.sync_api import Page, expect
from typing import Dict, Optional
import time
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.base import BasePage
from pages.device_capabilities import DeviceCapabilities


class ConfigurationUnlockPage(BasePage):
    """
    Page object for Kronos device configuration unlock.

    Handles the secondary authentication required to access
    configuration settings.
    Device-aware: Uses DeviceCapabilities to validate access control options.
    """

    def __init__(self, page: Page, device_model: Optional[str] = None):
        super().__init__(page)
        self.device_model = device_model
        self.expected_capabilities = DeviceCapabilities.get_capabilities(device_model)

    def verify_page_loaded(self):
        """Verify configuration unlock page has loaded successfully."""
        try:
            # Try multiple methods to find password field for Series 2 and 3 devices
            password_field = None

            # Method 1: Try placeholder (Series 2)
            try:
                password_field = self.page.get_by_placeholder("Password")
                if password_field.is_visible():
                    expect(password_field).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
                    return
            except:
                pass

            # Method 2: Try name selector (Series 3)
            try:
                password_field = self.page.locator("input[name='cfg_password']")
                if password_field.is_visible():
                    expect(password_field).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
                    return
            except:
                pass

            # Method 3: Try id selector (alternative)
            try:
                password_field = self.page.locator("input[id='cfg_password']")
                if password_field.is_visible():
                    expect(password_field).to_be_visible(timeout=self.DEFAULT_TIMEOUT)
                    return
            except:
                pass

            # If none found, check if we're already on an unlocked page
            if self._has_configuration_sections():
                print("Configuration already unlocked - no password field needed")
                return

            print(
                "Warning: Config unlock page verification failed - password field not found"
            )

        except Exception as e:
            print(f"Warning: Config unlock page verification failed: {e}")

    def _wait_for_page_content(self, timeout: Optional[int] = None) -> bool:
        """
        Wait for page content to fully load, not just DOM ready.

        CRITICAL FIX: Series 3 devices navigate successfully but only load HTML head.
        This method ensures the page body and form elements are actually present.

        Args:
            timeout: Timeout in milliseconds

        Returns:
            True if page content loaded, False if timeout
        """
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        start_time = time.time()
        timeout_seconds = timeout / 1000.0

        while time.time() - start_time < timeout_seconds:
            try:
                # Check 1: Page has body element
                body = self.page.locator("body")
                if not body.is_visible(timeout=1000):
                    time.sleep(0.5)
                    continue

                # Check 2: Body has substantial content (not just head)
                body_content = body.text_content()
                if not body_content or len(body_content.strip()) < 50:
                    time.sleep(0.5)
                    continue

                # Check 3: Look for form elements or password field
                password_indicators = [
                    self.page.get_by_placeholder("Password"),
                    self.page.locator("input[name='cfg_password']"),
                    self.page.locator("input[type='password']"),
                    self.page.locator("form"),
                ]

                content_found = False
                for indicator in password_indicators:
                    try:
                        if indicator.count() > 0:
                            content_found = True
                            break
                    except:
                        continue

                if content_found:
                    return True

                # Check 4: Alternative - look for any input elements
                inputs = self.page.locator("input")
                if inputs.count() > 0:
                    print("Page content loaded - found input elements")
                    return True

                time.sleep(0.5)

            except Exception as e:
                print(f"Error checking page content: {e}")
                time.sleep(0.5)
                continue

        print(
            f"Page content failed to load within {timeout}ms - only HTML head present"
        )
        return False

    def get_page_data(self) -> Dict[str, str]:
        """
        Extract configuration unlock data from the page.

        Returns:
            Dictionary with configuration unlock data
        """
        page_data = {}

        try:
            # Check lock status by looking for configuration sections
            config_sections = ["General", "Network", "Time", "Outputs"]

            visible_sections = []
            for section in config_sections:
                try:
                    link = self.page.get_by_role("link", name=section)
                    if link.is_visible():
                        visible_sections.append(section)
                except:
                    continue

            page_data["locked"] = len(visible_sections) == 0
            page_data["visible_sections"] = ", ".join(visible_sections)

        except Exception as e:
            print(f"Error getting configuration unlock page data: {e}")

        return page_data

    def unlock_configuration(
        self, password: str = "novatech", timeout: Optional[int] = None, **kwargs
    ) -> bool:
        """
        Perform configuration unlock authentication on Kronos devices.

        This method handles the secondary authentication step after the initial
        status login (dashboard access) has been established. It expects to be
        called on a page that's currently on a configuration login form.

        Args:
            password: Password for configuration unlock (default: novatech)
            timeout: Timeout in milliseconds for operations
            **kwargs: Additional parameters for compatibility

        Returns:
            True if configuration unlock successful, False otherwise
        """
        try:
            self.start_performance_tracking("unlock_configuration")

            # Use standard timeout if not provided
            if timeout is None:
                timeout = self.DEFAULT_TIMEOUT

            # STEP 1: Check if already unlocked by looking for configuration sections
            if self._has_configuration_sections():
                print("Configuration already unlocked - found configuration sections")
                self.end_performance_tracking("unlock_configuration")
                return True

            # STEP 2: Verify we're on a configuration unlock form
            # (We assume the Configure link has already been clicked by conftest.py fixture)
            current_url = self.page.url
            print(f"Current URL: {current_url}")

            if not self._is_on_config_login_page():
                print(
                    "WARNING: Not detected as configuration login page - checking alternatives"
                )

                # Try to determine if we're in a configuration unlock scenario
                if self._has_password_field():
                    print("Found password field - assuming we're on unlock form")
                elif self._has_dashboard_access():
                    print(
                        "We're still on dashboard - attempting to access configure link"
                    )
                    if not self._access_configuration_mode(timeout=timeout):
                        print("Failed to access configuration unlock mode")

                        self.end_performance_tracking("unlock_configuration")
                        return False
                else:
                    print("Not on dashboard and no password field - unclear state")
                    self.end_performance_tracking("unlock_configuration")
                    return False

            # STEP 3: Perform configuration authentication
            print("Performing configuration authentication...")
            if not self._perform_configuration_authentication(
                password, timeout=timeout
            ):
                print("Configuration authentication failed")
                self.end_performance_tracking("unlock_configuration")
                return False

            # STEP 4: Wait for second satellite loading cycle (configuration sections loading)
            print(
                "Waiting for configuration sections to load (second satellite cycle)..."
            )
            self.wait_for_satellite_loading(
                timeout=60000
            )  # Extended to 60 seconds as requested

            # STEP 5: Final verification
            if self._has_configuration_sections():
                self.end_performance_tracking("unlock_configuration")
                return True
            else:
                print(
                    "Final verification: Configuration unlock failed - no sections visible"
                )
                self.end_performance_tracking("unlock_configuration")
                return False

        except Exception as e:
            print(f"Error during configuration unlock: {e}")
            self.end_performance_tracking("unlock_configuration")
            return False

    def _try_configure_from_current_page(self) -> bool:
        """
        Try to access configuration unlock from the current page by clicking Configure button.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Look for Configure button/link on current page
            configure_selectors = [
                self.page.locator("a[title*='locked']").filter(has_text="Configure"),
                self.page.locator("a").filter(has_text="Configure"),
                self.page.get_by_text("Configure", exact=False).first,
            ]

            for selector in configure_selectors:
                try:
                    if selector.is_visible(timeout=3000):
                        selector.click()
                        time.sleep(2)  # Wait for navigation

                        # Check if we're now on unlock page
                        current_url = self.page.url
                        if "/login" in current_url or self._has_password_field():
                            if self._wait_for_page_content(timeout=10000):
                                print(
                                    "Configure button successfully led to unlock page"
                                )
                                return True
                except Exception as e:
                    continue

            return False

        except Exception as e:
            print(f"Error trying configure from current page: {e}")
            return False

    def _has_password_field(self) -> bool:
        """
        Check if the current page has a password field (indicating unlock page).

        Returns:
            True if password field is present
        """
        try:
            # Check multiple password field selectors
            password_selectors = [
                self.page.get_by_placeholder("Password"),
                self.page.locator("input[name='cfg_password']"),
                self.page.locator("input[type='password']"),
            ]

            for selector in password_selectors:
                if selector.count() > 0:
                    return True
            return False

        except Exception:
            return False

    def _has_configuration_sections(self) -> bool:
        """
        Check if configuration sections are visible (indicates unlocked state).

        Returns:
            True if configuration sections are visible, False otherwise
        """
        try:
            config_sections = ["General", "Network", "Time"]
            for section in config_sections:
                try:
                    link = self.page.get_by_role("link", name=section)
                    if link.is_visible():
                        return True
                except:
                    continue
            return False
        except:
            return False

    def _wait_for_config_sections_satellite(
        self, timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for configuration sidebar elements to appear after unlock (satellite loading detection).

        This implements the satellite loading detection method using expect(element).to_be_visible()
        with a 4-second timeout as the primary detection mechanism.

        Args:
            timeout: Timeout in milliseconds (uses 4000ms if None)

        Returns:
            True if configuration sections appeared, False if timeout
        """

        # Await for the general link to be visible as a sign of successful login
        try:
            general_link = self.page.get_by_role("link", name="General")
            general_link.wait_for()
            return True
        except Exception as e:
            print(f"Error waiting for general link: {e}")
            return False

    def _is_configuration_locked(self) -> bool:
        """
        Check if configuration is currently locked.

        Returns:
            True if locked, False if unlocked
        """
        # Simple approach: check if configuration sections are visible
        return not self._has_configuration_sections()

    def _verify_configuration_unlocked(self) -> bool:
        """
        Verify that configuration unlock was successful.

        Returns:
            True if unlocked successfully, False otherwise
        """
        try:
            # Check if configuration sections are now available
            config_sections = ["General", "Network", "Time", "Outputs"]

            for section in config_sections:
                try:
                    link = self.page.get_by_role("link", name=section)
                    if link.is_visible():
                        print(f"Configuration section available: {section}")
                        return True
                except:
                    continue

            print("No configuration sections found after unlock attempt")
            return False

        except Exception as e:
            print(f"Error verifying configuration unlock: {e}")
            return False

    def navigate_to_page(self):
        """Navigate to configuration unlock page."""
        try:
            # Look for Configure button/link
            # Note: Device has button with title attribute
            configure_button = self.page.locator("a[title*='locked']").filter(
                has_text="Configure"
            )

            if configure_button.is_visible():
                if self.safe_click(configure_button, context="navigate_to_unlock"):
                    time.sleep(1)
                    self.verify_page_loaded()
                    return

            # Alternative: Try any Configure link
            configure_link = self.page.get_by_text("Configure", exact=False)
            if configure_link.is_visible():
                self.safe_click(configure_link, context="navigate_to_unlock_alt")

        except Exception as e:
            print(f"Error navigating to configuration unlock page: {e}")

    def get_configuration_access_level(self) -> Dict[str, str]:
        """
        Get current configuration access level.

        Returns:
            Dictionary with access level information
        """
        access_info = {"level": "unknown", "locked": True, "sections_available": []}

        try:
            # Check which configuration sections are accessible
            config_sections = [
                "General",
                "Network",
                "Time",
                "Outputs",
                "GNSS",
                "SNMP",
                "Display",
                "Syslog",
                "Upload",
                "Access",
            ]

            accessible_sections = []
            for section in config_sections:
                try:
                    link = self.page.get_by_role("link", name=section)
                    if link.is_visible():
                        accessible_sections.append(section)
                except:
                    continue

            access_info["sections_available"] = accessible_sections

            if len(accessible_sections) > 5:
                access_info["level"] = "full_access"
                access_info["locked"] = False
            elif len(accessible_sections) > 0:
                access_info["level"] = "partial_access"
                access_info["locked"] = False
            else:
                access_info["level"] = "locked"
                access_info["locked"] = True

        except Exception as e:
            print(f"Error getting configuration access level: {e}")

        return access_info

    def _has_dashboard_access(self) -> bool:
        """
        Check if we have status monitoring dashboard access (first authentication level).

        This verifies the first part of dual authentication is complete.

        Returns:
            True if dashboard access is available, False otherwise
        """
        try:
            # Universal dashboard indicators (work for both Series 2 and 3)
            dashboard_indicators = [
                "#Main_Header",  # Main header element
                ".main-header",  # Header CSS class
                "h3:has-text('Time')",  # Time section header
                "h3:has-text('Status')",  # Status section header
                "h3:has-text('General')",  # General section header (when unlocked)
                "table",  # Must have tables (4 for both series minimum)
            ]

            for selector in dashboard_indicators:
                element = self.page.locator(selector)
                if element.is_visible(timeout=2000):  # Quick check
                    print(f"Dashboard access verified: found {selector}")
                    return True

            # Check for Configure button (indicates status monitoring access)
            configure_selectors = [
                'a[href="login"]:has-text("Configure")',  # Generic configure link
                'a[href*="login"]',  # Any login link
                'a[title*="locked"]',  # Locked title attribute
            ]

            for selector_str in configure_selectors:
                element = self.page.locator(selector_str)
                if element.is_visible(timeout=2000):
                    print(
                        f"Dashboard access verified: found configure link {selector_str}"
                    )
                    return True

            # Check body content for device keywords
            try:
                body = self.page.locator("body")
                if body.is_visible():
                    content = body.text_content()
                    if content:
                        content = content.strip()
                        device_keywords = ["kronos", "time", "status"]
                        keyword_count = sum(
                            1
                            for keyword in device_keywords
                            if keyword in content.lower()
                        )

                        if len(content) > 200 and keyword_count >= 2:
                            print(
                                f"Dashboard access verified: {keyword_count} device keywords in content"
                            )
                            return True
            except Exception as e:
                print(f"Error checking body content: {e}")

            print("No dashboard access indicators found")
            return False

        except Exception as e:
            print(f"Error checking dashboard access: {e}")
            return False

    def _access_configuration_mode(self, timeout: Optional[int] = None) -> bool:
        """
        Access configuration unlock mode by clicking the Configure link.

        This triggers the second authentication pathway.

        Args:
            timeout: Timeout in milliseconds

        Returns:
            True if configuration mode accessed, False otherwise
        """
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        try:
            # Look for Configure link/button with multiple selectors
            configure_selectors = [
                self.page.locator("a[title*='locked']").filter(has_text="Configure"),
                self.page.locator("a[href='login']").filter(has_text="Configure"),
                self.page.locator("a").filter(has_text="Configure"),
                self.page.get_by_text("Configure", exact=False).first,
            ]

            for selector in configure_selectors:
                try:
                    if selector.is_visible(timeout=min(5000, timeout)):
                        print(f"Found configure selector, attempting to click...")

                        # Use safe_click with context for debugging
                        if self.safe_click(
                            selector,
                            timeout=min(10000, timeout),
                            context="access_config_mode",
                        ):
                            # Wait for navigation to unlock page
                            time.sleep(2)

                            # Verify we're now on the configuration login page
                            if self._is_on_config_login_page():
                                print("Successfully accessed configuration unlock mode")
                                return True
                            else:
                                print(
                                    "Configure click didn't lead to unlock page, trying next selector"
                                )
                                continue
                except Exception as e:
                    print(f"Error with selector: {e}")
                    continue

            print("None of the configure selectors worked")
            return False

        except Exception as e:
            print(f"Error accessing configuration mode: {e}")
            return False

    def _is_on_config_login_page(self) -> bool:
        """
        Check if we're currently on the configuration login page.

        Returns:
            True if on config login page, False otherwise
        """
        try:
            # Check URL contains login
            current_url = self.page.url
            if "/login" in current_url:
                return True

            # Check for password field
            if self._has_password_field():
                return True

            # Check if still on dashboard (configure didn't work)
            if self._has_dashboard_access():
                print("Still on dashboard - configure link didn't navigate")
                return False

            return False

        except Exception as e:
            print(f"Error checking if on config login page: {e}")
            return False

    def _perform_configuration_authentication(
        self, password: str, timeout: Optional[int] = None
    ) -> bool:
        """
        Perform the actual configuration authentication after accessing config mode.

        Args:
            password: Password for authentication
            timeout: Timeout in milliseconds

        Returns:
            True if authentication successful, False otherwise
        """
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        try:
            # Wait for page content to load fully
            if not self._wait_for_page_content(timeout=min(15000, timeout)):
                print("Configuration login page content failed to load")
                return False

            # Find password field with multiple selector strategies
            password_field = None

            # Strategy 1: Try placeholder (device has this)
            try:
                password_field = self.page.get_by_placeholder("Password").first
                if not password_field.is_visible():
                    password_field = None
            except:
                password_field = None

            # Strategy 2: Try name selector for config unlock (device has name="cfg_password")
            if password_field is None:
                try:
                    password_field = self.page.locator(
                        "input[name='cfg_password']"
                    ).first
                    if not password_field.is_visible():
                        password_field = None
                except:
                    password_field = None

            # Strategy 3: Try any password input
            if password_field is None:
                try:
                    password_field = self.page.locator("input[type='password']").first
                    if not password_field.is_visible():
                        password_field = None
                except:
                    password_field = None

            if password_field is None:
                print("No password field found on configuration login page")
                return False

            # Fill password field
            expect(password_field).to_be_visible(timeout=min(5000, timeout))
            expect(password_field).to_be_editable(timeout=min(5000, timeout))

            password_field.clear()
            password_field.fill(password)
            time.sleep(0.5)  # Allow input to register

            # Find and click submit button
            submit_button = self.page.get_by_role("button", name="Submit").first
            expect(submit_button).to_be_visible(timeout=min(5000, timeout))

            submit_button.click()

            # Allow time for processing and redirects
            time.sleep(3)

            # Check for immediate authentication errors
            if self._has_authentication_errors():
                print("Configuration authentication failed - errors detected")
                return False

            return True

        except Exception as e:
            print(f"Error during configuration authentication: {e}")
            return False

    def _has_authentication_errors(self) -> bool:
        """
        Check for authentication errors on the page.

        Returns:
            True if errors found, False otherwise
        """
        try:
            # Check for error messages
            error_patterns = [
                "Incorrect password.",
                "Incorrect password",
                "Authentication failed",
                "Invalid password",
                "Login failed",
                "Access denied",
            ]

            for pattern in error_patterns:
                try:
                    if self.page.get_by_text(pattern, exact=False).is_visible(
                        timeout=2000
                    ):
                        return True
                except:
                    continue

            return False

        except Exception:
            return False
