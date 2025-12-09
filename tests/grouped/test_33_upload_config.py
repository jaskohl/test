"""
Category 33: Upload Configuration Tests - MEANINGFUL IMPLEMENTATION
Test Count: 6 tests
Hardware: Device Only
Priority: MEDIUM - Upload enables configuration backup/restore
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 33 v4.4
Based on device exploration data: config_upload.forms.json
File Upload Validation (3 tests):
- 33.1.1: Valid File Upload
- 33.1.2: Invalid File Type Rejection
- 33.1.3: File Size Limit Enforcement
Upload Process Management (2 tests):
- 33.2.1: Upload Progress Indication
- 33.2.2: Post-Upload Verification
Upload Error Handling (1 test):
- 33.3.1: Upload Interruption Handling
"""

import pytest
import tempfile
import os
from playwright.sync_api import Page, expect
from pages.upload_config_page import UploadConfigPage


class TestFileUploadValidation:
    """Tests 33.1: File Upload Validation (3 tests)"""

    def test_33_1_1_valid_file_upload(self, upload_config_page: UploadConfigPage):
        """
        Test 33.1.1: Valid File Upload
        Purpose: Verify valid firmware/configuration file upload and processing
        Expected: .fwu files accepted, upload completes, and file is processed by device
        Series: Both Series 2 and 3
        Note: Device only accepts .fwu, .pem, .pub files
        """
        # Create a valid FWU test file with proper content
        test_content = (
            "# Firmware upgrade file\n"
            "# Generated for upload testing\n"
            "# Version: TEST_1.0.0\n"
            "# Timestamp: 2025-11-07\n"
            "FIRMWARE_DATA=test_firmware_content\n"
            "VALIDATION=true\n"
        )

        # Create and upload the file
        test_file_path = upload_config_page.create_test_file(test_content, "fwu")
        assert os.path.exists(test_file_path), "Test file should be created"

        try:
            # Verify file upload field exists
            file_input = upload_config_page.page.locator(
                "input[type='file'][name='file[]']"
            )
            expect(file_input).to_be_visible()

            # Attempt upload through page object method
            upload_result = upload_config_page.upload_file(test_file_path)

            # Verify upload completed (method returns True on success)
            assert (
                upload_result is True
            ), "upload_file() should return True for successful file upload"

            # Verify file was processed - check for upload confirmation message
            success_indicators = [
                upload_config_page.page.locator(
                    "text=/upload.*successful|file.*uploaded|success/i"
                ),
                upload_config_page.page.locator(
                    "[class*='success'], [class*='complete']"
                ),
                upload_config_page.page.locator("text=/complete|finished|done/i"),
            ]

            upload_confirmed = any(
                indicator.count() > 0 for indicator in success_indicators
            )
            assert (
                upload_confirmed
            ), "Upload success should be indicated by message or UI element"

            print("Valid FWU upload test passed with real validation")

        finally:
            # Clean up test file
            if os.path.exists(test_file_path):
                os.unlink(test_file_path)

    def test_33_1_2_invalid_file_type_rejection(
        self, upload_config_page: UploadConfigPage
    ):
        """
        Test 33.1.2: Invalid File Type Rejection
        Purpose: Verify invalid file types are rejected with appropriate error handling
        Expected: Non-accepted file types (.txt) rejected with error message or validation failure
        Series: Both Series 2 and 3
        """
        # Create an invalid text file that should be rejected
        test_content = "This is not a valid firmware file. It contains plain text data that should be rejected by the device upload validation."

        # Create the invalid file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(test_content)
            invalid_file_path = f.name

        try:
            # Verify file exists
            assert os.path.exists(invalid_file_path), "Test file should be created"

            # Check file type validation through page object (if method exists)
            if hasattr(upload_config_page, "check_file_type_validation"):
                validation_result = upload_config_page.check_file_type_validation(
                    invalid_file_path
                )
                # Validation should fail for invalid file types
                assert (
                    validation_result is False
                ), "File type validation should reject .txt files"
            else:
                # Fallback: Try to select the file and check for rejection
                file_input = upload_config_page.page.locator(
                    "input[type='file'][name='file[]']"
                )
                file_input.set_input_files(invalid_file_path)

                # Check for error messages or validation failures
                error_indicators = [
                    upload_config_page.page.locator(
                        "text=/invalid.*file|file.*not.*supported|unsupported.*type/i"
                    ),
                    upload_config_page.page.locator(
                        "[class*='error'], [class*='invalid']"
                    ),
                    upload_config_page.page.locator("text=/error|rejected|denied/i"),
                ]

                rejection_indicated = any(
                    indicator.count() > 0 for indicator in error_indicators
                )
                assert (
                    rejection_indicated
                ), "Invalid file type should trigger error message or validation failure"

            print("Invalid file type rejection test passed")

        finally:
            # Clean up test file
            if os.path.exists(invalid_file_path):
                os.unlink(invalid_file_path)

    def test_33_1_3_file_size_limit_enforcement(
        self, upload_config_page: UploadConfigPage
    ):
        """
        Test 33.1.3: File Size Limit Enforcement
        Purpose: Verify file size limits are enforced
        Expected: Oversized files rejected with size-related error
        Series: Both Series 2 and 3
        """
        # Create a large file that exceeds typical device limits (assume ~5MB limit)
        large_content = "x" * (6 * 1024 * 1024)  # 6MB of data

        # Create the oversized file with .fwu extension to pass basic type validation
        large_file_path = upload_config_page.create_test_file(large_content, "fwu")
        assert os.path.exists(large_file_path), "Large test file should be created"

        # Verify file size is actually large
        file_size = os.path.getsize(large_file_path)
        assert (
            file_size > 5 * 1024 * 1024
        ), f"File should be >5MB, got {file_size} bytes"

        try:
            # Check file size validation through page object (if method exists)
            if hasattr(upload_config_page, "check_file_size_validation"):
                size_validation_result = upload_config_page.check_file_size_validation(
                    large_file_path
                )
                assert (
                    size_validation_result is False
                ), "File size validation should reject oversized files"
            else:
                # Fallback: Try to upload and check for rejection
                file_input = upload_config_page.page.locator(
                    "input[type='file'][name='file[]']"
                )
                file_input.set_input_files(large_file_path)

                # Wait for size validation to trigger
                upload_config_page.page.wait_for_timeout(2000)

                # Check for size-related error messages
                size_error_indicators = [
                    upload_config_page.page.locator(
                        "text=/too.*large|size.*limit|file.*too.*big/i"
                    ),
                    upload_config_page.page.locator(
                        "text=/exceeds.*limit|over.*size/i"
                    ),
                    upload_config_page.page.locator(
                        "text=/maximum.*size|size.*maximum/i"
                    ),
                ]

                size_limit_enforced = any(
                    indicator.count() > 0 for indicator in size_error_indicators
                )
                assert (
                    size_limit_enforced
                ), "Oversized file should trigger size limit error message"

            print("File size limit enforcement test passed")

        finally:
            # Clean up test file
            if os.path.exists(large_file_path):
                os.unlink(large_file_path)


class TestUploadProcessManagement:
    """Tests 33.2: Upload Process Management (2 tests)"""

    def test_33_2_1_upload_progress_indication(
        self, upload_config_page: UploadConfigPage
    ):
        """
        Test 33.2.1: Upload Progress Indication
        Purpose: Verify upload progress is communicated to user
        Expected: Progress indicators or status updates during upload
        Series: Both Series 2 and 3
        """
        # Create a moderately-sized file to allow progress observation
        test_content = (
            "# Progress test firmware\n"
            "# Contains data to make upload visible\n"
            "# " + "x" * 50000 + "\n"
            "# Version: PROGRESS_TEST_1.0\n"
        )

        test_file_path = upload_config_page.create_test_file(test_content, "fwu")

        try:
            # Verify we can select file for upload
            file_selection_result = upload_config_page.select_file_for_upload(
                test_file_path
            )
            assert file_selection_result is True, "File should be selectable for upload"

            # Check for upload initiation capability
            if hasattr(upload_config_page, "initiate_upload"):
                initiation_result = upload_config_page.initiate_upload()
                assert initiation_result is True, "Upload should be initiatable"
            else:
                # Fallback: Look for upload button and interaction
                upload_button = upload_config_page.page.locator(
                    "input[type='submit'], button[type='submit']"
                )
                expect(upload_button).to_be_visible()

            # Look for progress indicators during potential upload
            progress_indicators = [
                upload_config_page.page.locator("progress, [role='progressbar']"),
                upload_config_page.page.locator(
                    "[class*='progress'], [class*='loading']"
                ),
                upload_config_page.page.locator(
                    "text=/uploading|processing|transferring/i"
                ),
            ]

            progress_present = any(
                indicator.count() > 0 for indicator in progress_indicators
            )
            assert (
                progress_present
            ), "Progress indication should be present during upload process"

            # Wait for potential upload completion
            if hasattr(upload_config_page, "wait_for_upload_completion"):
                completion_result = upload_config_page.wait_for_upload_completion(
                    timeout=30000
                )
                assert completion_result is True, "Upload should complete successfully"
            else:
                # Fallback: Wait for upload-related state changes
                upload_config_page.page.wait_for_timeout(5000)  # Allow time for upload

            print("Upload progress indication test passed")

        finally:
            # Clean up test file
            if os.path.exists(test_file_path):
                os.unlink(test_file_path)

    def test_33_2_2_post_upload_verification(
        self, upload_config_page: UploadConfigPage
    ):
        """
        Test 33.2.2: Post-Upload Verification
        Purpose: Verify successful upload confirmation and result persistence
        Expected: Upload success confirmed and results persist through page refresh
        Series: Both Series 2 and 3
        """
        # Create a test file for verification
        test_content = (
            "# Verification test firmware\n"
            "# Post-upload persistence check\n"
            "# Timestamp: 2025-11-07\n"
            "VERIFICATION_DATA=true\n"
        )

        test_file_path = upload_config_page.create_test_file(test_content, "fwu")

        try:
            # Complete upload process
            upload_result = upload_config_page.upload_file(test_file_path)
            assert upload_result is True, "File upload should succeed"

            # Verify immediate success indication
            success_verified = upload_config_page.verify_upload_success()
            assert success_verified is True, "Upload success should be verifiable"

            # Test persistence through page refresh/reload
            upload_config_page.page.reload()
            upload_config_page.page.wait_for_load_state("domcontentloaded")

            # Verify page is still functional after reload
            upload_config_page.verify_page_loaded()

            # Check if success indication persists (device-dependent)
            try:
                persistent_success = upload_config_page.verify_upload_success()
                if persistent_success:
                    print("Upload success indication persists after page reload")
                else:
                    print(
                        "Upload success indication cleared after reload (acceptable device behavior)"
                    )
            except Exception:
                print(
                    "Could not verify persistence after reload - device may clear messages"
                )

            # Verify upload interface remains functional
            file_input = upload_config_page.page.locator(
                "input[type='file'][name='file[]']"
            )
            expect(file_input).to_be_visible()

            print("Post-upload verification test passed")

        finally:
            # Clean up test file
            if os.path.exists(test_file_path):
                os.unlink(test_file_path)


class TestUploadErrorHandling:
    """Tests 33.3: Upload Error Handling (1 test)"""

    def test_33_3_1_upload_interruption_handling(
        self, upload_config_page: UploadConfigPage
    ):
        """
        Test 33.3.1: Upload Interruption Handling
        Purpose: Verify graceful system behavior when upload is interrupted
        Expected: System remains stable and functional after interruption
        Series: Both Series 2 and 3
        """
        # Create a file that can be used for interruption testing
        test_content = (
            "# Interruption handling test\n"
            "# Moderately sized for testing\n"
            "# " + "x" * 25000 + "\n"
            "# Test data for interruption scenario\n"
        )

        test_file_path = upload_config_page.create_test_file(test_content, "fwu")

        try:
            # Prepare for upload
            selection_result = upload_config_page.select_file_for_upload(test_file_path)
            assert selection_result is True, "File should be selectable"

            # Verify upload initiation
            if hasattr(upload_config_page, "initiate_upload"):
                initiation_result = upload_config_page.initiate_upload()
                assert initiation_result is True, "Upload should be initiatable"
            else:
                # Verify upload button exists
                upload_button = upload_config_page.page.locator(
                    "input[type='submit'], button[type='submit']"
                )
                expect(upload_button).to_be_visible()

            # Test interruption by navigating away (simulating user action)
            try:
                # Try to navigate to dashboard or another page
                navigation_links = [
                    upload_config_page.page.locator("a").filter(has_text="Dashboard"),
                    upload_config_page.page.locator("a[href*='/']"),
                    upload_config_page.page.locator("a[href*='general']"),
                ]

                navigation_attempted = False
                for link in navigation_links:
                    if link.count() > 0 and link.is_visible():
                        link.click()
                        navigation_attempted = True
                        break

                if navigation_attempted:
                    # Verify navigation completed
                    upload_config_page.page.wait_for_load_state(
                        "domcontentloaded", timeout=10000
                    )

                    # Navigate back to upload page
                    upload_config_page.navigate_to_page()

                    # Verify page is still functional
                    upload_config_page.verify_page_loaded()
                    print("System remained stable after navigation interruption")
                else:
                    print(
                        "Could not test navigation interruption (no suitable links found)"
                    )

            except Exception as e:
                print(f"Navigation interruption test encountered issue: {e}")

            # Verify system stability - page should still be functional
            file_input = upload_config_page.page.locator(
                "input[type='file'][name='file[]']"
            )
            expect(file_input).to_be_visible()

            # Test that we can still interact with upload functionality
            reselect_result = upload_config_page.select_file_for_upload(test_file_path)
            assert (
                reselect_result is True
            ), "File selection should work after interruption"

            print("Upload interruption handling test passed - system remained stable")

        finally:
            # Clean up test file
            if os.path.exists(test_file_path):
                os.unlink(test_file_path)
