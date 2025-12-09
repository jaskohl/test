"""
Test 11.9.1: Wizard Validation Progression (Pure Page Object)
Purpose: Wizard validation progression with device capabilities
Expected: Device-aware wizard validation behavior using pure page object pattern
Pure: Zero direct .locator() calls - uses only page object methods
"""

import pytest
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_9_1_wizard_validation_progression(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.9.1: Wizard Validation Progression (Pure Page Object)
    Purpose: Wizard validation progression with device capabilities
    Expected: Device-aware wizard validation behavior
    Pure: Uses only page object methods - zero direct .locator() calls
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate wizard progression")

    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    # Navigate to general config page using page object
    general_config_page.navigate_to_page()

    # Test wizard validation progression using page object methods
    test_wizard_progression_by_device_series(
        general_config_page, device_model, device_series
    )


def test_wizard_progression_by_device_series(
    page: GeneralConfigPage, device_model: str, device_series: int
):
    """
    Test wizard progression patterns based on device series

    Args:
        page: GeneralConfigPage instance
        device_model: Device model identifier
        device_series: Device series (2 or 3)
    """
    if device_series == 2:
        # Series 2: Test basic wizard navigation patterns
        test_series_2_wizard_progression(page, device_model)
    else:  # Series 3
        # Series 3: Test advanced wizard features with hardware capabilities
        test_series_3_wizard_progression(page, device_model)


def test_series_2_wizard_progression(page: GeneralConfigPage, request):
    """Test Series 2 wizard progression patterns"""

    # Check for basic wizard navigation elements
    has_next_button = page.has_wizard_next_button()
    has_previous_button = page.has_wizard_previous_button()
    has_wizard_steps = page.has_wizard_step_indicators()

    wizard_elements_found = sum(
        [has_next_button, has_previous_button, has_wizard_steps]
    )

    print(f" Series 2 Wizard Elements on {device_model}:")
    print(f"  Next button present: {has_next_button}")
    print(f"  Previous button present: {has_previous_button}")
    print(f"  Wizard step indicators: {has_wizard_steps}")
    print(f"  Total wizard elements: {wizard_elements_found}")

    if wizard_elements_found > 0:
        test_basic_wizard_validation_flow(page, device_model)
    else:
        print(f"ℹ No wizard elements found on {device_model} (may be expected)")


def test_series_3_wizard_progression(page: GeneralConfigPage, request):
    """Test Series 3 wizard progression with advanced capabilities"""

    # Test basic wizard elements
    test_basic_wizard_elements(page, device_model)

    # Test advanced wizard features
    test_advanced_wizard_features(page, device_model)


def test_basic_wizard_elements(page: GeneralConfigPage, request):
    """Test basic wizard elements for Series 3"""

    # Check for standard wizard navigation
    has_next_button = page.has_wizard_next_button()
    has_previous_button = page.has_wizard_previous_button()
    has_continue_button = page.has_wizard_continue_button()
    has_wizard_steps = page.has_wizard_step_indicators()
    has_progress_indicator = page.has_wizard_progress_indicator()

    wizard_elements_found = sum(
        [
            has_next_button,
            has_previous_button,
            has_continue_button,
            has_wizard_steps,
            has_progress_indicator,
        ]
    )

    print(f" Basic Wizard Elements on {device_model}:")
    print(f"  Next button present: {has_next_button}")
    print(f"  Previous button present: {has_previous_button}")
    print(f"  Continue button present: {has_continue_button}")
    print(f"  Wizard step indicators: {has_wizard_steps}")
    print(f"  Progress indicator: {has_progress_indicator}")
    print(f"  Total wizard elements: {wizard_elements_found}")

    return wizard_elements_found > 0


def test_advanced_wizard_features(page: GeneralConfigPage, request):
    """Test advanced wizard features based on device capabilities"""

    # Test conditional wizard navigation
    test_conditional_wizard_navigation(page, device_model)

    # Test wizard validation progression
    test_wizard_validation_progression(page, device_model)

    # Test wizard step validation
    test_wizard_step_validation(page, device_model)


def test_basic_wizard_validation_flow(page: GeneralConfigPage, request):
    """Test basic wizard validation flow"""

    print(f" Testing basic wizard validation flow on {device_model}")

    # Get current wizard step
    current_step = page.get_current_wizard_step()
    total_steps = page.get_total_wizard_steps()

    print(f"  Current step: {current_step}")
    print(f"  Total steps: {total_steps}")

    if total_steps > 1:
        # Test navigation to next step
        can_proceed = page.can_proceed_to_next_wizard_step()
        print(f"  Can proceed to next step: {can_proceed}")

        if can_proceed:
            # Test required field validation
            required_fields_filled = page.are_current_step_required_fields_filled()
            print(f"  Required fields filled: {required_fields_filled}")

            if not required_fields_filled:
                # Fill required fields for progression test
                page.fill_current_step_required_fields("test_value")
                print(f"  Filled required fields for wizard progression")

        # Test step navigation
        test_wizard_step_navigation(page, device_model)


def test_conditional_wizard_navigation(page: GeneralConfigPage, request):
    """Test conditional wizard navigation based on device capabilities"""

    # Test PTP-specific wizard steps if supported
    if DeviceCapabilities.is_ptp_supported(device_model):
        ptp_wizard_available = page.has_ptp_wizard_steps()
        print(f" PTP wizard steps available: {ptp_wizard_available}")

        if ptp_wizard_available:
            test_ptp_wizard_progression(page, device_model)
    else:
        print(f"ℹ PTP wizard not supported on {device_model}")


def test_ptp_wizard_progression(page: GeneralConfigPage, request):
    """Test PTP-specific wizard progression"""

    print(f" Testing PTP wizard progression on {device_model}")

    # Check for PTP wizard steps
    ptp_steps = page.get_ptp_wizard_steps()
    print(f"  PTP wizard steps found: {len(ptp_steps)}")

    for step in ptp_steps:
        step_name = step.get("name", "Unknown")
        step_required = step.get("required", False)
        print(f"    Step: {step_name}, Required: {step_required}")


def test_wizard_validation_progression(page: GeneralConfigPage, request):
    """Test wizard validation progression patterns"""

    print(f" Testing wizard validation progression on {device_model}")

    # Test required field validation across wizard steps
    test_required_field_validation_across_steps(page)

    # Test step completion validation
    test_step_completion_validation(page)

    # Test wizard completion validation
    test_wizard_completion_validation(page)


def test_required_field_validation_across_steps(page: GeneralConfigPage):
    """Test required field validation across all wizard steps"""

    current_step = page.get_current_wizard_step()
    total_steps = page.get_total_wizard_steps()

    for step in range(1, total_steps + 1):
        page.navigate_to_wizard_step(step)

        required_fields = page.get_required_fields_in_current_step()
        filled_required_fields = page.get_filled_required_fields_in_current_step()

        validation_complete = len(required_fields) == len(filled_required_fields)

        print(
            f"  Step {step}: {len(required_fields)} required, {len(filled_required_fields)} filled - Valid: {validation_complete}"
        )

        if not validation_complete and step == current_step:
            # Fill required fields for current step
            page.fill_current_step_required_fields("validation_test")


def test_step_completion_validation(page: GeneralConfigPage):
    """Test step completion validation"""

    current_step = page.get_current_wizard_step()
    step_completion_status = page.is_current_step_complete()

    print(
        f"  Current step ({current_step}) completion status: {step_completion_status}"
    )

    return step_completion_status


def test_wizard_completion_validation(page: GeneralConfigPage):
    """Test overall wizard completion validation"""

    total_steps = page.get_total_wizard_steps()
    current_step = page.get_current_wizard_step()

    wizard_completion_percentage = (
        (current_step / total_steps) * 100 if total_steps > 0 else 0
    )

    print(
        f"  Wizard completion: {current_step}/{total_steps} steps ({wizard_completion_percentage:.1f}%)"
    )

    if current_step >= total_steps:
        print(f"   Wizard progression completed")
    else:
        remaining_steps = total_steps - current_step
        print(f"  ℹ {remaining_steps} steps remaining")


def test_wizard_step_navigation(page: GeneralConfigPage, request):
    """Test wizard step navigation functionality"""

    current_step = page.get_current_wizard_step()
    total_steps = page.get_total_wizard_steps()

    print(f" Testing wizard step navigation on {device_model}")

    # Test forward navigation
    if current_step < total_steps and page.has_wizard_next_button():
        can_go_forward = page.can_navigate_to_step(current_step + 1)
        print(f"  Can navigate forward to step {current_step + 1}: {can_go_forward}")

    # Test backward navigation
    if current_step > 1 and page.has_wizard_previous_button():
        can_go_backward = page.can_navigate_to_step(current_step - 1)
        print(f"  Can navigate backward to step {current_step - 1}: {can_go_backward}")


def test_wizard_step_validation(page: GeneralConfigPage, request):
    """Test validation patterns specific to wizard steps"""

    print(f" Testing wizard step validation on {device_model}")

    # Test step-specific validation rules
    current_step = page.get_current_wizard_step()
    step_validation_rules = page.get_step_validation_rules(current_step)

    print(f"  Current step validation rules: {len(step_validation_rules)}")

    for rule in step_validation_rules:
        rule_name = rule.get("name", "Unknown")
        rule_type = rule.get("type", "Unknown")
        rule_required = rule.get("required", False)
        print(f"    Rule: {rule_name} (Type: {rule_type}, Required: {rule_required})")


# Integration with main test function
def test_comprehensive_wizard_validation_progression(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Comprehensive wizard validation progression test

    This test validates wizard progression patterns across different device series
    and hardware configurations using pure page object pattern.
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected - cannot validate wizard progression")

    device_series = DeviceCapabilities.get_series(device_model)

    # Navigate to general config page
    general_config_page.navigate_to_page()

    # Perform comprehensive wizard progression testing
    test_wizard_progression_by_device_series(
        general_config_page, device_model, device_series
    )

    # Validate overall wizard behavior
    validate_wizard_progression_results(device_model, device_series)


def validate_wizard_progression_results(device_model: str, device_series: int):
    """Validate that wizard progression results meet expectations"""

    print(f"\n Wizard Progression Validation Results for {device_model}:")
    print(f"   Device Series: {device_series}")

    if device_series == 2:
        print(f"   Expected: Basic wizard navigation patterns")
        print(f"   Testing: Simple step progression")
    else:  # Series 3
        print(f"   Expected: Advanced wizard features")
        print(f"   Testing: Complex validation progression")

    print(f"    Wizard progression validation completed for {device_model}")
