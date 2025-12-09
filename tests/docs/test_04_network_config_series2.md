
# Category 4: Network Configuration Tests (Series 2)

**Test Count**: 12 tests  
**Hardware**: Device Only  
**Priority**: HIGH - Critical for network connectivity.  
**Series**: Series 2 ONLY  

Based on COMPLETE_TEST_LIST.md Section 4. This file contains tests specifically for the network configuration of Kronos Series 2 devices. Series 3 network tests are in a separate file (`test_29_network_config_series3.py`).

---

## 4.1-4.6: Network Mode Configuration (Series 2)

- **Purpose**: To verify the functionality of the six different network modes available on Series 2 devices.

- **Tests**:
    - **4.1.1: DHCP Mode**: Verifies that when DHCP mode is selected, the static IP and gateway fields are hidden or disabled.
    - **4.2.1: SINGLE Mode**: Verifies that `SINGLE` mode correctly allows for the configuration of a static IP address, netmask, and gateway.
    - **4.3.1: DUAL Mode**: Verifies that `DUAL` mode correctly shows fields for two independent IP addresses and netmasks.
    - **4.4.1: BALANCE-RR Mode**: Verifies the selection of the "Balance Round Robin" bonding mode and that the dual IP fields are visible.
    - **4.5.1: ACTIVE-BACKUP Mode**: Verifies the selection of the "Active-Backup" bonding mode.
    - **4.6.1: BROADCAST Mode**: Verifies the selection of the "Broadcast" bonding mode.

---

## 4.7: Network Field Validation (Series 2)

- **Purpose**: To verify the input validation rules for the network configuration fields.

- **Tests**:
    - **4.7.1: Gateway IP Validation**: Verifies that the gateway field accepts valid IP addresses and rejects invalid ones.
    - **4.7.2: IP Address Field Validation**: Verifies that the main IP address field correctly validates the IP format.
    - **4.7.3: Netmask Field Validation**: Verifies that the netmask field accepts standard, valid subnet masks.

---

## 4.8: Network Form Button Tests (Series 2)

- **Purpose**: To verify the correct behavior of the form control buttons on the network configuration page.

- **Tests**:
    - **4.8.1: Save Button State Management**: Verifies that the "Save" button is disabled initially and becomes enabled only when a change is made to a field.
    - **4.8.2: Cancel Button Reverts Changes**: Verifies that the "Cancel" button correctly reverts all fields to their last saved state.
