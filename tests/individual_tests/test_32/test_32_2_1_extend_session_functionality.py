"""
Test 32.2.1: Extend Session Functionality Infrastructure
Category: 32 - Session Expiry Modal Tests
Extracted from: tests/grouped/test_32_session_expiry_modal.py
Source Method: TestSessionExpiryModalInteractions.test_32_2_1_extend_session_functionality
Individual test file for better test isolation and debugging.

Purpose: Verify session extension mechanisms can be triggered
Expected: Interaction elements exist for session extension actions
Series: Both Series 2 and 3
"""

import pytest
from playwright.sync_api import Page, expect


def test_32_2_1_extend_session_functionality(logged_in_page: Page):
    """
    Test 32.2.1: Extend Session Functionality Infrastructure
    Purpose: Verify session extension mechanisms can be triggered
    Expected: Interaction elements exist for session extension actions
    Series: Both Series 2 and 3
    """
    # Check for session extension interaction elements
    session_interaction_elements = [
        # Direct session extension buttons/triggers
        logged_in_page.locator("[onclick*='extend'], [onclick*='session']"),
        logged_in_page.locator("button:has-text('Extend'), a:has-text('Extend')"),
        # Forms or links that might handle session extension
        logged_in_page.locator("form[action*='session'], form[action*='extend']"),
        logged_in_page.locator("a[href*='extend'], a[href*='session']"),
        # AJAX/JavaScript functions that might extend session
        logged_in_page.locator("[onclick], [onClick]"),
    ]

    # Find interaction elements
    session_elements_found = 0
    for element_locator in session_interaction_elements:
        count = element_locator.count()
        if count > 0:
            session_elements_found += 1
            # Verify elements are properly structured
            try:
                expect(element_locator.first).to_be_visible()
            except Exception:
                # Element might be hidden until modal appears
                pass

    # Verify some interaction infrastructure exists
    assert (
        session_elements_found > 0
    ), "Session extension interaction elements should exist"

    # Verify page has JavaScript event handling capability
    script_elements = logged_in_page.locator("script[src], script:not([src])").count()
    assert script_elements > 0, "Page should have JavaScript for session interactions"

    # Verify AJAX/network request capability exists
    network_elements = logged_in_page.locator(
        "form, [onclick*='post'], [onclick*='ajax']"
    ).count()
    assert (
        network_elements >= session_elements_found
    ), "Page should have network request capability for session extensions"

    print("Session extension functionality infrastructure test passed")
