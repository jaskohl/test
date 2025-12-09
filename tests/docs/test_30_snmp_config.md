
# SNMP Configuration Tests

**Priority**: MEDIUM  
**Series**: Both Series 2 and 3  

Based on device exploration data from `config_snmp.forms.json`. This file contains tests for the SNMP configuration page.

**IMPORTANT**: The SNMP page has three distinct sections, each with its own "Save" button:
- **Section 1**: v1/v2c read-only communities (`button#button_save_1`)
- **Section 2**: Trap configuration (`button#button_save_2`)
- **Section 3**: v3 authentication (`button#button_save_3`)

---

## SNMP v1/v2c Read-Only Community Configuration

### SNMP Read-Only Community 1 Required Validation
- **Purpose**: To verify that the `ro_community1` field is a required field.
- **Expected**: Leaving the field empty should prevent the form from being saved, either by disabling the save button or by showing a validation error.
- **Series**: Both 2 and 3.

### SNMP Read-Only Community 2 Configuration
- **Purpose**: To verify that a second, optional read-only community string can be configured.
- **Expected**: The `ro_community2` field is present, editable, and accepts a value.
- **Series**: Both 2 and 3.

### SNMP v1/v2c Section Save Button
- **Purpose**: To verify that the v1/v2c section can be saved independently of the other sections.
- **Expected**: The `button#button_save_1` button becomes enabled when a change is made in this section and, upon saving, only affects the v1/v2c settings.
- **Series**: Both 2 and 3.

---

## SNMP Trap Configuration

### SNMP Trap Community String Configuration
- **Purpose**: To verify that the SNMP trap community string can be configured.
- **Expected**: The trap community field is present and accepts input.
- **Series**: Both 2 and 3.

### SNMP Trap Destination IP Configuration
- **Purpose**: To verify that the IP address for the SNMP trap destination can be configured.
- **Expected**: The trap destination field is an IP address field that accepts valid input.
- **Series**: Both 2 and 3.

### SNMP Traps Section Save Button
- **Purpose**: To verify that the traps section can be saved independently.
- **Expected**: The `button#button_save_2` button becomes enabled when a change is made to the trap settings and saves only those settings.
- **Series**: Both 2 and 3.

---

## SNMPv3 Authentication Configuration

### SNMP v3 Enable Configuration
- **Purpose**: To verify that SNMPv3 can be enabled.
- **Expected**: An enable/disable checkbox or a visible section for SNMPv3 configuration is present.
- **Series**: Both 2 and 3.

### SNMP v3 Section Save Button
- **Purpose**: To verify that the v3 section can be saved independently.
- **Expected**: The `button#button_save_3` button becomes enabled when a change is made to the v3 settings and saves only those settings.
- **Series**: Both 2 and 3.

---

## SNMP Multi-Section Independence

### SNMP Sections Save Independently
- **Purpose**: To verify that making a change in one section only enables that section's save button, ensuring the sections are independent.
- **Expected**: When a field in the v1/v2c section is changed, only `button#button_save_1` becomes enabled, while `button#button_save_2` and `button#button_save_3` remain disabled.
- **Series**: Both 2 and 3.
