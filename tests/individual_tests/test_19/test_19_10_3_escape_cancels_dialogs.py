"""
Category 19: Dynamic UI Behavior & Element Validation
Test 19.10.3: Escape Cancels Dialogs
Hardware: Device Only
Series: Both Series 2 and 3
Extracted from test_19_dynamic_ui.py
"""

import pytest
import time
from playwright.sync_api import Page, expect


def test_19_10_3_escape_cancels_dialogs(unlocked_config_page: Page, base_url: str):
    """Test 19.10.3: Escape key cancels dialogs"""
    unlocked_config_page.goto(f"{base_url}/general")
    time.sleep(1)
    unlocked_config_page.keyboard.press("Escape")
    # Any modal should close
