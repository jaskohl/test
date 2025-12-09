
# Category 8: Display Configuration Tests

**Test Count**: 5 tests  
**Hardware**: Device Only  
**Priority**: MEDIUM - Controls the device's front panel display.  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 8. This file contains tests for the Display Configuration page.

---

## 8.1: Display Mode Configuration

- **Purpose**: To verify the selection and functionality of the various front panel display modes.

- **Tests**:
    - **8.1.1: Display Mode Dropdown**: Verifies that the display mode dropdown is present and contains all 5 expected modes: Status, Time, Date, IP, and Custom.
    - **8.1.2: Status Display Mode**: Verifies that the "Status" mode can be selected and that the setting persists after saving.
    - **8.1.3: Time Display Mode**: Verifies that the "Time" mode can be selected and that the setting persists after saving.
    - **8.1.4: Custom Display Mode**: Verifies that selecting the "Custom" mode correctly reveals a text input field, allowing the user to define a custom message for the display.

---

## 8.2: Display Form Controls

### 8.2.1: Display Save and Cancel Buttons
- **Purpose**: To verify the correct behavior of the "Save" and "Cancel" buttons on the display configuration page.
- **Test Steps**:
    1. Verifies that the "Save" button is disabled on page load.
    2. Changes the display mode and asserts that the "Save" button becomes enabled.
    3. Clicks the "Cancel" button.
    4. Asserts that the display mode reverts to its original, last-saved value.
    5. Asserts that the "Save" button becomes disabled again.
