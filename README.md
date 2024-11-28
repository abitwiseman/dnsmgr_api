# dnsmgr_api

`dnsmgr_api` is a Python library to configure `named` (BIND) and `dnsmasq` on remote servers via SSH.

## Installation

You can install the package directly from the source:

```bash
git clone https://github.com/abitwiseman/dnsmgr_api.git
cd dnsmgr_api
pip install .
```

Usage
DNS Management
```python
from dnsmgr_api import DNSManager

# Initialize DNSManager
dns_manager = DNSManager(server_ip="10.10.0.1", username="root", password="password")

# Create a DNS zone
dns_manager.create_zone(
    domain="example.com",
    master_ip="192.168.1.1"
)

# Add records to the zone
dns_manager.add_records(
    domain="example.com",
    records=[
        {"type": "A", "name": "www", "value": "192.168.1.1"},
        {"type": "CNAME", "name": "alias", "value": "www.example.com."}
    ]
)
```
Dnsmasq Configuration
```python
from dnsmgr_api import DnsmasqManager

# Initialize DnsmasqManager
dnsmasq_manager = DnsmasqManager(server_ip="10.10.0.2", username="root", password="password")

# Configure dnsmasq with an upstream server
dnsmasq_manager.configure_dnsmasq(upstream_server="8.8.8.8")
```