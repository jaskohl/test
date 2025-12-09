#!/bin/bash
# Note: While this script includes a bash shebang, it aims for POSIX
# compatibility in critical sections. This is because some execution
# environments (e.g., Jenkins CI using /bin/sh by default for shell steps)
# may override the shebang. Key areas, like Python environment setup,
# have been written to avoid bash-specific features to ensure broader
# compatibility.
# Ensure the ORION_IP environment variable is set to the correct IP address before running this script.
# example:
# export device_ip="172.16.66.1"
# sudo chmod +x ./jenkins.sh
# ./jenkins.sh
# --- Configuration Variables ---
# NUMBER_OF_WORKERS: Use proper shell variable assignment
NUMBER_OF_WORKERS=3
# --- Python Configuration (Merged from Original Selenium Script) ---
# Variable to control the Python version
PYTHON_VERSION=${PYTHON_VERSION:-"3.13.2"}
# Extracts major.minor version (e.g., "3.13")
PYTHON_EXEC_VERSION="${PYTHON_VERSION%.*}"
# **RESTORED:** This base path is used by the setup_virtualenv function
# to find the custom-installed Python executable.
PYTHON_INSTALL_BASE="/var/jenkins_home"
# Define the virtual environment directory variables
VENV="./venv/"
# Use the PYTHON_VERSION variable to define the venv path
VENV_PATH="${VENV}Python${PYTHON_VERSION}/"
export TEST_SUITE="./tests"
# -------------------------------
# Function to update the system and install a package if not already installed
# (Using the improved version from your Playwright attempt)
install_package() {
    PACKAGE=$1
    # Check if the package is installed using dpkg
    if ! dpkg -l | grep -q "^ii[[:space:]]\+$PACKAGE[[:space:]]\+"; then
        echo "Installing $PACKAGE..."
        # Add non-interactive flag for silent install
        sudo apt-get install -y "$PACKAGE"
    else
        echo "$PACKAGE is already installed"
    fi
}
# **MODIFIED: Using the setup_virtualenv function from your ORIGINAL Selenium script**
# This function finds the custom Python install and ACTIVATES the venv.
setup_virtualenv() {
    VENV=$1
    VENV_PATH=$2
    
    rm -rdf "$VENV"
    mkdir -p "$VENV"
    
    # Define potential paths for the Python executable within the custom installation
    PYTHON_BIN_DIR="${PYTHON_INSTALL_BASE}/Python-${PYTHON_VERSION}/bin"
    # POSIX-compliant way to check multiple paths
    FOUND_PYTHON_BIN=""
    
    # List potential executable names/paths to check
    potential_path1="${PYTHON_BIN_DIR}/python${PYTHON_EXEC_VERSION}"
    potential_path2="${PYTHON_BIN_DIR}/python3"
    potential_path3="${PYTHON_BIN_DIR}/python"
    if [ -f "$potential_path1" ]; then
        FOUND_PYTHON_BIN="$potential_path1"
    elif [ -f "$potential_path2" ]; then
        FOUND_PYTHON_BIN="$potential_path2"
    elif [ -f "$potential_path3" ]; then
        FOUND_PYTHON_BIN="$potential_path3"
    fi
    # Use the specified python version from the defined absolute path to create the virtual environment
    # Check if the specified Python executable exists before proceeding
    if [ -n "$FOUND_PYTHON_BIN" ]; then
        echo "Using Python executable: $FOUND_PYTHON_BIN"
        "$FOUND_PYTHON_BIN" -m venv "$VENV_PATH"
        
        # **ACTIVATION HAPPENS HERE** (as in your original script)
        if [ -f "${VENV_PATH}bin/activate" ]; then
            . "${VENV_PATH}bin/activate"
        else
            echo "Error: virtualenv activation script not found at ${VENV_PATH}bin/activate"
            exit 1
        fi
    else
        echo "Error: No Python executable found for version ${PYTHON_VERSION} at expected paths within ${PYTHON_BIN_DIR}."
        echo "Searched paths:"
        echo "  1. ${potential_path1}"
        echo "  2. ${potential_path2}"
        echo "  3. ${potential_path3}"
        echo "Please ensure Python ${PYTHON_VERSION} is correctly installed at ${PYTHON_INSTALL_BASE}/Python-${PYTHON_VERSION}/ and its executable is available."
        exit 1 # Exit if no suitable Python executable is found
    fi
}
# Function to install Python packages (runs in the activated VENV)
install_python_packages() {
    # Check if VIRTUAL_ENV is set (set by the activate script)
    if [ -z "$VIRTUAL_ENV" ]; then
        echo "Error: Virtual environment is not active. Cannot install packages."
        exit 1
    fi
    # Use pip from the activated environment
    python -m pip install -r ./requirements.txt || { echo "Failed to install requirements"; exit 1; }
    python -m pip install pytest-cov pytest-html pytest-rerunfailures || { echo "Failed to install testing packages"; exit 1; }
}
# Function to install Playwright browsers (runs in the activated VENV)
install_playwright() {
    echo "Installing Playwright browsers..."
    # Use the 'python' executable from the activated VENV
    python -m playwright install
    # Check the exit status of the previous command ($?)
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install Playwright browsers"
        exit 1
    fi
    echo "Playwright browsers installed successfully."
}
# --- Main script execution ---
echo "--- System Update and Package Installation ---"
sudo apt-get update
# Install necessary packages
install_package wget
install_package unzip
# **FIXED (from your attempt):** Use PYTHON_EXEC_VERSION (e.g., 3.13) to install the correct venv package
install_package "python${PYTHON_EXEC_VERSION}-venv"
install_package python3-pip
# Set up Python virtual environment
echo "--- Setting up and Activating Virtual Environment ---"
# **MODIFIED:** Call the setup/activate function directly, just like in your original script.
# Activation now happens inside this function.
setup_virtualenv "$VENV" "$VENV_PATH"
# Install required Python packages (VENV is now ACTIVE)
echo "--- Installing Python Packages and Playwright Browsers ---"
install_python_packages
# Install Playwright browsers (VENV is now ACTIVE)
install_playwright
# Create necessary directories
# **FIXED:** Changed 'selenium' to 'reports' to match your pytest argument
mkdir -p ./coverage_re
mkdir -p ./reports
# --- Create ARGS and Execute Test ---
echo ""
echo "--- Running Test Suite ---"
echo "Configuration:"
echo "  Device IP: ${device_ip}"
echo "  Browser Mode: ${BROWSER_MODE}"
echo "  Number of Workers: ${NUMBER_OF_WORKERS}"
# **MODIFIED:** Using an array for arguments is safer than 'eval'
PYTEST_ARGS=()
PYTEST_ARGS+=( "$TEST_SUITE" )
PYTEST_ARGS+=( "--device_ip=${device_ip}" )
PYTEST_ARGS+=( "--browser" "chromium" )
PYTEST_ARGS+=( "--html=reports/report.html" )
PYTEST_ARGS+=( "--self-contained-html" )
PYTEST_ARGS+=( "--reruns=2" )
# Conditional additions
if [ -n "$BROWSER_MODE" ] && [ "$BROWSER_MODE" != "--headless" ]; then
    PYTEST_ARGS+=( "$BROWSER_MODE" )
fi
# NUMBER_OF_WORKERS check
if [ "$NUMBER_OF_WORKERS" -ne 0 ]; then
    PYTEST_ARGS+=( "-n" "$NUMBER_OF_WORKERS" )
fi
# Execute tests
echo ""
# The [*] expansion shows the command as a single string for logging
echo "Executing: python -m pytest ${PYTEST_ARGS[*]}"
echo ""
# The [@] expansion correctly passes all array elements as distinct arguments
python -m pytest "${PYTEST_ARGS[@]}"
TEST_EXIT_CODE=$? # Capture the exit code
echo ""
echo "--- Test Execution Result ---"
if [ "$TEST_EXIT_CODE" -eq 0 ]; then
    echo "========================================"
    echo "          TEST EXECUTION COMPLETED     "
    echo "========================================"
    echo "All tests completed successfully!"
else
    echo "========================================"
    echo "          TEST EXECUTION FAILED        "
    echo "========================================"
    echo "One or more tests failed. Exit code: $TEST_EXIT_CODE"
    exit $TEST_EXIT_CODE
fi