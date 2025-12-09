
# Category 3: General Configuration Tests

**Test Count**: 6 tests  
**Hardware**: Device Only  
**Priority**: HIGH - Basic device identification is a fundamental feature.  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 3. This file contains tests for the General Configuration page, which includes the device's main identification fields.

---

## 3.1: General Configuration Field Tests

- **Purpose**: To verify that the main identification fields on the General Configuration page correctly accept and persist new values.

- **Tests**:
    - **3.1.1: Identifier Field**: Enters a new value in the `identifier` field, saves, reloads, and asserts that the new value was saved.
    - **3.1.2: Location Field**: Enters a new value in the `location` field, saves, reloads, and asserts that the new value was saved.
    - **3.1.3: Contact Field**: Enters a new value in the `contact` field, saves, reloads, and asserts that the new value was saved.

---

## 3.2: Field Validation Tests

- **Purpose**: To verify that the text input fields on this page correctly enforce their 32-character maximum length limit.

- **Tests**:
    - **3.2.1: Identifier Maximum Length**: Enters a string longer than 32 characters and asserts that the resulting value is truncated or limited to 32 characters.
    - **3.2.2: Location Maximum Length**: Performs the same length validation for the `location` field.
    - **3.2.3: Contact Maximum Length**: Performs the same length validation for the `contact` field.

---

## 3.3: Save and Cancel Button Tests

### 3.3.1: Save Button State Management
- **Purpose**: To verify the correct state management of the "Save" button.
- **Expected Behavior**:
    1. The button is disabled when the page first loads.
    2. The button becomes enabled after a field's value is changed.
    3. The button becomes disabled again immediately after a successful save.

### 3.3.2: Cancel Button Reverts Changes
- **Purpose**: To verify that the "Cancel" button correctly discards any unsaved changes.
- **Expected Behavior**: After changing a field's value, clicking "Cancel" reverts the field to its original, last-saved value and disables the "Save" button.
