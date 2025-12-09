"""
Page objects for Kronos device test automation.

This package contains page object implementations for all Kronos device pages,
following the established patterns from the memory bank.
"""

from .base import BasePage

# Import all page objects for easy access
from .login_page import LoginPage
from .dashboard_page import DashboardPage
from .configuration_unlock_page import ConfigurationUnlockPage
from .time_config_page import TimeConfigPage
from .network_config_page import NetworkConfigPage
from .outputs_config_page import OutputsConfigPage
from .snmp_config_page import SNMPConfigPage
from .display_config_page import DisplayConfigPage
from .upload_config_page import UploadConfigPage

__all__ = [
    "BasePage",
    "LoginPage",
    "DashboardPage",
    "ConfigurationUnlockPage",
    "TimeConfigPage",
    "NetworkConfigPage",
    "OutputsConfigPage",
    "SNMPConfigPage",
    "DisplayConfigPage",
    "UploadConfigPage",
]
