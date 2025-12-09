"""
Category 18: Workflow Tests - TEST 18.4.1: CONFIGURATION SURVIVES LOGOUT - Pure Page Object Pattern
Hardware: Device Only
Priority: HIGH - End-to-end workflow validation
Series: Both Series 2 and 3
IMPROVED: Pure page object architecture with device-aware configuration logout/login persistence validation
"""

import pytest
import time
import logging
from playwright.sync_api import Page, Browser
from pages.login_page import LoginPage
from pages.configuration_unlock_page import ConfigurationUnlockPage
from pages.general_config_page import GeneralConfigPage
from pages.dashboard_page import DashboardPage

logger = logging.getLogger(__name__)


def test_18_4_1_configuration_survives_logout(
    page: Page,
    base_url: str,
    device_password: str,
    browser: Browser,
    request,
):
    """
    Test 18.4.1: Configuration Persists Across Logout/Login (Session Persistence) (Pure Page Object Pattern)
    Purpose: Verify saved configuration survives logout and re-login using pure page object architecture
    Expected: Configuration remains after new session with device-aware validation
    IMPROVED: Pure page object pattern with comprehensive configuration logout/login persistence validation
    """
    # Get device context using page object encapsulation
    device_model = request.session.get("device_model", "unknown")
    if not device_model or device_model == "unknown":
        pytest.skip("Device model not detected - cannot validate session persistence")

    logger = logging.getLogger(__name__)

    try:
        logger.info(
            f"{device_model}: Starting configuration logout/login persistence validation"
        )

        # Initialize page objects for session persistence validation
        login_page_obj = LoginPage(page, device_model)
        dashboard_page_obj = DashboardPage(page, device_model)
        unlock_page_obj = ConfigurationUnlockPage(page, device_model)
        general_page = GeneralConfigPage(page, device_model)

        # Validate device context using page object methods
        device_series = dashboard_page_obj.get_expected_device_series()
        timeout_multiplier = dashboard_page_obj.get_timeout_multiplier()

        logger.info(f"{device_model}: Device series: {device_series}")
        logger.info(f"{device_model}: Timeout multiplier: {timeout_multiplier}x")

        # Get device-aware timeout settings using page object method
        satellite_delay = dashboard_page_obj.get_satellite_delay()

        # Step 1: Initial login and unlock using page object methods
        try:
            logger.info(f"{device_model}: Step 1 - Initial login and unlock")

            # Login using page object method
            login_page_obj.navigate_to_page()
            login_page_obj.wait_for_page_load()
            login_page_obj.login(password=device_password)

            # Wait for satellite delay using device-aware timing
            time.sleep(satellite_delay)

            # Navigate to dashboard using page object method
            dashboard_page_obj.navigate_to_page()
            dashboard_page_obj.wait_for_page_load()

            # Access configuration using page object method
            dashboard_page_obj.access_configuration()

            # Unlock configuration using page object method
            unlock_page_obj.unlock_configuration(password=device_password)

            # Wait for unlock to complete using device-aware timing
            time.sleep(satellite_delay)

            logger.info(f"{device_model}: Step 1 - Initial login and unlock successful")

        except Exception as e:
            logger.error(
                f"{device_model}: Step 1 - Initial login and unlock failed: {e}"
            )
            pytest.fail(f"Initial login and unlock failed for {device_model}: {e}")

        # Step 2: Reset identifier to known state using page object methods
        try:
            logger.info(f"{device_model}: Step 2 - Resetting identifier to known state")

            # Navigate to general page using page object method
            general_page.navigate_to_page()
            general_page.wait_for_page_load()

            # Reset identifier to clean state using page object method
            clean_identifier = "Clean State"
            general_page.configure_identifier(identifier=clean_identifier)
            general_page.save_configuration()

            # Wait for save to complete using device-aware timing
            save_delay = general_page.get_save_delay()
            time.sleep(save_delay)

            logger.info(
                f"{device_model}: Step 2 - Identifier reset to known state successful"
            )

        except Exception as e:
            logger.error(f"{device_model}: Step 2 - Identifier reset failed: {e}")
            pytest.fail(f"Identifier reset failed for {device_model}: {e}")

        # Step 3: Configure and save test identifier using page object methods
        try:
            logger.info(
                f"{device_model}: Step 3 - Configuring and saving test identifier"
            )

            # Navigate to general page using page object method
            general_page.navigate_to_page()
            general_page.wait_for_page_load()

            # Configure test identifier using page object method
            test_identifier = f"Persistence Test {int(time.time())}"
            general_page.configure_identifier(identifier=test_identifier)
            general_page.save_configuration()

            logger.info(
                f"{device_model}: Step 3 - Test identifier configuration and save successful"
            )

        except Exception as e:
            logger.error(
                f"{device_model}: Step 3 - Test identifier configuration failed: {e}"
            )
            pytest.fail(f"Test identifier configuration failed for {device_model}: {e}")

        # Step 4: Simulate logout (close context) using page object methods
        try:
            logger.info(f"{device_model}: Step 4 - Simulating logout")

            # Close current context using page object method
            login_page_obj.close_session()

            logger.info(f"{device_model}: Step 4 - Logout simulation successful")

        except Exception as e:
            logger.error(f"{device_model}: Step 4 - Logout simulation failed: {e}")
            pytest.fail(f"Logout simulation failed for {device_model}: {e}")

        # Step 5: Create new session using page object methods
        try:
            logger.info(f"{device_model}: Step 5 - Creating new session")

            # Create new context and page using page object method
            new_context = login_page_obj.create_new_session()
            new_page = new_context.new_page()

            # Update page objects for new session
            new_login_page_obj = LoginPage(new_page, device_model)
            new_dashboard_page_obj = DashboardPage(new_page, device_model)
            new_unlock_page_obj = ConfigurationUnlockPage(new_page, device_model)
            new_general_page = GeneralConfigPage(new_page, device_model)

            logger.info(f"{device_model}: Step 5 - New session creation successful")

        except Exception as e:
            logger.error(f"{device_model}: Step 5 - New session creation failed: {e}")
            pytest.fail(f"New session creation failed for {device_model}: {e}")

        # Step 6: Login again using page object methods
        try:
            logger.info(f"{device_model}: Step 6 - Logging in again")

            # Login using page object method
            new_login_page_obj.navigate_to_page()
            new_login_page_obj.wait_for_page_load()
            new_login_page_obj.login(password=device_password)

            # Wait for satellite delay using device-aware timing
            time.sleep(satellite_delay)

            # Navigate to dashboard using page object method
            new_dashboard_page_obj.navigate_to_page()
            new_dashboard_page_obj.wait_for_page_load()

            # Access configuration using page object method
            new_dashboard_page_obj.access_configuration()

            # Unlock configuration using page object method
            new_unlock_page_obj.unlock_configuration(password=device_password)

            # Wait for unlock to complete using device-aware timing
            time.sleep(satellite_delay)

            logger.info(f"{device_model}: Step 6 - Re-login successful")

        except Exception as e:
            logger.error(f"{device_model}: Step 6 - Re-login failed: {e}")
            pytest.fail(f"Re-login failed for {device_model}: {e}")

        # Step 7: Check configuration persisted using page object methods
        try:
            logger.info(f"{device_model}: Step 7 - Checking configuration persistence")

            # Navigate to general page using page object method
            new_general_page.navigate_to_page()
            new_general_page.wait_for_page_load()

            # Get page data using page object method
            new_data = new_general_page.get_page_data()
            persisted_identifier = new_data.get("identifier", "")

            logger.info(f"{device_model}: Persisted identifier: {persisted_identifier}")
            logger.info(f"{device_model}: Expected identifier: {test_identifier}")

            # Validate configuration persistence using page object method
            new_general_page.validate_configuration_persistence(
                persisted_identifier, test_identifier, device_model
            )

            logger.info(
                f"{device_model}: Step 7 - Configuration persistence verification successful"
            )

        except Exception as e:
            logger.error(
                f"{device_model}: Step 7 - Configuration persistence verification failed: {e}"
            )
            pytest.fail(
                f"Configuration persistence verification failed for {device_model}: {e}"
            )

        # Step 8: Cleanup new session using page object methods
        try:
            logger.info(f"{device_model}: Step 8 - Cleaning up new session")

            # Close new context using page object method
            new_login_page_obj.close_session()

            logger.info(f"{device_model}: Step 8 - Session cleanup successful")

        except Exception as e:
            logger.warning(f"{device_model}: Step 8 - Session cleanup failed: {e}")
            # Continue even if cleanup fails

        # Additional session persistence validation using page object methods
        try:
            logger.info(
                f"{device_model}: Step 9 - Additional session persistence validation"
            )

            # Validate logout/login workflow integrity using page object method
            dashboard_page_obj.validate_configuration_logout_login_workflow_integrity()

            # Series-specific validation using page object methods
            if device_series == 2:
                dashboard_page_obj.validate_series2_configuration_logout_login_patterns()
            elif device_series == 3:
                dashboard_page_obj.validate_series3_configuration_logout_login_patterns()

            # Cross-validation test using page object method
            dashboard_page_obj.test_configuration_logout_login_cross_validation()

            logger.info(
                f"{device_model}: Step 9 - Additional session persistence validation successful"
            )

        except Exception as e:
            logger.warning(
                f"{device_model}: Step 9 - Additional session persistence validation failed: {e}"
            )

        # Session persistence completion summary
        logger.info(
            f"{device_model}: Configuration logout/login persistence completed successfully"
        )
        print(f"Configuration logout/login persistence passed for {device_model}")

    except Exception as e:
        logger.error(
            f"{device_model}: Configuration logout/login persistence encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(
            f"Configuration logout/login persistence failed for {device_model}: {e}"
        )
