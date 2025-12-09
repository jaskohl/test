
# Category 28: Syslog Configuration Tests

**Test Count**: 11 tests  
**Hardware**: Device Only  
**Priority**: MEDIUM - System logging configuration  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 28 and device exploration data from `config_syslog.forms.json`.

**Note**: The Syslog page supports two independent syslog targets.

---

## 28.1: Syslog Target 1

### 28.1.1: Syslog Target 1 Enable
- **Purpose**: To verify that the first syslog target can be enabled and disabled.
- **Expected**: The checkbox for the first syslog target toggles its functionality.

### 28.1.2: Syslog Target 1 Server IP
- **Purpose**: To verify the configuration of the syslog server IP address for the first target.
- **Expected**: The input field accepts valid IPv4 addresses.

### 28.1.3: Syslog Target 1 Port Configuration
- **Purpose**: To verify the configuration of the syslog server port for the first target.
- **Expected**: The port field accepts valid port numbers, with a default of 514.

---

## 28.2: Syslog Target 2

### 28.2.1: Second Syslog Target Independent Configuration
- **Purpose**: To verify that the second syslog target can be configured independently of the first.
- **Expected**: The device supports two separate syslog destinations, and enabling/disabling the second does not affect the first.

### 28.2.2: Both Syslog Targets Simultaneously
- **Purpose**: To verify that both syslog targets can be enabled and configured at the same time.
- **Expected**: No conflicts arise, and both targets can be configured with different IP addresses.

---

## 28.3: Syslog Protocol

### 28.3.1: Syslog Protocol Selection (UDP/TCP)
- **Purpose**: To verify that the syslog protocol (UDP or TCP) can be selected.
- **Expected**: A dropdown or radio buttons are available to choose between UDP and/or TCP.

---

## 28.4: Syslog Facility

### 28.4.1: Syslog Facility Selection
- **Purpose**: To verify that the syslog facility code can be configured.
- **Expected**: A dropdown is available with standard syslog facilities (e.g., LOCAL0-LOCAL7).

---

## 28.5: Syslog Severity

### 28.5.1: Syslog Severity Level Selection
- **Purpose**: To verify that the minimum syslog severity level to be logged can be configured.
- **Expected**: A dropdown is available with standard syslog severity levels (e.g., Emergency, Alert, Critical).

---

## 28.6: Syslog Form Controls

### 28.6.1: Syslog Save Button State Management
- **Purpose**: To verify that the "Save" button becomes enabled only when a change is made to the syslog configuration.
- **Expected**: The button is disabled initially and becomes enabled upon a change.

### 28.6.2: Syslog Cancel Button Reverts Changes
- **Purpose**: To verify that the "Cancel" button reverts any unsaved changes.
- **Expected**: All fields return to their previously saved values.

---

## 28.7: Syslog Configuration Persistence

### 28.7.1: Syslog Configuration Persistence
- **Purpose**: To verify that syslog settings persist after being saved and reloading the page.
- **Expected**: The saved configuration is still present after a page reload.
