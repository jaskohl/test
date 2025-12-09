@echo off
setlocal enabledelayedexpansion
REM Kronos Test Suite - Windows Batch Execution Script
REM Comprehensive test automation for Kronos satellite timing clocks
REM ==============================================================================
REM == CONFIGURATION
REM ==============================================================================
set PYTHON_PATH=C:\Python311
set VENV_DIR=.venv
REM Default configuration
set DEFAULT_DEVICE_IP=172.16.190.47
set DEFAULT_PASSWORD=novatech
set RESULTS_DIR=ind-test-results-k3-190-47
set DEFAULT_MAX_FAIL=30
REM 0 means no limit (default pytest behavior)
REM Initialize variables
set DEVICE_IP=%DEFAULT_DEVICE_IP%
set PASSWORD=%DEFAULT_PASSWORD%
REM set BROWSER_MODE=
set BROWSER_MODE=
set DEBUG_MODE=
set SKIP_LOGIN=
set TEST_PATTERN=
set TEST_SUITE=tests\individual_tests\test_02
set VERBOSE=
set PARALLEL=
set HTML_REPORT=
set MAX_FAIL=2%DEFAULT_MAX_FAIL%
set PYTHONPATH=
echo ========================================
echo     Kronos Test Suite - Windows Runner
echo ========================================
echo.
REM ==============================================================================
REM == ARGUMENT PARSING
REM ==============================================================================
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
if "%1"=="--max_failures_allowed" (
    set MAX_FAIL=2%2
    shift
    shift
    goto parse_args
)
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
echo   --max_failures_allowed N  Stop testing after N failures (0=no limit, default: %DEFAULT_MAX_FAIL%)
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
echo   %0                      # Run all tests, one file at a time (NEW default)
echo   %0 --test_basic         # Run only basic tests in a single run
echo   %0 --test "navigation"  # Run tests matching "navigation" in a single run
echo   %0 --headless --test_advanced # Run advanced tests in headless mode
echo   %0 --max_failures_allowed 5 # Stop after 5 failures when running file-by-file
exit /b 0
REM ==============================================================================
REM == ENVIRONMENT SETUP
REM ==============================================================================
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
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if not defined VIRTUAL_ENV (
    echo Error: Failed to activate virtual environment in %VENV_DIR%.
    exit /b 1
)
echo Virtual environment activated
:install_dependencies
echo Installing Python dependencies...
if not exist requirements.txt (
    echo Error: requirements.txt not found
    goto cleanup
)
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install Python dependencies
    goto cleanup
)
echo Dependencies installed
echo Checking Playwright browsers...
python -m playwright install chromium
if errorlevel 1 (
    echo Error: Failed to install Playwright browsers
    goto cleanup
)
echo Playwright Chromium browser installed
:setup_test_environment
echo Setting up test environment...
if not exist "%RESULTS_DIR%" mkdir "%RESULTS_DIR%"
if not exist "%RESULTS_DIR%\screenshots" mkdir "%RESULTS_DIR%\screenshots"
if not exist "%RESULTS_DIR%\videos" mkdir "%RESULTS_DIR%\videos"
if not exist "%RESULTS_DIR%\html" mkdir "%RESULTS_DIR%\html"
set PYTEST_CURRENT_TEST=
echo Test environment ready
REM ==============================================================================
REM == TEST EXECUTION
REM ==============================================================================
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
if not exist conftest.py (
    echo Error: Must be run from the Kronos test suite root directory
    goto cleanup
)
if not exist tests (
    echo Error: tests directory not found
    goto cleanup
)
REM === NEW: Decide execution strategy ===
REM If a test pattern or suite is specified, run once. Otherwise, loop through files.
if not "%TEST_PATTERN%"=="" goto run_single_pytest_instance
if not "%TEST_SUITE%"=="" goto run_single_pytest_instance
goto run_individual_files
REM --- Individual File Execution Logic ---
:run_individual_files
echo.
REM --- MODIFICATION START ---
echo [MODE] Running tests for each file individually. (Auto-discovering .py files in 'tests\')
echo.
set MASTER_EXIT_CODE=0
REM REMOVED: The hard-coded TEST_FILE_LIST has been removed.
REM Build base pytest command (without target or HTML report)
set BASE_PYTEST_CMD=python -m pytest --device_ip=%DEVICE_IP% --browser chromium --results_dir %RESULTS_DIR%
if not "%BROWSER_MODE%"=="" set BASE_PYTEST_CMD=%BASE_PYTEST_CMD% %BROWSER_MODE%
if not "%DEBUG_MODE%"=="" set BASE_PYTEST_CMD=%BASE_PYTEST_CMD% %DEBUG_MODE%
if not "%SKIP_LOGIN%"=="" set BASE_PYTEST_CMD=%BASE_PYTEST_CMD% %SKIP_LOGIN%
if not "%VERBOSE%"=="" set BASE_PYTEST_CMD=%BASE_PYTEST_CMD% %VERBOSE%
if "%MAX_FAIL%" neq "0" set BASE_PYTEST_CMD=%BASE_PYTEST_CMD% --maxfail=%MAX_FAIL%
REM NEW: Use FOR /R to find all .py files in the 'tests' directory and its subdirectories
FOR /R "tests" %%F IN (*.py) DO (
    echo.
    echo ------------------------------------------------------------------------------
    echo -- Executing Test File: "%%F"
    echo ------------------------------------------------------------------------------
    
    REM %%~nF extracts just the filename (e.g., "test_login") from the full path %%F
    set "REPORT_PATH=%RESULTS_DIR%\html\report_%%~nF.html"
    
    REM %%F provides the full relative path to the test file (e.g., "tests\auth\test_login.py")
    set "FINAL_CMD=!BASE_PYTEST_CMD! "%%F" --html="!REPORT_PATH!" --self-contained-html"
    
    echo !FINAL_CMD!
    echo.
    
    !FINAL_CMD!
    if !errorlevel! neq 0 (
        echo.
        echo ^>^>^> WARNING: Test file '%%F' failed or contains errors. ^<^<^<
        set MASTER_EXIT_CODE=1
    )
)
REM --- MODIFICATION END ---
set TEST_EXIT_CODE=%MASTER_EXIT_CODE%
goto show_results
REM --- Single Pytest Instance Logic (Original Behavior) ---
:run_single_pytest_instance
echo.
echo [MODE] Running a single test instance with specified filters.
echo.
set PYTEST_CMD=python -m pytest
if not "%TEST_SUITE%"=="" (
    set PYTEST_CMD=%PYTEST_CMD% %TEST_SUITE%
) else (
    set PYTEST_CMD=%PYTEST_CMD% tests/
)
set PYTEST_CMD=%PYTEST_CMD% --device_ip=%DEVICE_IP% --browser chromium --results_dir %RESULTS_DIR% --html=%RESULTS_DIR%\report.html --self-contained-html
if not "%BROWSER_MODE%"=="" set PYTEST_CMD=%PYTEST_CMD% %BROWSER_MODE%
if not "%DEBUG_MODE%"=="" set PYTEST_CMD=%PYTEST_CMD% %DEBUG_MODE%
if not "%SKIP_LOGIN%"=="" set PYTEST_CMD=%PYTEST_CMD% %SKIP_LOGIN%
if not "%TEST_PATTERN%"=="" set PYTEST_CMD=%PYTEST_CMD% %TEST_PATTERN%
if not "%VERBOSE%"=="" set PYTEST_CMD=%PYTEST_CMD% %VERBOSE%
if "%MAX_FAIL%" neq "0" set PYTEST_CMD=%PYTEST_CMD% --maxfail=%MAX_FAIL%
echo Executing: %PYTEST_CMD%
echo.
%PYTEST_CMD%
set TEST_EXIT_CODE=%errorlevel%
goto show_results
REM ==============================================================================
REM == RESULTS AND CLEANUP
REM ==============================================================================
:show_results
echo.
if %TEST_EXIT_CODE%==0 (
    echo ========================================
    echo         TEST EXECUTION COMPLETED
    echo ========================================
    REM Show results summary
    if not "%TEST_PATTERN%"=="" (
         if exist "%RESULTS_DIR%\report.html" echo HTML Report: %RESULTS_DIR%\report.html
    ) else (
         echo Individual HTML Reports are located in: %RESULTS_DIR%\html\
    )
    set SCREENSHOT_COUNT=0
    for %%f in ("%RESULTS_DIR%\screenshots\*.png") do set /a SCREENSHOT_COUNT+=1
    if %SCREENSHOT_COUNT% gtr 0 (
        echo Screenshots: %SCREENSHOT_COUNT% files in %RESULTS_DIR%\screenshots\
    )
    set VIDEO_COUNT=0
    for %%f in ("%RESULTS_DIR%\videos\*.webm") do set /a VIDEO_COUNT+=1
    if %VIDEO_COUNT% gtr 0 (
        echo Videos: %VIDEO_COUNT% files in %RESULTS_DIR%\videos\
    )
    echo All tests completed successfully!
) else (
    echo ========================================
    echo         TEST EXECUTION FAILED
    echo ========================================
    echo One or more tests failed. Check the output above and the generated reports.
)
:cleanup
echo.
if defined VIRTUAL_ENV (
    echo Deactivating virtual environment: %VENV_DIR%
    call "%VENV_DIR%\Scripts\deactivate.bat"
)
exit /b %TEST_EXIT_CODE%
