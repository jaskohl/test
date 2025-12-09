"""
Simplified Time Configuration Page Object - Device-Intelligent Architecture

This page object follows the page-object-based/device-intelligent architecture:
- Encapsulates DeviceCapabilities calls internally (tests never call DeviceCapabilities directly)
- Provides essential methods only
- Handles device differences internally
- Uses simple, focused UI operations

Locator Strategy:
- PRIMARY (EXCELLENT): page.get_by_role() with .first to prevent multiple matches
- SECONDARY (GOOD): page.locator("a").filter(has_text=...)
- FALLBACK (ACCEPTABLE): CSS selectors when semantic approaches fail
  - Document all fallback usage with inline comments

Critical Navigation Fix:
- Replaced ambiguous a[href*='time'] with proper role-based locator
- Added .first to prevent strict mode violations from multiple matches
"""

from playwright.sync_api import Page, expect
from .base import BasePage
from .device_capabilities import DeviceCapabilities
from typing import Dict, Optional, Any
import time
import logging

logger = logging.getLogger(__name__)


class TimeConfigPage(BasePage):
    """
    Simplified time configuration page object.

    Essential methods only - device intelligence is encapsulated internally.
    Tests use only page object methods, never DeviceCapabilities directly.
    """

    def __init__(self, page: Page, device_model: Optional[str] = None):
        super().__init__(page, device_model)
        # CRITICAL FIX: Don't override self.device_model - BasePage already sets it
        # self.device_model = device_model  <-- REMOVED: This breaks proper inheritance

        # Device intelligence encapsulated internally
        self.device_series = (
            DeviceCapabilities.get_series(device_model) if device_model else 0
        )
        self.timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(
            self.device_model
        )

        logger.info(
            f"TimeConfigPage initialized: {device_model} (Series {self.device_series})"
        )

    def navigate_to_page(self):
        """Navigate to time configuration page."""
        try:
            # PRIMARY (EXCELLENT) - Use role-based locator with .first
            # Note: Using get_by_role as primary - Time link has semantic role
            time_config_link = self.page.get_by_role("link", name="Time").first
            if time_config_link.count() > 0:
                time_config_link.click()
            else:
                # FALLBACK - Role-based locator not available
                # Note: Using text filtering as fallback - Time link lacks proper role
                time_config_link = self.page.locator("a").filter(has_text="Time").first
                if time_config_link.count() > 0:
                    time_config_link.click()
                else:
                    # FINAL FALLBACK - Document why CSS selector is needed
                    # Note: Using CSS selector as fallback - embedded device UI lacks semantic attributes
                    time_config_link = self.page.locator("a[href*='time']").first
                    if time_config_link.count() > 0:
                        time_config_link.click()
                    else:
                        raise Exception("Time configuration link not found")

            # Device-aware wait
            self.page.wait_for_load_state(
                "networkidle", timeout=int(10000 * self.timeout_multiplier)
            )
            logger.info("Navigated to time configuration page")

        except Exception as e:
            logger.error(f"Error navigating to time config page: {e}")
            raise

    def verify_page_loaded(self):
        """Verify time configuration page loaded successfully."""
        try:
            # Device-aware timeout
            verification_timeout = int(self.DEFAULT_TIMEOUT * self.timeout_multiplier)

            if self.device_series == 2:
                # Series 2: Simple timezone select
                timezone_select = self.page.locator("select[name='timezones']")
                expect(timezone_select).to_be_visible(timeout=verification_timeout)
                logger.info("Series 2: Time config page verified")

            elif self.device_series == 3:
                # Series 3: Check for timezone collapse element
                timezone_collapse = self.page.locator("#timezone_collapse")
                if timezone_collapse.count() > 0:
                    logger.info("Series 3: Time config page verified")
                else:
                    logger.warning("Series 3: Timezone collapse element not found")

        except Exception as e:
            logger.error(f"Time config page verification failed: {e}")
            raise

    def select_timezone(self, timezone_value: str) -> bool:
        """
        Select timezone from dropdown.

        Args:
            timezone_value: Timezone to select

        Returns:
            True if selection successful
        """
        try:
            # Ensure timezone panel is expanded for Series 3
            if self.device_series == 3:
                self._ensure_timezone_panel_expanded()

            # Select timezone
            timezone_field = self.page.locator("select[name='timezones']")
            if timezone_field.count() == 0:
                logger.error("Timezone field not found")
                return False

            # Use safe select method from base page
            success = self.safe_select_option(
                timezone_field.first, timezone_value, context="timezone"
            )

            if success:
                logger.info(f"Timezone selected: {timezone_value}")
            else:
                logger.warning(f"Failed to select timezone: {timezone_value}")

            return success

        except Exception as e:
            logger.error(f"Error selecting timezone: {e}")
            return False

    def get_available_timezones(self) -> list:
        """Get list of available timezones."""
        try:
            timezone_field = self.page.locator("select[name='timezones']")
            if timezone_field.count() == 0:
                return []

            options = timezone_field.first.locator("option")
            count = options.count()

            timezones = []
            for i in range(count):
                value = options.nth(i).get_attribute("value")
                if value:
                    timezones.append(value)

            return timezones

        except Exception as e:
            logger.error(f"Error getting available timezones: {e}")
            return []

    def configure_dst(self, dst_enabled: bool, dst_name: str = "") -> bool:
        """
        Configure DST settings.

        Args:
            dst_enabled: Whether to enable DST
            dst_name: DST name (optional)

        Returns:
            True if configuration successful
        """
        try:
            # Ensure DST panel is expanded for Series 3
            if self.device_series == 3:
                self._ensure_dst_panel_expanded()

            success_count = 0

            # Enable/disable DST checkbox
            dst_checkbox = self.page.locator("input[name='dst_enable']")
            if dst_checkbox.count() > 0:
                if dst_enabled and not dst_checkbox.first.is_checked():
                    dst_checkbox.first.click()
                    success_count += 1
                elif not dst_enabled and dst_checkbox.first.is_checked():
                    dst_checkbox.first.click()
                    success_count += 1

            # Set DST name if provided
            if dst_name:
                dst_name_field = self.page.locator("input[name='dst_name']")
                if dst_name_field.count() > 0:
                    if self.safe_fill(
                        dst_name_field.first, dst_name, context="dst_name"
                    ):
                        success_count += 1

            logger.info(f"DST configuration: {success_count} fields set")
            return success_count > 0

        except Exception as e:
            logger.error(f"Error configuring DST: {e}")
            return False

    def get_dst_rules(self) -> list:
        """Get list of available DST rules."""
        try:
            dst_rule_field = self.page.locator("select[name='dst_rule']")
            if dst_rule_field.count() == 0:
                return []

            options = dst_rule_field.first.locator("option")
            count = options.count()

            rules = []
            for i in range(count):
                text = options.nth(i).inner_text()
                if text:
                    rules.append(text)

            return rules

        except Exception as e:
            logger.error(f"Error getting DST rules: {e}")
            return []

    def select_dst_rule(self, rule_name: str) -> bool:
        """Select DST rule from dropdown."""
        try:
            dst_rule_field = self.page.locator("select[name='dst_rule']")
            if dst_rule_field.count() == 0:
                logger.error("DST rule field not found")
                return False

            success = self.safe_select_option(
                dst_rule_field.first, rule_name, context="dst_rule"
            )

            if success:
                logger.info(f"DST rule selected: {rule_name}")

            return success

        except Exception as e:
            logger.error(f"Error selecting DST rule: {e}")
            return False

    def save_configuration(self) -> bool:
        """Save time configuration."""
        try:
            save_button = self._get_save_button()
            if save_button.count() == 0:
                logger.error("Save button not found")
                return False

            save_button.first.click()

            # Device-aware wait for save operation
            self.page.wait_for_load_state(
                "networkidle", timeout=int(10000 * self.timeout_multiplier)
            )

            logger.info("Time configuration saved")
            return True

        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False

    def get_current_timezone(self) -> str:
        """Get currently selected timezone."""
        try:
            timezone_field = self.page.locator("select[name='timezones']")
            if timezone_field.count() > 0:
                selected_option = timezone_field.first.locator("option:checked")
                if selected_option.count() > 0:
                    return selected_option.first.get_attribute("value") or ""
            return ""

        except Exception as e:
            logger.error(f"Error getting current timezone: {e}")
            return ""

    def is_dst_enabled(self) -> bool:
        """Check if DST is currently enabled."""
        try:
            dst_checkbox = self.page.locator("input[name='dst_enable']")
            if dst_checkbox.count() > 0:
                return dst_checkbox.first.is_checked()
            return False

        except Exception as e:
            logger.error(f"Error checking DST status: {e}")
            return False

    def get_save_button(self):
        """Get save button locator (public method for tests)."""
        return self._get_save_button()

    # Internal methods - device intelligence encapsulated

    def _ensure_timezone_panel_expanded(self) -> bool:
        """Ensure timezone panel is expanded (Series 3 only)."""
        if self.device_series != 3:
            return True

        try:
            collapse_element = self.page.locator("#timezone_collapse")
            if collapse_element.count() == 0:
                logger.warning("Timezone collapse element not found")
                return False

            # Check if already expanded
            class_attr = collapse_element.first.get_attribute("class") or ""
            is_expanded = "in" in class_attr or "show" in class_attr

            if not is_expanded:
                # Find and click expansion link
                panel_link = self.page.locator("a[href='#timezone_collapse']").first
                if panel_link.count() == 0:
                    panel_link = self.page.locator(
                        "a[data-toggle='collapse'][href='#timezone_collapse']"
                    ).first

                if panel_link.count() > 0:
                    panel_link.click()
                    time.sleep(0.5)  # Allow UI to update
                    logger.info("Timezone panel expanded")
                else:
                    logger.error("Timezone panel expansion link not found")
                    return False

            return True

        except Exception as e:
            logger.error(f"Error expanding timezone panel: {e}")
            return False

    def _ensure_dst_panel_expanded(self) -> bool:
        """Ensure DST panel is expanded (Series 3 only)."""
        if self.device_series != 3:
            return True

        try:
            collapse_element = self.page.locator("#dst_collapse")
            if collapse_element.count() == 0:
                logger.warning("DST collapse element not found")
                return False

            # Check if already expanded
            class_attr = collapse_element.first.get_attribute("class") or ""
            is_expanded = "in" in class_attr or "show" in class_attr

            if not is_expanded:
                # Find and click expansion link
                panel_link = self.page.locator("a[href='#dst_collapse']").first
                if panel_link.count() == 0:
                    panel_link = self.page.locator(
                        "a[data-toggle='collapse'][href='#dst_collapse']"
                    ).first

                if panel_link.count() > 0:
                    panel_link.click()
                    time.sleep(0.5)  # Allow UI to update
                    logger.info("DST panel expanded")
                else:
                    logger.error("DST panel expansion link not found")
                    return False

            return True

        except Exception as e:
            logger.error(f"Error expanding DST panel: {e}")
            return False

    def _get_save_button(self):
        """Get device-aware save button locator."""
        try:
            # Get device-specific save button pattern
            save_button_info = DeviceCapabilities.get_interface_specific_save_button(
                self.device_model or "Unknown_Device", "time_configuration"
            )

            if save_button_info and "selector" in save_button_info:
                save_button = self.page.locator(save_button_info["selector"])
                if save_button.count() > 0:
                    return save_button

            # Fallback patterns
            if self.device_series == 3:
                save_button = self.page.locator("button#button_save")
            else:
                save_button = self.page.locator("input#button_save")

            if save_button.count() > 0:
                return save_button

            # Final fallback
            return self.page.get_by_role("button", name="Save").first

        except Exception as e:
            logger.error(f"Error getting save button: {e}")
            return self.page.get_by_role("button", name="Save").first
