"""
 Access Configuration Page Object - Pure Page Object Architecture

This  page object inherits from BasePage and provides
all methods that tests expect for access configuration.

Key Principles:
- Inherits all essential methods from BasePage
- Device-aware access capability handling
- Series-specific access validation patterns (authentication levels)
- Essential methods only - no complex validation logic
"""

from playwright.sync_api import Page, expect
from .base import BasePage
from .device_capabilities import DeviceCapabilities
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)


class AccessConfigPage(BasePage):
    """
     access configuration page with pure page object architecture.

    This class inherits all essential methods from BasePage and adds
    access-specific functionality that tests expect.
    """

    def __init__(self, page: Page, device_model: Optional[str] = None):
        super().__init__(page, device_model)

        # Initialize device capabilities and available sections like other page objects
        if self.device_model:
            self.capabilities = DeviceCapabilities.get_capabilities(self.device_model)
            self.available_sections = DeviceCapabilities.get_available_sections(
                self.device_model
            )
        else:
            self.capabilities = {}
            self.available_sections = []

        logger.info(f"AccessConfigPage initialized: {self.device_model}")

    # ========================================================================
    #  ACCESS CONFIGURATION METHODS
    # ========================================================================

    def get_access_configuration(self) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive access configuration.

        Returns:
            Dictionary with access configuration or None if not accessible
        """
        try:
            access_config = {}

            # Get password fields
            password_fields = self.page.locator("input[type='password']")
            if password_fields.count() > 0:
                password_info = []
                for i in range(password_fields.count()):
                    field = password_fields.nth(i)
                    name = field.get_attribute("name")
                    placeholder = field.get_attribute("placeholder")
                    password_info.append(
                        {
                            "name": name,
                            "placeholder": placeholder,
                            "visible": field.is_visible(),
                            "enabled": field.is_enabled(),
                        }
                    )
                access_config["password_fields"] = password_info

            # Get authentication level settings if present
            auth_fields = self.page.locator("select[name*='auth'], input[name*='auth']")
            if auth_fields.count() > 0:
                auth_info = {}
                for i in range(auth_fields.count()):
                    field = auth_fields.nth(i)
                    name = field.get_attribute("name")
                    if field.get_attribute("type") == "select-one":
                        try:
                            selected = field.locator("option:checked").text_content()
                            auth_info[name] = selected
                        except:
                            auth_info[name] = None
                    else:
                        auth_info[name] = field.input_value()
                access_config["authentication_settings"] = auth_info

            # Get session timeout settings if present
            timeout_fields = self.page.locator(
                "input[name*='timeout'], input[name*='session']"
            )
            if timeout_fields.count() > 0:
                timeout_info = {}
                for i in range(timeout_fields.count()):
                    field = timeout_fields.nth(i)
                    name = field.get_attribute("name")
                    value = field.input_value()
                    timeout_info[name] = value
                access_config["timeout_settings"] = timeout_info

            return access_config if access_config else None

        except Exception as e:
            logger.warning(f"Error getting access configuration: {e}")
            return None

    def configure_access_password(
        self, password_name: str, password_value: str
    ) -> bool:
        """
        Configure access password settings.

        Args:
            password_name: Name of the password field
            password_value: New password value

        Returns:
            True if configuration successful
        """
        try:
            # Find the password field
            password_field = self.page.locator(
                f"input[type='password'][name='{password_name}']"
            )
            if password_field.count() == 0:
                # Try alternative patterns
                password_field = self.page.locator(
                    f"input[type='password'][name*='{password_name}']"
                )

            if password_field.count() == 0:
                logger.error(f"Access password field {password_name} not found")
                return False

            # Set the password value
            if self.safe_fill(
                password_field.first,
                password_value,
                context=f"access_password_{password_name}",
            ):
                logger.info(f"Access password {password_name} configured successfully")
                return True
            else:
                logger.warning(f"Failed to configure access password {password_name}")
                return False

        except Exception as e:
            logger.error(f"Error configuring access password {password_name}: {e}")
            return False

    def configure_authentication_level(self, auth_name: str, auth_value: str) -> bool:
        """
        Configure authentication level settings.

        Args:
            auth_name: Name of the authentication field
            auth_value: Authentication level value

        Returns:
            True if configuration successful
        """
        try:
            # Find the authentication field
            auth_field = self.page.locator(f"select[name='{auth_name}']")
            if auth_field.count() == 0:
                auth_field = self.page.locator(f"input[name='{auth_name}']")

            if auth_field.count() == 0:
                logger.error(f"Authentication field {auth_name} not found")
                return False

            # Set the authentication value
            if self.safe_select_option(
                auth_field.first, auth_value, context=f"auth_level_{auth_name}"
            ):
                logger.info(f"Authentication level {auth_name} set to: {auth_value}")
                return True
            else:
                logger.warning(f"Failed to set authentication level {auth_name}")
                return False

        except Exception as e:
            logger.error(f"Error configuring authentication level {auth_name}: {e}")
            return False

    def validate_access_accessibility(self) -> bool:
        """
        Validate that access configuration is accessible and configurable.

        Returns:
            True if access is accessible and configurable
        """
        try:
            # Check for access-specific elements
            access_elements = [
                "input[type='password']",
                "select[name*='auth']",
                "input[name*='auth']",
                "h3:has-text('Access')",
                "h4:has-text('Access')",
            ]

            for selector in access_elements:
                elements = self.page.locator(selector)
                if elements.count() > 0:
                    return True

            return False

        except Exception as e:
            logger.warning(f"Error validating access accessibility: {e}")
            return False

    # ========================================================================
    # PAGE-SPECIFIC OVERRIDES
    # ========================================================================

    def verify_page_loaded(self) -> bool:
        """
        Verify that access configuration page has loaded successfully.

        Returns:
            True if verification successful
        """
        try:
            # Look for access-specific elements
            access_indicators = [
                "input[type='password']",
                "select[name*='auth']",
                "input[name*='auth']",
                "h3:has-text('Access')",
                "h4:has-text('Access')",
            ]

            for indicator in access_indicators:
                element = self.page.locator(indicator)
                if element.count() > 0:
                    logger.info("Access config page verified")
                    return True

            logger.warning(
                "Access config page verification failed - no access elements found"
            )
            return False

        except Exception as e:
            logger.error(f"Access config page verification failed: {e}")
            return False

    def navigate_to_page(self) -> bool:
        """
        Navigate to access configuration page.

        Returns:
            True if navigation successful
        """
        try:
            # Ensure we're on dashboard first
            if hasattr(self, "ensure_dashboard_context"):
                if not self.ensure_dashboard_context(
                    self.page.url.split("/")[0] + "//" + self.page.url.split("/")[2]
                ):
                    logger.warning("Could not ensure dashboard context")

            # Navigate to access section
            access_link = self.page.get_by_role("link", name="Access")
            if access_link.count() > 0:
                access_link.click()
                self.wait_for_page_load()
                return self.verify_page_loaded()
            else:
                logger.error("Access navigation link not found")
                return False

        except Exception as e:
            logger.error(f"Error navigating to access configuration page: {e}")
            return False
