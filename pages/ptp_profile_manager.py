"""
PTP Profile Manager for Kronos device test automation.

Handles PTP profile field constraints and readonly status determination.
Extracted from ptp_config_page.py for better separation of concerns.

Provides:
- Profile constraint data for all Kronos PTP profiles
- Field readonly status determination based on profile selection
- Reusable logic for PTP profile field behavior validation
"""

from typing import Dict, Any, Optional


class PTPProfileManager:
    """
    Integrated PTP profile management for Kronos device configuration.

    Handles PTP profile field constraints and readonly status determination
    directly within the page object without requiring external utilities.
    """

    def __init__(self):
        """Initialize with built-in profile constraints."""
        self.profile_data = self._get_builtin_profile_data()

    def _get_builtin_profile_data(self) -> Dict[str, Dict[str, Any]]:
        """
        Return built-in profile data with field constraints.

        This contains the profile field constraints known from device exploration.
        """
        return {
            "profiles": {
                "IEEE C37.238-2011 (Power Profile)": {
                    "priority1": {
                        "hidden": False,
                        "grayedout": True,
                        "defaultValue": 128,
                    },
                    "priority2": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                },
                "IEEE C37.238-2017 (Power Profile)": {
                    "priority1": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                    "priority2": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                },
                "IEEC 61850-9-3:2016 (Utility Profile)": {
                    "priority1": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                    "priority2": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                },
                "Default Profile (UDPv4)": {
                    "priority1": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                    "priority2": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                },
                "Default Profile (802.3)": {
                    "priority1": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                    "priority2": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                },
                "Telecom G.8265.1 (frequency synchronization)": {
                    "priority1": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                    "priority2": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                },
                "Telecom G.8275.1 (phase/time synchronization with full timing support from the network)": {
                    "priority1": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                    "priority2": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                },
                "Telecom G.8275.2 (time/phase synchronization with partial timing support from the network)": {
                    "priority1": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                    "priority2": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                },
                "Custom": {
                    "priority1": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                    "priority2": {
                        "hidden": False,
                        "grayedout": False,
                        "defaultValue": 128,
                    },
                },
            }
        }

    def is_field_readonly(self, profile_name: str, field_name: str) -> bool:
        """
        Check if a field is read-only for a given profile.

        Args:
            profile_name: Name of the PTP profile
            field_name: Name of the field

        Returns:
            True if field is read-only (grayed out), False otherwise
        """
        try:
            profiles = self.profile_data.get("profiles", {})

            if profile_name not in profiles:
                print(f"Profile '{profile_name}' not found, defaulting to editable")
                return False

            profile_config = profiles[profile_name]

            if field_name not in profile_config:
                print(
                    f"Field '{field_name}' not found in profile '{profile_name}', defaulting to editable"
                )
                return False

            return profile_config[field_name].get("grayedout", False)

        except Exception as e:
            print(f"Error checking field readonly status: {e}")
            return False

    def get_profile_constraints(self, profile_name: str) -> Dict[str, Any]:
        """
        Get all field constraints for a specific profile.

        Args:
            profile_name: Name of the PTP profile

        Returns:
            Dictionary of field constraints for the profile
        """
        try:
            profiles = self.profile_data.get("profiles", {})

            if profile_name not in profiles:
                print(f"Profile '{profile_name}' not found")
                return {}

            return profiles[profile_name]

        except Exception as e:
            print(f"Error getting profile constraints for '{profile_name}': {e}")
            return {}

    def get_available_profiles(self) -> list[str]:
        """
        Get list of all available PTP profiles.

        Returns:
            List of profile names
        """
        try:
            profiles = self.profile_data.get("profiles", {})
            return list(profiles.keys())
        except Exception as e:
            print(f"Error getting available profiles: {e}")
            return []

    def validate_profile_exists(self, profile_name: str) -> bool:
        """
        Validate that a profile exists in the profile data.

        Args:
            profile_name: Name of the profile to validate

        Returns:
            True if profile exists, False otherwise
        """
        try:
            profiles = self.profile_data.get("profiles", {})
            return profile_name in profiles
        except Exception as e:
            print(f"Error validating profile existence: {e}")
            return False

    def get_field_default_value(
        self, profile_name: str, field_name: str
    ) -> Optional[int]:
        """
        Get the default value for a field in a specific profile.

        Args:
            profile_name: Name of the PTP profile
            field_name: Name of the field

        Returns:
            Default value for the field, or None if not found
        """
        try:
            field_config = self.get_profile_constraints(profile_name).get(field_name)
            if field_config:
                return field_config.get("defaultValue")
            return None
        except Exception as e:
            print(
                f"Error getting default value for field '{field_name}' in profile '{profile_name}': {e}"
            )
            return None
