
# Category 13: State Transitions Tests

**Test Count**: 8 tests  
**Hardware**: Device Only  
**Priority**: HIGH - Critical workflow functionality  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 13. This file contains tests for transitions between device states (locked/unlocked, etc).

---

## 13.1: Configuration Lock/Unlock State Transitions

### 13.1.1: Locked to Unlocked State Transition
- **Purpose**: Verify clean transition from locked to unlocked state.
- **Expected**: Configuration sections appear after unlock.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Start in a locked state (logged in but not unlocked).
    2. Attempt to access a configuration page (e.g., `/general`) and verify redirection or locked state.
    3. Click the "Configure" button to bring up the unlock page.
    4. Unlock the configuration using the device password.
    5. After the satellite loading delay, access the `/general` configuration page again.
    6. Assert that the URL is correct and the page is accessible.

### 13.1.2: Session Timeout Returns to Locked State
- **Purpose**: Verify session timeout locks configuration again.
- **Expected**: After timeout, must re-authenticate.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Start in an unlocked state on a configuration page.
    2. Wait for the session to time out (e.g., 5.5 minutes).
    3. Attempt to access the configuration page again.
    4. Assert that the page redirects to the authentication page.
- **Note**: This test is slow and skipped in automated runs.

---

## 13.2: Page Navigation State Management

### 13.2.1: Navigation Between Configuration Pages
- **Purpose**: Verify state is maintained when navigating between configuration pages.
- **Expected**: No re-authentication needed, smooth transitions.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Start in an unlocked state.
    2. Navigate sequentially to multiple configuration pages (`/general`, `/network`, `/time`, `/outputs`).
    3. For each page, assert that the URL is correct and a key element on the page is visible, confirming no re-authentication was required.

### 13.2.2: Dashboard to Configuration Page Transition
- **Purpose**: Verify can navigate from dashboard to configuration pages.
- **Expected**: Smooth transition, no state loss.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Start at the main dashboard.
    2. Navigate to a configuration page (e.g., `/general`).
    3. Assert that the URL is correct and a key element on the configuration page is visible.

### 13.2.3: Configuration Page to Dashboard Transition
- **Purpose**: Verify can return to dashboard from configuration pages.
- **Expected**: Dashboard data visible after returning.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Start on a configuration page.
    2. Navigate back to the main dashboard.
    3. Assert that the dashboard tables are visible.

---

## 13.3: Form State Transitions

### 13.3.1: Form Pristine to Dirty State
- **Purpose**: Verify form state changes when fields are modified.
- **Expected**: Save button enables when form becomes "dirty".
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Load a configuration page with a form.
    2. Assert that the "Save" button is initially disabled (pristine state).
    3. Modify a field in the form.
    4. Assert that the "Save" button becomes enabled (dirty state).

### 13.3.2: Dirty to Pristine State via Cancel
- **Purpose**: Verify cancel button returns form to pristine state.
- **Expected**: Form resets, save button disables.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Modify a field in a form to make it dirty.
    2. Assert that the "Save" button is enabled.
    3. Click the "Cancel" button.
    4. Assert that the field value reverts to its original state and the "Save" button becomes disabled.

### 13.3.3: Dirty to Pristine State via Save
- **Purpose**: Verify save button disables after successful save.
- **Expected**: Form returns to pristine after save.
- **Series**: Both 2 and 3.
- **Test Steps**:
    1. Modify a field in a form to make it dirty.
    2. Assert that the "Save" button is enabled.
    3. Click the "Save" button.
    4. Assert that the "Save" button becomes disabled after the save operation completes.
