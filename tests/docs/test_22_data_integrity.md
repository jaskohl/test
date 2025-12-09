
# Category 22: Data Integrity Testing

**Test Count**: 1 test  
**Hardware**: Device Only ()  
**Priority**: MEDIUM  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 22. This file contains tests for data integrity.

---

## 22.1: Configuration Data Integrity

### 22.1.1: Configuration persists when navigating between pages
- **Purpose**: To verify that configuration changes are saved and persist correctly even after navigating to different pages and then returning.
- **Test Steps**:
    1. Navigates to the `/general` configuration page.
    2. Enters a unique value into the `identifier` field.
    3. Saves the configuration.
    4. Navigates to a different page (e.g., `/network`).
    5. Navigates back to the `/general` page.
- **Assertion**: The test asserts that the value of the `identifier` field is the same as the value that was saved, confirming that the data persisted across page navigations.
