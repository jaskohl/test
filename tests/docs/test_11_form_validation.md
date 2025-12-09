
# Category 11: Form Validation Tests

**Test Count**: 15 tests  
**Hardware**: Device Only  
**Priority**: MEDIUM - Input validation is critical for data integrity.  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 11. This file contains tests for form validation rules across all configuration pages.

---

## 11.1: Required Field Validation

### 11.1.1: Required Field Empty Submission Prevention
- **Purpose**: To verify that forms cannot be submitted when a required field is left empty.
- **Expected**: The browser's built-in validation or a server-side check should block the form submission.

---

## 11.2: Maximum Length Validation

- **Purpose**: To verify that text fields correctly enforce their maximum character limits (typically 32 characters).
- **Tests**:
    - `11.2.1`: Identifier field (32 char limit).
    - `11.2.2`: Location field (32 char limit).
    - `11.2.3`: Contact field (32 char limit).
- **Expected**: When a string longer than the limit is entered, the field should either truncate the input or reject the excess characters.

---

## 11.3: IP Address Format Validation

### 11.3.1: Valid IP Address Acceptance
- **Purpose**: To verify that network configuration fields correctly accept standard, valid IPv4 addresses.

### 11.3.2: Invalid IP Address Rejection
- **Purpose**: To verify that fields expecting an IP address reject invalid formats.
- **Expected**: Entering an invalid IP (e.g., `999.999.999.999`, `invalid`, `192.168.1`) should result in a validation error or prevent the form from being saved.

---

## 11.4: Netmask Format Validation

### 11.4.1: Valid Netmask Acceptance
- **Purpose**: To verify that the netmask field accepts standard, valid subnet masks (e.g., `255.255.255.0`).

---

## 11.5: SNMP Community String Validation

### 11.5.1: SNMP Read-Only Community Required
- **Purpose**: To verify that the primary SNMP read-only community string is a required field.
- **Expected**: Leaving the field empty should prevent the SNMP v1/v2c configuration from being saved.

### 11.5.2: SNMP Community String Maximum Length
- **Purpose**: To verify that SNMP community string fields enforce a maximum length (typically 32 characters).

---

## 11.6: Numeric Field Validation

### 11.6.1: Numeric Fields Accept Valid Numbers
- **Purpose**: To verify that fields designed for numeric input correctly accept valid numbers (e.g., the `ant_delay` field).

### 11.6.2: Numeric Fields Reject Non-Numeric Input
- **Purpose**: To verify that numeric fields reject non-numeric characters (e.g., `abc`).
- **Expected**: The field should either block the input or clear the invalid characters, leaving the field empty or with only the numeric part of the input.

---

## 11.7: Decimal Field Validation

### 11.7.1: Decimal Fields Accept Valid Decimal Values
- **Purpose**: To verify that fields designed for decimal values correctly accept decimal notation (e.g., `0.5`, `1.0` in the `low_quality` field).

---

## 11.8: Complete Form Validation

### 11.8.1: Complete Form Validation Workflow
- **Purpose**: To perform an end-to-end test of a form's validation by submitting a complete set of valid data.
- **Expected**: The form is submitted successfully, and the data persists after reloading the page.
