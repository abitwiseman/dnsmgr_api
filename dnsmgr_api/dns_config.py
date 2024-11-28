import paramiko
import subprocess


class DNSManager:
    def __init__(self, server_ip, username, password, named_conf="/etc/named.conf"):
        """
        Initialize DNSManager with server credentials and named configuration file path.
        """
        self.server_ip = server_ip
        self.username = username
        self.password = password
        self.named_conf = named_conf

    def _ssh_execute(self, commands):
        """
        Execute a list of commands on a remote server via SSH.
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.server_ip, username=self.username, password=self.password)

            for command in commands:
                print(f"Executing: {command}")
                stdin, stdout, stderr = ssh.exec_command(command)
                print(stdout.read().decode().strip())
                error = stderr.read().decode().strip()
                if error:
                    print(f"Error: {error}")
            ssh.close()
        except Exception as e:
            print(f"Failed to execute commands: {e}")

    def is_zone_present(self, domain):
        """
        Check if the zone is already present in named.conf.
        """
        command = f"grep -q 'zone \"{domain}\"' {self.named_conf} && echo 'exists' || echo 'not_found'"
        result = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return "exists" in result.stdout

    def create_zone(self, domain, ttl=86400):
        """
        Create a DNS zone with basic SOA and NS records.
        """
        zone_file = f"/var/named/db.{domain}"

        # Check if the zone already exists
        if self.is_zone_present(domain):
            print(f"Zone {domain} already exists in named.conf. Skipping creation.")
            return

        # Add zone to named.conf
        zone_entry = f'zone "{domain}" {{ type master; file "{zone_file}"; }};\n'
        commands = [
            f"echo '{zone_entry}' >> {self.named_conf}",
            f"touch {zone_file}",  # Ensure the zone file exists
        ]

        # Add zone file with SOA and NS records
        zone_header = f"""
$TTL {ttl}
@   IN  SOA ns1.yourdomain.com. admin.yourdomain.com. (
            2023112601  ; Serial
            7200        ; Refresh
            3600        ; Retry
            2419200     ; Expire
            86400 )     ; Negative Cache TTL

; Name servers
@   IN  NS  ns1.yourdomain.com.
"""
        commands.append(f"echo '{zone_header}' > {zone_file}")

        # Execute the commands
        self._ssh_execute(commands)

        print(f"Zone {domain} created successfully with master_vm as the primary name server.")

    def add_records(self, domain, records):
        """
        Add multiple DNS records to a zone file.

        :param domain: The domain of the zone.
        :param records: List of dictionaries with record details.
                        Example: [
                            {"type": "A", "name": "www", "value": "192.168.1.1"},
                            {"type": "CNAME", "name": "alias", "value": "www.example.com."}
                        ]
        """
        zone_file = f"/var/named/db.{domain}"

        # Build record entries
        record_entries = []
        for record in records:
            record_entries.append(f"{record['name']} IN {record['type']} {record['value']}")

        # Append records to the zone file
        commands = [f"echo '{entry}' >> {zone_file}" for entry in record_entries]
        self._ssh_execute(commands)

        print(f"Added {len(records)} record(s) to zone {domain}.")

    def delete_zone(self, domain):
        """
        Delete a DNS zone and remove it from named.conf.
        """
        zone_file = f"/var/named/db.{domain}"

        # Remove zone entry from named.conf
        commands = [
            f"sed -i '/zone \"{domain}\"/,+2d' {self.named_conf}",
            f"rm -f {zone_file}",  # Remove the zone file
        ]

        # Execute the commands
        self._ssh_execute(commands)

        # Restart named service
        self._ssh_execute(["systemctl restart named"])
        print(f"Zone {domain} deleted successfully.")

    def restart_named(self):
        """
        Restart the named service.
        """

        # Restart named service
        self._ssh_execute(["systemctl restart named"])

class DnsmasqManager:
    def __init__(self, server_ip, username, password, dnsmasq_conf="/etc/dnsmasq.conf"):
        """
        Initialize DnsmasqManager with server credentials and dnsmasq configuration file path.
        """
        self.server_ip = server_ip
        self.username = username
        self.password = password
        self.dnsmasq_conf = dnsmasq_conf

    def _ssh_execute(self, commands):
        """
        Execute a list of commands on a remote server via SSH.
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.server_ip, username=self.username, password=self.password)

            for command in commands:
                print(f"Executing: {command}")
                stdin, stdout, stderr = ssh.exec_command(command)
                print(stdout.read().decode().strip())
                error = stderr.read().decode().strip()
                if error:
                    print(f"Error: {error}")
            ssh.close()
        except Exception as e:
            print(f"Failed to execute commands: {e}")

    def configure_dnsmasq(self, upstream_server, cache_size=0):
        """
        Configure dnsmasq to use the specified upstream DNS server.
        """
        commands = [
            f"echo -e 'server={upstream_server}\ncache-size={cache_size}' > {self.dnsmasq_conf}"
            "systemctl enable dnsmasq",
            "systemctl restart dnsmasq"
        ]
        self._ssh_execute(commands)
        print("dnsmasq configured successfully.")


# Example Usage
if __name__ == "__main__":
    dns_manager = DNSManager(server_ip="192.168.1.100", username="root", password="password")

    # Create a DNS zone
    dns_manager.create_zone(
        domain="example.com",
    )

    # Add multiple records to the zone
    dns_manager.add_records(
        domain="example.com",
        records=[
            {"type": "A", "name": "www", "value": "192.168.1.1"},
            {"type": "A", "name": "mail", "value": "192.168.1.2"},
            {"type": "CNAME", "name": "alias", "value": "www.example.com."}
        ]
    )

    # Delete the zone
    # dns_manager.delete_zone(domain="example.com")

    # Configure dnsmasq
    dnsmasq_manager = DnsmasqManager(server_ip="192.168.1.100", username="root", password="password")
    dnsmasq_manager.configure_dnsmasq(upstream_server="8.8.8.8")
