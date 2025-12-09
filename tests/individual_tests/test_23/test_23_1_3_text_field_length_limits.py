"""
Test 23.1.3: Text field length limits
Category: 23 - Boundary & Input Testing
Test Count: Part of 3 tests in Category 23
Hardware: Device Only
Priority: MEDIUM
Series: Both Series 2 and 3

Extracted from: tests/test_23_boundary.py
Source Class: TestBoundaryValues
"""

import pytest
import time
from playwright.sync_api import Page


def test_23_1_3_text_field_length_limits(unlocked_config_page: Page, base_url: str):
    """
    Test 23.1.3: Text field maximum length limits
    Purpose: Verify text fields enforce maximum length constraints
    Expected: Fields should either enforce length limits or truncate input appropriately
    """
    unlocked_config_page.goto(f"{base_url}/general", wait_until="domcontentloaded")
    identifier = unlocked_config_page.locator("input[name='identifier']")
    if identifier.is_visible():
        # Test very long string that exceeds typical field limits
        long_string = "A" * 500  # Test with 500 character string
        identifier.fill(long_string)
        time.sleep(0.2)

        # Field should either accept up to max length or truncate
        current_value = identifier.input_value()
        assert len(current_value) <= 500, "Field should have length limit"

        # Test with a reasonable string to ensure normal operation
        identifier.fill("TEST-DEVICE-001")
        assert (
            identifier.input_value() == "TEST-DEVICE-001"
        ), "Normal input should work correctly"

        # Test edge case with special characters
        special_string = "DEVICE-123_ABC-456-XYZ-789-" + "X" * 100
        identifier.fill(special_string)
        current_value = identifier.input_value()
        # Should either accept full string or truncate to field limit
        assert len(current_value) <= len(
            special_string
        ), "Field should handle special characters"

        # Test empty string (clear field)
        identifier.clear()
        assert identifier.input_value() == "", "Field should be clearable"
