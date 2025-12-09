
# Category 26: API & Alternative Interface Testing

**Test Count**: 5 tests  
**Hardware**: Conditional (WARNING)
**Priority**: LOW
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 26. This file contains tests for APIs and other non-web interfaces.

---

## 26.1: API and Alternative Interfaces

### 26.1.1: Check if REST API is available
- **Purpose**: To determine if a REST API is available on the device.
- **Test Steps**:
    1. Attempts to navigate to common API endpoints (e.g., `/api`, `/api/v1`, `/rest`).
    2. If a connection is successful and the URL is correct, the test considers the API present.
- **Note**: This test is skipped if no API endpoint is found, as the presence and location of the API are not documented.

### 26.1.2: API authentication mechanism
- **Purpose**: To test the authentication mechanism of the API.
- **Note**: This test is skipped because the API authentication method is not documented.

### 26.1.3: API returns JSON responses
- **Purpose**: To verify that the API returns responses in JSON format.
- **Note**: This test is skipped because the API endpoints are not documented.

### 26.1.4: Command line interface availability
- **Purpose**: To check for the availability of a command-line interface (CLI).
- **Note**: This test is skipped because CLI access would require SSH or telnet, which may not be enabled or accessible in the test environment.

### 26.1.5: Bulk configuration import/export
- **Purpose**: To test the functionality for bulk configuration import and export.
- **Test Steps**:
    1. Navigates to the `/upload` page.
    2. Checks for the presence of a file input element.
- **Note**: This test is skipped. If an upload function is found, it requires a valid configuration file for a manual test. If not found, the feature is considered unavailable through the web interface.
