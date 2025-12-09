
# Category 23: Boundary & Input Testing

**Test Count**: 3 tests  
**Hardware**: Device Only ()  
**Priority**: MEDIUM  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 23. This file contains tests for boundary values in input fields.

---

## 23.1: Boundary Value Testing

### 23.1.1: IP address field boundary values
- **Purpose**: To test the handling of boundary values in IP address fields.
- **Test Steps**:
    1. Navigates to the `/network` configuration page.
    2. Enters both valid and invalid boundary values into an IP address field.
    - **Valid**: `0.0.0.0`, `255.255.255.255`, and typical addresses.
    - **Invalid**: Values with segments greater than 255 or negative numbers.
- **Assertion**: The test asserts that valid IPs are accepted and invalid ones are either rejected or trigger a validation error.

### 23.1.2: Numeric field boundaries (domain number 0-255)
- **Purpose**: To test the boundary handling of a numeric field with a defined range, using the PTP domain number (0-255) as an example.
- **Series**: Series 3 Only.
- **Test Steps**:
    1. Navigates to the `/ptp` configuration page.
    2. Enters values at and beyond the expected boundaries into the `domain_number` field.
    - **In-bounds**: `0`, `127`, `255`.
    - **Out-of-bounds**: `-1`, `256`, `999`.
- **Assertion**: The test asserts that valid values are accepted and invalid ones are rejected.

### 23.1.3: Text field maximum length limits
- **Purpose**: To test the maximum length limits of a standard text input field, using the `identifier` field on the general configuration page as an example.
- **Test Steps**:
    1. Navigates to the `/general` configuration page.
    2. Enters a very long string (e.g., 500 characters) into the `identifier` field.
    3. Checks the resulting length of the input value.
- **Assertion**: The test asserts that the input value's length is less than or equal to the string that was entered, confirming that the field either truncates the input or has a maximum length.
