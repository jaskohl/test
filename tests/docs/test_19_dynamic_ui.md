
# Category 19: Dynamic UI Behavior & Element Validation

**Test Count**: 52 tests  
**Hardware**: Device Only  
**Priority**: MEDIUM  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 19. This file contains a comprehensive suite of tests for validating the dynamic behavior and visual feedback of the user interface.

---

## 19.1-19.5: Save Button State Management
- **Purpose**: To verify the correct behavior of "Save" buttons throughout the UI.
- **Tests**:
    - `19.1.1`: Save buttons are disabled by default when a page loads.
    - `19.1.2`: A save button becomes enabled when a field value is changed.
    - `19.1.3`: A save button becomes disabled again after a successful save operation.
    - `19.1.4`: On pages with multiple forms, each save button operates independently.
    - `19.1.5`: A save button may remain enabled even if there is a validation error in a field.

---

## 19.2-19.4: Cancel Button Behavior
- **Purpose**: To verify the correct behavior of "Cancel" buttons.
- **Tests**:
    - `19.2.1`: Cancel buttons are always enabled.
    - `19.2.2`: Clicking "Cancel" reverts any changes made to the form fields.
    - `19.2.3`: Clicking "Cancel" disables the corresponding "Save" button.

---

## 19.3-19.8: Field Interaction Behaviors
- **Purpose**: To verify standard UI interactions for various form fields.
- **Tests**:
    - `19.3.1`: Text fields show a visual highlight (focus) when selected.
    - `19.3.2`: Dropdown menus open when clicked.
    - `19.3.3`: Checkboxes toggle their state when clicked.
    - `19.3.4`: Read-only (disabled) fields cannot be edited.
    - `19.3.5`: Disabled fields have a distinct visual style.
    - `19.3.6`: Required fields are visually marked.

---

## 19.4-19.9: Validation Feedback
- **Purpose**: To verify that the UI provides clear feedback for input validation.
- **Tests**:
    - `19.4.1`: Entering an invalid IP address provides error feedback.
    - `19.4.2`: Leaving a required field empty provides error feedback.
    - `19.4.3`: A validation error message is cleared once the user corrects the invalid input.

---

## 19.5-19.15: Dynamic Field Behaviors
- **Purpose**: To test UI elements that dynamically change based on other selections.
- **Tests**:
    - `19.5.1`: On the PTP page, changing the profile to "Custom" makes other fields editable.
    - `19.5.2`: On the Network page, enabling VLAN may show or enable the VLAN ID and priority fields.
    - `19.5.3`: On the Network page, changing the network mode may change which fields are visible.

---

## 19.6-19.10: Table UI Behaviors
- **Purpose**: To verify the behavior of data tables in the UI.
- **Tests**:
    - `19.6.1`: Table rows can be selected.
    - `19.6.2`: Table data updates dynamically (e.g., on page refresh).
    - `19.6.3`: Table column headers are always visible.

---

## 19.7-19.12: Navigation UI Behaviors
- **Purpose**: To verify the visual feedback and behavior of the main navigation menu.
- **Tests**:
    - `19.7.1`: The currently active navigation item is visually highlighted.
    - `19.7.2`: All navigation items are clickable and lead to the correct page.
    - `19.7.3`: Navigation items show a visual hover effect.

---

## 19.8-19.15: Loading State Indicators
- **Purpose**: To verify that the UI provides feedback during loading operations.
- **Tests**:
    - `19.8.1`: A loading indicator is shown during a save operation.
    - `19.8.2`: A loading indicator is shown during page navigation.
    - `19.8.3`: The loading indicator is removed after the operation is complete.

---

## 19.9-19.12: Tooltips and Help Text
- **Purpose**: To verify the presence of helpful tooltips.
- **Tests**:
    - `19.9.1`: Tooltips appear when hovering over form fields.
    - `19.9.2`: Tooltips appear when hovering over buttons.

---

## 19.10-19.15: Accessibility Features
- **Purpose**: To verify basic accessibility features.
- **Tests**:
    - `19.10.1`: The "Tab" key correctly navigates between form fields.
    - `19.10.2`: The "Enter" key can be used to submit forms.
    - `19.10.3`: The "Escape" key can be used to close dialogs or modals.
