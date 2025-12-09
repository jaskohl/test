"""
 Syslog Configuration Page Object - Pure Page Object Architecture

This  page object inherits from BasePage and provides
all methods that tests expect for syslog configuration.

Key Principles:
- Inherits all essential methods from BasePage
- Device-aware syslog capability handling
- Series-specific syslog validation patterns
- Essential methods only - no complex validation logic
"""

from playwright.sync_api import Page, expect
from .base import BasePage
from .device_capabilities import DeviceCapabilities
from typing import Dict, Optional, List, Any
import logging

logger = logging.getLogger(__name__)


class SyslogConfigPage(BasePage):
    """
     syslog configuration page with pure page object architecture.

    This class inherits all essential methods from BasePage and adds
    syslog-specific functionality that tests expect.
    """

    def __init__(self, page: Page, device_model: Optional[str] = None):
        super().__init__(page, device_model)

        logger.info(f"SyslogConfigPage initialized: {self.device_model}")

    # ========================================================================
    #  SYSLOG CONFIGURATION METHODS
    # ========================================================================

    def get_syslog_configuration(self) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive syslog configuration.

        Returns:
            Dictionary with syslog configuration or None if not accessible
        """
        try:
            syslog_config = {}

            # Get syslog server settings
            server_fields = self.page.locator(
                "input[name*='server'], input[name*='syslog']"
            )
            if server_fields.count() > 0:
                server_info = {}
                for i in range(server_fields.count()):
                    field = server_fields.nth(i)
                    name = field.get_attribute("name")
                    value = field.input_value()
                    if name:
                        server_info[name] = value
                syslog_config["server_settings"] = server_info

            # Get syslog facility settings if present
            facility_fields = self.page.locator(
                "select[name*='facility'], input[name*='facility']"
            )
            if facility_fields.count() > 0:
                facility_info = {}
                for i in range(facility_fields.count()):
                    field = facility_fields.nth(i)
                    name = field.get_attribute("name")
                    if field.get_attribute("type") == "select-one":
                        try:
                            selected = field.locator("option:checked").text_content()
                            facility_info[name] = selected
                        except:
                            facility_info[name] = None
                    else:
                        facility_info[name] = field.input_value()
                syslog_config["facility_settings"] = facility_info

            # Get syslog severity settings if present
            severity_fields = self.page.locator(
                "select[name*='severity'], input[name*='severity']"
            )
            if severity_fields.count() > 0:
                severity_info = {}
                for i in range(severity_fields.count()):
                    field = severity_fields.nth(i)
                    name = field.get_attribute("name")
                    if field.get_attribute("type") == "select-one":
                        try:
                            selected = field.locator("option:checked").text_content()
                            severity_info[name] = selected
                        except:
                            severity_info[name] = None
                    else:
                        severity_info[name] = field.input_value()
                syslog_config["severity_settings"] = severity_info

            return syslog_config if syslog_config else None

        except Exception as e:
            logger.warning(f"Error getting syslog configuration: {e}")
            return None

    def configure_syslog_server(self, server_name: str, server_value: str) -> bool:
        """
        Configure syslog server settings.

        Args:
            server_name: Name of the server field
            server_value: Server address or hostname

        Returns:
            True if configuration successful
        """
        try:
            # Find the server field
            server_field = self.page.locator(f"input[name='{server_name}']")
            if server_field.count() == 0:
                # Try alternative patterns
                server_field = self.page.locator(f"input[name*='{server_name}']")

            if server_field.count() == 0:
                logger.error(f"Syslog server field {server_name} not found")
                return False

            # Set the server value
            if self.safe_fill(
                server_field.first, server_value, context=f"syslog_server_{server_name}"
            ):
                logger.info(f"Syslog server {server_name} set to: {server_value}")
                return True
            else:
                logger.warning(f"Failed to set syslog server {server_name}")
                return False

        except Exception as e:
            logger.error(f"Error configuring syslog server {server_name}: {e}")
            return False

    def configure_syslog_facility(
        self, facility_name: str, facility_value: str
    ) -> bool:
        """
        Configure syslog facility settings.

        Args:
            facility_name: Name of the facility field
            facility_value: Facility value

        Returns:
            True if configuration successful
        """
        try:
            # Find the facility field
            facility_field = self.page.locator(f"select[name='{facility_name}']")
            if facility_field.count() == 0:
                facility_field = self.page.locator(f"input[name='{facility_name}']")

            if facility_field.count() == 0:
                logger.error(f"Syslog facility field {facility_name} not found")
                return False

            # Set the facility value
            if self.safe_select_option(
                facility_field.first,
                facility_value,
                context=f"syslog_facility_{facility_name}",
            ):
                logger.info(f"Syslog facility {facility_name} set to: {facility_value}")
                return True
            else:
                logger.warning(f"Failed to set syslog facility {facility_name}")
                return False

        except Exception as e:
            logger.error(f"Error configuring syslog facility {facility_name}: {e}")
            return False

    def validate_syslog_accessibility(self) -> bool:
        """
        Validate that syslog configuration is accessible and configurable.

        Returns:
            True if syslog is accessible and configurable
        """
        try:
            # Check for syslog-specific elements
            syslog_elements = [
                "input[name*='syslog']",
                "input[name*='server']",
                "select[name*='facility']",
                "h3:has-text('Syslog')",
                "h4:has-text('Syslog')",
            ]

            for selector in syslog_elements:
                elements = self.page.locator(selector)
                if elements.count() > 0:
                    return True

            return False

        except Exception as e:
            logger.warning(f"Error validating syslog accessibility: {e}")
            return False

    # ========================================================================
    # PAGE-SPECIFIC OVERRIDES
    # ========================================================================

    def verify_page_loaded(self) -> bool:
        """
        Verify that syslog configuration page has loaded successfully.

        Returns:
            True if verification successful
        """
        try:
            # Look for syslog-specific elements
            syslog_indicators = [
                "input[name*='syslog']",
                "input[name*='server']",
                "select[name*='facility']",
                "h3:has-text('Syslog')",
                "h4:has-text('Syslog')",
            ]

            for indicator in syslog_indicators:
                element = self.page.locator(indicator)
                if element.count() > 0:
                    logger.info("Syslog config page verified")
                    return True

            logger.warning(
                "Syslog config page verification failed - no syslog elements found"
            )
            return False

        except Exception as e:
            logger.error(f"Syslog config page verification failed: {e}")
            return False

    def navigate_to_page(self) -> bool:
        """
        Navigate to syslog configuration page.

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

            # Navigate to syslog section
            syslog_link = self.page.get_by_role("link", name="Syslog")
            if syslog_link.count() > 0:
                syslog_link.click()
                self.wait_for_page_load()
                return self.verify_page_loaded()
            else:
                logger.error("Syslog navigation link not found")
                return False

        except Exception as e:
            logger.error(f"Error navigating to syslog configuration page: {e}")
            return False
