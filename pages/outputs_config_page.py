"""
 Outputs configuration page object for Kronos device test automation.

 with comprehensive DeviceCapabilities integration:
- Device-aware output channel detection (1-6 outputs based on device series)
- Series-specific signal type handling (Series 2 vs Series 3 extended options)
- Device-aware timeout management with timeout multipliers
-  error handling and debugging patterns
- Interface-specific save button handling
- Dynamic capability validation against device database

Series 2 (2 outputs): signal1, signal2 with basic options (OFF, IRIG-B variants, PPS, PPM)
Series 3 (6 outputs): signal1-signal6 with extended options (+ IRIG-B120/122/124/126)
Time reference selection (UTC/LOCAL) via radio buttons
Device-aware save button (input#button_save for Series 2, button#button_save for Series 3)
"""

from playwright.sync_api import Page, expect
from .base import BasePage
from .device_capabilities import DeviceCapabilities
from typing import Dict, Optional, List, Any, Union
import time


class OutputsConfigPage(BasePage):
    """
     page object for Kronos device outputs configuration.

    Features:
    - Full DeviceCapabilities integration for device-aware behavior
    - Dynamic output channel detection (1-6 based on device capabilities)
    - Series-specific signal type handling
    -  error handling and debugging
    - Device-aware timeout management
    - Interface-specific save button handling
    """

    def __init__(self, page: Page, device_model: Optional[str] = None):
        """Initialize  outputs configuration page."""
        super().__init__(page, device_model)

        # Use DeviceCapabilities for device-aware initialization
        self.timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(
            device_model or "UNKNOWN_DEVICE"
        )

        # Set up device-aware expectations from capabilities database
        self._setup_expectations()

        print(f"OutputsConfigPage initialized for {device_model}")
        print(f"  Series: {self.get_device_series()}")
        print(f"  Timeout multiplier: {self.timeout_multiplier}")

    def _setup_expectations(self):
        """Set up device-aware expectations based on capabilities database."""
        self.device_model = self.device_model or "UNKNOWN_DEVICE"

        try:
            capabilities = DeviceCapabilities.get_capabilities(self.device_model)
            if capabilities:
                self.expected_output_count = len(
                    capabilities.get("output_signal_types", {})
                )
                self.has_extended_signal_types = capabilities.get(
                    "supports_extended_irig", False
                )
                self.supports_utc_local_selection = capabilities.get(
                    "supports_utc_local_selection", True
                )
            else:
                # Fallback for unknown devices
                self.expected_output_count = 2
                self.has_extended_signal_types = False
                self.supports_utc_local_selection = True
        except Exception as e:
            print(f"Warning: Could not setup device-aware expectations: {e}")
            self.expected_output_count = 2
            self.has_extended_signal_types = False
            self.supports_utc_local_selection = True

    def get_device_series(self) -> str:
        """Get device series using DeviceCapabilities."""
        try:
            series = DeviceCapabilities.get_series(
                self.device_model or "UNKNOWN_DEVICE"
            )
            return str(series) if series else "Unknown"
        except Exception as e:
            print(f"Warning: Could not get device series: {e}")
            return "Unknown"

    def validate_capabilities(self) -> bool:
        """
        Validate that the page layout matches device capabilities from DeviceCapabilities.

         validation comparing expected capabilities (from device database)
        against actual detected capabilities to ensure database accuracy.

        Returns:
            bool: True if capabilities match, False if there are discrepancies
        """
        if not self.device_model:
            print("No device model available for validation")
            return True

        try:
            validation_passed = True
            actual_capabilities = self.detect_output_capabilities()
            device_capabilities = DeviceCapabilities.get_capabilities(self.device_model)

            if not device_capabilities:
                print(f"No capabilities found for device model: {self.device_model}")
                return False

            # Convert expected output_signal_types dict to expected count
            expected_signal_types = device_capabilities.get("output_signal_types", {})
            expected_output_count = len(expected_signal_types)
            actual_output_count = actual_capabilities.get("output_channels", 0)

            print(f"Validating {self.device_model} capabilities:")
            print(
                f"  Expected {expected_output_count} outputs, detected {actual_output_count}"
            )

            # Validate output count
            if expected_output_count != actual_output_count:
                print(
                    f"   Output count mismatch: expected {expected_output_count}, got {actual_output_count}"
                )
                validation_passed = False
            else:
                print("   Output count matches expected capabilities")

            # Validate signal types for each expected channel
            for channel_num in range(1, expected_output_count + 1):
                if channel_num <= actual_output_count:
                    # Get expected signals from device capabilities database
                    expected_signals = expected_signal_types.get(
                        f"signal{channel_num}", []
                    )
                    actual_channel_data = actual_capabilities.get(
                        f"channel_{channel_num}", {}
                    )
                    actual_signals = [
                        sig.get("value", "").strip()
                        for sig in actual_channel_data.get("available_options", [])
                    ]

                    # Compare signal sets (order doesn't matter)
                    expected_set = set(expected_signals)
                    actual_set = set(actual_signals)

                    if expected_set == actual_set:
                        print(
                            f"   Channel {channel_num}: signal types match ({len(expected_signals)} options)"
                        )
                    else:
                        print(f"   Channel {channel_num}: signal types don't match")
                        print(f"    Expected: {sorted(expected_set)}")
                        print(f"    Actual: {sorted(actual_set)}")
                        validation_passed = False
                else:
                    print(
                        f"   Channel {channel_num}: not found on page (page has only {actual_output_count} channels)"
                    )
                    validation_passed = False

            if validation_passed:
                print("   Capability validation PASSED")
            else:
                print(
                    "   Capability validation FAILED - device layout doesn't match database"
                )
            return validation_passed

        except Exception as e:
            print(f"Error during capability validation: {e}")
            return False

    def detect_output_capabilities(self) -> Dict[str, Any]:
        """
        Detect actual output capabilities from the page.

         detection with device-aware patterns and proper error handling.

        Returns:
            Dictionary with actual device output capabilities
        """
        try:
            output_count = 0

            # Use device-aware timeout
            timeout = int(self.DEFAULT_TIMEOUT * self.timeout_multiplier)

            # Initial scan - query all possible output channels
            for channel in range(1, 7):  # Check up to 6 possible channels
                signal_select = self.page.locator(f"select[name='signal{channel}']")
                if signal_select.count() > 0 and signal_select.is_visible():
                    output_count += 1
                else:
                    break  # Stop when we hit first missing channel

            print(f"Dynamic output detection: Found {output_count} output channels")

            # PROTECT AGAINST FALSE NEGATIVES: If finding 1 or fewer outputs,
            # wait for full page load before concluding (embedded device timing issues)
            if output_count <= 1:
                print("Only found 1 or fewer outputs - waiting for full page load...")

                # Wait for page loading to complete fully
                self.wait_for_page_load(timeout=timeout)
                time.sleep(2)  # Additional buffer for embedded device timing

                # Re-scan after full load to get accurate count
                output_count = 0
                for channel in range(1, 7):
                    signal_select = self.page.locator(f"select[name='signal{channel}']")
                    if signal_select.count() > 0 and signal_select.is_visible():
                        output_count += 1
                    else:
                        break

                print(
                    f"After full load verification: Confirmed {output_count} output channels"
                )

            # Detect signal capabilities for each available channel
            capabilities = {
                "output_channels": output_count,
                "detected_series": self.get_device_series(),
                "supports_pps": False,
                "supports_irig": False,
                "supports_frequency": False,
                "supports_ppm": False,
                "extended_irig_available": False,
            }

            # Add capability detection for each available channel
            for channel in range(1, output_count + 1):
                channel_capabilities = self._detect_channel_capabilities(channel)
                capabilities[f"channel_{channel}"] = channel_capabilities

                # Aggregate capabilities across all channels
                if channel_capabilities.get("supports_pps", False):
                    capabilities["supports_pps"] = True
                if channel_capabilities.get("supports_irig", False):
                    capabilities["supports_irig"] = True
                if channel_capabilities.get("supports_frequency", False):
                    capabilities["supports_frequency"] = True
                if channel_capabilities.get("supports_ppm", False):
                    capabilities["supports_ppm"] = True
                if channel_capabilities.get("extended_irig_available", False):
                    capabilities["extended_irig_available"] = True

            print(
                f" output capabilities: {output_count} channels with detected features"
            )
            return capabilities

        except Exception as e:
            print(f"Error detecting output capabilities: {e}")
            return {"output_channels": 0, "error": str(e)}

    def _detect_channel_capabilities(self, channel: int) -> Dict[str, Any]:
        """
        Detect capabilities for a specific output channel.

        Args:
            channel: Output channel number (1-6)

        Returns:
            Dictionary with capability flags for this channel
        """
        capabilities = {
            "supports_pps": False,
            "supports_irig": False,
            "supports_frequency": False,
            "supports_ppm": False,
            "extended_irig_available": False,
            "available_options": [],
        }

        try:
            signal_select = self.page.locator(f"select[name='signal{channel}']")
            if signal_select.is_visible():
                options = signal_select.locator("option")
                for i in range(options.count()):
                    option_text = options.nth(i).inner_text().upper()
                    option_value = options.nth(i).get_attribute("value") or ""

                    capabilities["available_options"].append(
                        {"value": option_value, "text": options.nth(i).inner_text()}
                    )

                    # Check for specific capabilities
                    if "PPS" in option_text:
                        capabilities["supports_pps"] = True
                    if "IRIG" in option_text:
                        capabilities["supports_irig"] = True
                        # Check for extended IRIG options (Series 3)
                        if any(
                            x in option_text
                            for x in [
                                "IRIG-B120",
                                "IRIG-B122",
                                "IRIG-B124",
                                "IRIG-B126",
                            ]
                        ):
                            capabilities["extended_irig_available"] = True
                    if any(
                        freq in option_text for freq in ["MHZ", "KHZ", "HZ", "FREQ"]
                    ):
                        capabilities["supports_frequency"] = True
                    if "PPM" in option_text:
                        capabilities["supports_ppm"] = True

        except Exception as e:
            print(f"Error detecting capabilities for channel {channel}: {e}")

        return capabilities

    def get_save_button_locator(self):
        """
        Get device-aware save button locator.

        Series 2: Uses input#button_save (input element with type="button")
        Series 3: Uses button#button_save (button element)

        Returns:
            Locator for save button (works for both device types)
        """
        device_series = self.get_device_series()

        # Try Series 3 button element first if device supports it
        if "Series 3" in device_series:
            save_button = self.page.locator("button#button_save")
            if save_button.count() > 0:
                print("Using Series 3 button#button_save")
                return save_button

        # Fallback to Series 2 input element
        save_button = self.page.locator("input#button_save")
        if save_button.count() > 0:
            print("Using Series 2 input#button_save")
            return save_button

        # Final fallback - try by role and text
        save_button = self.page.get_by_role("button", name="Save")
        return save_button

    def verify_page_loaded(self):
        """Verify outputs configuration page has loaded successfully."""
        try:
            # Device has signal1 select with specific name/id
            signal1_select = self.page.locator("select[name='signal1']")

            timeout = int(self.DEFAULT_TIMEOUT * self.timeout_multiplier)
            expect(signal1_select).to_be_visible(timeout=timeout)

            print(
                f"Outputs configuration page verification completed for {self.get_device_series()}"
            )

            # Additional verification: check output count matches expectations
            actual_capabilities = self.detect_output_capabilities()
            actual_count = actual_capabilities.get("output_channels", 0)

            if (
                hasattr(self, "expected_output_count")
                and actual_count != self.expected_output_count
            ):
                print(
                    f"Warning: Expected {self.expected_output_count} outputs, found {actual_count}"
                )

        except Exception as e:
            print(f"Warning: Outputs config page verification failed: {e}")

    def get_page_data(self) -> Dict[str, str]:
        """Extract outputs configuration data from the page."""
        page_data = {
            "device_series": self.get_device_series(),
            "device_model": self.device_model,
        }

        try:
            capabilities = self.detect_output_capabilities()
            output_count = capabilities.get("output_channels", 0)

            # Extract signal configurations for available channels
            for channel in range(1, output_count + 1):
                signal_select = self.page.locator(f"select[name='signal{channel}']")
                if signal_select.is_visible():
                    selected_option = signal_select.locator("option:checked")
                    if selected_option.is_visible():
                        page_data[f"signal{channel}"] = (
                            selected_option.get_attribute("value") or ""
                        )

                # Extract time reference (radio button)
                time_radios = self.page.locator(f"input[name='time{channel}']")
                for i in range(time_radios.count()):
                    radio = time_radios.nth(i)
                    if radio.is_checked():
                        page_data[f"time{channel}"] = radio.get_attribute("value") or ""
                        break

        except Exception as e:
            print(f"Error getting outputs configuration page data: {e}")

        return page_data

    def configure_output(
        self, channel: int, signal_type: str, time_reference: str = "UTC", **kwargs
    ) -> bool:
        """
        Configure output signal for a specific channel.

         with device-aware patterns and comprehensive error handling.

        Args:
            channel: Output channel number (1-2 for Series 2, 1-6 for Series 3)
            signal_type: Signal type (Series 2: OFF, IRIG-B variants, PPS, PPM | Series 3: + extended options)
            time_reference: Time reference (UTC or LOCAL)

        Returns:
            True if configuration successful, False otherwise
        """
        try:
            # Verify channel is valid for this device
            capabilities = self.detect_output_capabilities()
            if channel > capabilities["output_channels"]:
                print(
                    f"Error: Channel {channel} not available on {self.get_device_series()} (max: {capabilities['output_channels']})"
                )
                return False

            self.start_performance_tracking(f"configure_output_{channel}")

            # Select signal type with device-aware timeout
            signal_select = self.page.locator(f"select[name='signal{channel}']")
            timeout = int(self.DEFAULT_TIMEOUT * self.timeout_multiplier)
            expect(signal_select).to_be_visible(timeout=timeout)

            if not self.safe_select_option(
                signal_select, signal_type, context=f"signal{channel}"
            ):
                return False

            # Select time reference (radio button)
            time_radio = self.page.locator(
                f"input[name='time{channel}'][value='{time_reference}']"
            )
            expect(time_radio).to_be_visible(timeout=timeout)

            if not self.safe_click(
                time_radio, context=f"time{channel}_{time_reference}"
            ):
                return False

            self.end_performance_tracking(f"configure_output_{channel}")
            print(f"Output {channel} configured: {signal_type}, {time_reference}")
            return True

        except Exception as e:
            print(f"Error configuring output {channel}: {e}")
            self.end_performance_tracking(f"configure_output_{channel}")
            return False

    def save_configuration_with_modification(
        self,
        channel: int = 1,
        signal_type_original: Optional[str] = None,
        signal_type_modified: Optional[str] = None,
    ) -> bool:
        """
        Save outputs configuration changes with automatic modification if needed.

         with device-aware patterns and timeout management.

        The save button is only enabled after user makes configuration changes.
        This method ensures changes are made before attempting to save.
        """
        try:
            timeout = int(
                self.DEFAULT_TIMEOUT * self.timeout_multiplier * 2
            )  # Extended for save operations

            # Get current signal type if not provided
            if signal_type_original is None:
                capabilities = self.detect_output_capabilities()
                if channel <= capabilities["output_channels"]:
                    current_data = self.get_page_data()
                    signal_type_original = current_data.get(f"signal{channel}")

                    if signal_type_original:
                        # Choose a different signal type to modify
                        available_types = self.get_available_signal_types(channel)
                        signal_type_modified = None

                        # Find a different available type
                        for type_info in available_types:
                            if type_info["value"] != signal_type_original:
                                signal_type_modified = type_info["value"]
                                break

                        if signal_type_modified:
                            print(
                                f"CRITICAL FIX: Modifying signal{channel} from {signal_type_original} to {signal_type_modified} to enable save button"
                            )

                            # Make the configuration change
                            if not self.configure_output(channel, signal_type_modified):
                                print(
                                    "Failed to modify configuration - cannot enable save button"
                                )
                                return False

                            # Allow JavaScript to process the change and enable save button
                            time.sleep(2)

            # Now attempt to save with the enabled button
            return self.save_configuration()

        except Exception as e:
            print(f"Error saving outputs configuration with modification: {e}")
            return False

    def save_configuration(self) -> bool:
        """Save outputs configuration changes."""
        try:
            # Use  save button detection with device-aware patterns
            save_button = self.get_save_button_locator()
            timeout = int(self.DEFAULT_TIMEOUT * self.timeout_multiplier * 2)

            if save_button.count() > 0:
                if self.safe_click(
                    save_button, context="save_outputs_config", timeout=timeout
                ):
                    time.sleep(1)
                    print("Outputs configuration saved successfully")
                    return True
                else:
                    print("Error: Could not click save button on outputs config page")
                    return False
            else:
                print("Error: Save button not found on outputs config page")
                return False

        except Exception as e:
            print(f"Error saving outputs configuration: {e}")
            return False

    def get_available_signal_types(self, channel: int = 1) -> list:
        """Get list of available signal types for a specific channel."""
        signal_types = []

        try:
            signal_select = self.page.locator(f"select[name='signal{channel}']")
            if signal_select.is_visible():
                options = signal_select.locator("option")
                for i in range(options.count()):
                    option = options.nth(i)
                    value = option.get_attribute("value") or ""
                    text = option.inner_text()
                    signal_types.append({"value": value, "text": text})

        except Exception as e:
            print(f"Error getting available signal types: {e}")

        return signal_types

    def navigate_to_page(self):
        """Navigate to outputs configuration page."""
        try:
            # Note: Device has link with text "Outputs"
            outputs_link = self.page.get_by_role("link", name="Outputs")
            timeout = int(self.DEFAULT_TIMEOUT * self.timeout_multiplier)
            expect(outputs_link).to_be_visible(timeout=timeout)

            if self.safe_click(outputs_link, context="navigate_outputs_config"):
                self.wait_for_page_load()
                self.verify_page_loaded()

        except Exception as e:
            print(f"Error navigating to outputs configuration page: {e}")

    def configure_all_outputs(
        self, signal_types: List[str], time_references: Optional[List[str]] = None
    ) -> bool:
        """
        Configure all available output channels.

        Args:
            signal_types: List of signal types for each channel
            time_references: Optional list of time references (defaults to UTC for all)

        Returns:
            True if all configurations successful, False otherwise
        """
        if time_references is None:
            time_references = ["UTC"] * len(signal_types)

        try:
            capabilities = self.detect_output_capabilities()
            max_channels = capabilities["output_channels"]

            if len(signal_types) != len(time_references):
                print("Error: signal_types and time_references must have same length")
                return False

            if len(signal_types) > max_channels:
                print(
                    f"Error: Cannot configure {len(signal_types)} channels on {self.get_device_series()} (max: {max_channels})"
                )
                return False

            success_count = 0
            for i, (signal_type, time_ref) in enumerate(
                zip(signal_types, time_references), 1
            ):
                if self.configure_output(i, signal_type, time_ref):
                    success_count += 1
                else:
                    print(f"Failed to configure output {i}")

            return success_count == len(signal_types)

        except Exception as e:
            print(f"Error configuring all outputs: {e}")
            return False

    def get_all_signal_types_by_channel(self) -> Dict[str, list]:
        """Get signal types for all available channels."""
        all_types = {}

        try:
            capabilities = self.detect_output_capabilities()
            for channel in range(1, capabilities["output_channels"] + 1):
                all_types[f"channel_{channel}"] = self.get_available_signal_types(
                    channel
                )

        except Exception as e:
            print(f"Error getting signal types for all channels: {e}")

        return all_types
