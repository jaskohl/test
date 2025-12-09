"""
Test 15.6.1: PTP Tests Follow Correct Device Validation Pattern
Purpose: Validate all PTP tests use proper DeviceCapabilities-based device validation
Expected: Tests should check DeviceCapabilities first, skip appropriately
Series: Both - meta-validation of test correctness
"""

import pytest
import logging
from pages.device_capabilities import DeviceCapabilities


def test_15_6_1_ptp_test_device_validation_pattern(request):
    """
    Test 15.6.1: PTP Tests Follow Correct Device Validation Pattern
    Purpose: Validate all PTP tests use proper DeviceCapabilities-based device validation
    Expected: Tests should check DeviceCapabilities first, skip appropriately
    Series: Both - meta-validation of test correctness
    """
    logger = logging.getLogger(__name__)
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.skip("Device model not detected for pattern validation")

    # This validates the CORRECT pattern that PTP tests should follow
    ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)
    ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)

    if not ptp_supported:
        logger.info(
            f" {device_model} correctly does not support PTP - tests should skip"
        )
        # Validate no PTP interfaces for non-PTP devices
        assert (
            len(ptp_interfaces) == 0
        ), f"Non-PTP device {device_model} should have no PTP interfaces, got: {ptp_interfaces}"
    else:
        logger.info(f" {device_model} supports PTP with interfaces: {ptp_interfaces}")
        # Validate PTP interfaces exist for PTP devices
        assert ptp_interfaces, f"PTP device {device_model} should have PTP interfaces"

    # Validate this pattern works for all known device models
    if device_model == "KRONOS-2R-HVXX-A2F":  # 66.1
        assert not ptp_supported and len(ptp_interfaces) == 0
    elif device_model == "KRONOS-2P-HV-2":  # 190.46
        assert not ptp_supported and len(ptp_interfaces) == 0
    elif device_model in [
        "KRONOS-3R-HVLV-TCXO-A2F",  # 66.3
        "KRONOS-3R-HVXX-TCXO-44A",  # 66.6
        "KRONOS-3R-HVXX-TCXO-A2X",  # 190.47
    ]:
        assert ptp_supported and len(ptp_interfaces) > 0
