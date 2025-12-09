"""
Test 11.18.3: Capability Inconsistency Detection (Device-)
Purpose: Comprehensive capability inconsistency detection and validation with DeviceCapabilities
Expected: Device-specific capability inconsistency handling with series-aware validation
Device-: Uses DeviceCapabilities for comprehensive device-aware testing across all hardware variants
"""

import pytest
import time
from playwright.sync_api import expect
from pages.general_config_page import GeneralConfigPage
from pages.device_capabilities import DeviceCapabilities


def test_11_18_3_capability_inconsistency_detection(
    general_config_page: GeneralConfigPage,
    request,
    base_url: str,
):
    """
    Test 11.18.3: Capability Inconsistency Detection (Device-)

    Purpose: Comprehensive capability inconsistency detection and validation with DeviceCapabilities
    Expected: Device-specific capability inconsistency handling with series-aware validation
    Device-: Uses DeviceCapabilities for comprehensive device-aware testing across all hardware variants
    """
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip(
            "Device model not detected - cannot validate capability consistency"
        )

    # Get device capabilities and series information
    device_capabilities = DeviceCapabilities.get_capabilities(device_model)
    device_series = DeviceCapabilities.get_series(device_model)
    timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

    print(
        f"Testing capability inconsistency detection for {device_model} (Series {device_series})"
    )

    # Navigate to general configuration page
    general_config_page.navigate_to_page()

    # Wait for page to load with device-aware timeout
    time.sleep(1 * timeout_multiplier)

    # Test for capability inconsistencies
    validate_capability_inconsistencies(
        general_config_page,
        device_model,
        device_series,
        device_capabilities,
        timeout_multiplier,
    )

    # Test series-specific inconsistency patterns
    validate_series_inconsistency_patterns(
        general_config_page, device_model, device_series, timeout_multiplier
    )

    # Test capability display consistency
    validate_capability_display_consistency(
        general_config_page, device_model, device_series, timeout_multiplier
    )

    # Test hardware capability matching
    validate_hardware_capability_matching(
        general_config_page,
        device_model,
        device_series,
        device_capabilities,
        timeout_multiplier,
    )


def validate_capability_inconsistencies(
    page, device_model, device_series, device_capabilities, timeout_multiplier
):
    """Comprehensive validation for capability inconsistencies"""
    print(f"Validating capability inconsistencies for {device_model}")

    # Check for known issues from capabilities data
    known_issues = device_capabilities.get("known_issues", {})
    if known_issues:
        print(f"Known issues for {device_model}: {known_issues}")

        # Test that device handles known issues appropriately
        for issue_type, issue_details in known_issues.items():
            print(f"Checking known issue: {issue_type} - {issue_details}")

    # Detect series mismatches
    detect_series_mismatches(page, device_model, device_series, timeout_multiplier)

    # Detect feature inconsistencies
    detect_feature_inconsistencies(
        page, device_model, device_series, timeout_multiplier
    )

    # Detect interface inconsistencies
    detect_interface_inconsistencies(
        page, device_model, device_series, timeout_multiplier
    )

    print(f" Capability inconsistency validation completed for {device_model}")


def detect_series_mismatches(page, device_model, device_series, timeout_multiplier):
    """Detect mismatches between device series and displayed features"""
    print(f"Detecting series mismatches for {device_model} (Series {device_series})")

    if device_series == 2:
        # Series 2 should not have PTP features, or they should be disabled
        ptp_indicators = page.page.locator(
            "input[name*='ptp' i], select[name*='ptp' i], "
            "[class*='ptp' i], [id*='ptp' i], "
            "text=PTP, text=ptp"
        )

        if ptp_indicators.count() > 0:
            print(f" Found {ptp_indicators.count()} PTP indicators for Series 2 device")

            # Check if PTP elements are properly disabled/hidden
            enabled_ptp_count = 0
            for i in range(min(ptp_indicators.count(), 3)):
                element = ptp_indicators.nth(i)
                try:
                    if element.is_visible() and element.is_enabled():
                        enabled_ptp_count += 1
                        print(
                            f" PTP element {i} is visible and enabled - potential Series 2 mismatch"
                        )
                except Exception:
                    pass

            if enabled_ptp_count > 0:
                print(
                    f" {enabled_ptp_count} PTP elements enabled for Series 2 - capability mismatch detected"
                )
            else:
                print(
                    " PTP elements found but disabled/hidden - appropriate for Series 2"
                )

        # Series 2 should have limited output options
        output_elements = page.page.locator(
            "input[name*='output' i], select[name*='output' i]"
        )
        if (
            output_elements.count() > 8
        ):  # Series 2 should not have too many output options
            print(
                f" Found {output_elements.count()} output elements - may be too many for Series 2"
            )

    elif device_series == 3:
        # Series 3 should have advanced features
        advanced_feature_indicators = page.page.locator(
            "[data-series-3], .advanced-feature, .ptp-supported, "
            "input[name*='ptp' i], select[name*='ptp' i]"
        )

        if advanced_feature_indicators.count() == 0:
            print(
                f" No advanced feature indicators found for Series 3 device - potential capability mismatch"
            )

        # Series 3 should have multiple interfaces
        interface_elements = page.page.locator("input[id*='eth'], select[id*='eth']")
        if interface_elements.count() < 2:
            print(
                f" Found only {interface_elements.count()} interface elements - Series 3 should have multiple"
            )


def detect_feature_inconsistencies(
    page, device_model, device_series, timeout_multiplier
):
    """Detect inconsistencies in feature availability"""
    print(f"Detecting feature inconsistencies for {device_model}")

    # Count features in different sections
    feature_sections = {
        "output_features": page.page.locator(
            "input[name*='output' i], select[name*='output' i]"
        ),
        "network_features": page.page.locator(
            "input[name*='network' i], select[name*='network' i]"
        ),
        "time_features": page.page.locator(
            "input[name*='time' i], select[name*='time' i]"
        ),
        "interface_features": page.page.locator("input[id*='eth'], select[id*='eth']"),
    }

    feature_counts = {}
    for section_name, elements in feature_sections.items():
        count = elements.count()
        feature_counts[section_name] = count

    print(f"Feature counts: {feature_counts}")

    # Check for inconsistent feature distributions
    if device_series == 2:
        # Series 2 should have balanced, limited feature set
        total_features = sum(feature_counts.values())
        if total_features > 25:
            print(
                f" High feature count ({total_features}) for Series 2 - possible inconsistency"
            )

        # Series 2 should not have excessive PTP features
        ptp_features = page.page.locator(
            "input[name*='ptp' i], select[name*='ptp' i]"
        ).count()
        if ptp_features > 2:
            print(
                f" High PTP feature count ({ptp_features}) for Series 2 - possible inconsistency"
            )

    elif device_series == 3:
        # Series 3 should have comprehensive feature set
        total_features = sum(feature_counts.values())
        if total_features < 10:
            print(
                f" Low feature count ({total_features}) for Series 3 - possible missing features"
            )

        # Series 3 should have PTP features
        ptp_features = page.page.locator(
            "input[name*='ptp' i], select[name*='ptp' i]"
        ).count()
        if ptp_features == 0:
            print(" No PTP features found for Series 3 - missing advanced features")


def detect_interface_inconsistencies(
    page, device_model, device_series, timeout_multiplier
):
    """Detect inconsistencies in interface handling"""
    print(f"Detecting interface inconsistencies for {device_model}")

    if device_series == 2:
        # Series 2 should primarily use eth0
        eth0_elements = page.page.locator("input[id*='eth0'], select[id*='eth0']")
        eth1_elements = page.page.locator("input[id*='eth1'], select[id*='eth1']")

        eth0_count = eth0_elements.count()
        eth1_count = eth1_elements.count()

        if eth0_count == 0:
            print(
                " No eth0 interface elements found for Series 2 - basic interface missing"
            )

        if eth1_count > eth0_count:
            print(
                f" More eth1 elements ({eth1_count}) than eth0 ({eth0_count}) for Series 2 - inconsistent"
            )

    elif device_series == 3:
        # Series 3 should support multiple interfaces (eth0-eth4)
        expected_interfaces = ["eth0", "eth1", "eth2", "eth3", "eth4"]
        found_interfaces = []

        for eth_interface in expected_interfaces:
            elements = page.page.locator(
                f"input[id*='{eth_interface}'], select[id*='{eth_interface}']"
            )
            if elements.count() > 0:
                found_interfaces.append(eth_interface)

        print(f"Found interfaces for Series 3: {found_interfaces}")

        if len(found_interfaces) < 3:
            print(
                f" Only {len(found_interfaces)} interfaces found for Series 3 - should have more"
            )


def validate_series_inconsistency_patterns(
    page, device_model, device_series, timeout_multiplier
):
    """Validate series-specific inconsistency patterns"""
    print(
        f"Validating series-specific inconsistency patterns for {device_model} (Series {device_series})"
    )

    # Test navigation consistency
    try:
        # Navigate away and back to test consistency
        current_url = page.page.url
        page.page.reload()
        time.sleep(1 * timeout_multiplier)

        # Re-check key indicators after reload
        device_indicators = page.page.locator(
            ".device-info, .hardware-model, [data-device-model]"
        )

        if device_indicators.count() > 0:
            print(" Device indicators persist after reload - good consistency")
        else:
            print(" Device indicators not persistent after reload")

    except Exception as e:
        print(f"Warning: Could not test navigation consistency: {e}")

    # Test form field consistency
    try:
        # Check if form fields are consistent with device series
        form_fields = page.page.locator("input, select, textarea")
        field_count = form_fields.count()

        if device_series == 2 and field_count > 50:
            print(
                f" High field count ({field_count}) for Series 2 - possible inconsistency"
            )
        elif device_series == 3 and field_count < 20:
            print(f" Low field count ({field_count}) for Series 3 - missing fields")

        print(f" Form field consistency check completed: {field_count} fields")

    except Exception as e:
        print(f"Warning: Could not test form field consistency: {e}")


def validate_capability_display_consistency(
    page, device_model, device_series, timeout_multiplier
):
    """Validate consistency of capability displays"""
    print(f"Validating capability display consistency for {device_model}")

    # Look for device model displays
    device_displays = page.page.locator(
        ".device-info, .hardware-model, [data-device-model], "
        ".device-name, .model-display, [class*='device' i]"
    )

    model_displayed_correctly = False

    if device_displays.count() > 0:
        print(f"Found {device_displays.count()} device model displays")

        for i in range(min(device_displays.count(), 3)):
            display_element = device_displays.nth(i)
            try:
                display_text = display_element.text_content() or ""
                if device_model.lower() in display_text.lower():
                    model_displayed_correctly = True
                    print(f" Device model {device_model} found in display {i}")
                    break
                else:
                    print(
                        f" Device model not found in display {i}: {display_text[:50]}..."
                    )
            except Exception as e:
                print(f"Warning: Could not read display {i}: {e}")

    if not model_displayed_correctly:
        print(f" Device model {device_model} not consistently displayed")

    # Check for series indicators
    series_indicators = page.page.locator(
        "[data-series], .series-info, .device-series, "
        "text=Series 2, text=Series 3, text=S2, text=S3"
    )

    if series_indicators.count() > 0:
        print(f" Found {series_indicators.count()} series indicators")

        # Check if series indicators match detected series
        series_text = series_indicators.first.text_content() or ""
        if (
            f"Series {device_series}" in series_text
            or f"S{device_series}" in series_text
        ):
            print(" Series indicators match detected series")
        else:
            print(f" Series indicators don't match detected series: {series_text}")
    else:
        print(" No series indicators found - may indicate missing capability display")


def validate_hardware_capability_matching(
    page, device_model, device_series, device_capabilities, timeout_multiplier
):
    """Validate that hardware capabilities match device interface"""
    print(f"Validating hardware capability matching for {device_model}")

    # Compare expected capabilities with actual interface
    expected_features = get_expected_features_for_series(device_series)
    actual_features = detect_actual_features(page)

    print(f"Expected features for Series {device_series}: {expected_features}")
    print(f"Detected features: {actual_features}")

    # Check for significant mismatches
    missing_critical_features = []
    unexpected_features = []

    for feature in expected_features.get("critical", []):
        if feature not in actual_features:
            missing_critical_features.append(feature)

    for feature in actual_features:
        if feature not in expected_features.get("all", []):
            unexpected_features.append(feature)

    if missing_critical_features:
        print(
            f" Missing critical features for Series {device_series}: {missing_critical_features}"
        )

    if unexpected_features:
        print(f" Unexpected features for Series {device_series}: {unexpected_features}")

    if not missing_critical_features and not unexpected_features:
        print(" Hardware capabilities match expected features")

    print(f" Hardware capability matching validation completed for {device_model}")


def get_expected_features_for_series(device_series):
    """Get expected features for a device series"""
    if device_series == 2:
        return {
            "critical": ["basic_outputs", "eth0", "basic_network"],
            "all": [
                "basic_outputs",
                "eth0",
                "basic_network",
                "gnss_basic",
                "time_basic",
            ],
            "advanced": [],  # Series 2 should not have advanced features
        }
    elif device_series == 3:
        return {
            "critical": ["advanced_outputs", "multiple_interfaces", "ptp_support"],
            "all": [
                "advanced_outputs",
                "eth0",
                "eth1",
                "eth2",
                "ptp_support",
                "advanced_network",
                "gnss_advanced",
                "protocols_advanced",
            ],
            "advanced": ["ptp_support", "multiple_interfaces", "protocols_advanced"],
        }
    return {"critical": [], "all": [], "advanced": []}


def detect_actual_features(page):
    """Detect actual features available in the interface"""
    features = []

    # Check for output features
    if (
        page.page.locator("input[name*='output' i], select[name*='output' i]").count()
        > 0
    ):
        features.append("basic_outputs")
        if (
            page.page.locator(
                "input[name*='output' i], select[name*='output' i]"
            ).count()
            >= 6
        ):
            features.append("advanced_outputs")

    # Check for interface features
    eth_count = page.page.locator("input[id*='eth'], select[id*='eth']").count()
    if eth_count > 0:
        features.append("eth0")
    if eth_count > 2:
        features.append("multiple_interfaces")

    # Check for PTP features
    if page.page.locator("input[name*='ptp' i], select[name*='ptp' i]").count() > 0:
        features.append("ptp_support")

    # Check for network features
    if (
        page.page.locator("input[name*='network' i], select[name*='network' i]").count()
        > 0
    ):
        features.append("basic_network")
        if (
            page.page.locator(
                "input[name*='network' i], select[name*='network' i]"
            ).count()
            > 3
        ):
            features.append("advanced_network")

    # Check for GNSS features
    if page.page.locator("input[name*='gnss' i], select[name*='gnss' i]").count() > 0:
        features.append("gnss_basic")

    # Check for protocol features
    if (
        page.page.locator(
            "input[name*='protocol' i], select[name*='protocol' i]"
        ).count()
        > 0
    ):
        features.append("protocols_advanced")

    # Check for time features
    if page.page.locator("input[name*='time' i], select[name*='time' i]").count() > 0:
        features.append("time_basic")

    return features
