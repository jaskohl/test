
# Category 17: Cross-Browser & Responsive Tests

**Test Count**: 6 tests  
**Hardware**: Device Only  
**Priority**: LOW  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 17. This file contains tests for browser compatibility and responsive design.

---

## 17.1-17.3: Browser Compatibility

### 17.1.1: Full functionality in Chromium
- **Purpose**: To verify that the device's web interface is fully functional in Chromium-based browsers (e.g., Google Chrome, Microsoft Edge).
- **Note**: This is the default browser for the test suite, so this test serves as a baseline.

### 17.1.2: Full functionality in Firefox
- **Purpose**: To verify that the device's web interface is fully functional in Mozilla Firefox.
- **Note**: This test is skipped by default as it requires a specific browser configuration to run tests in Firefox.

### 17.1.3: Full functionality in WebKit
- **Purpose**: To verify that the device's web interface is fully functional in WebKit-based browsers (e.g., Apple Safari).
- **Note**: This test is skipped by default as it requires a specific browser configuration to run tests in WebKit.

---

## 17.4-17.6: Responsive Design

### 17.4.1: UI works at 1920x1080 (Desktop)
- **Purpose**: To verify that the UI renders correctly and is fully usable at a standard desktop resolution.
- **Test Steps**: Sets the browser viewport to 1920x1080 and asserts that key UI elements are visible.

### 17.4.2: UI works at 1366x768 (Laptop)
- **Purpose**: To verify that the UI renders correctly and is fully usable at a common laptop resolution.
- **Test Steps**: Sets the browser viewport to 1366x768 and asserts that key UI elements are visible.

### 17.4.3: UI works at 1024x768 (Tablet)
- **Purpose**: To verify that the UI renders correctly and is fully usable at a common tablet resolution.
- **Test Steps**: Sets the browser viewport to 1024x768 and asserts that key UI elements, especially navigation, remain accessible.
