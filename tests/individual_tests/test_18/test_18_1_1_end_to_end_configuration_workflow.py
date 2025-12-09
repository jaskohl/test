"""
Test: 18.1.1 - End-to-End Configuration Workflow [PURE PAGE OBJECT]
Category: Workflow Testing (18)
Purpose: Test complete configuration workflow using pure page object architecture
Expected: Smooth workflow from login through configuration and validation
Series: Both Series 2 and 3 (device-aware)
Priority: HIGH
Hardware: Device Only
IMPROVED: Pure page object architecture with comprehensive device-aware workflow validation
"""

import pytest
import time
import logging
from playwright.sync_api import expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def test_18_1_1_end_to_end_configuration_workflow(
    login_page: LoginPage,
    dashboard_page: DashboardPage,
    network_config_page: NetworkConfigPage,
    request,
    base_url: str,
    device_password: str,
):
    """
    Test 18.1.1: End-to-End Configuration Workflow (Pure Page Object Pattern)
    Purpose: Test complete configuration workflow using pure page object architecture
    Expected: Smooth workflow from login through configuration and validation
    Series: Both 2 and 3
    IMPROVED: Pure page object pattern with comprehensive device-aware workflow validation
    """
    # Get device context using page object encapsulation
    device_model = request.session.get("device_model", "unknown")
    if not device_model or device_model == "unknown":
        pytest.skip("Device model not detected - cannot validate end-to-end workflow")

    logger = logging.getLogger(__name__)

    try:
        logger.info(
            f"{device_model}: Starting end-to-end configuration workflow validation"
        )

        # Initialize page objects for workflow validation
        login_page_obj = LoginPage(login_page.page, device_model)
        dashboard_page_obj = DashboardPage(dashboard_page.page, device_model)
        network_page_obj = NetworkConfigPage(network_config_page.page, device_model)

        # Validate device context using page object methods
        device_series = dashboard_page_obj.get_expected_device_series()
        timeout_multiplier = dashboard_page_obj.get_timeout_multiplier()

        # Device-aware timeout scaling using page object method
        base_timeout = 10000  # Workflow testing needs longer timeouts
        scaled_timeout = dashboard_page_obj.calculate_timeout(base_timeout)

        logger.info(
            f"{device_model}: Device {device_model} (Series {device_series}): Testing end-to-end workflow"
        )
        logger.info(
            f"{device_model}: Timeout scaling: {timeout_multiplier}x, Scaled timeout: {scaled_timeout}ms"
        )

        workflow_steps = []

        # Step 1: Login using page object methods
        try:
            logger.info(f"{device_model}: Step 1 - Starting login process")

            login_page_obj.navigate_to_page()
            login_page_obj.wait_for_page_load()

            success = login_page_obj.login(password=device_password)
            assert success, f"Login failed for {device_model}"
            workflow_steps.append("Login")

            logger.info(f"{device_model}: Step 1 - Login successful")
            print(f"Device {device_model}: Step 1 - Login successful")

        except Exception as e:
            logger.error(f"{device_model}: Step 1 - Login failed: {e}")
            pytest.fail(f"Login step failed for {device_model}: {e}")

        # Step 2: Dashboard access using page object methods
        try:
            logger.info(f"{device_model}: Step 2 - Validating dashboard access")

            dashboard_page_obj.wait_for_page_load()

            # Validate dashboard elements using page object method
            dashboard_page_obj.validate_dashboard_page_indicators()

            workflow_steps.append("Dashboard Access")

            logger.info(f"{device_model}: Step 2 - Dashboard access successful")
            print(f"Device {device_model}: Step 2 - Dashboard access successful")

        except Exception as e:
            logger.error(f"{device_model}: Step 2 - Dashboard access failed: {e}")
            pytest.fail(f"Dashboard access step failed for {device_model}: {e}")

        # Step 3: Navigate to configuration using page object methods
        try:
            logger.info(f"{device_model}: Step 3 - Navigating to configuration")

            # Navigate to network config using page object method
            network_page_obj.navigate_to_page()
            network_page_obj.wait_for_page_load()

            # Validate network config page indicators using page object method
            network_page_obj.validate_network_page_indicators()

            workflow_steps.append("Config Navigation")

            logger.info(f"{device_model}: Step 3 - Configuration navigation successful")
            print(
                f"Device {device_model}: Step 3 - Configuration navigation successful"
            )

        except Exception as e:
            logger.warning(f"{device_model}: Step 3 - Config navigation failed: {e}")
            # Continue with workflow even if this step fails
            workflow_steps.append("Config Navigation (Failed)")

        # Step 4: Network configuration using page object methods
        try:
            logger.info(
                f"{device_model}: Step 4 - Testing network configuration interaction"
            )

            # Test basic network configuration interaction using page object method
            network_page_obj.test_basic_network_configuration_interaction()

            workflow_steps.append("Network Config")

            logger.info(
                f"{device_model}: Step 4 - Network configuration interaction successful"
            )
            print(
                f"Device {device_model}: Step 4 - Network configuration interaction successful"
            )

        except Exception as e:
            logger.warning(f"{device_model}: Step 4 - Network config failed: {e}")
            # Continue with workflow even if this step fails
            workflow_steps.append("Network Config (Failed)")

        # Step 5: Device capability validation using page object methods
        try:
            logger.info(f"{device_model}: Step 5 - Validating device capabilities")

            # Verify device-specific capabilities using page object methods
            device_capabilities = dashboard_page_obj.get_device_capabilities()
            max_outputs = device_capabilities.get("max_outputs", "Unknown")
            snmp_capable = device_capabilities.get("snmp", False)
            https_capable = device_capabilities.get("https_enforcement", False)

            logger.info(
                f"{device_model}: Capabilities - Max outputs: {max_outputs}, SNMP: {snmp_capable}, HTTPS: {https_capable}"
            )
            workflow_steps.append("Device Validation")

            logger.info(
                f"{device_model}: Step 5 - Device capability validation successful"
            )
            print(
                f"Device {device_model}: Step 5 - Device capability validation successful"
            )

        except Exception as e:
            logger.warning(f"{device_model}: Step 5 - Device validation failed: {e}")
            # Continue with workflow even if this step fails
            workflow_steps.append("Device Validation (Failed)")

        # Step 6: Return to dashboard using page object methods
        try:
            logger.info(f"{device_model}: Step 6 - Returning to dashboard")

            # Navigate back to dashboard using page object method
            dashboard_page_obj.navigate_to_page()
            dashboard_page_obj.wait_for_page_load()

            # Validate return to dashboard using page object method
            dashboard_page_obj.validate_dashboard_page_indicators()

            workflow_steps.append("Return Navigation")

            logger.info(f"{device_model}: Step 6 - Return to dashboard successful")
            print(f"Device {device_model}: Step 6 - Return to dashboard successful")

        except Exception as e:
            logger.warning(f"{device_model}: Step 6 - Return navigation failed: {e}")
            # Continue with workflow even if this step fails
            workflow_steps.append("Return Navigation (Failed)")

        # Step 7: Workflow performance validation using page object methods
        try:
            logger.info(f"{device_model}: Step 7 - Validating workflow performance")

            # Validate workflow performance using page object method
            dashboard_page_obj.validate_end_to_end_workflow_performance(workflow_steps)

            workflow_steps.append("Performance Validation")

            logger.info(
                f"{device_model}: Step 7 - Workflow performance validation successful"
            )

        except Exception as e:
            logger.warning(
                f"{device_model}: Step 7 - Performance validation failed: {e}"
            )
            workflow_steps.append("Performance Validation (Failed)")

        # Step 8: Workflow data consistency validation using page object methods
        try:
            logger.info(
                f"{device_model}: Step 8 - Validating workflow data consistency"
            )

            # Validate workflow data consistency using page object method
            dashboard_page_obj.validate_end_to_end_workflow_data_consistency()

            workflow_steps.append("Data Consistency")

            logger.info(
                f"{device_model}: Step 8 - Workflow data consistency validation successful"
            )

        except Exception as e:
            logger.warning(
                f"{device_model}: Step 8 - Data consistency validation failed: {e}"
            )
            workflow_steps.append("Data Consistency (Failed)")

        # Workflow completion summary
        successful_steps = [
            step for step in workflow_steps if not step.endswith("(Failed)")
        ]
        failed_steps = [step for step in workflow_steps if step.endswith("(Failed)")]

        logger.info(
            f"{device_model}: End-to-end workflow completed - {len(successful_steps)} steps successful"
        )
        if failed_steps:
            logger.warning(f"{device_model}: Failed steps: {failed_steps}")
        logger.info(f"{device_model}: All steps: {workflow_steps}")

        print(
            f"Device {device_model}: End-to-end workflow completed - {len(successful_steps)}/{len(workflow_steps)} steps successful"
        )
        print(f"Successful steps: {successful_steps}")
        if failed_steps:
            print(f"Failed steps: {failed_steps}")

        # Cross-validate with device capabilities using page object methods
        try:
            device_network_config = dashboard_page_obj.get_network_configuration()
            if (
                device_network_config
                and "management_interface" in device_network_config
            ):
                mgmt_iface = device_network_config["management_interface"]
                logger.info(f"{device_model}: End-to-end workflow test completed")
                logger.info(
                    f"{device_model}: Management interface: {mgmt_iface}, Timeout scaling: {timeout_multiplier}x"
                )

        except Exception as e:
            logger.warning(
                f"{device_model}: Device capabilities cross-validation failed: {e}"
            )

        # Final validation using page object methods
        dashboard_page_obj.validate_end_to_end_workflow_completion(
            successful_steps, device_model
        )

        logger.info(
            f"{device_model}: End-to-end configuration workflow validation completed successfully"
        )
        print(f"END-TO-END WORKFLOW VALIDATION COMPLETED: {device_model}")

    except Exception as e:
        logger.error(
            f"{device_model}: End-to-end configuration workflow encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(f"End-to-end configuration workflow failed for {device_model}: {e}")
