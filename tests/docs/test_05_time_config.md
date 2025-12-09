
# Category 5: Time Configuration Tests

**Test Count**: 10 tests  
**Hardware**: Device Only  
**Priority**: HIGH - Critical for time synchronization.  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 5. This file contains tests for the Time Configuration page.

**IMPORTANT**: The Time page has two independent sections, each with its own "Save" button:
- **Section 1**: Timezone configuration (`button#button_save_1`)
- **Section 2**: DST (Daylight Saving Time) configuration (`button#button_save_2`)

---

## 5.1: Timezone Selection and Configuration

- **Purpose**: To verify the configuration of the device's main timezone settings.

- **Tests**:
    - **5.1.1: Timezone Dropdown Selection**: Verifies that the timezone dropdown contains all 16 expected options.
    - **5.1.2: Timezone Offset Field**: Verifies that the manual timezone offset field accepts valid `+/-HH:MM` formats.
    - **5.1.3: Standard Timezone Name**: Verifies that the standard time name field (e.g., "CST") accepts input.
    - **5.1.4: DST Timezone Name**: Verifies that the DST time name field (e.g., "CDT") accepts input.
    - **5.1.5: Timezone Section Independent Save**: Verifies that the timezone section can be saved independently using its own save button and that the settings persist.

---

## 5.2: Daylight Saving Time Configuration

- **Purpose**: To verify the configuration of the device's Daylight Saving Time (DST) rules.

- **Tests**:
    - **5.2.1: DST Rule Selection**: Verifies that the DST rule dropdown contains all 7 predefined rules (e.g., CUSTOM, OFF, USA, etc.).
    - **5.2.2: DST Begin Date Configuration**: Verifies that all fields for setting a custom DST start date (week, day, month, time) are present and configurable.
    - **5.2.3: DST End Date Configuration**: Verifies that all fields for setting a custom DST end date are present and configurable.
    - **5.2.4: DST Section Independent Save**: Verifies that the DST section can be saved independently using its own save button.
    - **5.2.5: Complete Time Configuration Workflow**: A comprehensive test that configures and saves both the timezone and DST sections independently, then reloads the page to ensure both configurations have persisted correctly.
