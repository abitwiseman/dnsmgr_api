"""
dnsmgr_api - A Python library for managing DNS configurations via SSH.

This package provides:
- DNSManager: To configure `named` (BIND) and manage DNS zones.
- DnsmasqManager: To configure `dnsmasq`.

Author: Your Name
Email: your.email@example.com
Version: 1.0.0
"""

from .dns_config import DNSManager, DnsmasqManager

__version__ = "1.0.0"
__all__ = ["DNSManager", "DnsmasqManager"]
