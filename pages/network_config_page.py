"""
Network configuration page object - DeviceCapabilities

 network configuration page with comprehensive DeviceCapabilities integration.

Key Enhancements:
- Device-aware multi-interface support for Series 3
- Interface-specific panel expansion patterns
- Device-aware timeout management with timeout multipliers
- Series-specific network configuration handling
- Comprehensive capability validation
- Network interface targeting for Series 3 PTP interfaces

Based on device_capabilities.py integration requirements
"""

from playwright.sync_api import Page, expect
from .base import BasePage
from .device_capabilities import DeviceCapabilities
from typing import Dict, Optional, List, Any
import re
import time
import logging

logger = logging.getLogger(__name__)


class NetworkConfigPage(BasePage):
    """
     network configuration page with DeviceCapabilities integration.

    Handles network configuration for ALL Kronos device variants:
    - Series 2: Single network interface, dual network modes
    - Series 3: Multi-interface support with PTP capabilities
    - Device-aware timeout management and interface targeting
    - Comprehensive capability validation
    """

    def __init__(self, page: Page, device_model: Optional[str] = None):
        super().__init__(page, device_model)
        self.capabilities = (
            DeviceCapabilities.get_capabilities(device_model) if device_model else {}
        )
        self.ptp_interfaces = (
            DeviceCapabilities.get_ptp_interfaces(device_model) if device_model else []
        )
        self.network_interfaces = (
            DeviceCapabilities.get_network_interfaces(device_model)
            if device_model
            else []
        )

        # Initialize form state tracking
        self._form_state = {
            "initialized": False,
            "panels_expanded": set(),
            "elements_visible": False,
        }

        logger.info(f"NetworkConfigPageDevice initialized: {device_model}")
        logger.info(
            f"  Series: {self.device_series}, Timeout multiplier: {self.timeout_multiplier}x"
        )
        logger.info(f"  Network interfaces: {self.network_interfaces}")
        logger.info(f"  PTP interfaces: {self.ptp_interfaces}")

    def validate_capabilities(self) -> bool:
        """
        Validate network capabilities against DeviceCapabilities database.

         validation comparing expected network capabilities (from device database)
        against actual detected capabilities to ensure database accuracy.

        Returns:
            bool: True if capabilities match, False if there are discrepancies
        """
        if not self.device_model or not self.capabilities:
            logger.warning("No device model or capabilities available for validation")
            return True

        try:
            validation_passed = True
            actual_capabilities = self.detect_device_capabilities()

            logger.info(f"Validating {self.device_model} network capabilities:")

            # Validate Series 2 vs Series 3 network capabilities
            expected_series = 2 if self.device_model.startswith("KRONOS-2") else 3
            if expected_series != self.device_series:
                logger.warning(
                    f"  Series mismatch - expected {expected_series}, detected {self.device_series}"
                )

            # Validate network interface count
            expected_network_interfaces = self.capabilities.get(
                "network_config", {}
            ).get("interfaces", [])
            if expected_network_interfaces:
                expected_count = len(expected_network_interfaces)
                actual_interfaces = actual_capabilities.get("available_interfaces", [])
                actual_count = len(actual_interfaces)

                logger.info(
                    f"  Expected {expected_count} interfaces, detected {actual_count}"
                )

                if expected_count != actual_count:
                    logger.warning(
                        f"   Network interface count mismatch: expected {expected_count}, got {actual_count}"
                    )
                    validation_passed = False
                else:
                    logger.info(
                        "   Network interface count matches expected capabilities"
                    )

            # Validate PTP interface availability for Series 3
            if self.device_series == 3 and self.ptp_interfaces:
                expected_ptp_interfaces = set(self.ptp_interfaces)
                actual_ptp_interfaces = set(
                    actual_capabilities.get("ptp_capable_interfaces", [])
                )

                if not expected_ptp_interfaces.issubset(actual_ptp_interfaces):
                    missing_ptp = expected_ptp_interfaces - actual_ptp_interfaces
                    logger.warning(f"   Missing PTP interfaces: {missing_ptp}")
                    validation_passed = False

            if validation_passed:
                logger.info(f"   Network capability validation PASSED")
            else:
                logger.warning(
                    f"   Network capability validation FAILED - some mismatches detected"
                )

            return validation_passed

        except Exception as e:
            logger.error(f"Error during network capability validation: {e}")
            return False

    def detect_device_capabilities(self) -> Dict[str, Any]:
        """
        Detect actual network capabilities from the page with device-aware patterns.

         detection with device-aware loading protection and comprehensive validation.

        Returns:
            Dictionary with actual device network capabilities
        """
        try:
            capabilities = {
                "device_series": self.device_series,
                "has_mode_select": False,
                "has_dual_network": False,
                "has_bonding_modes": False,
                "has_multi_form": False,
                "has_sfp_mode": False,
                "has_ptp_per_port": False,
                "available_interfaces": [],
                "ptp_capable_interfaces": [],
                "ethernet_ports": [],
            }

            if self.device_series == 2:
                # Series 2: Single network interface with dual modes
                capabilities.update(
                    {
                        "has_mode_select": True,
                        "has_dual_network": True,
                        "has_bonding_modes": True,
                        "ethernet_ports": ["single_mode"],
                        "available_interfaces": ["single_mode"],
                    }
                )

                # Validate mode select presence
                mode_select = self.page.locator("select[name='mode']")
                if mode_select.count() > 0:
                    logger.info("Series 2: Mode select found")
                else:
                    logger.warning("Series 2: Mode select not found (unexpected)")

            elif self.device_series == 3:
                # Series 3: Multi-interface support with PTP
                capabilities.update(
                    {
                        "has_multi_form": True,
                        "has_sfp_mode": True,
                        "has_ptp_per_port": True,
                    }
                )

                # Detect available network interfaces
                available_interfaces = self._query_available_interfaces()
                capabilities["ethernet_ports"] = available_interfaces
                capabilities["available_interfaces"] = available_interfaces

                # Identify PTP-capable interfaces
                ptp_capable = []
                for interface in available_interfaces:
                    if interface in self.ptp_interfaces:
                        ptp_capable.append(interface)
                capabilities["ptp_capable_interfaces"] = ptp_capable

                logger.info(
                    f"Series 3: Detected {len(available_interfaces)} interfaces, {len(ptp_capable)} PTP-capable"
                )

            return capabilities

        except Exception as e:
            logger.error(f"Error detecting network capabilities: {e}")
            return {
                "device_series": self.device_series,
                "available_interfaces": [],
                "error": str(e),
            }

    def _query_available_interfaces(self) -> List[str]:
        """
        Query actual available network interfaces with device-aware loading protection.

         version with comprehensive loading protection and timeout management.

        Returns:
            List of interface names found on this device
        """
        try:
            available_interfaces = []

            # Use device-aware timeout
            detection_timeout = int(self.DEFAULT_TIMEOUT * self.timeout_multiplier)

            # Query for known interface patterns
            interface_patterns = [
                "input[name='ip_eth0']",
                "input[name='ip_eth1']",
                "input[name='ip_eth2']",
                "input[name='ip_eth3']",
                "input[name='ip_eth4']",
            ]

            logger.info("Device-aware interface detection starting...")

            # Initial scan - query all possible interfaces
            for pattern in interface_patterns:
                locator = self.page.locator(pattern)
                if locator.count() > 0:
                    match = re.search(r"ip_(eth\d+)", pattern)
                    if match:
                        interface = match.group(1)
                        available_interfaces.append(interface)
                        logger.info(f"Found interface: {interface}")

            # PROTECT AGAINST FALSE NEGATIVES: Device-aware loading protection
            if len(available_interfaces) <= 1:
                logger.info(
                    "Only found 1 or fewer interfaces - applying device-aware loading protection..."
                )

                # Extended wait for full page load
                self.wait_for_page_load(timeout=detection_timeout)
                time.sleep(2)  # Additional buffer for embedded device timing

                # Re-scan after full load
                available_interfaces = []
                for pattern in interface_patterns:
                    locator = self.page.locator(pattern)
                    if locator.count() > 0:
                        match = re.search(r"ip_(eth\d+)", pattern)
                        if match:
                            interface = match.group(1)
                            available_interfaces.append(interface)

                logger.info(
                    f"After device-aware loading: {len(available_interfaces)} interfaces - {available_interfaces}"
                )

            # Sort interfaces for consistency
            available_interfaces.sort()

            logger.info(
                f"Final device-aware interface detection: {available_interfaces}"
            )
            return available_interfaces

        except Exception as e:
            logger.error(f"Error in device-aware interface detection: {e}")
            return []

    def verify_page_loaded(self):
        """Verify network configuration page with device-aware validation."""
        try:
            # Device-aware timeout
            verification_timeout = int(self.DEFAULT_TIMEOUT * self.timeout_multiplier)

            if self.device_series == 2:
                # Series 2: Validate mode select presence
                mode_select = self.page.locator("select[name='mode']")
                expect(mode_select).to_be_visible(timeout=verification_timeout)
                logger.info("Series 2: Network config page verified")

            elif self.device_series == 3:
                # Series 3: Validate at least one interface presence
                eth0_ip = self.page.locator("input[name='ip_eth0']")
                if eth0_ip.count() > 0:
                    logger.info(
                        "Series 3: Network config page verified (eth0 interface found)"
                    )
                else:
                    logger.warning(
                        "Series 3: eth0 interface not found (may be in collapsed panel)"
                    )

            logger.info(
                f"Network config page verification completed for {self.device_model}"
            )

        except Exception as e:
            logger.error(f"Network config page verification failed: {e}")

    def get_save_button_locator(self):
        """
        Get device-aware save button locator.

        Returns:
            Locator for save button (works for both device types)
        """
        try:
            # Try device-specific save button patterns
            device_model = self.device_model or "Unknown_Device"

            # Get interface-specific save button pattern if available
            save_button_info = DeviceCapabilities.get_interface_specific_save_button(
                device_model, "network_configuration"
            )

            if save_button_info and "selector" in save_button_info:
                save_button = self.page.locator(save_button_info["selector"])
                if save_button.count() > 0:
                    logger.info(
                        f"Using device-specific save button: {save_button_info['selector']}"
                    )
                    return save_button

            # Fallback to Series-specific patterns
            if self.device_series == 3:
                # Series 3: Try button element first
                save_button = self.page.locator("button#button_save")
                if save_button.count() > 0:
                    logger.info("Using Series 3 button#button_save")
                    return save_button

            # Series 2: Use input element
            save_button = self.page.locator("input#button_save")
            if save_button.count() > 0:
                logger.info("Using input#button_save")
                return save_button

            # Final fallback
            logger.warning("Save button not found with device-specific patterns")
            return self.page.get_by_role("button", name="Save")

        except Exception as e:
            logger.error(f"Error getting save button locator: {e}")
            return self.page.get_by_role("button", name="Save")

    def expand_network_interface_panel(self, interface: str) -> bool:
        """
        Expand network interface panel for Series 3 devices.

        Args:
            interface: Network interface name (e.g., 'eth0', 'eth1', 'eth2', 'eth3', 'eth4')

        Returns:
            True if panel was expanded successfully
        """
        if self.device_series != 3:
            logger.info(f"Panel expansion not needed for Series {self.device_series}")
            return True

        if interface not in self.network_interfaces:
            logger.warning(
                f"Interface {interface} not in network interfaces list: {self.network_interfaces}"
            )
            return False

        try:
            # Device-aware timeout
            expansion_timeout = int(5 * self.timeout_multiplier)

            # Find the panel header link
            panel_link = self.page.locator(f"a[href='#{interface}_collapse']")
            if panel_link.count() == 0:
                # Alternative selector patterns
                panel_link = self.page.locator(
                    f"a[data-toggle='collapse'][href='#{interface}_collapse']"
                )

            if panel_link.count() == 0:
                logger.error(f"Network interface panel link not found for {interface}")
                return False

            # Check if panel is already expanded
            collapse_element = self.page.locator(f"#{interface}_collapse")
            if collapse_element.count() > 0:
                class_attr = collapse_element.get_attribute("class") or ""
                is_expanded = "in" in class_attr or "show" in class_attr

                if not is_expanded:
                    logger.info(f"Expanding network interface panel for {interface}")
                    panel_link.click()

                    # Device-aware wait for expansion
                    self.page.wait_for_load_state(
                        "networkidle", timeout=expansion_timeout
                    )
                    time.sleep(0.5)

                    # Verify expansion
                    try:
                        expect(collapse_element).to_have_class("in", timeout=5000)
                        logger.info(
                            f"Network interface panel {interface} expanded successfully"
                        )
                        return True
                    except Exception as e:
                        logger.warning(
                            f"Network interface panel {interface} may not have expanded: {e}"
                        )
                        return False
                else:
                    logger.info(f"Network interface panel {interface} already expanded")
                    return True
            else:
                logger.error(
                    f"Network interface collapse element not found: {interface}_collapse"
                )
                return False

        except Exception as e:
            logger.error(f"Error expanding network interface panel {interface}: {e}")
            return False

    def configure_network_interface(
        self, interface: str, config_data: Dict[str, Any]
    ) -> bool:
        """
        Configure network settings for a specific interface.

        Args:
            interface: Network interface name
            config_data: Network configuration dictionary

        Returns:
            True if configuration successful
        """
        if self.device_series == 2:
            logger.error("Network interface configuration not applicable for Series 2")
            return False

        if interface not in self.network_interfaces:
            logger.error(
                f"Interface {interface} not available: {self.network_interfaces}"
            )
            return False

        try:
            # Ensure panel is expanded first
            if not self.expand_network_interface_panel(interface):
                logger.error(
                    f"Cannot configure interface - failed to expand panel for {interface}"
                )
                return False

            # Device-aware timeout
            config_timeout = int(self.DEFAULT_TIMEOUT * self.timeout_multiplier)

            success_count = 0

            # Configure IP address if specified
            if "ip_address" in config_data:
                ip_field = self.page.locator(f"input[name='ip_{interface}']")
                if ip_field.count() > 0:
                    if self.safe_fill(
                        ip_field, config_data["ip_address"], context=f"ip_{interface}"
                    ):
                        success_count += 1
                    else:
                        logger.warning(f"Failed to set IP address for {interface}")
                else:
                    logger.warning(f"IP address field not found for {interface}")

            # Configure netmask if specified
            if "netmask" in config_data:
                mask_field = self.page.locator(f"input[name='mask_{interface}']")
                if mask_field.count() > 0:
                    if self.safe_fill(
                        mask_field, config_data["netmask"], context=f"mask_{interface}"
                    ):
                        success_count += 1
                    else:
                        logger.warning(f"Failed to set netmask for {interface}")
                else:
                    logger.warning(f"Netmask field not found for {interface}")

            # Configure gateway if specified (eth0 only)
            if "gateway" in config_data and interface == "eth0":
                gateway_field = self.page.locator("input[name='gateway']")
                if gateway_field.count() > 0:
                    if self.safe_fill(
                        gateway_field, config_data["gateway"], context="gateway"
                    ):
                        success_count += 1
                    else:
                        logger.warning(f"Failed to set gateway for {interface}")
                else:
                    logger.warning(f"Gateway field not found")

            logger.info(
                f"Network interface {interface} configuration: {success_count} fields set"
            )
            return success_count > 0

        except Exception as e:
            logger.error(f"Error configuring network interface {interface}: {e}")
            return False

    def get_page_data(self) -> Dict[str, Any]:
        """Extract network configuration data from the page."""
        page_data = {
            "device_series": self.device_series,
            "device_model": self.device_model,
        }

        try:
            if self.device_series == 2:
                # Series 2: Extract network mode and IP configuration
                mode_select = self.page.locator("select[name='mode']")
                if mode_select.is_visible():
                    selected_option = mode_select.locator("option:checked")
                    if selected_option.is_visible():
                        page_data["mode"] = selected_option.get_attribute("value") or ""

                # Extract IP configuration
                for field in ["ipaddr", "ipmask", "gateway", "ipaddrB", "ipmaskB"]:
                    input_field = self.page.locator(f"input[name='{field}']")
                    if input_field.is_visible():
                        page_data[field] = input_field.input_value()

            else:  # Series 3
                # Series 3: Extract ethernet port configurations
                capabilities = self.detect_device_capabilities()
                for port in capabilities["available_interfaces"]:
                    ip_field = self.page.locator(f"input[name='ip_{port}']")
                    mask_field = self.page.locator(f"input[name='mask_{port}']")

                    if ip_field.is_visible():
                        page_data[f"{port}_ip"] = ip_field.input_value()
                        page_data[f"{port}_netmask"] = mask_field.input_value()

            # Extract gateway (eth0 only)
            gateway_field = self.page.locator("input[name='gateway']")
            if gateway_field.is_visible():
                page_data["gateway"] = gateway_field.input_value()

            # Extract DHCP settings
            dhcp_checkbox = self.page.locator("input[name='dhcp']")
            if dhcp_checkbox.is_visible():
                page_data["dhcp_enabled"] = dhcp_checkbox.is_checked()

            logger.info(
                f"Extracted network configuration data: {len(page_data)} fields"
            )
            return page_data

        except Exception as e:
            logger.error(f"Error extracting network configuration data: {e}")
            return page_data

    def set_network_mode(self, mode: str) -> bool:
        """
        Set network mode for Series 2 devices.

        Args:
            mode: Network mode ('dhcp', 'static', etc.)

        Returns:
            True if mode set successfully
        """
        if self.device_series != 2:
            logger.warning(
                f"Network mode setting not applicable for Series {self.device_series}"
            )
            return False

        try:
            mode_select = self.page.locator("select[name='mode']")
            if mode_select.count() > 0:
                mode_select.select_option(mode)
                logger.info(f"Network mode set to: {mode}")
                return True
            else:
                logger.error("Mode select element not found")
                return False

        except Exception as e:
            logger.error(f"Error setting network mode: {e}")
            return False

    def configure_dhcp_mode(self, interface: str = "eth0") -> bool:
        """
        Configure DHCP mode for specified interface.

        Args:
            interface: Network interface name

        Returns:
            True if DHCP configured successfully
        """
        try:
            if self.device_series == 2:
                # Series 2: Set mode to DHCP
                return self.set_network_mode("dhcp")
            else:
                # Series 3: Check DHCP checkbox for specific interface
                dhcp_checkbox = self.page.locator(f"input[name='dhcp_{interface}']")
                if dhcp_checkbox.count() > 0:
                    if not dhcp_checkbox.is_checked():
                        dhcp_checkbox.click()
                    logger.info(f"DHCP mode enabled for {interface}")
                    return True
                else:
                    logger.warning(f"DHCP checkbox not found for {interface}")
                    return False

        except Exception as e:
            logger.error(f"Error configuring DHCP mode for {interface}: {e}")
            return False

    def configure_static_ip(
        self, interface: str, ip_address: str, netmask: str, gateway: str
    ) -> bool:
        """
        Configure static IP address for specified interface.

        Args:
            interface: Network interface name
            ip_address: Static IP address
            netmask: Network netmask
            gateway: Gateway address (optional, eth0 only)

        Returns:
            True if static IP configured successfully
        """
        try:
            if self.device_series == 2:
                # Series 2: Set mode to static, then configure IP
                if not self.set_network_mode("static"):
                    return False

                # Configure IP address
                ip_field = self.page.locator("input[name='ipaddr']")
                if ip_field.count() > 0 and not self.safe_fill(
                    ip_field, ip_address, context="ipaddr"
                ):
                    logger.warning("Failed to set static IP address")
                    return False

                # Configure netmask
                mask_field = self.page.locator("input[name='ipmask']")
                if mask_field.count() > 0 and not self.safe_fill(
                    mask_field, netmask, context="ipmask"
                ):
                    logger.warning("Failed to set static netmask")
                    return False

                # Configure gateway if provided
                if gateway:
                    gateway_field = self.page.locator("input[name='gateway']")
                    if gateway_field.count() > 0 and not self.safe_fill(
                        gateway_field, gateway, context="gateway"
                    ):
                        logger.warning("Failed to set gateway")
                        return False

                logger.info("Series 2 static IP configuration completed")
                return True

            else:
                # Series 3: Use interface-specific configuration
                return self.configure_network_interface(
                    interface,
                    {"ip_address": ip_address, "netmask": netmask, "gateway": gateway},
                )

        except Exception as e:
            logger.error(f"Error configuring static IP for {interface}: {e}")
            return False

    def save_network_config(self, interface: str) -> bool:
        """
        Save network configuration with device-aware save button handling.

        Args:
            interface: Specific interface to save (optional)

        Returns:
            True if configuration saved successfully
        """
        try:
            save_button = self.get_save_button_locator()
            if not save_button or save_button.count() == 0:
                logger.error("Save button not found")
                return False

            # Device-aware timeout
            save_timeout = int(self.DEFAULT_TIMEOUT * self.timeout_multiplier)

            logger.info(
                f"Saving network configuration"
                + (f" for {interface}" if interface else "")
            )

            # Click save button
            save_button.click()

            # Wait for save operation with device-aware timeout
            self.page.wait_for_load_state("networkidle", timeout=save_timeout)

            # Additional wait for embedded device save processing
            time.sleep(2 * self.timeout_multiplier)

            # Verify save was successful (check for success message or absence of errors)
            success_indicators = [
                "input[name='message'][value*='success']",
                ".alert-success",
                "input[name='message'][value*='saved']",
            ]

            for indicator in success_indicators:
                if self.page.locator(indicator).count() > 0:
                    logger.info("Network configuration saved successfully")
                    return True

            # If no explicit success indicator, assume success if no error
            error_indicators = [
                "input[name='message'][value*='error']",
                ".alert-danger",
                "input[name='message'][value*='failed']",
            ]

            has_errors = any(
                self.page.locator(error).count() > 0 for error in error_indicators
            )

            if not has_errors:
                logger.info("Network configuration save completed (no errors detected)")
                return True
            else:
                logger.error("Network configuration save failed (errors detected)")
                return False

        except Exception as e:
            logger.error(f"Error saving network configuration: {e}")
            return False

    def validate_network_config(self, expected_config: Dict[str, Any]) -> bool:
        """
        Validate network configuration matches expected settings.

        Args:
            expected_config: Expected network configuration

        Returns:
            True if configuration matches expected values
        """
        try:
            current_config = self.get_page_data()
            validation_passed = True

            logger.info("Validating network configuration...")

            # Validate device series consistency
            if "device_series" in expected_config:
                if (
                    current_config.get("device_series")
                    != expected_config["device_series"]
                ):
                    logger.error(
                        f"Device series mismatch: expected {expected_config['device_series']}, got {current_config.get('device_series')}"
                    )
                    validation_passed = False

            # Validate network mode for Series 2
            if self.device_series == 2 and "mode" in expected_config:
                if current_config.get("mode") != expected_config["mode"]:
                    logger.error(
                        f"Network mode mismatch: expected {expected_config['mode']}, got {current_config.get('mode')}"
                    )
                    validation_passed = False

            # Validate IP configuration
            for field, expected_value in expected_config.items():
                if field.startswith("ip_") or field in ["gateway", "netmask"]:
                    if current_config.get(field) != expected_value:
                        logger.error(
                            f"{field} mismatch: expected '{expected_value}', got '{current_config.get(field)}'"
                        )
                        validation_passed = False

            if validation_passed:
                logger.info("Network configuration validation PASSED")
            else:
                logger.error("Network configuration validation FAILED")

            return validation_passed

        except Exception as e:
            logger.error(f"Error validating network configuration: {e}")
            return False

    def reset_to_defaults(self, interface: str) -> bool:
        """
        Reset network configuration to defaults.

        Args:
            interface: Specific interface to reset (optional)

        Returns:
            True if reset successful
        """
        try:
            logger.info(
                "Resetting network configuration to defaults"
                + (f" for {interface}" if interface else "")
            )

            # This would typically involve clicking a reset/defaults button
            # For now, implement basic DHCP mode setting as default
            if self.device_series == 2:
                return self.configure_dhcp_mode()
            else:
                # For Series 3, configure eth0 as DHCP by default
                return self.configure_dhcp_mode("eth0")

        except Exception as e:
            logger.error(f"Error resetting network configuration: {e}")
            return False

    def get_network_status(self) -> Dict[str, Any]:
        """
        Get current network status and link state.

        Returns:
            Dictionary with network status information
        """
        status = {
            "device_series": self.device_series,
            "interfaces": {},
            "overall_status": "unknown",
        }

        try:
            # Get current configuration data
            current_config = self.get_page_data()

            if self.device_series == 2:
                # Series 2: Single interface status
                status["interfaces"]["primary"] = {
                    "mode": current_config.get("mode", "unknown"),
                    "ip_address": current_config.get("ipaddr", ""),
                    "status": "active",  # Series 2 doesn't have detailed link status
                }
            else:
                # Series 3: Multi-interface status
                capabilities = self.detect_device_capabilities()
                for interface in capabilities["available_interfaces"]:
                    interface_data = {
                        "ip_address": current_config.get(f"{interface}_ip", ""),
                        "netmask": current_config.get(f"{interface}_netmask", ""),
                        "status": "active",  # Would need actual link detection
                        "ptp_capable": interface in self.ptp_interfaces,
                    }
                    status["interfaces"][interface] = interface_data

            status["overall_status"] = "active"
            logger.info(
                f"Network status retrieved for {len(status['interfaces'])} interfaces"
            )
            return status

        except Exception as e:
            logger.error(f"Error getting network status: {e}")
            status["overall_status"] = "error"
            return status

    def get_firewall_configuration(self) -> Dict[str, Any]:
        """
        Get firewall and ACL configuration settings.

        Returns:
            Dictionary with firewall configuration information
        """
        firewall_config = {
            "has_firewall_fields": False,
            "fields_enabled": False,
            "firewall_fields": [],
            "acl_fields": [],
        }

        try:
            # Look for firewall fields
            firewall_fields = self.page.locator("input[name*='firewall' i]")
            if firewall_fields.count() > 0:
                firewall_config["has_firewall_fields"] = True
                firewall_config["firewall_fields"] = [
                    field.get_attribute("name")
                    for field in firewall_fields.all()
                    if field.is_visible()
                ]

                # Check if fields are enabled
                enabled_fields = [
                    field for field in firewall_fields.all() if field.is_enabled()
                ]
                firewall_config["fields_enabled"] = len(enabled_fields) > 0

            # Look for ACL fields
            acl_fields = self.page.locator(
                "select[name*='acl' i], input[name*='acl' i]"
            )
            if acl_fields.count() > 0:
                firewall_config["has_firewall_fields"] = True
                firewall_config["acl_fields"] = [
                    field.get_attribute("name")
                    for field in acl_fields.all()
                    if field.is_visible()
                ]

            logger.info(f"Firewall configuration: {firewall_config}")
            return firewall_config

        except Exception as e:
            logger.error(f"Error getting firewall configuration: {e}")
            return firewall_config

    def get_acl_configuration(self) -> Dict[str, Any]:
        """
        Get ACL (Access Control List) configuration settings.

        Returns:
            Dictionary with ACL configuration information
        """
        acl_config = {
            "has_acl_fields": False,
            "fields_editable": False,
            "acl_textareas": [],
            "acl_rules": [],
        }

        try:
            # Look for ACL textareas
            acl_textareas = self.page.locator("textarea[name*='acl' i]")
            if acl_textareas.count() > 0:
                acl_config["has_acl_fields"] = True
                acl_config["acl_textareas"] = [
                    field.get_attribute("name")
                    for field in acl_textareas.all()
                    if field.is_visible()
                ]

                # Check if fields are editable
                editable_fields = [
                    field for field in acl_textareas.all() if field.is_editable()
                ]
                acl_config["fields_editable"] = len(editable_fields) > 0

            # Look for ACL rule inputs
            acl_rules = self.page.locator("input[name*='acl_rule' i]")
            if acl_rules.count() > 0:
                acl_config["has_acl_fields"] = True
                acl_config["acl_rules"] = [
                    field.get_attribute("name")
                    for field in acl_rules.all()
                    if field.is_visible()
                ]

                # Check if rule fields are editable
                editable_rules = [
                    field for field in acl_rules.all() if field.is_editable()
                ]
                if len(editable_rules) > 0:
                    acl_config["fields_editable"] = True

            logger.info(f"ACL configuration: {acl_config}")
            return acl_config

        except Exception as e:
            logger.error(f"Error getting ACL configuration: {e}")
            return acl_config

    def get_port_security_configuration(self) -> Dict[str, Any]:
        """
        Get port security and MAC filtering configuration settings.

        Returns:
            Dictionary with port security configuration information
        """
        port_security_config = {
            "has_port_security_fields": False,
            "fields_enabled": False,
            "port_security_fields": [],
            "mac_filter_fields": [],
        }

        try:
            # Look for port security fields
            port_security_fields = self.page.locator("input[name*='port_security' i]")
            if port_security_fields.count() > 0:
                port_security_config["has_port_security_fields"] = True
                port_security_config["port_security_fields"] = [
                    field.get_attribute("name")
                    for field in port_security_fields.all()
                    if field.is_visible()
                ]

                # Check if fields are enabled
                enabled_fields = [
                    field for field in port_security_fields.all() if field.is_enabled()
                ]
                port_security_config["fields_enabled"] = len(enabled_fields) > 0

            # Look for MAC filter fields
            mac_filter_fields = self.page.locator("select[name*='mac_filter' i]")
            if mac_filter_fields.count() > 0:
                port_security_config["has_port_security_fields"] = True
                port_security_config["mac_filter_fields"] = [
                    field.get_attribute("name")
                    for field in mac_filter_fields.all()
                    if field.is_visible()
                ]

                # Check if fields are enabled
                enabled_mac_filters = [
                    field for field in mac_filter_fields.all() if field.is_enabled()
                ]
                if len(enabled_mac_filters) > 0:
                    port_security_config["fields_enabled"] = True

            logger.info(f"Port security configuration: {port_security_config}")
            return port_security_config

        except Exception as e:
            logger.error(f"Error getting port security configuration: {e}")
            return port_security_config

    def get_interface_statistics_configuration(self) -> Dict[str, Any]:
        """
        Get interface statistics and monitoring configuration settings.

        Returns:
            Dictionary with interface statistics configuration information
        """
        interface_stats_config = {
            "has_statistics_fields": False,
            "fields_enabled": False,
            "statistics_buttons": [],
            "statistics_links": [],
        }

        try:
            # Look for statistics buttons
            stats_buttons = self.page.locator("button[name*='stats' i]")
            if stats_buttons.count() > 0:
                interface_stats_config["has_statistics_fields"] = True
                interface_stats_config["statistics_buttons"] = [
                    field.get_attribute("name")
                    for field in stats_buttons.all()
                    if field.is_visible()
                ]

                # Check if buttons are enabled
                enabled_buttons = [
                    field for field in stats_buttons.all() if field.is_enabled()
                ]
                interface_stats_config["fields_enabled"] = len(enabled_buttons) > 0

            # Look for statistics links
            stats_links = self.page.locator("a[href*='statistics']")
            if stats_links.count() > 0:
                interface_stats_config["has_statistics_fields"] = True
                interface_stats_config["statistics_links"] = [
                    field.get_attribute("href")
                    for field in stats_links.all()
                    if field.is_visible()
                ]

                # Check if links are enabled
                enabled_links = [
                    field for field in stats_links.all() if field.is_enabled()
                ]
                if len(enabled_links) > 0:
                    interface_stats_config["fields_enabled"] = True

            logger.info(f"Interface statistics configuration: {interface_stats_config}")
            return interface_stats_config

        except Exception as e:
            logger.error(f"Error getting interface statistics configuration: {e}")
            return interface_stats_config

    def get_link_status_monitoring_configuration(self) -> Dict[str, Any]:
        """
        Get link status monitoring configuration settings.

        Returns:
            Dictionary with link status monitoring configuration information
        """
        link_status_config = {
            "has_link_status_fields": False,
            "fields_visible": False,
            "status_spans": [],
            "link_status_divs": [],
        }

        try:
            # Look for status spans
            status_spans = self.page.locator("span[name*='status' i]")
            if status_spans.count() > 0:
                link_status_config["has_link_status_fields"] = True
                link_status_config["status_spans"] = [
                    field.get_attribute("name")
                    for field in status_spans.all()
                    if field.is_visible()
                ]

                # Check if spans are visible
                visible_spans = [
                    field for field in status_spans.all() if field.is_visible()
                ]
                link_status_config["fields_visible"] = len(visible_spans) > 0

            # Look for link status divs
            link_status_divs = self.page.locator("div[class*='link-status']")
            if link_status_divs.count() > 0:
                link_status_config["has_link_status_fields"] = True
                link_status_config["link_status_divs"] = [
                    field.get_attribute("class")
                    for field in link_status_divs.all()
                    if field.is_visible()
                ]

                # Check if divs are visible
                visible_divs = [
                    field for field in link_status_divs.all() if field.is_visible()
                ]
                if len(visible_divs) > 0:
                    link_status_config["fields_visible"] = True

            logger.info(f"Link status monitoring configuration: {link_status_config}")
            return link_status_config

        except Exception as e:
            logger.error(f"Error getting link status monitoring configuration: {e}")
            return link_status_config

    def get_network_diagnostics_configuration(self) -> Dict[str, Any]:
        """
        Get network diagnostics and troubleshooting configuration settings.

        Returns:
            Dictionary with network diagnostics configuration information
        """
        network_diagnostics_config = {
            "has_diagnostics_fields": False,
            "fields_enabled": False,
            "diagnostic_buttons": [],
            "ping_buttons": [],
            "traceroute_buttons": [],
        }

        try:
            # Look for diagnostic buttons
            diag_buttons = self.page.locator("button[name*='diag' i]")
            if diag_buttons.count() > 0:
                network_diagnostics_config["has_diagnostics_fields"] = True
                network_diagnostics_config["diagnostic_buttons"] = [
                    field.get_attribute("name")
                    for field in diag_buttons.all()
                    if field.is_visible()
                ]

                # Check if buttons are enabled
                enabled_diag = [
                    field for field in diag_buttons.all() if field.is_enabled()
                ]
                network_diagnostics_config["fields_enabled"] = len(enabled_diag) > 0

            # Look for ping buttons
            ping_buttons = self.page.locator("button[name*='ping' i]")
            if ping_buttons.count() > 0:
                network_diagnostics_config["has_diagnostics_fields"] = True
                network_diagnostics_config["ping_buttons"] = [
                    field.get_attribute("name")
                    for field in ping_buttons.all()
                    if field.is_visible()
                ]

                # Check if ping buttons are enabled
                enabled_ping = [
                    field for field in ping_buttons.all() if field.is_enabled()
                ]
                if len(enabled_ping) > 0:
                    network_diagnostics_config["fields_enabled"] = True

            # Look for traceroute buttons
            traceroute_buttons = self.page.locator("button[name*='traceroute' i]")
            if traceroute_buttons.count() > 0:
                network_diagnostics_config["has_diagnostics_fields"] = True
                network_diagnostics_config["traceroute_buttons"] = [
                    field.get_attribute("name")
                    for field in traceroute_buttons.all()
                    if field.is_visible()
                ]

                # Check if traceroute buttons are enabled
                enabled_traceroute = [
                    field for field in traceroute_buttons.all() if field.is_enabled()
                ]
                if len(enabled_traceroute) > 0:
                    network_diagnostics_config["fields_enabled"] = True

            logger.info(
                f"Network diagnostics configuration: {network_diagnostics_config}"
            )
            return network_diagnostics_config

        except Exception as e:
            logger.error(f"Error getting network diagnostics configuration: {e}")
            return network_diagnostics_config

    def get_vlan_creation_configuration(self) -> Dict[str, Any]:
        """
        Get VLAN creation and ID assignment configuration settings.

        Returns:
            Dictionary with VLAN creation configuration information
        """
        vlan_config = {
            "has_vlan_fields": False,
            "vlan_fields_found": False,
            "port_vlan_fields": {},
            "global_vlan_fields": [],
            "available_ports": [],
        }

        try:
            # Available ports to check (skip eth2 as it's combined with eth1)
            available_ports = ["eth0", "eth1", "eth3", "eth4"]

            # Check VLAN configuration on each available port
            for port in available_ports:
                vlan_id_input = self.page.locator(f"input[name='vlan_id_{port}']")
                vlan_enable_input = self.page.locator(
                    f"input[name='vlan_enable_{port}']"
                )

                # Check if VLAN ID input exists and is visible for this port
                if vlan_id_input.count() > 0:
                    vlan_config["has_vlan_fields"] = True
                    vlan_config["available_ports"].append(port)

                    # Try to expand panel if needed
                    panel_selector = f"a[href='#port_{port}_collapse']"
                    panel_toggle = self.page.locator(panel_selector)
                    if panel_toggle.count() > 0:
                        aria_expanded = panel_toggle.get_attribute("aria-expanded")
                        if aria_expanded != "true":
                            panel_toggle.click()
                            time.sleep(0.5)  # Wait for panel expansion

                    # Check if VLAN ID input is visible
                    if vlan_id_input.is_visible():
                        vlan_config["vlan_fields_found"] = True
                        vlan_config["port_vlan_fields"][port] = {
                            "vlan_id_field": True,
                            "vlan_enable_field": vlan_enable_input.count() > 0,
                            "visible": True,
                        }
                    else:
                        vlan_config["port_vlan_fields"][port] = {
                            "vlan_id_field": True,
                            "vlan_enable_field": vlan_enable_input.count() > 0,
                            "visible": False,
                        }

            # If no port-specific VLAN found, look for global VLAN settings
            if not vlan_config["vlan_fields_found"]:
                global_vlan_id = self.page.locator("input[name='vlan_id']")
                global_vlan = self.page.locator("input[name='vlan']")

                if global_vlan_id.count() > 0 and global_vlan_id.first.is_visible():
                    vlan_config["has_vlan_fields"] = True
                    vlan_config["vlan_fields_found"] = True
                    vlan_config["global_vlan_fields"].append("vlan_id")

                if global_vlan.count() > 0 and global_vlan.first.is_visible():
                    vlan_config["has_vlan_fields"] = True
                    vlan_config["vlan_fields_found"] = True
                    vlan_config["global_vlan_fields"].append("vlan")

            logger.info(f"VLAN creation configuration: {vlan_config}")
            return vlan_config

        except Exception as e:
            logger.error(f"Error getting VLAN creation configuration: {e}")
            return vlan_config

    def test_vlan_id_range(self, port: str = None, vlan_ids: List[str] = None) -> bool:
        """
        Test VLAN ID range validation (1-4094).

        Args:
            port: Specific port to test (optional)
            vlan_ids: List of VLAN IDs to test (optional)

        Returns:
            True if VLAN ID testing successful
        """
        try:
            if vlan_ids is None:
                vlan_ids = ["1", "100", "4094"]  # Test valid VLAN ID range

            if port:
                # Test VLAN ID on specific port
                vlan_id_input = self.page.locator(f"input[name='vlan_id_{port}']")
                if vlan_id_input.count() > 0 and vlan_id_input.is_visible():
                    for vid in vlan_ids:
                        vlan_id_input.fill(vid)
                        actual_value = vlan_id_input.input_value()
                        if actual_value != vid:
                            logger.warning(f"VLAN ID {vid} not set correctly on {port}")
                            return False
                    logger.info(f"VLAN ID range test passed on port {port}")
                    return True
                else:
                    logger.warning(
                        f"VLAN ID input not found or not visible on port {port}"
                    )
                    return False
            else:
                # Test on first available VLAN field
                vlan_config = self.get_vlan_creation_configuration()

                # Try port-specific VLAN fields first
                for port_name in vlan_config.get("available_ports", []):
                    vlan_id_input = self.page.locator(
                        f"input[name='vlan_id_{port_name}']"
                    )
                    if vlan_id_input.count() > 0 and vlan_id_input.is_visible():
                        for vid in vlan_ids:
                            vlan_id_input.fill(vid)
                            actual_value = vlan_id_input.input_value()
                            if actual_value != vid:
                                logger.warning(
                                    f"VLAN ID {vid} not set correctly on {port_name}"
                                )
                                return False
                        logger.info(f"VLAN ID range test passed on port {port_name}")
                        return True

                # Try global VLAN fields
                global_vlan = self.page.locator("input[name='vlan_id']")
                if global_vlan.count() > 0 and global_vlan.first.is_visible():
                    for vid in vlan_ids:
                        global_vlan.first.fill(vid)
                        actual_value = global_vlan.first.input_value()
                        if actual_value != vid:
                            logger.warning(f"Global VLAN ID {vid} not set correctly")
                            return False
                    logger.info("Global VLAN ID range test passed")
                    return True

                logger.warning("No VLAN ID fields found for testing")
                return False

        except Exception as e:
            logger.error(f"Error testing VLAN ID range: {e}")
            return False

    def get_vlan_port_assignment_configuration(self) -> Dict[str, Any]:
        """
        Get VLAN port assignment configuration settings.

        Returns:
            Dictionary with VLAN port assignment configuration information
        """
        vlan_port_assignment_config = {
            "has_port_assignment_fields": False,
            "fields_enabled": False,
            "vlan_ports_selects": [],
            "tagged_ports_inputs": [],
        }

        try:
            # Look for VLAN port assignment selects
            vlan_ports_selects = self.page.locator("select[name*='vlan_ports' i]")
            if vlan_ports_selects.count() > 0:
                vlan_port_assignment_config["has_port_assignment_fields"] = True
                vlan_port_assignment_config["vlan_ports_selects"] = [
                    field.get_attribute("name")
                    for field in vlan_ports_selects.all()
                    if field.is_visible()
                ]

                # Check if fields are enabled
                enabled_selects = [
                    field for field in vlan_ports_selects.all() if field.is_enabled()
                ]
                vlan_port_assignment_config["fields_enabled"] = len(enabled_selects) > 0

            # Look for tagged ports inputs
            tagged_ports_inputs = self.page.locator("input[name*='tagged_ports' i]")
            if tagged_ports_inputs.count() > 0:
                vlan_port_assignment_config["has_port_assignment_fields"] = True
                vlan_port_assignment_config["tagged_ports_inputs"] = [
                    field.get_attribute("name")
                    for field in tagged_ports_inputs.all()
                    if field.is_visible()
                ]

                # Check if inputs are enabled
                enabled_inputs = [
                    field for field in tagged_ports_inputs.all() if field.is_enabled()
                ]
                if len(enabled_inputs) > 0:
                    vlan_port_assignment_config["fields_enabled"] = True

            logger.info(
                f"VLAN port assignment configuration: {vlan_port_assignment_config}"
            )
            return vlan_port_assignment_config

        except Exception as e:
            logger.error(f"Error getting VLAN port assignment configuration: {e}")
            return vlan_port_assignment_config

    def get_vlan_trunking_configuration(self) -> Dict[str, Any]:
        """
        Get VLAN trunking and tagging configuration settings.

        Returns:
            Dictionary with VLAN trunking configuration information
        """
        vlan_trunking_config = {
            "has_trunking_fields": False,
            "fields_enabled": False,
            "trunk_inputs": [],
            "vlan_mode_selects": [],
        }

        try:
            # Look for trunk configuration inputs
            trunk_inputs = self.page.locator("input[name*='trunk' i]")
            if trunk_inputs.count() > 0:
                vlan_trunking_config["has_trunking_fields"] = True
                vlan_trunking_config["trunk_inputs"] = [
                    field.get_attribute("name")
                    for field in trunk_inputs.all()
                    if field.is_visible()
                ]

                # Check if fields are enabled
                enabled_trunks = [
                    field for field in trunk_inputs.all() if field.is_enabled()
                ]
                vlan_trunking_config["fields_enabled"] = len(enabled_trunks) > 0

            # Look for VLAN mode selects
            vlan_mode_selects = self.page.locator("select[name*='vlan_mode' i]")
            if vlan_mode_selects.count() > 0:
                vlan_trunking_config["has_trunking_fields"] = True
                vlan_trunking_config["vlan_mode_selects"] = [
                    field.get_attribute("name")
                    for field in vlan_mode_selects.all()
                    if field.is_visible()
                ]

                # Check if selects are enabled
                enabled_modes = [
                    field for field in vlan_mode_selects.all() if field.is_enabled()
                ]
                if len(enabled_modes) > 0:
                    vlan_trunking_config["fields_enabled"] = True

            logger.info(f"VLAN trunking configuration: {vlan_trunking_config}")
            return vlan_trunking_config

        except Exception as e:
            logger.error(f"Error getting VLAN trunking configuration: {e}")
            return vlan_trunking_config

    def close(self):
        """Clean up resources."""
        try:
            logger.info(f"NetworkConfigPageDevice closing for {self.device_model}")
            super().close()
        except Exception as e:
            logger.error(f"Error closing NetworkConfigPageDevice: {e}")
