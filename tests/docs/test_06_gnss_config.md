
# Category 6: GNSS Configuration Tests

**Test Count**: 15 tests  
**Hardware**: Device Only  
**Priority**: HIGH - GNSS is the primary time source.  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 6. This file contains tests for the GNSS (Global Navigation Satellite System) Configuration page.

**IMPORTANT**: The GNSS page has two independent forms, each with its own "Save" button:
- **Form 1**: Constellation selection (`button#button_save_gnss`)
- **Form 2**: Out-of-Band (OOB) limits (`button#button_save_oob_limits`)

---

## 6.1-6.4: Individual Constellation Tests

- **Purpose**: To verify the selection and configuration of each individual satellite constellation.

- **Tests**:
    - **6.1.1: GPS Checkbox Always Enabled**: Verifies that the GPS checkbox is always present, checked, and disabled, as it is a mandatory constellation.
    - **6.2.1: Galileo Constellation**: Verifies that the Galileo constellation can be enabled or disabled, and that its state persists after saving.
    - **6.3.1: GLONASS Constellation**: Verifies that the GLONASS constellation can be enabled or disabled, and that its state persists after saving.
    - **6.4.1: BeiDou Constellation**: Verifies that the BeiDou constellation can be enabled or disabled, and that its state persists after saving.

---

## 6.5: Multiple Constellation Selection

### 6.5.1: Enable All Constellations Simultaneously
- **Purpose**: To verify that all available constellations can be enabled at the same time without conflicts.
- **Expected**: The test enables all optional constellations, saves, and asserts that they all remain enabled after a page reload.

---

## 6.6: GPS-Only Configuration

### 6.6.1: GPS-Only Operation
- **Purpose**: To verify that the device can operate in a GPS-only mode.
- **Expected**: The test disables all optional constellations, saves, and asserts that only the mandatory GPS constellation remains active.

---

## 6.7-6.8: GNSS Form Controls

### 6.7.1: GNSS Save Button State Management
- **Purpose**: To verify that the save button for the constellation selection form (`button#button_save_gnss`) has correct state management.
- **Expected**: The button is disabled on load and becomes enabled when a constellation checkbox is toggled.

### 6.8.1: GNSS Cancel Button Behavior
- **Purpose**: To verify that the cancel button for the constellation form correctly reverts any unsaved changes.

---

## 6.9: Antenna Delay Configuration

### 6.9.1: Antenna Delay Field Validation
- **Purpose**: To verify the functionality of the antenna/cable delay compensation field.
- **Expected**: The field accepts valid numeric input (representing nanoseconds) and has a default value of "60".

---

## 6.10: Force GNSS Configuration

### 6.10.1: Force GNSS Checkbox
- **Purpose**: To verify the functionality of the `force_gnss` checkbox.

### 6.10.2: Force Time Field
- **Purpose**: To verify that the `force_time` input field is present and accepts time input, which may be used when the `force_gnss` option is enabled.

---

## 6.11: Out-of-Band (OOB) Limits Configuration

- **Purpose**: To verify the configuration of the second form on the page, which controls Out-of-Band signal limits.

- **Tests**:
    - **6.11.1: Low Quality Threshold**: Verifies the signal quality threshold field accepts valid decimal input (e.g., 0.0-1.0).
    - **6.11.2: Bad Time Threshold**: Verifies the time error threshold field accepts valid numeric input.
    - **6.11.3: OOB Limits Save Button Independence**: Verifies that making a change in the OOB form enables only the OOB save button (`button#button_save_oob_limits`), not the main constellation save button.
    - **6.11.4: OOB Limits Cancel Button**: Verifies that the cancel button in the OOB section reverts only the OOB fields.
