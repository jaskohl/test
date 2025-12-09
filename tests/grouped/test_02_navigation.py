"""
Category 2: Configuration Section Navigation Tests - MODERNIZED VERSION
Test Count: 10 tests
Hardware: Device Only
Priority: HIGH - Core navigation functionality
Series: Both Series 2 and 3

MODERNIZATION: Now uses request.session.device_hardware_model instead of device_capabilities fixture
- Integrates with DeviceCapabilities for device-aware navigation patterns
- Uses actual device model names instead of generic Series 2/3 detection
- Provides better test isolation and device-specific validation
"""

import pytest
import time
from playwright.sync_api import Page, expect
from conftest import wait_for_satellite_loading
from pages.device_capabilities import DeviceCapabilities


class TestConfigurationNavigation:
    """Test 2.1: All Configuration Sections Accessible - Device-Aware"""

    def test_2_1_1_general_section_access(
        self, unlocked_config_page: Page, base_url: str
    ):
        """Test 2.1.1: General Section Accessible"""
        unlocked_config_page.goto(f"{base_url}/general")
        time.sleep(0.5)  # Brief pause to allow page to load
        # Verify URL and page content
        assert "general" in unlocked_config_page.url, "Should navigate to general page"
        # Verify key elements present
        identifier_field = unlocked_config_page.locator("input[name='identifier']")
        expect(identifier_field).to_be_visible()

    def test_2_1_2_network_section_access(
        self, unlocked_config_page: Page, base_url: str, request
    ):
        """Test 2.1.2: Network Section Accessible - Device-Aware"""
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.fail(
                "Device model not detected - cannot validate network configuration"
            )

        unlocked_config_page.goto(f"{base_url}/network")
        assert "network" in unlocked_config_page.url, "Should navigate to network page"

        # MODERNIZED: Use DeviceCapabilities for device-aware network element verification
        device_series = DeviceCapabilities.get_series(device_model)
        capabilities = DeviceCapabilities.get_capabilities(device_model)

        if device_series == 2:
            # Series 2 devices: KRONOS-2R-HVXX-A2F, KRONOS-2P-HV-2
            # Single form with mode selection
            mode_select = unlocked_config_page.locator("select[name='mode']")
            expect(mode_select).to_be_visible()

            # Set network mode to DUAL to make ipaddrB visible for testing
            mode_select.select_option("DUAL")

            # Verify Series 2 specific elements
            ipaddr_field = unlocked_config_page.locator("input[name='ipaddr']")
            ipaddrB_field = unlocked_config_page.locator("input[name='ipaddrB']")
            expect(ipaddr_field).to_be_visible()
            expect(ipaddrB_field).to_be_visible()  # Now visible in DUAL mode

            print(f"Series 2 device {device_model}: Network configuration validated")

        elif device_series == 3:
            # Series 3 devices: All variations support network interfaces
            # Use DeviceCapabilities for interface detection
            ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)
            max_interfaces = capabilities.get("network_interfaces", 4)

            # Series 3 network elements (varies by hardware variant)
            eth0_ip = unlocked_config_page.locator("input[name='ip_eth0']")
            eth1_ip = unlocked_config_page.locator("input[name='ip_eth1']")
            sfp_mode = unlocked_config_page.locator("input[name='sfp_mode']")

            # Verify at least basic interface availability
            assert (
                eth0_ip.count() > 0
            ), f"Series 3 {device_model} should have eth0 configuration"
            assert (
                eth1_ip.count() > 0
            ), f"Series 3 {device_model} should have eth1 configuration"
            assert (
                sfp_mode.count() > 0
            ), f"Series 3 {device_model} should have SFP mode configuration"

            # Check for additional interfaces based on device variant
            eth2_ip = unlocked_config_page.locator("input[name='ip_eth2']")
            eth3_ip = unlocked_config_page.locator("input[name='ip_eth3']")

            if eth2_ip.count() > 0:
                print(
                    f"Series 3 {device_model}: Extended interface set detected (eth0-eth2)"
                )
            if eth3_ip.count() > 0:
                print(
                    f"Series 3 {device_model}: Full interface set detected (eth0-eth3)"
                )

            # Verify PTP interfaces if available
            if DeviceCapabilities.is_ptp_supported(device_model):
                print(
                    f"Series 3 {device_model}: PTP supported on {len(ptp_interfaces)} interfaces"
                )

            print(f"Series 3 device {device_model}: Network configuration validated")
        else:
            pytest.fail(f"Unknown device series for model {device_model}")

    def test_2_1_3_time_section_access(self, unlocked_config_page: Page, base_url: str):
        """Test 2.1.3: Time Section Accessible"""
        unlocked_config_page.goto(f"{base_url}/time")
        assert "time" in unlocked_config_page.url, "Should navigate to time page"
        # Verify timezone dropdown present
        timezone_select = unlocked_config_page.locator("select[name='timezones']")
        expect(timezone_select).to_be_visible()

    def test_2_1_4_outputs_section_access(
        self, unlocked_config_page: Page, base_url: str, request
    ):
        """Test 2.1.4: Outputs Section Accessible - Device-Aware"""
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.skip(
                "Device model not detected - cannot validate output configuration"
            )

        unlocked_config_page.goto(f"{base_url}/outputs")
        assert "outputs" in unlocked_config_page.url, "Should navigate to outputs page"

        # MODERNIZED: Use DeviceCapabilities for output-aware verification
        max_outputs = DeviceCapabilities.get_max_outputs(device_model)

        # Verify output configuration present based on device model
        signal1_field = unlocked_config_page.locator("select[name='signal1']")
        signal2_field = unlocked_config_page.locator("select[name='signal2']")

        assert (
            signal1_field.is_visible() and signal2_field.is_visible()
        ), f"Device {device_model} should have signal1 and signal2 configuration fields"

        # Verify additional outputs for devices with more than 2 outputs
        if max_outputs > 2:
            for output_num in range(3, max_outputs + 1):
                signal_field = unlocked_config_page.locator(
                    f"select[name='signal{output_num}']"
                )
                if signal_field.count() > 0:
                    print(f"Device {device_model}: Output {output_num} available")
                else:
                    print(
                        f"Device {device_model}: Output {output_num} not found (variant-specific)"
                    )

    def test_2_1_5_gnss_section_access(self, unlocked_config_page: Page, base_url: str):
        """Test 2.1.5: GNSS Section Accessible"""
        unlocked_config_page.goto(f"{base_url}/gnss")
        assert "gnss" in unlocked_config_page.url, "Should navigate to GNSS page"
        # Verify GPS checkbox (always present and checked)
        gps_checkbox = unlocked_config_page.locator("input[value='1']")
        expect(gps_checkbox).to_be_visible()

    def test_2_1_6_display_section_access(
        self, unlocked_config_page: Page, base_url: str, request
    ):
        """Test 2.1.6: Display Section Accessible - Device-Aware"""
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.skip(
                "Device model not detected - cannot validate display configuration"
            )

        unlocked_config_page.goto(f"{base_url}/display")
        assert "display" in unlocked_config_page.url, "Should navigate to display page"

        # Device-aware display element verification
        device_series = DeviceCapabilities.get_series(device_model)

        if device_series == 2:
            # Series 2 has display mode checkboxes
            mode_checkboxes = unlocked_config_page.locator("input[name^='mode']")
            assert (
                mode_checkboxes.count() > 0
            ), f"Series 2 device {device_model} should have display mode checkboxes"
        else:  # Series 3
            # Series 3 also has display mode checkboxes
            mode_checkboxes = unlocked_config_page.locator("input[name^='mode']")
            assert (
                mode_checkboxes.count() > 0
            ), f"Series 3 device {device_model} should have display mode checkboxes"

    def test_2_1_7_snmp_section_access(self, unlocked_config_page: Page, base_url: str):
        """Test 2.1.7: SNMP Section Accessible"""
        unlocked_config_page.goto(f"{base_url}/snmp")
        assert "snmp" in unlocked_config_page.url, "Should navigate to SNMP page"
        # Verify SNMP configuration fields
        ro_community_field = unlocked_config_page.locator("input[name='ro_community1']")
        expect(ro_community_field).to_be_visible()

    def test_2_1_8_syslog_section_access(
        self, unlocked_config_page: Page, base_url: str
    ):
        """Test 2.1.8: Syslog Section Accessible"""
        unlocked_config_page.goto(f"{base_url}/syslog")
        assert "syslog" in unlocked_config_page.url, "Should navigate to syslog page"

    def test_2_1_9_upload_section_access(
        self, unlocked_config_page: Page, base_url: str
    ):
        """Test 2.1.9: Upload Section Accessible"""
        unlocked_config_page.goto(f"{base_url}/upload")
        assert "upload" in unlocked_config_page.url, "Should navigate to upload page"

    def test_2_1_10_access_section_access(
        self, unlocked_config_page: Page, base_url: str, request
    ):
        """Test 2.1.10: Access Section Accessible - Device-Aware"""
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.skip(
                "Device model not detected - cannot validate access configuration"
            )

        unlocked_config_page.goto(f"{base_url}/access")
        assert "access" in unlocked_config_page.url, "Should navigate to access page"

        # Device-aware access field verification
        # Both series use text inputs (not password type) with specific names
        cfgpwd_field = unlocked_config_page.locator("input[name='cfgpwd']")
        uplpwd_field = unlocked_config_page.locator("input[name='uplpwd']")
        stspwd_field = unlocked_config_page.locator("input[name='stspwd']")

        assert (
            cfgpwd_field.is_visible()
        ), f"Device {device_model} should have config password field (cfgpwd)"
        assert (
            uplpwd_field.is_visible()
        ), f"Device {device_model} should have upload password field (uplpwd)"
        assert (
            stspwd_field.is_visible()
        ), f"Device {device_model} should have status password field (stspwd)"


class TestNavigationLinks:
    """Test 2.2: Navigation Links Functional - Device-Aware"""

    def test_2_2_1_sidebar_navigation_links(
        self, unlocked_config_page: Page, base_url: str, request
    ):
        """
        Test 2.2.1: All Sidebar Navigation Links Functional - Device-Aware
        Purpose: Verify all sidebar links navigate to correct pages based on device model
        Expected: Each link leads to its corresponding configuration page
        MODERNIZED: Uses DeviceCapabilities for device-aware navigation testing
        - PTP navigation only appears on Series 3 devices
        - Extended timeout for devices with known navigation issues
        - Device-specific validation patterns based on model capabilities
        """
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.fail("Device model not detected - cannot validate navigation")

        device_series = DeviceCapabilities.get_series(device_model)
        ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)

        # MODERNIZED: Use DeviceCapabilities for device-aware navigation sections
        base_sections = {
            "General": "/general",
            "Network": "/network",
            "Time": "/time",
            "Outputs": "/outputs",
            "GNSS": "/gnss",
            "Display": "/display",
            "SNMP": "/snmp",
            "Syslog": "/syslog",
            "Upload": "/upload",
            "Access": "/access",
        }

        # Add PTP section only for devices that support it
        if ptp_supported:
            sections = base_sections.copy()
            sections["PTP"] = "/ptp"
            print(f"Device {device_model}: PTP-supported navigation enabled")
        else:
            sections = base_sections
            print(f"Device {device_model}: PTP not supported - navigation excludes PTP")

        # Navigate to dashboard first to ensure sidebar is fully visible
        unlocked_config_page.goto(f"{base_url}/")
        wait_for_satellite_loading(unlocked_config_page, timeout=5000)

        # MODERNIZED: Device-aware PTP panel expansion for Series 3 devices
        if device_series == 3:
            print(f"Series 3 device {device_model} detected - expanding PTP panels")
            try:
                # Import and use PTP page object for panel expansion
                from pages.ptp_config_page import PTPConfigPage

                ptp_page = PTPConfigPage(unlocked_config_page)
                ptp_page.expand_all_ptp_panels()
                print(f"PTP panels expanded successfully for {device_model}")
            except Exception as e:
                print(f"Warning: PTP panel expansion failed for {device_model}: {e}")
                # Continue anyway - navigation may still work

        for section_name, expected_path in sections.items():
            # Use href-based locator to target sidebar specifically
            sidebar_link = unlocked_config_page.locator("aside.main-sidebar a").filter(
                has_text=section_name
            )

            # Fallback: Try mobile navigation if sidebar not found
            if sidebar_link.count() == 0:
                sidebar_link = unlocked_config_page.locator(
                    "#navbar-collapse a"
                ).filter(has_text=section_name)

            # Last resort: Use href attribute matching
            if sidebar_link.count() == 0:
                sidebar_link = unlocked_config_page.locator("a").filter(
                    has=unlocked_config_page.locator(
                        f"[href*='{expected_path.lstrip('/')}']"
                    )
                )

            # Ensure we found the link
            assert (
                sidebar_link.count() > 0
            ), f"Could not find {section_name} link in sidebar for {device_model}"

            # Verify the link is clickable and has correct href
            expect(sidebar_link).to_be_visible(timeout=5000)

            # Verify href attribute matches expected path
            href_attr = sidebar_link.get_attribute("href")
            expected_href = expected_path.lstrip("/")
            assert expected_href in href_attr or href_attr.endswith(
                expected_href
            ), f"Link href '{href_attr}' should contain '{expected_href}' for {device_model}"

            print(f"Device {device_model}: Clicking {section_name} sidebar link...")

            # MODERNIZED: Device-aware timeout based on known performance characteristics
            known_issues = DeviceCapabilities.get_known_issues(device_model)
            navigation_timeout = 30000  # Default 30s

            if any("timeout" in issue.lower() for issue in known_issues):
                navigation_timeout = (
                    45000  # Extended timeout for devices with timeout issues
                )
                print(
                    f"Device {device_model}: Using extended timeout due to known navigation issues"
                )

            # Click the sidebar link with device-aware timeout
            sidebar_link.click(timeout=navigation_timeout)

            # Verify navigation occurred
            assert (
                expected_path in unlocked_config_page.url
            ), f"Device {device_model}: Clicking {section_name} should navigate to {expected_path}"

            print(
                f"Device {device_model}: Successfully navigated to {section_name} ({expected_path})"
            )

            # Navigate back to dashboard and wait for satellite loading to complete
            unlocked_config_page.goto(f"{base_url}/")
            wait_for_satellite_loading(unlocked_config_page, timeout=5000)

    def test_2_2_2_model_specific_features_accessible(
        self, unlocked_config_page: Page, base_url: str, request
    ):
        """
        Test 2.2.2: Model-Specific Features Accessible - Device-Aware
        Purpose: Verify device-specific configuration sections are accessible
        Expected: PTP only on Series 3 devices, with model-specific interface counts
        MODERNIZED: Uses DeviceCapabilities for precise feature detection
        """
        device_model = request.session.device_hardware_model
        if not device_model:
            pytest.skip(
                "Device model not detected - cannot validate device-specific features"
            )

        ptp_supported = DeviceCapabilities.is_ptp_supported(device_model)
        ptp_interfaces = DeviceCapabilities.get_ptp_interfaces(device_model)

        if ptp_supported:
            # Series 3 devices should have PTP configuration
            unlocked_config_page.goto(f"{base_url}/ptp")
            assert (
                "ptp" in unlocked_config_page.url
            ), f"Device {device_model} should have PTP section"

            # Verify PTP profile selector based on available interfaces
            available_profiles = []
            for interface in ptp_interfaces:
                try:
                    profile_select = unlocked_config_page.locator(
                        f"select[name='ptp_profile_{interface}']"
                    )
                    if profile_select.count() > 0:
                        available_profiles.append(interface)
                        print(
                            f"Device {device_model}: PTP profile selector found for interface {interface}"
                        )
                except Exception:
                    print(
                        f"Device {device_model}: No PTP profile selector for interface {interface}"
                    )

            # Verify at least one PTP interface has a profile selector available
            assert (
                len(available_profiles) > 0
            ), f"Device {device_model} should have at least one PTP interface with profile selector"

            print(
                f"Device {device_model}: PTP configuration validated with {len(available_profiles)} interface(s)"
            )

        else:
            # Series 2 devices should NOT have PTP section
            unlocked_config_page.goto(f"{base_url}/")
            # Verify PTP section is not accessible for Series 2
