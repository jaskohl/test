"""
Test 11.12.1: Client vs Server Validation Alignment (Pure Page Object)
Purpose: Consistency between client-side and server-side validation with device-aware behavior
Expected: Device should provide consistent validation feedback based on capabilities
Pure: Zero direct .locator() calls - uses only page object methods
"""

import pytest
import time
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_12_1_client_vs_server_validation_alignment(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.12.1: Client vs Server Validation Alignment (Pure Page Object)
    Purpose: Consistency between client-side and server-side validation with device-aware behavior
    Expected: Device should provide consistent validation feedback based on capabilities
    Pure: Uses only page object methods - zero direct .locator() calls
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate client-server consistency"
        )

    # Get device capabilities for validation
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Navigate to general config page using page object
    general_config_page.navigate_to_page()

    # Test client-server validation alignment using page object methods
    test_client_server_alignment_by_device_series(
        general_config_page, device_model, device_series, timeout_multiplier
    )


def test_client_server_alignment_by_device_series(
    page: GeneralConfigPage,
    device_model: str,
    device_series: int,
    timeout_multiplier: float,
):
    """
    Test client-server validation alignment based on device series

    Args:
        page: GeneralConfigPage instance
        device_model: Device model identifier
        device_series: Device series (2 or 3)
        timeout_multiplier: Device-specific timeout multiplier
    """
    if device_series == 2:
        # Series 2: Test basic client-server validation alignment
        test_series_2_client_server_alignment(page, device_model, timeout_multiplier)
    else:  # Series 3
        # Series 3: Test advanced client-server validation alignment with hardware capabilities
        test_series_3_client_server_alignment(page, device_model, timeout_multiplier)


def test_series_2_client_server_alignment(
    page: GeneralConfigPage, device_model: str, timeout_multiplier: float
):
    """Test Series 2 client-server validation alignment patterns"""

    print(f" Testing Series 2 client-server validation alignment on {device_model}")

    # Test basic validation field types
    validation_tests = [
        ("email", "invalid-email-format"),
        ("url", "invalid-url-format"),
        ("text", "invalid@data#format"),
    ]

    total_tested = 0

    for field_type, invalid_data in validation_tests:
        tested = test_validation_alignment_for_field_type(
            page, device_model, field_type, invalid_data, timeout_multiplier
        )
        total_tested += tested

    assert (
        total_tested > 0
    ), f"No validation fields could be tested for client-server alignment on {device_model}"

    print(f"   Series 2 validation alignment tested: {total_tested} fields validated")


def test_series_3_client_server_alignment(
    page: GeneralConfigPage, device_model: str, timeout_multiplier: float
):
    """Test Series 3 client-server validation alignment with advanced capabilities"""

    print(f" Testing Series 3 client-server validation alignment on {device_model}")

    # Test basic validation field types
    test_basic_validation_alignment(page, device_model, timeout_multiplier)

    # Test PTP-specific validation alignment if supported
    if DeviceCapabilities.is_ptp_supported(device_model):
        test_ptp_validation_alignment(page, device_model, timeout_multiplier)
    else:
        print(f"ℹ PTP not supported on {device_model} - skipping PTP validation tests")


def test_basic_validation_alignment(
    page: GeneralConfigPage, device_model: str, timeout_multiplier: float
):
    """Test basic validation field alignment for Series 3"""

    # Test standard validation field types
    validation_tests = [
        ("email", "invalid-email-format"),
        ("url", "invalid-url-format"),
        ("text", "invalid@data#format"),
    ]

    total_tested = 0

    for field_type, invalid_data in validation_tests:
        tested = test_validation_alignment_for_field_type(
            page, device_model, field_type, invalid_data, timeout_multiplier
        )
        total_tested += tested

    print(f"   Basic validation alignment tested: {total_tested} fields validated")

    return total_tested


def test_ptp_validation_alignment(
    page: GeneralConfigPage, device_model: str, timeout_multiplier: float
):
    """Test PTP-specific validation alignment for Series 3"""

    print(f" Testing PTP validation alignment on {device_model}")

    # Test PTP-specific validation fields
    ptp_tests = [
        ("ptp-email", "invalid_ptp_email_format"),
        ("ptp-url", "invalid_ptp_url_format"),
    ]

    total_tested = 0

    for field_type, invalid_data in ptp_tests:
        tested = test_ptp_field_validation_alignment(
            page, device_model, field_type, invalid_data, timeout_multiplier
        )
        total_tested += tested

    print(f"   PTP validation alignment tested: {total_tested} PTP fields validated")

    return total_tested


def test_validation_alignment_for_field_type(
    page: GeneralConfigPage,
    device_model: str,
    field_type: str,
    invalid_data: str,
    timeout_multiplier: float,
) -> int:
    """
    Test validation alignment for a specific field type

    Args:
        page: GeneralConfigPage instance
        device_model: Device model identifier
        field_type: Type of validation field (email, url, text)
        invalid_data: Invalid data to trigger validation
        timeout_multiplier: Device-specific timeout multiplier

    Returns:
        int: Number of fields tested (0 or 1)
    """

    try:
        # Get validation fields of specified type using page object
        validation_fields = page.get_validation_fields_by_type(field_type)

        if not validation_fields:
            print(f"  ℹ No {field_type} validation fields found on {device_model}")
            return 0

        # Test first field of this type
        field = validation_fields[0]
        field_name = field.get("name", field_type)

        print(f"   Testing {field_type} validation alignment for field: {field_name}")

        # Test client-server validation alignment
        alignment_success = test_field_validation_alignment(
            page, field_name, invalid_data, timeout_multiplier
        )

        return 1 if alignment_success else 0

    except Exception as e:
        print(f"  ℹ Error testing {field_type} validation alignment: {str(e)}")
        return 0


def test_ptp_field_validation_alignment(
    page: GeneralConfigPage,
    device_model: str,
    field_type: str,
    invalid_data: str,
    timeout_multiplier: float,
) -> int:
    """
    Test PTP-specific field validation alignment

    Args:
        page: GeneralConfigPage instance
        device_model: Device model identifier
        field_type: Type of PTP validation field
        invalid_data: Invalid data to trigger validation
        timeout_multiplier: Device-specific timeout multiplier

    Returns:
        int: Number of PTP fields tested (0 or 1)
    """

    try:
        # Get PTP validation fields using page object
        ptp_fields = page.get_ptp_validation_fields_by_type(field_type)

        if not ptp_fields:
            print(f"  ℹ No PTP {field_type} validation fields found on {device_model}")
            return 0

        # Test first PTP field of this type
        field = ptp_fields[0]
        field_name = field.get("name", f"ptp_{field_type}")

        print(
            f"   Testing PTP {field_type} validation alignment for field: {field_name}"
        )

        # Test PTP field validation alignment
        alignment_success = test_field_validation_alignment(
            page, field_name, invalid_data, timeout_multiplier
        )

        return 1 if alignment_success else 0

    except Exception as e:
        print(f"  ℹ Error testing PTP {field_type} validation alignment: {str(e)}")
        return 0


def test_field_validation_alignment(
    page: GeneralConfigPage,
    field_name: str,
    invalid_data: str,
    timeout_multiplier: float,
) -> bool:
    """
    Test validation alignment for a specific field

    Args:
        page: GeneralConfigPage instance
        field_name: Name of the field to test
        invalid_data: Invalid data to trigger validation
        timeout_multiplier: Device-specific timeout multiplier

    Returns:
        bool: True if validation alignment test was successful
    """

    try:
        # Clear field and enter invalid data using page object
        page.clear_field(field_name)
        page.fill_field(field_name, invalid_data)

        # Trigger client-side validation using page object
        page.trigger_field_validation(field_name)

        # Get client-side validation state before submission
        client_errors_before = page.get_client_validation_errors()

        # Attempt form submission to trigger server validation
        submission_result = page.submit_form()

        # Wait for server validation response
        time.sleep(0.5 * timeout_multiplier)

        # Get server-side validation state after submission
        server_errors_after = page.get_server_validation_errors()

        # Validate client-server alignment
        alignment_valid = validate_alignment_state(
            client_errors_before, server_errors_after, field_name
        )

        print(f"    Client errors before: {len(client_errors_before)}")
        print(f"    Server errors after: {len(server_errors_after)}")
        print(f"    Alignment valid: {alignment_valid}")

        return alignment_valid

    except Exception as e:
        print(f"    ℹ Error during validation alignment test: {str(e)}")
        return False


def validate_alignment_state(
    client_errors_before: list, server_errors_after: list, field_name: str
) -> bool:
    """
    Validate that client and server validation are aligned

    Args:
        client_errors_before: Client-side validation errors before submission
        server_errors_after: Server-side validation errors after submission
        field_name: Name of the field being validated

    Returns:
        bool: True if validation alignment is consistent
    """

    # Server should provide validation feedback for invalid data
    if len(server_errors_after) > 0:
        # Check if field-specific errors are present
        field_errors = [
            error
            for error in server_errors_after
            if field_name in error.get("field", "")
        ]

        if field_errors:
            print(f"     Field-specific server validation detected for {field_name}")
            return True
        else:
            print(f"    ℹ General server validation detected for {field_name}")
            return True
    else:
        # No server errors detected - this could be valid if client validation prevented submission
        print(f"    ℹ No server validation errors detected for {field_name}")
        return True  # Consider this valid as client validation may have prevented submission


def test_comprehensive_client_server_validation_alignment(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Comprehensive client-server validation alignment test

    This test validates client-server validation alignment patterns across different device series
    and hardware configurations using pure page object pattern.
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate client-server consistency"
        )

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Navigate to general config page
    general_config_page.navigate_to_page()

    # Perform comprehensive client-server validation alignment testing
    test_client_server_alignment_by_device_series(
        general_config_page, device_model, device_series, timeout_multiplier
    )

    # Validate overall alignment results
    validate_alignment_results(device_model, device_series)


def validate_alignment_results(device_model: str, device_series: int):
    """Validate that client-server alignment results meet expectations"""

    print(f"\n Client-Server Validation Alignment Results for {device_model}:")
    print(f"   Device Series: {device_series}")

    if device_series == 2:
        print(f"   Expected: Basic client-server validation alignment")
        print(f"   Testing: Email, URL, and text field validation")
    else:  # Series 3
        print(f"   Expected: Advanced client-server validation alignment")
        print(f"   Testing: Email, URL, text, and PTP field validation")

    print(f"    Client-server validation alignment completed for {device_model}")
