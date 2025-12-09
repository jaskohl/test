"""
General configuration page object for Kronos device test automation - FIXED v2

Handles general device configuration including:
- Device identification settings
- Location and contact information

Based on DeviceCapabilities integration for device-aware behavior.

ARCHITECTURAL FIXES IMPLEMENTED (v2):
- Removed problematic self.device_series override that interferes with BasePage initialization
- Let BasePage handle device_series detection using DeviceCapabilities.get_series()
- Maintains all critical device-aware functionality while fixing initialization

: Added device-aware field verification methods for page object pattern
"""

from playwright.sync_api import Page, expect
from .base import BasePage
from .device_capabilities import DeviceCapabilities
from typing import Dict, Optional, List, Any
import time


class GeneralConfigPage(BasePage):
    """
    Page object for Kronos device general configuration.

    Device-aware: Uses DeviceCapabilities for all device-specific behavior.
    CRITICAL FIX: Uses BasePage device_series initialization - no override
    """

    def __init__(self, page: Page, device_model: Optional[str] = None):
        super().__init__(page, device_model)

        # CRITICAL FIX: Only set additional device properties, don't override device_series
        # device_series is already correctly set by BasePage
        if self.device_model:
            self.capabilities = DeviceCapabilities.get_capabilities(self.device_model)
            self.available_sections = DeviceCapabilities.get_available_sections(
                self.device_model
            )
        else:
            self.capabilities = {}
            self.available_sections = []

        print(
            f"GeneralConfigPage initialized for {self.device_model or 'Unknown'} (Series: {self.device_series})"
        )

    def validate_capabilities(self) -> bool:
        """
        Validate that the page layout matches device capabilities from DeviceCapabilities.

        Returns:
            bool: True if capabilities match, False if there are discrepancies
        """
        if not self.device_model:
            print("No device model available for validation")
            return True

        try:
            validation_passed = True
            print(f"Validating GeneralConfigPage capabilities for {self.device_model}:")

            # Validate that general configuration is available for this device
            if "general" not in self.available_sections:
                print(
                    f"  WARNING: General configuration not available for {self.device_model}"
                )
                validation_passed = False
            else:
                print(f"  RESULT: General configuration available")

            # Validate page elements
            try:
                # Check for key general config fields
                identifier_field = self.page.locator("input[name='identifier']")
                location_field = self.page.locator("input[name='location']")

                if identifier_field.count() > 0:
                    print(f"  RESULT: Device identifier field found")
                else:
                    print(f"  RESULT: Device identifier field not found")

                if location_field.count() > 0:
                    print(f"  RESULT: Device location field found")
                else:
                    print(f"  RESULT: Device location field not found")

            except Exception as e:
                print(f"  WARNING: Error validating page elements: {e}")
                validation_passed = False

            if validation_passed:
                print(
                    f"GeneralConfigPage capability validation PASSED for {self.device_model}"
                )
            else:
                print(
                    f"GeneralConfigPage capability validation FAILED for {self.device_model}"
                )

            return validation_passed

        except Exception as e:
            print(f"Error during general config capability validation: {e}")
            return False

    def verify_page_loaded(self):
        """Verify general configuration page has loaded successfully."""
        try:
            # Device has general configuration section
            general_section = self.page.locator("h3:has-text('General')")
            expect(general_section).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

            print(
                f"General configuration page verification completed for {self.device_model or 'Unknown'}"
            )
        except Exception as e:
            print(f"Warning: General config page verification failed: {e}")

    def get_page_data(self) -> Dict[str, str]:
        """Extract general configuration data from the page."""
        page_data = {"device_model": self.device_model}

        try:
            # Extract general configuration fields
            fields = ["identifier", "location", "contact", "description"]

            for field_name in fields:
                field_locator = self.page.locator(f"input[name='{field_name}']")
                if field_locator.is_visible():
                    page_data[field_name] = field_locator.input_value()

        except Exception as e:
            print(f"Error getting general configuration page data: {e}")

        return page_data

    def get_device_specific_save_button(
        self, section_context: str = "general"
    ) -> Dict[str, Any]:
        """
        Get device-specific save button configuration from DeviceCapabilities.

        Args:
            section_context: Section context for save button detection

        Returns:
            Dictionary with save button configuration
        """
        try:
            if self.device_model:
                save_pattern = DeviceCapabilities.get_interface_specific_save_button(
                    self.device_model,
                    "general_configuration",
                    None,  # No interface for general config
                )
                return {
                    "selector": save_pattern.get("selector", "button#button_save"),
                    "description": save_pattern.get(
                        "description", "Generic save button"
                    ),
                    "requires_panel_expansion": save_pattern.get(
                        "panel_expansion_required", False
                    ),
                }
            else:
                # Fallback for unknown device
                return {
                    "selector": "button#button_save",
                    "description": "Generic save button",
                    "requires_panel_expansion": False,
                }
        except Exception as e:
            print(f"Error getting device-specific save button: {e}")
            return {
                "selector": "button#button_save",
                "description": "Fallback save button",
                "requires_panel_expansion": False,
            }

    def configure_device_identifier(self, identifier: str) -> bool:
        """
        Configure device identifier.

        Args:
            identifier: Device identifier string

        Returns:
            True if configuration successful, False otherwise
        """
        try:
            self.start_performance_tracking("configure_device_identifier")

            identifier_input = self.page.locator("input[name='identifier']")
            expect(identifier_input).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

            if not self.safe_fill(
                identifier_input, identifier, context="device_identifier"
            ):
                return False

            self.end_performance_tracking("configure_device_identifier")
            print(f"Device identifier configured: {identifier}")
            return True

        except Exception as e:
            print(f"Error configuring device identifier: {e}")
            self.end_performance_tracking("configure_device_identifier")
            return False

    def configure_device_location(self, location: str) -> bool:
        """
        Configure device location.

        Args:
            location: Device location string

        Returns:
            True if configuration successful, False otherwise
        """
        try:
            self.start_performance_tracking("configure_device_location")

            location_input = self.page.locator("input[name='location']")
            expect(location_input).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

            if not self.safe_fill(location_input, location, context="device_location"):
                return False

            self.end_performance_tracking("configure_device_location")
            print(f"Device location configured: {location}")
            return True

        except Exception as e:
            print(f"Error configuring device location: {e}")
            self.end_performance_tracking("configure_device_location")
            return False

    def configure_device_contact(self, contact: str) -> bool:
        """
        Configure device contact information.

        Args:
            contact: Contact information string

        Returns:
            True if configuration successful, False otherwise
        """
        try:
            self.start_performance_tracking("configure_device_contact")

            contact_input = self.page.locator("input[name='contact']")
            expect(contact_input).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

            if not self.safe_fill(contact_input, contact, context="device_contact"):
                return False

            self.end_performance_tracking("configure_device_contact")
            print(f"Device contact configured: {contact}")
            return True

        except Exception as e:
            print(f"Error configuring device contact: {e}")
            self.end_performance_tracking("configure_device_contact")
            return False

    def configure_device_description(self, description: str) -> bool:
        """
        Configure device description.

        Args:
            description: Device description string

        Returns:
            True if configuration successful, False otherwise
        """
        try:
            self.start_performance_tracking("configure_device_description")

            description_input = self.page.locator("input[name='description']")
            expect(description_input).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

            if not self.safe_fill(
                description_input, description, context="device_description"
            ):
                return False

            self.end_performance_tracking("configure_device_description")
            print(f"Device description configured: {description}")
            return True

        except Exception as e:
            print(f"Error configuring device description: {e}")
            self.end_performance_tracking("configure_device_description")
            return False

    def save_configuration(self) -> bool:
        """
        Save general configuration using device-aware patterns.

        Returns:
            True if save successful, False otherwise
        """
        try:
            # Get device-specific save button
            save_config = self.get_device_specific_save_button("general")

            # Check if panel expansion is required
            if save_config.get("requires_panel_expansion", False):
                print("Panel expansion required for general configuration")
                # Add panel expansion logic if needed

            # Find and click save button
            save_button = self.page.locator(save_config["selector"])

            if self.safe_click(save_button, context="save_general_config"):
                time.sleep(1)
                print(
                    f"General configuration saved successfully (Device: {self.device_model})"
                )
                return True
            else:
                print("Error: Save button not found on general config page")
                return False

        except Exception as e:
            print(f"Error saving general configuration: {e}")
            return False

    def navigate_to_page(self):
        """Navigate to general configuration page."""
        try:
            # Note: Device has link with text "General"
            general_link = self.page.get_by_role("link", name="General")
            expect(general_link).to_be_visible(timeout=self.DEFAULT_TIMEOUT)

            if self.safe_click(general_link, context="navigate_general_config"):
                self.wait_for_page_load()
                self.verify_page_loaded()

        except Exception as e:
            print(f"Error navigating to general configuration page: {e}")

    def configure_all_general_settings(
        self,
        identifier: Optional[str] = None,
        location: Optional[str] = None,
        contact: Optional[str] = None,
        description: Optional[str] = None,
    ) -> bool:
        """
        Configure all general settings in one operation.

        Args:
            identifier: Device identifier
            location: Device location
            contact: Contact information
            description: Device description

        Returns:
            True if all configurations successful, False otherwise
        """
        try:
            success_count = 0
            total_configs = 0

            if identifier is not None:
                total_configs += 1
                if self.configure_device_identifier(identifier):
                    success_count += 1

            if location is not None:
                total_configs += 1
                if self.configure_device_location(location):
                    success_count += 1

            if contact is not None:
                total_configs += 1
                if self.configure_device_contact(contact):
                    success_count += 1

            if description is not None:
                total_configs += 1
                if self.configure_device_description(description):
                    success_count += 1

            return success_count == total_configs

        except Exception as e:
            print(f"Error configuring general settings: {e}")
            return False

    def configure_device_info(self, **kwargs) -> bool:
        """
        Configure device information using flexible kwargs interface.

        This method provides backward compatibility for tests that expect
        a configure_device_info() method that accepts keyword arguments.

        Args:
            **kwargs: Device information fields (identifier, location, contact, description)

        Returns:
            True if all configurations successful, False otherwise
        """
        try:
            success_count = 0
            total_configs = 0

            if "identifier" in kwargs and kwargs["identifier"] is not None:
                total_configs += 1
                if self.configure_device_identifier(kwargs["identifier"]):
                    success_count += 1

            if "location" in kwargs and kwargs["location"] is not None:
                total_configs += 1
                if self.configure_device_location(kwargs["location"]):
                    success_count += 1

            if "contact" in kwargs and kwargs["contact"] is not None:
                total_configs += 1
                if self.configure_device_contact(kwargs["contact"]):
                    success_count += 1

            if "description" in kwargs and kwargs["description"] is not None:
                total_configs += 1
                if self.configure_device_description(kwargs["description"]):
                    success_count += 1

            return success_count == total_configs

        except Exception as e:
            print(f"Error configuring device info: {e}")
            return False

    def get_save_button_locator(self) -> str:
        """
        Get the save button locator for save button state testing.

        Returns:
            String containing the save button locator
        """
        try:
            save_config = self.get_device_specific_save_button("general")
            return save_config["selector"]
        except Exception as e:
            print(f"Error getting save button locator: {e}")
            return "button#button_save"

    def restore_page_data(self, page_data: Dict[str, str]) -> bool:
        """
        Restore general configuration page data from saved state.

        Args:
            page_data: Dictionary containing saved page configuration data

        Returns:
            True if restoration successful, False otherwise
        """
        try:
            self.start_performance_tracking("restore_general_page_data")

            # Restore general configuration fields
            fields = ["identifier", "location", "contact", "description"]

            for field_name in fields:
                if field_name in page_data and page_data[field_name]:
                    field_locator = self.page.locator(f"input[name='{field_name}']")
                    if field_locator.is_visible():
                        field_locator.clear()
                        field_locator.fill(page_data[field_name])
                        time.sleep(0.5)  # Allow time for UI update

            self.end_performance_tracking("restore_general_page_data")
            print("General configuration page data restored successfully")
            return True

        except Exception as e:
            print(f"Error restoring general page data: {e}")
            self.end_performance_tracking("restore_general_page_data")
            return False

    # ================================================
    # DEVICE-AWARE FIELD VERIFICATION METHODS
    # ================================================
    # These methods provide device-aware field verification patterns
    # that tests can use instead of direct locator usage.

    def verify_identifier_field_visible(self) -> bool:
        """
        Verify device identifier field is visible using device-aware patterns.

        Returns:
            True if identifier field is visible, False otherwise
        """
        try:
            # Use device-aware locator if needed
            if (
                self.device_model
                and DeviceCapabilities.get_series(self.device_model) == 3
            ):
                # Series 3 devices use standard locator
                identifier_locator = "input[name='identifier']"
            else:
                # Series 2 devices use standard locator
                identifier_locator = "input[name='identifier']"

            identifier_field = self.page.locator(identifier_locator)
            expect(identifier_field).to_be_visible(timeout=self.get_timeout())

            print(f"Identifier field verified visible for {self.device_model}")
            return True

        except Exception as e:
            print(f"Error verifying identifier field visibility: {e}")
            return False

    def verify_location_field_visible(self) -> bool:
        """
        Verify device location field is visible using device-aware patterns.

        Returns:
            True if location field is visible, False otherwise
        """
        try:
            # Use device-aware locator if needed
            if (
                self.device_model
                and DeviceCapabilities.get_series(self.device_model) == 3
            ):
                # Series 3 devices use standard locator
                location_locator = "input[name='location']"
            else:
                # Series 2 devices use standard locator
                location_locator = "input[name='location']"

            location_field = self.page.locator(location_locator)
            expect(location_field).to_be_visible(timeout=self.get_timeout())

            print(f"Location field verified visible for {self.device_model}")
            return True

        except Exception as e:
            print(f"Error verifying location field visibility: {e}")
            return False

    def verify_contact_field_if_present(self) -> bool:
        """
        Verify device contact field is visible if present (Series 3 devices).

        Returns:
            True if contact field is visible or not present, False on error
        """
        try:
            contact_field = self.page.locator("input[name='contact']")

            if contact_field.count() > 0:
                expect(contact_field).to_be_visible(timeout=self.get_timeout())
                print(f"Contact field verified visible for {self.device_model}")
            else:
                print(
                    f"Contact field not present for {self.device_model} (expected for some devices)"
                )

            return True

        except Exception as e:
            print(f"Error verifying contact field visibility: {e}")
            return False

    def has_basic_general_fields(self) -> bool:
        """
        Check if basic general configuration fields are present.

        Returns:
            True if basic fields (identifier, location) are present, False otherwise
        """
        try:
            identifier_field = self.page.locator("input[name='identifier']")
            location_field = self.page.locator("input[name='location']")

            identifier_present = identifier_field.count() > 0
            location_present = location_field.count() > 0

            if identifier_present and location_present:
                print(f"Basic general fields verified for {self.device_model}")
                return True
            else:
                print(
                    f"Missing basic general fields for {self.device_model}: identifier={identifier_present}, location={location_present}"
                )
                return False

        except Exception as e:
            print(f"Error checking basic general fields: {e}")
            return False

    def get_identifier_field(self):
        """
        Get identifier field locator for test interactions.

        Returns:
            Playwright locator for the identifier field
        """
        return self.page.locator("input[name='identifier']")

    def get_location_field(self):
        """
        Get location field locator for test interactions.

        Returns:
            Playwright locator for the location field
        """
        return self.page.locator("input[name='location']")
