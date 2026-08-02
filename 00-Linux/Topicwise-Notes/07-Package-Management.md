# 📦 Package Management and Software Repositories

Covers package installation, updates, repositories, and package managers on Linux.

## 25. 📦 Package Management

Software installation and updates are a routine part of Linux administration. Package managers simplify this process by handling dependencies, repositories, and version control consistently.

### 25.1 APT — Debian/Ubuntu

```bash
# Update package index:
apt update                               # Refresh package lists
apt upgrade                              # Upgrade installed packages
apt full-upgrade                         # Upgrade + handle dependencies
apt dist-upgrade                         # Full upgrade (may remove pkgs)

# Install / Remove:
apt install nginx                        # Install package
apt install nginx mysql-server           # Install multiple
apt install -y nginx                     # Auto-confirm
apt install nginx=1.18.0-0ubuntu1        # Specific version
apt remove nginx                         # Remove (keep config files)
apt purge nginx                          # Remove including config files
apt autoremove                           # Remove unused dependencies
apt clean                               # Clear downloaded package cache
apt autoclean                           # Remove only obsolete packages

# Search and info:
apt search nginx                         # Search packages
apt show nginx                           # Package details
apt list --installed                     # List installed packages
apt list --upgradable                    # List upgradable packages
dpkg -l                                  # List all installed packages
dpkg -l nginx                            # Status of specific package
dpkg -s nginx                            # Package info
dpkg -L nginx                            # Files installed by package
dpkg -S /etc/nginx/nginx.conf            # Which package owns this file

# Manual .deb install:
dpkg -i package.deb                      # Install .deb file
dpkg -r nginx                            # Remove package

# apt-get (older, still works):
apt-get update && apt-get upgrade -y
```

### 25.2 YUM / DNF — RHEL/CentOS/Fedora

```bash
# DNF (modern, Fedora 22+, RHEL 8+):
dnf update                               # Update all packages
dnf install nginx                        # Install
dnf install -y nginx                     # Auto-confirm
dnf remove nginx                         # Remove
dnf autoremove                           # Remove unused dependencies
dnf search nginx                         # Search
dnf info nginx                           # Package info
dnf list installed                       # All installed packages
dnf list available nginx                 # Available versions
dnf history                              # Transaction history
dnf history undo 5                       # Undo transaction #5
dnf clean all                            # Clean cache
dnf repolist                             # List repositories
dnf config-manager --add-repo URL        # Add repository

# YUM (older, RHEL 7 and older):
yum update
yum install nginx
yum remove nginx
yum search nginx
yum info nginx
yum list installed
yum clean all
yum history

# RPM (low-level package manager):
rpm -ivh package.rpm                     # Install .rpm file
rpm -Uvh package.rpm                     # Upgrade .rpm
rpm -e nginx                             # Remove
rpm -qa                                  # List all installed
rpm -qi nginx                            # Package info
rpm -ql nginx                            # Files from package
rpm -qf /etc/nginx/nginx.conf            # Package owning this file
rpm -V nginx                             # Verify package files
```

### 25.3 Repository Management

```bash
# APT repositories:
cat /etc/apt/sources.list                # Main repo list
ls /etc/apt/sources.list.d/             # Additional repos
add-apt-repository ppa:nginx/stable     # Add PPA (Ubuntu)
add-apt-repository --remove ppa:name    # Remove PPA

# DNF/YUM repositories:
ls /etc/yum.repos.d/                    # Repo files
dnf config-manager --enable repo-name  # Enable repo
dnf config-manager --disable repo-name # Disable repo

# Add EPEL on RHEL/CentOS:
dnf install epel-release
```

---

## 26. 📦 Software Management — YUM Server Setup

### 26.1 YUM — Yellowdog Updater Modified (RHEL 7 and older)

```bash
yum install nginx -y              # Install
yum remove nginx                  # Remove
yum update                        # Update all
yum update nginx                  # Update specific
yum upgrade                       # Update with obsoletes

yum search nginx                  # Search
yum info nginx                    # Package info
yum list installed                # All installed
yum list available                # All available
yum provides /etc/nginx/nginx.conf  # Who provides file
yum deplist nginx                 # Dependencies list
yum history                       # Transaction history
yum history undo 5               # Rollback transaction 5
yum clean all                    # Clean all cache
yum repolist                     # List enabled repos
yum repolist all                 # All repos including disabled
```

### 26.2 Setting Up a Local YUM Repository Server

```bash
# Step 1: Install HTTP server and createrepo:
yum install httpd createrepo -y

# Step 2: Create directory for packages:
mkdir -p /var/www/html/repos/centos7/

# Step 3: Copy/mount ISO or download packages:
mount /dev/cdrom /mnt/
cp -r /mnt/Packages/* /var/www/html/repos/centos7/

# Step 4: Create repo metadata:
createrepo /var/www/html/repos/centos7/
# Re-run after adding new packages:
createrepo --update /var/www/html/repos/centos7/

# Step 5: Start HTTP server:
systemctl enable --now httpd
# firewall-cmd --permanent --add-service=http && firewall-cmd --reload

# Step 6: Configure clients to use local repo:
cat > /etc/yum.repos.d/local.repo << EOF
[local-base]
name=Local CentOS Repository
baseurl=http://192.168.1.10/repos/centos7/
enabled=1
gpgcheck=0
EOF

# With GPG check:
# gpgcheck=1
# gpgkey=http://192.168.1.10/repos/RPM-GPG-KEY-CentOS-7

# Test:
yum clean all && yum repolist
yum install nginx -y
```

### 26.3 vsftpd with GPG Check

```bash
# vsftpd — Very Secure FTP Daemon:
yum install vsftpd -y

# Configuration:
cat /etc/vsftpd/vsftpd.conf
```

```ini
# Key vsftpd settings:
anonymous_enable=NO          # Disable anonymous FTP
local_enable=YES             # Allow local users
write_enable=YES             # Allow uploads
chroot_local_user=YES        # Jail users to their home directory
chroot_list_enable=YES       # Exceptions list
chroot_list_file=/etc/vsftpd/chroot_list

# Passive mode (for firewalled servers):
pasv_enable=YES
pasv_min_port=10090
pasv_max_port=10100
pasv_address=192.168.1.100   # Server's external IP

listen=YES
listen_ipv6=NO
```

```bash
systemctl enable --now vsftpd

# GPG check for RPM packages served over FTP:
# When using a repo over FTP:
cat > /etc/yum.repos.d/ftp-repo.repo << EOF
[ftp-repo]
name=FTP Repository
baseurl=ftp://192.168.1.10/pub/repos/
enabled=1
gpgcheck=1
gpgkey=ftp://192.168.1.10/pub/RPM-GPG-KEY
EOF
```
---
