
# Category 12: Error Handling Tests

**Test Count**: 12 tests  
**Hardware**: Device Only  
**Priority**: HIGH - Proper error handling is critical for reliability.  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 12.

---

## 12.1: Authentication Error Handling

### 12.1.1: Invalid Login Password Error Message
- **Purpose**: Verify that an appropriate error is displayed upon entering an invalid login password.
- **Expected**: A clear error message is shown, and the login form remains accessible for another attempt.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Navigate to the login page.
    2. Attempt to log in with an incorrect password.
    3. Assert that the login fails.
    4. Check for and assert that an authentication error message is displayed.

### 12.1.2: Invalid Configuration Password Error
- **Purpose**: Verify that an error is shown when an invalid password is used to unlock the configuration.
- **Expected**: An error message is displayed, and the device configuration remains locked.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Log in successfully.
    2. Attempt to unlock the configuration with an incorrect password.
    3. Assert that the unlock operation fails.

---

## 12.2: Network Configuration Error Handling

### 12.2.1: Invalid IP Address Error Handling
- **Purpose**: Verify the system's error handling for invalid IP address formats.
- **Expected**: The system prevents saving the configuration or displays a clear validation error message.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Navigate to the network configuration page.
    2. Enter an invalid IP address (e.g., "999.999.999.999").
    3. Fill other required fields with valid data.
    4. Attempt to save the configuration.
    5. Assert that the save is either prevented or an error is indicated.

### 12.2.2: Missing Required Gateway Error
- **Purpose**: Verify that an error occurs when the required gateway field is left empty.
- **Expected**: The system prevents saving the configuration due to the missing required field.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Navigate to the network configuration page.
    2. Clear the gateway field.
    3. Fill other required fields with valid data.
    4. Assert that browser validation or a server-side check prevents the form from being saved.

---

## 12.3: SNMP Configuration Error Handling

### 12.3.1: Empty SNMP Community String Error
- **Purpose**: Verify that an error is triggered when a required SNMP community string is left empty.
- **Expected**: The system prevents saving or displays an error message.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Navigate to the SNMP configuration page.
    2. Clear a required community string field.
    3. Attempt to save the configuration.
    4. Assert that the save button is disabled or an error is shown upon clicking.

### 12.3.2: Invalid SNMP Trap Destination Error
- **Purpose**: Verify error handling for an invalid SNMP trap destination IP address.
- **Expected**: The system prevents saving the configuration with an invalid IP.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Navigate to the SNMP configuration page.
    2. Enter an invalid IP address in a trap destination field.
    3. Attempt to save the configuration.
    4. Assert that a validation error is displayed.

---

## 12.4: Error Recovery Mechanisms

### 12.4.1: Error Recovery Using Cancel Button
- **Purpose**: Verify that the "Cancel" button correctly recovers the form from a validation error state.
- **Expected**: Clicking "Cancel" clears any validation errors and reverts the form to its last valid state.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. On a configuration page, note the original, valid data.
    2. Enter invalid data into a field (e.g., a value that exceeds the maximum length).
    3. Click the "Cancel" button.
    4. Assert that the field reverts to its original, valid value.

### 12.4.2: Page Reload Clears Error State
- **Purpose**: Verify that reloading the page recovers the form from an error state.
- **Expected**: A fresh page load displays the last saved valid state, not the unsaved invalid entries.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Enter invalid data into a form field.
    2. Reload the page.
    3. Assert that the field displays its last saved valid value, not the unsaved invalid one.

---

## 12.5: Concurrent Operation Error Handling

### 12.5.1: Multiple Field Validation Errors
- **Purpose**: Verify the system's ability to handle multiple validation errors at the same time.
- **Expected**: All errors are clearly indicated, providing comprehensive feedback to the user.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Navigate to a configuration page.
    2. Enter invalid data into multiple fields simultaneously.
    3. Attempt to save the configuration.
    4. Assert that multiple errors are indicated (specific implementation may vary).

---

## 12.6: Error Message Quality

### 12.6.1: Error Messages Are Descriptive
- **Purpose**: Verify that error messages are clear, specific, and descriptive.
- **Expected**: Error messages should explain the problem specifically, rather than showing a generic "Error" message.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Trigger a validation error (e.g., clear a required field).
    2. Attempt to save the form.
    3. Inspect the resulting error message to ensure it is descriptive.
    4. This test focuses on the capability to detect and report errors clearly.
