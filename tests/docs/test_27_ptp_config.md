
# Category 27: PTP Configuration Tests (Series 3 Only)

**Test Count**: 36 tests total  
- **Variant A**: 25 tests (eth1, eth3 only)
- **Variant B**: 36 tests (eth1, eth2, eth3, eth4)

**Hardware**: Device Only, Variant Specific ()  
**Priority**: HIGH - PTP is a critical feature for Series 3 devices.  
**Series**: Series 3 ONLY  

Based on COMPLETE_TEST_LIST.md Section 27 v4.1.

---

## 27.1: PTP Profile Selection

### 27.1.1: Verify 9 PTP profile options and field state changes
- **Purpose**: To verify that the PTP profile dropdown contains 9 options and that selecting a profile correctly updates the state of other fields.

---

## 27.2: Domain Number Configuration

### 27.2.1: Domain number 0-255 range
- **Purpose**: To verify that the PTP domain number field accepts values within the valid range of 0-255.

---

## 27.3: PTP Priority Configuration

### 27.3.1: Priority 1 field 0-255 range
- **Purpose**: To verify that the `priority_1` field accepts values within the valid range of 0-255.

### 27.3.2: Priority 2 field 0-255 range
- **Purpose**: To verify that the `priority_2` field accepts values within the valid range of 0-255.

---

## 27.4: Timing Intervals Configuration

- **Purpose**: To verify the configuration of various PTP timing interval fields.
- **Tests**:
    - `27.4.1`: Log announce interval
    - `27.4.2`: Log sync interval
    - `27.4.3`: Log min delay req interval
    - `27.4.4`: Announce receipt timeout

---

## 27.5: Delay Mechanism Configuration

### 27.5.1: P2P/E2E delay mechanism selection
- **Purpose**: To verify the selection of the PTP delay mechanism (Peer-to-Peer or End-to-End).

### 27.5.2: Hybrid E2E checkbox configuration
- **Purpose**: To verify the configuration of the Hybrid E2E checkbox.

---

## 27.6: Network Transport Configuration

### 27.6.1: L2/UDPv4 network transport selection
- **Purpose**: To verify the selection of the PTP network transport (Layer 2 or UDPv4).

### 27.6.2: UDP TTL value configuration
- **Purpose**: To verify the configuration of the UDP Time-To-Live (TTL) value.

---

## 27.7: Port Configuration Independence

### 27.7.1: Each PTP port configures independently
- **Purpose**: To verify that the configurations for different PTP ports are independent of each other.

---

## 27.8: Form Save/Cancel Buttons

- **Purpose**: To verify the functionality of the save and cancel buttons for each PTP port's configuration form.
- **Tests**:
    - `27.8.1`: Independent save buttons per port.
    - `27.8.2`: Independent cancel buttons per port.

---

## 27.9: Variant Detection

### 27.9.1: Detect Variant A (2 ports) or B (4 ports)
- **Purpose**: To automatically detect the Series 3 hardware variant (A or B) by inspecting the PTP configuration page.
- **Logic**: Checks for the number of PTP forms (2 for Variant A, 4 for Variant B) and the presence of specific port profiles.

---

## 27.10: Variant B - eth2 and eth4 Tests

These tests are specific to **Variant B** devices.

- **Purpose**: To verify the complete PTP configuration for the `eth2` and `eth4` ports, which are only present on Variant B.
- **Tests**:
    - `27.10.1`: eth2 PTP profile selection
    - `27.10.2`: eth2 domain number
    - `27.10.3`: eth2 priority configuration
    - `27.10.4`: eth2 timing intervals
    - `27.10.5`: eth2 delay mechanism
    - `27.10.6`: eth2 network transport
    - `27.10.7`: eth2 multicast/unicast configuration
    - `27.10.8`: eth2 G.8275 telecom configuration
    - `27.10.9`: eth2 MAC address configuration
    - `27.10.10`: eth2 save/cancel buttons
    - `27.10.11`: eth4 complete PTP configuration (summary test)

---

## 27.11: Variant A Verification

This test is specific to **Variant A** devices.

### 27.11.1: Verify Variant A has only eth1 and eth3
- **Purpose**: To confirm that a Variant A device correctly shows PTP configuration forms for only `eth1` and `eth3`, and not for `eth2` or `eth4`.
