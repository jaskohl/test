@echo off
setlocal enabledelayedexpansion
REM Kronos Test Suite - Windows Batch Execution Script
REM Comprehensive test automation for Kronos satellite timing clocks
REM Configuration
set PYTHON_PATH=C:\Python311
set VENV_DIR=.venv
REM Default configuration
set DEVICE_IP=172.16.190.46
set RESULTS_DIR=190-46-k2
set MAX_FAIL=2
REM if NUMBER_OF_WORKERS is greater than 0, browser will run in headless mode
set NUMBER_OF_WORKERS=1
REM BROWSER_MODE=--headed or BROWSER_MODE=
set BROWSER_MODE=
REM Initialize variables
set PASSWORD=novatech
set DEBUG_MODE=
set SKIP_LOGIN=
set TEST_PATTERN=
set TEST_SUITE=tests\individual_tests\test_02

REM tests\individual_tests\test_01
REM tests\individual_tests\test_02
REM tests\individual_tests\test_03
REM tests\individual_tests\test_04
REM tests\individual_tests\test_05
REM tests\individual_tests\test_06
REM tests\individual_tests\test_07
REM tests\individual_tests\test_08
REM tests\individual_tests\test_09
REM tests\individual_tests\test_10
REM tests\individual_tests\test_11
REM tests\individual_tests\test_12
REM tests\individual_tests\test_13
REM tests\individual_tests\test_14
REM tests\individual_tests\test_15
REM tests\individual_tests\test_16
REM tests\individual_tests\test_17
REM tests\individual_tests\test_18
REM tests\individual_tests\test_19
REM tests\individual_tests\test_20
REM tests\individual_tests\test_21
REM tests\individual_tests\test_22
REM tests\individual_tests\test_23
REM tests\individual_tests\test_24
REM tests\individual_tests\test_25
REM tests\individual_tests\test_26
REM tests\individual_tests\test_27
REM tests\individual_tests\test_28
REM tests\individual_tests\test_29
REM tests\individual_tests\test_30
REM tests\individual_tests\test_31
REM tests\individual_tests\test_32
REM tests\individual_tests\test_33


REM tests\test_01_authentication.py tests\test_02_navigation.py tests\test_03_general_config.py tests\test_04_network_config_series2.py tests\test_05_time_config.py tests\test_06_gnss_config.py tests\test_07_outputs_config.py tests\test_08_display_config.py tests\test_09_access_config.py tests\test_10_dashboard.py tests\test_11_form_validation.py tests\test_12_error_handling.py tests\test_13_state_transitions.py tests\test_14_performance.py tests\test_15_capability_detection.py tests\test_16_integration.py tests\test_17_cross_browser.py tests\test_18_workflow.py tests\test_19_dynamic_ui.py tests\test_20_security.py tests\test_22_data_integrity.py tests\test_23_boundary.py tests\test_25_time_sync_edge_cases.py tests\test_26_api_interfaces.py tests\test_27_ptp_config.py tests\test_28_syslog_config.py tests\test_29_network_config_series3.py tests\test_30_snmp_config.py tests\test_31_upload_config.py
REM tests\test_01_authentication.py
REM tests\test_02_navigation.py
REM tests\test_03_general_config.py
REM tests\test_04_network_config_series2.py
REM tests\test_05_time_config.py
REM tests\test_06_gnss_config.py
REM tests\test_07_outputs_config.py
REM tests\test_08_display_config.py
REM tests\test_09_access_config.py
REM tests\test_10_dashboard.py
REM tests\test_11_form_validation.py
REM tests\test_12_error_handling.py
REM tests\test_13_state_transitions.py
REM tests\test_14_performance.py
REM tests\test_15_capability_detection.py
REM tests\test_16_integration.py
REM tests\test_17_cross_browser.py
REM tests\test_18_workflow.py
REM tests\test_19_dynamic_ui.py
REM tests\test_20_security.py
REM tests\test_22_data_integrity.py
REM tests\test_23_boundary.py
REM tests\test_25_time_sync_edge_cases.py
REM tests\test_26_api_interfaces.py
REM tests\test_27_ptp_config.py
REM tests\test_28_syslog_config.py
REM tests\test_29_network_config_series3.py
REM tests\test_30_snmp_config.py
REM tests\test_31_upload_config.py
set VERBOSE=
set PARALLEL=
set HTML_REPORT=
set PYTHONPATH=
echo ========================================
echo     Kronos Test Suite - Windows Runner
echo ========================================
echo.
:check_dependencies
echo Checking dependencies...
REM Check Python
"%PYTHON_PATH%\python.exe" --version >nul 2>&1
if errorlevel 1 (
echo Error: Python is required but not installed
echo Please install Python 3.7 or later from https://python.org
goto cleanup
)
echo Python found at %PYTHON_PATH%
:create_virtual_env
echo Setting up virtual environment...
REM Check if virtual environment already exists
if exist "%VENV_DIR%" (
echo Virtual environment already exists
) else (
echo Creating virtual environment...
"%PYTHON_PATH%\python.exe" -m venv "%VENV_DIR%"
if errorlevel 1 (
echo Error: Failed to create virtual environment
goto cleanup
)
echo Virtual environment created successfully
)
REM Activate virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if not defined VIRTUAL_ENV (
echo Error: Failed to activate virtual environment in %VENV_DIR%. The VIRTUAL_ENV variable was not set.
exit /b 1
)
REM Verify virtual environment activation
python --version >nul 2>&1
if errorlevel 1 (
echo Error: Virtual environment not properly activated.
goto cleanup
)
echo Virtual environment activated
:install_dependencies
echo Installing Python dependencies...
if not exist requirements.txt (
echo Error: requirements.txt not found
goto cleanup
)
REM Use 'pip' from the activated VENV
pip install -r requirements.txt
if errorlevel 1 (
echo Error: Failed to install Python dependencies
goto cleanup
)
echo Dependencies installed
REM Install Playwright browsers (in the VENV)
echo Installing Playwright browsers...
REM Always install browsers to ensure they are available and up-to-date
python -m playwright install chromium
if errorlevel 1 (
echo Error: Failed to install Playwright browsers
goto cleanup
)
echo Playwright Chromium browser installed
:setup_test_environment
echo Setting up test environment...
REM Create results directory structure
if not exist "%RESULTS_DIR%" mkdir "%RESULTS_DIR%"
if not exist "%RESULTS_DIR%\screenshots" mkdir "%RESULTS_DIR%\screenshots"
if not exist "%RESULTS_DIR%\videos" mkdir "%RESULTS_DIR%\videos"
if not exist "%RESULTS_DIR%\html" mkdir "%RESULTS_DIR%\html"
REM Set environment variables
set PYTEST_CURRENT_TEST=
echo Test environment ready
goto test_connectivity_or_run
:test_connectivity
echo Testing connectivity to device...
REM Simple connectivity test using ping (more reliable than curl on Windows)
ping -n 1 -w 5000 %DEVICE_IP% >nul 2>&1
if errorlevel 1 (
echo   Warning: Device may not be reachable at %DEVICE_IP%
echo   This could be normal if device is on a different network
echo   Tests will continue but may fail if device is not accessible
) else (
echo Device is reachable at %DEVICE_IP%
)
:test_connectivity_or_run
:run_tests
echo Running Kronos test suite...
echo Configuration:
echo   Device IP: %DEVICE_IP%
echo   Password: [PROTECTED]
echo   Browser Mode: %BROWSER_MODE%
echo   Results Directory: %RESULTS_DIR%
if not "%MAX_FAIL%"=="" if not "%MAX_FAIL%"=="0" echo   Max Failures: %MAX_FAIL%
if not "%TEST_SUITE%"=="" echo   Test Suite: %TEST_SUITE%
if not "%TEST_PATTERN%"=="" echo   Test Pattern: %TEST_PATTERN%
echo.
REM Check if we're in the right directory
if not exist conftest.py (
echo Error: Must be run from the Kronos test suite root directory
echo Expected files: conftest.py, tests
goto cleanup
)
if not exist tests (
echo Error: tests directory not found
echo Expected directory structure: pages, tests
goto cleanup
)
REM Build pytest command
set PYTEST_CMD=python -m pytest
REM Add test target
if not "%TEST_SUITE%"=="" (
set PYTEST_CMD=%PYTEST_CMD% %TEST_SUITE%
) else (
set PYTEST_CMD=%PYTEST_CMD% tests/
)
REM Add options
set PYTEST_CMD=%PYTEST_CMD% --device_ip=%DEVICE_IP% --browser chromium --results_dir %RESULTS_DIR% --html=%RESULTS_DIR%\report.html --self-contained-html
if not "%BROWSER_MODE%"=="" if not "%BROWSER_MODE%"=="--headless" set PYTEST_CMD=%PYTEST_CMD% %BROWSER_MODE%
if not "%DEBUG_MODE%"=="" set PYTEST_CMD=%PYTEST_CMD% %DEBUG_MODE%
if not "%TEST_PATTERN%"=="" set PYTEST_CMD=%PYTEST_CMD% %TEST_PATTERN%
if not "%VERBOSE%"=="" set PYTEST_CMD=%PYTEST_CMD% %VERBOSE%
if not "%HTML_REPORT%"=="" set PYTEST_CMD=%PYTEST_CMD% %HTML_REPORT%
if not "%MAX_FAIL%"=="" if not "%MAX_FAIL%"=="0" set PYTEST_CMD=%PYTEST_CMD% --maxfail=%MAX_FAIL%
if not "%NUMBER_OF_WORKERS%"=="" if not "%NUMBER_OF_WORKERS%"=="0" set PYTEST_CMD=%PYTEST_CMD% -n %NUMBER_OF_WORKERS%
rem set PYTEST_CMD=%PYTEST_CMD% -n 3
REM Execute tests
echo Executing: %PYTEST_CMD%
echo.
%PYTEST_CMD%
set TEST_EXIT_CODE=%errorlevel%
echo.
if %TEST_EXIT_CODE%==0 (
echo ========================================
echo          TEST EXECUTION COMPLETED
echo ========================================
REM Show results summary
if exist "%RESULTS_DIR%\report.html" (
    echo HTML Report: %RESULTS_DIR%\report.html
)
REM Count screenshots
set SCREENSHOT_COUNT=0
for %%f in ("%RESULTS_DIR%\screenshots\*.png") do set /a SCREENSHOT_COUNT+=1
if %SCREENSHOT_COUNT% gtr 0 (
    echo Screenshots: %SCREENSHOT_COUNT% files in %RESULTS_DIR%\screenshots\
)
REM Count videos
set VIDEO_COUNT=0
for %%f in ("%RESULTS_DIR%\videos\*.webm") do set /a VIDEO_COUNT+=1
if %VIDEO_COUNT% gtr 0 (
    echo Videos: %VIDEO_COUNT% files in %RESULTS_DIR%\videos\
)
echo All tests completed successfully!
) else (
echo ========================================
echo          TEST EXECUTION FAILED
echo ========================================
echo Test execution failed!
)
goto cleanup
REM Cleanup block to ensure the environment is deactivated
:cleanup
echo.
if defined VIRTUAL_ENV (
echo Deactivating virtual environment: %VENV_DIR%
call "%VENV_DIR%\Scripts\deactivate.bat"
) else (
echo Virtual environment was not active or VIRTUAL_ENV not defined. Skipping deactivation.
)
exit /b %TEST_EXIT_CODE%
