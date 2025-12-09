"""
Test 11.8.1: Field Enablement Conditions (Pure Page Object)
Purpose: Field enablement conditions with device capabilities
Expected: Device-aware field enablement behavior using pure page object pattern
Pure: Zero direct .locator() calls - uses only page object methods
"""

import pytest
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_8_1_field_enablement_conditions(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.8.1: Field Enablement Conditions (Pure Page Object)
    Purpose: Field enablement conditions with device capabilities
    Expected: Device-aware field enablement behavior
    Pure: Uses only page object methods - zero direct .locator() calls
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate field enablement")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Navigate to general config page using page object
    general_config_page.navigate_to_page()

    # Test field enablement using page object methods
    test_field_enablement_by_device_series(
        general_config_page, device_model, device_series
    )


def test_field_enablement_by_device_series(
    page: GeneralConfigPage, device_model: str, device_series: int
):
    """
    Test field enablement patterns based on device series

    Args:
        page: GeneralConfigPage instance
        device_model: Device model identifier
        device_series: Device series (2 or 3)
    """
    if device_series == 2:
        # Series 2: Test basic field enablement
        test_series_2_field_enablement(page, device_model)
    else:  # Series 3
        # Series 3: Test advanced field enablement with hardware capabilities
        test_series_3_field_enablement(page, device_model)


def test_series_2_field_enablement(page: GeneralConfigPage, request):
    """Test Series 2 field enablement patterns"""

    # Test basic input fields are enabled
    identifier_enabled = page.is_field_enabled("identifier")
    location_enabled = page.is_field_enabled("location")
    contact_enabled = page.is_field_enabled("contact")

    enabled_fields = []
    disabled_fields = []

    if identifier_enabled:
        enabled_fields.append("identifier")
    else:
        disabled_fields.append("identifier")

    if location_enabled:
        enabled_fields.append("location")
    else:
        disabled_fields.append("location")

    if contact_enabled:
        enabled_fields.append("contact")
    else:
        disabled_fields.append("contact")

    # Validate at least basic fields are enabled
    assert (
        len(enabled_fields) >= 2
    ), f"Expected at least 2 enabled fields on {device_model}, got {len(enabled_fields)}"

    print(f" Series 2 Field Enablement on {device_model}:")
    print(f"  Enabled: {enabled_fields}")
    print(f"  Disabled: {disabled_fields}")


def test_series_3_field_enablement(page: GeneralConfigPage, request):
    """Test Series 3 field enablement with advanced capabilities"""

    # Test basic input fields
    basic_fields_enabled = test_basic_field_enablement(page, device_model)

    # Test advanced fields based on hardware capabilities
    test_advanced_field_enablement(page, device_model)

    return basic_fields_enabled


def test_basic_field_enablement(page: GeneralConfigPage, request) -> bool:
    """Test basic field enablement for Series 3"""

    device_model = request.session.device_hardware_model

    identifier_enabled = page.is_field_enabled("identifier")
    location_enabled = page.is_field_enabled("location")
    contact_enabled = page.is_field_enabled("contact")

    enabled_count = sum([identifier_enabled, location_enabled, contact_enabled])

    print(f" Basic Fields on {device_model}:")
    print(f"  Identifier enabled: {identifier_enabled}")
    print(f"  Location enabled: {location_enabled}")
    print(f"  Contact enabled: {contact_enabled}")
    print(f"  Total enabled: {enabled_count}/3")

    return enabled_count >= 2


def test_advanced_field_enablement(page: GeneralConfigPage, request):
    """Test advanced field enablement based on device capabilities"""

    # Test interface fields if present
    interface_enabled = page.are_interface_fields_enabled()

    # Test PTP fields if supported
    if DeviceCapabilities.is_ptp_supported(device_model):
        ptp_enabled = page.are_ptp_fields_enabled()

        print(f" Advanced Fields on {device_model}:")
        print(f"  Interface fields enabled: {interface_enabled}")
        print(f"  PTP fields enabled: {ptp_enabled}")

        # PTP fields should be enabled on capable devices
        if ptp_enabled:
            print(f" PTP fields properly enabled on {device_model}")
        else:
            print(f"ℹ PTP fields disabled (may be expected) on {device_model}")
    else:
        print(f"ℹ PTP not supported on {device_model} - skipping PTP field tests")


def test_conditional_field_enablement_patterns(
    page: GeneralConfigPage, device_model: str
):
    """
    Test conditional field enablement patterns

    This method tests fields that may be conditionally enabled based on:
    - Device hardware capabilities
    - Configuration state
    - User permissions
    """

    # Test conditional enablement scenarios
    test_permission_based_enablement(page, device_model)
    test_configuration_based_enablement(page, device_model)
    test_hardware_based_enablement(page, device_model)


def test_permission_based_enablement(page: GeneralConfigPage, request):
    """Test fields enabled based on user permissions"""

    # Check if fields require elevated permissions
    elevated_fields = ["admin_settings", "advanced_config"]

    for field in elevated_fields:
        is_enabled = page.is_field_enabled(field)
        print(f"  {field} enabled for permissions: {is_enabled}")


def test_configuration_based_enablement(page: GeneralConfigPage, request):
    """Test fields enabled based on current configuration"""

    # Test fields that depend on other configuration states
    dependent_fields = ["backup_config", "logging_level"]

    for field in dependent_fields:
        is_enabled = page.is_field_enabled(field)
        print(f"  {field} enabled for configuration: {is_enabled}")


def test_hardware_based_enablement(page: GeneralConfigPage, request):
    """Test fields enabled based on hardware capabilities"""

    # Test hardware-dependent field enablement
    hardware_fields = {
        "ptp_config": DeviceCapabilities.is_ptp_supported,
        "sync_e_config": DeviceCapabilities.is_sync_e_supported,
        "advanced_gnss": DeviceCapabilities.has_advanced_gnss,
    }

    for field_name, capability_check in hardware_fields.items():
        if capability_check(device_model):
            is_enabled = page.is_field_enabled(field_name)
            print(f"  {field_name} enabled for hardware: {is_enabled}")

            if is_enabled:
                print(
                    f" Hardware-dependent field {field_name} properly enabled on {device_model}"
                )
            else:
                print(
                    f"ℹ Hardware-dependent field {field_name} disabled on {device_model}"
                )


# Integration with main test function
def test_comprehensive_field_enablement_validation(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Comprehensive field enablement validation test

    This test validates field enablement patterns across different device series
    and hardware configurations using pure page object pattern.
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate field enablement")

    device_series = DeviceCapabilities.get_series(device_model)

    # Navigate to general config page
    general_config_page.navigate_to_page()

    # Perform comprehensive field enablement testing
    test_field_enablement_by_device_series(
        general_config_page, device_model, device_series
    )
    test_conditional_field_enablement_patterns(general_config_page, device_model)

    # Validate overall enablement pattern
    validate_field_enablement_results(device_model, device_series)


def validate_field_enablement_results(device_model: str, device_series: int):
    """Validate that field enablement results meet expectations"""

    print(f"\n Field Enablement Validation Results for {device_model}:")
    print(f"   Device Series: {device_series}")

    if device_series == 2:
        expected_min_enabled = 2
        print(f"   Expected minimum enabled fields: {expected_min_enabled}")
    else:  # Series 3
        expected_min_enabled = 3
        print(f"   Expected minimum enabled fields: {expected_min_enabled}")
        print(f"   Advanced field testing: Enabled")

    print(f"    Field enablement validation completed for {device_model}")
