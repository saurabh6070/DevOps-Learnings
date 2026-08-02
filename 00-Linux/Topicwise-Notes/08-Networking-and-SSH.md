# Networking, SSH, Firewall, and Routing

> Extracted from [00-Linux/01-Introduction.md](../01-Introduction.md)
>
> Covers source sections 27-32 from the original Linux introduction note.

## 27. 🌐 Networking in Linux

### 27.1 Network Interfaces

```bash
# View interfaces:
ip addr                          # All interfaces with IPs (modern)
ip addr show eth0                # Specific interface
ip link show                     # Link layer info
ifconfig                         # Older tool (net-tools package)
ifconfig eth0                    # Specific interface

# Interface management:
ip link set eth0 up              # Bring interface up
ip link set eth0 down            # Bring interface down
ip addr add 192.168.1.100/24 dev eth0    # Add IP address
ip addr del 192.168.1.100/24 dev eth0   # Remove IP address
ip addr flush dev eth0           # Remove all IPs from interface

# Rename interface:
ip link set eth0 name lan0
```

### 27.2 Routing

```bash
# View routing table:
ip route                         # Current routes
ip route show                    # Same
route -n                         # Older command (shows numeric IPs)
netstat -rn                      # Routing table (older)

# Add/remove routes:
ip route add 192.168.2.0/24 via 192.168.1.1    # Add route
ip route add default via 192.168.1.1            # Add default gateway
ip route del 192.168.2.0/24                     # Delete route
ip route replace default via 192.168.1.254      # Change default gateway
```

### 27.3 DNS Configuration

```bash
# DNS resolution:
cat /etc/resolv.conf             # DNS servers
cat /etc/hosts                   # Local hostname resolution

# Edit DNS (modern — NetworkManager):
nmcli con mod eth0 ipv4.dns "8.8.8.8 8.8.4.4"
nmcli con mod eth0 ipv4.ignore-auto-dns yes

# Test DNS:
nslookup google.com              # Basic DNS lookup
nslookup google.com 8.8.8.8     # Use specific DNS server
dig google.com                   # Detailed DNS lookup
dig google.com @8.8.8.8          # Use specific DNS server
dig MX gmail.com                 # Look up MX records
host google.com                  # Simple DNS lookup
```

### 27.4 Network Diagnostics

```bash
# Connectivity tests:
ping google.com                  # ICMP ping
ping -c 4 google.com             # Ping 4 times
ping -i 0.5 google.com           # Ping every 0.5 seconds
ping6 google.com                 # IPv6 ping
ping -I eth0 google.com          # Ping via specific interface

# Traceroute — path to destination:
traceroute google.com            # Show hops to destination
tracepath google.com             # traceroute alternative (no root needed)
mtr google.com                   # Real-time traceroute + ping stats

# Port testing:
telnet 192.168.1.10 80           # Test TCP port (Ctrl+] to exit)
nc -zv 192.168.1.10 80           # Netcat port test
nc -zv 192.168.1.10 1-1000       # Scan port range

# Connection info:
ss -tuln                         # All listening ports (modern)
ss -tulnp                        # Include process name
ss -s                            # Summary statistics
netstat -tuln                    # Same (older)
netstat -tulnp                   # With process (older)

# Network statistics:
ip -s link                       # Interface stats (bytes/packets)
ip -s link show eth0             # Specific interface stats
sar -n DEV 1 5                   # Network I/O per second
nethogs                          # Bandwidth per process (install needed)
iftop                            # Real-time bandwidth monitor
```

### 27.5 NetworkManager

```bash
# nmcli — NetworkManager CLI:
nmcli general status             # Overall status
nmcli device status              # All devices
nmcli con show                   # All connections
nmcli con show --active          # Active connections
nmcli con up eth0                # Activate connection
nmcli con down eth0              # Deactivate connection
nmcli con reload                 # Reload all connections

# Configure static IP:
nmcli con mod "Wired connection 1" ipv4.addresses "192.168.1.100/24"
nmcli con mod "Wired connection 1" ipv4.gateway "192.168.1.1"
nmcli con mod "Wired connection 1" ipv4.dns "8.8.8.8"
nmcli con mod "Wired connection 1" ipv4.method manual
nmcli con up "Wired connection 1"

# Configure DHCP:
nmcli con mod "Wired connection 1" ipv4.method auto
nmcli con up "Wired connection 1"

# Hostname:
hostnamectl                      # View hostname and info
hostnamectl set-hostname myserver.example.com
```

### 27.6 Network Config Files

```bash
# Ubuntu/Debian — Netplan:
cat /etc/netplan/*.yaml
netplan apply                    # Apply netplan config

# Example netplan config:
# /etc/netplan/01-netcfg.yaml
# network:
#   version: 2
#   ethernets:
#     eth0:
#       addresses: [192.168.1.100/24]
#       gateway4: 192.168.1.1
#       nameservers:
#         addresses: [8.8.8.8]

# RHEL/CentOS — ifcfg files:
ls /etc/sysconfig/network-scripts/
cat /etc/sysconfig/network-scripts/ifcfg-eth0
# TYPE=Ethernet
# BOOTPROTO=static
# IPADDR=192.168.1.100
# NETMASK=255.255.255.0
# GATEWAY=192.168.1.1
# DNS1=8.8.8.8
# ONBOOT=yes
```

---

## 28. 🌐 Networking in Linux — LAN, WAN, OSI, and Configuration Files

### 28.1 LAN vs WAN

| Type | Full Name | Description | Range |
|------|-----------|-------------|-------|
| **LAN** | Local Area Network | Devices on the same physical/logical network | Room, building, campus |
| **WAN** | Wide Area Network | Networks connected across large distances | City, country, internet |
| **MAN** | Metropolitan Area Network | City-wide network | City |
| **VLAN** | Virtual LAN | Logical segmentation of LAN | Software-defined |

### 28.2 OSI Model — 7 Layers

```
7 │ Application  │ HTTP, FTP, SSH, DNS, SMTP, SNMP
  ├──────────────┤
6 │ Presentation │ SSL/TLS, encryption, compression, encoding
  ├──────────────┤
5 │ Session      │ Manages sessions, authentication
  ├──────────────┤
4 │ Transport    │ TCP, UDP — ports, flow control, error correction
  ├──────────────┤
3 │ Network      │ IP, ICMP, routing — logical addressing
  ├──────────────┤
2 │ Data Link    │ Ethernet, MAC addresses, switches, ARP
  ├──────────────┤
1 │ Physical     │ Cables, hubs, bits, NIC, signals
```

**Remember:** "**A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing" (top-down)

| Layer | Protocol Examples | Linux Tools |
|-------|------------------|-------------|
| 7 Application | HTTP, DNS, SSH | curl, dig, ssh |
| 4 Transport | TCP, UDP | ss, netstat |
| 3 Network | IP, ICMP | ip, ping, traceroute |
| 2 Data Link | Ethernet, ARP | arp, ip link |
| 1 Physical | Ethernet cable | ethtool, mii-tool |

### 28.3 Types of Casting (Communication Modes)

| Type | Description | Example |
|------|-------------|---------|
| **Unicast** | One-to-One | SSH, HTTP, HTTPS |
| **Broadcast** | One-to-All (same subnet) | ARP requests, DHCP discover |
| **Multicast** | One-to-Many (subscribed group) | Streaming, routing protocols (OSPF) |
| **Anycast** | One-to-Nearest (from a group) | DNS root servers, CDN |

```bash
# Broadcast address: last address in subnet
# 192.168.1.0/24 → broadcast: 192.168.1.255

# Send broadcast message to all logged-in users:
wall "System will reboot in 5 minutes!"
broadcast -a "Maintenance window starting now"
```

### 28.4 RHEL Network Config Files — /etc/sysconfig/network-scripts/

```bash
# RHEL 7 and older — ifcfg files:
ls /etc/sysconfig/network-scripts/
cat /etc/sysconfig/network-scripts/ifcfg-eth0
```

```ini
TYPE=Ethernet
BOOTPROTO=static          # static, dhcp, or none
NAME=eth0
DEVICE=eth0
ONBOOT=yes                # ← KEY: yes=activate at boot, no=don't activate
IPADDR=192.168.1.100
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
DNS1=8.8.8.8
DNS2=8.8.4.4
IPV6INIT=no
NM_CONTROLLED=yes         # Managed by NetworkManager

# For DHCP:
# BOOTPROTO=dhcp
# Remove IPADDR, NETMASK, GATEWAY lines
```

```bash
# Restart network interface after changes:
ifdown eth0 && ifup eth0        # RHEL 7 and older
nmcli con reload && nmcli con up eth0   # With NetworkManager
```

### 28.5 NetworkManager in RHEL

```bash
# NetworkManager manages network connections dynamically:
systemctl status NetworkManager       # Status
systemctl enable --now NetworkManager # Enable + start

# nmcli — NetworkManager CLI:
nmcli general status                  # Overall status
nmcli device status                   # All interfaces
nmcli con show                        # All connections
nmcli con show --active               # Active connections
nmcli device show eth0                # Detailed interface info

# Create a static IP connection:
nmcli con add type ethernet con-name static-eth0 ifname eth0
nmcli con mod static-eth0 ipv4.addresses "192.168.1.100/24"
nmcli con mod static-eth0 ipv4.gateway "192.168.1.1"
nmcli con mod static-eth0 ipv4.dns "8.8.8.8 8.8.4.4"
nmcli con mod static-eth0 ipv4.method manual
nmcli con up static-eth0

# Switch to DHCP:
nmcli con mod eth0 ipv4.method auto
nmcli con up eth0

# View/edit connection profiles:
ls /etc/NetworkManager/system-connections/
nmcli con edit eth0

# Disable NetworkManager for an interface (use ifcfg instead):
# Add to ifcfg file:  NM_CONTROLLED=no
```

### 28.6 /etc/network/interfaces — Debian/Ubuntu (Older)

```bash
cat /etc/network/interfaces
```

```ini
# Loopback:
auto lo
iface lo inet loopback

# Static IP:
auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8 8.8.4.4

# DHCP:
auto eth0
iface eth0 inet dhcp
```

```bash
# Apply changes:
ifdown eth0 && ifup eth0
/etc/init.d/networking restart
```

### 28.7 Changing Hostname

```bash
# View current hostname:
hostname                              # Short hostname
hostname -f                           # FQDN (fully qualified domain name)
hostnamectl                           # Detailed info

# Change hostname:
hostnamectl set-hostname myserver.example.com   # Permanent (survives reboot)
hostname newname                                # Temporary (lost on reboot)

# Update /etc/hosts to reflect new name:
echo "127.0.1.1 myserver.example.com myserver" >> /etc/hosts

# Three types of hostname:
hostnamectl set-hostname myserver              # Static hostname
hostnamectl set-hostname "My Production Server" --pretty  # Pretty name
# Transient hostname (set by DHCP/mDNS, temporary)
```

### 28.8 /etc/hosts — Local Name Resolution

```bash
cat /etc/hosts
```

```
127.0.0.1     localhost
127.0.1.1     myserver.example.com myserver
192.168.1.101 web1.example.com web1
192.168.1.102 web2.example.com web2
192.168.1.103 db1.example.com db1

# Format: IP_address  canonical_name  [aliases...]
```

```bash
# Resolution order (checked in /etc/nsswitch.conf):
cat /etc/nsswitch.conf | grep hosts
# hosts: files dns        ← 'files' = /etc/hosts, then 'dns'
```

### 28.9 /etc/hosts.deny and /etc/hosts.allow — TCP Wrappers

```bash
# TCP Wrappers control access to services that support libwrap
cat /etc/hosts.allow       # Whitelist — checked FIRST
cat /etc/hosts.deny        # Blacklist — checked SECOND

# /etc/hosts.allow:
# sshd: 192.168.1.0/24           # Allow SSH from subnet
# ALL: LOCAL                      # Allow all local connections
# sshd: 10.0.0.5                  # Allow specific IP

# /etc/hosts.deny:
# ALL: ALL                         # Deny everything not explicitly allowed
# sshd: 10.0.0.100                # Block specific IP from SSH
# in.ftpd: ALL                    # Block all FTP access

# Rule: if in hosts.allow → ALLOW. Else if in hosts.deny → DENY. Else → ALLOW
```
---

## 29. 🔒 SSH & Remote Access

### 29.1 SSH Client

```bash
# Basic connections:
ssh user@hostname                  # Connect to remote host
ssh -p 2222 user@hostname          # Non-default port
ssh user@192.168.1.100             # By IP address
ssh -v user@hostname               # Verbose (debug connection issues)
ssh -X user@hostname               # X11 forwarding (run GUI apps)

# SSH key authentication:
ssh-keygen -t rsa -b 4096          # Generate RSA key pair
ssh-keygen -t ed25519              # Generate Ed25519 key (recommended)
ssh-keygen -t ed25519 -C "alice@example.com"  # With comment
# Keys stored in: ~/.ssh/id_ed25519 (private), ~/.ssh/id_ed25519.pub (public)

# Copy public key to remote server:
ssh-copy-id user@hostname          # Copies ~/.ssh/id_rsa.pub
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@hostname

# Manual method:
cat ~/.ssh/id_ed25519.pub | ssh user@host "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# SSH key permissions (CRITICAL):
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/id_ed25519        # Private key
chmod 644 ~/.ssh/id_ed25519.pub    # Public key
```

### 29.2 SSH Config File (~/.ssh/config)

```bash
# Create SSH client config for shortcuts:
cat ~/.ssh/config
```

```
Host myserver
    HostName 192.168.1.100
    User alice
    Port 2222
    IdentityFile ~/.ssh/id_ed25519

Host bastion
    HostName bastion.example.com
    User admin
    ForwardAgent yes

Host internal
    HostName 10.0.0.5
    User root
    ProxyJump bastion       # Jump through bastion host
```

```bash
# Now connect with shortcut:
ssh myserver               # Instead of: ssh -p 2222 alice@192.168.1.100
```

### 29.3 SCP and SFTP — Secure File Transfer

```bash
# SCP — Secure Copy:
scp file.txt user@host:/remote/path/      # Upload file
scp user@host:/remote/file.txt ./         # Download file
scp -r mydir/ user@host:/remote/          # Upload directory
scp -P 2222 file.txt user@host:/path/     # Non-default port

# SFTP — interactive:
sftp user@host
# Inside sftp:
# put localfile remotefile    → upload
# get remotefile localfile    → download
# ls, pwd, cd                 → navigate remote
# lls, lpwd, lcd              → navigate local
# quit                        → exit

# rsync — efficient sync:
rsync -avz localdir/ user@host:/remotedir/    # Sync local to remote
rsync -avz user@host:/remotedir/ localdir/    # Sync remote to local
rsync -avz --delete localdir/ user@host:/remotedir/  # Mirror (delete extras)
rsync -avzn localdir/ user@host:/remotedir/  # Dry run
```

### 29.4 SSH Server Configuration (/etc/ssh/sshd_config)

```bash
# Key sshd_config settings:
Port 22                              # Change to non-standard port
PermitRootLogin no                   # Disable root login (security!)
PasswordAuthentication no            # Disable password auth (key only)
PubkeyAuthentication yes             # Enable key auth
AllowUsers alice bob                 # Only allow specific users
DenyUsers nobody                     # Deny specific users
AllowGroups sshusers                 # Only allow group members
MaxAuthTries 3                       # Limit auth attempts
LoginGraceTime 60                    # Seconds to authenticate
ClientAliveInterval 300              # Timeout for idle connections
ClientAliveCountMax 2                # Max keepalive attempts
X11Forwarding no                     # Disable GUI forwarding (security)
Banner /etc/ssh/banner               # Show banner before login

# After changing sshd_config:
sshd -t                              # Test config (ALWAYS do this first!)
systemctl restart sshd               # Apply changes
```

### 29.5 SSH Tunneling

```bash
# Local port forwarding (access remote service locally):
ssh -L 8080:localhost:80 user@remote-host
# Now: curl http://localhost:8080 → accesses remote's port 80

# Remote port forwarding (expose local service remotely):
ssh -R 9090:localhost:3000 user@remote-host
# On remote: curl http://localhost:9090 → accesses your local port 3000

# Dynamic SOCKS proxy:
ssh -D 1080 user@remote-host
# Configure browser to use SOCKS5 proxy at localhost:1080
```

---

## 30. 🔐 Password-less SSH Authentication — Complete Setup

### 30.1 How Key-Based Auth Works

```
1. Admin generates key pair:  private key (secret) + public key (shareable)
2. Public key is copied to remote server's ~/.ssh/authorized_keys
3. On SSH connect: server sends challenge encrypted with public key
4. Only the holder of the PRIVATE key can decrypt it → proves identity
5. No password needed!
```

### 30.2 Step-by-Step Setup

```bash
# Step 1: Generate key pair (on CLIENT):
ssh-keygen -t ed25519 -C "alice@workstation"
# -t ed25519  = Ed25519 algorithm (recommended, faster than RSA)
# -C          = comment (optional, for identification)
# Creates: ~/.ssh/id_ed25519 (private) and ~/.ssh/id_ed25519.pub (public)

# For RSA (older systems):
ssh-keygen -t rsa -b 4096 -C "alice@workstation"

# With custom filename:
ssh-keygen -t ed25519 -f ~/.ssh/myserver_key

# Step 2: Copy public key to remote server:
ssh-copy-id alice@192.168.1.100                     # Default key
ssh-copy-id -i ~/.ssh/id_ed25519.pub alice@192.168.1.100  # Specific key
ssh-copy-id -p 2222 alice@192.168.1.100             # Custom port

# Manual method (when ssh-copy-id not available):
cat ~/.ssh/id_ed25519.pub | ssh alice@192.168.1.100 \
    "mkdir -p ~/.ssh && chmod 700 ~/.ssh && \
     cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# Step 3: Verify correct permissions (critical!):
# On REMOTE server:
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# Step 4: Test:
ssh alice@192.168.1.100   # Should connect WITHOUT password

# Step 5: Disable password auth (optional, highly recommended):
sudo vim /etc/ssh/sshd_config
# Set: PasswordAuthentication no
sudo systemctl restart sshd

# Step 6: Use SSH agent to avoid entering passphrase:
eval $(ssh-agent)          # Start SSH agent
ssh-add ~/.ssh/id_ed25519  # Add key to agent (asks passphrase once)
ssh-add -l                 # List loaded keys
ssh alice@192.168.1.100    # Now connects without passphrase prompt
```


---

## 31. 🔥 Firewall Management

### 31.1 firewalld (RHEL/CentOS/Fedora)

```bash
# Service management:
systemctl start firewalld
systemctl enable firewalld
systemctl status firewalld

# Zone info:
firewall-cmd --get-default-zone          # Get default zone
firewall-cmd --get-active-zones          # Active zones + interfaces
firewall-cmd --list-all                  # All rules in default zone
firewall-cmd --list-all --zone=public    # Specific zone

# Allow/deny services:
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --permanent --add-service=ssh
firewall-cmd --permanent --remove-service=http

# Allow/deny ports:
firewall-cmd --permanent --add-port=8080/tcp
firewall-cmd --permanent --add-port=9000-9100/tcp
firewall-cmd --permanent --remove-port=8080/tcp

# Rich rules (advanced):
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" service name="http" accept'
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.0.0.5" drop'

# Apply changes and reload:
firewall-cmd --reload

# Temporary rules (no --permanent — lost on reload):
firewall-cmd --add-port=8080/tcp         # Temporary (for testing)

# List everything:
firewall-cmd --permanent --list-all
firewall-cmd --list-services
firewall-cmd --list-ports
```

### 31.2 ufw — Uncomplicated Firewall (Ubuntu)

```bash
# Enable / Disable:
ufw enable
ufw disable
ufw status                         # Status and rules
ufw status verbose                 # Detailed status
ufw status numbered                # Numbered rules

# Default policies:
ufw default deny incoming          # Block all incoming by default
ufw default allow outgoing         # Allow all outgoing by default

# Allow rules:
ufw allow ssh                      # Allow SSH (port 22)
ufw allow 22                       # Same — by port number
ufw allow 80/tcp                   # Allow HTTP
ufw allow 443                      # Allow HTTPS
ufw allow 8080:8090/tcp            # Allow port range
ufw allow from 192.168.1.0/24     # Allow from subnet
ufw allow from 192.168.1.100 to any port 22   # Specific source to SSH

# Deny rules:
ufw deny 23                        # Deny telnet
ufw deny from 10.0.0.5             # Block IP

# Delete rules:
ufw delete allow 80                # Delete by rule
ufw delete 3                       # Delete rule #3 (from numbered status)

# Reset:
ufw reset                          # Reset all rules
```

### 31.3 iptables — Low-Level Firewall

```bash
# View rules:
iptables -L                        # List all rules
iptables -L -v -n                  # Verbose with packet counts, no DNS
iptables -L INPUT                  # Only INPUT chain

# Basic rules:
iptables -A INPUT -p tcp --dport 22 -j ACCEPT     # Allow SSH
iptables -A INPUT -p tcp --dport 80 -j ACCEPT     # Allow HTTP
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT  # Allow established
iptables -A INPUT -j DROP                          # Drop everything else

# Block IP:
iptables -A INPUT -s 10.0.0.5 -j DROP

# Delete rule:
iptables -D INPUT -p tcp --dport 80 -j ACCEPT

# Save/restore rules:
iptables-save > /etc/iptables/rules.v4             # Save
iptables-restore < /etc/iptables/rules.v4          # Restore

# Flush (clear) all rules:
iptables -F                        # Flush all chains
```

---

## 32. 🔥 Firewall — SNAT, DNAT, Source-Based Routing

### 32.1 NAT — Network Address Translation

```
SNAT (Source NAT):     Change SOURCE IP      → Used for internet access from LAN
DNAT (Destination NAT): Change DESTINATION IP → Used for port forwarding / load balancing
```

**SNAT — Share one public IP across a LAN:**
```
LAN clients (192.168.1.x) → [Linux Router] SNAT → Internet
All outgoing traffic appears to come from ONE public IP
```

```bash
# SNAT with iptables (static public IP):
iptables -t nat -A POSTROUTING -o eth0 -s 192.168.1.0/24 -j SNAT --to-source 203.0.113.1

# SNAT with MASQUERADE (dynamic IP — changes, e.g., PPPoE/DHCP):
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Enable IP forwarding (REQUIRED for routing/NAT):
echo 1 > /proc/sys/net/ipv4/ip_forward          # Temporary
echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.conf  # Permanent
sysctl -p                                        # Apply
```

**DNAT — Port Forwarding (expose internal service):**
```
Internet → [Linux Router] DNAT → 192.168.1.50:80
Public port 80 → forwards to internal web server
```

```bash
# DNAT — Forward port 80 to internal server:
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to-destination 192.168.1.50:80
iptables -A FORWARD -p tcp -d 192.168.1.50 --dport 80 -j ACCEPT

# DNAT — Forward port 2222 to internal SSH port 22:
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 2222 -j DNAT --to-destination 192.168.1.10:22
```

### 32.2 Source-Based Routing (Policy Routing)

Used when a server has **multiple network interfaces** and you need traffic from different sources to go through different gateways.

```bash
# Scenario: Server has eth0 (ISP1: 203.0.113.0/24) and eth1 (ISP2: 198.51.100.0/24)
# Traffic from eth0 clients should return via eth0, and eth1 via eth1

# Step 1: Create routing tables:
echo "200 isp1table" >> /etc/iproute2/rt_tables
echo "201 isp2table" >> /etc/iproute2/rt_tables

# Step 2: Add routes to each table:
ip route add default via 203.0.113.1 table isp1table
ip route add default via 198.51.100.1 table isp2table

# Step 3: Add routing rules (policy):
ip rule add from 203.0.113.0/24 table isp1table priority 100
ip rule add from 198.51.100.0/24 table isp2table priority 101

# Step 4: View rules:
ip rule list
ip route show table isp1table
```

### 32.3 sysctl.conf — IP Forwarding and Kernel Network Parameters

```bash
cat /etc/sysctl.conf
```

```ini
# IP Forwarding — MUST enable for routing/NAT between interfaces:
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1

# Why enable IP forwarding?
# Without it: Linux drops packets NOT destined for itself
# With it: Linux ROUTES packets between interfaces (acts as router/NAT gateway)
# Required for: Docker, VMs, VPN servers, NAT routers, Kubernetes nodes

# TCP security settings:
net.ipv4.tcp_syncookies = 1              # SYN flood protection
net.ipv4.icmp_echo_ignore_broadcasts = 1 # Ignore broadcast pings
net.ipv4.conf.all.rp_filter = 1         # Reverse path filtering
net.ipv4.conf.all.accept_redirects = 0  # Don't accept ICMP redirects
net.ipv4.conf.all.send_redirects = 0    # Don't send ICMP redirects

# Performance tuning:
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
fs.file-max = 2097152
```

```bash
# Apply sysctl changes:
sysctl -p                              # Apply from /etc/sysctl.conf
sysctl -p /etc/sysctl.d/99-custom.conf # Apply specific file
sysctl -w net.ipv4.ip_forward=1        # Temporary change (not persistent)

# View all kernel parameters:
sysctl -a                              # All parameters
sysctl net.ipv4.ip_forward             # Specific parameter
cat /proc/sys/net/ipv4/ip_forward      # Same via proc
```

---
