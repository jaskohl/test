
# Category 1: Authentication & Session Management Tests

**Test Count**: 8 tests  
**Hardware**: Device Only  
**Priority**: CRITICAL - Authentication is the foundation for all other tests.  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 1. This file contains tests for the two main authentication gates: initial login and configuration unlock.

---

## 1.1: Status Monitoring Authentication (Login)

- **Purpose**: To verify the initial login process for status monitoring.

- **Tests**:
    - **1.1.1: Valid Password Login**: Verifies that a user can successfully log in with the correct password.
    - **1.1.2: Invalid Password Error**: Verifies that an appropriate error message is displayed when an incorrect password is used.
    - **1.1.3: Empty Password Submission**: Verifies that submitting an empty password field fails, either through browser validation or a server-side rejection.

---

## 1.2: Configuration Access Authentication (Unlock)

- **Purpose**: To verify the second authentication step required to unlock the device's configuration sections.

- **Tests**:
    - **1.2.1: Valid Password Configuration Unlock**: Verifies that, after logging in, a user can successfully unlock the configuration with the correct password.
    - **1.2.2: Invalid Password Unlock Error**: Verifies that using an incorrect password at the unlock stage results in an error and keeps the configuration locked.

---

## 1.3: Dual Authentication Workflow

### 1.3.1: Complete Dual Authentication Flow
- **Purpose**: To test the entire, two-step authentication process in a single workflow.
- **Expected**: The test asserts that a user can successfully log in and then successfully unlock the configuration, gaining full access to the device settings.

---

## 1.4: Session Management

### 1.4.1: Session Timeout Detection
- **Purpose**: To verify that the user's session automatically times out after a period of inactivity (approximately 5 minutes).
- **Note**: This test is marked as `slow` and is skipped in automated runs. It involves logging in, waiting for 5.5 minutes, and then asserting that any subsequent action redirects to the login page.
