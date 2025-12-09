
# Category 10: Dashboard Data Extraction Tests

**Test Count**: 12 tests  
**Hardware**: Device Only  
**Priority**: HIGH - The dashboard is the primary interface for monitoring device status.  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 10. This file contains tests that verify the presence and data integrity of the four main tables on the device's dashboard.

---

## 10.1: Dashboard 4-Table Structure

### 10.1.1: All 4 Dashboard Tables Present
- **Purpose**: To verify that the dashboard correctly displays all four main status tables.
- **Expected**: The test locates four `<table>` elements, corresponding to the Status, GNSS, Time Sync, and Alarms tables.

---

## 10.2: Status Table (Table 1) Data Extraction

- **Purpose**: To verify that key information can be extracted from the main status table.
- **Tests**:
    - `10.2.1`: Extract Device Identifier (should be non-empty).
    - `10.2.2`: Extract Location.
    - `10.2.3`: Extract Firmware Version.

---

## 10.3: GNSS Table (Table 2) Data Extraction

- **Purpose**: To verify that key information can be extracted from the GNSS status table.
- **Tests**:
    - `10.3.1`: Extract Satellite Count (should be a non-negative number).
    - `10.3.2`: Extract GNSS Lock Status.

---

## 10.4: Time Sync Table (Table 3) Data Extraction

- **Purpose**: To verify that key information can be extracted from the Time Synchronization status table.
- **Tests**:
    - `10.4.1`: Extract Active Time Source (e.g., GPS, Network).
    - `10.4.2`: Extract Time Synchronization Accuracy (e.g., offset, drift).

---

## 10.5: Alarms Table (Table 4) Data Extraction

- **Purpose**: To verify that alarm information can be extracted from the Alarms table.
- **Tests**:
    - `10.5.1`: Extract the list of active alarms. The test expects that this data can be extracted, even if the list is empty (no active alarms).
    - `10.5.2`: Extract the total count of active alarms.

---

## 10.6: Complete Dashboard Data Extraction

### 10.6.1: Extract Complete Dashboard Data
- **Purpose**: To perform a comprehensive check by extracting data from all four dashboard tables in a single test.
- **Expected**: The test asserts that data can be successfully extracted from all four tables.

### 10.6.2: Dashboard Data Refresh
- **Purpose**: To verify that the dashboard data can be successfully extracted both before and after a page refresh.
- **Expected**: Data extraction should work consistently, confirming that the data loading mechanism is reliable.
