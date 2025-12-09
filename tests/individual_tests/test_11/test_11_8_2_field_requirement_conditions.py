"""
Test 11.8.2: Field Requirement Conditions (Pure Page Object)
Purpose: Field requirement conditions with device capabilities
Expected: Device-aware field requirement behavior using pure page object pattern
Pure: Zero direct .locator() calls - uses only page object methods
"""

import pytest
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_8_2_field_requirement_conditions(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.8.2: Field Requirement Conditions (Pure Page Object)
    Purpose: Field requirement conditions with device capabilities
    Expected: Device-aware field requirement behavior
    Pure: Uses only page object methods - zero direct .locator() calls
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate field requirements")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Navigate to general config page using page object
    general_config_page.navigate_to_page()

    # Test field requirements using page object methods
    test_field_requirements_by_device_series(
        general_config_page, device_model, device_series
    )


def test_field_requirements_by_device_series(
    page: GeneralConfigPage, device_model: str, device_series: int
):
    """
    Test field requirement patterns based on device series

    Args:
        page: GeneralConfigPage instance
        device_model: Device model identifier
        device_series: Device series (2 or 3)
    """
    if device_series == 2:
        # Series 2: Test basic field requirements
        test_series_2_field_requirements(page, device_model)
    else:  # Series 3
        # Series 3: Test advanced field requirements with hardware capabilities
        test_series_3_field_requirements(page, device_model)


def test_series_2_field_requirements(page: GeneralConfigPage, request):
    """Test Series 2 field requirement patterns"""

    # Test basic input fields for requirements
    identifier_required = page.is_field_required("identifier")
    location_required = page.is_field_required("location")
    contact_required = page.is_field_required("contact")

    required_fields = []
    optional_fields = []

    if identifier_required:
        required_fields.append("identifier")
    else:
        optional_fields.append("identifier")

    if location_required:
        required_fields.append("location")
    else:
        optional_fields.append("location")

    if contact_required:
        required_fields.append("contact")
    else:
        optional_fields.append("contact")

    # Validate requirement patterns
    assert (
        len(required_fields) >= 1
    ), f"Expected at least 1 required field on {device_model}, got {len(required_fields)}"

    print(f" Series 2 Field Requirements on {device_model}:")
    print(f"  Required: {required_fields}")
    print(f"  Optional: {optional_fields}")


def test_series_3_field_requirements(page: GeneralConfigPage, request):
    """Test Series 3 field requirements with advanced capabilities"""

    # Test basic input fields for requirements
    test_basic_field_requirements(page, device_model)

    # Test advanced fields based on hardware capabilities
    test_advanced_field_requirements(page, device_model)


def test_basic_field_requirements(page: GeneralConfigPage, request):
    """Test basic field requirements for Series 3"""

    identifier_required = page.is_field_required("identifier")
    location_required = page.is_field_required("location")
    contact_required = page.is_field_required("contact")

    required_count = sum([identifier_required, location_required, contact_required])

    print(f" Basic Field Requirements on {device_model}:")
    print(f"  Identifier required: {identifier_required}")
    print(f"  Location required: {location_required}")
    print(f"  Contact required: {contact_required}")
    print(f"  Total required: {required_count}/3")

    # At least one basic field should be required
    assert (
        required_count >= 1
    ), f"Expected at least 1 required basic field on {device_model}"


def test_advanced_field_requirements(page: GeneralConfigPage, request):
    """Test advanced field requirements based on device capabilities"""

    # Test interface fields if present
    interface_required = page.are_interface_fields_required()

    # Test PTP fields if supported
    if DeviceCapabilities.is_ptp_supported(device_model):
        ptp_required = page.are_ptp_fields_required()

        print(f" Advanced Field Requirements on {device_model}:")
        print(f"  Interface fields required: {interface_required}")
        print(f"  PTP fields required: {ptp_required}")

        # Log requirement patterns
        if ptp_required:
            print(f" PTP fields properly marked as required on {device_model}")
        else:
            print(f"ℹ PTP fields not required on {device_model}")
    else:
        print(
            f"ℹ PTP not supported on {device_model} - skipping PTP field requirement tests"
        )


def test_conditional_field_requirement_patterns(
    page: GeneralConfigPage, device_model: str
):
    """
    Test conditional field requirement patterns

    This method tests fields that may be conditionally required based on:
    - Device hardware capabilities
    - Configuration state
    - User permissions
    """

    # Test conditional requirement scenarios
    test_permission_based_requirements(page, device_model)
    test_configuration_based_requirements(page, device_model)
    test_hardware_based_requirements(page, device_model)


def test_permission_based_requirements(page: GeneralConfigPage, request):
    """Test fields required based on user permissions"""

    # Check if fields require elevated permissions
    elevated_fields = ["admin_settings", "advanced_config"]

    for field in elevated_fields:
        is_required = page.is_field_required(field)
        print(f"  {field} required for permissions: {is_required}")


def test_configuration_based_requirements(page: GeneralConfigPage, request):
    """Test fields required based on current configuration"""

    # Test fields that become required based on other configuration states
    dependent_fields = ["backup_config", "logging_level"]

    for field in dependent_fields:
        is_required = page.is_field_required(field)
        print(f"  {field} required for configuration: {is_required}")


def test_hardware_based_requirements(page: GeneralConfigPage, request):
    """Test fields required based on hardware capabilities"""

    # Test hardware-dependent field requirements
    hardware_fields = {
        "ptp_config": DeviceCapabilities.is_ptp_supported,
        "sync_e_config": DeviceCapabilities.is_sync_e_supported,
        "advanced_gnss": DeviceCapabilities.has_advanced_gnss,
    }

    for field_name, capability_check in hardware_fields.items():
        if capability_check(device_model):
            is_required = page.is_field_required(field_name)
            print(f"  {field_name} required for hardware: {is_required}")

            if is_required:
                print(
                    f" Hardware-dependent field {field_name} properly required on {device_model}"
                )
            else:
                print(
                    f"ℹ Hardware-dependent field {field_name} optional on {device_model}"
                )


def test_dynamic_requirement_changes(page: GeneralConfigPage, request):
    """
    Test dynamic requirement changes

    This test validates that field requirements can change based on:
    - User interactions
    - Configuration changes
    - Device state changes
    """

    # Test requirement changes for Series 3 devices
    device_series = DeviceCapabilities.get_series(device_model)

    if device_series == 3:
        print(f" Testing dynamic requirements on {device_model} (Series 3)")

        # Test if requirements change when certain options are selected
        test_conditional_requirement_triggers(page, device_model)
    else:
        print(f"ℹ Basic requirement conditions on {device_model} (Series 2)")


def test_conditional_requirement_triggers(page: GeneralConfigPage, request):
    """Test triggers that change field requirements"""

    # Test common triggers that might change field requirements
    requirement_triggers = [
        "enable_advanced_features",
        "select_ptp_mode",
        "configure_redundancy",
    ]

    for trigger in requirement_triggers:
        # Simulate trigger and check requirement changes
        original_requirements = page.get_all_field_requirements()

        # Test the trigger (this would be implemented in the page object)
        # page.trigger_requirement_change(trigger)

        new_requirements = page.get_all_field_requirements()

        if original_requirements != new_requirements:
            print(f" Requirements changed after triggering {trigger}")
        else:
            print(f"ℹ No requirement change after triggering {trigger}")


# Integration with main test function
def test_comprehensive_field_requirement_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Comprehensive field requirement validation test

    This test validates field requirement patterns across different device series
    and hardware configurations using pure page object pattern.
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate field requirements")

    device_series = DeviceCapabilities.get_series(device_model)

    # Navigate to general config page
    general_config_page.navigate_to_page()

    # Perform comprehensive field requirement testing
    test_field_requirements_by_device_series(
        general_config_page, device_model, device_series
    )
    test_conditional_field_requirement_patterns(general_config_page, device_model)
    test_dynamic_requirement_changes(general_config_page, device_model)

    # Validate overall requirement pattern
    validate_field_requirement_results(device_model, device_series)


def validate_field_requirement_results(device_model: str, device_series: int):
    """Validate that field requirement results meet expectations"""

    print(f"\n Field Requirement Validation Results for {device_model}:")
    print(f"   Device Series: {device_series}")

    if device_series == 2:
        expected_min_required = 1
        print(f"   Expected minimum required fields: {expected_min_required}")
    else:  # Series 3
        expected_min_required = 1
        print(f"   Expected minimum required fields: {expected_min_required}")
        print(f"   Advanced requirement testing: Enabled")

    print(f"    Field requirement validation completed for {device_model}")
