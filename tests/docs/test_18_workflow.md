
# Category 18: Workflow Tests

**Test Count**: 8 tests  
**Hardware**: Device Only  
**Priority**: HIGH - End-to-end workflow validation is critical.  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 18. This file contains tests that validate complete user workflows, from logging in to saving configurations.

---

## 18.1: Complete Configuration Workflow

### 18.1.1: Complete Login to Configuration Workflow
- **Purpose**: To verify the entire end-to-end workflow of logging in, unlocking the configuration, making a change, saving it, and verifying that the change persisted.
- **Workflow**:
    1. **Login**: Authenticate to the device.
    2. **Unlock**: Enter the password again to unlock the configuration sections.
    3. **Configure**: Navigate to a configuration page and change a value.
    4. **Save**: Save the new configuration.
    5. **Verify**: Reload the page and assert that the new value was saved correctly.

### 18.1.2: Multiple Section Configuration Workflow
- **Purpose**: To verify that a user can successfully configure multiple, different sections of the device in a single session.
- **Workflow**:
    1. Configure and save a setting on the "General" page.
    2. Navigate to the "Display" page, configure and save a setting there.
    3. Re-visit both pages to assert that both changes have persisted correctly.

---

## 18.2: Error Recovery Workflow

### 18.2.1: Recovery from Invalid Input
- **Purpose**: To verify that a user can gracefully recover from an input validation error.
- **Workflow**:
    1. Enter invalid data into a field.
    2. Click the "Cancel" button to revert the form to its last known valid state.
    3. Enter a new, valid change.
    4. Save and verify that the new valid change was persisted.

---

## 18.3: Configuration Navigation Workflow

### 18.3.1: Navigate Through All Configuration Sections
- **Purpose**: To ensure that a user can navigate through all available configuration sections without encountering errors or being logged out.
- **Workflow**: Sequentially navigates to every main configuration page and asserts that each page loads correctly by checking for the presence of a key element.

---

## 18.4: Data Persistence Across Sessions

### 18.4.1: Configuration Persists Across Logout/Login
- **Purpose**: To verify that saved configuration settings are persistent and survive a full logout and login cycle.
- **Workflow**:
    1. Log in, unlock, and save a new configuration value.
    2. Simulate a logout by closing the browser context.
    3. Start a new session in a new browser context.
    4. Log in and unlock the configuration again.
    5. Navigate to the page and assert that the value saved in the first session is still present.

---

## 18.5: Rapid Configuration Workflow

### 18.5.1: Rapid Switching Between Sections
- **Purpose**: To test the stability of the system when a user navigates rapidly between different configuration sections.
- **Workflow**: Cycles through a list of configuration pages multiple times with very short delays.
- **Assertion**: Asserts that the session remains stable and the user is not redirected to the authentication page during the rapid navigation.
