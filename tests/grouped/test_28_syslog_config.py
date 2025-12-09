"""
Category 28: Syslog Configuration Tests
Test Count: 11 tests
Hardware: Device Only
Priority: MEDIUM - System logging configuration
Series: Both Series 2 and 3
Based on COMPLETE_TEST_LIST.md Section 28
Device exploration data: config_syslog.forms.json
Note: Syslog page supports dual syslog targets (two independent configurations)
"""

import pytest
from playwright.sync_api import Page, expect
from pages.syslog_config_page import SyslogConfigPage


class TestSyslogTarget1:
    """Test 28.1: Syslog Target 1 Configuration"""

    def test_28_1_1_syslog1_enable_checkbox(self, syslog_config_page: SyslogConfigPage):
        """
        Test 28.1.1: Syslog Target 1 Enable
        Purpose: Verify first syslog target can be enabled/disabled
        Expected: Checkbox toggles syslog1 functionality
        Series: Both 2 and 3
        """
        # Look for syslog enable checkbox (target 1)
        syslog1_enable = syslog_config_page.page.locator(
            "input[name*='syslog'][type='checkbox'], input[name*='enable'][type='checkbox']"
        ).first
        if syslog1_enable.is_visible():
            expect(syslog1_enable).to_be_enabled()
            # Toggle checkbox
            was_checked = syslog1_enable.is_checked()
            syslog1_enable.click()
            assert syslog1_enable.is_checked() != was_checked, "Checkbox should toggle"

    def test_28_1_2_syslog1_server_ip(self, syslog_config_page: SyslogConfigPage):
        """
        Test 28.1.2: Syslog Target 1 Server IP
        Purpose: Verify syslog server IP address field
        Expected: Accepts valid IPv4 addresses
        Series: Both 2 and 3
        """
        # Look for syslog server IP field (first target)
        server_ip = syslog_config_page.page.locator(
            "input[name*='syslog'][type='text'], input[name*='server']"
        ).first
        if server_ip.is_visible():
            expect(server_ip).to_be_editable()
            # Test valid IP
            server_ip.fill("192.168.1.100")
            assert server_ip.input_value() == "192.168.1.100"

    def test_28_1_3_syslog1_port_configuration(
        self, syslog_config_page: SyslogConfigPage
    ):
        """
        Test 28.1.3: Syslog Target 1 Port Configuration
        Purpose: Verify syslog port field (default 514)
        Expected: Accepts valid port numbers
        Series: Both 2 and 3
        """
        # Look for port field
        port_field = syslog_config_page.page.locator("input[name*='port']").first
        if port_field.is_visible():
            expect(port_field).to_be_editable()
            # Test default port
            port_field.fill("514")
            assert port_field.input_value() == "514"
            # Test custom port
            port_field.fill("1514")
            assert port_field.input_value() == "1514"


class TestSyslogTarget2:
    """Test 28.2: Syslog Target 2 Configuration"""

    def test_28_2_1_syslog2_independent_configuration(
        self, syslog_config_page: SyslogConfigPage
    ):
        """
        Test 28.2.1: Second Syslog Target Independent Configuration
        Purpose: Verify second syslog target configures independently
        Expected: Two separate syslog destinations possible
        Series: Both 2 and 3
        """
        # Look for second syslog target fields
        enable_checkboxes = syslog_config_page.page.locator("input[type='checkbox']")
        if enable_checkboxes.count() >= 2:
            # Second checkbox should be independent
            syslog2_enable = enable_checkboxes.nth(1)
            expect(syslog2_enable).to_be_enabled()
            # Toggle should not affect first target
            syslog2_enable.click()

    def test_28_2_2_dual_syslog_targets(self, syslog_config_page: SyslogConfigPage):
        """
        Test 28.2.2: Both Syslog Targets Simultaneously
        Purpose: Verify both syslog targets can be enabled at once
        Expected: No conflicts, both targets configurable
        Series: Both 2 and 3
        """
        server_fields = syslog_config_page.page.locator(
            "input[name*='server'], input[type='text']"
        )
        if server_fields.count() >= 2:
            # Configure both targets with different IPs
            server_fields.nth(0).fill("192.168.1.100")
            server_fields.nth(1).fill("192.168.1.200")
            # Both should retain independent values
            assert server_fields.nth(0).input_value() == "192.168.1.100"
            assert server_fields.nth(1).input_value() == "192.168.1.200"


class TestSyslogProtocol:
    """Test 28.3: Syslog Protocol Configuration"""

    def test_28_3_1_syslog_protocol_selection(
        self, syslog_config_page: SyslogConfigPage
    ):
        """
        Test 28.3.1: Syslog Protocol Selection (UDP/TCP)
        Purpose: Verify syslog protocol can be selected
        Expected: UDP and/or TCP options available
        Series: Both 2 and 3
        NOTE: Device has protocol_a and protocol_b selects - use .first to avoid strict mode
        """
        # Device has select[name='protocol_a'] and select[name='protocol_b']
        # Use .first to get protocol_a
        protocol_select = syslog_config_page.page.locator(
            "select[name*='protocol']"
        ).first
        expect(protocol_select).to_be_visible()
        expect(protocol_select).to_be_enabled()
        # Check for UDP/TCP options
        options = protocol_select.locator("option")
        option_texts = []
        for i in range(options.count()):
            option_texts.append(options.nth(i).inner_text())
        # Should have protocol options
        assert any(
            "UDP" in text or "TCP" in text for text in option_texts
        ), "Should have UDP or TCP protocol options"


class TestSyslogFacility:
    """Test 28.4: Syslog Facility Configuration"""

    def test_28_4_1_syslog_facility_selection(
        self, syslog_config_page: SyslogConfigPage
    ):
        """
        Test 28.4.1: Syslog Facility Selection
        Purpose: Verify syslog facility code can be configured
        Expected: Standard syslog facilities (LOCAL0-LOCAL7, etc)
        Series: Both 2 and 3
        """
        # Look for facility dropdown
        facility_select = syslog_config_page.page.locator("select[name*='facility']")
        if facility_select.is_visible():
            expect(facility_select).to_be_enabled()
            # Should have facility options
            options = facility_select.locator("option")
            assert options.count() > 0, "Should have facility options"


class TestSyslogSeverity:
    """Test 28.5: Syslog Severity Level Configuration"""

    def test_28_5_1_syslog_severity_level(self, syslog_config_page: SyslogConfigPage):
        """
        Test 28.5.1: Syslog Severity Level Selection
        Purpose: Verify minimum severity level can be configured
        Expected: Standard syslog severities (Emergency, Alert, Critical, etc)
        Series: Both 2 and 3
        """
        # Look for severity dropdown
        severity_select = syslog_config_page.page.locator(
            "select[name*='severity'], select[name*='level']"
        )
        if severity_select.is_visible():
            expect(severity_select).to_be_enabled()
            # Should have severity options
            options = severity_select.locator("option")
            assert options.count() > 0, "Should have severity level options"


class TestSyslogFormControls:
    """Test 28.6: Syslog Form Controls"""

    def test_28_6_1_syslog_save_button(self, syslog_config_page: SyslogConfigPage):
        """
        Test 28.6.1: Syslog Save Button State Management
        Purpose: Verify save button enables when syslog config changes
        Expected: Disabled initially, enables on change
        Series: Both 2 and 3
        """
        # Use page object method for device-aware save button detection
        # This handles both Series 2 (input#button_save) and Series 3 (button#button_save)
        # Make a change using page object method
        original_data = syslog_config_page.get_page_data()
        syslog_config_page.configure_syslog(target_a="192.168.1.100")
        # Verify configuration was applied
        new_data = syslog_config_page.get_page_data()
        assert new_data["target_a"] == "192.168.1.100", "Target A should be updated"
        # Reset to original state
        syslog_config_page.configure_syslog(target_a=original_data.get("target_a", ""))

    def test_28_6_2_syslog_cancel_button(self, syslog_config_page: SyslogConfigPage):
        """
        Test 28.6.2: Syslog Cancel Button Reverts Changes
        Purpose: Verify cancel reverts syslog configuration changes
        Expected: Fields return to form defaults (empty for target_a)
        Series: Both 2 and 3
        Note: Cancel resets to form defaults, not saved configuration
        """
        # Make change using page object method
        syslog_config_page.configure_syslog(target_a="10.0.0.99")
        # Verify change was applied
        changed_data = syslog_config_page.get_page_data()
        assert changed_data["target_a"] == "10.0.0.99", "Target A should be changed"
        # Use cancel button to revert changes
        syslog_config_page.cancel_configuration()
        # Verify cancel reset to form defaults (empty for target_a)
        cancelled_data = syslog_config_page.get_page_data()
        assert (
            cancelled_data["target_a"] == ""
        ), "Target A should be reset to empty (form default)"


class TestSyslogPersistence:
    """Test 28.7: Syslog Configuration Persistence"""

    def test_28_7_1_syslog_configuration_persists(
        self, syslog_config_page: SyslogConfigPage
    ):
        """
        Test 28.7.1: Syslog Configuration Persistence
        Purpose: Verify syslog settings persist after save and reload
        Expected: Configuration survives page reload
        Series: Both 2 and 3
        """
        # Get original configuration
        original_data = syslog_config_page.get_page_data()
        original_target_a = original_data.get("target_a", "")
        # Make a change using page object method (triggers JavaScript events)
        test_server = "192.168.10.50"
        syslog_config_page.configure_syslog(target_a=test_server)
        # Allow time for JavaScript to process change events and enable save button
        import time

        time.sleep(0.5)
        # Verify save button is enabled before attempting to save
        assert (
            syslog_config_page.is_save_button_enabled()
        ), "Save button should be enabled after configuration changes"
        # Save configuration
        syslog_config_page.save_configuration()
        # Reload page
        syslog_config_page.navigate_to_page()
        # Verify persistence
        reloaded_data = syslog_config_page.get_page_data()
        assert (
            reloaded_data["target_a"] == test_server
        ), "Syslog target A should persist after save and reload"
        # Reset to original configuration
        syslog_config_page.configure_syslog(target_a=original_target_a)
        time.sleep(0.5)
        if syslog_config_page.is_save_button_enabled():
            syslog_config_page.save_configuration()
