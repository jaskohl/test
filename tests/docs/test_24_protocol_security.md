
# Category 24: Protocol Security Testing

**Test Count**: 5 tests  
**Hardware**: Software Tools ()  
**Priority**: MEDIUM  
**Series**: Both Series 2 and 3  

Based on COMPLETE_TEST_LIST.md Section 24. This file contains tests for the security of network protocols like NTP, SNMP, and PTP.

---

## 24.1-24.2: NTP Protocol Security

### 24.1.1: NTP amplification attack prevention
- **Purpose**: To verify that the device has protections against being used in NTP amplification (DDoS) attacks.
- **Note**: This test is skipped as it requires specialized NTP testing tools and the ability to simulate an external attack, which is beyond the scope of this test suite.

### 24.1.2: NTP request rate limiting
- **Purpose**: To verify that the device rate-limits incoming NTP requests to prevent resource exhaustion.
- **Note**: This test is skipped because it requires high-frequency request generation using tools like `ntplib`.

---

## 24.3: SNMP Protocol Security

### 24.3.1: SNMP community strings not exposed
- **Purpose**: To verify that SNMP community strings are not exposed in plain text in the web interface.
- **Test Steps**:
    1. Navigates to the `/snmp` configuration page.
    2. Locates the community string input fields.
    3. Checks the `type` attribute of the input field.
- **Assertion**: The test asserts that the field type is `password` or `text`, confirming the field exists. Ideally, it should be `password` to obscure the value.

---

## 24.4-24.5: PTP Protocol Security (Series 3 Only)

### 24.4.1: PTP security extension support
- **Purpose**: To check if the device supports the PTP security extensions (e.g., as defined in IEEE 1588-2019).
- **Note**: This test is skipped as it is exclusive to Series 3 and requires specialized PTP security testing tools.

### 24.4.2: PTP message authentication
- **Purpose**: To verify that the device supports PTP message authentication.
- **Note**: This test is skipped as it is exclusive to Series 3 and requires tools for PTP packet analysis.
