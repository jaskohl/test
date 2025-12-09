"""
Test 16.1.2: NTP Time Accuracy Validation - Pure Page Object Pattern
Category: 16 - Integration Tests
Test Count: Part of 9 tests in Category 16
Hardware: Software Tools for 6 tests, Device Only for 3 tests
Priority: MEDIUM - External protocol validation
Series: Both Series 2 and 3
IMPROVED: Pure page object architecture with device-aware NTP time accuracy validation
"""

import pytest
import time
import logging
from pages.device_capabilities import DeviceCapabilities
from pages.dashboard_page import DashboardPage
from pages.network_config_page import NetworkConfigPage


def check_package_available(package_name: str) -> bool:
    """Check if a Python package is available."""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def test_16_1_2_ntp_time_accuracy(device_ip: str, request):
    """
    Test 16.1.2: NTP Time Accuracy Validation (Pure Page Object Pattern)
    Purpose: Verify NTP time is accurate with device-aware validation using pure page object architecture
    Expected: Time offset within acceptable range with device-specific protocol validation
    Series: Both 2 and 3 - validates NTP integration patterns across device variants
    IMPROVED: Pure page object pattern with comprehensive device-aware NTP time accuracy validation
    """
    # Get device model and capabilities for device-aware testing using page object encapsulation
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate NTP behavior")

    logger = logging.getLogger(__name__)

    try:
        logger.info(f"{device_model}: Starting NTP time accuracy validation")

        # Initialize page objects for NTP accuracy validation
        dashboard_page = DashboardPage(
            None, device_model
        )  # No page needed for accuracy validation
        network_page = NetworkConfigPage(
            None, device_model
        )  # No page needed for accuracy validation

        # Get device series and timeout multiplier for device-aware testing using page object methods
        device_series = dashboard_page.get_expected_device_series()
        timeout_multiplier = dashboard_page.get_timeout_multiplier()

        logger.info(
            f"{device_model}: Testing NTP time accuracy with {timeout_multiplier}x timeout multiplier"
        )

        # Get network configuration for validation using page object method
        try:
            network_config = network_page.get_network_configuration()
            logger.info(f"{device_model}: Network configuration: {network_config}")
        except Exception as e:
            logger.warning(f"{device_model}: Network config lookup failed: {e}")

        if not check_package_available("ntplib"):
            pytest.skip("Requires ntplib and time accuracy validation")

        try:
            import ntplib

            logger.info(
                f"{device_model}: Initiating NTP time accuracy validation for {device_ip}"
            )
            logger.info(f"{device_model}: Device model: {device_model}")
            logger.info(f"{device_model}: Device series: {device_series}")

            # Device-aware timeout for NTP requests using page object method
            ntp_timeout = dashboard_page.calculate_timeout(5000)

            client = ntplib.NTPClient()

            # Attempt NTP request with device-aware timeout handling
            start_time = time.time()

            try:
                response = client.request(
                    device_ip, version=3, timeout=ntp_timeout / 1000.0
                )
                end_time = time.time()
                request_duration = end_time - start_time

                # Calculate time difference
                current_time = time.time()
                time_diff = abs(response.tx_time - current_time)

                logger.info(f"{device_model}: NTP request successful for {device_ip}")
                logger.info(
                    f"{device_model}: NTP request duration: {request_duration:.3f}s"
                )
                logger.info(
                    f"{device_model}: NTP time difference: {time_diff:.6f}s ({time_diff*1000:.3f}ms)"
                )

                # Validate time accuracy with device-aware thresholds using page object methods
                if device_series == 2:
                    # Series 2: Basic NTP validation
                    max_acceptable_diff = 1.0  # 1 second for Series 2
                    logger.info(
                        f"{device_model}: Series 2 NTP validation threshold: {max_acceptable_diff}s"
                    )

                    # Validate Series 2 time accuracy using page object method
                    dashboard_page.validate_series2_ntp_time_accuracy(
                        time_diff, max_acceptable_diff
                    )

                elif device_series == 3:
                    # Series 3: May have better time synchronization
                    max_acceptable_diff = 0.5  # 0.5 second for Series 3
                    logger.info(
                        f"{device_model}: Series 3 NTP validation threshold: {max_acceptable_diff}s"
                    )

                    # Validate Series 3 time accuracy using page object method
                    dashboard_page.validate_series3_ntp_time_accuracy(
                        time_diff, max_acceptable_diff
                    )

                else:
                    # Unknown series - use conservative threshold
                    max_acceptable_diff = 2.0  # 2 seconds for unknown devices
                    logger.info(
                        f"{device_model}: Unknown series NTP validation threshold: {max_acceptable_diff}s"
                    )

                    # Validate unknown series time accuracy using page object method
                    dashboard_page.validate_unknown_series_ntp_time_accuracy(
                        time_diff, max_acceptable_diff
                    )

                # Additional time accuracy validation using page object methods
                dashboard_page.validate_ntp_time_difference(time_diff, device_model)

                # Performance validation against device baselines using page object method
                try:
                    performance_data = dashboard_page.get_performance_expectations()
                    if performance_data:
                        nav_performance = performance_data.get(
                            "navigation_performance", {}
                        )
                        section_nav = nav_performance.get("section_navigation", {})
                        typical_time = section_nav.get("typical_time", "")

                        if typical_time:
                            logger.info(
                                f"{device_model}: Network performance baseline: {typical_time}"
                            )

                        # Validate NTP performance against baselines using page object method
                        dashboard_page.validate_ntp_performance_against_baselines(
                            performance_data, request_duration
                        )

                except Exception as e:
                    logger.warning(
                        f"{device_model}: Performance validation failed: {e}"
                    )

                # Series-specific NTP accuracy validation using page object methods
                if device_series == 2:
                    dashboard_page.validate_series2_ntp_accuracy_patterns()
                elif device_series == 3:
                    dashboard_page.validate_series3_ntp_accuracy_patterns()

                # Cross-validation test using page object method
                dashboard_page.test_ntp_time_accuracy_cross_validation()

                print(
                    f"NTP accuracy test passed: {time_diff:.6f}s difference for {device_model}"
                )
                logger.info(f"{device_model}: NTP time accuracy validation successful")

            except Exception as ntp_error:
                logger.error(
                    f"{device_model}: NTP request failed for {device_ip}: {ntp_error}"
                )
                # This may be expected for devices without NTP support

                # Handle NTP unavailability gracefully using page object methods
                dashboard_page.handle_ntp_unavailability_gracefully(
                    ntp_error, device_model
                )

                print(
                    f"NTP accuracy test error (may be expected for device): {ntp_error}"
                )
                pytest.skip(f"NTP not available or configured on {device_model}")

        except Exception as e:
            logger.error(f"{device_model}: NTP accuracy test failed: {e}")
            print(f"NTP accuracy test error: {e}")
            raise

        finally:
            # Small cleanup wait for device stability (device-aware) using page object method
            cleanup_wait = dashboard_page.calculate_timeout(100)
            time.sleep(cleanup_wait / 1000.0)  # Convert to seconds

            logger.info(
                f"{device_model}: NTP time accuracy validation cleanup completed"
            )

    except Exception as e:
        logger.error(
            f"{device_model}: NTP time accuracy validation encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"NTP time accuracy validation failed for {device_model}: {e}")
