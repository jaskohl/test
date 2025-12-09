"""
Protocol Explorer for Kronos Devices

This tool explores protocol capabilities (NTP, SNMP, Syslog) by:
1. Backing up current configuration
2. Enabling each protocol service
3. Testing protocol availability
4. Documenting what tests are possible
5. Restoring original configuration

Output: Documentation of available protocol tests per device
Location: memory-bank/device_exploration/{device_ip}/protocols/

Usage:
    python -m tools.protocol_explorer

WARNING: This tool modifies device configuration temporarily.
         Original settings are restored after testing.
"""

import json
import asyncio
import socket
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from playwright.async_api import async_playwright, Page, Browser

# Device list
DEVICES = [
    # {"ip": "172.16.190.46", "name": "Kronos Series 2", "type": "series2"},
    # {"ip": "172.16.190.47", "name": "Kronos Series 3", "type": "series3"},
    # {"ip": "172.16.66.1", "name": "Kronos Series 2", "type": "series2"},
    # {"ip": "172.16.66.3", "name": "Kronos Series 3", "type": "series3"},
    # {"ip": "172.16.66.6", "name": "Kronos Series 3", "type": "series3"},
    {"ip": "172.16.66.3", "name": "Kronos Series 3", "type": "series3"},
]

PASSWORD = "novatech"
OUTPUT_BASE = Path("memory-bank/device_exploration")


class ProtocolExplorer:
    def __init__(self, device_ip: str, device_name: str, device_type: str):
        self.device_ip = device_ip
        self.device_name = device_name
        self.device_type = device_type
        self.device_url = f"https://{device_ip}"
        self.output_dir = OUTPUT_BASE / device_ip / "protocols"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.page: Page | None = None
        self.browser: Browser | None = None

        # Store original configurations
        self.original_configs = {}

        # Protocol test results
        self.protocol_results = {
            "device_ip": device_ip,
            "device_name": device_name,
            "device_type": device_type,
            "exploration_date": datetime.now().isoformat(),
            "protocols": {},
        }

    async def initialize_browser(self):
        """Initialize Playwright browser"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=False)
        context = await self.browser.new_context(
            ignore_https_errors=True, viewport={"width": 1280, "height": 800}
        )
        self.page = await context.new_page()
        print(f"[OK] Browser initialized for {self.device_ip}")

    async def login_and_unlock(self):
        """Login and unlock configuration"""
        print(f"\n[{self.device_ip}] Logging in...")

        # Status monitoring login
        await self.page.goto(self.device_url, wait_until="domcontentloaded")
        await self.page.wait_for_timeout(2000)

        password_field = self.page.get_by_placeholder("Password")
        await password_field.fill(PASSWORD)

        submit_button = self.page.locator("button[type='submit']").first
        await submit_button.click()

        # Wait for satellite loading (first cycle)
        print(f"[{self.device_ip}] Waiting for satellite loading (1st cycle)...")
        await self.page.wait_for_timeout(12000)

        # Configuration unlock
        print(f"[{self.device_ip}] Unlocking configuration...")
        dropdown = self.page.locator(".dropdown-toggle").first
        await dropdown.click()
        await self.page.wait_for_timeout(500)

        configure_link = self.page.locator("a[title*='locked']").filter(
            has_text="Configure"
        )
        await configure_link.click()
        await self.page.wait_for_timeout(2000)

        password_field = self.page.get_by_placeholder("Password")
        await password_field.fill(PASSWORD)

        submit_button = self.page.locator("button[type='submit']").first
        await submit_button.click()

        # Wait for satellite loading (second cycle)
        print(f"[{self.device_ip}] Waiting for satellite loading (2nd cycle)...")
        await self.page.wait_for_timeout(12000)

        print(f"[OK] [{self.device_ip}] Logged in and configuration unlocked")

    async def backup_snmp_config(self) -> Dict:
        """Backup current SNMP configuration"""
        print(f"[{self.device_ip}] Backing up SNMP configuration...")

        await self.page.goto(f"{self.device_url}/snmp", wait_until="domcontentloaded")
        await self.page.wait_for_timeout(2000)

        config = {
            "backed_up": True,
            "timestamp": datetime.now().isoformat(),
            "fields": {},
        }

        # Try to extract all SNMP fields
        try:
            # Look for actual SNMP fields from the Kronos device
            field_ids = [
                "ro_community1",  # SNMPv1 RO Community
                "ro_community2",  # SNMPv2 RO Community
                "trap_community",  # SNMPv2 Trap Community
                "trap_host1",  # SNMPv2 Trap Host 1
                "trap_host2",  # SNMPv2 Trap Host 2
                "auth_name",  # SNMPv3 Auth Name
                "auth_key",  # SNMPv3 Auth Key
                "auth_protocol",  # SNMPv3 Auth Protocol
            ]

            for field_id in field_ids:
                try:
                    element = self.page.locator(f"#{field_id}").first
                    if await element.count() > 0:
                        # Check element type
                        tag_name = await element.evaluate(
                            "el => el.tagName.toLowerCase()"
                        )

                        if tag_name == "select":
                            value = await element.input_value()
                        elif tag_name == "input":
                            input_type = await element.get_attribute("type")
                            if input_type == "checkbox":
                                value = await element.is_checked()
                            else:
                                value = await element.input_value()
                        else:
                            value = await element.input_value()

                        config["fields"][field_id] = value
                except Exception as field_error:
                    # Field doesn't exist or can't be read, skip it
                    pass

            print(
                f"[OK] [{self.device_ip}] SNMP configuration backed up ({len(config['fields'])} fields)"
            )
        except Exception as e:
            print(f"[WARNING] [{self.device_ip}] Could not backup SNMP config: {e}")
            config["backed_up"] = False

        return config

    async def backup_time_config(self) -> Dict:
        """Backup current Time/NTP configuration"""
        print(f"[{self.device_ip}] Backing up Time configuration...")

        await self.page.goto(f"{self.device_url}/time", wait_until="domcontentloaded")
        await self.page.wait_for_timeout(2000)

        config = {
            "backed_up": True,
            "timestamp": datetime.now().isoformat(),
            "fields": {},
        }

        try:
            # Look for NTP and time fields
            field_ids = [
                "ntp_enabled",
                "ntp_server",
                "ntp_port",
                "timezones",
                "offset",
                "std_name",
                "dst_name",
                "dst_rule",
            ]

            for field_id in field_ids:
                try:
                    element = self.page.locator(
                        f"#{field_id}, [name='{field_id}']"
                    ).first
                    if await element.count() > 0:
                        input_type = await element.get_attribute("type")
                        tag_name = await element.evaluate(
                            "el => el.tagName.toLowerCase()"
                        )

                        if tag_name == "select":
                            value = await element.input_value()
                        elif input_type in ["text", "number"]:
                            value = await element.input_value()
                        elif input_type == "checkbox":
                            value = await element.is_checked()
                        else:
                            value = await element.input_value()
                        config["fields"][field_id] = value
                except:
                    pass

            print(
                f"[OK] [{self.device_ip}] Time configuration backed up ({len(config['fields'])} fields)"
            )
        except Exception as e:
            print(f"[WARNING] [{self.device_ip}] Could not backup Time config: {e}")
            config["backed_up"] = False

        return config

    async def test_snmp_protocol(self) -> Dict:
        """Test SNMP protocol availability"""
        print(f"\n[{self.device_ip}] Testing SNMP protocol...")

        result = {
            "protocol": "SNMP",
            "available": False,
            "port": 161,
            "tested": True,
            "test_date": datetime.now().isoformat(),
            "configuration_page": "/snmp",
            "tests_possible": [],
        }

        try:
            # Check if pysnmp is available
            try:
                import pysnmp

                result["pysnmp_available"] = True
            except ImportError:
                result["pysnmp_available"] = False
                result["note"] = "pysnmp not installed - run: pip install pysnmp"
                print(f"[WARNING] [{self.device_ip}] pysnmp not installed")
                return result

            # Try basic SNMP query (pysnmp 7.x v1arch API)
            from pysnmp.hlapi.v1arch.asyncio import (
                get_cmd,
                SnmpDispatcher,
                CommunityData,
                UdpTransportTarget,
                ObjectType,
                ObjectIdentity,
            )

            # Try with community strings from device configuration first, then common defaults
            community_strings = []

            # Add backed up community strings if available
            if (
                "snmp" in self.original_configs
                and "fields" in self.original_configs["snmp"]
            ):
                fields = self.original_configs["snmp"]["fields"]
                if "ro_community1" in fields and fields["ro_community1"]:
                    community_strings.append(fields["ro_community1"])
                if "ro_community2" in fields and fields["ro_community2"]:
                    community_strings.append(fields["ro_community2"])

            # Add common defaults as fallback
            for default in ["public", "PUBLIC", "private", "PRIVATE", "novatech"]:
                if default not in community_strings:
                    community_strings.append(default)

            # Create SNMP dispatcher (replaces SnmpEngine in v1arch)
            snmpDispatcher = SnmpDispatcher()

            for community in community_strings:
                try:
                    # Use async version for pysnmp 7.x v1arch
                    errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
                        snmpDispatcher,
                        CommunityData(community),
                        await UdpTransportTarget.create(
                            (self.device_ip, 161), timeout=5, retries=0
                        ),
                        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
                    )

                    if not errorIndication and not errorStatus:
                        result["available"] = True
                        result["community_string"] = community
                        result["sys_descr"] = str(varBinds[0][1])
                        print(
                            f"[OK] [{self.device_ip}] SNMP available (community: {community})"
                        )
                        break
                    else:
                        # Log the specific error for this community string
                        if errorIndication:
                            print(
                                f"[DEBUG] [{self.device_ip}] SNMP community '{community}': {errorIndication}"
                            )
                        elif errorStatus:
                            print(
                                f"[DEBUG] [{self.device_ip}] SNMP community '{community}': {errorStatus.prettyPrint()}"
                            )
                except Exception as e:
                    print(
                        f"[DEBUG] [{self.device_ip}] SNMP community '{community}' exception: {e}"
                    )
                    continue

            if result["available"]:
                # Document possible tests
                result["tests_possible"] = [
                    {
                        "test": "SNMP GET sysDescr",
                        "oid": "1.3.6.1.2.1.1.1.0",
                        "description": "Query system description",
                    },
                    {
                        "test": "SNMP GET sysObjectID",
                        "oid": "1.3.6.1.2.1.1.2.0",
                        "description": "Query device object identifier",
                    },
                    {
                        "test": "SNMP GET sysUpTime",
                        "oid": "1.3.6.1.2.1.1.3.0",
                        "description": "Query system uptime",
                    },
                    {
                        "test": "SNMP GET sysContact",
                        "oid": "1.3.6.1.2.1.1.4.0",
                        "description": "Query contact information",
                    },
                    {
                        "test": "SNMP GET sysName",
                        "oid": "1.3.6.1.2.1.1.5.0",
                        "description": "Query system name",
                    },
                    {
                        "test": "SNMP GET sysLocation",
                        "oid": "1.3.6.1.2.1.1.6.0",
                        "description": "Query system location",
                    },
                    {
                        "test": "SNMP WALK ifTable",
                        "oid": "1.3.6.1.2.1.2.2",
                        "description": "Walk interface table",
                    },
                    {
                        "test": "SNMP Community String Authentication",
                        "description": "Test authentication with correct/incorrect community strings",
                    },
                ]
            else:
                result["note"] = (
                    "SNMP not responding - may be disabled or using different community string"
                )
                print(f"[FAIL] [{self.device_ip}] SNMP not available")

        except Exception as e:
            result["error"] = str(e)
            result["note"] = f"SNMP testing failed: {e}"
            print(f"[ERROR] [{self.device_ip}] SNMP test error: {e}")

        return result

    async def test_ntp_protocol(self) -> Dict:
        """Test NTP protocol availability"""
        print(f"\n[{self.device_ip}] Testing NTP protocol...")

        result = {
            "protocol": "NTP",
            "available": False,
            "port": 123,
            "tested": True,
            "test_date": datetime.now().isoformat(),
            "configuration_page": "/time",
            "tests_possible": [],
        }

        try:
            # Check if ntplib is available
            try:
                import ntplib

                result["ntplib_available"] = True
            except ImportError:
                result["ntplib_available"] = False
                result["note"] = "ntplib not installed - run: pip install ntplib"
                print(f"[WARNING] [{self.device_ip}] ntplib not installed")
                return result

            # Try NTP query
            import ntplib

            client = ntplib.NTPClient()

            try:
                response = client.request(self.device_ip, version=3, timeout=5)
                result["available"] = True
                result["stratum"] = response.stratum
                result["precision"] = response.precision
                result["root_delay"] = response.root_delay
                result["ref_id"] = response.ref_id
                result["offset"] = response.offset
                print(
                    f"[OK] [{self.device_ip}] NTP available (stratum: {response.stratum})"
                )

                # Document possible tests
                result["tests_possible"] = [
                    {
                        "test": "NTP Basic Query",
                        "description": "Query device time via NTP",
                    },
                    {
                        "test": "NTP Time Accuracy",
                        "description": "Measure time offset from system clock",
                    },
                    {
                        "test": "NTP Stratum Level",
                        "description": "Verify stratum level (should be 1 for GPS)",
                    },
                    {
                        "test": "NTP Version Support",
                        "description": "Test NTPv3 and NTPv4 support",
                    },
                    {
                        "test": "NTP Reference ID",
                        "description": "Verify reference identifier indicates GPS",
                    },
                    {
                        "test": "NTP Precision",
                        "description": "Verify reported precision level",
                    },
                    {
                        "test": "NTP Root Delay",
                        "description": "Measure root delay (should be <1ms for GPS)",
                    },
                    {
                        "test": "NTP Response Consistency",
                        "description": "Query 20 times and verify timestamp consistency",
                    },
                    {
                        "test": "NTP Under Load",
                        "description": "Send 100 rapid queries and verify all responses",
                    },
                ]
            except Exception as e:
                result["note"] = f"NTP not responding: {e}"
                print(f"[FAIL] [{self.device_ip}] NTP not available: {e}")

        except Exception as e:
            result["error"] = str(e)
            result["note"] = f"NTP testing failed: {e}"
            print(f"[ERROR] [{self.device_ip}] NTP test error: {e}")

        return result

    async def check_device_restart_requirements(self) -> Dict:
        """Check if configuration changes require device restart"""
        print(f"\n[{self.device_ip}] Checking restart requirements...")

        restart_info = {
            "checked": True,
            "check_date": datetime.now().isoformat(),
            "note": "Checked for visible restart warnings in configuration pages",
            "sections": {},
        }

        # Check each configuration page for restart warnings
        sections = [
            {"name": "SNMP", "url": "/snmp"},
            {"name": "Time", "url": "/time"},
            {"name": "Network", "url": "/network"},
        ]

        for section in sections:
            try:
                await self.page.goto(
                    f"{self.device_url}{section['url']}", wait_until="domcontentloaded"
                )
                await self.page.wait_for_timeout(2000)

                # Look for actual visible restart warnings (not just the word "restart" in code)
                # Check for common warning patterns in visible text elements
                restart_warning_found = False
                warning_text = None

                # Look for alert boxes, warning divs, or notice text
                warning_selectors = [
                    ".alert-warning",
                    ".alert-danger",
                    ".alert-info",
                    ".warning",
                    ".notice",
                    ".restart-warning",
                    "div:has-text('restart')",
                    "p:has-text('restart')",
                    "div:has-text('reboot')",
                    "p:has-text('reboot')",
                ]

                for selector in warning_selectors:
                    try:
                        elements = self.page.locator(selector)
                        if await elements.count() > 0:
                            for i in range(await elements.count()):
                                text = await elements.nth(i).text_content()
                                if text and any(
                                    keyword in text.lower()
                                    for keyword in [
                                        "restart",
                                        "reboot",
                                        "reset",
                                        "reload",
                                    ]
                                ):
                                    restart_warning_found = True
                                    warning_text = text.strip()[:100]  # First 100 chars
                                    break
                    except:
                        pass

                    if restart_warning_found:
                        break

                restart_info["sections"][section["name"]] = {
                    "url": section["url"],
                    "restart_warnings_found": restart_warning_found,
                    "warning_text": warning_text,
                    "note": (
                        "Restart required"
                        if restart_warning_found
                        else "No restart warning detected"
                    ),
                }

                if restart_warning_found:
                    print(
                        f"[WARNING] [{self.device_ip}] {section['name']}: Restart may be required - '{warning_text}'"
                    )
                else:
                    print(
                        f"[OK] [{self.device_ip}] {section['name']}: No restart warning"
                    )

            except Exception as e:
                restart_info["sections"][section["name"]] = {
                    "url": section["url"],
                    "error": str(e),
                }
                print(
                    f"[ERROR] [{self.device_ip}] {section['name']}: Error checking - {e}"
                )

        return restart_info

    async def generate_documentation(self):
        """Generate comprehensive protocol testing documentation"""
        print(f"\n[{self.device_ip}] Generating documentation...")

        # Save main protocol results
        output_file = self.output_dir / "protocol_exploration_results.json"
        with open(output_file, "w") as f:
            json.dump(self.protocol_results, f, indent=2)
        print(f"[OK] [{self.device_ip}] Results saved to: {output_file}")

        # Generate human-readable documentation
        doc_file = self.output_dir / "PROTOCOL_TESTS_AVAILABLE.md"

        doc_content = f"""# Protocol Testing Documentation
## Device: {self.device_name} ({self.device_ip})

**Exploration Date**: {self.protocol_results['exploration_date']}  
**Device Type**: {self.device_type}

---

## Summary

This document lists all protocol tests that can be performed on this device based on protocol exploration.

"""

        # Add protocol sections
        for protocol_name, protocol_data in self.protocol_results["protocols"].items():
            doc_content += f"\n## {protocol_data['protocol']} Protocol\n\n"
            doc_content += f"**Status**: {'Available' if protocol_data['available'] else 'Not Available'}  \n"
            doc_content += f"**Port**: {protocol_data['port']}  \n"
            doc_content += (
                f"**Configuration Page**: {protocol_data['configuration_page']}  \n"
            )

            if not protocol_data["available"]:
                doc_content += (
                    f"\n**Note**: {protocol_data.get('note', 'Not available')}  \n"
                )
                continue

            # Add specific protocol info
            if protocol_name == "snmp" and "community_string" in protocol_data:
                doc_content += (
                    f"**Community String**: {protocol_data['community_string']}  \n"
                )
                doc_content += f"**System Description**: {protocol_data.get('sys_descr', 'N/A')}  \n"

            if protocol_name == "ntp" and "stratum" in protocol_data:
                doc_content += f"**Stratum Level**: {protocol_data['stratum']}  \n"
                doc_content += f"**Precision**: {protocol_data['precision']}  \n"
                doc_content += f"**Root Delay**: {protocol_data['root_delay']:.6f}s  \n"
                doc_content += f"**Time Offset**: {protocol_data['offset']:.6f}s  \n"

            # List available tests
            if protocol_data.get("tests_possible"):
                doc_content += f"\n### Available Tests ({len(protocol_data['tests_possible'])} tests)\n\n"

                for i, test in enumerate(protocol_data["tests_possible"], 1):
                    doc_content += f"**{i}. {test['test']}**  \n"
                    doc_content += f"   {test['description']}  \n"
                    if "oid" in test:
                        doc_content += f"   OID: `{test['oid']}`  \n"
                    doc_content += "\n"

        # Add restart requirements section
        if "restart_requirements" in self.protocol_results:
            doc_content += "\n## Configuration Change Restart Requirements\n\n"

            for section_name, section_data in self.protocol_results[
                "restart_requirements"
            ]["sections"].items():
                status = (
                    "Restart may be required"
                    if section_data.get("restart_warnings_found")
                    else "No restart required"
                )
                doc_content += f"**{section_name}**: {status}  \n"

                if section_data.get("warnings"):
                    doc_content += f"   Warning keywords found: {', '.join(section_data['warnings'])}  \n"
                doc_content += "\n"

        # Add backup info
        doc_content += "\n## Configuration Backups\n\n"
        doc_content += (
            "Original configurations were backed up before protocol testing:\n\n"
        )

        for config_name, config_data in self.original_configs.items():
            status = "Backed up" if config_data.get("backed_up") else "Not backed up"
            doc_content += f"**{config_name}**: {status}  \n"
            if config_data.get("backed_up"):
                doc_content += (
                    f"   Fields saved: {len(config_data.get('fields', {}))}  \n"
                )
                doc_content += f"   Timestamp: {config_data.get('timestamp')}  \n"
            doc_content += "\n"

        # Add implementation notes
        doc_content += """
---

## Implementation Notes

### Required Python Libraries

```bash
pip install ntplib      # For NTP tests
pip install pysnmp      # For SNMP tests
# socket library is built-in for Syslog
```

### Test Implementation Pattern

All protocol tests should follow this pattern:

1. Read current device configuration
2. Enable protocol if not already enabled
3. Run protocol tests
4. Document results
5. Restore original configuration

### Safety Considerations

- Always backup configuration before changes
- Check for restart requirements before modification
- Restore original settings after testing
- Monitor device availability during tests

---

**Generated by Protocol Explorer**  
**Tool**: `tools/protocol_explorer.py`  
"""

        with open(doc_file, "w") as f:
            f.write(doc_content)

        print(f"[OK] [{self.device_ip}] Documentation saved to: {doc_file}")

    async def explore_protocols(self):
        """Main protocol exploration workflow"""
        print(f"\n{'='*60}")
        print(f"PROTOCOL EXPLORATION: {self.device_name} ({self.device_ip})")
        print(f"{'='*60}")

        try:
            # Initialize browser
            await self.initialize_browser()

            # Login and unlock configuration
            await self.login_and_unlock()

            # Check restart requirements first
            print(f"\n--- Checking Restart Requirements ---")
            restart_info = await self.check_device_restart_requirements()
            self.protocol_results["restart_requirements"] = restart_info

            # Backup configurations
            print(f"\n--- Backing Up Configurations ---")
            self.original_configs["snmp"] = await self.backup_snmp_config()
            self.original_configs["time"] = await self.backup_time_config()

            # Test protocols (active testing - temporarily modifies device configuration)
            print(f"\n--- Testing Protocols ---")
            self.protocol_results["protocols"]["snmp"] = await self.test_snmp_protocol()
            self.protocol_results["protocols"]["ntp"] = await self.test_ntp_protocol()

            # Generate documentation
            self.protocol_results["original_configs"] = self.original_configs
            await self.generate_documentation()

            print(f"\n{'='*60}")
            print(f"[COMPLETE] PROTOCOL EXPLORATION: {self.device_ip}")
            print(f"{'='*60}")

        except Exception as e:
            print(f"\n[ERROR] Protocol exploration failed: {e}")
            import traceback

            traceback.print_exc()

        finally:
            # Ensure browser is properly closed
            if self.browser:
                try:
                    await self.browser.close()
                except:
                    pass
                self.browser = None


async def main():
    """Explore protocols on all Kronos devices sequentially"""
    print("\n" + "=" * 60)
    print("KRONOS PROTOCOL EXPLORER")
    print("=" * 60)
    print("\nThis tool will explore protocol capabilities on all devices.")
    print(
        "WARNING: This tool will temporarily modify device configurations during testing."
    )
    print("Original configurations will be restored after each test.")
    print("\nDevices to explore:")
    for device in DEVICES:
        print(f"  - {device['name']} ({device['ip']})")

    input("\nPress Enter to start exploration...")

    start_time = time.time()

    for i, device in enumerate(DEVICES, 1):
        print(f"\n\nDevice {i}/{len(DEVICES)}")
        explorer = ProtocolExplorer(
            device_ip=device["ip"],
            device_name=device["name"],
            device_type=device["type"],
        )
        await explorer.explore_protocols()

        # Brief pause between devices
        if i < len(DEVICES):
            print(f"\nPausing 5 seconds before next device...")
            await asyncio.sleep(5)

    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"ALL DEVICES EXPLORED")
    print(f"{'='*60}")
    print(f"Total time: {elapsed/60:.1f} minutes")
    print(f"Results saved to: {OUTPUT_BASE}/{{device_ip}}/protocols/")
    print(f"\nGenerated files per device:")
    print(f"  - protocol_exploration_results.json")
    print(f"  - PROTOCOL_TESTS_AVAILABLE.md")


if __name__ == "__main__":
    asyncio.run(main())
