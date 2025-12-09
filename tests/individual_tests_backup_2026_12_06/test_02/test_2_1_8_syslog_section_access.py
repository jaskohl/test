"""
Test 2.1.8: Syslog Section Accessible
Purpose: Verify syslog section navigation and configuration availability

Category: 2 - Configuration Section Navigation
Test Type: Unit Test
Priority: HIGH
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_2_1_8_syslog_section_access(unlocked_config_page: Page, base_url: str):
    """Test 2.1.8: Syslog Section Accessible"""
    unlocked_config_page.goto(f"{base_url}/syslog")
    assert "syslog" in unlocked_config_page.url, "Should navigate to syslog page"
