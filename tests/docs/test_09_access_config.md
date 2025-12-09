
# Category 9: Access Configuration Tests

**Test Count**: 4 tests  
**Hardware**: Device Only  
**Priority**: HIGH - Security configuration is critical.  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 9. This file contains tests for the Access Configuration page, which is responsible for changing device passwords.

---

## 9.1-9.2: Password Change Functionality

### 9.1.1: Status Password Change
- **Purpose**: To verify that the password for status monitoring can be changed.
- **Expected**: The test confirms that the password and confirmation fields are present and editable. It does not actually change the password to avoid disrupting other tests.

### 9.2.1: Configuration Password Change
- **Purpose**: To verify that the password for unlocking the configuration can be changed.
- **Expected**: The test confirms that the password and confirmation fields for the configuration password are present and editable.

---

## 9.3: Password Validation Rules

### 9.3.1: Password Confirmation Must Match
- **Purpose**: To verify that the system validates that the new password and the confirmation password match.
- **Expected**: If the two password fields do not match, the "Save" button should either be disabled or, if clicked, should trigger a validation error.

---

## 9.4: Access Form Controls

### 9.4.1: Access Save and Cancel Buttons
- **Purpose**: To verify the functionality of the "Save" and "Cancel" buttons on the access page.
- **Expected**: The test verifies that clicking the "Cancel" button clears any text that has been entered into the password fields.
