
# Category 29: Network Configuration Series 3

**Test Count**: 70 tests  
**Hardware**: Device Only, Variant Specific  
**Priority**: HIGH  
**Series**: Series 3 ONLY  

Based on COMPLETE_TEST_LIST.md Section 29 v4.1. This file contains the complete implementation of all 70 tests for the Series 3 network configuration.

---

## Test Structure

This test suite is organized based on the two discovered Series 3 hardware variants:
- **Variant A**: 3 data ports (eth0, eth1, eth3) with HSR/PRP redundancy.
- **Variant B**: 5 data ports (eth0, eth1, eth2, eth3, eth4) without redundancy.
---

## Sections 29.1-29.3: Common Tests (Applicable to Both Variants)

These tests cover network settings that are common to both Series 3 variants.

### 29.1: Gateway Configuration (6 tests)
- **Purpose**: Verify the configuration of the main network gateway.
- **Tests**: Field presence, validation, default value, save/cancel functionality, and persistence.

### 29.2: SFP Mode (5 tests)
- **Purpose**: Verify the configuration of the SFP (Small Form-factor Pluggable) port mode.
- **Tests**: Field presence, options, save/cancel functionality, and persistence.

### 29.3: eth0 Management Port (10 tests)
- **Purpose**: Verify the configuration of the `eth0` management port.
- **Tests**: IP/Netmask, MTU (defaults to 1500), NTP/SNMP service enablement, VLAN configuration, save/cancel, and confirms that PTP is not available on this port.

---

## Section 29.4: Variant A - eth1/eth3 with Redundancy (18 tests)

These tests are specific to **Variant A** devices and verify the unique redundancy features.

### 29.4.1-29.4.9: Variant A eth1 Configuration (9 tests)
- **Purpose**: Verify the full configuration of the `eth1` port on Variant A.
- **Tests**: Redundancy mode (HSR/PRP), IP/Netmask, MTU (defaults to 1494), NTP/PTP/SNMP service enablement, VLAN, and save/cancel.

### 29.4.10-29.4.18: Variant A eth3 Configuration (9 tests)
- **Purpose**: Verify the full configuration of the `eth3` port on Variant A.
- **Tests**: Identical to the `eth1` tests, ensuring both redundant ports are fully configurable.

---

## Sections 29.5-29.6: Port Independence and Variant Detection

### 29.5: Port Independence (1 test)
- **Purpose**: Verify that all network port configurations are independent of each other.
- **Test Steps**: Sets distinct IP addresses on `eth0` and `eth1` and asserts that they do not interfere.

### 29.6: Variant Detection (1 test)
- **Purpose**: Automatically detect the hardware variant (A or B) based on UI elements.
- **Detection Logic**: Checks the number of forms on the network page and the presence/absence of the `redundancy_mode` and `eth2` fields.

---

## Section 29.7: Variant B - eth2/eth4 Configuration (21 tests)

These tests are specific to **Variant B** devices, focusing on the additional `eth2` and `eth4` ports.

### 29.7.1-29.7.10: Variant B eth2 Configuration (10 tests)
- **Purpose**: Verify the full configuration of the `eth2` port on Variant B.
- **Tests**: IP/Netmask, MTU (defaults to 1500), NTP/PTP/SNMP service enablement, VLAN, save/cancel, and confirms that redundancy mode is not present.

### 29.7.11-29.7.21: Variant B eth4 Configuration (11 tests)
- **Purpose**: Verify the full configuration of the `eth4` port on Variant B.
- **Tests**: Identical to the `eth2` tests, and includes a final verification of the MTU pattern (`eth2` and `eth4` are 1500).

---

## Section 29.8: Variant B - eth1/eth3 Without Redundancy (16 tests)

These tests are specific to **Variant B** and verify the configuration of `eth1` and `eth3` without the redundancy features found in Variant A.

### 29.8.1-29.8.8: Variant B eth1 (No Redundancy) (8 tests)
- **Purpose**: Verify the configuration of `eth1` on Variant B.
- **Tests**: Confirms `redundancy_mode` is not present, and tests IP/Netmask, MTU (1494), services, VLAN, and form controls.

### 29.8.9-29.8.14: Variant B eth3 (No Redundancy) (6 tests)
- **Purpose**: Verify the configuration of `eth3` on Variant B.
- **Tests**: Similar to `eth1` tests for Variant B.

### 29.8.15-29.8.16: Variant B Verification (2 tests)
- **Purpose**: Final verification of key Variant B characteristics.
- **Tests**: Confirms `redundancy_mode` is absent on both `eth1` and `eth3`, and verifies the specific, alternating MTU pattern across all data ports (1494, 1500, 1494, 1500).
