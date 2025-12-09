
# Category 7: Output Configuration Tests

**Test Count**: 10 tests  
**Hardware**: Device Only  
**Priority**: HIGH - Signal output is a critical device function.  
**Series**: Both Series 2 and 3 (with different output counts)  

Based on COMPLETE_TEST_LIST.md Section 7. This file contains tests for the Outputs Configuration page.

**Note**: Series 2 devices have 4 configurable outputs, while Series 3 devices have 6.

---

## 7.1-7.3: Output Type Configuration

- **Purpose**: To verify that the various output signal types can be selected from the configuration dropdowns.

- **Tests**:
    - **7.1.1: PPS (Pulse Per Second) Output**: Verifies that "PPS" or "Pulse" is an available option.
    - **7.2.1: Time Code Output (IRIG-B, etc)**: Verifies that time code formats like "IRIG", "ASCII", or "Time Code" are available.
    - **7.3.1: Frequency Output**: Verifies that frequency options like "MHz", "kHz", or "Hz" are available.

---

## 7.4: Output Channel Count Verification

- **Purpose**: To verify that the correct number of output channels is displayed based on the device series.

- **Tests**:
    - **7.4.1: Series 2 Has 4 Outputs**: Asserts that exactly 4 output configuration dropdowns are present on a Series 2 device.
    - **7.4.2: Series 3 Has 6 Outputs**: Asserts that exactly 6 output configuration dropdowns are present on a Series 3 device.

---

## 7.5-7.6: Output Configuration and Persistence

### 7.5.1: Output Configuration Persists
- **Purpose**: To verify that any changes made to the output configuration are correctly saved and persist after a page reload.

### 7.6.1: Multiple Outputs Configure Independently
- **Purpose**: To verify that each output channel can be configured with a different setting without interfering with the others.
- **Test Steps**: Sets each of the first few outputs to a different available option, saves, reloads, and then asserts that each output has retained its unique configuration.

---

## 7.7: Output Form Controls

### 7.7.1: Output Save Button State Management
- **Purpose**: To verify the correct state management of the "Save" button.
- **Expected**: The button is disabled on page load, becomes enabled when an output type is changed, and becomes disabled again after a successful save.

### 7.7.2: Output Cancel Button Reverts Changes
- **Purpose**: To verify that the "Cancel" button correctly discards any unsaved changes.
- **Expected**: After changing an output, clicking "Cancel" reverts the dropdown to its original, last-saved value.
