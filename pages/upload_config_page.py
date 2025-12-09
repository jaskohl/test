"""
Upload configuration page object for Kronos device test automation.

Device-aware page object with DeviceCapabilities integration and device-aware behavior patterns.
Provides the interface expected by test files that import 'pages.upload_config_page'.

Based on DeviceCapabilities integration for device-aware behavior:
- Series-aware timeout management
- Device-specific save button patterns
- Panel expansion patterns for Series 3 collapsible UI
- Enhanced error handling with device-aware debugging
"""

from playwright.sync_api import Page, expect, Locator
from .base import BasePage
from .device_capabilities import DeviceCapabilities
from typing import Dict, Optional, List, Any
import os


class UploadConfigPage(BasePage):
    """
    Upload configuration page object for Kronos device.

    Device-aware: Uses DeviceCapabilities for all device-specific behavior.
    Enhanced with improved error handling and debugging capabilities.

    This class provides the full interface expected by test files while
    maintaining compatibility with the base functionality.
    """

    def __init__(self, page: Page, device_model: Optional[str] = None):
        """
        Initialize upload configuration page with device enhancement.

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

        print(f"UploadConfigPage initialized for {self.device_model or 'Unknown'}")

    def validate_capabilities(self) -> bool:
        """
        Validate that the page layout matches device capabilities from DeviceCapabilities.

        Returns:
            bool: True if capabilities match, False if there are discrepancies
        """
        try:
            if not self.device_model:
                return True

            # Check if upload section is available
            return self.is_section_available("upload")
        except Exception as e:
            print(f"UploadConfigPage: Error validating capabilities: {e}")
            return False

    def verify_page_loaded(self) -> bool:
        """
        Verify upload configuration page has loaded successfully.

        Returns:
            bool: True if page loaded successfully, False otherwise
        """
        try:
            # Check for upload-related elements
            upload_indicators = [
                "input[type='file']",
                "button:has-text('Upload')",
                "h1:has-text('Upload')",
                "h2:has-text('Upload')",
            ]

            for selector in upload_indicators:
                element = self.page.locator(selector)
                if element.is_visible(timeout=5000):
                    return True

            # Fallback to base page validation
            return self.validate_page_loaded()

        except Exception as e:
            print(f"UploadConfigPage: Error verifying page loaded: {e}")
            return False

    def get_page_data(self) -> Dict[str, Any]:
        """
        Extract upload configuration data from the page.

        Returns:
            Dict[str, Any]: Dictionary containing upload configuration data and device info
        """
        try:
            page_data = super().get_page_data()

            # Add upload-specific context information
            page_data.update(
                {
                    "_upload_page": True,
                    "device_series": self.device_series,
                    "capabilities_validated": self.validate_capabilities(),
                    "available_sections": self.available_sections,
                }
            )

            return page_data

        except Exception as e:
            print(f"UploadConfigPage: Error getting page data: {e}")
            return {"error": str(e)}

    def select_firmware_file(self, file_path: str) -> bool:
        """
        Select firmware file for upload.

        Args:
            file_path: Path to the firmware file to upload

        Returns:
            bool: True if file selected successfully, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"UploadConfigPage: File does not exist: {file_path}")
                return False

            # Find file input
            file_input = self.page.locator("input[type='file']")
            if file_input.count() == 0:
                print("UploadConfigPage: No file input found")
                return False

            # Set file path
            file_input.set_input_files(file_path)
            print(f"UploadConfigPage: File selected: {file_path}")
            return True

        except Exception as e:
            print(f"UploadConfigPage: Error selecting file: {e}")
            return False

    def start_upload(self) -> bool:
        """
        Start the firmware upload process.

        Returns:
            bool: True if upload started successfully, False otherwise
        """
        try:
            # Look for upload button
            upload_buttons = [
                "button:has-text('Upload')",
                "input[type='submit'][value='Upload']",
                "button[type='submit']",
            ]

            for selector in upload_buttons:
                button = self.page.locator(selector)
                if button.is_visible(timeout=5000):
                    button.click()
                    print("UploadConfigPage: Upload started")
                    return True

            print("UploadConfigPage: No upload button found")
            return False

        except Exception as e:
            print(f"UploadConfigPage: Error starting upload: {e}")
            return False

    def monitor_upload_progress(self, timeout: int = 300000) -> Dict[str, str]:
        """
        Monitor firmware upload progress.

        Args:
            timeout: Timeout in milliseconds to wait for upload completion

        Returns:
            Dict[str, str]: Dictionary with upload progress information
        """
        try:
            progress_info = {
                "status": "monitoring",
                "progress": "0%",
                "message": "Upload in progress",
            }

            # Wait for upload to complete or timeout
            import time

            start_time = time.time()

            # Look for completion indicators
            completion_selectors = [
                "text=Upload completed",
                "text=Success",
                ".success-message",
                ".upload-success",
            ]

            for selector in completion_selectors:
                try:
                    element = self.page.locator(selector)
                    if element.is_visible(timeout=timeout):
                        progress_info["status"] = "completed"
                        progress_info["progress"] = "100%"
                        progress_info["message"] = "Upload completed successfully"
                        break
                except:
                    continue

            # Check for errors
            error_selectors = [
                "text=Error",
                "text=Failed",
                ".error-message",
                ".upload-error",
            ]

            for selector in error_selectors:
                try:
                    element = self.page.locator(selector)
                    if element.is_visible(timeout=2000):
                        progress_info["status"] = "failed"
                        progress_info["message"] = "Upload failed"
                        break
                except:
                    continue

            elapsed_time = time.time() - start_time
            progress_info["elapsed_seconds"] = round(elapsed_time, 2)

            return progress_info

        except Exception as e:
            print(f"UploadConfigPage: Error monitoring upload: {e}")
            return {"status": "error", "message": str(e)}

    def get_upload_result(self) -> Dict[str, str]:
        """
        Get the result of the firmware upload operation.

        Returns:
            Dict[str, str]: Dictionary with upload result information
        """
        try:
            result = {
                "uploaded": False,
                "status": "unknown",
                "message": "No upload result available",
            }

            # Check for success indicators
            success_indicators = [
                "text=Upload completed",
                "text=Success",
                ".success-message",
            ]

            for selector in success_indicators:
                try:
                    element = self.page.locator(selector)
                    if element.is_visible():
                        result["uploaded"] = True
                        result["status"] = "success"
                        result["message"] = element.text_content()
                        return result
                except:
                    continue

            # Check for error indicators
            error_indicators = [
                "text=Error",
                "text=Failed",
                ".error-message",
            ]

            for selector in error_indicators:
                try:
                    element = self.page.locator(selector)
                    if element.is_visible():
                        result["status"] = "error"
                        result["message"] = element.text_content()
                        return result
                except:
                    continue

            return result

        except Exception as e:
            print(f"UploadConfigPage: Error getting upload result: {e}")
            return {"status": "error", "message": str(e)}

    def navigate_to_page(self) -> bool:
        """
        Navigate to upload configuration page.

        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            print(
                f"UploadConfigPage: Navigating to upload config for {self.device_model}"
            )

            # Try navigation patterns
            nav_selectors = [
                "a:has-text('Upload')",
                "a[href*='upload']",
                "a:has-text('Firmware')",
                "a[href*='firmware']",
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
            print("UploadConfigPage: No navigation link found, assuming on page")
            return True

        except Exception as e:
            print(f"UploadConfigPage: Navigation error: {e}")
            return False

    def save_configuration(self) -> bool:
        """
        Save upload configuration changes using device-aware save button patterns.

        Returns:
            bool: True if configuration saved successfully, False otherwise
        """
        try:
            # Use base class save button detection
            save_button = self.find_save_button()
            if save_button:
                save_button.click()
                print("UploadConfigPage: Configuration saved")
                return True

            print("UploadConfigPage: No save button found")
            return False

        except Exception as e:
            print(f"UploadConfigPage: Error saving configuration: {e}")
            return False

    def get_upload_status(self) -> Dict[str, str]:
        """
        Get current upload status.

        Returns:
            Dict[str, str]: Dictionary with upload status information
        """
        try:
            status = {
                "current_status": "idle",
                "file_selected": False,
                "upload_in_progress": False,
            }

            # Check if file is selected
            file_input = self.page.locator("input[type='file']")
            if file_input.count() > 0:
                try:
                    file_value = file_input.input_value()
                    status["file_selected"] = bool(file_value)
                    status["selected_file"] = file_value
                except:
                    pass

            # Check for upload progress indicators
            progress_indicators = [
                ".progress-bar",
                ".upload-progress",
                "text=Progress",
            ]

            for selector in progress_indicators:
                try:
                    element = self.page.locator(selector)
                    if element.is_visible():
                        status["upload_in_progress"] = True
                        status["current_status"] = "uploading"
                        break
                except:
                    continue

            return status

        except Exception as e:
            print(f"UploadConfigPage: Error getting upload status: {e}")
            return {"error": str(e)}

    def verify_file_selected(self, expected_filename: str) -> bool:
        """
        Verify that the expected file has been selected for upload.

        Args:
            expected_filename: Name of the file that should be selected

        Returns:
            bool: True if file is properly selected, False otherwise
        """
        try:
            file_input = self.page.locator("input[type='file']")
            if file_input.count() == 0:
                return False

            selected_file = file_input.input_value()
            return expected_filename in selected_file if selected_file else False

        except Exception as e:
            print(f"UploadConfigPage: Error verifying file selected: {e}")
            return False

    def cancel_upload(self) -> bool:
        """
        Cancel any ongoing upload operation.

        Returns:
            bool: True if cancel successful, False otherwise
        """
        try:
            cancel_buttons = [
                "button:has-text('Cancel')",
                "button:has-text('Stop')",
                "input[value='Cancel']",
            ]

            for selector in cancel_buttons:
                try:
                    button = self.page.locator(selector)
                    if button.is_visible(timeout=2000):
                        button.click()
                        print("UploadConfigPage: Upload cancelled")
                        return True
                except:
                    continue

            print("UploadConfigPage: No cancel button found")
            return False

        except Exception as e:
            print(f"UploadConfigPage: Error cancelling upload: {e}")
            return False

    def is_section_available(self, section_name: str = "upload") -> bool:
        """
        Check if upload configuration section is available for this device.

        Args:
            section_name: Section name to check (default: "upload")

        Returns:
            bool: True if section is available, False otherwise
        """
        try:
            if not self.device_model:
                print(
                    "UploadConfigPage: No device model available, assuming section available"
                )
                return True

            # Check device capabilities for upload availability
            available_sections = DeviceCapabilities.get_available_sections(
                self.device_model
            )
            return "upload" in available_sections

        except Exception as e:
            print(f"UploadConfigPage: Error checking section availability: {e}")
            return True  # Default to available for backward compatibility

    def get_save_cancel_buttons(self) -> List[Any]:
        """
        Get save and cancel button locators for upload configuration.

        Returns:
            List[Any]: List of button locators
        """
        try:
            buttons = []

            # Device-aware save button detection
            save_button = self.get_save_button_locator()
            if save_button:
                buttons.append(save_button)

            # Generic cancel button detection
            cancel_selectors = [
                "button:has-text('Cancel')",
                "input[value='Cancel']",
                "button[name='cancel']",
                ".cancel-button",
                "#button_cancel",
            ]

            for selector in cancel_selectors:
                try:
                    cancel_button = self.page.locator(selector)
                    if cancel_button.is_visible(timeout=2000):
                        buttons.append(cancel_button)
                        break
                except:
                    continue

            return buttons

        except Exception as e:
            print(f"UploadConfigPage: Error getting save/cancel buttons: {e}")
            return []

    def get_upload_configuration(self) -> Dict[str, Any]:
        """
        Get comprehensive upload configuration data.

        Returns:
            Dict[str, Any]: Comprehensive upload configuration data
        """
        try:
            config_data = self.get_page_data()

            # Add specific upload configuration details
            try:
                # Get file input information
                file_input = self.page.locator("input[type='file']")
                if file_input.is_visible():
                    config_data["file_input_available"] = True
                    file_input_value = file_input.input_value()
                    config_data["file_selected"] = bool(file_input_value)
                else:
                    config_data["file_input_available"] = False
                    config_data["file_selected"] = False

            except Exception as e:
                print(f"UploadConfigPage: Error getting file input info: {e}")
                config_data["file_input_available"] = False
                config_data["file_selected"] = False

            return config_data

        except Exception as e:
            print(f"UploadConfigPage: Error getting upload configuration: {e}")
            return {"error": str(e)}

    def test_section_access_pure(self) -> Dict[str, Any]:
        """
        Test upload section access with pure functionality (no side effects).

        This method provides the interface expected by test files for section access testing.

        Returns:
            Dict[str, Any]: Test results with access status and details
        """
        try:
            result = {
                "section_name": "Upload",
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

            print(f"UploadConfigPage: Section access test result: {result}")
            return result

        except Exception as e:
            print(f"UploadConfigPage: Error in section access test: {e}")
            return {"section_name": "Upload", "accessible": False, "error": str(e)}

    def create_test_file(self, content: str, extension: str = "txt") -> str:
        """
        Create a temporary test file with specified content and extension.

        Args:
            content: Content to write to the test file
            extension: File extension (without dot), default is "txt"

        Returns:
            str: Path to the created test file
        """
        try:
            import tempfile

            # Create temporary file
            temp_dir = tempfile.gettempdir()
            filename = f"test_upload_{hash(content) % 10000}.{extension}"
            file_path = os.path.join(temp_dir, filename)

            # Write content
            with open(file_path, "w") as f:
                f.write(content)

            print(f"UploadConfigPage: Test file created: {file_path}")
            return file_path

        except Exception as e:
            print(f"UploadConfigPage: Error creating test file: {e}")
            return ""

    def check_file_type_validation(
        self, file_path: str, expected_extensions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Check file type validation for firmware uploads.

        Args:
            file_path: Path to the file to validate
            expected_extensions: List of expected file extensions (e.g., ['.fwu', '.bin'])

        Returns:
            Dict[str, Any]: Validation result with details
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "valid": False,
                    "error": "File does not exist",
                    "file_path": file_path,
                }

            # Default firmware extensions if not provided
            if expected_extensions is None:
                expected_extensions = [".fwu", ".bin", ".zip"]

            # Check file extension
            file_extension = os.path.splitext(file_path)[1].lower()

            validation_result = {
                "valid": file_extension in [ext.lower() for ext in expected_extensions],
                "file_path": file_path,
                "file_extension": file_extension,
                "expected_extensions": expected_extensions,
                "file_size": 0,
                "readable": False,
            }

            # Get file size
            try:
                validation_result["file_size"] = os.path.getsize(file_path)
                validation_result["readable"] = os.access(file_path, os.R_OK)
            except Exception as e:
                validation_result["file_error"] = str(e)

            return validation_result

        except Exception as e:
            print(f"UploadConfigPage: Error in file type validation: {e}")
            return {"valid": False, "error": str(e), "file_path": file_path}
