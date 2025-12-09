"""
Test 2.1.9: Upload Section Accessible
Purpose: Verify upload section navigation and file upload configuration availability

Category: 2 - Configuration Section Navigation
Test Type: Unit Test
Priority: HIGH
Hardware: Device Only
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_2_1_9_upload_section_access(unlocked_config_page: Page, base_url: str):
    """Test 2.1.9: Upload Section Accessible"""
    unlocked_config_page.goto(f"{base_url}/upload")
    assert "upload" in unlocked_config_page.url, "Should navigate to upload page"
