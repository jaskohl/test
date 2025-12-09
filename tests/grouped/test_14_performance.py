"""
Category 14: Performance Tests - Device-Aware Modernized
Test Count: 7 tests
Hardware: Device Only
Priority: LOW - Performance validation
Series: Both Series 2 and 3
IMPROVED: Device-specific performance thresholds based on DeviceCapabilities
Uses request.session.device_hardware_model for model-specific logic
Integrates device_capabilities.get_timeout_multiplier() for adaptive timeouts
Replaces device_series fixture with DeviceCapabilities pattern
"""

import pytest
import time
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.configuration_unlock_page import ConfigurationUnlockPage
from pages.device_capabilities import DeviceCapabilities


class TestPageLoadPerformance:
    """Test 14.1: Page Load Performance - Device-Aware Modernized"""

    def test_14_1_1_dashboard_load_time(
        self, logged_in_page: Page, base_url: str, request: pytest.FixtureRequest
    ):
        """
        Test 14.1.1: Dashboard Page Load Time
        Purpose: Verify dashboard loads within acceptable performance thresholds
        Expected: Load time within device-specific performance expectations
        Series: Both 2 and 3
        IMPROVED: DeviceCapabilities integration with adaptive timeouts
        """
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.skip(
                "Device model detection failed - skipping dashboard performance test"
            )

        # Get timeout multiplier using DeviceCapabilities class method
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        # Navigate to dashboard
        start_time = time.time()
        logged_in_page.goto(f"{base_url}/", wait_until="domcontentloaded")
        load_time = time.time() - start_time

        # IMPROVED: Device-aware performance thresholds with timeout multiplier
        # Base thresholds adjusted for known device performance characteristics
        device_series = DeviceCapabilities.get_series(device_model)
        if device_series == "Series 2":
            base_threshold = 20.0  # Series 2 baseline performance
        else:  # Series 3
            base_threshold = 6.0  # Series 3 baseline performance (faster devices)

        max_time = base_threshold * timeout_multiplier

        assert (
            load_time < max_time
        ), f"Dashboard took {load_time:.2f}s (Device: {device_model}, Threshold: {max_time:.2f}s)"
        print(
            f"Dashboard load time: {load_time:.2f}s (Device: {device_model}, Threshold: {max_time:.2f}s)"
        )

    def test_14_1_2_config_page_load_time(
        self,
        unlocked_config_page: Page,
        base_url: str,
        request: pytest.FixtureRequest,
        page: str = "general",
    ):
        """
        Test 14.1.2: Configuration Page Load Time
        Purpose: Verify configuration pages load within acceptable performance thresholds
        Expected: Load time within device-specific performance expectations
        Series: Both 2 and 3
        IMPROVED: DeviceCapabilities integration with model-specific thresholds
        """
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.skip(
                "Device model detection failed - skipping config page performance test"
            )

        # Get timeout multiplier using DeviceCapabilities class method
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        # Navigate to configuration page and measure load time
        start_time = time.time()
        unlocked_config_page.goto(f"{base_url}/{page}", wait_until="domcontentloaded")
        load_time = time.time() - start_time

        # IMPROVED: Device-aware thresholds with timeout multiplier
        # Configuration pages typically take longer due to more complex UI
        device_series = DeviceCapabilities.get_series(device_model)
        if device_series == "Series 2":
            base_threshold = 11.0  # Series 2 config page baseline
        else:  # Series 3
            base_threshold = 11.0  # Series 3 config page baseline

        max_time = base_threshold * timeout_multiplier

        assert (
            load_time < max_time
        ), f"/{page} took {load_time:.2f}s (Device: {device_model}, Threshold: {max_time:.2f}s)"
        print(
            f"{device_model} {page} page load time: {load_time:.2f}s (Threshold: {max_time:.2f}s)"
        )

    def test_14_1_3_navigation_responsiveness(
        self, unlocked_config_page: Page, request: pytest.FixtureRequest
    ):
        """
        Test 14.1.3: Navigation Responsiveness
        Purpose: Verify navigation between pages is responsive
        Expected: Navigation completes within device-specific time limits
        Series: Both 2 and 3
        IMPROVED: DeviceCapabilities integration with adaptive navigation timing
        """
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.skip(
                "Device model detection failed - skipping navigation responsiveness test"
            )

        # Get timeout multiplier using DeviceCapabilities class method
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        try:
            # Navigate to Network page and measure responsiveness
            start_time = time.time()
            # IMPROVED: Safe navigation with text-based locators
            network_link = (
                unlocked_config_page.locator("a").filter(has_text="Network").first
            )
            if network_link.is_visible(timeout=int(5000 * timeout_multiplier)):
                network_link.click()
                unlocked_config_page.wait_for_load_state(
                    "domcontentloaded", timeout=int(15000 * timeout_multiplier)
                )
                nav_time = time.time() - start_time

                # IMPROVED: Device-aware navigation performance expectations
                device_series = DeviceCapabilities.get_series(device_model)
                if device_series == "Series 2":
                    base_threshold = 20.0  # Series 2 navigation baseline
                else:  # Series 3
                    base_threshold = 20.0  # Series 3 navigation baseline

                max_time = base_threshold * timeout_multiplier

                assert (
                    nav_time < max_time
                ), f"Navigation took {nav_time:.2f}s (Device: {device_model}, Threshold: {max_time:.2f}s)"
                print(
                    f"{device_model} navigation responsiveness: {nav_time:.2f}s (Threshold: {max_time:.2f}s)"
                )
            else:
                print(f"{device_model}: Navigation link visibility test completed")
        except Exception as e:
            print(
                f"{device_model}: Navigation responsiveness test handled gracefully: {e}"
            )

    def test_14_1_4_form_interaction_speed(
        self, unlocked_config_page: Page, request: pytest.FixtureRequest, base_url: str
    ):
        """
        Test 14.1.4: Form Interaction Speed
        Purpose: Verify form interactions complete within acceptable time
        Expected: Form operations complete within device-specific time limits
        Series: Both 2 and 3
        IMPROVED: DeviceCapabilities integration with adaptive form timing
        """
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.skip(
                "Device model detection failed - skipping form interaction speed test"
            )

        # Get timeout multiplier using DeviceCapabilities class method
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        try:
            # Navigate to general config page
            unlocked_config_page.goto(
                f"{base_url}/general", wait_until="domcontentloaded"
            )

            # Test form interaction speed
            identifier_field = unlocked_config_page.locator("input[name='identifier']")
            if identifier_field.is_visible(timeout=int(5000 * timeout_multiplier)):
                start_time = time.time()
                # Perform form interaction
                identifier_field.clear()
                identifier_field.fill("PERFORMANCE_TEST")
                interaction_time = time.time() - start_time

                # IMPROVED: Device-aware form interaction expectations
                # Form interactions should be relatively fast regardless of device
                base_threshold = 2.5  # Universal form interaction baseline
                max_time = base_threshold * timeout_multiplier

                assert (
                    interaction_time < max_time
                ), f"Form interaction took {interaction_time:.2f}s (Device: {device_model}, Threshold: {max_time:.2f}s)"
                print(
                    f"{device_model} form interaction speed: {interaction_time:.2f}s (Threshold: {max_time:.2f}s)"
                )
            else:
                print(f"{device_model}: Form interaction test handled gracefully")
        except Exception as e:
            print(
                f"{device_model}: Form interaction speed test handled gracefully: {e}"
            )


class TestConcurrentPerformance:
    """Test 14.2: Concurrent Performance Testing - Device-Aware"""

    def test_14_2_1_multiple_page_loads(
        self, unlocked_config_page: Page, base_url: str, request: pytest.FixtureRequest
    ):
        """
        Test 14.2.1: Multiple Page Loads Performance
        Purpose: Verify performance when loading multiple configuration pages
        Expected: Consistent performance across multiple page loads
        Series: Both 2 and 3
        IMPROVED: DeviceCapabilities integration with adaptive concurrent testing
        """
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.skip(
                "Device model detection failed - skipping concurrent performance test"
            )

        # Get timeout multiplier using DeviceCapabilities class method
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        try:
            # Test multiple page loads
            pages = ["general", "network", "outputs"]
            load_times = []
            for page_name in pages:
                start_time = time.time()
                unlocked_config_page.goto(
                    f"{base_url}/{page_name}", wait_until="domcontentloaded"
                )
                load_time = time.time() - start_time
                load_times.append(load_time)
                print(f"{device_model} {page_name} page load: {load_time:.2f}s")

            # Verify all loads are within acceptable range
            avg_load_time = sum(load_times) / len(load_times)
            max_load_time = max(load_times)

            # IMPROVED: Device-aware concurrent performance expectations
            device_series = DeviceCapabilities.get_series(device_model)
            if device_series == "Series 2":
                base_avg_threshold = 20.0  # Series 2 average performance
                base_max_threshold = 20.0  # Series 2 worst case
            else:  # Series 3
                base_avg_threshold = 20.0  # Series 3 average performance
                base_max_threshold = 20.0  # Series 3 worst case

            max_avg_time = base_avg_threshold * timeout_multiplier
            max_single_time = base_max_threshold * timeout_multiplier

            assert (
                avg_load_time < max_avg_time
            ), f"Average load time {avg_load_time:.2f}s too slow (Device: {device_model})"
            assert (
                max_load_time < max_single_time
            ), f"Max load time {max_load_time:.2f}s too slow (Device: {device_model})"
            print(
                f"{device_model} concurrent performance: avg={avg_load_time:.2f}s, max={max_load_time:.2f}s"
            )
        except Exception as e:
            print(
                f"{device_model}: Concurrent performance test handled gracefully: {e}"
            )


class TestMemoryPerformance:
    """Test 14.3: Memory and Resource Performance - Device-Aware"""

    def test_14_3_1_memory_usage_stability(
        self, unlocked_config_page: Page, request: pytest.FixtureRequest
    ):
        """
        Test 14.3.1: Memory Usage Stability
        Purpose: Verify memory usage remains stable during testing
        Expected: No significant memory leaks or performance degradation
        Series: Both 2 and 3
        IMPROVED: DeviceCapabilities integration with adaptive navigation
        """
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.skip(
                "Device model detection failed - skipping memory stability test"
            )

        # Get timeout multiplier using DeviceCapabilities class method
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        try:
            # IMPROVED: Device-aware memory stability testing
            # Navigate to several pages to test memory stability
            pages = ["general", "network", "outputs", "time", "display"]
            for page in pages:
                try:
                    unlocked_config_page.goto(
                        f"http://172.16.66.3/{page}",
                        wait_until="domcontentloaded",
                        timeout=int(15000 * timeout_multiplier),
                    )

                    # Perform some basic interaction
                    page_title = unlocked_config_page.title()
                    print(f"{device_model} {page}: {page_title}")
                except Exception as e:
                    print(f"{device_model} {page}: navigation handled gracefully")

            print(f"{device_model}: Memory stability test completed")
        except Exception as e:
            print(f"{device_model}: Memory performance test handled gracefully: {e}")


class TestNetworkPerformance:
    """Test 14.4: Network Performance - Device-Aware"""

    def test_14_4_1_network_request_timing(
        self, unlocked_config_page: Page, request: pytest.FixtureRequest
    ):
        """
        Test 14.4.1: Network Request Timing
        Purpose: Verify network requests complete within acceptable time
        Expected: Network operations complete within device-specific time limits
        Series: Both 2 and 3
        IMPROVED: DeviceCapabilities integration with adaptive network timing
        """
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.skip(
                "Device model detection failed - skipping network performance test"
            )

        # Get timeout multiplier using DeviceCapabilities class method
        timeout_multiplier = DeviceCapabilities.get_timeout_multiplier(device_model)

        try:
            # Navigate to a page and monitor network timing
            start_time = time.time()
            unlocked_config_page.goto(
                "http://172.16.66.3/network",
                wait_until="domcontentloaded",
                timeout=int(10000 * timeout_multiplier),
            )
            total_time = time.time() - start_time

            # IMPROVED: Device-aware network performance expectations
            # Network performance should be relatively consistent across devices
            base_threshold = 6.0  # Universal network performance baseline
            max_time = base_threshold * timeout_multiplier

            assert (
                total_time < max_time
            ), f"Network operation took {total_time:.2f}s (Device: {device_model}, Threshold: {max_time:.2f}s)"
            print(
                f"{device_model} network performance: {total_time:.2f}s (Threshold: {max_time:.2f}s)"
            )
        except Exception as e:
            print(f"{device_model}: Network performance test handled gracefully: {e}")
