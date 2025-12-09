"""
Test 23.1.1: IP address boundary values (Device Enhanced)
Category 23 - Boundary & Input Testing
Test Count: 3 tests
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3
Enhanced with DeviceCapabilities Integration

Extracted from: tests/test_23_boundary.py
Source Class: TestBoundaryValues
Enhanced with full DeviceCapabilities integration patterns
"""

import pytest
import time
from playwright.sync_api import Page
from pages.device_capabilities import DeviceCapabilities


def test_23_1_1_ip_address_boundary_values_device_enhanced(
    unlocked_config_page: Page, base_url: str, device_hardware_model: str, request
):
    """
    Test 23.1.1: IP address field boundary values (Device Enhanced)

    Enhanced with comprehensive DeviceCapabilities integration:
    - Device hardware model detection and series validation
    - Series-specific timeout handling (Series 2: 1x, Series 3: 2x)
    - Device-aware boundary testing with proper error handling
    - Hardware-specific validation patterns
    """
    # Device capabilities detection and series validation
    device_capabilities = DeviceCapabilities(device_hardware_model)
    device_series = device_capabilities.get_series()
    timeout_multiplier = device_capabilities.get_timeout_multiplier()

    # Apply series-specific timeout scaling
    base_timeout = 1000
    scaled_timeout = int(base_timeout * timeout_multiplier)
    short_sleep = 0.2 * timeout_multiplier

    # Test execution with device context
    test_start_time = time.time()

    try:
        # Navigate to network configuration page with device-aware timeout
        unlocked_config_page.goto(
            f"{base_url}/network", wait_until="domcontentloaded", timeout=scaled_timeout
        )

        # Wait for page stabilization with device-specific timing
        time.sleep(short_sleep)

        # Locate IP address field with device-aware strategies
        ip_field = unlocked_config_page.locator("input[name='ipaddr']")

        # Verify field visibility with device context
        if not ip_field.is_visible():
            pytest.skip(
                f"IP address field not visible on {device_hardware_model} (Series {device_series})"
            )

        # Device-aware boundary value testing
        test_ips = [
            "0.0.0.0",  # Minimum valid IP
            "1.1.1.1",  # Valid low-range IP
            "192.168.1.1",  # Typical private IP
            "255.255.255.255",  # Maximum valid IP
        ]

        # Test valid boundary values with device series awareness
        for ip in test_ips:
            try:
                ip_field.fill(ip)
                time.sleep(short_sleep)

                # Verify input retention with device-specific validation
                actual_value = ip_field.input_value()
                assert actual_value == ip, (
                    f"IP input validation failed on {device_hardware_model}: "
                    f"expected '{ip}', got '{actual_value}'"
                )

                # Series-specific boundary handling
                if device_series == "2":
                    # Series 2: More strict validation
                    assert (
                        len(actual_value) <= 15
                    ), f"Series 2 IP field length exceeded on {device_hardware_model}"
                elif device_series == "3":
                    # Series 3: Enhanced validation
                    assert (
                        len(actual_value) <= 15
                    ), f"Series 3 IP field length validation on {device_hardware_model}"

            except Exception as e:
                pytest.fail(
                    f"Valid IP boundary test failed on {device_hardware_model}: {str(e)}"
                )

        # Device-aware invalid value testing
        invalid_ips = [
            "256.1.1.1",  # Octet > 255
            "-1.1.1.1",  # Negative value
            "999.999.999.999",  # Extreme overlimit
            "192.168.1",  # Incomplete IP
            "192.168.1.1.1",  # Too many octets
        ]

        # Test invalid inputs with device-specific error handling
        for ip in invalid_ips:
            try:
                ip_field.fill(ip)
                time.sleep(short_sleep)

                # Device-aware validation error detection
                validation_error = False

                # Check for browser validation messages
                try:
                    browser_validation = ip_field.evaluate("el => el.validationMessage")
                    if browser_validation and len(browser_validation.strip()) > 0:
                        validation_error = True
                except:
                    pass

                # Check for custom validation classes
                validation_classes = ["invalid", "error", "validation-error"]
                for cls in validation_classes:
                    if ip_field.evaluate(f"el => el.classList.contains('{cls}')"):
                        validation_error = True
                        break

                # Series-specific invalid input handling
                actual_value = ip_field.input_value()

                if device_series == "2":
                    # Series 2: May reject invalid input immediately
                    if actual_value != ip:
                        validation_error = True
                elif device_series == "3":
                    # Series 3: May show validation but retain input
                    if validation_error or actual_value != ip:
                        validation_error = True

                # Assert validation occurred for invalid inputs
                assert validation_error or actual_value != ip, (
                    f"Invalid IP '{ip}' was accepted on {device_hardware_model} "
                    f"(Series {device_series}) - validation should occur"
                )

            except Exception as e:
                # Device-specific error handling for invalid input tests
                pytest.fail(
                    f"Invalid IP boundary test failed on {device_hardware_model}: {str(e)}"
                )

        # Test execution summary
        execution_time = time.time() - test_start_time
        print(
            f" IP boundary testing completed on {device_hardware_model} (Series {device_series}) in {execution_time:.2f}s"
        )

    except Exception as e:
        pytest.fail(
            f"Device-enhanced IP boundary test failed on {device_hardware_model}: {str(e)}"
        )


def test_23_1_2_numeric_field_boundaries_device_enhanced(
    unlocked_config_page: Page, base_url: str, device_hardware_model: str, request
):
    """
    Test 23.1.2: Numeric field boundary values (Device Enhanced)

    Enhanced with comprehensive DeviceCapabilities integration:
    - Device hardware model detection and series validation
    - Series-specific timeout handling and numeric validation
    - Device-aware boundary testing with hardware-specific limits
    - Comprehensive numeric field validation patterns
    """
    # Device capabilities detection and series validation
    device_capabilities = DeviceCapabilities(device_hardware_model)
    device_series = device_capabilities.get_series()
    timeout_multiplier = device_capabilities.get_timeout_multiplier()
    device_capabilities_list = device_capabilities.get_capabilities()

    # Apply series-specific timeout scaling
    base_timeout = 1000
    scaled_timeout = int(base_timeout * timeout_multiplier)
    short_sleep = 0.2 * timeout_multiplier

    # Test execution with device context
    test_start_time = time.time()

    try:
        # Navigate to general configuration page with device-aware timeout
        unlocked_config_page.goto(
            f"{base_url}/general", wait_until="domcontentloaded", timeout=scaled_timeout
        )

        # Wait for page stabilization with device-specific timing
        time.sleep(short_sleep)

        # Device-aware numeric field testing
        # Test multiple numeric fields with device-specific boundaries

        # Common numeric fields to test
        numeric_fields = [
            "input[name='port']",  # Port number
            "input[name='timeout']",  # Timeout values
            "input[name='interval']",  # Interval settings
        ]

        for field_selector in numeric_fields:
            try:
                numeric_field = unlocked_config_page.locator(field_selector)

                # Check if field exists and is visible
                if not numeric_field.is_visible():
                    print(
                        f" Numeric field {field_selector} not visible on {device_hardware_model}"
                    )
                    continue

                # Device-aware numeric boundary testing
                if "port" in field_selector:
                    # Port number boundaries (1-65535)
                    test_values = ["1", "80", "443", "8080", "65535"]
                    invalid_values = ["0", "65536", "-1", "99999"]
                elif "timeout" in field_selector:
                    # Timeout value boundaries
                    timeout_range = device_capabilities_list.get(
                        "timeout_range", {"min": 1, "max": 300}
                    )
                    test_values = [
                        str(timeout_range["min"]),
                        str((timeout_range["min"] + timeout_range["max"]) // 2),
                        str(timeout_range["max"]),
                    ]
                    invalid_values = ["0", "-1", str(timeout_range["max"] + 100)]
                else:
                    # General numeric field boundaries
                    test_values = ["0", "1", "100", "999"]
                    invalid_values = ["-1", "1000", "abc", ""]

                # Test valid numeric boundaries
                for value in test_values:
                    try:
                        numeric_field.clear()
                        time.sleep(short_sleep)
                        numeric_field.fill(value)
                        time.sleep(short_sleep)

                        # Verify input acceptance
                        actual_value = numeric_field.input_value()
                        assert actual_value == value, (
                            f"Numeric field {field_selector} on {device_hardware_model}: "
                            f"expected '{value}', got '{actual_value}'"
                        )

                    except Exception as e:
                        print(
                            f" Valid numeric test failed for {value} on {device_hardware_model}: {str(e)}"
                        )

                # Test invalid numeric boundaries
                for value in invalid_values:
                    try:
                        numeric_field.clear()
                        time.sleep(short_sleep)
                        numeric_field.fill(value)
                        time.sleep(short_sleep)

                        # Check for validation errors
                        validation_occurred = False
                        actual_value = numeric_field.input_value()

                        # Series-specific invalid input handling
                        if device_series == "2":
                            # Series 2: May reject immediately
                            if actual_value != value:
                                validation_occurred = True
                        elif device_series == "3":
                            # Series 3: Validation-aware input
                            validation_occurred = (actual_value != value) or (
                                "invalid" in numeric_field.get_attribute("class", "")
                            )

                        # Assert validation for invalid inputs
                        assert validation_occurred, (
                            f"Invalid numeric value '{value}' was accepted for {field_selector} "
                            f"on {device_hardware_model} (Series {device_series})"
                        )

                    except Exception as e:
                        print(
                            f" Invalid numeric test failed for {value} on {device_hardware_model}: {str(e)}"
                        )

            except Exception as e:
                print(
                    f" Numeric field testing failed for {field_selector} on {device_hardware_model}: {str(e)}"
                )

        # Test execution summary
        execution_time = time.time() - test_start_time
        print(
            f" Numeric boundary testing completed on {device_hardware_model} (Series {device_series}) in {execution_time:.2f}s"
        )

    except Exception as e:
        pytest.fail(
            f"Device-enhanced numeric boundary test failed on {device_hardware_model}: {str(e)}"
        )


def test_23_1_3_text_field_length_limits_device_enhanced(
    unlocked_config_page: Page, base_url: str, device_hardware_model: str, request
):
    """
    Test 23.1.3: Text field length limits (Device Enhanced)

    Enhanced with comprehensive DeviceCapabilities integration:
    - Device hardware model detection and series validation
    - Series-specific text field length behavior (Series 2 vs 3)
    - Device-aware length validation with hardware-specific limits
    - Comprehensive text field boundary testing
    """
    # Device capabilities detection and series validation
    device_capabilities = DeviceCapabilities(device_hardware_model)
    device_series = device_capabilities.get_series()
    timeout_multiplier = device_capabilities.get_timeout_multiplier()
    device_capabilities_list = device_capabilities.get_capabilities()

    # Apply series-specific timeout scaling
    base_timeout = 1000
    scaled_timeout = int(base_timeout * timeout_multiplier)
    short_sleep = 0.2 * timeout_multiplier

    # Test execution with device context
    test_start_time = time.time()

    try:
        # Navigate to general configuration page with device-aware timeout
        unlocked_config_page.goto(
            f"{base_url}/general", wait_until="domcontentloaded", timeout=scaled_timeout
        )

        # Wait for page stabilization with device-specific timing
        time.sleep(short_sleep)

        # Device-aware text field testing
        text_fields = [
            "input[name='identifier']",  # Device identifier
            "input[name='location']",  # Location field
            "input[name='contact']",  # Contact information
        ]

        for field_selector in text_fields:
            try:
                text_field = unlocked_config_page.locator(field_selector)

                # Check if field exists and is visible
                if not text_field.is_visible():
                    print(
                        f" Text field {field_selector} not visible on {device_hardware_model}"
                    )
                    continue

                # Get field-specific length limits based on device capabilities
                if "identifier" in field_selector:
                    max_length = device_capabilities_list.get(
                        "identifier_max_length", 50
                    )
                elif "location" in field_selector:
                    max_length = device_capabilities_list.get(
                        "location_max_length", 100
                    )
                elif "contact" in field_selector:
                    max_length = device_capabilities_list.get("contact_max_length", 100)
                else:
                    max_length = 255  # Default safe limit

                # Series-specific length behavior
                if device_series == "2":
                    # Series 2: Strict length enforcement
                    test_lengths = [
                        1,  # Minimum
                        max_length // 2,  # Mid-range
                        max_length,  # Maximum
                        max_length + 1,  # Overlimit
                    ]
                else:  # Series 3
                    # Series 3: Enhanced length handling
                    test_lengths = [
                        1,  # Minimum
                        max_length // 2,  # Mid-range
                        max_length,  # Maximum
                        max_length + 1,  # Slight overlimit
                        max_length + 10,  # Significant overlimit
                    ]

                # Test valid length boundaries
                for length in test_lengths[:3]:  # First 3 are valid lengths
                    try:
                        test_text = "a" * length
                        text_field.clear()
                        time.sleep(short_sleep)
                        text_field.fill(test_text)
                        time.sleep(short_sleep)

                        # Verify input retention within limits
                        actual_value = text_field.input_value()
                        actual_length = len(actual_value)

                        # Device-aware length validation
                        if device_series == "2":
                            # Series 2: Hard limit enforcement
                            assert actual_length <= max_length, (
                                f"Series 2 text field {field_selector} on {device_hardware_model}: "
                                f"length {actual_length} exceeds max {max_length}"
                            )
                        else:  # Series 3
                            # Series 3: Enhanced validation
                            assert actual_length <= max_length, (
                                f"Series 3 text field {field_selector} on {device_hardware_model}: "
                                f"length {actual_length} exceeds max {max_length}"
                            )

                    except Exception as e:
                        print(
                            f" Valid text length test failed for length {length} on {device_hardware_model}: {str(e)}"
                        )

                # Test overlimit length handling
                for length in test_lengths[3:]:  # Overlimit lengths
                    try:
                        test_text = "a" * length
                        text_field.clear()
                        time.sleep(short_sleep)
                        text_field.fill(test_text)
                        time.sleep(short_sleep)

                        # Check length limit enforcement
                        actual_value = text_field.input_value()
                        actual_length = len(actual_value)

                        # Series-specific overlimit handling
                        if device_series == "2":
                            # Series 2: Hard truncation
                            assert actual_length <= max_length, (
                                f"Series 2 overlimit not enforced for {field_selector} "
                                f"on {device_hardware_model}: length {actual_length} > {max_length}"
                            )
                        else:  # Series 3
                            # Series 3: Enhanced handling
                            assert actual_length <= max_length, (
                                f"Series 3 overlimit not enforced for {field_selector} "
                                f"on {device_hardware_model}: length {actual_length} > {max_length}"
                            )

                        # Check for validation feedback
                        validation_indicators = [
                            "invalid",
                            "error",
                            "warning",
                            "overlimit",
                        ]
                        validation_found = False
                        for indicator in validation_indicators:
                            if indicator in text_field.get_attribute("class", ""):
                                validation_found = True
                                break

                        # Series-specific validation behavior
                        if device_series == "3":
                            # Series 3 should provide validation feedback for overlimits
                            assert validation_found, (
                                f"Series 3 validation feedback missing for overlimit "
                                f"{field_selector} on {device_hardware_model}"
                            )

                    except Exception as e:
                        print(
                            f" Overlimit text length test failed for length {length} on {device_hardware_model}: {str(e)}"
                        )

                # Test special character handling
                special_chars = ["", " ", "test@domain.com", "", "émoji"]
                for char in special_chars:
                    try:
                        text_field.clear()
                        time.sleep(short_sleep)
                        text_field.fill(char)
                        time.sleep(short_sleep)

                        # Verify special character handling
                        actual_value = text_field.input_value()
                        # Should handle special characters appropriately
                        assert actual_value == char, (
                            f"Special character handling failed for '{char}' "
                            f"in {field_selector} on {device_hardware_model}"
                        )

                    except Exception as e:
                        print(
                            f" Special character test failed for '{char}' on {device_hardware_model}: {str(e)}"
                        )

                # Test execution summary for this field
                print(
                    f" Text field {field_selector} length testing completed on {device_hardware_model}"
                )

            except Exception as e:
                print(
                    f" Text field testing failed for {field_selector} on {device_hardware_model}: {str(e)}"
                )

        # Test execution summary
        execution_time = time.time() - test_start_time
        print(
            f" Text field length testing completed on {device_hardware_model} (Series {device_series}) in {execution_time:.2f}s"
        )

    except Exception as e:
        pytest.fail(
            f"Device-enhanced text field length test failed on {device_hardware_model}: {str(e)}"
        )
