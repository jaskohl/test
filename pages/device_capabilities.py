"""
Device Capabilities Module - CORRECTED VERSION
Complete Kronos device knowledge base for test automation.

This module centralizes all device capability information from exploration data,
providing a single source of truth for device configurations, capabilities, and behaviors.
CORRECTED: All data now matches actual device exploration data from memory-bank/device_exploration/
"""

from typing import Dict, List, Any


class DeviceCapabilities:
    """
    Centralized Kronos device capability management.

    This class provides comprehensive device information extracted from exploration data,
    including hardware specifications, software capabilities, performance baselines,
    known issues, and device-specific behaviors.
    """

    # Complete device database - permanent hardware capabilities only
    # CORRECTED: Data now matches actual device exploration data
    DEVICE_DATABASE = {
        "KRONOS-2R-HVXX-A2F": {
            "device_info": {
                "series": 2,
                "model": "Series 2",
                "hardware_model": "KRONOS-2R-HVXX-A2F",
                "serial_number": "20245",
                "firmware_version": "04.04.00",
            },
            "capabilities": {
                "ptp_supported": False,
                "network_interfaces": 1,
                "interface_names": ["eth0"],
                "max_outputs": 4,  # CORRECTED: Was 6, actual is 4
                "gnss_constellations": ["GPS", "Galileo", "GLONASS", "BeiDou"],
                "authentication_levels": ["status", "configuration"],
                "http_redirect": False,
            },
            "network_config": {"interfaces": []},  # Single network interface device
            "performance_baseline": {
                "page_load_times": {},
                "session_timeout_minutes": 30,
                "max_concurrent_sessions": 5,
            },
            "known_issues": [],
            "output_signal_types": {
                1: [
                    "OFF",
                    "IRIG-B120",
                    "IRIG-B122",
                    "IRIG-B124",
                    "IRIG-B126",
                ],
                2: [
                    "OFF",
                    "IRIG-B120",
                    "IRIG-B122",
                    "IRIG-B124",
                    "IRIG-B126",
                ],
                3: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                4: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                # CORRECTED: Outputs 1-2 use IRIG-B120 series, outputs 3-4 use IRIG-B000 series
            },
            "time_reference_rules": {
                "IRIG-B*": ["UTC", "LOCAL"],  # Both time radios visible
                "PPS": ["LOCAL"],  # Only LOCAL visible
                "PPM": ["LOCAL"],  # Only LOCAL visible
                "OFF": ["UTC", "LOCAL"],  # Both visible for OFF
            },
            "timezone_data": {
                "available_timezones": [
                    "US/Eastern",
                    "US/Central",
                    "US/Mountain",
                    "US/Pacific",
                    "US/Alaska",
                    "US/Hawaii",
                    "America/Toronto",
                    "America/Vancouver",
                    "America/Edmonton",
                    "America/Winnipeg",
                    "America/Mexico_City",
                    "America/Anchorage",
                    "America/Puerto_Rico",
                    "America/Sao_Paulo",
                    "Europe/London",
                    "UTC",
                ],
                "timezone_mapping": {
                    "US/New York": "US/Eastern",
                    "US/Chicago": "US/Central",
                    "US/Denver": "US/Mountain",
                    "US/Los Angeles": "US/Pacific",
                    "US/Anchorage": "America/Anchorage",
                    "Pacific/Honolulu": "US/Hawaii",
                    "America/Toronto": "America/Toronto",
                    "America/Vancouver": "America/Vancouver",
                    "America/Edmonton": "America/Edmonton",
                    "America/Winnipeg": "America/Winnipeg",
                    "America/Mexico City": "America/Mexico_City",
                    "America/Puerto Rico": "America/Puerto_Rico",
                    "America/Sao Paulo": "America/Sao_Paulo",
                    "Europe/London": "Europe/London",
                    "UTC": "UTC",
                },
                "timezone_count": 16,
                "includes_utc": True,
            },
            "behavior_data": {
                "authentication_workflow": {
                    "dual_authentication_required": True,
                    "status_monitoring_login": {
                        "typical_time": "2-3 seconds",
                        "post_login_behavior": "redirects to dashboard with 4 status tables",
                    },
                    "configuration_unlock": {
                        "typical_time": "1-2 seconds",
                        "trigger": "dashboard dropdown → Configure link",
                        "device_specific_behavior": "requires separate password entry",
                    },
                },
                "navigation_patterns": {
                    "dashboard_structure": {
                        "tables_present": 4,
                        "table_descriptions": [
                            "Time Information (UTC/Local)",
                            "GNSS Status (LOCKED state)",
                            "Device Information (11 fields)",
                            "Satellite Tracking (Id, C/No, Constellation, State)",
                        ],
                        "navigation_options": ["dropdown menu with 'Configure' link"],
                    },
                    "configuration_sections": {
                        "available_sections": [
                            "general",
                            "network",
                            "time",
                            "gnss",
                            "outputs",
                            "display",
                            "snmp",
                            "syslog",
                            "access",
                            "contact",
                        ],
                        "access_patterns": {
                            "status_mode": "read-only dashboard access",
                            "config_mode": "full read-write configuration access",
                        },
                    },
                },
                "state_transition_timing": {
                    "login_to_dashboard": {
                        "duration": "2-3 seconds",
                        "validation": "4 tables visible on page",
                        "satellite_loading": True,
                    },
                    "dashboard_to_config_unlock": {
                        "duration": "1-2 seconds",
                        "validation": "password field visible",
                    },
                    "config_unlock_to_section": {
                        "duration": "1-2 seconds",
                        "validation": "section-specific content loaded",
                    },
                },
                "dynamic_ui_behaviors": {
                    "outputs_page_dropdown_dependency": {
                        "description": "signal type selection affects radio button visibility",
                        "observed_patterns": {
                            "IRIG-B_signals": {
                                "time1_visible": True,
                                "time2_visible": True,
                            },
                            "PPS_PPM_signals": {
                                "time1_visible": False,
                                "time2_visible": True,
                            },
                        },
                        "state_transitions": "layout changes occur within 1 second",
                    },
                    "network_config_readonly": {
                        "description": "network settings are read-only to prevent connectivity loss",
                        "safety_measures": "configuration changes blocked in UI",
                    },
                },
                "satellite_loading_behavior": {
                    "dual_cycle_confirmed": True,
                    "first_cycle_trigger": "status monitoring login",
                    "second_cycle_trigger": "configuration unlock",
                    "typical_durations": {
                        "first_cycle": "5-15 seconds",
                        "second_cycle": "5-15 seconds",
                        "total_dual_cycle": "10-30 seconds",
                    },
                    "loading_detection_methods": [
                        {
                            "method": "text-based detection",
                            "pattern": "Loading satellite data",
                            "reliability": "high",
                            "locator": "page.get_by_text('Loading satellite data', exact=False)",
                        },
                        {
                            "method": "JavaScript evaluation",
                            "pattern": "document.body.textContent.includes('Loading satellite data')",
                            "reliability": "medium",
                            "fallback": True,
                        },
                    ],
                    "device_characteristics": {
                        "satellite_availability_impact": "variable timing based on satellite lock status",
                        "network_latency_impact": "embedded device timing variations",
                        "performance_baseline": "8-12 seconds per cycle",
                    },
                },
                "performance_expectations": {
                    "authentication_performance": {
                        "status_monitoring_login": {
                            "typical_time": "2-3 seconds",
                            "best_case": "< 2 seconds",
                            "worst_case": "< 5 seconds",
                        },
                        "configuration_unlock": {
                            "typical_time": "1-2 seconds",
                            "best_case": "< 1 second",
                            "worst_case": "< 3 seconds",
                            "includes_satellite_loading": False,
                        },
                    },
                    "navigation_performance": {
                        "dashboard_to_config_unlock": {
                            "typical_time": "1-2 seconds",
                            "best_case": "< 1 second",
                            "worst_case": "< 3 seconds",
                            "includes_satellite_loading": False,
                        },
                        "section_navigation": {
                            "typical_time": "1-2 seconds",
                            "best_case": "< 1 second",
                            "worst_case": "< 3 seconds",
                            "includes_satellite_loading": False,
                        },
                    },
                    "satellite_loading_performance": {
                        "first_cycle": {
                            "trigger": "after status monitoring login",
                            "typical_time": "5-15 seconds",
                            "best_case": "< 5 seconds",
                            "worst_case": "< 30 seconds",
                        },
                        "second_cycle": {
                            "trigger": "after configuration unlock",
                            "typical_time": "5-15 seconds",
                            "best_case": "< 5 seconds",
                            "worst_case": "< 30 seconds",
                        },
                    },
                    "complete_workflow_targets": {
                        "end_to_end_time": "< 30 seconds",
                        "ui_responsiveness": "< 2 seconds",
                        "embedded_device_constraints": "< 15 seconds",
                    },
                },
            },
        },
        "KRONOS-2P-HV-2": {
            "device_info": {
                "series": 2,
                "model": "Series 2",
                "hardware_model": "KRONOS-2P-HV-2",
                "serial_number": "20216",
                "firmware_version": "04.04.00",
            },
            "capabilities": {
                "ptp_supported": False,
                "network_interfaces": 1,
                "interface_names": ["eth0"],
                "max_outputs": 4,  # Verified from exploration data
                "gnss_constellations": ["GPS", "Galileo", "GLONASS", "BeiDou"],
                "authentication_levels": ["status", "configuration"],
                "http_redirect": False,  # Added from exploration data
            },
            "network_config": {"interfaces": []},  # Single network interface device
            "performance_baseline": {
                "page_load_times": {},
                "session_timeout_minutes": 30,
                "max_concurrent_sessions": 5,
            },
            "known_issues": [
                "HTTP to HTTPS redirect causes browser compatibility test failures"
            ],
            "output_signal_types": {
                1: [
                    "OFF",
                    "IRIG-B120",
                    "IRIG-B122",
                    "IRIG-B124",
                    "IRIG-B126",
                ],
                2: [
                    "OFF",
                    "IRIG-B120",
                    "IRIG-B122",
                    "IRIG-B124",
                    "IRIG-B126",
                ],
                3: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                4: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                # CORRECTED: Outputs 1-2 use IRIG-B120 series, outputs 3-4 use IRIG-B000 series
            },
            "time_reference_rules": {
                "IRIG-B*": ["UTC", "LOCAL"],  # Both time radios visible
                "PPS": ["LOCAL"],  # Only LOCAL visible
                "PPM": ["LOCAL"],  # Only LOCAL visible
                "OFF": ["UTC", "LOCAL"],  # Both visible for OFF
            },
            "timezone_data": {
                "available_timezones": [
                    "US/Eastern",
                    "US/Central",
                    "US/Mountain",
                    "US/Pacific",
                    "US/Alaska",
                    "US/Hawaii",
                    "America/Toronto",
                    "America/Vancouver",
                    "America/Edmonton",
                    "America/Winnipeg",
                    "America/Mexico_City",
                    "America/Anchorage",
                    "America/Puerto_Rico",
                    "America/Sao_Paulo",
                    "Europe/London",
                    "UTC",
                ],
                "timezone_mapping": {
                    "US/New York": "US/Eastern",
                    "US/Chicago": "US/Central",
                    "US/Denver": "US/Mountain",
                    "US/Los Angeles": "US/Pacific",
                    "US/Anchorage": "America/Anchorage",
                    "Pacific/Honolulu": "US/Hawaii",
                    "America/Toronto": "America/Toronto",
                    "America/Vancouver": "America/Vancouver",
                    "America/Edmonton": "America/Edmonton",
                    "America/Winnipeg": "America/Winnipeg",
                    "America/Mexico City": "America/Mexico_City",
                    "America/Puerto Rico": "America/Puerto_Rico",
                    "America/Sao Paulo": "America/Sao_Paulo",
                    "Europe/London": "Europe/London",
                    "UTC": "UTC",
                },
                "timezone_count": 16,
                "includes_utc": True,
            },
            "behavior_data": {
                "authentication_workflow": {
                    "dual_authentication_required": True,
                    "status_monitoring_login": {
                        "typical_time": "2-3 seconds",
                        "post_login_behavior": "redirects to dashboard with 4 status tables",
                    },
                    "configuration_unlock": {
                        "typical_time": "1-2 seconds",
                        "trigger": "dashboard dropdown → Configure link",
                        "device_specific_behavior": "requires separate password entry",
                    },
                },
                "navigation_patterns": {
                    "dashboard_structure": {
                        "tables_present": 4,
                        "table_descriptions": [
                            "Time Information (UTC/Local)",
                            "GNSS Status (LOCKED state)",
                            "Device Information (11 fields)",
                            "Satellite Tracking (Id, C/No, Constellation, State)",
                        ],
                        "navigation_options": ["dropdown menu with 'Configure' link"],
                    },
                    "configuration_sections": {
                        "available_sections": [
                            "general",
                            "network",
                            "time",
                            "gnss",
                            "outputs",
                            "display",
                            "snmp",
                            "syslog",
                            "access",
                            "contact",
                        ],
                        "access_patterns": {
                            "status_mode": "read-only dashboard access",
                            "config_mode": "full read-write configuration access",
                        },
                    },
                },
                "state_transition_timing": {
                    "login_to_dashboard": {
                        "duration": "2-3 seconds",
                        "validation": "4 tables visible on page",
                        "satellite_loading": True,
                    },
                    "dashboard_to_config_unlock": {
                        "duration": "1-2 seconds",
                        "validation": "password field visible",
                    },
                    "config_unlock_to_section": {
                        "duration": "1-2 seconds",
                        "validation": "section-specific content loaded",
                    },
                },
                "dynamic_ui_behaviors": {
                    "outputs_page_dropdown_dependency": {
                        "description": "signal type selection affects radio button visibility",
                        "observed_patterns": {
                            "IRIG-B_signals": {
                                "time1_visible": True,
                                "time2_visible": True,
                            },
                            "PPS_PPM_signals": {
                                "time1_visible": False,
                                "time2_visible": True,
                            },
                        },
                        "state_transitions": "layout changes occur within 1 second",
                    },
                    "network_config_readonly": {
                        "description": "network settings are read-only to prevent connectivity loss",
                        "safety_measures": "configuration changes blocked in UI",
                    },
                    "http_to_https_redirect": {
                        "description": "automatic HTTP to HTTPS redirect enabled",
                        "impact": "affects browser compatibility testing",
                    },
                },
                "satellite_loading_behavior": {
                    "dual_cycle_confirmed": True,
                    "first_cycle_trigger": "status monitoring login",
                    "second_cycle_trigger": "configuration unlock",
                    "typical_durations": {
                        "first_cycle": "5-15 seconds",
                        "second_cycle": "5-15 seconds",
                        "total_dual_cycle": "10-30 seconds",
                    },
                    "loading_detection_methods": [
                        {
                            "method": "text-based detection",
                            "pattern": "Loading satellite data",
                            "reliability": "high",
                            "locator": "page.get_by_text('Loading satellite data', exact=False)",
                        },
                        {
                            "method": "JavaScript evaluation",
                            "pattern": "document.body.textContent.includes('Loading satellite data')",
                            "reliability": "medium",
                            "fallback": True,
                        },
                    ],
                    "device_characteristics": {
                        "satellite_availability_impact": "variable timing based on satellite lock status",
                        "network_latency_impact": "embedded device timing variations",
                        "performance_baseline": "8-12 seconds per cycle",
                    },
                },
                "performance_expectations": {
                    "authentication_performance": {
                        "status_monitoring_login": {
                            "typical_time": "2-3 seconds",
                            "best_case": "< 2 seconds",
                            "worst_case": "< 5 seconds",
                        },
                        "configuration_unlock": {
                            "typical_time": "1-2 seconds",
                            "best_case": "< 1 second",
                            "worst_case": "< 3 seconds",
                            "includes_satellite_loading": False,
                        },
                    },
                    "navigation_performance": {
                        "dashboard_to_config_unlock": {
                            "typical_time": "1-2 seconds",
                            "best_case": "< 1 second",
                            "worst_case": "< 3 seconds",
                            "includes_satellite_loading": False,
                        },
                        "section_navigation": {
                            "typical_time": "1-2 seconds",
                            "best_case": "< 1 second",
                            "worst_case": "< 3 seconds",
                            "includes_satellite_loading": False,
                        },
                    },
                    "satellite_loading_performance": {
                        "first_cycle": {
                            "trigger": "after status monitoring login",
                            "typical_time": "5-15 seconds",
                            "best_case": "< 5 seconds",
                            "worst_case": "< 30 seconds",
                        },
                        "second_cycle": {
                            "trigger": "after configuration unlock",
                            "typical_time": "5-15 seconds",
                            "best_case": "< 5 seconds",
                            "worst_case": "< 30 seconds",
                        },
                    },
                    "complete_workflow_targets": {
                        "end_to_end_time": "< 30 seconds",
                        "ui_responsiveness": "< 2 seconds",
                        "embedded_device_constraints": "< 15 seconds",
                    },
                },
            },
        },
        "KRONOS-3R-HVLV-TCXO-A2F": {
            "device_info": {
                "series": 3,
                "model": "Series 3",
                "hardware_model": "KRONOS-3R-HVLV-TCXO-A2F",
                "serial_number": "30165",
                "firmware_version": "02.06.04",
            },
            "capabilities": {
                "ptp_supported": True,
                "network_interfaces": 4,
                "interface_names": [
                    "eth0",
                    "eth1",
                    "eth2",
                    "eth3",
                ],
                "ptp_interfaces": ["eth1", "eth2", "eth3"],  # From exploration data
                "max_outputs": 6,
                "gnss_constellations": [
                    "GPS",
                    "GLONASS",
                    "Galileo",
                    "BeiDou",
                ],
                "authentication_levels": ["status", "configuration"],
                "http_redirect": False,
            },
            "network_config": {
                "interface_configs": {
                    "eth0": [
                        "ip",
                        "mask",
                        "mtu",
                        "ntp",
                        "snmp",
                        "vlan",
                    ],  # Management interface (no changeip, no redundancy)
                    "eth1": [
                        "ip",
                        "mask",
                        "mtu",
                        "redundancy",
                        "ntp",
                        "ptp",
                        "snmp",
                        "vlan",
                    ],  # High-availability with PTP
                    "eth2": [
                        "ip",
                        "mask",
                        "mtu",
                        "redundancy",
                        "ntp",
                        "ptp",
                        "snmp",
                        "vlan",
                    ],  # High-availability with PTP
                    "eth3": [
                        "ip",
                        "mask",
                        "mtu",
                        "redundancy",
                        "ntp",
                        "ptp",
                        "snmp",
                        "vlan",
                    ],  # High-availability with PTP
                    # eth4 removed - device only has 4 interfaces
                }
            },
            "performance_baseline": {
                "page_load_times": {},
                "session_timeout_minutes": 30,
                "max_concurrent_sessions": 5,
            },
            "known_issues": [
                "PTP panels collapsed by default",
                "Multi-interface locator ambiguity",
            ],
            "output_signal_types": {
                1: [
                    "OFF",
                    "IRIG-B120",
                    "IRIG-B122",
                    "IRIG-B124",
                    "IRIG-B126",
                ],
                2: [
                    "OFF",
                    "IRIG-B120",
                    "IRIG-B122",
                    "IRIG-B124",
                    "IRIG-B126",
                ],
                3: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                4: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                5: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                6: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                # CORRECTED: Outputs 1-2 use IRIG-B120 series, outputs 3-6 use IRIG-B000 series
            },
            "time_reference_rules": {
                "IRIG-B*": ["UTC", "LOCAL"],  # Both time radios visible
                "PPS": ["LOCAL"],  # Only LOCAL visible
                "PPM": ["LOCAL"],  # Only LOCAL visible
                "OFF": ["UTC", "LOCAL"],  # Both visible for OFF
            },
            "timezone_data": {
                "available_timezones": [
                    "US/Eastern",
                    "US/Central",
                    "US/Mountain",
                    "US/Pacific",
                    "US/Alaska",
                    "US/Hawaii",
                    "America/Toronto",
                    "America/Vancouver",
                    "America/Edmonton",
                    "America/Winnipeg",
                    "America/Mexico_City",
                    "America/Anchorage",
                    "America/Puerto_Rico",
                    "America/Sao_Paulo",
                    "Europe/London",
                    "UTC",
                    "Australia/Sydney",
                ],
                "timezone_mapping": {
                    "US/New York": "US/Eastern",
                    "US/Chicago": "US/Central",
                    "US/Denver": "US/Mountain",
                    "US/Los Angeles": "US/Pacific",
                    "US/Anchorage": "America/Anchorage",
                    "Pacific/Honolulu": "US/Hawaii",
                    "America/Toronto": "America/Toronto",
                    "America/Vancouver": "America/Vancouver",
                    "America/Edmonton": "America/Edmonton",
                    "America/Winnipeg": "America/Winnipeg",
                    "America/Mexico City": "America/Mexico_City",
                    "America/Puerto Rico": "America/Puerto_Rico",
                    "America/Sao Paulo": "America/Sao_Paulo",
                    "Europe/London": "Europe/London",
                    "Australia/Sydney": "Australia/Sydney",
                    "UTC": "UTC",
                },
                "timezone_count": 17,
                "includes_utc": True,
            },
            "behavior_data": {
                "authentication_workflow": {
                    "dual_authentication_required": True,
                    "status_monitoring_login": {
                        "typical_time": "2-3 seconds",
                        "post_login_behavior": "redirects to dashboard with 4 status tables",
                    },
                    "configuration_unlock": {
                        "typical_time": "1-2 seconds",
                        "trigger": "dashboard dropdown → Configure link",
                        "device_specific_behavior": "requires separate password entry",
                    },
                },
                "navigation_patterns": {
                    "dashboard_structure": {
                        "tables_present": 4,
                        "table_descriptions": [
                            "Time Information (UTC/Local)",
                            "GNSS Status (LOCKED state)",
                            "Device Information (11 fields)",
                            "Satellite Tracking (Id, C/No, Constellation, State)",
                        ],
                        "navigation_options": ["dropdown menu with 'Configure' link"],
                    },
                    "configuration_sections": {
                        "available_sections": [
                            "general",
                            "network",
                            "time",
                            "gnss",
                            "outputs",
                            "display",
                            "snmp",
                            "syslog",
                            "access",
                            "contact",
                        ],
                        "device_series_specific": "ptp",
                        "access_patterns": {
                            "status_mode": "read-only dashboard access",
                            "config_mode": "full read-write configuration access",
                        },
                    },
                },
                "state_transition_timing": {
                    "login_to_dashboard": {
                        "duration": "2-3 seconds",
                        "validation": "4 tables visible on page",
                        "satellite_loading": True,
                    },
                    "dashboard_to_config_unlock": {
                        "duration": "1-2 seconds",
                        "validation": "password field visible",
                    },
                    "config_unlock_to_section": {
                        "duration": "1-2 seconds",
                        "validation": "section-specific content loaded",
                    },
                },
                "dynamic_ui_behaviors": {
                    "outputs_page_dropdown_dependency": {
                        "description": "signal type selection affects radio button visibility",
                        "observed_patterns": {
                            "IRIG-B_signals": {
                                "time1_visible": True,
                                "time2_visible": True,
                            },
                            "PPS_PPM_signals": {
                                "time1_visible": False,
                                "time2_visible": True,
                            },
                        },
                        "state_transitions": "layout changes occur within 1 second",
                    },
                    "network_config_readonly": {
                        "description": "network settings are read-only to prevent connectivity loss",
                        "safety_measures": "configuration changes blocked in UI",
                    },
                    "ptp_panels_collapsed": {
                        "description": "PTP configuration panels start collapsed by default",
                        "user_action_required": "manual expansion needed to access PTP settings",
                    },
                    "multi_interface_locator_ambiguity": {
                        "description": "multiple network interfaces cause locator identification issues",
                        "impact": "test automation may need specific interface targeting",
                    },
                },
                "satellite_loading_behavior": {
                    "dual_cycle_confirmed": True,
                    "first_cycle_trigger": "status monitoring login",
                    "second_cycle_trigger": "configuration unlock",
                    "typical_durations": {
                        "first_cycle": "5-15 seconds",
                        "second_cycle": "5-15 seconds",
                        "total_dual_cycle": "10-30 seconds",
                    },
                    "loading_detection_methods": [
                        {
                            "method": "text-based detection",
                            "pattern": "Loading satellite data",
                            "reliability": "high",
                            "locator": "page.get_by_text('Loading satellite data', exact=False)",
                        },
                        {
                            "method": "JavaScript evaluation",
                            "pattern": "document.body.textContent.includes('Loading satellite data')",
                            "reliability": "medium",
                            "fallback": True,
                        },
                    ],
                    "device_characteristics": {
                        "satellite_availability_impact": "variable timing based on satellite lock status",
                        "network_latency_impact": "embedded device timing variations",
                        "performance_baseline": "8-12 seconds per cycle",
                    },
                },
                "performance_expectations": {
                    "authentication_performance": {
                        "status_monitoring_login": {
                            "typical_time": "2-3 seconds",
                            "best_case": "< 2 seconds",
                            "worst_case": "< 5 seconds",
                        },
                        "configuration_unlock": {
                            "typical_time": "1-2 seconds",
                            "best_case": "< 1 second",
                            "worst_case": "< 3 seconds",
                            "includes_satellite_loading": False,
                        },
                    },
                    "navigation_performance": {
                        "dashboard_to_config_unlock": {
                            "typical_time": "1-2 seconds",
                            "best_case": "< 1 second",
                            "worst_case": "< 3 seconds",
                            "includes_satellite_loading": False,
                        },
                        "section_navigation": {
                            "typical_time": "1-2 seconds",
                            "best_case": "< 1 second",
                            "worst_case": "< 3 seconds",
                            "includes_satellite_loading": False,
                        },
                    },
                    "satellite_loading_performance": {
                        "first_cycle": {
                            "trigger": "after status monitoring login",
                            "typical_time": "5-15 seconds",
                            "best_case": "< 5 seconds",
                            "worst_case": "< 30 seconds",
                        },
                        "second_cycle": {
                            "trigger": "after configuration unlock",
                            "typical_time": "5-15 seconds",
                            "best_case": "< 5 seconds",
                            "worst_case": "< 30 seconds",
                        },
                    },
                    "complete_workflow_targets": {
                        "end_to_end_time": "< 30 seconds",
                        "ui_responsiveness": "< 2 seconds",
                        "embedded_device_constraints": "< 15 seconds",
                    },
                },
            },
        },
        "KRONOS-3R-HVXX-TCXO-44A": {
            "device_info": {
                "series": 3,
                "model": "Series 3",
                "hardware_model": "KRONOS-3R-HVXX-TCXO-44A",
                "serial_number": "30134",
                "firmware_version": "02.06.04",
            },
            "capabilities": {
                "ptp_supported": True,
                "network_interfaces": 3,
                "interface_names": ["eth0", "eth1", "eth3"],
                "ptp_interfaces": ["eth1", "eth3"],
                "max_outputs": 6,
                "gnss_constellations": ["GPS", "Galileo", "GLONASS", "BeiDou"],
                "authentication_levels": ["status", "configuration"],
                "http_redirect": False,
            },
            "network_config": {
                "interface_configs": {
                    "eth0": [
                        "ip",
                        "mask",
                        "mtu",
                        "ntp",
                        "snmp",
                        "vlan",
                        "changeip",
                    ],  # Management interface only
                    "eth1": [
                        "ip",
                        "mask",
                        "mtu",
                        "redundancy",
                        "ntp",
                        "ptp",
                        "snmp",
                        "vlan",
                    ],  # High-availability with redundancy and PTP
                    "eth3": [
                        "ip",
                        "mask",
                        "mtu",
                        "redundancy",
                        "ntp",
                        "ptp",
                        "snmp",
                        "vlan",
                    ],  # High-availability with redundancy and PTP
                }
            },
            "performance_baseline": {
                "page_load_times": {},
                "session_timeout_minutes": 30,
                "max_concurrent_sessions": 5,
            },
            "known_issues": [
                "PTP panels collapsed by default",
                "Multi-interface locator ambiguity",
                "Configuration unlock timeouts (3 errors vs 0-1 on other devices)",
                "Navigation timeout issues",
            ],
            "output_signal_types": {
                1: [
                    "OFF",
                    "IRIG-B120",
                    "IRIG-B122",
                    "IRIG-B124",
                    "IRIG-B126",
                ],
                2: [
                    "OFF",
                    "IRIG-B120",
                    "IRIG-B122",
                    "IRIG-B124",
                    "IRIG-B126",
                ],
                3: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                4: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                5: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                6: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                # CORRECTED: Outputs 1-2 use IRIG-B120 series, outputs 3-6 use IRIG-B000 series
            },
            "time_reference_rules": {
                "IRIG-B*": ["UTC", "LOCAL"],
                "PPS": ["LOCAL"],
                "PPM": ["LOCAL"],
                "OFF": ["UTC", "LOCAL"],
            },
            "timezone_data": {
                "available_timezones": [
                    "US/Eastern",
                    "US/Central",
                    "US/Mountain",
                    "US/Pacific",
                    "US/Alaska",
                    "US/Hawaii",
                    "America/Toronto",
                    "America/Vancouver",
                    "America/Edmonton",
                    "America/Winnipeg",
                    "America/Mexico_City",
                    "America/Anchorage",
                    "America/Puerto_Rico",
                    "America/Sao_Paulo",
                    "Europe/London",
                    "UTC",
                    "Australia/Sydney",
                ],
                "timezone_mapping": {
                    "US/New York": "US/Eastern",
                    "US/Chicago": "US/Central",
                    "US/Denver": "US/Mountain",
                    "US/Los Angeles": "US/Pacific",
                    "US/Anchorage": "America/Anchorage",
                    "Pacific/Honolulu": "US/Hawaii",
                    "America/Toronto": "America/Toronto",
                    "America/Vancouver": "America/Vancouver",
                    "America/Edmonton": "America/Edmonton",
                    "America/Winnipeg": "America/Winnipeg",
                    "America/Mexico City": "America/Mexico_City",
                    "America/Puerto Rico": "America/Puerto_Rico",
                    "America/Sao Paulo": "America/Sao_Paulo",
                    "Europe/London": "Europe/London",
                    "Australia/Sydney": "Australia/Sydney",
                    "UTC": "UTC",
                },
                "timezone_count": 17,
                "includes_utc": True,
            },
            "behavior_data": {
                "authentication_workflow": {
                    "dual_authentication_required": True,
                    "status_monitoring_login": {
                        "typical_time": "2-3 seconds",
                        "post_login_behavior": "redirects to dashboard with 4 status tables",
                    },
                    "configuration_unlock": {
                        "typical_time": "1-2 seconds",
                        "trigger": "dashboard dropdown → Configure link",
                        "device_specific_behavior": "requires separate password entry",
                    },
                },
                "navigation_patterns": {
                    "dashboard_structure": {
                        "tables_present": 4,
                        "table_descriptions": [
                            "Time Information (UTC/Local)",
                            "GNSS Status (LOCKED state)",
                            "Device Information (11 fields)",
                            "Satellite Tracking (Id, C/No, Constellation, State)",
                        ],
                        "navigation_options": ["dropdown menu with 'Configure' link"],
                    },
                    "configuration_sections": {
                        "available_sections": [
                            "general",
                            "network",
                            "time",
                            "gnss",
                            "outputs",
                            "display",
                            "snmp",
                            "syslog",
                            "access",
                            "contact",
                        ],
                        "access_patterns": {
                            "status_mode": "read-only dashboard access",
                            "config_mode": "full read-write configuration access",
                        },
                    },
                },
                "state_transition_timing": {
                    "login_to_dashboard": {
                        "duration": "2-3 seconds",
                        "validation": "4 tables visible on page",
                        "satellite_loading": True,
                    },
                    "dashboard_to_config_unlock": {
                        "duration": "1-2 seconds",
                        "validation": "password field visible",
                    },
                    "config_unlock_to_section": {
                        "duration": "1-2 seconds",
                        "validation": "section-specific content loaded",
                    },
                },
                "dynamic_ui_behaviors": {
                    "outputs_page_dropdown_dependency": {
                        "description": "signal type selection affects radio button visibility",
                        "observed_patterns": {
                            "IRIG-B_signals": {
                                "time1_visible": True,
                                "time2_visible": True,
                            },
                            "PPS_PPM_signals": {
                                "time1_visible": False,
                                "time2_visible": True,
                            },
                        },
                        "state_transitions": "layout changes occur within 1 second",
                    },
                    "network_config_readonly": {
                        "description": "network settings are read-only to prevent connectivity loss",
                        "safety_measures": "configuration changes blocked in UI",
                    },
                },
                "satellite_loading_behavior": {
                    "dual_cycle_confirmed": True,
                    "first_cycle_trigger": "status monitoring login",
                    "second_cycle_trigger": "configuration unlock",
                    "typical_durations": {
                        "first_cycle": "5-15 seconds",
                        "second_cycle": "5-15 seconds",
                        "total_dual_cycle": "10-30 seconds",
                    },
                    "loading_detection_methods": [
                        {
                            "method": "text-based detection",
                            "pattern": "Loading satellite data",
                            "reliability": "high",
                            "locator": "page.get_by_text('Loading satellite data', exact=False)",
                        },
                        {
                            "method": "JavaScript evaluation",
                            "pattern": "document.body.textContent.includes('Loading satellite data')",
                            "reliability": "medium",
                            "fallback": True,
                        },
                    ],
                    "device_characteristics": {
                        "satellite_availability_impact": "variable timing based on satellite lock status",
                        "network_latency_impact": "embedded device timing variations",
                        "performance_baseline": "8-12 seconds per cycle",
                    },
                },
                "performance_expectations": {
                    "authentication_performance": {
                        "status_monitoring_login": {
                            "typical_time": "2-3 seconds",
                            "best_case": "< 2 seconds",
                            "worst_case": "< 5 seconds",
                        },
                        "configuration_unlock": {
                            "typical_time": "1-2 seconds",
                            "best_case": "< 1 second",
                            "worst_case": "< 3 seconds",
                            "includes_satellite_loading": False,
                        },
                    },
                    "navigation_performance": {
                        "dashboard_to_config_unlock": {
                            "typical_time": "1-2 seconds",
                            "best_case": "< 1 second",
                            "worst_case": "< 3 seconds",
                            "includes_satellite_loading": False,
                        },
                        "section_navigation": {
                            "typical_time": "1-2 seconds",
                            "best_case": "< 1 second",
                            "worst_case": "< 3 seconds",
                            "includes_satellite_loading": False,
                        },
                    },
                    "satellite_loading_performance": {
                        "first_cycle": {
                            "trigger": "after status monitoring login",
                            "typical_time": "5-15 seconds",
                            "best_case": "< 5 seconds",
                            "worst_case": "< 30 seconds",
                        },
                        "second_cycle": {
                            "trigger": "after configuration unlock",
                            "typical_time": "5-15 seconds",
                            "best_case": "< 5 seconds",
                            "worst_case": "< 30 seconds",
                        },
                    },
                    "complete_workflow_targets": {
                        "end_to_end_time": "< 30 seconds",
                        "ui_responsiveness": "< 2 seconds",
                        "embedded_device_constraints": "< 15 seconds",
                    },
                },
            },
        },
        "KRONOS-3R-HVXX-TCXO-A2X": {
            "device_info": {
                "series": 3,
                "model": "Series 3 (Comprehensive)",
                "hardware_model": "KRONOS-3R-HVXX-TCXO-A2X",
                "serial_number": "30134",
                "firmware_version": "02.06.04",
            },
            "capabilities": {
                "ptp_supported": True,
                "network_interfaces": 5,
                "interface_names": ["eth0", "eth1", "eth2", "eth3", "eth4"],
                "ptp_interfaces": ["eth1", "eth3"],
                "max_outputs": 6,
                "gnss_constellations": ["GPS", "Galileo", "GLONASS", "BeiDou"],
                "authentication_levels": ["status", "configuration"],
                "http_redirect": False,
            },
            "network_config": {
                "interface_configs": {
                    "eth0": [
                        "ip",
                        "mask",
                        "mtu",
                        "ntp",
                        "snmp",
                        "vlan",
                        "changeip",
                    ],  # Management interface
                    "eth1": [
                        "ip",
                        "mask",
                        "mtu",
                        "redundancy",
                        "ntp",
                        "ptp",
                        "snmp",
                        "vlan",
                    ],  # Redundant with PTP
                    "eth2": [
                        "ip",
                        "mask",
                        "mtu",
                        "redundancy",
                        "ntp",
                        "ptp",
                        "snmp",
                        "vlan",
                    ],  # Redundant with PTP
                    "eth3": [
                        "ip",
                        "mask",
                        "mtu",
                        "redundancy",
                        "ntp",
                        "ptp",
                        "snmp",
                        "vlan",
                    ],  # Redundant with PTP
                    "eth4": [
                        "ip",
                        "mask",
                        "mtu",
                        "redundancy",
                        "ntp",
                        "ptp",
                        "snmp",
                        "vlan",
                    ],  # Redundant with PTP
                }
            },
            "performance_baseline": {
                "page_load_times": {},
                "session_timeout_minutes": 30,
                "max_concurrent_sessions": 5,
            },
            "known_issues": [
                "PTP panels collapsed by default",
                "Multi-interface locator ambiguity",
                "Configuration unlock timeouts (3 errors vs 0-1 on other devices)",
                "Navigation timeout issues",
            ],
            "output_signal_types": {
                1: [
                    "OFF",
                    "IRIG-B120",
                    "IRIG-B122",
                    "IRIG-B124",
                    "IRIG-B126",
                ],
                2: [
                    "OFF",
                    "IRIG-B120",
                    "IRIG-B122",
                    "IRIG-B124",
                    "IRIG-B126",
                ],
                3: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                4: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                5: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                6: [
                    "OFF",
                    "IRIG-B000",
                    "IRIG-B002",
                    "IRIG-B004",
                    "IRIG-B006",
                    "PPS",
                    "PPM",
                ],
                # CORRECTED: Outputs 1-2 use IRIG-B120 series, outputs 3-6 use IRIG-B000 series
            },
            "time_reference_rules": {
                "IRIG-B*": ["UTC", "LOCAL"],
                "PPS": ["LOCAL"],
                "PPM": ["LOCAL"],
                "OFF": ["UTC", "LOCAL"],
            },
            "timezone_data": {
                "available_timezones": [
                    "US/Eastern",
                    "US/Central",
                    "US/Mountain",
                    "US/Pacific",
                    "US/Alaska",
                    "US/Hawaii",
                    "America/Toronto",
                    "America/Vancouver",
                    "America/Edmonton",
                    "America/Winnipeg",
                    "America/Mexico_City",
                    "America/Anchorage",
                    "America/Puerto_Rico",
                    "America/Sao_Paulo",
                    "Europe/London",
                    "UTC",
                    "Australia/Sydney",
                ],
                "timezone_mapping": {
                    "US/New York": "US/Eastern",
                    "US/Chicago": "US/Central",
                    "US/Denver": "US/Mountain",
                    "US/Los Angeles": "US/Pacific",
                    "US/Anchorage": "America/Anchorage",
                    "Pacific/Honolulu": "US/Hawaii",
                    "America/Toronto": "America/Toronto",
                    "America/Vancouver": "America/Vancouver",
                    "America/Edmonton": "America/Edmonton",
                    "America/Winnipeg": "America/Winnipeg",
                    "America/Mexico City": "America/Mexico_City",
                    "America/Puerto Rico": "America/Puerto_Rico",
                    "America/Sao Paulo": "America/Sao_Paulo",
                    "Europe/London": "Europe/London",
                    "Australia/Sydney": "Australia/Sydney",
                    "UTC": "UTC",
                },
                "timezone_count": 17,
                "includes_utc": True,
            },
            "behavior_data": {
                "authentication_workflow": {
                    "dual_authentication_required": True,
                    "status_monitoring_login": {
                        "typical_time": "2-3 seconds",
                        "post_login_behavior": "redirects to dashboard with 4 status tables",
                    },
                    "configuration_unlock": {
                        "typical_time": "1-2 seconds",
                        "trigger": "dashboard dropdown → Configure link",
                        "device_specific_behavior": "requires separate password entry",
                    },
                },
                "navigation_patterns": {
                    "dashboard_structure": {
                        "tables_present": 4,
                        "table_descriptions": [
                            "Time Information (UTC/Local)",
                            "GNSS Status (LOCKED state)",
                            "Device Information (11 fields)",
                            "Satellite Tracking (Id, C/No, Constellation, State)",
                        ],
                        "navigation_options": ["dropdown menu with 'Configure' link"],
                    },
                    "configuration_sections": {
                        "available_sections": [
                            "general",
                            "network",
                            "time",
                            "gnss",
                            "outputs",
                            "display",
                            "snmp",
                            "syslog",
                            "access",
                            "contact",
                        ],
                        "access_patterns": {
                            "status_mode": "read-only dashboard access",
                            "config_mode": "full read-write configuration access",
                        },
                    },
                },
                "state_transition_timing": {
                    "login_to_dashboard": {
                        "duration": "2-3 seconds",
                        "validation": "4 tables visible on page",
                        "satellite_loading": True,
                    },
                    "dashboard_to_config_unlock": {
                        "duration": "1-2 seconds",
                        "validation": "password field visible",
                    },
                    "config_unlock_to_section": {
                        "duration": "1-2 seconds",
                        "validation": "section-specific content loaded",
                    },
                },
                "dynamic_ui_behaviors": {
                    "outputs_page_dropdown_dependency": {
                        "description": "signal type selection affects radio button visibility",
                        "observed_patterns": {
                            "IRIG-B_signals": {
                                "time1_visible": True,
                                "time2_visible": True,
                            },
                            "PPS_PPM_signals": {
                                "time1_visible": False,
                                "time2_visible": True,
                            },
                        },
                        "state_transitions": "layout changes occur within 1 second",
                    },
                    "network_config_readonly": {
                        "description": "network settings are read-only to prevent connectivity loss",
                        "safety_measures": "configuration changes blocked in UI",
                    },
                },
                "satellite_loading_behavior": {
                    "dual_cycle_confirmed": True,
                    "first_cycle_trigger": "status monitoring login",
                    "second_cycle_trigger": "configuration unlock",
                    "typical_durations": {
                        "first_cycle": "5-15 seconds",
                        "second_cycle": "5-15 seconds",
                        "total_dual_cycle": "10-30 seconds",
                    },
                    "loading_detection_methods": [
                        {
                            "method": "text-based detection",
                            "pattern": "Loading satellite data",
                            "reliability": "high",
                            "locator": "page.get_by_text('Loading satellite data', exact=False)",
                        },
                        {
                            "method": "JavaScript evaluation",
                            "pattern": "document.body.textContent.includes('Loading satellite data')",
                            "reliability": "medium",
                            "fallback": True,
                        },
                    ],
                    "device_characteristics": {
                        "satellite_availability_impact": "variable timing based on satellite lock status",
                        "network_latency_impact": "embedded device timing variations",
                        "performance_baseline": "8-12 seconds per cycle",
                    },
                },
                "performance_expectations": {
                    "authentication_performance": {
                        "status_monitoring_login": {
                            "typical_time": "2-3 seconds",
                            "best_case": "< 2 seconds",
                            "worst_case": "< 5 seconds",
                        },
                        "configuration_unlock": {
                            "typical_time": "1-2 seconds",
                            "best_case": "< 1 second",
                            "worst_case": "< 3 seconds",
                            "includes_satellite_loading": False,
                        },
                    },
                    "navigation_performance": {
                        "dashboard_to_config_unlock": {
                            "typical_time": "1-2 seconds",
                            "best_case": "< 1 second",
                            "worst_case": "< 3 seconds",
                            "includes_satellite_loading": False,
                        },
                        "section_navigation": {
                            "typical_time": "1-2 seconds",
                            "best_case": "< 1 second",
                            "worst_case": "< 3 seconds",
                            "includes_satellite_loading": False,
                        },
                    },
                    "satellite_loading_performance": {
                        "first_cycle": {
                            "trigger": "after status monitoring login",
                            "typical_time": "5-15 seconds",
                            "best_case": "< 5 seconds",
                            "worst_case": "< 30 seconds",
                        },
                        "second_cycle": {
                            "trigger": "after configuration unlock",
                            "typical_time": "5-15 seconds",
                            "best_case": "< 5 seconds",
                            "worst_case": "< 30 seconds",
                        },
                    },
                    "complete_workflow_targets": {
                        "end_to_end_time": "< 30 seconds",
                        "ui_responsiveness": "< 2 seconds",
                        "embedded_device_constraints": "< 15 seconds",
                    },
                },
            },
        },
    }

    @classmethod
    def has_capability(cls, model: str, capability: str) -> bool:
        """
        Check if device has specific capability.

        Args:
            model: Hardware model string
            capability: Capability name to check

        Returns:
            True if device has capability, False otherwise
        """
        capabilities = cls.get_capabilities(model)
        return capabilities.get(capability, False)

    @classmethod
    def get_series(cls, model: str) -> int:
        """
        Get device series number.

        Args:
            model: Hardware model string

        Returns:
            Integer series number (2 for Series 2, 3 for Series 3)
        """
        return (
            cls.DEVICE_DATABASE.get(model, {}).get("device_info", {}).get("series", 0)
        )

    @classmethod
    def get_device_info(cls, model: str) -> Dict[str, Any]:
        """
        Get complete device information.

        Args:
            model: Hardware model string

        Returns:
            Dictionary with device info (series, model, hardware_model, serial_number)
        """
        return cls.DEVICE_DATABASE.get(model, {}).get("device_info", {})

    @classmethod
    def get_capabilities(cls, model: str) -> Dict[str, Any]:
        """
        Get device capabilities.

        Args:
            model: Hardware model string

        Returns:
            Dictionary with capabilities (ptp, network, outputs, etc.)
        """
        return cls.DEVICE_DATABASE.get(model, {}).get("capabilities", {})

    @classmethod
    def get_performance_baseline(cls, model: str) -> Dict[str, Any]:
        """
        Get performance baseline expectations.

        Args:
            model: Hardware model string

        Returns:
            Dictionary with performance expectations
        """
        return cls.DEVICE_DATABASE.get(model, {}).get("performance_baseline", {})

    @classmethod
    def get_network_config(cls, model: str) -> Dict[str, Any]:
        """
        Get network configuration details.

        Args:
            model: Hardware model string

        Returns:
            Dictionary with network configuration
        """
        return cls.DEVICE_DATABASE.get(model, {}).get("network_config", {})

    @classmethod
    def get_known_issues(cls, model: str) -> List[str]:
        """
        Get known issues for this device model.

        Args:
            model: Hardware model string

        Returns:
            List of known issues
        """
        return cls.DEVICE_DATABASE.get(model, {}).get("known_issues", [])

    @classmethod
    def get_output_signal_types(cls, model: str, output_num: int) -> List[str]:
        """
        Get available signal types for a specific output on a specific model.

        Args:
            model: Hardware model string
            output_num: Output number (1-6)

        Returns:
            List of available signal types for this output
        """
        output_types = cls.DEVICE_DATABASE.get(model, {}).get("output_signal_types", {})
        return output_types.get(output_num, [])

    @classmethod
    def get_time_reference_rules(cls, model: str) -> Dict[str, List[str]]:
        """
        Get time reference visibility rules for a model.

        Args:
            model: Hardware model string

        Returns:
            Dictionary mapping signal patterns to visible time references
        """
        return cls.DEVICE_DATABASE.get(model, {}).get("time_reference_rules", {})

    # Convenience methods for common queries

    @classmethod
    def is_ptp_supported(cls, model: str) -> bool:
        """Check if PTP is supported on this model."""
        return cls.get_capabilities(model).get("ptp_supported", False)

    @classmethod
    def get_max_outputs(cls, model: str) -> int:
        """Get maximum output count for this model."""
        return cls.get_capabilities(model).get("max_outputs", 0)

    @classmethod
    def get_network_interfaces(cls, model: str) -> List[str]:
        """Get network interface names for this model."""
        return cls.get_capabilities(model).get("interface_names", [])

    @classmethod
    def get_ptp_interfaces(cls, model: str) -> List[str]:
        """Get PTP-capable interfaces for this model."""
        return cls.get_capabilities(model).get("ptp_interfaces", [])

    @classmethod
    def get_session_timeout(cls, model: str) -> int:
        """Get session timeout in minutes for this model."""
        return cls.get_performance_baseline(model).get("session_timeout_minutes", 30)

    @classmethod
    def get_gnss_constellations(cls, model: str) -> List[str]:
        """Get supported GNSS constellations for this model."""
        return cls.get_capabilities(model).get("gnss_constellations", [])

    @classmethod
    def get_series_number(cls, model: str) -> int:
        """Get series number for this model."""
        return cls.get_device_info(model).get("series", 0)

    @classmethod
    def get_all_models(cls) -> List[str]:
        """Get list of all known device models."""
        return list(cls.DEVICE_DATABASE.keys())

    @classmethod
    def validate_device_config(
        cls, model: str, output_num: int, signal_type: str
    ) -> bool:
        """
        Validate that a signal type is available on a specific output for a model.

        Args:
            model: Hardware model string
            output_num: Output number (1-6)
            signal_type: Signal type to validate

        Returns:
            True if valid, False otherwise
        """
        available_types = cls.get_output_signal_types(model, output_num)
        return signal_type in available_types

    @classmethod
    def get_expected_time_refs(cls, model: str, signal_type: str) -> List[str]:
        """
        Get expected visible time references for a signal type on a model.

        Args:
            model: Hardware model string
            signal_type: Signal type

        Returns:
            List of expected visible time references
        """
        rules = cls.get_time_reference_rules(model)

        # Check for pattern matches
        for pattern, time_refs in rules.items():
            if pattern.endswith("*"):
                base_pattern = pattern[:-1]  # Remove *
                if signal_type.startswith(base_pattern):
                    return time_refs
            elif signal_type == pattern:
                return time_refs

        return ["UTC", "LOCAL"]  # Default fallback

    @classmethod
    def get_timezone_data(cls, model: str) -> Dict[str, Any]:
        """
        Get timezone configuration data for a model.

        Args:
            model: Hardware model string

        Returns:
            Dictionary with timezone data (available_timezones, mapping, count, includes_utc)
        """
        return cls.DEVICE_DATABASE.get(model, {}).get("timezone_data", {})

    @classmethod
    def get_available_timezones(cls, model: str) -> List[str]:
        """
        Get list of available timezones for a model.

        Args:
            model: Hardware model string

        Returns:
            List of available timezone names
        """
        timezone_data = cls.get_timezone_data(model)
        return timezone_data.get("available_timezones", [])

    @classmethod
    def get_timezone_mapping(cls, model: str) -> Dict[str, str]:
        """
        Get timezone mapping for a model.

        Args:
            model: Hardware model string

        Returns:
            Dictionary mapping display names to canonical timezone names
        """
        timezone_data = cls.get_timezone_data(model)
        return timezone_data.get("timezone_mapping", {})

    @classmethod
    def get_behavior_data(cls, model: str) -> Dict[str, Any]:
        """
        Get device-specific behavior data including UI patterns and authentication workflows.

        Args:
            model: Hardware model string

        Returns:
            Dictionary with behavioral data (authentication, navigation, dynamic behaviors, etc.)
        """
        return cls.DEVICE_DATABASE.get(model, {}).get("behavior_data", {})

    @classmethod
    def get_authentication_workflow(cls, model: str) -> Dict[str, Any]:
        """
        Get authentication workflow patterns for this device model.

        Args:
            model: Hardware model string

        Returns:
            Dictionary with authentication workflow details
        """
        behavior_data = cls.get_behavior_data(model)
        return behavior_data.get("authentication_workflow", {})

    @classmethod
    def get_navigation_patterns(cls, model: str) -> Dict[str, Any]:
        """
        Get navigation patterns and dashboard structure for this device model.

        Args:
            model: Hardware model string

        Returns:
            Dictionary with navigation pattern details
        """
        behavior_data = cls.get_behavior_data(model)
        return behavior_data.get("navigation_patterns", {})

    @classmethod
    def get_state_transition_timing(cls, model: str) -> Dict[str, Any]:
        """
        Get state transition timing expectations for this device model.

        Args:
            model: Hardware model string

        Returns:
            Dictionary with timing expectations for state transitions
        """
        behavior_data = cls.get_behavior_data(model)
        return behavior_data.get("state_transition_timing", {})

    @classmethod
    def get_dynamic_ui_behaviors(cls, model: str) -> Dict[str, Any]:
        """
        Get dynamic UI behavior patterns for this device model.

        Args:
            model: Hardware model string

        Returns:
            Dictionary with dynamic UI behavior details
        """
        behavior_data = cls.get_behavior_data(model)
        return behavior_data.get("dynamic_ui_behaviors", {})

    @classmethod
    def get_satellite_loading_behavior(cls, model: str) -> Dict[str, Any]:
        """
        Get satellite loading behavior patterns for this device model.

        Args:
            model: Hardware model string

        Returns:
            Dictionary with satellite loading behavior details
        """
        behavior_data = cls.get_behavior_data(model)
        return behavior_data.get("satellite_loading_behavior", {})

    @classmethod
    def get_performance_expectations(cls, model: str) -> Dict[str, Any]:
        """
        Get comprehensive performance expectations for this device model.

        Args:
            model: Hardware model string

        Returns:
            Dictionary with performance timing expectations
        """
        behavior_data = cls.get_behavior_data(model)
        return behavior_data.get("performance_expectations", {})

    @classmethod
    def get_timezone_count(cls, model: str) -> int:
        """
        Get timezone count for a model.

        Args:
            model: Hardware model string

        Returns:
            Number of available timezones
        """
        timezone_data = cls.get_timezone_data(model)
        return timezone_data.get("timezone_count", 0)

    @classmethod
    def is_utc_included(cls, model: str) -> bool:
        """
        Check if UTC is included in available timezones.

        Args:
            model: Hardware model string

        Returns:
            True if UTC is available, False otherwise
        """
        timezone_data = cls.get_timezone_data(model)
        return timezone_data.get("includes_utc", False)

    @classmethod
    def validate_timezone_selection(cls, model: str, timezone: str) -> bool:
        """
        Validate that a timezone is available for a model.

        Args:
            model: Hardware model string
            timezone: Timezone to validate

        Returns:
            True if valid, False otherwise
        """
        available_timezones = cls.get_available_timezones(model)
        return timezone in available_timezones

    @classmethod
    def get_timeout_multiplier(cls, model: str) -> float:
        """
        Get device-specific timeout multiplier based on known issues.

        Args:
            model: Hardware model string

        Returns:
            Timeout multiplier (1.0 = normal, >1.0 = extended for problematic devices)
        """
        # Handle unknown device model gracefully
        if not model or model == "Unknown":
            return 1.0

        known_issues = cls.get_known_issues(model)

        # Check for specific timeout-related issues
        for issue in known_issues:
            issue_lower = issue.lower()
            if "timeout" in issue_lower or "navigation" in issue_lower:
                return 2.0  # 2x timeout for devices with timeout issues
            elif "ptp" in issue_lower or "multi-interface" in issue_lower:
                return 1.5  # 1.5x timeout for PTP/interface complexity

        # Default multiplier for devices without specific timeout issues
        return 1.0

    # ================================================
    # DEVICE-SPECIFIC SAVE BUTTON PATTERNS
    # ================================================
    # CORRECTED: Based on actual device exploration data
    # Series 2 devices use generic buttons, Series 3 devices use interface-specific buttons

    SAVE_BUTTON_PATTERNS = {
        # Series 2 devices - Single interface, generic save button
        "series_2": {
            "generic": {
                "selector": "button#button_save",
                "description": "Generic save button for all Series 2 configurations",
                "section_fields": ["all_fields"],
                "panel_expansion_required": False,
            }
        },
        # Series 3 devices - Multi-interface, interface-specific buttons
        "series_3": {
            "network_configuration": {
                "eth0": {
                    "selector": "button#button_save_port_eth0",
                    "description": "Save button for eth0 (management interface)",
                    "section_fields": [
                        "ip",
                        "mask",
                        "mtu",
                        "ntp",
                        "snmp",
                        "vlan",
                        "changeip",
                    ],
                    "panel_expansion_required": False,
                },
                "eth1": {
                    "selector": "button#button_save_port_eth1",
                    "description": "Save button for eth1 (high-availability with PTP)",
                    "section_fields": [
                        "ip",
                        "mask",
                        "mtu",
                        "redundancy",
                        "ntp",
                        "ptp",
                        "snmp",
                        "vlan",
                    ],
                    "panel_expansion_required": False,
                },
                "eth2": {
                    "selector": "button#button_save_port_eth2",
                    "description": "Save button for eth2 (high-availability with PTP)",
                    "section_fields": [
                        "ip",
                        "mask",
                        "mtu",
                        "redundancy",
                        "ntp",
                        "ptp",
                        "snmp",
                        "vlan",
                    ],
                    "panel_expansion_required": False,
                },
                "eth3": {
                    "selector": "button#button_save_port_eth3",
                    "description": "Save button for eth3 (high-availability with PTP)",
                    "section_fields": [
                        "ip",
                        "mask",
                        "mtu",
                        "redundancy",
                        "ntp",
                        "ptp",
                        "snmp",
                        "vlan",
                    ],
                    "panel_expansion_required": False,
                },
                "eth4": {
                    "selector": "button#button_save_port_eth4",
                    "description": "Save button for eth4 (high-availability with PTP)",
                    "section_fields": [
                        "ip",
                        "mask",
                        "mtu",
                        "redundancy",
                        "ntp",
                        "ptp",
                        "snmp",
                        "vlan",
                    ],
                    "panel_expansion_required": False,
                },
            },
            "ptp_configuration": {
                "eth1": {
                    "selector": "button#button_save_port_eth1",
                    "description": "Save button for eth1 PTP settings",
                    "section_fields": [
                        "ptp_profile",
                        "domain",
                        "priority",
                        "transport",
                        "multicast",
                    ],
                    "panel_expansion_required": True,  # PTP panels start collapsed
                },
                "eth2": {
                    "selector": "button#button_save_port_eth2",
                    "description": "Save button for eth2 PTP settings",
                    "section_fields": [
                        "ptp_profile",
                        "domain",
                        "priority",
                        "transport",
                        "multicast",
                    ],
                    "panel_expansion_required": True,  # PTP panels start collapsed
                },
                "eth3": {
                    "selector": "button#button_save_port_eth3",
                    "description": "Save button for eth3 PTP settings",
                    "section_fields": [
                        "ptp_profile",
                        "domain",
                        "priority",
                        "transport",
                        "multicast",
                    ],
                    "panel_expansion_required": True,  # PTP panels start collapsed
                },
                "eth4": {
                    "selector": "button#button_save_port_eth4",
                    "description": "Save button for eth4 PTP settings",
                    "section_fields": [
                        "ptp_profile",
                        "domain",
                        "priority",
                        "transport",
                        "multicast",
                    ],
                    "panel_expansion_required": True,  # PTP panels start collapsed
                },
            },
            # Other configuration types use generic button
            "time_configuration": {
                "generic": {
                    "selector": "button#button_save",
                    "description": "Generic save button for time configuration",
                    "section_fields": ["timezone", "time_reference", "daylight_saving"],
                    "panel_expansion_required": False,
                }
            },
            "outputs_configuration": {
                "generic": {
                    "selector": "button#button_save",
                    "description": "Generic save button for outputs configuration",
                    "section_fields": ["signal_type", "time_reference", "rate"],
                    "panel_expansion_required": False,
                }
            },
            "general_configuration": {
                "generic": {
                    "selector": "button#button_save",
                    "description": "Generic save button for general configuration",
                    "section_fields": ["device_name", "description", "location"],
                    "panel_expansion_required": False,
                }
            },
        },
    }

    @classmethod
    def get_interface_specific_save_button(
        cls, model: str, config_type: str, interface: str
    ) -> Dict[str, Any]:
        """
        Get device-specific save button information based on hardware model and configuration type.

        This method demonstrates WHY both hardware model and configuration type parameters are essential:
        - Same config type, different hardware = different buttons
        - Same hardware, different config types = different buttons

        Args:
            model: Hardware model string (e.g., "KRONOS-3R-HVLV-TCXO-A2F")
            config_type: Configuration type ("network_configuration", "ptp_configuration", etc.)
            interface: Network interface name (e.g., "eth1", "eth2") - required for Series 3 multi-interface

        Returns:
            Dictionary with save button information including:
            - selector: CSS selector for the save button
            - description: Human-readable description
            - section_fields: Fields affected by this save action
            - panel_expansion_required: Whether UI panel needs expansion before clicking
        """
        device_series = cls.get_series(model)

        # Handle Series 2 devices (single interface, generic buttons)
        if device_series == 2:
            if config_type in cls.SAVE_BUTTON_PATTERNS["series_2"]:
                return cls.SAVE_BUTTON_PATTERNS["series_2"][config_type]
            else:
                # Default fallback for Series 2
                return cls.SAVE_BUTTON_PATTERNS["series_2"]["generic"]

        # Handle Series 3 devices (multi-interface, interface-specific buttons)
        elif device_series == 3:
            if config_type not in cls.SAVE_BUTTON_PATTERNS["series_3"]:
                return {
                    "selector": "button#button_save",
                    "description": f"Generic save button for {config_type}",
                    "section_fields": ["all_fields"],
                    "panel_expansion_required": False,
                }

            config_patterns = cls.SAVE_BUTTON_PATTERNS["series_3"][config_type]

            # For interface-specific configurations (network, PTP)
            if interface and interface in config_patterns:
                return config_patterns[interface]

            # For non-interface-specific configurations or missing interface
            elif "generic" in config_patterns:
                return config_patterns["generic"]
            else:
                # Fallback - try to find any available interface
                first_interface = next(iter(config_patterns))
                return config_patterns[first_interface]

        # Unknown device series - return generic fallback
        return {
            "selector": "button#button_save",
            "description": "Generic fallback save button",
            "section_fields": ["all_fields"],
            "panel_expansion_required": False,
        }

    @classmethod
    def get_available_network_interfaces(cls, model: str) -> List[str]:
        """
        Get list of available network interfaces for a device model.

        Args:
            model: Hardware model string

        Returns:
            List of network interface names
        """
        return cls.get_network_interfaces(model)

    @classmethod
    def get_available_ptp_interfaces(cls, model: str) -> List[str]:
        """
        Get list of PTP-capable interfaces for a device model.

        Args:
            model: Hardware model string

        Returns:
            List of PTP-capable interface names
        """
        return cls.get_ptp_interfaces(model)

    @classmethod
    def get_available_sections(cls, model: str) -> List[str]:
        """
        Get available configuration sections for a device model.

        This method was causing AttributeError across 25+ tests in general config,
        access config, and dashboard modules.

        Args:
            model: Hardware model string

        Returns:
            List of available configuration section names
        """
        if not model or model == "None":
            # Default fallback - return Series 2 sections
            return [
                "general",
                "network",
                "time",
                "gnss",
                "outputs",
                "display",
                "access",
                "snmp",
                "syslog",
            ]

        device_info = cls.get_device_info(model)
        series = device_info.get("series", 2)

        if series == 2:
            # Series 2 devices - basic configuration sections
            return [
                "general",
                "network",
                "time",
                "gnss",
                "outputs",
                "display",
                "access",
                "snmp",
                "syslog",
            ]
        elif series == 3:
            # Series 3 devices - includes PTP and upload sections
            return [
                "general",
                "network",
                "time",
                "gnss",
                "outputs",
                "display",
                "access",
                "snmp",
                "syslog",
                "upload",
                "ptp",
            ]
        else:
            # Unknown series - default to Series 2 sections
            return [
                "general",
                "network",
                "time",
                "gnss",
                "outputs",
                "display",
                "access",
                "snmp",
                "syslog",
            ]

    @classmethod
    def get_gnss_patterns(cls, model: str) -> Dict[str, Any]:
        """
        Get GNSS configuration patterns for a device model.

        This method provides device-specific GNSS patterns including constellation
        configurations, satellite detection patterns, and UI element mappings.

        Args:
            model: Hardware model string

        Returns:
            Dictionary with GNSS patterns including constellation mappings,
            satellite detection methods, and configuration patterns
        """
        if not model or model == "None":
            # Default fallback patterns
            return {
                "constellation_patterns": {
                    "GPS": {"enabled_by_default": True, "checkbox_name": "gps_enabled"},
                    "GLONASS": {
                        "enabled_by_default": False,
                        "checkbox_name": "glonass_enabled",
                    },
                    "Galileo": {
                        "enabled_by_default": False,
                        "checkbox_name": "galileo_enabled",
                    },
                    "BeiDou": {
                        "enabled_by_default": False,
                        "checkbox_name": "beidou_enabled",
                    },
                },
                "satellite_detection": {
                    "satellite_types": ["GPS", "GLONASS", "Galileo", "BeiDou"],
                    "detection_methods": ["checkbox", "select", "radio"],
                    "status_indicators": ["Detected", "Tracking", "Locked"],
                },
                "gnss_configuration_patterns": {
                    "antenna_types": ["Active", "Passive"],
                    "satellite_field_selectors": [
                        "input[name*='satellite']",
                        "input[id*='satellite']",
                        ".satellite-field",
                    ],
                },
                "ui_element_patterns": {
                    "save_button_selectors": ["button#button_save"],
                    "cancel_button_selectors": ["button#button_cancel"],
                    "loading_indicators": ["Loading satellite data"],
                },
            }

        device_info = cls.get_device_info(model)
        series = device_info.get("series", 2)
        capabilities = cls.get_capabilities(model)
        gnss_constellations = capabilities.get("gnss_constellations", ["GPS"])

        # Base constellation patterns
        constellation_patterns = {}
        for constellation in gnss_constellations:
            constellation_patterns[constellation] = {
                "enabled_by_default": constellation
                == "GPS",  # GPS typically enabled by default
                "checkbox_name": f"{constellation.lower()}_enabled",
            }

        # Series-specific patterns
        if series == 2:
            return {
                "constellation_patterns": constellation_patterns,
                "satellite_detection": {
                    "satellite_types": gnss_constellations,
                    "detection_methods": ["select"],  # Series 2 uses select dropdown
                    "status_indicators": ["Detected", "Tracking", "Locked"],
                },
                "gnss_configuration_patterns": {
                    "antenna_types": ["Active", "Passive"],
                    "constellation_method": "select_dropdown",
                    "satellite_field_selectors": [
                        "input[name*='satellite']",
                        "input[id*='satellite']",
                        ".satellite-field",
                    ],
                },
                "ui_element_patterns": {
                    "save_button_selectors": ["button#button_save"],
                    "cancel_button_selectors": ["button#button_cancel"],
                    "loading_indicators": ["Loading satellite data"],
                },
                "device_specific": {
                    "series": 2,
                    "supports_multiple_constellations": False,
                    "constellation_selection_method": "single_select",
                },
            }
        elif series == 3:
            return {
                "constellation_patterns": constellation_patterns,
                "satellite_detection": {
                    "satellite_types": gnss_constellations,
                    "detection_methods": ["checkbox"],  # Series 3 uses checkboxes
                    "status_indicators": ["Detected", "Tracking", "Locked"],
                },
                "gnss_configuration_patterns": {
                    "antenna_types": ["Active", "Passive"],
                    "constellation_method": "multiple_checkboxes",
                    "satellite_field_selectors": [
                        "input[name*='satellite']",
                        "input[id*='satellite']",
                        ".satellite-field",
                        ".gnss-field",
                    ],
                },
                "ui_element_patterns": {
                    "save_button_selectors": ["button#button_save"],
                    "cancel_button_selectors": ["button#button_cancel"],
                    "loading_indicators": ["Loading satellite data"],
                },
                "device_specific": {
                    "series": 3,
                    "supports_multiple_constellations": True,
                    "constellation_selection_method": "multiple_checkboxes",
                },
            }
        else:
            # Unknown series - return generic patterns
            return {
                "constellation_patterns": constellation_patterns,
                "satellite_detection": {
                    "satellite_types": gnss_constellations,
                    "detection_methods": ["checkbox", "select"],
                    "status_indicators": ["Detected", "Tracking", "Locked"],
                },
                "gnss_configuration_patterns": {
                    "antenna_types": ["Active", "Passive"],
                    "satellite_field_selectors": [
                        "input[name*='satellite']",
                        "input[id*='satellite']",
                    ],
                },
                "ui_element_patterns": {
                    "save_button_selectors": ["button#button_save"],
                    "cancel_button_selectors": ["button#button_cancel"],
                    "loading_indicators": ["Loading satellite data"],
                },
                "device_specific": {
                    "series": series,
                    "supports_multiple_constellations": True,
                    "constellation_selection_method": "unknown",
                },
            }
