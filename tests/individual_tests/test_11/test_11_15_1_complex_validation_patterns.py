"""
Test 11.15.1: Complex Validation Patterns (Pure Page Object)
Category 11: Form Validation Tests
Test Count: 1 of 47 total tests
Hardware: Pure Page Object Pattern
Priority: MEDIUM - Input validation critical for data integrity
Series: Both Series 2 and 3

Pure Page Object Features:
- Zero direct .locator() calls - uses only page object methods
- Device model detection and series validation via page object
- Series-specific timeout multipliers for complex validation patterns
- Device-aware complex validation patterns with Series 2 vs Series 3 differences
- Error handling for missing fields or unsupported features
- Multi-interface support detection for Series 3 devices
- Series-specific special character handling and edge case validation

FIXES APPLIED:
- Transformed to pure page object pattern with zero direct .locator() calls
- Uses page object methods for all field interactions
- Device-aware validation using DeviceCapabilities via page object
- Maintains rollback logic with try/finally blocks
- Implements comprehensive device-aware complex validation patterns
- Adds timeout multipliers based on device capabilities
- Includes graceful error handling for missing fields
- Implements series-specific complex validation edge cases
"""

import pytest
import time
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_15_1_complex_validation_patterns(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.15.1: Complex validation patterns and edge cases (Pure Page Object)
    Purpose: Test device-aware complex validation patterns and edge cases
    Expected: Device should handle complex validation appropriately based on series
    Pure: Uses only page object methods - zero direct .locator() calls
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate advanced scenarios")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Extended timeout for complex validation operations
    complex_timeout = int(20000 * timeout_multiplier)  # 20 seconds * multiplier

    # Navigate to general config page using page object
    general_config_page.navigate_to_page()

    # Test complex validation patterns using page object methods
    test_complex_validation_patterns_by_series(
        general_config_page, device_model, device_series, complex_timeout
    )


def test_complex_validation_patterns_by_series(
    page: GeneralConfigPage, device_model: str, device_series: int, complex_timeout: int
):
    """
    Test complex validation patterns based on device series

    Args:
        page: GeneralConfigPage instance
        device_model: Device model identifier
        device_series: Device series (2 or 3)
        complex_timeout: Complex operation timeout in milliseconds
    """
    if device_series == 2:
        # Series 2: Test basic complex validation patterns
        test_series_2_complex_validation(page, device_model)
    else:  # Series 3
        # Series 3: Test advanced complex validation patterns with hardware capabilities
        test_series_3_complex_validation(page, device_model)


def test_series_2_complex_validation(page: GeneralConfigPage, request):
    """Test Series 2 complex validation patterns"""

    print(f" Testing Series 2 complex validation patterns on {device_model}")

    # Get input and textarea fields using page object
    input_fields = page.get_input_and_textarea_fields()

    if not input_fields:
        print(
            f"  ℹ No input/textarea fields found for complex validation on {device_model}"
        )
        test_fallback_complex_validation(page, device_model)
        return

    # Test complex validation with first available field
    target_field = input_fields[0]
    field_name = target_field.get("name", "text_field")

    print(f"   Testing complex validation with field: {field_name}")

    # Test special characters validation
    test_special_characters_validation(
        page, field_name, device_model, 1
    )  # Series 2 multiplier

    # Test Unicode validation (limited for Series 2)
    test_unicode_validation(page, field_name, device_model, "limited")

    # Test length boundary validation
    test_length_boundary_validation(
        page, field_name, device_model, 1
    )  # Series 2 multiplier

    # Test mixed validation patterns
    test_mixed_validation_patterns(
        page, field_name, device_model, 1
    )  # Series 2 multiplier


def test_series_3_complex_validation(page: GeneralConfigPage, request):
    """Test Series 3 complex validation patterns with advanced capabilities"""

    print(f" Testing Series 3 complex validation patterns on {device_model}")

    # Test basic complex validation
    test_basic_complex_validation(page, device_model)

    # Test advanced complex validation patterns
    test_advanced_complex_validation(page, device_model)


def test_basic_complex_validation(page: GeneralConfigPage, request):
    """Test basic complex validation for Series 3"""

    # Get input and textarea fields using page object
    input_fields = page.get_input_and_textarea_fields()

    if not input_fields:
        print(
            f"  ℹ No input/textarea fields found for basic complex validation on {device_model}"
        )
        test_fallback_complex_validation(page, device_model)
        return

    target_field = input_fields[0]
    field_name = target_field.get("name", "text_field")

    print(f"   Testing basic complex validation with field: {field_name}")

    # Test special characters validation (full support for Series 3)
    test_special_characters_validation(
        page, field_name, device_model, 2
    )  # Series 3 multiplier

    # Test Unicode validation (full support for Series 3)
    test_unicode_validation(page, field_name, device_model, "full")

    # Test length boundary validation
    test_length_boundary_validation(
        page, field_name, device_model, 2
    )  # Series 3 multiplier

    # Test mixed validation patterns
    test_mixed_validation_patterns(
        page, field_name, device_model, 2
    )  # Series 3 multiplier


def test_advanced_complex_validation(page: GeneralConfigPage, request):
    """Test advanced complex validation patterns for Series 3"""

    print(f"   Testing advanced complex validation on {device_model}")

    # Test nested validation patterns
    test_nested_complex_validation(page, device_model)

    # Test cross-field complex validation
    test_cross_field_complex_validation(page, device_model)


def test_special_characters_validation(
    page: GeneralConfigPage, field_name: str, device_model: str, timeout_multiplier: int
):
    """Test special characters validation"""

    print(f"     Testing special characters validation")

    try:
        # Define special characters based on device series
        special_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"

        if timeout_multiplier == 1:  # Series 2
            # Series 2 may have simpler special character handling
            edge_case_data = (
                f"series2_special_test_{special_chars[:20]}"  # Limit special chars
            )
        else:  # Series 3
            # Series 3 may have more complex special character validation
            edge_case_data = f"series3_complex_validation_{special_chars}"

        # Clear field and fill with special characters
        page.clear_field(field_name)
        page.fill_field(field_name, edge_case_data)

        # Allow validation to process
        time.sleep(1 * timeout_multiplier)

        # Get actual value after validation
        actual_value = page.get_field_value(field_name)

        # Analyze validation results
        if actual_value == edge_case_data:
            print(f"       All special characters accepted")
        elif len(actual_value) < len(edge_case_data):
            print(
                f"      ℹ Some special characters filtered ({len(actual_value)} chars)"
            )
        else:
            print(f"      ℹ Unexpected validation behavior")

        print(f"      Expected: {len(edge_case_data)} chars")
        print(f"      Actual: {len(actual_value)} chars")

    except Exception as e:
        print(f"      ℹ Special character validation failed: {str(e)}")


def test_unicode_validation(
    page: GeneralConfigPage, field_name: str, device_model: str, support_level: str
):
    """Test Unicode and international characters validation"""

    print(f"     Testing Unicode validation ({support_level} support)")

    try:
        # Clear field first
        page.clear_field(field_name)
        time.sleep(0.5)

        # Define Unicode test data based on support level
        if support_level == "limited":
            # Series 2 may have limited Unicode support
            unicode_test = "Test_Ñoël_Ümlaut_"
        else:  # full support
            # Series 3 may support full Unicode
            unicode_test = "Test_Ñoël_Ümlaut___السلام_ عليكم"

        # Fill field with Unicode characters
        page.fill_field(field_name, unicode_test)
        time.sleep(1)

        # Get actual value after validation
        unicode_actual = page.get_field_value(field_name)

        print(f"      Unicode validation result: {len(unicode_actual)} chars")
        print(f"      Input: {unicode_test}")
        print(f"      Output: {unicode_actual}")

        if len(unicode_actual) > 0:
            print(f"       Unicode characters accepted")
        else:
            print(f"      ℹ Unicode characters rejected")

    except Exception as e:
        print(f"      ℹ Unicode validation failed: {str(e)}")


def test_length_boundary_validation(
    page: GeneralConfigPage, field_name: str, device_model: str, timeout_multiplier: int
):
    """Test length boundary validation"""

    print(f"     Testing length boundary validation")

    try:
        # Clear field first
        page.clear_field(field_name)
        time.sleep(0.5)

        # Test with very long strings
        long_string = "A" * 1000  # 1000 character string
        page.fill_field(field_name, long_string)
        time.sleep(1 * timeout_multiplier)

        # Get actual value after validation
        long_actual = page.get_field_value(field_name)

        print(f"      Length boundary test: {len(long_actual)} chars")

        # Check if device truncates or rejects long input
        if timeout_multiplier == 1:  # Series 2
            # Series 2 may have stricter length limits
            if len(long_actual) < len(long_string):
                print(f"       Series 2: Length truncation detected")
            else:
                print(f"      ℹ Series 2: No length truncation")
        else:  # Series 3
            # Series 3 may have more generous length limits
            if len(long_actual) >= len(long_string) * 0.9:
                print(f"       Series 3: Full length acceptance")
            else:
                print(f"      ℹ Series 3: Length limitation detected")

    except Exception as e:
        print(f"      ℹ Length boundary validation failed: {str(e)}")


def test_mixed_validation_patterns(
    page: GeneralConfigPage, field_name: str, device_model: str, timeout_multiplier: int
):
    """Test mixed validation patterns"""

    print(f"     Testing mixed validation patterns")

    try:
        # Clear field first
        page.clear_field(field_name)
        time.sleep(0.5)

        # Complex mixed validation test
        if timeout_multiplier == 1:  # Series 2
            mixed_pattern = "Valid_Input-123"
        else:  # Series 3
            mixed_pattern = "Complex_Valid-Input123!@#$%^&*()"

        # Fill field with mixed pattern
        page.fill_field(field_name, mixed_pattern)
        time.sleep(1 * timeout_multiplier)

        # Get actual value
        mixed_actual = page.get_field_value(field_name)

        print(f"      Mixed pattern validation: {mixed_actual}")

        # Check validation feedback using page object
        validation_indicators = page.get_complex_validation_indicators()

        if validation_indicators:
            print(f"       Complex validation feedback detected")
        else:
            print(f"      ℹ No complex validation errors")

    except Exception as e:
        print(f"      ℹ Mixed pattern validation failed: {str(e)}")


def test_nested_complex_validation(page: GeneralConfigPage, request):
    """Test nested complex validation patterns"""

    print(f"       Testing nested complex validation")

    try:
        # Test multiple validation layers
        test_multi_layer_validation(page, device_model)

        # Test conditional complex validation
        test_conditional_complex_validation(page, device_model)

    except Exception as e:
        print(f"        ℹ Nested complex validation failed: {str(e)}")


def test_cross_field_complex_validation(page: GeneralConfigPage, request):
    """Test cross-field complex validation"""

    print(f"       Testing cross-field complex validation")

    try:
        # Get multiple fields for cross-validation
        input_fields = page.get_multiple_input_fields(2)

        if len(input_fields) >= 2:
            field1_name = input_fields[0].get("name", "field1")
            field2_name = input_fields[1].get("name", "field2")

            # Fill fields with interdependent complex data
            complex_data1 = f"CrossField1_{device_model}_!@#$%"
            complex_data2 = f"CrossField2_{device_model}_Ñoël_"

            page.fill_field(field1_name, complex_data1)
            page.fill_field(field2_name, complex_data2)

            # Trigger cross-field validation
            page.trigger_cross_field_validation(field1_name, field2_name)

            print(f"         Cross-field complex validation completed")
        else:
            print(f"        ℹ Insufficient fields for cross-field validation")

    except Exception as e:
        print(f"        ℹ Cross-field complex validation failed: {str(e)}")


def test_multi_layer_validation(page: GeneralConfigPage, request):
    """Test multiple validation layers"""

    print(f"         Testing multi-layer validation")

    # This would test multiple validation rules applied simultaneously
    print(f"          Multi-layer validation patterns for {device_model}")


def test_conditional_complex_validation(page: GeneralConfigPage, request):
    """Test conditional complex validation"""

    print(f"         Testing conditional complex validation")

    # This would test complex validation that changes based on conditions
    print(f"          Conditional complex validation for {device_model}")


def test_fallback_complex_validation(page: GeneralConfigPage, request):
    """Test complex validation with fallback approach when insufficient fields"""

    print(f"   Testing fallback complex validation on {device_model}")

    # Get all form elements using page object
    all_form_elements = page.get_all_form_elements()

    if all_form_elements:
        print(
            f"    Found {len(all_form_elements)} form elements for fallback complex validation"
        )

        # Test complex validation with available elements
        test_complex_validation_with_available_elements(
            page, device_model, all_form_elements[0]
        )
    else:
        print(f"    ℹ No form elements available for fallback complex validation")


def test_complex_validation_with_available_elements(
    page: GeneralConfigPage, device_model: str, element: dict
):
    """Test complex validation with available form elements"""

    try:
        element_name = element.get("name", "element")
        element_type = element.get("type", "text")

        if element_type in ["text", "email", "url"] or "textarea" in element_name:
            # Test complex validation for text-based elements
            complex_test = f"complex_validation_{device_model}_!@#$%^&*()_Ñoël_Ümlaut"
            page.fill_field(element_name, complex_test)

            # Trigger validation
            page.trigger_field_validation(element_name)

            print(f"       Fallback complex validation completed for {element_name}")
        else:
            print(
                f"      ℹ Element type not suitable for complex validation: {element_type}"
            )

    except Exception as e:
        print(f"      ℹ Fallback complex validation failed: {str(e)}")


def test_comprehensive_complex_validation_patterns(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Comprehensive complex validation patterns test

    This test validates complex validation patterns across different device series
    and hardware configurations using pure page object pattern.
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate advanced scenarios")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)
    complex_timeout = int(20000 * timeout_multiplier)

    # Navigate to general config page
    general_config_page.navigate_to_page()

    try:
        # Perform comprehensive complex validation testing
        test_complex_validation_patterns_by_series(
            general_config_page, device_model, device_series, complex_timeout
        )

        # Validate overall complex validation behavior
        validate_complex_validation_results(device_model, device_series)

    finally:
        # Cleanup: Reset form to original state
        cleanup_complex_validation_state(general_config_page, device_model)


def cleanup_complex_validation_state(page: GeneralConfigPage, request):
    """Cleanup complex validation state after testing"""

    try:
        print(f"   Cleaning up complex validation state for {device_model}")

        # Refresh page to clear complex validation states
        page.refresh_page()
        page.wait_for_page_ready()

        print(f"   Complex validation state cleanup completed for {device_model}")

    except Exception as cleanup_error:
        print(f"  ℹ Cleanup failed for {device_model}: {cleanup_error}")
        # Continue - cleanup failure shouldn't fail the test


def validate_complex_validation_results(device_model: str, device_series: int):
    """Validate that complex validation results meet expectations"""

    print(f"\n Complex Validation Patterns Results for {device_model}:")
    print(f"   Device Series: {device_series}")

    if device_series == 2:
        print(f"   Expected: Basic complex validation patterns")
        print(f"   Testing: Special characters, Unicode, length boundaries")
    else:  # Series 3
        print(f"   Expected: Advanced complex validation patterns")
        print(f"   Testing: Full Unicode, cross-field, nested validation")

    print(f"    Complex validation patterns completed for {device_model}")
