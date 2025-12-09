
# Category 2: Configuration Section Navigation Tests

**Test Count**: 10 tests  
**Hardware**: Device Only  
**Priority**: HIGH - Core navigation functionality is essential.  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 2. This file contains tests to verify that all configuration sections are accessible and that the navigation links function correctly.

---

## 2.1: All Configuration Sections Accessible

- **Purpose**: To verify that each main configuration page can be accessed directly by its URL after the configuration has been unlocked.

- **Tests**:
    - **2.1.1: General Section**: Navigates to `/general` and verifies the page loads.
    - **2.1.2: Network Section**: Navigates to `/network` and verifies the page loads.
    - **2.1.3: Time Section**: Navigates to `/time` and verifies the page loads.
    - **2.1.4: Outputs Section**: Navigates to `/outputs` and verifies the page loads.
    - **2.1.5: GNSS Section**: Navigates to `/gnss` and verifies the page loads.
    - **2.1.6: Display Section**: Navigates to `/display` and verifies the page loads.
    - **2.1.7: SNMP Section**: Navigates to `/snmp` and verifies the page loads.
    - **2.1.8: Syslog Section**: Navigates to `/syslog` and verifies the page loads.
    - **2.1.9: Upload Section**: Navigates to `/upload` and verifies the page loads.
    - **2.1.10: Access Section**: Navigates to `/access` and verifies the page loads.

- **Assertion**: For each test, it asserts that the final URL contains the correct path and that a key, unique element on that page is visible.

---

## 2.2: Navigation Links Functional

### 2.2.1: All Sidebar Navigation Links Functional
- **Purpose**: To verify that clicking each link in the main sidebar navigation menu correctly navigates the user to the corresponding page.
- **Test Steps**:
    1. Iterates through a dictionary of section names and their expected URL paths.
    2. For each section, it finds the link in the sidebar by its text name and clicks it.
    3. Asserts that the browser's current URL matches the expected path for that section.
