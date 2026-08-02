# 🛠️ DNS, DHCP, NTP, Samba, NFS, Apache, and sudo

Covers common Linux services and server roles used in real environments.

## 33. 🌐 DNS Server Setup — named.conf, Record Types, Zones

Many Linux services depend on name resolution and centralized configuration. DNS is the service that translates human-readable names into addresses, making modern networked applications possible.

### 33. 🔹 1 DNS Concepts

```
DNS Resolution order on Linux:
1. /etc/hosts           (local file)
2. /etc/resolv.conf     (DNS servers to query)
3. DNS Server           (recursive lookup)

# Check resolution order:
cat /etc/nsswitch.conf | grep hosts
# hosts: files dns myhostname
```

### 33. 🔹 2 /etc/resolv.conf — Client DNS Config

```bash
cat /etc/resolv.conf
```

```
nameserver 8.8.8.8          # Primary DNS server
nameserver 8.8.4.4          # Secondary DNS server
search example.com          # Search domain (appended for short names)
domain example.com          # Local domain name
options ndots:5             # Try as FQDN only if 5+ dots
options timeout:2           # Timeout per query
options attempts:3          # Retry attempts
```

```bash
# DNS testing tools:
nslookup google.com                          # Basic lookup
nslookup google.com 8.8.8.8                 # Use specific server
nslookup -type=MX gmail.com                 # Query MX records

dig google.com                               # Detailed query
dig google.com @8.8.8.8                     # Use specific server
dig MX gmail.com                             # MX records
dig A www.example.com                        # A record
dig AAAA www.example.com                     # IPv6 record
dig PTR 100.1.168.192.in-addr.arpa          # Reverse lookup (PTR)
dig +short google.com                        # Just the answer
dig +trace google.com                        # Full resolution trace

host google.com                              # Simple lookup
host -t MX gmail.com                         # MX records
```

### 33. 🔹 3 DNS Record Types

| Record | Purpose | Example |
|--------|---------|---------|
| **A** | Hostname → IPv4 address | `www.example.com → 93.184.216.34` |
| **AAAA** | Hostname → IPv6 address | `www.example.com → 2001:db8::1` |
| **CNAME** | Alias → canonical name | `ftp.example.com → web.example.com` |
| **MX** | Mail exchange server | `example.com → mail.example.com (priority 10)` |
| **NS** | Authoritative name servers | `example.com → ns1.example.com` |
| **PTR** | IP → Hostname (reverse DNS) | `34.216.184.93.in-addr.arpa → www.example.com` |
| **SOA** | Start of Authority | Zone info: primary NS, admin, serial, refresh timers |
| **TXT** | Text records | SPF, DKIM, domain verification |
| **SRV** | Service location | `_sip._tcp.example.com → priority weight port host` |
| **NAPTR** | Naming Authority Pointer | ENUM, VoIP, URI mapping |

### 33. 🔹 4 Setting Up BIND DNS Server

```bash
# Install BIND:
yum install bind bind-utils -y         # RHEL
apt install bind9 bind9utils -y        # Ubuntu

# Main config file:
cat /etc/named.conf                    # RHEL location
cat /etc/bind/named.conf               # Ubuntu location
```

```bash
# /etc/named.conf — main BIND configuration:
cat > /etc/named.conf << 'EOF'
options {
    listen-on port 53 { 127.0.0.1; 192.168.1.100; };
    directory "/var/named";
    allow-query { localhost; 192.168.1.0/24; };
    recursion yes;                          # Allow recursive queries
    forwarders { 8.8.8.8; 8.8.4.4; };     # Forward unknown queries upstream
    forward only;                           # Only use forwarders (caching DNS)
};

// Forward lookup zone:
zone "example.com" IN {
    type master;
    file "/var/named/example.com.zone";
    allow-update { none; };
};

// Reverse lookup zone:
zone "1.168.192.in-addr.arpa" IN {
    type master;
    file "/var/named/192.168.1.rev";
};
EOF
```

**Forward Lookup Zone File:**
```bash
cat > /var/named/example.com.zone << 'EOF'
$TTL 86400
@       IN  SOA  ns1.example.com. admin.example.com. (
                  2025011501  ; Serial (YYYYMMDDnn)
                  3600        ; Refresh
                  1800        ; Retry
                  604800      ; Expire
                  86400 )     ; Minimum TTL

; Name servers:
@       IN  NS   ns1.example.com.
@       IN  NS   ns2.example.com.

; A records:
ns1     IN  A    192.168.1.100
ns2     IN  A    192.168.1.101
www     IN  A    192.168.1.200
ftp     IN  A    192.168.1.201
mail    IN  A    192.168.1.202
@       IN  A    192.168.1.200

; CNAME record:
webmail IN  CNAME mail

; MX records:
@       IN  MX   10  mail.example.com.

; SRV record:
_sip._tcp IN SRV 10 20 5060 sip.example.com.

; NAPTR record:
@       IN  NAPTR 100 10 "u" "E2U+sip" "!^.*$!sip:info@example.com!" .

; TXT record:
@       IN  TXT  "v=spf1 mx -all"
EOF
```

**Reverse Lookup Zone File:**
```bash
cat > /var/named/192.168.1.rev << 'EOF'
$TTL 86400
@       IN  SOA  ns1.example.com. admin.example.com. (
                  2025011501
                  3600
                  1800
                  604800
                  86400 )

@       IN  NS   ns1.example.com.

; PTR records (last octet only):
100     IN  PTR  ns1.example.com.
200     IN  PTR  www.example.com.
202     IN  PTR  mail.example.com.
EOF
```

```bash
# Set correct permissions:
chown root:named /var/named/example.com.zone
chmod 640 /var/named/example.com.zone

# Verify config files:
named-checkconf /etc/named.conf
named-checkzone example.com /var/named/example.com.zone
named-checkzone 1.168.192.in-addr.arpa /var/named/192.168.1.rev

# Start and enable BIND:
systemctl enable --now named

# Allow DNS through firewall:
firewall-cmd --permanent --add-service=dns
firewall-cmd --reload

# Test:
dig @192.168.1.100 www.example.com
dig @192.168.1.100 -x 192.168.1.200     # Reverse lookup
nslookup www.example.com 192.168.1.100
```

---

## 34. 🖥️ DHCP Server Setup

### 34. 🔹 1 Installing and Configuring dhcpd

```bash
# Install:
yum install dhcp -y               # RHEL
apt install isc-dhcp-server -y    # Ubuntu

# Main config:
cat /etc/dhcp/dhcpd.conf
```

```bash
# /etc/dhcp/dhcpd.conf — complete example:
cat > /etc/dhcp/dhcpd.conf << 'EOF'
# Global settings:
default-lease-time 86400;        # 24 hours
max-lease-time 604800;           # 7 days
ddns-update-style none;
authoritative;                   # This is THE DHCP server for this network

# Options sent to all clients:
option domain-name "example.com";
option domain-name-servers 192.168.1.100, 8.8.8.8;
option ntp-servers 192.168.1.1;

# Subnet declaration:
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.50 192.168.1.200;      # DHCP pool
    option routers 192.168.1.1;            # Default gateway
    option broadcast-address 192.168.1.255;
    default-lease-time 86400;
    max-lease-time 604800;
}

# Static reservation (fixed IP by MAC address):
host webserver {
    hardware ethernet aa:bb:cc:dd:ee:ff;
    fixed-address 192.168.1.10;
    option host-name "webserver.example.com";
}

host printer {
    hardware ethernet 11:22:33:44:55:66;
    fixed-address 192.168.1.20;
}
EOF
```

```bash
# Specify which interface to listen on (Ubuntu):
echo 'INTERFACESv4="eth0"' >> /etc/default/isc-dhcp-server

# Start DHCP server:
systemctl enable --now dhcpd         # RHEL
systemctl enable --now isc-dhcp-server  # Ubuntu

# Allow DHCP through firewall:
firewall-cmd --permanent --add-service=dhcp
firewall-cmd --reload

# View active leases:
cat /var/lib/dhcpd/dhcpd.leases
# or: cat /var/lib/dhcp/dhcpd.leases (Ubuntu)
```

---

## 35. 🕐 NTP — Network Time Protocol

### 35. 🔹 1 Importance of Time Sync

Accurate time is critical for: logs correlation, SSL certificates, Kerberos auth, cron jobs, distributed systems, databases.

### 35. 🔹 2 chrony (Modern — RHEL 7+, Ubuntu 20.04+)

```bash
# Install:
yum install chrony -y     # RHEL
apt install chrony -y     # Ubuntu

# Configuration:
cat /etc/chrony.conf
```

```ini
# /etc/chrony.conf:
server pool.ntp.org iburst        # Public NTP server pool
server 0.centos.pool.ntp.org iburst
server 1.centos.pool.ntp.org iburst
server time.cloudflare.com iburst

# Allow local network to sync from this server (if acting as NTP server):
allow 192.168.1.0/24

driftfile /var/lib/chrony/drift
logfile /var/log/chrony/chrony.log
```

```bash
# Start and enable:
systemctl enable --now chronyd

# Check sync status:
chronyc tracking              # Current sync status
chronyc sources               # List NTP sources
chronyc sources -v            # Verbose sources
chronyc makestep              # Force immediate time sync

# Allow NTP through firewall:
firewall-cmd --permanent --add-service=ntp
```

### 35. 🔹 3 ntpd (Older)

```bash
yum install ntp -y
cat /etc/ntp.conf
# server pool.ntp.org iburst
systemctl enable --now ntpd
ntpstat                       # Sync status
ntpq -p                       # Peer table
```

### 35. 🔹 4 timedatectl (systemd time management)

```bash
timedatectl                           # Status
timedatectl set-time "2025-01-15 10:30:00"  # Set time manually
timedatectl set-timezone Asia/Kolkata        # Set timezone
timedatectl list-timezones                   # Available timezones
timedatectl set-ntp true                     # Enable NTP sync
timedatectl set-ntp false                    # Disable NTP sync
```


---

## 36. 🌐 Samba Server — Full Implementation

### 36. 🔹 1 Samba Overview

Samba allows Linux to share files/printers with **Windows** clients using the **SMB/CIFS** protocol.

```bash
# Install:
yum install samba samba-client samba-common -y   # RHEL
apt install samba samba-common smbclient cifs-utils -y  # Ubuntu
```

### 36. 🔹 2 Complete smb.conf

```bash
cat > /etc/samba/smb.conf << 'EOF'
[global]
    workgroup = WORKGROUP
    server string = Linux Samba Server %v
    netbios name = LINUXSERVER
    security = user                    # user, share, domain, ads
    map to guest = bad user            # Map unknown users to guest
    dns proxy = no
    log file = /var/log/samba/log.%m
    max log size = 1000
    logging = file

    # Performance:
    socket options = TCP_NODELAY IPTOS_LOWDELAY SO_RCVBUF=65536 SO_SNDBUF=65536
    read raw = yes
    write raw = yes

[homes]
    comment = Home Directories
    browseable = no
    writable = yes
    valid users = %S

[public]
    comment = Public Share (read-only)
    path = /opt/samba/public
    public = yes
    browseable = yes
    writable = no
    guest ok = yes

[shared]
    comment = Department Shared Folder
    path = /opt/samba/shared
    browseable = yes
    writable = yes
    valid users = @developers, alice, bob
    create mask = 0664
    directory mask = 0775
    force group = developers

[printers]
    comment = All Printers
    path = /var/spool/samba
    browseable = no
    printable = yes
EOF
```

### 36. 🔹 3 Samba Setup Steps

```bash
# Step 1: Create directories:
mkdir -p /opt/samba/public /opt/samba/shared
chmod 755 /opt/samba/public
chmod 770 /opt/samba/shared
chown root:developers /opt/samba/shared

# Step 2: Create Linux users and Samba users:
useradd -M -s /sbin/nologin alice       # -M = no home dir
smbpasswd -a alice                      # Set Samba password
smbpasswd -e alice                      # Enable Samba user

# Step 3: Validate config:
testparm                                # Test smb.conf

# Step 4: Start Samba:
systemctl enable --now smbd nmbd

# Step 5: Firewall:
firewall-cmd --permanent --add-service=samba
firewall-cmd --reload

# Step 6: SELinux for Samba (RHEL):
setsebool -P samba_enable_home_dirs on
setsebool -P samba_export_all_rw on
chcon -R -t samba_share_t /opt/samba/

# Step 7: Test from Linux:
smbclient -L //192.168.1.100 -U alice    # List shares
smbclient //192.168.1.100/shared -U alice # Connect to share

# Mount Samba share:
mount -t cifs //192.168.1.100/shared /mnt/smb -o username=alice,password=pass
# In /etc/fstab:
# //192.168.1.100/shared /mnt/smb cifs credentials=/etc/samba/creds,_netdev 0 0
```

---

## 37. 🗃️ NFS & Samba (File Sharing)

### 37. 🔹 1 NFS — Network File System

```bash
# NFS Server setup:
apt install nfs-kernel-server          # Install NFS server (Ubuntu)
yum install nfs-utils                  # Install NFS (RHEL)

# Configure exports (/etc/exports):
cat /etc/exports
# /opt/shared        192.168.1.0/24(rw,sync,no_subtree_check)
# /home/public       *(ro,sync,no_root_squash)
# /data              10.0.0.5(rw,sync,root_squash)

# Export options:
# rw           → read-write
# ro           → read-only
# sync         → write synchronously (safe)
# async        → write asynchronously (fast but risky)
# no_root_squash → root on client = root on server (careful!)
# root_squash  → root on client = nobody on server (safer)
# no_subtree_check → disable subtree checking (recommended)

# Apply exports:
exportfs -a             # Export all shares
exportfs -r             # Re-export all shares (refresh)
exportfs -v             # List current exports

# Start NFS:
systemctl enable --now nfs-server   # RHEL
systemctl enable --now nfs-kernel-server  # Ubuntu

# NFS Client:
showmount -e 192.168.1.10           # List exports from server
mount -t nfs 192.168.1.10:/opt/shared /mnt/nfs  # Mount
mount -t nfs4 192.168.1.10:/opt/shared /mnt/nfs  # NFSv4

# Add to /etc/fstab:
# 192.168.1.10:/opt/shared  /mnt/nfs  nfs  defaults,_netdev  0  0
```

### 37. 🔹 2 Samba — SMB/CIFS (Windows-compatible sharing)

```bash
# Install:
apt install samba samba-common-bin   # Ubuntu
yum install samba samba-client       # RHEL

# Configuration (/etc/samba/smb.conf):
cat /etc/samba/smb.conf
```

```ini
[global]
    workgroup = WORKGROUP
    server string = Linux File Server
    security = user
    map to guest = bad user

[shared]
    comment = Shared Folder
    path = /opt/shared
    browseable = yes
    writable = yes
    valid users = alice, @developers
    create mask = 0664
    directory mask = 0775

[public]
    comment = Public Folder (no auth needed)
    path = /opt/public
    browseable = yes
    guest ok = yes
    read only = yes
```

```bash
# Add Samba user (must be existing Linux user):
smbpasswd -a alice             # Add alice with Samba password
smbpasswd -e alice             # Enable user
smbpasswd -d alice             # Disable user

# Test config:
testparm                       # Validate smb.conf

# Start Samba:
systemctl enable --now smbd nmbd

# Mount from Linux:
mount -t cifs //192.168.1.10/shared /mnt/smb -o username=alice
# Or in /etc/fstab:
# //192.168.1.10/shared /mnt/smb cifs credentials=/etc/samba/creds,_netdev 0 0
```

---

## 38. 🌐 HTTP Server — Apache httpd.conf

### 38. 🔹 1 Apache httpd Configuration

```bash
# Install:
yum install httpd -y              # RHEL
apt install apache2 -y            # Ubuntu

# Main config file:
/etc/httpd/conf/httpd.conf        # RHEL
/etc/apache2/apache2.conf         # Ubuntu

# Key directives:
cat /etc/httpd/conf/httpd.conf
```

```apache
# /etc/httpd/conf/httpd.conf — key settings:

ServerRoot "/etc/httpd"
Listen 80                          # Port to listen on
Listen 443                         # HTTPS

ServerAdmin webmaster@example.com
ServerName www.example.com:80      # FQDN of server

# Document root:
DocumentRoot "/var/www/html"

<Directory "/var/www/html">
    Options Indexes FollowSymLinks  # Indexes=dir listing, remove for security
    AllowOverride All               # Allow .htaccess files
    Require all granted
</Directory>

# Log files:
ErrorLog "/var/log/httpd/error_log"
CustomLog "/var/log/httpd/access_log" combined
LogLevel warn

# Virtual Hosts:
<VirtualHost *:80>
    ServerName site1.example.com
    DocumentRoot /var/www/site1
    ErrorLog /var/log/httpd/site1-error.log
    CustomLog /var/log/httpd/site1-access.log combined
</VirtualHost>

<VirtualHost *:443>
    ServerName site1.example.com
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/site1.crt
    SSLCertificateKeyFile /etc/ssl/private/site1.key
    DocumentRoot /var/www/site1
</VirtualHost>

# Security settings:
ServerTokens Prod                  # Hide detailed version
ServerSignature Off                # No version in error pages
TraceEnable Off                    # Disable TRACE method
```

```bash
# Apache management:
systemctl enable --now httpd
apachectl configtest               # Test config before restart
apachectl -t                       # Same
apachectl restart                  # Restart
apachectl graceful                 # Graceful restart (no connection drop)

# Ubuntu:
a2ensite site1.conf                # Enable virtual host
a2dissite site1.conf               # Disable virtual host
a2enmod ssl                        # Enable module
a2dismod ssl                       # Disable module
apache2ctl configtest
```


---

## 39. 🔒 sudo and visudo — Privilege Management

### 39. 🔹 1 sudo — Superuser Do

```bash
# Run single command as root:
sudo command
sudo apt update

# Run as specific user:
sudo -u alice command
sudo -u www-data /opt/app/restart.sh

# Open root shell:
sudo -i                    # Login shell (sources root's profile)
sudo -s                    # Shell (inherits current environment)
sudo bash                  # Same as -s

# Run last command with sudo:
sudo !!

# Sudo without password (if configured):
sudo -n command            # Non-interactive (fail if password needed)

# List your sudo permissions:
sudo -l                    # What can current user sudo?
sudo -l -U alice           # What can alice sudo? (root only)

# Sudo timeout:
sudo -k                    # Invalidate cached credentials
sudo -v                    # Validate (refresh) cached credentials

# Switch to another user permanently:
su alice                   # Switch (needs alice's password)
su -                       # Switch to root (needs root password)
su - alice                 # Login shell as alice
```

### 39. 🔹 2 visudo — Safe Sudoers Editor

```bash
# ALWAYS use visudo — it validates syntax before saving!
visudo                     # Edit /etc/sudoers
visudo -f /etc/sudoers.d/alice  # Edit a specific drop-in file
```

```bash
# /etc/sudoers syntax:
# user  HOST=(runas_user:runas_group)  [NOPASSWD:]  commands
#
# Aliases:
User_Alias    ADMINS = alice, bob, carol
Cmnd_Alias    NETWORKING = /sbin/ifconfig, /sbin/route, /sbin/ip
Cmnd_Alias    SERVICES = /usr/bin/systemctl start *, /usr/bin/systemctl stop *

# Allow full root access:
alice   ALL=(ALL:ALL) ALL
%sudo   ALL=(ALL:ALL) ALL              # Group sudo

# Allow without password:
alice   ALL=(ALL) NOPASSWD: ALL        # Everything, no password
bob     ALL=(ALL) NOPASSWD: /sbin/reboot   # Only reboot

# Allow specific commands:
carol   ALL=(ALL) /usr/bin/apt install, /usr/bin/apt update
deploy  ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx

# Allow aliases:
ADMINS  ALL=(ALL) NETWORKING, SERVICES

# Secure defaults:
Defaults env_reset                     # Clean environment
Defaults mail_badpass                  # Email on bad password
Defaults secure_path="..."             # Secure PATH for sudo
Defaults timestamp_timeout=5          # Cache credentials for 5 min
Defaults requiretty                    # Must have TTY (prevents remote sudo)
```

```bash
# Drop-in files (preferred over editing main sudoers):
ls /etc/sudoers.d/
cat > /etc/sudoers.d/alice << 'EOF'
alice ALL=(ALL) NOPASSWD: /sbin/reboot, /sbin/shutdown
EOF
chmod 440 /etc/sudoers.d/alice
```

---
