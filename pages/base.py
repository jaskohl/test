"""
Base page object for Kronos device test automation.

Provides common functionality used across all page objects including:
- Error handling and debug capture
- Performance tracking and timing
- Satellite loading detection
- Configuration section management
- Common utility methods

"""

from playwright.sync_api import Page, expect, TimeoutError
from typing import Dict, List, Optional, Tuple, Union, Any
from datetime import datetime
import time
import re
import json
import os

# Import centralized device capability system
from pages.device_capabilities import DeviceCapabilities


class BasePage:
    """
    Base page object class providing common functionality for all Kronos device pages.

    This class implements the core patterns established in the project:
    - User-facing locators (get_by_role, get_by_label, get_by_text)
    - Comprehensive error handling with debug capture
    - Performance tracking and timing measurements
    - Embedded device constraint handling (satellite loading, etc.)
    - Dynamic interface adaptation
    """

    def __init__(self, page: Page, device_model: Optional[str] = None):
        """
        Initialize base page object.

        Args:
            page: Playwright page object
            device_model: Device model for device-aware behavior (e.g., "KRONOS-2R-HVXX-A2F")
        """
        self.page = page
        self.device_model = device_model

        # Use centralized device capability system for device-aware behavior
        if self.device_model:
            self.device_capabilities = DeviceCapabilities.get_capabilities(
                self.device_model
            )
            self.device_series = DeviceCapabilities.get_series(self.device_model)
        else:
            # Fallback detection for backward compatibility
            self.device_capabilities = {}
            self.device_series = self._detect_device_series_fallback()

        # Device-aware timeouts - Series 3 devices are slower due to additional features
        if self.device_series == "Series 3":
            self.DEFAULT_TIMEOUT = 90000  # 90 seconds for Series 3
            self.SHORT_TIMEOUT = 10000  # 10 seconds for quick operations
            self.LONG_TIMEOUT = 120000  # 120 seconds for satellite operations
        else:
            self.DEFAULT_TIMEOUT = 30000  # 30 seconds for Series 2
            self.SHORT_TIMEOUT = 5000  # 5 seconds for quick operations
            self.LONG_TIMEOUT = 60000  # 60 seconds for satellite operations

        # Performance tracking
        self.start_time = None
        self.operation_times = {}

        # Debug information
        self.debug_info = {}

    def _detect_device_series_fallback(self) -> str:
        """
        Fallback method for device series detection when device_model not provided.
        DEPRECATED: Use device_capabilities.py instead.

        This method is kept for backward compatibility only.
        """
        try:
            title = self.page.title()
            if "Series 2" in title:
                return "Series 2"
            elif "Series 3" in title:
                return "Series 3"
            return "Unknown"
        except Exception:
            return "Unknown"

    def get_device_info(self) -> Dict[str, Any]:
        """
        Get complete device information using centralized system.

        Returns:
            Dictionary with device capabilities and series information
        """
        if self.device_model:
            return DeviceCapabilities.get_device_info(self.device_model)
        else:
            return {
                "series": self.device_series,
                "model": "Unknown",
                "capabilities": self.device_capabilities,
            }

    def start_performance_tracking(self, operation_name: str):
        """
        Start tracking performance for an operation.

        Args:
            operation_name: Name of the operation to track
        """
        self.start_time = time.time()
        self.operation_times[operation_name] = {
            "start": self.start_time,
            "end": None,
            "duration": None,
        }

    def end_performance_tracking(self, operation_name: str) -> float:
        """
        End tracking performance for an operation.

        Args:
            operation_name: Name of the operation being tracked

        Returns:
            Duration in seconds
        """
        if self.start_time is None:
            return 0.0

        end_time = time.time()
        duration = end_time - self.start_time

        if operation_name in self.operation_times:
            self.operation_times[operation_name]["end"] = end_time
            self.operation_times[operation_name]["duration"] = duration

        self.start_time = None
        return duration

    def _capture_debug_info(
        self,
        context: str = "unknown",
        test_context: Optional[Dict[str, str]] = None,
        failure_reason: str = "unknown_failure",
    ):
        """
        Capture debug information for troubleshooting ONLY during actual failures/errors.

        Args:
            context: Context description for the debug capture
            test_context: Optional dictionary containing test identification information:
                - test_function_name: Name of the test function
                - test_class_name: Name of the test class
                - test_file: Test file name
                - device_ip: Device IP address being tested
                - device_model: Device model being tested
            failure_reason: Description of what specifically failed/error occurred
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        try:
            # Capture page state
            debug_data = {
                "timestamp": timestamp,
                "context": context,
                "failure_reason": failure_reason,
                "url": self.page.url,
                "title": self.page.title(),
                "viewport_size": self.page.viewport_size,
                "page_content": self.page.content()[:2000],  # First 2KB
                "performance_times": self.operation_times.copy(),
                "device_model": self.device_model,
                "device_series": self.device_series,
            }

            # Add test context if provided
            if test_context:
                debug_data["test_context"] = test_context
            else:
                debug_data["test_context"] = {
                    "note": "No test context provided - enable test context passing for enhanced debugging"
                }

            # Add screenshot if possible
            try:
                screenshot_path = f"debug_{context}_{timestamp}.png"
                self.page.screenshot(path=screenshot_path)
                debug_data["screenshot"] = screenshot_path
            except Exception as e:
                debug_data["screenshot_error"] = str(e)

            # Save debug info
            debug_filename = f"debug_{context}_{timestamp}.json"
            with open(debug_filename, "w") as f:
                json.dump(debug_data, f, indent=2, default=str)

            print(f"Debug info captured: {debug_filename}")

        except Exception as e:
            print(f"Error capturing debug info: {e}")

    def wait_for_page_load(self, timeout: Optional[int] = None) -> bool:
        """
        Wait for page to load completely.

        Args:
            timeout: Timeout in milliseconds (uses DEFAULT_TIMEOUT if None)

        Returns:
            True if page loaded, False if timeout
        """
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        try:
            # Wait for body to be visible and stable
            body = self.page.locator("body")
            expect(body).to_be_visible(timeout=timeout)

            # Wait for no loading indicators
            loading_indicators = [
                "text=Loading",
                "text=Please wait",
                "[class*=loading]",
                "[class*=spinner]",
                "[id*=loading]",
            ]

            for indicator in loading_indicators:
                try:
                    loading_element = self.page.locator(indicator)
                    expect(loading_element).to_be_hidden(timeout=self.SHORT_TIMEOUT)
                except (TimeoutError, Exception):
                    # Loading indicator not found or still visible, continue
                    pass

            return True

        except Exception as e:
            print(f"Page load timeout or error: {e}")
            self._capture_debug_info(
                "page_load_failure", failure_reason=f"Page load failed: {str(e)}"
            )
            return False

    def wait_for_satellite_loading(self, timeout: Optional[int] = None) -> bool:
        """
        Wait for satellite loading to complete using multiple detection methods.

        Args:
            timeout: Timeout in milliseconds (uses LONG_TIMEOUT if None)

        Returns:
            True if loading completed, False if timeout
        """

        # ENHANCED: Longer timeout for all devices to handle slower initialization
        max_wait_time = 20000  # 20 seconds (increased from 5 seconds)
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

                # SECOND: Check for Configure button using exact selector from device
                configure_button = self.page.locator('a[href="login"][title*="locked"]')
                if configure_button.is_visible():
                    return True

                # THIRD: Generic Configure link
                configure_generic = self.page.locator(
                    'a[href="login"]:has-text("Configure")'
                )
                if configure_generic.is_visible():
                    return True

                # FOURTH: Dashboard content
                dashboard_elements = [
                    "h3:has-text('Time')",  # Time section header
                    "h3:has-text('Status')",  # Status section header
                    "h3:has-text('General')",  # General section header
                    "#Main_Header",  # Main header element
                    ".main-header",  # Header CSS class
                ]

                for element_selector in dashboard_elements:
                    element = self.page.locator(element_selector)
                    if element.is_visible():
                        return True

                # FIFTH: Basic page structure with device content
                try:
                    body = self.page.locator("body")
                    if body.is_visible():
                        text_content = body.text_content()
                        if text_content:
                            content = text_content.strip()
                            if len(content) > 100 and any(
                                word in content.lower()
                                for word in ["kronos", "time", "status", "gnss"]
                            ):
                                return True
                except Exception:
                    pass

            except Exception as e:
                print(f"Error during verification check: {e}")

            time.sleep(check_interval / 1000)  # Convert to seconds
        return False

    def safe_click(
        self, locator, timeout: Optional[int] = None, context: str = "click"
    ) -> bool:
        """
        Safely click an element with error handling.

        Args:
            locator: Playwright locator to click
            timeout: Timeout in milliseconds
            context: Context description for error handling

        Returns:
            True if click successful, False otherwise
        """
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        try:
            expect(locator).to_be_visible(timeout=timeout)
            expect(locator).to_be_enabled(timeout=timeout)
            locator.click()
            return True

        except Exception as e:
            print(f"Click failed ({context}): {e}")
            return False

    def safe_fill(
        self, locator, value: str, timeout: Optional[int] = None, context: str = "fill"
    ) -> bool:
        """
        Safely fill a text field with error handling and change event triggering.

        Args:
            locator: Playwright locator to fill
            value: Value to enter
            timeout: Timeout in milliseconds
            context: Context description for error handling

        Returns:
            True if fill successful, False otherwise
        """
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        try:
            expect(locator).to_be_visible(timeout=timeout)
            expect(locator).to_be_editable(timeout=timeout)

            # Fill the field and trigger change events for device firmware
            locator.fill(value)

            # Trigger change events that device firmware expects
            locator.dispatch_event("input")  # For real-time validation
            locator.dispatch_event("change")  # For form state management
            locator.dispatch_event("blur")  # When field loses focus

            return True

        except Exception as e:
            print(f"Fill failed ({context}): {e}")
            return False

    def safe_select_option(
        self,
        locator,
        option: str,
        timeout: Optional[int] = None,
        context: str = "select",
    ) -> bool:
        """
        Safely select an option from a dropdown with error handling.

        Args:
            locator: Playwright locator for the select element
            option: Option value or text to select
            timeout: Timeout in milliseconds
            context: Context description for error handling

        Returns:
            True if selection successful, False otherwise
        """
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        try:
            expect(locator).to_be_visible(timeout=timeout)
            expect(locator).to_be_enabled(timeout=timeout)
            locator.select_option(option)
            return True

        except Exception as e:
            print(f"Select failed ({context}): {e}")
            return False

    def find_save_button(self, section_context: Optional[str] = None) -> Optional[Any]:
        """
        Enhanced save button detection with comprehensive section-aware patterns and device-specific handling.

        Based on debug file analysis and Kronos UI structure analysis showing save button failures in:
        - DST configuration sections (button#button_save_2)
        - Timezone configuration sections (button#button_save_1)
        - Output configuration sections (button#button_save)
        - SNMP configuration sections (button#button_save_1, button#button_save_2, button#button_save_3)
        - General configuration sections (button#button_save)

        ENHANCED PATTERNS:
        1. Device-specific patterns (Series 2 vs Series 3 differences)
        2. Section-specific patterns based on actual UI structure
        3. Bootstrap collapsible panel handling
        4. Multiple save button disambiguation

        Args:
            section_context: Optional section context for targeted save button detection
                - "timezone" for timezone configuration (button#button_save_1)
                - "dst" for DST configuration (button#button_save_2)
                - "general" for general configuration (button#button_save)
                - "network" for network configuration (button#button_save)
                - "outputs" for outputs configuration (button#button_save)
                - "gnss" for GNSS configuration (button#button_save)
                - "snmp_v1", "snmp_traps", "snmp_v3" for SNMP sections
                - "ptp" for PTP configuration (button#button_save)
                - "time" for time configuration (generic save)

        Returns:
            Playwright locator for the save button, or None if not found
        """
        # ENHANCED SECTION-AWARE SAVE BUTTON PATTERNS
        save_button_patterns = []

        if section_context:
            section_context = section_context.lower()

            # DEVICE-SPECIFIC PATTERNS - Series 2 vs Series 3 differences
            if self.device_series == "Series 2":
                # Series 2 often uses input elements for save buttons
                if section_context in ["timezone", "dst"]:
                    save_button_patterns.extend(
                        [
                            # Series 2 specific: button#button_save_1 (timezone), button#button_save_2 (dst)
                            f'input#button_save_{"1" if section_context == "timezone" else "2"}',
                            f'button#button_save_{"1" if section_context == "timezone" else "2"}',
                            # Section-aware text patterns
                            f'input[type="submit"][value="Save"]:near(text="{section_context.title()}")',
                            f'button:has-text("Save"):near(text="{section_context.title()}")',
                            # Panel-aware patterns
                            f'input[type="submit"][value="Save"]:near(h4:has-text("{section_context.title()}"))',
                            f'button:has-text("Save"):near(h4:has-text("{section_context.title()}"))',
                        ]
                    )
                elif section_context in ["general", "network", "outputs", "gnss"]:
                    # Series 2 single save button sections
                    save_button_patterns.extend(
                        [
                            "input#button_save",
                            "button#button_save",
                            'input[type="submit"][value="Save"]',
                            'button:has-text("Save")',
                            # Section-specific patterns
                            f'input[type="submit"][value="Save"]:near(h3:has-text("{section_context.title()}"))',
                            f'button:has-text("Save"):near(h3:has-text("{section_context.title()}"))',
                        ]
                    )
                elif "snmp" in section_context:
                    # SNMP sections (3 separate save buttons)
                    snmp_index = {"snmp_v1": "1", "snmp_traps": "2", "snmp_v3": "3"}
                    if section_context in snmp_index:
                        idx = snmp_index[section_context]
                        save_button_patterns.extend(
                            [
                                f"input#button_save_{idx}",
                                f"button#button_save_{idx}",
                                f'input[type="submit"][value="Save"]:near(h4:has-text("SNMP v{idx if idx != "3" else "3"}"))',
                                f'button:has-text("Save"):near(h4:has-text("SNMP v{idx if idx != "3" else "3"}"))',
                            ]
                        )
            else:  # Series 3
                # Series 3 often uses button elements for save buttons
                if section_context in ["timezone", "dst"]:
                    save_button_patterns.extend(
                        [
                            # Series 3 specific: button#button_save_1 (timezone), button#button_save_2 (dst)
                            f'button#button_save_{"1" if section_context == "timezone" else "2"}',
                            f'input#button_save_{"1" if section_context == "timezone" else "2"}',
                            # Section-aware text patterns
                            f'button:has-text("Save"):near(text="{section_context.title()}")',
                            f'input[type="submit"][value="Save"]:near(text="{section_context.title()}")',
                            # Bootstrap panel patterns
                            f'button:has-text("Save"):near(h4:has-text("{section_context.title()}"))',
                            f'input[type="submit"][value="Save"]:near(h4:has-text("{section_context.title()}"))',
                        ]
                    )
                elif section_context in [
                    "general",
                    "network",
                    "outputs",
                    "gnss",
                    "ptp",
                ]:
                    # Series 3 single save button sections
                    save_button_patterns.extend(
                        [
                            "button#button_save",
                            "input#button_save",
                            'button:has-text("Save")',
                            'input[type="submit"][value="Save"]',
                            # Section-specific patterns
                            f'button:has-text("Save"):near(h3:has-text("{section_context.title()}"))',
                            f'input[type="submit"][value="Save"]:near(h3:has-text("{section_context.title()}"))',
                        ]
                    )
                elif "snmp" in section_context:
                    # SNMP sections (3 separate save buttons)
                    snmp_index = {"snmp_v1": "1", "snmp_traps": "2", "snmp_v3": "3"}
                    if section_context in snmp_index:
                        idx = snmp_index[section_context]
                        save_button_patterns.extend(
                            [
                                f"button#button_save_{idx}",
                                f"input#button_save_{idx}",
                                f'button:has-text("Save"):near(h4:has-text("SNMP v{idx if idx != "3" else "3"}"))',
                                f'input[type="submit"][value="Save"]:near(h4:has-text("SNMP v{idx if idx != "3" else "3"}"))',
                            ]
                        )

            # ENHANCED SECTION-SPECIFIC PATTERNS (Device-agnostic)
            if section_context == "timezone":
                save_button_patterns.extend(
                    [
                        # Bootstrap collapsible panel patterns
                        'button:has-text("Save"):near(#timezone_collapse)',
                        'input[type="submit"][value="Save"]:near(#timezone_collapse)',
                        'button:has-text("Save"):near([href="#timezone_collapse"])',
                        # Field proximity patterns
                        'button:has-text("Save"):near(input[name="timezones"])',
                        'button:has-text("Save"):near(input[name="std_name"])',
                    ]
                )
            elif section_context == "dst":
                save_button_patterns.extend(
                    [
                        # Bootstrap collapsible panel patterns
                        'button:has-text("Save"):near(#dst_collapse)',
                        'input[type="submit"][value="Save"]:near(#dst_collapse)',
                        'button:has-text("Save"):near([href="#dst_collapse"])',
                        # Field proximity patterns
                        'button:has-text("Save"):near(input[name="dst_name"])',
                    ]
                )
            elif section_context == "outputs":
                save_button_patterns.extend(
                    [
                        # Output-specific patterns
                        'button:has-text("Save"):near(select[name="signal1"])',
                        'button:has-text("Save"):near(select[name="signal2"])',
                        'button:has-text("Save"):near(h3:has-text("Output"))',
                        # Series 3 multi-output patterns
                        'button:has-text("Save"):near(select[name="signal3"])',
                        'button:has-text("Save"):near(select[name="signal4"])',
                    ]
                )
            elif section_context == "general":
                save_button_patterns.extend(
                    [
                        # General config specific patterns
                        'button:has-text("Save"):near(input[name="identifier"])',
                        'button:has-text("Save"):near(input[name="location"])',
                        'button:has-text("Save"):near(input[name="contact"])',
                    ]
                )
            elif section_context == "network":
                save_button_patterns.extend(
                    [
                        # Network config specific patterns
                        'button:has-text("Save"):near(select[name="mode"])',  # Series 2
                        'button:has-text("Save"):near(input[name="ip_eth0"])',  # Series 3
                        'button:has-text("Save"):near(input[name="sfp_mode"])',
                    ]
                )
            elif section_context == "gnss":
                save_button_patterns.extend(
                    [
                        # GNSS config specific patterns
                        'button:has-text("Save"):near(input[name="gps"])',
                        'button:has-text("Save"):near(input[name="galileo"])',
                        'button:has-text("Save"):near(input[name="ant_delay"])',
                    ]
                )
            elif section_context == "ptp":
                save_button_patterns.extend(
                    [
                        # PTP config specific patterns
                        'button:has-text("Save"):near(select[name="profile"])',
                        'button:has-text("Save"):near(input[name="domain"])',
                        'button:has-text("Save"):near(input[name="ptp_enable"])',
                    ]
                )

        # ENHANCED FALLBACK PATTERNS - Comprehensive coverage
        fallback_patterns = [
            # PRIMARY: Exact ID patterns (most reliable)
            "button#button_save",
            "input#button_save",
            'button[id*="button_save"]',
            'input[id*="button_save"]',
            # PRIMARY: Text-based patterns (user-facing)
            'button:has-text("Save")',
            'input[type="submit"][value="Save"]',
            'input[type="button"][value="Save"]',
            # ALTERNATIVE: Apply/Submit variations
            'button:has-text("Apply")',
            'input[type="submit"][value="Apply"]',
            'button:has-text("Submit")',
            'input[type="submit"][value="Submit"]',
            'button:has-text("Confirm")',
            'input[type="submit"][value="Confirm"]',
            # CONTEXTUAL: Form and section contexts
            'form button:has-text("Save")',
            'form input[type="submit"][value="Save"]',
            '.form-actions button:has-text("Save")',
            '.form-actions input[type="submit"][value="Save"]',
            '.panel-footer button:has-text("Save")',
            '.panel-footer input[type="submit"][value="Save"]',
            # CONFIGURATION: Panel and section patterns
            '.config-panel button:has-text("Save")',
            '.configuration-panel button:has-text("Save")',
            '[class*="config"] button:has-text("Save")',
            # ATTRIBUTE: ID and class patterns
            'button[id*="save"]',
            'input[id*="save"][type="submit"]',
            'button[class*="save"]',
            'input[class*="save"][type="submit"]',
            # SECTION: Section-based patterns
            'section button:has-text("Save")',
            '.section button:has-text("Save")',
        ]

        # Combine section-specific patterns with fallback patterns
        all_patterns = save_button_patterns + fallback_patterns

        # Try each pattern until we find a visible, enabled save button
        for pattern in all_patterns:
            try:
                save_locator = self.page.locator(pattern)

                # Check if the element exists and is visible/enabled
                if save_locator.count() > 0:
                    # Try to get the first visible, enabled element
                    for i in range(save_locator.count()):
                        element = save_locator.nth(i)
                        if element.is_visible() and element.is_enabled():
                            print(f"Found save button using pattern: {pattern}")
                            return element

            except Exception as e:
                # Pattern didn't match, try next one
                continue

        # If no save button found with patterns, try a final comprehensive search
        try:
            # Look for any button or input submit that contains save-related text
            all_buttons = self.page.locator(
                'button, input[type="submit"], input[type="button"]'
            )

            for i in range(all_buttons.count()):
                element = all_buttons.nth(i)
                if element.is_visible() and element.is_enabled():
                    text_content = (
                        element.get_attribute("value") or element.text_content() or ""
                    )
                    text_content = text_content.lower().strip()

                    # Check for save-related keywords
                    if any(
                        keyword in text_content
                        for keyword in ["save", "apply", "submit", "confirm"]
                    ):
                        print(
                            f"Found save button via comprehensive search: {text_content}"
                        )
                        return element

        except Exception:
            pass

        return None

    def safe_save_click(
        self,
        section_context: Optional[str] = None,
        timeout: Optional[int] = None,
        context: str = "save",
    ) -> bool:
        """
        Enhanced save button clicking with section-aware detection and comprehensive fallbacks.

        Addresses save button failures identified in debug files:
        - debug_dst_config_save_error_*.json
        - debug_timezone_config_save_error_*.json
        - debug_outputs_config_save_error_*.json

        Args:
            section_context: Section context for targeted save button detection
            timeout: Timeout in milliseconds
            context: Context description for error handling

        Returns:
            True if save successful, False otherwise
        """
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        try:
            # Try to find save button with section-aware patterns
            save_button = self.find_save_button(section_context)

            if save_button:
                print(
                    f"Attempting to click save button for section: {section_context or 'unknown'}"
                )

                # Ensure the button is visible and enabled before clicking
                expect(save_button).to_be_visible(timeout=timeout)
                expect(save_button).to_be_enabled(timeout=timeout)

                # Click the save button
                save_button.click()

                # Wait a moment for the save operation to process
                time.sleep(1)

                print(
                    f"Save button clicked successfully for section: {section_context or 'unknown'}"
                )
                return True
            else:
                # No save button found - capture debug info for analysis
                failure_reason = (
                    f"Save button not found for section: {section_context or 'unknown'}"
                )
                print(f"Save operation failed: {failure_reason}")

                self._capture_debug_info(
                    context=f"{section_context or 'unknown'}_save_button_not_found",
                    failure_reason=failure_reason,
                )
                return False

        except Exception as e:
            # Save button click failed - capture debug info
            failure_reason = f"Save button click failed: {str(e)}"
            print(f"Save operation failed ({context}): {e}")

            self._capture_debug_info(
                context=f"{section_context or 'unknown'}_save_button_error",
                failure_reason=failure_reason,
            )
            return False

    def wait_for_save_completion(self, timeout: Optional[int] = None) -> bool:
        """
        Wait for save operation completion with loading state detection.

        Args:
            timeout: Timeout in milliseconds

        Returns:
            True if save completed successfully, False if timeout or error
        """
        if timeout is None:
            timeout = self.SHORT_TIMEOUT

        try:
            start_time = time.time()

            while (time.time() - start_time) * 1000 < timeout:
                # Check for loading indicators
                loading_indicators = [
                    "[class*='saving']",
                    "[class*='loading']",
                    "text=Saving",
                    "text=Please wait",
                    "[class*='spinner']",
                ]

                loading_found = False
                for indicator in loading_indicators:
                    try:
                        loading_element = self.page.locator(indicator)
                        if loading_element.is_visible():
                            loading_found = True
                            break
                    except Exception:
                        continue

                if not loading_found:
                    # No loading indicators - save likely complete
                    return True

                time.sleep(0.5)

            # Timeout waiting for save completion
            return False

        except Exception as e:
            print(f"Error during save completion wait: {e}")
            return False

    def _get_device_behavior_data(self) -> Dict[str, Any]:
        """
        Get device-specific behavioral data from unused device capabilities.

        Returns:
            Dictionary containing dynamic UI behaviors, state transition timing,
            and performance expectations for this device model
        """
        if not self.device_model:
            return {}

        try:
            behavior_data = DeviceCapabilities.get_behavior_data(self.device_model)
            timing_data = DeviceCapabilities.get_state_transition_timing(
                self.device_model
            )
            performance_data = DeviceCapabilities.get_performance_expectations(
                self.device_model
            )

            return {
                "dynamic_ui_behaviors": behavior_data.get("dynamic_ui_behaviors", {}),
                "state_transition_timing": timing_data,
                "performance_expectations": performance_data.get(
                    "authentication_performance", {}
                ),
                "satellite_loading_behavior": behavior_data.get(
                    "satellite_loading_behavior", {}
                ),
            }
        except Exception as e:
            print(f"Error getting device behavior data: {e}")
            return {}

    def _get_form_change_patterns(self, section_context: str) -> Dict[str, Any]:
        """
        Get device-specific form change detection patterns for a section.

        Args:
            section_context: Section context (timezone, dst, general, etc.)

        Returns:
            Dictionary with form change patterns for this device and section
        """
        behavior_data = self._get_device_behavior_data()
        ui_behaviors = behavior_data.get("dynamic_ui_behaviors", {})

        # Default patterns if device-specific data not available
        default_patterns = {
            "change_events": ["input", "change", "blur"],
            "save_button_states": {
                "disabled": "[disabled]",
                "enabled": ":not([disabled])",
                "hidden": ":hidden",
            },
            "legitimate_change_required": True,
            "change_detection_method": "substantial_value_difference",
        }

        # Get section-specific patterns
        section_patterns = ui_behaviors.get(f"{section_context}_page", {})
        if not section_patterns:
            section_patterns = ui_behaviors.get("form_save_enablement", {})

        # Merge with defaults
        patterns = default_patterns.copy()
        patterns.update(section_patterns)

        return patterns

    def _wait_for_save_button_enabled(
        self, save_button_locator, timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for save button to become enabled using device-specific timing.

        Args:
            save_button_locator: Locator for the save button
            timeout: Timeout in milliseconds

        Returns:
            True if save button became enabled, False if timeout
        """
        if timeout is None:
            # Use device-specific timing if available
            behavior_data = self._get_device_behavior_data()
            timing_data = behavior_data.get("state_transition_timing", {})
            form_timing = timing_data.get("form_change_to_save_enable", {})

            # Default timeout with device-aware adjustments
            base_timeout = 10000  # 10 seconds base
            timeout_multiplier = (
                DeviceCapabilities.get_timeout_multiplier(self.device_model)
                if self.device_model
                else 1.0
            )
            timeout = int(base_timeout * timeout_multiplier)
        else:
            timeout = int(timeout)

        try:
            start_time = time.time()

            while (time.time() - start_time) * 1000 < timeout:
                # Check if save button is now enabled
                if save_button_locator.count() > 0:
                    element = save_button_locator.first
                    if element.is_visible() and element.is_enabled():
                        print("Save button enabled after form change")
                        return True

                time.sleep(0.5)  # Check every 500ms

            print("Timeout waiting for save button to become enabled")
            return False

        except Exception as e:
            print(f"Error waiting for save button enablement: {e}")
            return False

    def trigger_legitimate_form_change(
        self, field_locator, new_value: str, context: str = "form_change"
    ) -> bool:
        """
        Trigger a legitimate form change that will enable save buttons.

        This replaces the flawed "_enable_and_click_save_button" logic that used
        fake space changes. Instead, it makes real value changes that trigger
        proper JavaScript change events.

        Args:
            field_locator: Locator for the form field
            new_value: New value to set (must be different from current)
            context: Context description for error handling

        Returns:
            True if change was successful and triggers save enablement, False otherwise
        """
        try:
            # Get current value
            if field_locator.count() == 0:
                print(f"Form field not found for {context}")
                return False

            current_value = field_locator.input_value()

            # Only proceed if we're making a real change
            if current_value == new_value:
                print(f"No change needed for {context} - values are the same")
                return True

            # Make the legitimate change
            print(
                f"Making legitimate form change for {context}: '{current_value}' -> '{new_value}'"
            )

            # Clear field first to ensure clean change
            field_locator.clear()

            # Fill with new value
            field_locator.fill(new_value)

            # Trigger proper change events that device firmware expects
            field_locator.dispatch_event("input")  # Real-time validation
            field_locator.dispatch_event("change")  # Form state management
            field_locator.dispatch_event("blur")  # Field loses focus

            # Wait for device to process the change
            time.sleep(1)

            print(f"Legitimate form change completed for {context}")
            return True

        except Exception as e:
            print(f"Error triggering form change for {context}: {e}")
            return False

    def find_and_enable_save_button(
        self, section_context: str, timeout: Optional[int] = None
    ) -> bool:
        """
        Find save button for a section and wait for it to become enabled.

        This method combines save button detection with legitimate form change triggering
        to properly enable save buttons using device-specific patterns.

        Args:
            section_context: Section context (timezone, dst, general, etc.)
            timeout: Timeout in milliseconds

        Returns:
            True if save button found and enabled, False otherwise
        """
        try:
            # Get device-specific patterns for this section
            patterns = self._get_form_change_patterns(section_context)

            print(f"Looking for save button for section: {section_context}")

            # Try to find the save button
            save_button = self.find_save_button(section_context)

            if not save_button:
                print(f"Save button not found for section: {section_context}")
                return False

            # Check if save button is already enabled
            if save_button.is_enabled():
                print(f"Save button already enabled for section: {section_context}")
                return True

            # Wait for save button to become enabled with device-specific timing
            print(
                f"Waiting for save button to become enabled for section: {section_context}"
            )
            return self._wait_for_save_button_enabled(save_button, timeout)

        except Exception as e:
            print(f"Error finding and enabling save button for {section_context}: {e}")
            return False

    def configure_and_save(
        self, section_context: str, field_config: Dict[str, Any]
    ) -> bool:
        """
        Configure form fields and save configuration using device-aware patterns.

        This method replaces the flawed approach of making fake changes to trigger
        save buttons. Instead, it makes legitimate changes using device-specific
        patterns and waits appropriately for save button enablement.

        Args:
            section_context: Section context (timezone, dst, general, etc.)
            field_config: Dictionary with field configurations:
                - field_locator: Locator for the field to configure
                - new_value: New value to set
                - field_type: Type of field ("select", "input", "checkbox")

        Returns:
            True if configuration and save successful, False otherwise
        """
        try:
            print(f"Configuring and saving section: {section_context}")

            # Configure the field with legitimate change
            field_locator = field_config.get("field_locator")
            new_value = field_config.get("new_value")
            field_type = field_config.get("field_type", "input")

            if not field_locator or new_value is None:
                print(f"Missing field configuration for {section_context}")
                return False

            # Make legitimate form change
            if not self.trigger_legitimate_form_change(
                field_locator, new_value, section_context
            ):
                return False

            # Wait for and find enabled save button
            if not self.find_and_enable_save_button(section_context):
                return False

            # Click the save button
            return self.safe_save_click(
                section_context, context=f"configure_and_save_{section_context}"
            )

        except Exception as e:
            print(f"Error in configure_and_save for {section_context}: {e}")
            return False

    def get_device_specific_timeouts(self) -> Dict[str, int]:
        """
        Get device-specific timeout values using unused performance data.

        Returns:
            Dictionary with device-specific timeout values for various operations
        """
        behavior_data = self._get_device_behavior_data()
        performance_data = behavior_data.get("performance_expectations", {})

        # Base timeouts
        timeouts = {
            "form_save_enablement": 10000,  # 10 seconds
            "navigation": 30000,  # 30 seconds
            "satellite_loading": 60000,  # 60 seconds
            "page_load": self.DEFAULT_TIMEOUT,
        }

        # Apply device-specific adjustments
        if self.device_model:
            timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(
                self.device_model
            )

            # Adjust timeouts based on device characteristics
            for key in timeouts:
                timeouts[key] = int(timeouts[key] * timeout_multiplier)

        # Get specific timing from device capabilities if available
        auth_performance = performance_data.get("authentication_performance", {})
        if auth_performance:
            # Use device-specific authentication timing
            config_unlock = auth_performance.get("configuration_unlock", {})
            typical_time = config_unlock.get("typical_time", "")
            if typical_time:
                # Parse time format like "1-2 seconds" to milliseconds
                if "1-2 seconds" in typical_time:
                    timeouts["form_save_enablement"] = 5000  # 5 seconds
                elif "2-3 seconds" in typical_time:
                    timeouts["form_save_enablement"] = 8000  # 8 seconds

        return timeouts

    def ensure_dashboard_context(
        self, base_url: str, timeout: Optional[int] = None
    ) -> bool:
        """
        Ensure we're on the dashboard page before performing navigation operations.

        This method addresses the root cause of navigation failures where tests
        start from configuration pages (e.g., /general) and try to access
        navigation menus that only exist on the dashboard (/).

        Args:
            base_url: Base URL of the device (e.g., "https://172.16.66.1")
            timeout: Timeout in milliseconds (uses DEFAULT_TIMEOUT if None)

        Returns:
            True if successfully on dashboard or already on dashboard, False otherwise
        """
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        try:
            current_url = self.page.url
            print(f"Current URL: {current_url}")

            # Check if we're already on the dashboard
            if current_url.endswith("/") or "/index" in current_url:
                print("Already on dashboard page")
                return True

            # Check if we're on a configuration page
            config_sections = [
                "/general",
                "/network",
                "/time",
                "/gnss",
                "/outputs",
                "/display",
                "/access",
                "/snmp",
                "/syslog",
                "/ptp",
                "/upload",
            ]

            is_on_config_page = any(
                current_url.endswith(section) for section in config_sections
            )

            if is_on_config_page:
                print(f"Currently on configuration page, navigating to dashboard")

                # Navigate to dashboard
                dashboard_url = f"{base_url}/"
                print(f"Navigating to: {dashboard_url}")

                self.page.goto(
                    dashboard_url, wait_until="domcontentloaded", timeout=timeout
                )

                # Wait for page stabilization
                self.wait_for_page_load(timeout=timeout)

                # Verify we're now on dashboard
                final_url = self.page.url
                if final_url.endswith("/") or "/index" in final_url:
                    print(f"Successfully navigated to dashboard: {final_url}")
                    return True
                else:
                    print(f"Navigation failed, still on: {final_url}")
                    self._capture_debug_info(
                        "dashboard_navigation_failure",
                        failure_reason=f"Failed to navigate from {current_url} to dashboard",
                    )
                    return False
            else:
                # Unknown page state - try to navigate to dashboard anyway
                print(
                    f"Unknown page state ({current_url}), attempting to navigate to dashboard"
                )
                dashboard_url = f"{base_url}/"
                self.page.goto(
                    dashboard_url, wait_until="domcontentloaded", timeout=timeout
                )
                self.wait_for_page_load(timeout=timeout)
                return True

        except Exception as e:
            print(f"Error ensuring dashboard context: {e}")
            self._capture_debug_info(
                "dashboard_context_error",
                failure_reason=f"Dashboard context error: {str(e)}",
            )
            return False

    def _is_save_button_enabled(self, save_button_locator) -> bool:
        """
        Check if a save button is enabled without waiting.

        Args:
            save_button_locator: Locator for the save button to check

        Returns:
            True if save button is visible and enabled, False otherwise
        """
        try:
            if not save_button_locator or save_button_locator.count() == 0:
                return False

            # Check if the save button is visible and enabled
            element = save_button_locator.first
            return element.is_visible() and element.is_enabled()

        except Exception as e:
            print(f"Error checking save button enabled state: {e}")
            return False

    # ================================================
    # DEVICE CAPABILITIES WRAPPER METHODS
    # ================================================
    # These standardized wrapper methods provide consistent access to
    # DeviceCapabilities functionality across all page objects.

    def get_timeout(self, base_timeout: int = None) -> int:
        """
        Get timeout adjusted for device characteristics.

        Uses DeviceCapabilities.get_timeout_multiplier() to adjust timeouts
        based on known device issues (e.g., slower Series 3 devices).

        Args:
            base_timeout: Base timeout in milliseconds (uses DEFAULT_TIMEOUT if None)

        Returns:
            Adjusted timeout in milliseconds
        """
        if base_timeout is None:
            base_timeout = self.DEFAULT_TIMEOUT
        if self.device_model:
            multiplier = DeviceCapabilities.get_timeout_multiplier(self.device_model)
            return int(base_timeout * multiplier)
        return base_timeout

    def get_save_button_config(
        self, section_context: str, interface: str = None
    ) -> Dict[str, Any]:
        """
        Get device-specific save button configuration from DeviceCapabilities.

        Handles the complexity of Series 2 vs Series 3 save button patterns:
        - Series 2: Generic button#button_save
        - Series 3: Interface-specific buttons (button#button_save_port_eth1, etc.)

        Args:
            section_context: Configuration section (e.g., "network", "ptp", "general")
            interface: Network interface for multi-interface configs (e.g., "eth1")

        Returns:
            Dictionary with:
            - selector: CSS selector for the save button
            - description: Human-readable description
            - panel_expansion_required: Whether panel needs expansion before clicking
        """
        if self.device_model:
            return DeviceCapabilities.get_interface_specific_save_button(
                self.device_model, f"{section_context}_configuration", interface
            )
        return {
            "selector": "button#button_save",
            "description": "Generic save button",
            "panel_expansion_required": False,
        }

    def is_panel_expanded(self, panel_id: str) -> bool:
        """
        Check if a Bootstrap collapsible panel is currently expanded.

        Series 3 devices use Bootstrap collapse panels that start collapsed by default.
        This method checks the current expansion state.

        Args:
            panel_id: Panel identifier (e.g., "eth1", "ptp_eth1", "gateway")

        Returns:
            True if panel is expanded, False if collapsed
        """
        try:
            collapse_element = self.page.locator(f"#{panel_id}_collapse")
            if collapse_element.count() > 0:
                class_attr = collapse_element.get_attribute("class") or ""
                # Bootstrap 3 uses "in", Bootstrap 4/5 uses "show"
                return "in" in class_attr or "show" in class_attr
            return True  # Assume expanded if panel structure not found
        except Exception as e:
            print(f"Error checking panel expansion state for {panel_id}: {e}")
            return True  # Assume expanded on error to avoid blocking

    def expand_panel(self, panel_id: str) -> bool:
        """
        Expand a Bootstrap collapsible panel if it's currently collapsed.

        Args:
            panel_id: Panel identifier (e.g., "eth1", "ptp_eth1", "gateway")

        Returns:
            True if panel is now expanded, False if expansion failed
        """
        try:
            if self.is_panel_expanded(panel_id):
                print(f"Panel {panel_id} already expanded")
                return True

            # Find and click the panel toggle
            toggle = self.page.locator(f"a[href='#{panel_id}_collapse']")
            if toggle.count() > 0:
                toggle.click()
                time.sleep(0.5)  # Wait for animation

                # Verify expansion
                if self.is_panel_expanded(panel_id):
                    print(f"Panel {panel_id} expanded successfully")
                    return True
                else:
                    print(f"Panel {panel_id} expansion verification failed")
                    return False
            else:
                print(f"Panel toggle not found for {panel_id}")
                return False

        except Exception as e:
            print(f"Error expanding panel {panel_id}: {e}")
            return False

    def is_section_available(self, section_name: str) -> bool:
        """
        Check if a configuration section is available for this device.

        Uses DeviceCapabilities.get_available_sections() to determine
        which sections are accessible based on device series.

        Args:
            section_name: Section name (e.g., "ptp", "network", "general")

        Returns:
            True if section is available for this device, False otherwise
        """
        if self.device_model:
            available_sections = DeviceCapabilities.get_available_sections(
                self.device_model
            )
            return section_name.lower() in [s.lower() for s in available_sections]
        return True  # Assume available for unknown devices

    def get_interface_aware_locator(
        self, field_name: str, interface: str = None
    ) -> str:
        """
        Get interface-specific locator for Series 3 multi-interface pages.

        Series 3 devices have multiple network interfaces (eth0, eth1, eth2, eth3, eth4)
        and use interface-prefixed field IDs to distinguish them.

        Args:
            field_name: Base field name (e.g., "ip", "mask", "profile")
            interface: Network interface (e.g., "eth1") - required for Series 3

        Returns:
            CSS selector string for the field
        """
        if self.device_model and DeviceCapabilities.get_series(self.device_model) == 3:
            if interface:
                return f"#{interface}_{field_name}"
            else:
                print(
                    f"Warning: Series 3 device but no interface specified for {field_name}"
                )
                return f"#{field_name}"
        return f"#{field_name}"  # Series 2 uses generic selectors

    def get_available_interfaces(self) -> List[str]:
        """
        Get list of available network interfaces for this device.

        Uses DeviceCapabilities.get_network_interfaces() for authoritative data.

        Returns:
            List of interface names (e.g., ["eth0", "eth1", "eth3"])
        """
        if self.device_model:
            return DeviceCapabilities.get_network_interfaces(self.device_model)
        return ["eth0"]  # Fallback for unknown devices

    def get_ptp_interfaces(self) -> List[str]:
        """
        Get list of PTP-capable interfaces for this device.

        Uses DeviceCapabilities.get_ptp_interfaces() for authoritative data.

        Returns:
            List of PTP-capable interface names (e.g., ["eth1", "eth3"])
        """
        if self.device_model:
            return DeviceCapabilities.get_ptp_interfaces(self.device_model)
        return []  # No PTP interfaces for unknown devices

    def is_ptp_supported(self) -> bool:
        """
        Check if PTP is supported on this device.

        Uses DeviceCapabilities.is_ptp_supported() for authoritative data.

        Returns:
            True if PTP is supported, False otherwise
        """
        if self.device_model:
            return DeviceCapabilities.is_ptp_supported(self.device_model)
        return False  # Assume no PTP for unknown devices

    def get_max_outputs(self) -> int:
        """
        Get maximum output count for this device.

        Uses DeviceCapabilities.get_max_outputs() for authoritative data.

        Returns:
            Maximum number of outputs (4 for Series 2, 6 for Series 3)
        """
        if self.device_model:
            return DeviceCapabilities.get_max_outputs(self.device_model)
        return 4  # Conservative default
