@echo off
setlocal enabledelayedexpansion
REM Kronos Test Suite - Windows Batch Execution Script
REM Comprehensive test automation for Kronos satellite timing clocks
REM Configuration
set PYTHON_PATH=C:\Python311
set VENV_DIR=.venv
REM Default configuration
set DEFAULT_DEVICE_IP=172.16.190.47
set DEFAULT_PASSWORD=novatech
set RESULTS_DIR=test-results-k3
set DEFAULT_MAX_FAIL=0
REM 0 means no limit (default pytest behavior)
REM Initialize variables
set "DEVICE_IP=%DEFAULT_DEVICE_IP%"
set "PASSWORD=%DEFAULT_PASSWORD%"
set "BROWSER_MODE="
set "DEBUG_MODE="
set "SKIP_LOGIN="
set "TEST_PATTERN="
set "TEST_SUITE="
set "VERBOSE="
set "PARALLEL="
set "HTML_REPORT="
set "MAX_FAIL=%DEFAULT_MAX_FAIL%"
set PYTHONPATH=
echo ========================================
echo     Kronos Test Suite - Windows Runner
echo ========================================
echo.
REM Parse command line arguments
:parse_args
if "%1"=="" goto check_dependencies
if "%1"=="--device_ip" (
set DEVICE_IP=%2
shift
shift
goto parse_args
)
if "%1"=="--headed" (
set BROWSER_MODE=--headed
shift
goto parse_args
)
if "%1"=="--headless" (
set BROWSER_MODE=
shift
goto parse_args
)
if "%1"=="--debug" (
set DEBUG_MODE=--debug_mode
shift
goto parse_args
)
if "%1"=="--skip_login" (
set SKIP_LOGIN=--skip_login
shift
goto parse_args
)
if "%1"=="--test" (
set TEST_PATTERN=-k %2
shift
shift
goto parse_args
)
REM === NEW: Add max_failures_allowed argument handling ===
if "%1"=="--max_failures_allowed" (
set MAX_FAIL=2%2
shift
shift
goto parse_args
)
REM =======================================================
if "%1"=="--verbose" (
set VERBOSE=-v
shift
goto parse_args
)
if "%1"=="--test_basic" (
set TEST_PATTERN=-k "test_basic or test_smoke or test_quick"
shift
goto parse_args
)
if "%1"=="--test_integration" (
set TEST_PATTERN=-k "integration"
shift
goto parse_args
)
if "%1"=="--test_advanced" (
set TEST_PATTERN=-k "advanced or behavior or resilience or compatibility"
shift
goto parse_args
)
if "%1"=="--test_performance" (
set TEST_PATTERN=-k "performance or timing or benchmark"
shift
goto parse_args
)
if "%1"=="--test_all" (
set TEST_PATTERN=
shift
goto parse_args
)
if "%1"=="--help" (
goto show_help
)
echo Error: Unknown option '%1'
echo Use --help for usage information
exit /b 1
:show_help
echo Usage: %0 [OPTIONS]
echo.
echo Options:
echo   --device_ip IP          Device IP address (default: %DEFAULT_DEVICE_IP%)
echo   --headed                Run with browser visible (default)
echo   --headless              Run browser in headless mode
echo   --debug                 Enable debug mode with extra screenshots
echo   --skip_login            Skip automatic login (for auth tests)
REM === NEW: Add max_failures_allowed to help output ===
echo   --max_failures_allowed N  Stop testing after N failures (0=no limit, default: %DEFAULT_MAX_FAIL%)
REM =======================================================
echo   --verbose               Enable verbose output
echo   --help                  Show this help message
echo.
echo Test Categories:
echo   --test_basic            Run basic functionality tests only
echo   --test_integration      Run integration workflow tests
echo   --test_advanced         Run advanced device behavior tests
echo   --test_performance      Run performance and timing tests
echo   --test_all              Run all test categories (default)
echo.
echo Examples:
echo   %0                      # Run all tests against Kronos Series 2
echo   %0 --test_basic         # Run only basic tests
echo   %0 --test_integration   # Run integration tests
echo   %0 --test_performance   # Run performance tests
echo   %0 --headless --test_advanced # Run advanced tests in headless mode
echo   %0 --max_failures_allowed 5 --test_basic # Stop basic tests after 5 failures
exit /b 0
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
echo Checking Playwright browsers...
REM FIX: Use 'python' from the VENV instead of the hardcoded path
python -c "import playwright; print('Playwright available')" >nul 2>&1
if errorlevel 1 (
echo Installing Playwright browsers...
REM FIX: Use 'python -m' from the VENV instead of the hardcoded path
python -m playwright install chromium
if errorlevel 1 (
echo Error: Failed to install Playwright browsers
goto cleanup
)
echo Playwright Chromium browser installed
) else (
echo Playwright browsers already available
)
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
if "%MAX_FAIL%" neq "0" echo   Max Failures: %MAX_FAIL%
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
if not "%BROWSER_MODE%"=="" set PYTEST_CMD=%PYTEST_CMD% %BROWSER_MODE%
if not "%DEBUG_MODE%"=="" set PYTEST_CMD=%PYTEST_CMD% %DEBUG_MODE%
if not "%SKIP_LOGIN%"=="" set PYTEST_CMD=%PYTEST_CMD% %SKIP_LOGIN%
if not "%TEST_PATTERN%"=="" set PYTEST_CMD=%PYTEST_CMD% %TEST_PATTERN%
if not "%VERBOSE%"=="" set PYTEST_CMD=%PYTEST_CMD% %VERBOSE%
if not "%PARALLEL%"=="" set PYTEST_CMD=%PYTEST_CMD% %PARALLEL%
if not "%HTML_REPORT%"=="" set PYTEST_CMD=%PYTEST_CMD% %HTML_REPORT%
REM === NEW: Add --maxfail=N to pytest command if set ===
if "%MAX_FAIL%" neq "0" set PYTEST_CMD=%PYTEST_CMD% --maxfail=%MAX_FAIL%
REM =======================================================
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
