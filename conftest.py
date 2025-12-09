"""
Pytest configuration and fixtures for Kronos device comprehensive test suite.
Provides enhanced fixtures for device testing with proper authentication,
configuration unlock, and error handling following established patterns.
Based on COMPLETE_TEST_LIST.md v4.1 and device exploration data.
"""

from urllib.parse import urlparse
import pytest
import json
import time
import re
from playwright.sync_api import Page, Browser, BrowserContext, expect
from typing import Generator, Dict, Any, List
from datetime import datetime
import os
import sys

# Add parent directory to path for page object imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.login_page import LoginPage
from pages.configuration_unlock_page import ConfigurationUnlockPage
from pages.dashboard_page import DashboardPage
from pages.general_config_page import GeneralConfigPage
from pages.network_config_page import NetworkConfigPage
from pages.time_config_page import TimeConfigPage
from pages.outputs_config_page import OutputsConfigPage
from pages.gnss_config_page import GNSSConfigPage
from pages.display_config_page import DisplayConfigPage
from pages.snmp_config_page import SNMPConfigPage
from pages.syslog_config_page import SyslogConfigPage
from pages.upload_config_page import UploadConfigPage
from pages.access_config_page import AccessConfigPage
from pages.ptp_config_page import PTPConfigPage
from pages.device_capabilities import DeviceCapabilities


# Enhanced utility functions for dynamic waiting
def wait_for_satellite_loading(page: Page, timeout: int = 30000) -> bool:
    """
    Enhanced wait for satellite loading to complete with multiple detection methods.

    FIXED: Replaced flawed logic with comprehensive state detection that works across all device variants.
    Args:
        page: Playwright page object
        timeout: Timeout in milliseconds (reduced from 60s to 30s for better responsiveness)
    Returns:
        True if loading completed or page is ready, False if timeout
    """
    start_time = time.time()
    timeout_seconds = timeout / 1000.0

    # Quick check: if page is already in ready state, return immediately
    if is_page_ready_state(page):
        return True

    # Main waiting loop with multiple detection strategies
    while time.time() - start_time < timeout_seconds:
        try:
            # Strategy 1: Check for active loading indicators
            if has_active_loading_indicators(page):
                time.sleep(0.3)  # Wait a bit longer when loading is active
                continue
        except Exception as e:
            print(f"Warning: Error checking loading indicators: {e}")
            # Continue trying even if detection has issues
            pass
        time.sleep(0.2)  # Brief pause between checks

    # Final verification: if we can't detect loading, assume ready
    return is_page_ready_state(page)


def has_active_loading_indicators(page: Page) -> bool:
    """
    Check for active loading indicators that prevent interaction.

    Returns:
        True if loading indicators are active, False otherwise
    """
    try:
        # Check for loading mask/overlay
        loading_masks = page.locator(
            '.page_loading_mask, [class*="loading"][class*="mask"], .pageLoadingMask'
        )
        if loading_masks.first.is_visible():
            return True

        # Check for specific loading text
        loading_text = page.get_by_text("Loading satellite data...", exact=False)
        if loading_text.is_visible():
            return True

        # Check for spinning indicators
        spinners = page.locator(
            '[class*="spinner"], [class*="loading"]:not([class*="mask"])'
        )
        if spinners.count() > 0:
            # Only consider it active if actually visible
            for i in range(
                min(spinners.count(), 3)
            ):  # Check first 3 to avoid strict mode
                if spinners.nth(i).is_visible():
                    return True

        return False
    except:
        return False


def is_page_ready_state(page: Page) -> bool:
    """
    Check if page is in interactive/ready state for testing.

    Returns:
        True if page is ready for interaction, False otherwise
    """
    try:
        # Check for main header (indicates page structure is loaded)
        header = page.locator("#Main_Header, .main-header")
        if not header.is_visible():
            return False

        # Check for navigation elements
        nav_elements = page.locator('.sidebar, .navbar, [class*="nav"]')
        if nav_elements.count() > 0 and not nav_elements.first.is_visible():
            return False

        # Check for main content area
        main_content = page.locator(".content, .main-content, .wrapper")
        if not main_content.is_visible():
            return False

        # Check that body has meaningful content
        body = page.locator("body")
        if body.is_visible():
            content = body.text_content()
            if content and len(content.strip()) > 50:  # Has substantial content
                return True

        return False
    except:
        return False


def has_device_readiness_indicators(page: Page) -> bool:
    """
    Check for device-specific indicators that show it's ready for configuration.

    Returns:
        True if device-specific readiness indicators are present
    """
    try:
        # Check for Configure button (indicates unlocked state)
        configure_buttons = [
            'a[href="login"]',
            'a:has-text("Configure")',
            'a[title*="locked"]',
        ]

        for selector in configure_buttons:
            button = page.locator(selector)
            if button.is_visible():
                return True

        # Check for configuration section links
        config_sections = page.locator(
            'a[href*="general"], a[href*="time"], a[href*="network"]'
        )
        if config_sections.count() > 0:
            return True

        # Check for form elements that indicate configuration is available
        forms = page.locator("form, input, select")
        if forms.count() > 5:  # Substantial form content
            return True

        return False
    except:
        return False


def pytest_addoption(parser):
    """Add command line options for Kronos testing."""
    parser.addoption(
        "--device_ip",
        action="store",
        default="172.16.190.46",
        help="Kronos device IP address",
    )
    parser.addoption(
        "--password",
        action="store",
        default="novatech",
        help="Device password for authentication",
    )
    parser.addoption(
        "--results_dir",
        action="store",
        default="test-results",
        help="Directory to save test results",
    )
    parser.addoption(
        "--ignore_ssl",
        action="store_true",
        default=True,
        help="Ignore SSL certificate errors (for self-signed certificates)",
    )


# Session-scoped fixtures
@pytest.fixture(scope="session")
def device_ip(request) -> str:
    """Get device IP from command line or default."""
    return request.config.getoption("--device_ip")


@pytest.fixture(scope="session")
def device_password(request) -> str:
    """Get device password from command line or default."""
    return request.config.getoption("--password")


@pytest.fixture(scope="session")
def results_dir(request) -> str:
    """Get results directory from command line or default."""
    results_dir_path = request.config.getoption("--results_dir")
    os.makedirs(results_dir_path, exist_ok=True)
    os.makedirs(os.path.join(results_dir_path, "screenshots"), exist_ok=True)
    return results_dir_path


@pytest.fixture(scope="session")
def ignore_ssl(request) -> bool:
    """Get SSL ignore setting."""
    return request.config.getoption("--ignore_ssl")


@pytest.fixture(scope="session")
def base_url(device_ip) -> str:
    """Construct base URL for device."""
    return f"https://{device_ip}"


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    Inject custom launch arguments needed for embedded devices
    while preserving the --headed setting handled by the plugin.
    """

    # Custom launch arguments for security and certificate handling
    custom_args = [
        "--ignore-ssl-errors",
        "--ignore-certificate-errors",
        "--ignore-certificate-errors-spki-list",
        "--disable-web-security",
        "--allow-running-insecure-content",
        "--allow-insecure-localhost",
        "--disable-dev-shm-usage",
    ]

    # Merge custom args with the existing default launch args provided by the plugin
    # The 'headless' argument is automatically handled by the plugin based on --headed
    browser_type_launch_args["args"] = (
        browser_type_launch_args.get("args", []) + custom_args
    )

    return browser_type_launch_args


# Function-scoped fixtures
@pytest.fixture(scope="function")
def context(
    browser: Browser, ignore_ssl: bool
) -> Generator[BrowserContext, None, None]:
    """Create a new browser context for each test with enhanced SSL handling."""
    context_options = {
        "viewport": {"width": 1024, "height": 768},
        "ignore_https_errors": ignore_ssl,
        "accept_downloads": True,
        "java_script_enabled": True,
        "bypass_csp": True,  # Bypass Content Security Policy for embedded devices
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    context = browser.new_context(**context_options)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Create a new page in the context."""
    return context.new_page()


@pytest.fixture(scope="function")
def logged_in_page(page: Page, base_url: str, device_password: str, request) -> Page:
    """
    Provide a page that is logged in to status monitoring.
    Handles the first authentication (status monitoring).
    """
    try:
        page.goto(base_url, wait_until="domcontentloaded")
        login_page = LoginPage(page)
        login_page.verify_page_loaded()
        success = login_page.login(password=device_password)
        if not success:
            pytest.fail("Failed to login to device")
        # Wait for page navigation away from authenticate page (indicates login success)
        expect(page).not_to_have_url("**/authenticate", timeout=10000)
        # OPTIMIZATION: Wait 3 seconds for any satellite loading (based on device exploration timing)
        # This is much faster than the previous hardcoded 12-second sleep and dynamic waiting issues
        login_page.wait_for_satellite_loading()  # Wait for satellite loading to complete

        # Extract and store device hardware model globally (only if not already set)
        if (
            not hasattr(request.session, "device_hardware_model")
            or request.session.device_hardware_model is None
        ):
            dashboard_page = DashboardPage(page)
            device_info = dashboard_page.get_device_info()
            hardware_model = device_info.get("Model Number")
            if hardware_model:
                request.session.device_hardware_model = hardware_model
                print(f"Detected device hardware model: {hardware_model}")
            else:
                print("Warning: Could not detect device hardware model from dashboard")

        return page
    except Exception as e:
        # Enhanced error reporting for certificate/connection issues
        pytest.fail(
            f"Failed to login to device at {base_url}: {str(e)}. "
            f"This may be due to SSL certificate issues. "
            f"Try running with --ignore_ssl=true (already default)"
        )


def navigate_with_retry(
    page: Page, url: str, device_ip: str, device_series: str, max_retries: int = 3
) -> bool:
    """
    Navigate to URL with retry logic and device-specific handling.
    Args:
        page: Playwright page object
        url: Target URL to navigate to
        device_ip: Device IP address for special handling
        device_series: Device series for timeout adjustments
        max_retries: Maximum number of retry attempts
    Returns:
        True if navigation successful, False otherwise
    """
    device_ip_clean = device_ip.replace("https://", "").replace("http://", "")
    # Device-specific timeout adjustments
    base_timeout = 60000
    for attempt in range(max_retries):
        current_timeout = base_timeout * (2**attempt)  # Exponential backoff
        print(
            f"Navigation attempt {attempt + 1}/{max_retries} to {url} (timeout: {current_timeout}ms)"
        )
        try:
            # Pre-navigation health check
            start_time = time.time()
            response = page.goto(
                url, timeout=current_timeout, wait_until="domcontentloaded"
            )
            response_time = time.time() - start_time
            if response and response.ok:
                print(f"Navigation successful in {response_time:.2f}s")
                time.sleep(1)  # Brief stabilization pause
                return True
            else:
                print(
                    f"Navigation failed with status: {response.status if response else 'No response'}"
                )
        except Exception as e:
            error_msg = str(e)
            print(f"Navigation attempt {attempt + 1} failed: {error_msg}")
            # Try HTTP fallback for HTTPS failures on first attempt
            if attempt == 0 and "https://" in url:
                try:
                    http_url = url.replace("https://", "http://")
                    print(f"Trying HTTP fallback: {http_url}")
                    response = page.goto(
                        http_url, timeout=current_timeout, wait_until="domcontentloaded"
                    )
                    if response and response.ok:
                        print("HTTP fallback successful")
                        time.sleep(1)
                        return True
                except Exception as http_e:
                    print(f"HTTP fallback also failed: {http_e}")
            # Don't wait after last attempt
            if attempt < max_retries - 1:
                wait_time = min(5, 2**attempt)  # Cap wait time
                print(f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
    return False


@pytest.fixture(scope="function")
def unlocked_config_page(
    logged_in_page: Page, base_url: str, device_password: str
) -> Page:
    """
    Provide a page with configuration access unlocked.
    Handles both authentications (status + configuration).
    FIXED: Follows device exploration workflow - Dashboard → Configure link → Unlock auth

    Device exploration data shows proper workflow:
    1. Status login to dashboard (handled by logged_in_page)
    2. Click "Configure" link from dashboard (required trigger)
    3. THEN secondary authentication page loads
    """
    unlock_page = ConfigurationUnlockPage(logged_in_page)

    url = logged_in_page.url

    # Use urlparse to break the URL into its components
    parsed_url = urlparse(url)

    # The .netloc attribute contains the network location (domain or IP address)
    # and automatically strips the protocol (http:// or https://) and the path.
    device_ip = parsed_url.netloc

    # Device-aware unlock timeout
    unlock_timeout = 60000
    print(f"Using {unlock_timeout}ms unlock timeout for ({device_ip})")

    # FIXED: Follow device exploration workflow per LOCATOR_STRATEGY.md
    # Device exploration shows config unlock requires clicking "Configure" from dashboard

    try:
        # Device exploration shows: Dropdown menú → Configure link
        # Note: Using text selector as fallback - Configure link has title but text is reliable per exploration
        configure_link = (
            logged_in_page.locator("a[title*='locked']")
            .filter(has_text="Configure")
            .first
        )

        # Alternative selector if specific ID fails
        if not configure_link.is_visible(timeout=2000):
            configure_link = logged_in_page.get_by_text("Configure", exact=False).first

        expect(configure_link).to_be_visible(timeout=5000)
        configure_link.click()
        time.sleep(2)  # Allow secondary auth page to load

        # Now unlock with password (device exploration shows this is required)
        print("Secondary authentication triggered - unlocking configuration...")
        success = unlock_page.unlock_configuration(
            password=device_password, timeout=unlock_timeout
        )

        if success:
            return logged_in_page
        else:
            pytest.fail(f"Configuration unlock failed after clicking Configure.")

    except Exception as e:
        # If workflow fails, log detailed state for troubleshooting
        error_details = {
            "device_ip": device_ip,
            "error": f"Configure workflow failed: {str(e)}",
            "current_url": logged_in_page.url,
            "page_title": logged_in_page.title(),
            "configure_links_found": logged_in_page.get_by_text("Configure").count(),
            "locked_links_found": logged_in_page.locator("a[title*='locked']").count(),
            "navigation_success": False,
            "timestamp": datetime.now().isoformat(),
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_file = (
            f"debug_configure_workflow_{device_ip.replace('.', '_')}_{timestamp}.json"
        )
        with open(debug_file, "w") as f:
            json.dump(error_details, f, indent=2)

            pytest.fail(
                f"Configure link workflow failed. Debug info saved to {debug_file}"
            )


# Page object fixtures
@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture(scope="function")
def configuration_unlock_page(logged_in_page: Page, request) -> ConfigurationUnlockPage:
    logged_in_page.goto(f"{base_url}/login", wait_until="domcontentloaded")
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate network configuration")
    return ConfigurationUnlockPage(logged_in_page, device_model=device_model)


@pytest.fixture(scope="function")
def dashboard_page(unlocked_config_page: Page) -> DashboardPage:
    return DashboardPage(unlocked_config_page)


@pytest.fixture(scope="function")
def general_config_page(
    unlocked_config_page: Page, base_url: str, request
) -> GeneralConfigPage:
    unlocked_config_page.goto(f"{base_url}/general", wait_until="domcontentloaded")
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate network configuration")
    return GeneralConfigPage(unlocked_config_page, device_model=device_model)


@pytest.fixture(scope="function")
def network_config_page(unlocked_config_page: Page, base_url: str) -> NetworkConfigPage:
    unlocked_config_page.goto(f"{base_url}/network", wait_until="domcontentloaded")
    return NetworkConfigPage(unlocked_config_page)


@pytest.fixture(scope="function")
def time_config_page(
    unlocked_config_page: Page, base_url: str, request
) -> TimeConfigPage:
    unlocked_config_page.goto(f"{base_url}/time", wait_until="domcontentloaded")
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate network configuration")
    return TimeConfigPage(unlocked_config_page, device_model=device_model)


@pytest.fixture(scope="function")
def outputs_config_page(
    unlocked_config_page: Page, base_url: str, request
) -> OutputsConfigPage:
    unlocked_config_page.goto(f"{base_url}/outputs", wait_until="domcontentloaded")
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate network configuration")
    device_series = DeviceCapabilities.get_series(device_model)
    return OutputsConfigPage(unlocked_config_page, device_series)


@pytest.fixture(scope="function")
def gnss_config_page(
    unlocked_config_page: Page, base_url: str, request
) -> GNSSConfigPage:
    unlocked_config_page.goto(f"{base_url}/gnss", wait_until="domcontentloaded")
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate network configuration")
    return GNSSConfigPage(unlocked_config_page, device_model=device_model)


@pytest.fixture(scope="function")
def display_config_page(unlocked_config_page: Page, base_url: str) -> DisplayConfigPage:
    unlocked_config_page.goto(f"{base_url}/display", wait_until="domcontentloaded")
    return DisplayConfigPage(unlocked_config_page)


@pytest.fixture(scope="function")
def snmp_config_page(unlocked_config_page: Page, base_url: str) -> SNMPConfigPage:
    unlocked_config_page.goto(f"{base_url}/snmp", wait_until="domcontentloaded")
    return SNMPConfigPage(unlocked_config_page)


@pytest.fixture(scope="function")
def syslog_config_page(unlocked_config_page: Page, base_url: str) -> SyslogConfigPage:
    unlocked_config_page.goto(f"{base_url}/syslog", wait_until="domcontentloaded")
    return SyslogConfigPage(unlocked_config_page)


@pytest.fixture(scope="function")
def upload_config_page(unlocked_config_page: Page, base_url: str) -> UploadConfigPage:
    unlocked_config_page.goto(f"{base_url}/upload", wait_until="domcontentloaded")
    return UploadConfigPage(unlocked_config_page)


@pytest.fixture(scope="function")
def access_config_page(unlocked_config_page: Page, base_url: str) -> AccessConfigPage:
    unlocked_config_page.goto(f"{base_url}/access", wait_until="domcontentloaded")
    return AccessConfigPage(unlocked_config_page)


@pytest.fixture(scope="function")
def ptp_config_page(
    unlocked_config_page: Page, base_url: str, request
) -> PTPConfigPage:
    unlocked_config_page.goto(f"{base_url}/ptp", wait_until="domcontentloaded")
    device_model = request.session.device_hardware_model
    if not device_model:
        pytest.fail("Device model not detected - cannot validate network configuration")
    device_series = DeviceCapabilities.get_series(device_model)
    return PTPConfigPage(unlocked_config_page, device_series=device_series)


def detect_https_enforcement_mode(access_config_page: Page, device_ip: str) -> str:
    """
    Detect HTTPS enforcement mode by checking device configuration access page.

    DEVICE-AWARE: Returns default "NEVER" mode if selector not implemented on device,
    rather than failing. Many devices don't have HTTPS enforcement capability.

    Args:
        page: Playwright page object
        device_ip: Device IP for URL construction

    Returns:
        HTTPS enforcement mode: "NEVER", "CFG_ONLY", "ALWAYS", or "UNKNOWN"
    """
    try:
        # Check for HTTPS enforcement selector
        enforce_https_select = access_config_page.locator(
            "select[name='enforce_https']"
        )
        if not enforce_https_select.is_visible(timeout=2000):
            # DEVICE-AWARE FALLBACK: Return default if selector doesn't exist
            # Many Kronos devices don't implement HTTPS enforcement
            print(
                f"HTTPS enforcement selector not found on device {device_ip} - using default 'NEVER' mode"
            )
            return "NEVER"

        # Read current enforcement mode
        selected_option = enforce_https_select.locator("option:checked")
        if selected_option.is_visible():
            mode = selected_option.get_attribute("value")
            return (
                mode
                if mode in ["NEVER", "CFG_ONLY", "ALWAYS"]
                else "UNKNOWN"  # Return UNKNOWN instead of failing
            )
        else:
            # DEVICE-AWARE FALLBACK: Return default if can't read value
            print(
                f"Could not read HTTPS enforcement mode from device {device_ip} - using default 'NEVER' mode"
            )
            return "NEVER"
    except Exception as e:
        # DEVICE-AWARE FALLBACK: Return default on any error
        print(
            f"Error detecting HTTPS enforcement mode on device {device_ip}: {e} - using default 'NEVER' mode"
        )
        return "NEVER"


# CRITICAL FIX: Missing fixtures that were causing 98 ERROR tests
# Added to resolve fixture injection failures
@pytest.fixture(scope="function")
def device_series(request, logged_in_page) -> str:
    """
    Get device series information (Series 2 vs Series 3).

    This fixture depends on logged_in_page to ensure device_hardware_model
    is populated during the login process.
    """
    device_model = getattr(request.session, "device_hardware_model")
    if not device_model:
        pytest.fail("Device model not detected - device must be logged in first")

    # Direct method call instead of relying on potentially broken DeviceCapabilities.get_series()
    try:
        device_info = DeviceCapabilities.DEVICE_DATABASE.get(device_model, {}).get(
            "device_info", {}
        )
        device_series = device_info.get("model", "")
        if device_series:
            request.session.device_series = device_series
            print(f"Device series determined: {device_series}")
        else:
            pytest.fail(f"Could not determine device series for model: {device_model}")
    except Exception as e:
        pytest.fail(f"Error determining device series for model {device_model}: {e}")

    return device_series


@pytest.fixture(scope="function")
def device_capabilities(request, logged_in_page) -> dict:
    """
    Get device capabilities dictionary.

    Provides device capability information by using DeviceCapabilities.get_capabilities()
    with additional derived capabilities like timeout multipliers.
    """
    device_model = getattr(request.session, "device_hardware_model")
    if not device_model:
        pytest.fail("Device model not detected - device must be logged in first")

    # Get base capabilities
    capabilities = DeviceCapabilities.get_capabilities(device_model)

    # Add derived capabilities
    if capabilities:
        # Add timeout multipliers based on device series
        device_series = DeviceCapabilities.get_series(device_model)
        if device_series == "Series 3":
            capabilities["timeout_multiplier"] = 1.5
            capabilities["loading_timeout"] = 8000  # 8 seconds for Series 3
        else:  # Series 2
            capabilities["timeout_multiplier"] = 1.0
            capabilities["loading_timeout"] = 5000  # 5 seconds for Series 2

        # Store in session for metadata
        request.session.device_capabilities = capabilities
        print(f"Device capabilities loaded: {len(capabilities)} capabilities")
    else:
        pytest.fail(f"Could not get capabilities for device model: {device_model}")

    return capabilities


# Pytest hooks
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "high_priority: mark test as high priority")
    config.addinivalue_line(
        "markers", "requires_tools: mark test as requiring additional software tools"
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test result for all phases (setup, call, teardown).

    CORRECTED: October 28, 2025
    - Now stores reports for ALL phases in a dictionary keyed by phase name
    - Previous version only stored last phase, causing outcome capture to fail
    - This allows test_metadata fixture to explicitly read the call phase report
    """
    outcome = yield
    report = outcome.get_result()

    # Store reports for all phases (setup, call, teardown)
    # Key insight: pytest runs tests in three phases, each generating a report
    # We need to preserve all of them so fixtures can access the correct phase
    if not hasattr(item, "reports"):
        item.reports = {}

    # Store this report keyed by its phase name
    item.reports[report.when] = report


@pytest.fixture(scope="function", autouse=True)
def test_metadata(request, results_dir, page: Page):
    """
    Capture test metadata including enhanced debugging data for failed tests.

    Enhanced: November 21, 2025
    - Added test context passing to debug files (replacing generic message)
    - Captures test file, function name, class name for better debugging
    - Includes device series and IP in context
    """
    test_start_time = datetime.now()

    # Capture current test context for debug files
    test_context = {
        "test_function_name": request.node.name,
        "test_class_name": (
            getattr(request.node.cls, "__name__", "Unknown")
            if request.node.cls
            else "Unknown"
        ),
        "test_file": request.node.fspath.basename,
        "device_ip": request.config.getoption("--device_ip", "unknown"),
        "device_series": getattr(request.session, "device_series", "Unknown"),
    }

    # Capture browser console logs during test execution
    console_logs = []
    js_errors = []

    def handle_console(msg):
        # Use current timestamp since msg.time is not available
        current_ts = time.time()
        if msg.type == "error":
            js_errors.append(
                {
                    "text": msg.text,
                    "timestamp": current_ts,
                    "location": str(getattr(msg, "location", "unknown")),
                }
            )
        else:
            console_logs.append(
                {"text": msg.text, "timestamp": current_ts, "type": msg.type}
            )

    page.on("console", handle_console)

    # Capture failed network requests
    failed_requests = []

    def handle_response(response):
        if not response.ok:
            failed_requests.append(
                {
                    "url": response.url,
                    "status": response.status,
                    "status_text": response.status_text,
                    "method": response.request.method,
                }
            )

    page.on("response", handle_response)

    yield

    try:
        test_duration = (datetime.now() - test_start_time).total_seconds()

        # Get the call phase report (actual test execution)
        reports = getattr(request.node, "reports", {})
        call_report = reports.get("call", None)

        outcome = "unknown"
        if call_report:
            if call_report.passed:
                outcome = "passed"
            elif call_report.failed:
                outcome = "failed"
            elif call_report.skipped:
                outcome = "skipped"
        else:
            print(f"WARNING: No call report for {request.node.name}")
            print(f"Available report phases: {list(reports.keys())}")
            if "setup" in reports and reports["setup"].failed:
                outcome = "setup_failed"
            elif "teardown" in reports and reports["teardown"].failed:
                outcome = "teardown_failed"

        # Base metadata for all tests
        metadata = {
            "test_name": request.node.name,
            "test_file": request.node.fspath.basename,
            "test_context": test_context,  # Now includes detailed test context
            "duration": test_duration,
            "timestamp": test_start_time.isoformat(),
            "outcome": outcome,
            "screenshot": "N/A",
        }

        # Enhanced metadata for failed tests
        # CHECK FOR EXPECTED FAILURES: Skip debug capture for intentional authentication errors
        is_expected_failure = False
        test_name_lower = request.node.name.lower()

        # Check for authentication-related expected failures
        auth_failure_patterns = [
            "invalid_password_error",
            "empty_password_submission",
            "invalid_password_unlock_error",
        ]

        if any(pattern in test_name_lower for pattern in auth_failure_patterns):
            is_expected_failure = True
            print(
                f"Detected expected authentication failure test: {request.node.name} - skipping debug file creation"
            )

        if outcome == "failed" and call_report and not is_expected_failure:
            # Capture error details from pytest report
            error_details = {
                "error_message": (
                    str(call_report.longrepr)
                    if call_report.longrepr
                    else "No error message available"
                ),
                "error_type": "Unknown",
                "failure_location": "Unknown",
            }

            # Extract error type and location from the longrepr
            if call_report.longrepr:
                longrepr_str = str(call_report.longrepr)

                # Try to extract error type (common patterns)
                error_type_match = re.search(
                    r"([A-Za-z]+Error|[A-Za-z]+Exception)", longrepr_str
                )
                if error_type_match:
                    error_details["error_type"] = error_type_match.group(1)

                # Pattern for file:line information
                location_match = re.search(r"([/\\][^:]+:\d+)", longrepr_str)
                if location_match:
                    error_details["failure_location"] = location_match.group(1)

            # Get device information from fixtures
            device_info = {}
            try:
                device_ip = request.config.getoption("--device_ip")
                device_info["device_ip"] = device_ip
                device_info["device_series"] = getattr(
                    request.session, "device_series", "Unknown"
                )
                device_info["series_variant"] = getattr(
                    request.session, "series3_variant", "Unknown"
                )
            except:
                pass

            # Get browser information
            browser_info = {}
            try:
                browser_info["user_agent"] = page.evaluate("navigator.userAgent")
                browser_info["viewport"] = page.viewport_size
                browser_info["url"] = page.url
                title = page.title()
                if title:
                    browser_info["page_title"] = title
            except:
                pass

            # Add all debugging data to metadata
            metadata.update(
                {
                    "error_details": error_details,
                    "device_info": device_info,
                    "browser_info": browser_info,
                    "console_errors": js_errors,
                    "console_logs": (
                        console_logs[-10:] if console_logs else []
                    ),  # Last 10 non-error logs
                    "failed_requests": failed_requests,
                    "test_markers": list(request.node.keywords.keys()),
                }
            )

            # Take screenshot
            screenshot_path = os.path.join(
                results_dir, "screenshots", f"{request.node.name}_failure.png"
            )
            try:
                page.screenshot(path=screenshot_path)
                metadata["screenshot"] = os.path.relpath(screenshot_path, results_dir)
            except Exception as e:
                print(f"Failed to take screenshot: {e}")
                metadata["screenshot"] = "Error"

        # For expected failures, update metadata but skip debug files
        elif outcome == "failed" and call_report and is_expected_failure:
            metadata.update(
                {
                    "expected_failure": True,
                    "failure_reason": "Intentional authentication error test - debug files suppressed",
                    "screenshot": "Suppressed (expected failure)",
                }
            )
        # Write metadata file
        metadata_file = os.path.join(results_dir, f"{request.node.name}_metadata.json")
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

    except Exception as e:
        # Ensure metadata capture failures don't break tests
        print(f"ERROR in test_metadata fixture: {e}")
        import traceback

        traceback.print_exc()
