
# Category 25: Time Synchronization Edge Cases

**Test Count**: 5 tests  
**Hardware**: Device Only ()  
**Priority**: MEDIUM  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 25. This file contains tests for edge cases in time synchronization.

---

## 25.1: Time Synchronization Edge Cases

### 25.1.1: Leap second handling in time configuration
- **Purpose**: To verify how the device handles leap seconds.
- **Note**: This test is skipped because leap second handling is typically done automatically by the GNSS receiver and is not manually configurable.

### 25.1.2: Year 2038 problem handling
- **Purpose**: To test the device's resilience to the Year 2038 problem (where 32-bit time representations may overflow).
- **Note**: This test is skipped because it cannot be automated without manipulating the system clock to a future date, which is outside the scope of these tests.

### 25.1.3: DST transition handling
- **Purpose**: To verify how the device handles Daylight Saving Time (DST) transitions.
- **Test Steps**:
    1. Navigates to the `/time` configuration page.
    2. Checks for the presence of a DST enable/disable control.
- **Outcome**: If a DST control is visible and enabled, the test passes, confirming that DST is configurable. If not, the test is skipped.

### 25.1.4: Negative UTC offset handling
- **Purpose**: To ensure the device can correctly handle timezones with negative UTC offsets.
- **Test Steps**:
    1. Navigates to the `/time` configuration page.
    2. Locates the timezone selection dropdown.
    3. Iterates through the available options to find and select a timezone with a negative offset (e.g., "US/Pacific").
- **Outcome**: The test asserts true if a negative offset can be selected, confirming the capability.

### 25.1.5: GNSS signal loss handling
- **Purpose**: To test how the device behaves when it loses the GNSS signal, which is its primary time source.
- **Test Steps**:
    1. Navigates to the main dashboard.
    2. Checks for the presence of GNSS status tables.
- **Note**: This test is skipped because it requires manually blocking the GNSS signal to observe the device's holdover mode, which cannot be done in an automated test.
