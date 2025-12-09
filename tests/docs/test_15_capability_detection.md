
# Category 15: Device Capability Detection Tests

**Test Count**: 8 tests  
**Hardware**: Device Only  
**Priority**: CRITICAL - These tests are the foundation for conditional test execution.  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 15. This file contains tests designed to detect the specific capabilities and hardware variants of the device under test. The results of these tests are used to conditionally skip or run other tests in the suite.

---

## 15.1: Device Series Detection

### 15.1.1: Detect Device Series from Page Title
- **Purpose**: To determine whether the device is a Kronos Series 2 or Series 3.
- **Detection Logic**: Checks the page title after logging in for the string "Kronos Series 2" or "Kronos Series 3". This is the primary method for distinguishing between the two series.

### 15.1.2: Series 2 Has 4 Outputs
- **Purpose**: To confirm that a device identified as a Series 2 has the expected number of output channels (4).
- **Series**: Series 2 Only.
- **Detection Logic**: Navigates to the Outputs page and asserts that there are 4 output configuration elements.

### 15.1.3: Series 3 Has 6 Outputs
- **Purpose**: To confirm that a device identified as a Series 3 has the expected number of output channels (6).
- **Series**: Series 3 Only.
- **Detection Logic**: Navigates to the Outputs page and asserts that there are 6 output configuration elements.

---

## 15.2: PTP Capability Detection

### 15.2.1: Series 3 Has PTP Configuration
- **Purpose**: To verify that Series 3 devices have PTP (Precision Time Protocol) capability.
- **Series**: Series 3 Only.
- **Detection Logic**: Attempts to navigate to the `/ptp` page and asserts that the page loads and contains PTP configuration elements.

### 15.2.2: Series 2 Does Not Have PTP
- **Purpose**: To verify that Series 2 devices do not have PTP capability.
- **Series**: Series 2 Only.
- **Detection Logic**: Attempts to navigate to the `/ptp` page and asserts that the page is not found (e.g., a 404 error) or redirects, confirming the absence of PTP features.

---

## 15.3: Series 3 Hardware Variant Detection

### 15.3.1: Detect Series 3 PTP Variant (A or B)
- **Purpose**: To determine the specific hardware variant of a Series 3 device by inspecting the PTP configuration page.
- **Series**: Series 3 Only.
- **Detection Logic**:
    - **Variant A**: Has 2 PTP configuration forms (for `eth1` and `eth3`).
    - **Variant B**: Has 4 PTP configuration forms (for `eth1`, `eth2`, `eth3`, and `eth4`).

### 15.3.2: Detect Series 3 Network Variant
- **Purpose**: To determine the Series 3 hardware variant by inspecting the Network configuration page, and to confirm that this matches the PTP variant.
- **Series**: Series 3 Only.
- **Detection Logic**:
    - **Variant A**: Has 5 network forms and a `redundancy_mode` (HSR/PRP) field.
    - **Variant B**: Has 7 network forms and no `redundancy_mode` field.

---

## 15.4: Network Mode Capability Detection

### 15.4.1: Series 2 Network Modes Available
- **Purpose**: To verify that a Series 2 device has the correct set of 6 legacy network modes.
- **Series**: Series 2 Only.
- **Detection Logic**: Navigates to the Network page and asserts that the mode selection dropdown contains exactly 6 options: DHCP, SINGLE, DUAL, BALANCE-RR, ACTIVE-BACKUP, and BROADCAST.
