
# Category 21: Session & Concurrency Testing

**Test Count**: 3 tests  
**Hardware**: Device Only ()  
**Priority**: MEDIUM  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 21. This file contains tests for session management and concurrency.

---

## 21.1: Concurrent Session Management

### 21.1.1: Multiple browser sessions can access device
- **Purpose**: To verify that the device allows multiple, simultaneous user sessions.
- **Test Steps**:
    1. Creates two separate browser contexts to simulate two different users.
    2. Logs in to the device from both contexts.
- **Assertion**: The test asserts that both sessions can successfully log in and view the main page, confirming that the device supports concurrent sessions.

### 21.1.2: Concurrent configuration changes handling
- **Purpose**: To observe how the device handles concurrent configuration changes from multiple sessions, which typically results in a "last write wins" scenario.
- **Test Steps**:
    1. Creates two separate browser contexts.
    2. Logs in and unlocks the configuration in both sessions.
    3. Navigates both sessions to the same configuration page (e.g., `/display`).
    4. Makes a different change to the same field from each session.
- **Note**: This test demonstrates the behavior of concurrent edits but does not assert a specific outcome, as the expected result is simply that the last change saved will be the one that persists.

---

## 21.2: Session Persistence

### 21.2.1: Session persists across page refresh
- **Purpose**: To verify that a user's session remains active after a page refresh.
- **Test Steps**:
    1. Logs in to the device.
    2. Reloads the current page.
- **Assertion**: The test asserts that the user is still logged in and is not redirected to the authentication page, confirming session persistence.
