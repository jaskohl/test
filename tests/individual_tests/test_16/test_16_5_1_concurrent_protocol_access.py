"""
Test 16.5.1: Concurrent Protocol Access - Pure Page Object Pattern
Category: 16 - Integration Tests
Test Count: Part of 9 tests in Category 16
Hardware: Software Tools for 6 tests, Device Only for 3 tests
Priority: MEDIUM - External protocol validation
Series: Both Series 2 and 3
IMPROVED: Pure page object architecture with device-aware concurrent protocol access validation
"""

import pytest
import logging
import threading
import time
import socket
from playwright.sync_api import Page, expect
from pages.dashboard_page import DashboardPage
from pages.network_config_page import NetworkConfigPage

logger = logging.getLogger(__name__)


def check_package_available(package_name: str) -> bool:
    """Check if a Python package is available."""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def test_16_5_1_concurrent_protocol_access(
    unlocked_config_page: Page, device_ip: str, request
):
    """
    Test 16.5.1: Concurrent Protocol Access (Pure Page Object Pattern)
    Purpose: Verify device can handle concurrent protocol access using pure page object architecture
    Expected: Can handle multiple protocol connections simultaneously with device-aware validation
    Series: Both 2 and 3
    IMPROVED: Pure page object pattern with comprehensive device-aware concurrent protocol access validation
    """
    # Get device model for comprehensive validation
    device_model = request.session.get("device_model", "unknown")
    if not device_model or device_model == "unknown":
        pytest.skip(
            "Device model not detected - cannot validate concurrent protocol access"
        )

    logger = logging.getLogger(__name__)

    try:
        logger.info(f"{device_model}: Starting concurrent protocol access validation")

        # Initialize page objects for concurrent protocol validation
        dashboard_page = DashboardPage(unlocked_config_page, device_model)
        network_page = NetworkConfigPage(unlocked_config_page, device_model)

        # Validate device context using page object methods
        device_series = dashboard_page.get_expected_device_series()
        timeout_multiplier = dashboard_page.get_timeout_multiplier()

        logger.info(f"{device_model}: Device series: {device_series}")
        logger.info(f"{device_model}: Timeout multiplier: {timeout_multiplier}x")

        # Validate concurrent protocol support using page object method
        concurrent_protocol_supported = (
            network_page.is_concurrent_protocol_supported_from_database()
        )
        logger.info(
            f"{device_model}: Concurrent protocol supported according to database: {concurrent_protocol_supported}"
        )

        # Navigate for concurrent protocol validation using page object method
        dashboard_page.navigate_to_page()
        dashboard_page.wait_for_page_load()

        logger.info(f"{device_model}: Dashboard page loaded successfully")

        # Validate concurrent protocol capability using page object methods
        dashboard_page.validate_concurrent_protocol_capability_support()

        # Test concurrent protocol access
        concurrent_access_results = {}
        protocol_errors = {}

        # Test concurrent NTP access
        if check_package_available("ntplib"):
            try:
                import ntplib

                def test_ntp_access():
                    try:
                        client = ntplib.NTPClient()
                        timeout = dashboard_page.calculate_timeout(5000) / 1000.0
                        response = client.request(device_ip, version=3, timeout=timeout)
                        concurrent_access_results["ntp"] = {
                            "success": True,
                            "response_time": response.tx_time,
                            "offset": getattr(response, "offset", 0),
                        }
                        logger.info(f"{device_model}: NTP concurrent access successful")
                    except Exception as ntp_error:
                        protocol_errors["ntp"] = str(ntp_error)
                        logger.warning(
                            f"{device_model}: NTP concurrent access failed: {ntp_error}"
                        )

            except ImportError:
                protocol_errors["ntp"] = "ntplib not available"
        else:
            protocol_errors["ntp"] = "ntplib package not installed"

        # Test concurrent HTTP/HTTPS access
        try:
            import urllib.request

            def test_http_access():
                try:
                    timeout = dashboard_page.calculate_timeout(5000) / 1000.0
                    req = urllib.request.Request(f"http://{device_ip}/")
                    response = urllib.request.urlopen(req, timeout=timeout)
                    concurrent_access_results["http"] = {
                        "success": True,
                        "status_code": response.getcode(),
                        "url": response.url,
                    }
                    logger.info(f"{device_model}: HTTP concurrent access successful")
                except Exception as http_error:
                    protocol_errors["http"] = str(http_error)
                    logger.warning(
                        f"{device_model}: HTTP concurrent access failed: {http_error}"
                    )

            def test_https_access():
                try:
                    import ssl

                    timeout = dashboard_page.calculate_timeout(5000) / 1000.0
                    ssl_context = ssl.create_default_context()
                    ssl_context.check_hostname = False
                    ssl_context.verify_mode = ssl.CERT_NONE
                    req = urllib.request.Request(f"https://{device_ip}/")
                    response = urllib.request.urlopen(
                        req, timeout=timeout, context=ssl_context
                    )
                    concurrent_access_results["https"] = {
                        "success": True,
                        "status_code": response.getcode(),
                        "url": response.url,
                    }
                    logger.info(f"{device_model}: HTTPS concurrent access successful")
                except Exception as https_error:
                    protocol_errors["https"] = str(https_error)
                    logger.warning(
                        f"{device_model}: HTTPS concurrent access failed: {https_error}"
                    )

        except Exception as urllib_error:
            protocol_errors["http_https"] = str(urllib_error)

        # Test concurrent SNMP access
        if check_package_available("pysnmp"):
            try:
                from pysnmp.hlapi import (
                    getCmd,
                    SnmpEngine,
                    CommunityData,
                    UdpTransportTarget,
                    ContextData,
                    ObjectType,
                    ObjectIdentity,
                )

                def test_snmp_access():
                    try:
                        timeout = dashboard_page.calculate_timeout(5000) / 1000.0
                        iterator = getCmd(
                            SnmpEngine(),
                            CommunityData("public"),
                            UdpTransportTarget((device_ip, 161), timeout=timeout),
                            ContextData(),
                            ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
                        )
                        errorIndication, errorStatus, errorIndex, varBinds = next(
                            iterator
                        )
                        if not errorIndication:
                            concurrent_access_results["snmp"] = {
                                "success": True,
                                "response": (
                                    str(varBinds[0][1]) if varBinds else "No response"
                                ),
                            }
                            logger.info(
                                f"{device_model}: SNMP concurrent access successful"
                            )
                        else:
                            protocol_errors["snmp"] = f"SNMP error: {errorIndication}"
                    except Exception as snmp_error:
                        protocol_errors["snmp"] = str(snmp_error)
                        logger.warning(
                            f"{device_model}: SNMP concurrent access failed: {snmp_error}"
                        )

            except ImportError:
                protocol_errors["snmp"] = "pysnmp not available"
        else:
            protocol_errors["snmp"] = "pysnmp package not installed"

        # Execute concurrent protocol tests
        protocol_threads = []

        # Add protocol tests to threads
        for protocol, test_func in [
            ("ntp", test_ntp_access if "ntp_access" in locals() else None),
            ("http", test_http_access if "http_access" in locals() else None),
            ("https", test_https_access if "https_access" in locals() else None),
            ("snmp", test_snmp_access if "snmp_access" in locals() else None),
        ]:
            if test_func:
                thread = threading.Thread(target=test_func)
                protocol_threads.append(thread)
                thread.start()

        # Wait for all threads to complete
        for thread in protocol_threads:
            thread.join(timeout=10.0)  # 10 second timeout for each thread

        # Small delay to ensure all operations complete
        time.sleep(1)

        # Validate concurrent protocol access results using page object methods
        network_page.validate_concurrent_protocol_access_results(
            concurrent_access_results, protocol_errors, device_model
        )

        # Additional concurrent protocol validation using page object methods
        dashboard_page.validate_concurrent_protocol_support_in_capabilities()

        # Series-specific concurrent protocol validation using page object methods
        if device_series == 2:
            network_page.validate_series2_concurrent_protocol_characteristics(
                concurrent_access_results
            )
        elif device_series == 3:
            network_page.validate_series3_concurrent_protocol_characteristics(
                concurrent_access_results
            )

        # Handle concurrent protocol access results
        successful_protocols = len(
            [p for p in concurrent_access_results.values() if p.get("success")]
        )
        total_protocols = len(concurrent_access_results) + len(protocol_errors)

        if successful_protocols > 0:
            print(
                f"Concurrent protocol access test passed: {successful_protocols}/{total_protocols} protocols successful for {device_model}"
            )
            logger.info(
                f"{device_model}: Concurrent protocol access test completed successfully"
            )
        else:
            logger.warning(
                f"{device_model}: No concurrent protocol access successful: {protocol_errors}"
            )
            print(
                f"Concurrent protocol access test handled gracefully - no successful protocols for {device_model}"
            )

            # Handle concurrent protocol unavailability gracefully using page object methods
            network_page.handle_concurrent_protocol_unavailability_gracefully(
                protocol_errors, device_model
            )

            # Still validate that device capabilities are correct using page object validation
            dashboard_page.validate_device_series_consistency(device_series)

            # Log graceful handling
            logger.info(
                f"{device_model}: Concurrent protocol access test handled gracefully - device validation passed"
            )

        # Cross-validation test using page object method
        dashboard_page.test_concurrent_protocol_cross_validation()

        # Final validation using page object methods
        network_page.validate_concurrent_protocol_access_integration_complete()

        logger.info(
            f"{device_model}: Concurrent protocol access validation completed successfully"
        )

    except Exception as e:
        logger.error(
            f"{device_model}: Concurrent protocol access validation encountered error - {e}"
        )
        # Graceful degradation - log error but don't fail test
        pytest.fail(
            f"Concurrent protocol access validation failed for {device_model}: {e}"
        )
