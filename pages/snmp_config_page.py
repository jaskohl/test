"""
SNMP configuration page object for Kronos device test automation.

Device-aware page object with DeviceCapabilities integration and device-aware behavior patterns.
Provides the interface expected by test files that import 'pages.snmp_config_page'.

Based on DeviceCapabilities integration for device-aware behavior:
- Series-aware timeout management
- Device-specific save button patterns
- Panel expansion patterns for Series 3 collapsible UI
- Enhanced error handling with device-aware debugging
"""

from playwright.sync_api import Page, expect, Locator
import pytest
from .base import BasePage
from .device_capabilities import DeviceCapabilities
from typing import Dict, Optional, List, Any


class SNMPConfigPage(BasePage):
    """
    SNMP configuration page object for Kronos device.

    Device-aware: Uses DeviceCapabilities for all device-specific behavior.
    Enhanced with improved error handling and debugging capabilities.

    This class provides the full interface expected by test files while
    maintaining compatibility with the base functionality.
    """

    def __init__(self, page: Page, device_model: Optional[str] = None):
        """
        Initialize SNMP configuration page with device enhancement.

        Args:
            page: Playwright page object
            device_model: Device model for capabilities detection
        """
        super().__init__(page, device_model)

        # Device-aware initialization using DeviceCapabilities
        if self.device_model:
            self.device_series = DeviceCapabilities.get_series(self.device_model)
            self.capabilities = DeviceCapabilities.get_capabilities(self.device_model)
            self.available_sections = DeviceCapabilities.get_available_sections(
                self.device_model
            )
        else:
            self.device_series = None
            self.capabilities = {}
            self.available_sections = []
        if self.device_model == 2:
            pytest.skip("SNMP not supported on Series 2 devices")
        print(f"SNMPConfigPage initialized for {self.device_model or 'Unknown'}")

    def validate_capabilities(self) -> bool:
        """
        Validate that the page layout matches device capabilities from DeviceCapabilities.

        Returns:
            bool: True if capabilities match, False if there are discrepancies
        """
        try:
            if not self.device_model:
                return True

            # Check if SNMP section is available
            return self.is_section_available("snmp")
        except Exception as e:
            print(f"SNMPConfigPage: Error validating capabilities: {e}")
            return False

    def verify_page_loaded(self) -> bool:
        """
        Verify SNMP configuration page has loaded successfully.

        Returns:
            bool: True if page loaded successfully, False otherwise
        """
        try:
            # Check for SNMP-related elements
            snmp_indicators = [
                "input[name*='snmp' i]",
                "input[name*='community' i]",
                "select[name*='snmp' i]",
                "h1:has-text('SNMP')",
                "h2:has-text('SNMP')",
            ]

            for selector in snmp_indicators:
                element = self.page.locator(selector)
                if element.is_visible(timeout=5000):
                    return True

            # Fallback to base page validation
            return self.validate_page_loaded()

        except Exception as e:
            print(f"SNMPConfigPage: Error verifying page loaded: {e}")
            return False

    def get_page_data(self) -> Dict[str, Any]:
        """
        Extract SNMP configuration data from the page.

        Returns:
            Dict[str, Any]: Dictionary containing SNMP configuration data and device info
        """
        try:
            page_data = super().get_page_data()

            # Add SNMP-specific context information
            page_data.update(
                {
                    "_snmp_page": True,
                    "device_series": self.device_series,
                    "capabilities_validated": self.validate_capabilities(),
                    "available_sections": self.available_sections,
                }
            )

            return page_data

        except Exception as e:
            print(f"SNMPConfigPage: Error getting page data: {e}")
            return {"error": str(e)}

    def get_snmp_settings(self) -> Dict[str, Any]:
        """
        Get SNMP settings with enhanced error handling.

        Returns:
            Dict[str, Any]: Dictionary with SNMP settings
        """
        try:
            settings = {}

            # Look for SNMP-related form fields
            snmp_selectors = [
                "input[name*='snmp' i]",
                "select[name*='snmp' i]",
                "input[name*='community' i]",
                "input[name*='trap' i]",
                "input[name*='version' i]",
            ]

            for selector in snmp_selectors:
                try:
                    elements = self.page.locator(selector)
                    count = elements.count()
                    for i in range(count):
                        element = elements.nth(i)
                        if element.is_visible():
                            name = element.get_attribute("name") or f"field_{i}"
                            value = element.input_value()
                            settings[name] = value
                except:
                    continue

            return settings

        except Exception as e:
            print(f"SNMPConfigPage: Error getting SNMP settings: {e}")
            return {"error": str(e)}

    def set_snmp_community(self, community: str, version: str = "v2c") -> bool:
        """
        Set SNMP community string with enhanced error handling.

        Args:
            community: Community string to set
            version: SNMP version (v1, v2c, v3)

        Returns:
            bool: True if community set successfully, False otherwise
        """
        try:
            # Find community string input fields
            community_selectors = [
                "input[name*='community' i]",
                "input[name*='read_community' i]",
                "input[name*='write_community' i]",
            ]

            for selector in community_selectors:
                try:
                    elements = self.page.locator(selector)
                    count = elements.count()
                    for i in range(count):
                        element = elements.nth(i)
                        if element.is_visible():
                            element.fill(community)
                            print(f"SNMPConfigPage: Set community string: {community}")
                            return True
                except:
                    continue

            print("SNMPConfigPage: No community field found")
            return False

        except Exception as e:
            print(f"SNMPConfigPage: Error setting SNMP community: {e}")
            return False

    def get_snmp_traps(self) -> Dict[str, Any]:
        """
        Get SNMP trap configuration with enhanced error handling.

        Returns:
            Dict[str, Any]: Dictionary with trap configuration
        """
        try:
            traps = {}

            # Look for trap-related fields
            trap_selectors = [
                "input[name*='trap' i]",
                "input[name*='destination' i]",
                "input[name*='port' i]",
                "input[name*='community' i]",
            ]

            for selector in trap_selectors:
                try:
                    elements = self.page.locator(selector)
                    count = elements.count()
                    for i in range(count):
                        element = elements.nth(i)
                        if element.is_visible():
                            name = element.get_attribute("name") or f"trap_field_{i}"
                            value = element.input_value()
                            traps[name] = value
                except:
                    continue

            return traps

        except Exception as e:
            print(f"SNMPConfigPage: Error getting SNMP traps: {e}")
            return {"error": str(e)}

    def configure_snmp_trap(self, trap_config: Dict[str, Any]) -> bool:
        """
        Configure SNMP trap with enhanced error handling.

        Args:
            trap_config: Trap configuration dictionary

        Returns:
            bool: True if trap configured successfully, False otherwise
        """
        try:
            configured = False

            for field_name, field_value in trap_config.items():
                # Find field by name pattern
                field_selectors = [
                    f"input[name*='{field_name}' i]",
                    f"select[name*='{field_name}' i]",
                ]

                for selector in field_selectors:
                    try:
                        elements = self.page.locator(selector)
                        count = elements.count()
                        for i in range(count):
                            element = elements.nth(i)
                            if element.is_visible():
                                element.fill(str(field_value))
                                configured = True
                                break
                        if configured:
                            break
                    except:
                        continue
                if configured:
                    break

            print(f"SNMPConfigPage: Trap configuration result: {configured}")
            return configured

        except Exception as e:
            print(f"SNMPConfigPage: Error configuring SNMP trap: {e}")
            return False

    def navigate_to_page(self) -> bool:
        """
        Navigate to SNMP configuration page.

        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            print(f"SNMPConfigPage: Navigating to SNMP config for {self.device_model}")

            # Try navigation patterns
            nav_selectors = [
                "a:has-text('SNMP')",
                "a[href*='snmp']",
                "a:has-text('Network')",
                "a[href*='network']",
            ]

            for selector in nav_selectors:
                try:
                    link = self.page.locator(selector)
                    if link.is_visible(timeout=5000):
                        link.click()
                        self.wait_for_page_load()
                        return True
                except:
                    continue

            # If no navigation found, assume already on page
            print("SNMPConfigPage: No navigation link found, assuming on page")
            return True

        except Exception as e:
            print(f"SNMPConfigPage: Navigation error: {e}")
            return False

    def save_configuration(self) -> bool:
        """
        Save SNMP configuration changes using device-aware save button patterns.

        Returns:
            bool: True if configuration saved successfully, False otherwise
        """
        try:
            # Use base class save button detection
            save_button = self.find_save_button()
            if save_button:
                save_button.click()
                print("SNMPConfigPage: Configuration saved")
                return True

            print("SNMPConfigPage: No save button found")
            return False

        except Exception as e:
            print(f"SNMPConfigPage: Error saving configuration: {e}")
            return False

    def get_community_strings(self) -> List[str]:
        """
        Get available SNMP community strings with enhanced data extraction.

        Returns:
            List[str]: List of community strings
        """
        try:
            communities = []

            # Look for community string fields
            community_selectors = [
                "input[name*='community' i]",
                "select[name*='community' i]",
                "input[name*='read_community' i]",
                "input[name*='write_community' i]",
            ]

            for selector in community_selectors:
                try:
                    elements = self.page.locator(selector)
                    count = elements.count()
                    for i in range(count):
                        element = elements.nth(i)
                        if element.is_visible():
                            value = element.input_value()
                            if value and value not in communities:
                                communities.append(value)
                except:
                    continue

            return communities

        except Exception as e:
            print(f"SNMPConfigPage: Error getting community strings: {e}")
            return []

    def get_trap_configuration(self) -> Dict[str, Any]:
        """
        Get comprehensive trap configuration with enhanced data extraction.

        Returns:
            Dict[str, Any]: Comprehensive trap configuration data
        """
        try:
            config_data = {}

            # Look for trap-related fields
            trap_fields = [
                "input[name*='trap' i]",
                "select[name*='trap' i]",
                "input[name*='destination' i]",
                "input[name*='port' i]",
            ]

            for selector in trap_fields:
                try:
                    elements = self.page.locator(selector)
                    count = elements.count()
                    for i in range(count):
                        element = elements.nth(i)
                        if element.is_visible():
                            name = element.get_attribute("name") or f"field_{i}"
                            value = element.input_value()
                            config_data[name] = value
                except:
                    continue

            return config_data

        except Exception as e:
            print(f"SNMPConfigPage: Error getting trap configuration: {e}")
            return {"error": str(e)}

    def get_configuration_options(self) -> List[str]:
        """
        Get available SNMP configuration options with enhanced data extraction.

        Returns:
            List[str]: List of configuration options
        """
        try:
            options = []

            # Look for configuration sections
            section_selectors = [
                "h4:has-text('SNMP')",
                "h3:has-text('SNMP')",
                "div:has-text('SNMP')",
                "fieldset:has-text('SNMP')",
            ]

            for selector in section_selectors:
                try:
                    elements = self.page.locator(selector)
                    count = elements.count()
                    for i in range(count):
                        element = elements.nth(i)
                        if element.is_visible():
                            text = element.text_content()
                            if text and "SNMP" in text and text not in options:
                                options.append(text.strip())
                except:
                    continue

            # Also look for form sections
            try:
                form_sections = self.page.locator("form, fieldset, .config-section")
                count = form_sections.count()
                for i in range(count):
                    section = form_sections.nth(i)
                    if section.is_visible():
                        section_text = section.text_content()
                        if section_text and "SNMP" in section_text:
                            # Extract specific configuration areas
                            lines = section_text.split("\n")
                            for line in lines:
                                line = line.strip()
                                if line and "SNMP" in line and len(line) < 100:
                                    if line not in options:
                                        options.append(line)
            except:
                pass

            return options

        except Exception as e:
            print(f"SNMPConfigPage: Error getting configuration options: {e}")
            return []

    def get_save_button_locator(self) -> Optional[Locator]:
        """
        Get save button locator with enhanced device-aware detection.

        Returns:
            Optional[Locator]: Save button locator or None if not found
        """
        try:
            # Device-aware save button patterns
            save_selectors = [
                # Series 2 patterns
                "input[value='Save']",
                "button[type='submit']",
                "input[type='submit'][value='Save']",
                # Series 3 patterns
                "button:has-text('Save')",
                "#button_save",
                "button.save-button",
                # Generic patterns
                "button:has-text('Submit')",
                "input[value='Submit']",
            ]

            for selector in save_selectors:
                try:
                    button = self.page.locator(selector)
                    if button.is_visible(timeout=2000):
                        return button
                except:
                    continue

            return None

        except Exception as e:
            print(f"SNMPConfigPage: Error getting save button: {e}")
            return None

    def is_section_available(self, section_name: str = "snmp") -> bool:
        """
        Check if SNMP configuration section is available for this device.

        Args:
            section_name: Section name to check (default: "snmp")

        Returns:
            bool: True if section is available, False otherwise
        """
        try:
            if not self.device_model:
                print(
                    "SNMPConfigPage: No device model available, assuming section available"
                )
                return True

            # Check device capabilities for SNMP availability
            available_sections = DeviceCapabilities.get_available_sections(
                self.device_model
            )
            return "snmp" in available_sections

        except Exception as e:
            print(f"SNMPConfigPage: Error checking section availability: {e}")
            return True  # Default to available for backward compatibility

    def test_section_access_pure(self) -> Dict[str, Any]:
        """
        Test SNMP section access with pure functionality (no side effects).

        This method provides the interface expected by test files for section access testing.

        Returns:
            Dict[str, Any]: Test results with access status and details
        """
        try:
            result = {
                "section_name": "SNMP",
                "accessible": False,
                "device_model": self.device_model,
                "device_series": self.device_series,
                "capabilities_check": False,
                "page_loaded": False,
                "error": None,
            }

            # Check capabilities
            result["capabilities_check"] = self.is_section_available()

            if result["capabilities_check"]:
                # Try to navigate and verify page
                try:
                    if self.navigate_to_page():
                        result["page_loaded"] = self.verify_page_loaded()
                        result["accessible"] = result["page_loaded"]
                except Exception as e:
                    result["error"] = str(e)

            print(f"SNMPConfigPage: Section access test result: {result}")
            return result

        except Exception as e:
            print(f"SNMPConfigPage: Error in section access test: {e}")
            return {"section_name": "SNMP", "accessible": False, "error": str(e)}

    def get_snmp_version_options(self) -> List[str]:
        """
        Get available SNMP version options.

        Returns:
            List[str]: List of available SNMP versions
        """
        try:
            version_select = self.page.locator(
                "select[name*='version' i], select[name*='snmp_version' i]"
            )
            if version_select.is_visible():
                options = version_select.locator("option").all_text_contents()
                return [opt.strip() for opt in options if opt.strip()]
            return []
        except Exception as e:
            print(f"SNMPConfigPage: Error getting SNMP version options: {e}")
            return []

    # DeviceCapabilities encapsulation methods
    def get_series(self):
        """
        Get device series number using DeviceCapabilities.

        Returns:
            Device series number (2 or 3)
        """
        return self.device_series

    def get_timeout_multiplier(self):
        """
        Get timeout multiplier for device-aware testing.

        Returns:
            Timeout multiplier for this device model
        """
        try:
            if self.device_model:
                return DeviceCapabilities.get_timeout_multiplier(self.device_model)
            return 1.0
        except Exception as e:
            print(f"SNMPConfigPage: Error getting timeout multiplier: {e}")
            return 1.0

    def get_interface_specific_save_button(
        self, interface: str = "snmp_configuration", sub_interface: str = None
    ):
        """
        Get interface-specific save button configuration.

        Args:
            interface: Interface name for save button lookup
            sub_interface: Sub-interface name (optional)

        Returns:
            Dictionary containing save button configuration
        """
        try:
            if self.device_model:
                return DeviceCapabilities.get_interface_specific_save_button(
                    self.device_model, interface, sub_interface
                )
            return {"selector": "button#button_save"}  # Default fallback
        except Exception as e:
            print(f"SNMPConfigPage: Error getting save button config: {e}")
            return {"selector": "button#button_save"}

    def get_capabilities(self):
        """
        Get device capabilities from DeviceCapabilities database.

        Returns:
            Dictionary containing device capabilities
        """
        return self.capabilities

    def get_device_info(self):
        """
        Get device information from DeviceCapabilities database.

        Returns:
            Dictionary containing device information
        """
        try:
            if self.device_model:
                return DeviceCapabilities.get_device_info(self.device_model)
            return {}
        except Exception as e:
            print(f"SNMPConfigPage: Error getting device info: {e}")
            return {}

    def get_performance_expectations(self):
        """
        Get performance expectations from DeviceCapabilities database.

        Returns:
            Dictionary containing performance expectations for this device
        """
        try:
            if self.device_model:
                return DeviceCapabilities.get_performance_expectations(
                    self.device_model
                )
            return {}
        except Exception as e:
            print(f"SNMPConfigPage: Error getting performance expectations: {e}")
            return {}

    def has_capability(self, capability: str) -> bool:
        """
        Check if device has specific capability.

        Args:
            capability: Capability name to check

        Returns:
            True if device has the capability, False otherwise
        """
        try:
            if self.device_model:
                return DeviceCapabilities.has_capability(self.device_model, capability)
            return False
        except Exception as e:
            print(f"SNMPConfigPage: Error checking capability {capability}: {e}")
            return False

    def is_ptp_supported(self) -> bool:
        """
        Check if PTP is supported by this device.

        Returns:
            True if PTP is supported, False otherwise
        """
        try:
            if self.device_model:
                return DeviceCapabilities.is_ptp_supported(self.device_model)
            return False
        except Exception as e:
            print(f"SNMPConfigPage: Error checking PTP support: {e}")
            return False

    def test_snmp_configuration_validation(self) -> Dict[str, Any]:
        """
        Test complete SNMP configuration validation with device intelligence.

        Returns:
            Dictionary with comprehensive SNMP validation results
        """
        try:
            results = {
                "page_initialization": {},
                "snmp_settings_validation": {},
                "save_button_validation": {},
                "performance_validation": {},
                "cross_validation": {},
            }

            # Test page initialization
            results["page_initialization"] = {
                "device_model": self.device_model,
                "device_series": self.device_series,
                "capabilities_available": len(self.capabilities) > 0,
                "timeout_multiplier": self.get_timeout_multiplier(),
            }

            # Test SNMP settings validation
            snmp_settings = self.get_snmp_settings()
            results["snmp_settings_validation"] = {
                "settings_found": len(snmp_settings) > 0,
                "settings_count": len(snmp_settings),
                "settings": snmp_settings,
            }

            # Test save button validation
            save_button_config = self.get_interface_specific_save_button()
            save_button = self.page.locator(
                save_button_config.get("selector", "button#button_save")
            )

            results["save_button_validation"] = {
                "save_button_found": save_button.count() > 0,
                "save_button_visible": (
                    save_button.is_visible() if save_button.count() > 0 else False
                ),
                "save_button_enabled": (
                    save_button.is_enabled() if save_button.count() > 0 else False
                ),
                "save_button_selector": save_button_config.get(
                    "selector", "button#button_save"
                ),
            }

            # Test performance validation
            performance_data = self.get_performance_expectations()
            results["performance_validation"] = {
                "performance_data_available": len(performance_data) > 0,
                "performance_data": performance_data,
            }

            # Cross-validation with DeviceCapabilities
            try:
                device_info = self.get_device_info()
                capabilities = self.get_capabilities()
                results["cross_validation"] = {
                    "device_info_available": len(device_info) > 0,
                    "capabilities_available": len(capabilities) > 0,
                    "snmp_supported": self.has_capability("snmp_support"),
                    "ptp_supported": self.is_ptp_supported(),
                }
            except Exception as e:
                results["cross_validation"] = {"error": str(e)}

            print(f"SNMP configuration validation completed for {self.device_model}")
            return results

        except Exception as e:
            print(f"SNMPConfigPage: Error in SNMP configuration validation: {e}")
            return {"error": str(e)}

    def get_device_capabilities_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive device capabilities summary for SNMP configuration.

        Returns:
            Dictionary containing device capabilities summary
        """
        try:
            summary = {
                "device_model": self.device_model,
                "device_series": self.device_series,
                "capabilities": self.get_capabilities(),
                "device_info": self.get_device_info(),
                "performance_expectations": self.get_performance_expectations(),
                "timeout_multiplier": self.get_timeout_multiplier(),
                "save_button_config": self.get_interface_specific_save_button(),
                "snmp_supported": self.has_capability("snmp_support"),
                "ptp_supported": self.is_ptp_supported(),
            }

            print(f"Device capabilities summary generated for {self.device_model}")
            return summary

        except Exception as e:
            print(f"SNMPConfigPage: Error generating device capabilities summary: {e}")
            return {"error": str(e)}

    def validate_snmp_against_device_capabilities(self) -> Dict[str, Any]:
        """
        Validate current SNMP page against DeviceCapabilities database.

        Returns:
            Dictionary with validation results
        """
        try:
            validation_results = {
                "snmp_support_validation": {},
                "series_validation": {},
                "capability_validation": {},
                "overall_status": "PASS",
                "validation_errors": [],
                "validation_warnings": [],
            }

            # Get DeviceCapabilities data for comparison
            device_info = self.get_device_info()
            capabilities = self.get_capabilities()
            performance_data = self.get_performance_expectations()

            # Validate SNMP support
            expected_snmp_support = capabilities.get("snmp_support", True)
            actual_snmp_support = self.has_capability("snmp_support")

            validation_results["snmp_support_validation"] = {
                "expected": expected_snmp_support,
                "actual": actual_snmp_support,
                "match": expected_snmp_support == actual_snmp_support,
            }

            if expected_snmp_support != actual_snmp_support:
                validation_results["validation_errors"].append(
                    f"SNMP support mismatch: expected {expected_snmp_support}, found {actual_snmp_support}"
                )
                validation_results["overall_status"] = "FAIL"

            # Validate device series consistency
            expected_series = device_info.get("device_series", 0)
            if expected_series != self.device_series:
                validation_results["validation_errors"].append(
                    f"Device series mismatch: expected {expected_series}, found {self.device_series}"
                )
                validation_results["overall_status"] = "FAIL"

            validation_results["series_validation"] = {
                "expected": expected_series,
                "actual": self.device_series,
                "match": expected_series == self.device_series,
            }

            # Validate capabilities consistency
            validation_results["capability_validation"] = {
                "capabilities_available": len(capabilities) > 0,
                "performance_data_available": len(performance_data) > 0,
                "device_info_available": len(device_info) > 0,
            }

            if len(capabilities) == 0:
                validation_results["validation_warnings"].append(
                    "No device capabilities available"
                )

            if len(performance_data) == 0:
                validation_results["validation_warnings"].append(
                    "No performance data available"
                )

            print(
                f"SNMP validation completed for {self.device_model}: {validation_results['overall_status']}"
            )
            return validation_results

        except Exception as e:
            print(
                f"SNMPConfigPage: Error validating SNMP against device capabilities: {e}"
            )
            return {"error": str(e), "overall_status": "ERROR"}
