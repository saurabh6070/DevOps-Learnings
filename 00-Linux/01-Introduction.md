# 🐧 Linux — Complete Notes (Basics to System Administration)

> 🚀 A comprehensive guide covering Linux fundamentals, file system, inodes, fdisk, permissions, user/group management (UID/GID/shadow/passwd), shell profiles (.bashrc/.bash_profile/.bash_logout), networking (LAN/WAN/OSI/ifcfg/NetworkManager), firewall (SNAT/DNAT/iptables), DNS/DHCP/NTP/Samba/NFS/FTP servers, SSH, LVM, RAID-5, GRUB recovery, shell scripting, cron/at, sysctl, and all Linux Administration tasks.

---

## 📌 Table of Contents

| # | Section |
|---|---------|
| 1 | [🐧 Introduction to Linux](#1--introduction-to-linux) |
| 2 | [🖥️ Linux Architecture](#2-%EF%B8%8F-linux-architecture) |
| 3 | [📂 Linux File System Hierarchy](#3--linux-file-system-hierarchy) |
| 4 | [⌨️ Essential Linux Commands](#4-%EF%B8%8F-essential-linux-commands) |
| 5 | [🔐 File Permissions & Ownership](#5--file-permissions--ownership) |
| 6 | [📁 File & Directory Management — softlink, hardlink, hidden files, tar, gzip, bzip2](#6--file--directory-management) |
| 7 | [🐚 Vi / Vim Editor](#7--vi--vim-editor) |
| 8 | [🔗 Shell & Environment Variables — .bash_profile, .bashrc, .bash_logout, alias](#8--shell--environment-variables) |
| 9 | [🐚 Shell Profile Files — .bash_profile, .bashrc, .bash_logout](#9--shell-profile-files--bash_profile-bashrc-bash_logout) |
| 10 | [🔑 Hidden Files and alias](#10--hidden-files-and-aliases) |
| 11 | [👤 User & Group Management — UIDs, GIDs, passwd, shadow, root↔normal conversion](#11--user--group-management) |
| 12 | [👥 UIDs & GIDs — root UID=0, system vs user IDs, root↔normal conversion](#12--uids-gids--user-and-group-ids-in-linux) 
| 13 | [📁 /etc/passwd and /etc/shadow — complete field breakdown](#13--etcpasswd-and-etcshadow--user-database-files) |
| 14 | [🔄 /etc/inittab, Runlevels — switching GUI↔CLI](#14--etcinittab-and-runlevels--switching-between-gui-and-cli) |
| 15 | [📊 wall — broadcast messages, /etc/motd](#15--wall--broadcast-message-to-all-users) |
| 16 | [⚙️ Systemd & Service Management](#16-%EF%B8%8F-systemd--service-management) |
| 17 | [⚙️ Process Management](#17-%EF%B8%8F-process-management) |
| 18 | [🧠 Memory & CPU Management](#18--memory--cpu-management) |
| 19 | [📋 Linux Logs & Monitoring](#19--linux-logs--monitoring) |
| 20 | [💾 Disk & Storage Management — fdisk (primary/extended/logical), mkfs, inodes, fstab](#20--disk--storage-management) |
| 21 | [💾 Advanced fdisk — Primary, Extended, Logical Partitions, mkfs, fstab](#21--advanced-disk-management--fdisk-partitions--filesystems) |
| 22 | [🗂️ Inodes — Linux Filesystem Internals](#22-%EF%B8%8F-inodes--understanding-the-linux-filesystem-internals) |
| 23 | [💡 LVM — PV, VG, LV — create, extend, reduce, snapshots](#23--lvm--logical-volume-management) |
| 24 | [🔒 RAID-5 — theory, implementation with mdadm](#24--raid--redundant-array-of-independent-disks) |
| 25 | [📦 Package Management — RPM, YUM, YUM server setup, vsftpd+GPG](#25--package-management) |
| 26 | [📦 RPM, YUM Server Setup, vsftpd with GPGcheck](#26--software-management--rpm-yum-server-setup) |
| 27 | [🌐 Networking — LAN, WAN, OSI, ifcfg/ONBOOT, NetworkManager, hostname, hosts.deny, /etc/network/interfaces, casting types](#27--networking-in-linux) |
| 28 | [🌐 Networking Deep Dive — LAN/WAN, OSI 7 layers, RHEL ifcfg ONBOOT, NetworkManager, hostname, hosts.deny, casting types, SDN](#28--networking-in-linux--lan-wan-osi-and-configuration-files) |
| 29 | [🔒 SSH — config, key auth, passwordless, SCP, protocols](#29--ssh--remote-access) |
| 30 | [🔐 Passwordless SSH — step-by-step setup](#30--password-less-ssh-authentication--complete-setup) |
| 31 | [🔥 Firewall — firewalld, ufw, iptables, SNAT, DNAT, source-based routing](#31--firewall-management) |
| 32 | [🔥 Firewall — SNAT, DNAT, Source-Based Routing, sysctl IP forwarding](#32--firewall--snat-dnat-source-based-routing) |
| 33 | [🌐 DNS Server — named.conf, A/CNAME/MX/NS/SRV/NAPTR/PTR records, forward/reverse zones, resolv.conf, nslookup](#33--dns-server-setup--namedconf-record-types-zones) |
| 34 | [🖥️ DHCP Server — dhcpd.conf, static reservations](#34--dhcp-server-setup) |
| 35 | [🕐 NTP — chrony, ntpd, timedatectl](#35--ntp--network-time-protocol) |
| 36 | [🌐 Samba Server — full implementation, smb.conf, mount](#36--samba-server--full-implementation) |
| 37 | [🗃️ NFS & Samba — /etc/exports, smb.conf, full setup](#37-%EF%B8%8F-nfs--samba-file-sharing) |
| 38 | [🌐 Apache — httpd.conf, VirtualHost, SSL](#38--http-server--apache-httpdconf) |
| 39 | [🔒 sudo and visudo — sudoers syntax, NOPASSWD, aliases](#39--sudo-and-visudo--privilege-management) |
| 40 | [🔒 Linux Security & Hardening — SELinux, sudo, visudo](#40--linux-security--hardening) |
| 41 | [🔐 GRUB2 Password Recovery + /etc/rc.local](#41--grub2-password--recovery-when-password-forgotten) |
| 42 | [🔄 Backup & Recovery](#42--backup--recovery) |
| 43 | [🚀 Performance Tuning — sysctl.conf, IP forwarding, ulimit](#43--performance-tuning) |
| 44 | [📝 Text Processing — grep, awk, sed](#44--text-processing--grep-awk-sed) |
| 45 | [📜 Shell Scripting](#45--shell-scripting) |
| 46 | [⏰ Scheduling Tasks — Cron & At](#46--scheduling-tasks--cron--at) |
| 47 | [⚡ Quick Reference Cheat Sheet](#47--quick-reference-cheat-sheet) |

## 1. 🐧 Introduction to Linux

### 1.1 What is Linux?

**Linux** is a Unix-like operating system kernel that powers servers, desktops, cloud platforms, mobile devices, and supercomputers.
Linux was created in 1991 by **Linus Torvalds**.

Strictly speaking:
Linux = Kernel

When combined with tools from GNU Project, it forms a complete operating system often called GNU/Linux.
```
Linux = Kernel (core) + GNU Tools + Shell + Applications
```

---

#### ⚙️ What is an Operating System?

#### An Operating System (OS):
> Manages CPU, memory, disk, and devices.
> Runs applications.
> Provides security and user management.
> Handles networking.

#### Examples of Operating Systems:
> Microsoft Windows
> macOS
> linux


### 1.2 Why Linux?

| Feature | Description |
|---------|-------------|
| 🆓 **Free & Open Source** | No licensing cost; source code freely available |
| 🔐 **Secure** | Strong permission model; less malware than Windows |
| 🏋️ **Stable & Reliable** | Servers run for years without reboots |
| ⚙️ **Customizable** | Modify kernel and every component |
| 📈 **Scalable** | Powers tiny Raspberry Pi to world's fastest supercomputers |
| 🌐 **Dominant in Cloud** | 90%+ of cloud workloads run on Linux |
| 🐳 **Container Native** | Docker, Kubernetes all built on Linux kernel features |

### 1.3 Popular Linux Distributions

| Family | Distributions | Package Manager |
|--------|--------------|----------------|
| **Debian** | Ubuntu, Debian, Kali, Linux Mint | `apt` / `dpkg` |
| **Red Hat** | RHEL, CentOS, Rocky Linux, Fedora, AlmaLinux | `yum` / `dnf` / `rpm` |
| **SUSE** | openSUSE, SLES | `zypper` / `rpm` |
| **Arch** | Arch Linux, Manjaro | `pacman` |
| **Independent** | Alpine, Gentoo, Slackware | varies |

> 💡 **Ubuntu** is most popular for beginners and cloud. **RHEL/CentOS** dominate enterprise environments.

### 1.4 Linux Kernel Version

```bash
# Check kernel version:
uname -r           # e.g., 6.1.0-21-amd64
uname -a           # Full system info
cat /proc/version  # Detailed kernel info
```

---

## 2. 🖥️ Linux Architecture

```
┌─────────────────────────────────────────────────────┐
│                  USER SPACE                          │
│                                                     │
│  ┌──────────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Applications │  │  Shell   │  │  System Libs │  │
│  │ (vim, nginx) │  │ (bash)   │  │  (glibc)     │  │
│  └──────────────┘  └──────────┘  └──────────────┘  │
│                         ↕ System Calls               │
├─────────────────────────────────────────────────────┤
│                  KERNEL SPACE                        │
│                                                     │
│  ┌──────────┐  ┌────────┐  ┌──────┐  ┌──────────┐  │
│  │ Process  │  │ Memory │  │ File │  │ Network  │  │
│  │ Mgmt     │  │ Mgmt   │  │ Sys  │  │ Stack    │  │
│  └──────────┘  └────────┘  └──────┘  └──────────┘  │
├─────────────────────────────────────────────────────┤
│                   HARDWARE                           │
│    CPU    RAM    Disk    NIC    GPU    Peripherals   │
└─────────────────────────────────────────────────────┘
```

### 2.1 Key Layers

| Layer | Description |
|-------|-------------|
| **Hardware** | Physical components — CPU, RAM, disk, network card |
| **Kernel** | Core OS — manages hardware, processes, memory, filesystem |
| **System Libraries** | Standard functions (glibc) that programs call |
| **Shell** | Command interpreter — bash, zsh, sh, ksh, fish |
| **Applications** | User programs — nginx, vim, Python, MySQL |

### 2.2 Types of Shells

| Shell | Description |
|-------|-------------|
| `bash` | Bourne Again SHell — default on most Linux distros |
| `sh` | Original Bourne shell — minimal, POSIX compliant |
| `zsh` | Z Shell — feature-rich, used by macOS default |
| `ksh` | Korn Shell — common in enterprise Unix |
| `fish` | Friendly Interactive Shell — user-friendly |
| `dash` | Lightweight sh for scripting |

```bash
# Check current shell:
echo $SHELL
echo $0

# List available shells:
cat /etc/shells

# Switch shell:
chsh -s /bin/zsh
```

---

## 3. 📂 Linux File System Hierarchy

Linux uses a **single root** (`/`) hierarchy — everything hangs from `/`. Unlike Windows, there are no drive letters.

```
/
├── bin/        ← Essential user commands (ls, cp, mv)
├── sbin/       ← Essential system admin commands (fdisk, reboot)
├── etc/        ← System configuration files
├── home/       ← User home directories (/home/alice, /home/bob)
├── root/       ← Root user's home directory
├── var/        ← Variable data — logs, spool, temp files
├── tmp/        ← Temporary files (cleared on reboot)
├── usr/        ← User programs, libraries, documentation
│   ├── bin/    ← Non-essential user commands
│   ├── lib/    ← Libraries for usr/bin programs
│   └── local/  ← Locally compiled/installed software
├── lib/        ← Essential shared libraries and kernel modules
├── proc/       ← Virtual FS — real-time kernel/process info
├── sys/        ← Virtual FS — device and kernel info
├── dev/        ← Device files (disks, terminals)
├── mnt/        ← Temporary mount points
├── media/      ← Removable media mount points (USB, CD)
├── opt/        ← Optional/third-party software
├── boot/       ← Boot loader files, kernel images
├── srv/        ← Data served by the system (web, ftp)
└── run/        ← Runtime data (PID files, sockets)
```

### 3.1 Key Directories Explained

| Directory | Purpose | Examples |
|-----------|---------|---------|
| `/etc` | ALL system config files | `/etc/passwd`, `/etc/nginx/`, `/etc/ssh/` |
| `/var/log` | System and application logs | `/var/log/syslog`, `/var/log/nginx/` |
| `/proc` | Live kernel/process data | `/proc/cpuinfo`, `/proc/meminfo` |
| `/dev` | Device files | `/dev/sda` (disk), `/dev/null`, `/dev/tty` |
| `/home` | User personal directories | `/home/username/` |
| `/tmp` | Temp files — world-writable | Cleared on reboot |
| `/usr/local/bin` | User-installed binaries | Custom scripts, compiled software |

### 3.2 Absolute vs Relative Paths

```bash
# Absolute path — always starts with /:
/home/alice/documents/report.txt

# Relative path — relative to current directory:
documents/report.txt    # from /home/alice/
../alice/documents/     # go up one level, then down

# Special path shortcuts:
~           # Current user's home directory (/home/alice)
.           # Current directory
..          # Parent directory
-           # Previous directory (cd -)
```

---

## 4. ⌨️ Essential Linux Commands

### 4.1 Navigation

```bash
pwd                    # Print Working Directory — where am I?
ls                     # List files
ls -l                  # Long listing (permissions, size, date)
ls -la                 # Long listing including hidden files
ls -lh                 # Human-readable file sizes
ls -lt                 # Sort by modification time (newest first)
ls -R                  # Recursive listing
ls -ld /etc            # Info about directory itself, not its contents

cd /path/to/dir        # Change directory
cd ~                   # Go to home directory
cd ..                  # Go up one level
cd -                   # Go to previous directory
cd /                   # Go to root directory
```

### 4.2 Getting Help

```bash
man ls                 # Manual page for 'ls'
man -k keyword         # Search man pages by keyword
ls --help              # Built-in help
info ls                # GNU info pages (more detailed)
whatis ls              # One-line description
which ls               # Full path of a command
whereis ls             # Binary, source, manual locations
type ls                # Shows if command is alias/builtin/file
```

### 4.3 System Information

```bash
# OS and kernel:
uname -a               # All system info
uname -r               # Kernel version only
cat /etc/os-release    # Distro name and version
lsb_release -a         # Distro info (Debian/Ubuntu)
hostnamectl            # Hostname and OS info

# Hardware:
lscpu                  # CPU details
lsmem                  # Memory details
lsblk                  # Block devices (disks)
lspci                  # PCI devices
lsusb                  # USB devices
dmidecode              # Hardware info from BIOS/UEFI
hwinfo --short         # Short hardware summary

# System uptime and load:
uptime                 # How long system has been running + load average
w                      # Who is logged in + what they're doing
last                   # Login history
lastlog                # Last login for all users
```

### 4.4 Date and Time

```bash
date                   # Current date and time
date +"%Y-%m-%d %H:%M:%S"   # Custom format
date -s "2025-01-15 10:30:00"  # Set date/time (root)
timedatectl            # Show/set timezone and NTP info
timedatectl list-timezones    # All available timezones
timedatectl set-timezone Asia/Kolkata   # Set timezone
timedatectl set-ntp true      # Enable NTP sync
cal                    # Calendar for current month
cal 2025               # Calendar for whole year
```

### 4.5 Clear, Reset, History

```bash
clear                  # Clear screen
reset                  # Reset terminal
history                # Show command history
history 20             # Show last 20 commands
!50                    # Re-run command #50 from history
!!                     # Re-run last command
!nginx                 # Re-run last command starting with 'nginx'
history -c             # Clear history
Ctrl + R               # Reverse search through history
Ctrl + L               # Clear screen (same as clear)
```
---

## 5. 🔐 File Permissions & Ownership

### 5.1 Understanding Permissions

Every file has **three sets of permissions** for three types of users:

```
-rwxr-xr--  1  alice  developers  4096  Jan 15  file.txt
│││││││││
││││││││└── Other: r-- (read only)
│││││││└─── Group: r-x (read + execute)
││││││└──── Owner: rwx (read + write + execute)
│││││└───── File type: - (regular), d (dir), l (link), c (char), b (block)
```

### 5.2 Permission Values

| Permission | Symbol | Numeric Value |
|-----------|--------|:------------:|
| Read | `r` | 4 |
| Write | `w` | 2 |
| Execute | `x` | 1 |
| None | `-` | 0 |

```
Common permission combos:
rwx = 4+2+1 = 7   (full access)
rw- = 4+2+0 = 6   (read + write)
r-x = 4+0+1 = 5   (read + execute)
r-- = 4+0+0 = 4   (read only)
--- = 0+0+0 = 0   (no access)

Common patterns:
755 = rwxr-xr-x  → Directories, executable scripts
644 = rw-r--r--  → Regular files
600 = rw-------  → Private files (SSH keys)
777 = rwxrwxrwx  → ⚠️ Avoid — world-writable!
```

### 5.3 chmod — Change Permissions

```bash
# Numeric (octal) method:
chmod 755 script.sh          # rwxr-xr-x
chmod 644 file.txt           # rw-r--r--
chmod 600 ~/.ssh/id_rsa      # rw------- (SSH private key)
chmod -R 755 /var/www/html/  # Recursive

# Symbolic method:
chmod u+x script.sh          # Add execute for owner (u=user)
chmod g+w file.txt           # Add write for group
chmod o-r file.txt           # Remove read from others
chmod a+x script.sh          # Add execute for ALL (a=all)
chmod u+x,g-w file.txt       # Multiple changes
chmod go= file.txt           # Remove ALL permissions from group and others
chmod u=rwx,g=rx,o= file.txt # Set exact permissions

# Common use cases:
chmod +x script.sh           # Make script executable
chmod -R 755 /opt/app/       # Set website directory permissions
chmod 400 private.key        # Read-only, owner only
```

### 5.4 chown — Change Ownership

```bash
chown alice file.txt              # Change owner to alice
chown alice:developers file.txt   # Change owner AND group
chown :developers file.txt        # Change only group
chown -R www-data:www-data /var/www/html/  # Recursive ownership change
chown --reference=source.txt dest.txt      # Copy ownership from source
```

### 5.5 chgrp — Change Group

```bash
chgrp developers file.txt          # Change group ownership
chgrp -R developers /opt/project/  # Recursive
```

### 5.6 Special Permissions

```bash
# SUID (Set User ID) — run file as owner, not executor:
chmod u+s /usr/bin/passwd      # Numeric: chmod 4755 file
ls -l /usr/bin/passwd          # Shows: -rwsr-xr-x (s instead of x)

# SGID (Set Group ID) — run as group owner / inherit group in dir:
chmod g+s /opt/shared/         # Numeric: chmod 2755 dir
# New files in this dir inherit the directory's group

# Sticky Bit — only owner can delete their own files:
chmod +t /tmp                  # Numeric: chmod 1777 /tmp
ls -ld /tmp                    # Shows: drwxrwxrwt (t at end)
# Used on /tmp so users can't delete each other's temp files
```

### 5.7 umask — Default Permissions

```bash
umask                     # Show current umask (e.g., 0022)
umask 0022                # Set umask

# How umask works:
# Files created with: 666 - umask = default file permissions
# Dirs created with:  777 - umask = default dir permissions
# umask 0022 → files get 644, dirs get 755

umask 0027                # Files: 640, Dirs: 750 (group-readable only)
```

### 5.8 ACL — Access Control Lists

```bash
# Extended permissions beyond owner/group/other:
getfacl file.txt                              # View ACL
setfacl -m u:bob:rw file.txt                  # Give bob read+write
setfacl -m g:developers:rx /opt/project/      # Group access
setfacl -R -m u:alice:rwx /opt/project/       # Recursive
setfacl -x u:bob file.txt                     # Remove bob's ACL
setfacl -b file.txt                           # Remove ALL ACLs
```

---

## 6. 📁 File & Directory Management

### 6.1 Creating Files and Directories

```bash
# Create files:
touch file.txt               # Create empty file / update timestamp
touch file1.txt file2.txt    # Create multiple files
echo "Hello" > file.txt      # Create file with content (overwrites)
echo "Hello" >> file.txt     # Append to file
cat > file.txt               # Create file, type content, Ctrl+D to save
nano file.txt                # Create/edit with nano editor
vim file.txt                 # Create/edit with vim editor

# Create directories:
mkdir mydir                  # Create directory
mkdir -p /opt/app/logs       # Create directory + all parents
mkdir -p dir1 dir2 dir3      # Create multiple directories
```

### 6.2 Copying, Moving, Renaming

```bash
# Copy:
cp file.txt backup.txt           # Copy file
cp -r mydir/ backup/             # Copy directory recursively
cp -p file.txt dest/             # Preserve permissions and timestamps
cp -v file.txt dest/             # Verbose — show what's being copied
cp -i file.txt dest/             # Interactive — ask before overwrite
cp *.txt /backup/                # Copy all .txt files

# Move / Rename:
mv file.txt newname.txt          # Rename file
mv file.txt /opt/app/            # Move to directory
mv -i file.txt dest/             # Prompt before overwrite
mv -v *.log /var/log/archive/    # Verbose move

# Rename multiple files:
for f in *.txt; do mv "$f" "${f%.txt}.bak"; done
```

### 6.3 Deleting Files and Directories

```bash
rm file.txt                  # Remove file
rm -f file.txt               # Force remove (no prompt)
rm -i file.txt               # Interactive — ask before delete
rm -v file.txt               # Verbose
rm *.log                     # Remove all .log files
rmdir emptydir               # Remove EMPTY directory only
rm -r mydir/                 # Remove directory recursively
rm -rf mydir/                # Force recursive remove (⚠️ DANGEROUS!)
```

> ⚠️ **`rm -rf /` will DESTROY the entire system.** Always double-check paths before using `-rf`.

### 6.4 Viewing File Contents

```bash
cat file.txt                 # Print entire file
cat -n file.txt              # Print with line numbers
cat file1.txt file2.txt      # Concatenate multiple files

less file.txt                # Page through file (q to quit, /search)
more file.txt                # Older pager (less is better)

head file.txt                # First 10 lines
head -n 20 file.txt          # First 20 lines
head -n 1 file.txt           # First line only

tail file.txt                # Last 10 lines
tail -n 50 file.txt          # Last 50 lines
tail -f /var/log/syslog      # Follow file in real-time (great for logs!)
tail -F /var/log/app.log     # Follow + reopen if file rotated

# Side-by-side comparison:
diff file1.txt file2.txt     # Show differences between files
diff -u file1.txt file2.txt  # Unified diff format (git-style)
```

### 6.5 Finding Files

```bash
# find — most powerful:
find /home -name "*.txt"                  # Find all .txt files in /home
find / -name "nginx.conf"                 # Find file anywhere
find /var/log -name "*.log" -mtime -7    # Modified in last 7 days
find /tmp -type f -size +100M            # Files larger than 100MB
find /home -type d -name "projects"      # Find directories named projects
find / -user alice -type f               # Files owned by alice
find / -perm 777                         # Files with 777 permissions
find . -name "*.log" -delete             # Find AND delete .log files
find . -name "*.txt" -exec grep "error" {} \;  # Find + run command on results

# locate — uses database (faster but not real-time):
locate nginx.conf          # Find file (uses index — updatedb first)
updatedb                   # Rebuild the locate database

# which / whereis:
which python3              # Path of executable
whereis nginx              # Binary + source + man page locations
```

### 6.6 File Compression and Archives

```bash

# gzip / gunzip:
gzip file.txt              # Compress → creates file.txt.gz
gzip -k file.txt           # Compress keeping original
gunzip file.txt.gz         # Decompress
gzip -d file.txt.gz        # Decompress (same as gunzip)
gzip -l file.txt.gz        # List compression info

# zip / unzip:
zip archive.zip file1 file2    # Create zip
zip -r archive.zip directory/  # Zip recursively
unzip archive.zip              # Extract zip
unzip -l archive.zip           # List contents
unzip archive.zip -d /opt/     # Extract to directory


# xz (Best Compression):
xz file.txt                        # Creates file.txt.xz
xz -k file.txt                     # Keep original
xz -d file.txt.xz                  # Decompress
unxz file.txt.xz                   # Same

#bzip2
## Compress (better ratio than gzip, slower):
bzip2 file.txt                     # Creates file.txt.bz2
bzip2 -k file.txt                  # Keep original
bzip2 -9 file.txt                  # Max compression

## Decompress:
bzip2 -d file.txt.bz2
bunzip2 file.txt.bz2


# tar — most common:
 TAR OPTIONS:
 c = create    x = extract   t = list
 v = verbose   f = filename  z = gzip   j = bzip2   J = xz
 C = extract to dir          p = preserve permissions
 --exclude = exclude pattern
 --newer-mtime = incremental backup


tar -cvf archive.tar files/        # Create tar archive
tar -cvzf archive.tar.gz files/    # Create gzip-compressed tar
tar -cvjf archive.tar.bz2 files/   # Create bzip2-compressed tar
tar -xvf archive.tar               # Extract tar archive
tar -xvzf archive.tar.gz           # Extract gzip tar
tar -xvzf archive.tar.gz -C /opt/  # Extract to specific directory
tar -tvf archive.tar               # List contents without extracting
tar -xvzf archive.tar.gz file.txt  # Extract specific file

```



### 6.7 Links — Hard and Symbolic

```bash
# Hard link — another name for the same inode (same data):
ln file.txt hardlink.txt
# Both names point to same data; deleting one keeps the other

# Symbolic (soft) link — like a shortcut/pointer:
ln -s /etc/nginx/nginx.conf ~/nginx.conf
ln -s /opt/app-v2.1/ /opt/app     # Version pointer pattern
ls -la                             # Shows link → target

# View inode numbers:
ls -li                             # Shows inode number

# Find broken symlinks:
find /etc -type l -xtype l         # Find broken symlinks
```

---
## 7. 🐚 Vi / Vim Editor

### 7.1 Vim Modes

```
Normal Mode     → Default mode. Navigate and issue commands.
Insert Mode     → Type/edit text. Enter with: i, I, a, A, o, O
Command Mode    → Run commands. Enter with: : (colon)
Visual Mode     → Select text. Enter with: v, V, Ctrl+v
```

### 7.2 Essential Vim Commands

```bash
vim file.txt        # Open file in vim
vi file.txt         # Open with vi

# MODE SWITCHING:
i        # Insert before cursor
I        # Insert at start of line
a        # Insert after cursor
A        # Insert at end of line
o        # Open new line below
O        # Open new line above
Esc      # Return to Normal mode

# SAVING AND QUITTING (in Command mode — press : first):
:w           # Save (write)
:q           # Quit (if no changes)
:wq          # Save and quit
:x           # Save and quit (same as :wq)
ZZ           # Save and quit (Normal mode shortcut)
:q!          # Quit WITHOUT saving (force)
:w filename  # Save as different filename

# NAVIGATION (Normal mode):
0            # Jump to start of line
$            # Jump to end of line
gg           # Jump to first line of file
G            # Jump to last line of file


# EDITING (Normal mode):
x            # Delete character under cursor
dd           # Delete (cut) current line
5dd          # Delete 5 lines
dw           # Delete word
d$           # Delete to end of line
d0           # Delete to start of line
yy           # Yank (copy) current line
5yy          # Yank 5 lines
p            # Paste after cursor
P            # Paste before cursor
u            # Undo
Ctrl+r       # Redo
>>           # Indent line right
<<           # Indent line left

# SEARCH (Normal mode):
/pattern      # Search forward
?pattern      # Search backward
n             # Next match
N             # Previous match
*             # Search for word under cursor (forward)
#             # Search for word under cursor (backward)

# SEARCH AND REPLACE (Command mode):
:s/old/new/          # Replace first occurrence in current line
:s/old/new/g         # Replace all in current line
:%s/old/new/g        # Replace all in entire file
:%s/old/new/gc       # Replace all with confirmation
:5,10s/old/new/g     # Replace in lines 5-10

# VISUAL MODE:
v            # Character visual mode
V            # Line visual mode
Ctrl+v       # Block visual mode
# Then: d=delete, y=yank, >=indent, <=unindent, :=command

# MULTIPLE FILES:
:e file.txt      # Open another file


# USEFUL COMMANDS:
:set number          # Show line numbers
:set nonumber        # Hide line numbers
:set syntax=python   # Set syntax highlighting
:syntax on           # Enable syntax highlighting
:set paste           # Paste mode (preserves formatting)
:set nopaste         # Disable paste mode
:set ignorecase      # Case-insensitive search
gg=G                 # Auto-indent entire file
```

---
## 8. 🔗 Shell & Environment Variables

### 8.1 Variables

```bash
# Define variables:
name="Alice"                      # No spaces around =
NUMBER=42
readonly CONSTANT="pi"            # Read-only variable

# Use variables:
echo $name
echo ${name}                      # Better syntax — avoids ambiguity
echo ${name:-"default"}           # Use default if variable is empty
echo ${name:="default"}           # Assign default if empty
echo ${#name}                     # Length of variable

# Unset:
unset name                        # Remove variable

# Environment variables (available to subprocesses):
export name="Alice"
export PATH="$PATH:/opt/myapp/bin"

# View all environment variables:
env                               # All exported variables
printenv                          # Same
printenv HOME                     # Specific variable
set                               # All variables + functions (shell)
```

### 8.2 Important Environment Variables

| Variable | Description |
|----------|-------------|
| `$HOME` | Current user's home directory |
| `$USER` / `$LOGNAME` | Current username |
| `$PATH` | Directories searched for commands |
| `$SHELL` | Current shell path |
| `$PWD` | Current working directory |
| `$OLDPWD` | Previous working directory |
| `$HOSTNAME` | Machine hostname |
| `$PS1` | Primary prompt string |
| `$PS2` | Secondary prompt (continuation) |
| `$EDITOR` | Default text editor |
| `$LANG` | System language/locale |
| `$TZ` | Timezone |
| `$UID` | Current user's ID |
| `$?` | Exit status of last command |
| `$!` | PID of last background process |
| `$$` | PID of current shell |
| `$0` | Name of current script/shell |
| `$#` | Number of arguments to script |
| `$@` | All arguments to script |
| `$*` | All arguments as single string |

### 8.3 Shell Profile Files

```bash
# Login shell startup order:
/etc/environment        # System-wide environment variables
/etc/profile            # System-wide profile (all users)
/etc/profile.d/*.sh     # Drop-in profile scripts
~/.bash_profile         # User-specific (login shell)
~/.bash_login           # Fallback if .bash_profile not found
~/.profile              # Fallback (POSIX sh)

# Interactive non-login shell:
/etc/bash.bashrc        # System-wide bashrc
~/.bashrc               # User-specific bashrc

# Reload without logout:
source ~/.bashrc
. ~/.bashrc             # Same as source
```

### 8.4 PATH Management

```bash
# View current PATH:
echo $PATH
# /usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin

# Add to PATH (in ~/.bashrc or ~/.bash_profile):
export PATH="$PATH:/opt/myapp/bin"        # Append
export PATH="/opt/myapp/bin:$PATH"        # Prepend (higher priority)

# Check which binary will run:
which python3
type python3
command -v python3
```
---

## 9. 🐚 Shell Profile Files — `.bash_profile`, `.bashrc`, `.bash_logout`

### 9.1 Profile File Execution Order

```
LOGIN SHELL (SSH, TTY login):
  /etc/environment        → System-wide env vars (all shells)
  /etc/profile            → System-wide (bash login)
  /etc/profile.d/*.sh     → Drop-in scripts
  ~/.bash_profile         → User login config (FIRST choice)
  ~/.bash_login           → Fallback if .bash_profile missing
  ~/.profile              → Fallback (POSIX compatible)
  ~/.bash_logout          → Runs when login shell EXITS

NON-LOGIN INTERACTIVE SHELL (new terminal, bash in GUI):
  /etc/bash.bashrc        → System-wide (Ubuntu/Debian)
  /etc/bashrc             → System-wide (RHEL/CentOS)
  ~/.bashrc               → User-specific interactive config
```

### 9.2 `.bash_profile` — Login Shell Config

```bash
cat ~/.bash_profile
```

```bash
# ~/.bash_profile — runs once at LOGIN
# Purpose: Set environment, PATH, export variables

# Source .bashrc to share settings with non-login shells:
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

# PATH customization:
export PATH="$HOME/.local/bin:$HOME/bin:$PATH"
export PATH="$PATH:/opt/myapp/bin"

# Environment variables:
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
export EDITOR=vim
export PAGER=less
export HISTSIZE=10000
export HISTFILESIZE=20000

# Greeting at login:
echo "Welcome back, $USER! Today is $(date)"
```

### 9.3 `.bashrc` — Interactive Shell Config

```bash
cat ~/.bashrc
```

```bash
# ~/.bashrc — runs for every NEW interactive bash session
# Purpose: Aliases, functions, prompt, history settings

# If not running interactively, exit:
case $- in
    *i*) ;;
      *) return;;
esac

# History settings:
HISTSIZE=10000
HISTFILESIZE=20000
HISTCONTROL=ignoreboth:erasedups   # Ignore duplicates and lines starting with space
HISTTIMEFORMAT="%Y-%m-%d %H:%M:%S "
shopt -s histappend                # Append to history, don't overwrite

# Window size check after each command:
shopt -s checkwinsize

# Prompt customization:
PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
# Colors: 32=green, 34=blue, 31=red, 33=yellow

# Aliases:
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias df='df -h'
alias du='du -sh'
alias free='free -h'
alias ps='ps aux'
alias update='sudo apt update && sudo apt upgrade -y'
alias vi='vim'
alias cls='clear'

# Custom functions:
mkcd() { mkdir -p "$1" && cd "$1"; }
extract() {
    case "$1" in
        *.tar.gz)  tar -xzf "$1" ;;
        *.tar.bz2) tar -xjf "$1" ;;
        *.zip)     unzip "$1" ;;
        *.gz)      gunzip "$1" ;;
        *) echo "Unknown format: $1" ;;
    esac
}
```

### 9.4 `.bash_logout` — Logout Cleanup

```bash
cat ~/.bash_logout
```

```bash
# ~/.bash_logout — runs when LOGIN shell exits
# Purpose: Cleanup, security, messages

# Clear terminal for security:
clear

# Save command history:
history -a

# Remove temp files:
rm -f /tmp/mytempfile 2>/dev/null

# Optional: log logout time
echo "$(date) - $USER logged out from $HOSTNAME" >> ~/.logout_history
```

### 9.5 Applying Changes Without Logout

```bash
source ~/.bashrc           # Reload .bashrc
. ~/.bashrc                # Same (POSIX syntax)
source ~/.bash_profile     # Reload .bash_profile
exec bash                  # Replace current shell with fresh one
```

---

## 10. 🔑 Hidden Files and Aliases

### 10.1 Hidden Files in Linux

```bash
# Files/directories starting with . are hidden:
ls                   # Shows regular files only
ls -a                # Shows ALL including hidden (. files)
ls -la               # Hidden files with details

# Common hidden files in home directory:
~/.bashrc            # Shell config
~/.bash_profile      # Login shell config
~/.bash_history      # Command history
~/.ssh/              # SSH keys directory
~/.gitconfig         # Git config
~/.vimrc             # Vim config
~/.profile           # Generic shell profile

# Create hidden file:
touch .myhiddenfile

# Create hidden directory:
mkdir .myhiddendir

# Find ALL hidden files in a directory:
find /home/alice -name ".*" -type f

# Find hidden files (exclude . and ..):
ls -la | grep '^\.' 
find . -name ".*" ! -name "." ! -name ".."
```

### 10.2 alias — Command Shortcuts

```bash
# Create temporary alias (lost on logout):
alias ll='ls -alF'
alias ..='cd ..'
alias update='sudo apt update && sudo apt upgrade -y'
alias vi='vim'
alias ports='ss -tuln'
alias myip='curl -s ifconfig.me'
alias df='df -h'
alias ping='ping -c 4'

# View all aliases:
alias

# View specific alias:
alias ll

# Remove alias:
unalias ll
unalias -a                         # Remove ALL aliases

# Permanent aliases — add to ~/.bashrc:
echo "alias ll='ls -alF'" >> ~/.bashrc
source ~/.bashrc

# Alias with sudo:
alias apt-update='sudo apt update && sudo apt upgrade -y'

# Useful admin aliases:
alias sysl='sudo journalctl -f'
alias nginx-reload='sudo systemctl reload nginx'
alias grep='grep --color=auto'
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)"'

# Bypass alias (run actual command):
\cp file1 file2          # Run 'cp' not aliased version
command cp file1 file2   # Same
```



---

## 11. 👤 User & Group Management

### 11.1 User Accounts

```bash
# View user info:
whoami                         # Current username
id                             # UID, GID, and groups
id alice                       # Info for specific user
who                            # Currently logged-in users
w                              # Who + what they're doing
users                          # Simple list of logged-in users
finger alice                   # User info (if finger installed)

# User database:
cat /etc/passwd                # All user accounts
# Format: username:x:UID:GID:comment:home:shell
getent passwd alice            # Look up specific user
```

### 11.2 Creating and Managing Users

```bash
# Create user:
useradd alice                            # Basic user creation
useradd -m alice                         # Create with home directory
useradd -m -s /bin/bash alice            # Set shell
useradd -m -s /bin/bash -c "Alice Smith" alice   # Add comment/full name
useradd -m -G sudo,docker alice          # Add to groups
useradd -u 1500 -g 1500 -m alice         # Specify UID and GID
useradd -e 2025-12-31 alice              # Account expiry date
useradd -d /custom/home alice            # Custom home directory

# Set/change password:
passwd alice                             # Set password for alice
passwd                                   # Change own password
echo "alice:MyPass123" | chpasswd        # Set password non-interactively
passwd -l alice                          # Lock account
passwd -u alice                          # Unlock account
passwd -e alice                          # Expire password (force change on login)
passwd -n 7 -x 90 -w 14 alice           # Min 7 days, max 90 days, warn 14 days before

# Modify user:
usermod -s /bin/zsh alice                # Change shell
usermod -d /new/home -m alice            # Change home + move files
usermod -l newname alice                 # Rename user
usermod -aG docker alice                 # Add to group (keep existing groups!)
usermod -G docker alice                  # Set groups (REPLACES existing groups!)
usermod -L alice                         # Lock user
usermod -U alice                         # Unlock user
usermod -e 2025-12-31 alice              # Set expiry

# Delete user:
userdel alice                            # Delete user (keep home dir)
userdel -r alice                         # Delete user + home directory + mail
```

### 11.3 Password Policy — /etc/shadow

```bash
cat /etc/shadow     # Encrypted passwords + expiry info
# Format: user:hash:lastchange:min:max:warn:inactive:expire

chage -l alice              # View password aging for alice
chage -M 90 alice           # Max 90 days before password change required
chage -m 7 alice            # Min 7 days between password changes
chage -W 14 alice           # Warn 14 days before expiry
chage -I 30 alice           # Account inactive after 30 days of expired password
chage -E 2025-12-31 alice   # Account expires on date
chage -d 0 alice            # Force password change on next login
```

### 11.4 Group Management

```bash
# View groups:
cat /etc/group              # All groups
groups                      # Groups current user belongs to
groups alice                # Groups alice belongs to
getent group developers     # Info on specific group

# Create group:
groupadd developers          # Create group
groupadd -g 1500 developers  # Specify GID

# Modify group:
groupmod -n devteam developers   # Rename group
groupmod -g 1600 developers      # Change GID

# Delete group:
groupdel developers              # Delete group

# Add/remove user from group:
gpasswd -a alice developers      # Add alice to developers
gpasswd -d alice developers      # Remove alice from developers
gpasswd -M alice,bob developers  # Set group members (replaces all)
gpasswd -A alice developers      # Make alice group admin

# Switch to group temporarily:
newgrp developers
```

### 11.5 sudo — Privilege Escalation

```bash
# Run command as root:
sudo command                  # Run single command as root
sudo -i                       # Switch to root shell (login shell)
sudo -s                       # Switch to root shell (current env)
sudo -u alice command         # Run command as another user
sudo !!                       # Re-run last command with sudo
su -                          # Switch to root (needs root password)
su alice                      # Switch to alice user

# Edit sudoers (ALWAYS use visudo — validates syntax!):
visudo                        # Edit /etc/sudoers safely
visudo -f /etc/sudoers.d/alice  # Edit a drop-in file

# Common sudoers entries:
# alice ALL=(ALL) ALL                      → alice can run everything as root
# alice ALL=(ALL) NOPASSWD: ALL            → No password prompt
# alice ALL=(ALL) NOPASSWD: /sbin/reboot   → Only specific command
# %developers ALL=(ALL) ALL               → Group developers

# Add user to sudo group (Ubuntu/Debian):
usermod -aG sudo alice

# Add user to wheel group (RHEL/CentOS):
usermod -aG wheel alice
```

### 11.6 Key User Files

| File | Contents |
|------|---------|
| `/etc/passwd` | User accounts (username, UID, GID, home, shell) |
| `/etc/shadow` | Encrypted passwords + aging info (root only) |
| `/etc/group` | Group definitions and memberships |
| `/etc/gshadow` | Secure group info |
| `/etc/sudoers` | Sudo rules |
| `/etc/skel/` | Template files copied to new user home dirs |
| `/etc/login.defs` | Default values for user account creation |
---

## 12. 👥 UIDs, GIDs — User and Group IDs in Linux

### 12.1 UID — User ID

Every user has a **UID (User ID)** — a numeric identifier. UIDs are unique per user.

```
UID 0        → root (ALWAYS — superuser on all Linux systems)
UID 1–999    → System users / service accounts (nginx, www-data, mysql)
UID 1000+    → Regular users (first human user = 1000 on most distros)
```

```bash
# View UIDs:
id                                 # Your UID, GID, and groups
id alice                           # Specific user's UID
cat /etc/passwd                    # All users with UIDs
# Format: username:x:UID:GID:comment:home:shell
# root:x:0:0:root:/root:/bin/bash
# alice:x:1001:1001:Alice:/home/alice:/bin/bash

getent passwd alice                # Look up by name
getent passwd 1001                 # Look up by UID
```

### 12.2 GID — Group ID

```
GID 0        → root group
GID 1–999    → System groups (daemon, bin, sys, www-data)
GID 1000+    → User groups (usually matching their UID)
```

```bash
# View groups:
cat /etc/group
# Format: groupname:x:GID:member1,member2
# root:x:0:
# sudo:x:27:alice,bob
# developers:x:1500:alice,carol

groups                             # Your groups
groups alice                       # Alice's groups
id alice                           # UID + all GIDs

# Numeric group info:
getent group developers
getent group 1500
```

### 12.3 root User Special Properties

```bash
# root is ALWAYS UID=0, GID=0 — regardless of username
# (If you rename root to 'admin', UID=0 still has full power)

whoami                             # Shows "root" if UID=0
id                                 # uid=0(root) gid=0(root)

# root's home: /root (not /home/root)
# root's shell: /bin/bash (can run anything)

# Check if running as root in scripts:
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

# Or:
if [ "$(id -u)" != "0" ]; then
    echo "Must be root"
    exit 1
fi
```

### 12.4 Convert Root User ↔ Normal User

```bash
# Convert normal user to ROOT-equivalent (dangerous!):
# Method 1: Change UID to 0 in /etc/passwd
usermod -u 0 alice              # ⚠️ Now alice has root power!
# Edit /etc/passwd:  alice:x:0:0:Alice:/home/alice:/bin/bash

# Method 2: Add to sudo/wheel group (SAFER — recommended):
usermod -aG sudo alice          # Ubuntu — sudo group
usermod -aG wheel alice         # RHEL/CentOS — wheel group

# Convert root-equivalent user BACK to normal:
usermod -u 1001 alice           # Assign a normal UID
# Edit /etc/passwd to remove from root GID

# Check current sudo access:
sudo -l -U alice                # List alice's sudo privileges
```


---
## 13. 📁 /etc/passwd and /etc/shadow — User Database Files

### 13.1 /etc/passwd — User Account Database

```bash
cat /etc/passwd
# root:x:0:0:root:/root:/bin/bash
# daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
# alice:x:1001:1001:Alice Smith,,,:/home/alice:/bin/bash
```

**Field breakdown:**

```
root  :  x  :  0  :  0  :  root  :  /root  :  /bin/bash
 ①       ②     ③    ④      ⑤        ⑥           ⑦

① username        → login name
② password        → 'x' means stored in /etc/shadow; '' = no password
③ UID             → User ID (0 = root)
④ GID             → Primary Group ID
⑤ GECOS/comment   → Full name, room, phone (comma-separated)
⑥ home directory  → Path to home
⑦ shell           → Login shell (/sbin/nologin = no login allowed)
```

```bash
# Common nologin shells (system accounts that can't login):
/sbin/nologin
/usr/sbin/nologin
/bin/false

# Create user with home directory and specific settings:
useradd -m -d /home/alice -s /bin/bash -c "Alice Smith" -u 1001 -g 1001 alice
```

### 13.2 /etc/shadow — Encrypted Password Storage

```bash
# Only readable by root:
sudo cat /etc/shadow
# alice:$6$salt$hashedpassword:19000:0:90:14:::
```

**Field breakdown:**

```
alice : $6$... : 19000 : 0  : 90  : 14  :     :     :
 ①       ②        ③      ④    ⑤     ⑥     ⑦     ⑧    ⑨

① username
② password hash  ($6$=SHA-512, $5$=SHA-256, $1$=MD5, !!= locked, *=no login)
③ last change    → days since 1970-01-01 when password was last changed
④ min days       → min days before password can change (0 = any time)
⑤ max days       → max days before password must change (99999 = never)
⑥ warn days      → warn N days before password expires
⑦ inactive days  → days after expiry before account disabled
⑧ expire date    → absolute date account expires (days since epoch)
⑨ reserved
```

```bash
# View password aging:
chage -l alice

# Force password change on next login:
chage -d 0 alice

# Lock/unlock account (prefixes hash with !):
passwd -l alice         # Lock
passwd -u alice         # Unlock
usermod -L alice        # Lock (alternative)
usermod -U alice        # Unlock (alternative)
```

---

## 14. 🔄 /etc/inittab and Runlevels — Switching Between GUI and CLI

### 14.1 Traditional Runlevels (/etc/inittab)

```bash
# Traditional SysV init runlevels (pre-systemd):
cat /etc/inittab        # On older RHEL 6 and below systems
```

```
# Runlevel definitions:
# 0 → Halt (shutdown)
# 1 → Single-user mode (recovery/maintenance)
# 2 → Multi-user, no networking (Debian/Ubuntu)
# 3 → Multi-user with networking, NO GUI (CLI mode)
# 4 → Unused (user-definable)
# 5 → Multi-user with networking AND GUI
# 6 → Reboot

# /etc/inittab format (RHEL 6):
# id:runlevel:action:process
id:3:initdefault:       ← Boot into CLI mode (runlevel 3)
id:5:initdefault:       ← Boot into GUI mode (runlevel 5)
```

### 14.2 Switching Between GUI and CLI (Modern systemd)

```bash
# View current target (equivalent of runlevel):
systemctl get-default

# Switch to CLI mode (no GUI) — runlevel 3 equivalent:
systemctl set-default multi-user.target     # Permanent (survives reboot)
systemctl isolate multi-user.target         # Immediate (no reboot needed)

# Switch to GUI mode — runlevel 5 equivalent:
systemctl set-default graphical.target      # Permanent
systemctl isolate graphical.target          # Immediate

# Other targets:
systemctl isolate rescue.target             # Single-user recovery mode
systemctl isolate emergency.target          # Emergency mode (read-only root)

# Reboot / Shutdown:
systemctl reboot
systemctl poweroff
systemctl halt
init 6                                      # Legacy: reboot
init 0                                      # Legacy: shutdown
```

### 14.3 Runlevel-to-Target Mapping

| Old Runlevel | systemd Target | Description |
|:---:|---|---|
| 0 | `poweroff.target` | Shutdown |
| 1 | `rescue.target` | Single-user/rescue |
| 2, 3, 4 | `multi-user.target` | CLI multi-user |
| 5 | `graphical.target` | GUI |
| 6 | `reboot.target` | Reboot |

```bash
# Legacy runlevel commands still work:
runlevel            # Show current and previous runlevel
telinit 3           # Switch to runlevel 3
who -r              # Show current runlevel
```

---

## 15. 📊 wall — Broadcast Message to All Users

```bash
# wall (write all) — send message to all logged-in terminal users:
wall "Server will reboot in 10 minutes for maintenance"
wall < message.txt                # Send file contents

# With timeout (mesg must be enabled):
echo "Maintenance at 10 PM tonight" | wall

# /etc/motd — Message of the Day (shown at login):
cat /etc/motd
echo "Welcome! Please read /etc/policies before proceeding" > /etc/motd

# /etc/issue — Shown BEFORE login prompt:
cat /etc/issue
echo "Unauthorized access is prohibited" > /etc/issue

# /etc/issue.net — Shown for network logins (SSH):
cat /etc/issue.net

# Enable issue.net banner in SSH:
# /etc/ssh/sshd_config:  Banner /etc/issue.net
```

---

---

## 16. ⚙️ Systemd & Service Management

### 16.1 systemctl — Control Services

```bash
# Service state:
systemctl status nginx               # Status of nginx service
systemctl is-active nginx            # Just returns active/inactive
systemctl is-enabled nginx           # Returns enabled/disabled/static

# Start / Stop / Restart:
systemctl start nginx                # Start service
systemctl stop nginx                 # Stop service
systemctl restart nginx              # Stop then start
systemctl reload nginx               # Reload config (no downtime)
systemctl try-restart nginx          # Restart only if running
systemctl try-reload-or-restart nginx # Reload if supported, else restart

# Enable / Disable (start at boot):
systemctl enable nginx               # Enable at boot
systemctl disable nginx              # Disable at boot
systemctl enable --now nginx         # Enable AND start immediately
systemctl disable --now nginx        # Disable AND stop immediately

# Mask / Unmask (completely prevent starting):
systemctl mask nginx                 # Prevent starting (even manually)
systemctl unmask nginx               # Unmask service

# List services:
systemctl list-units                 # All loaded units
systemctl list-units --type=service  # Only services
systemctl list-units --state=failed  # Failed services
systemctl list-unit-files            # All unit files + enabled status
```

### 16.2 systemd Unit Files

```bash
# Unit file locations:
/lib/systemd/system/             # System-provided unit files (don't edit)
/etc/systemd/system/             # Admin-created/overriding unit files
/etc/systemd/system/nginx.d/     # Drop-in override directory

# View unit file:
systemctl cat nginx              # Print unit file content
systemctl edit nginx             # Edit/create drop-in override
systemctl edit --full nginx      # Edit the full unit file

# Example service unit file:
cat /etc/systemd/system/myapp.service
```

```ini
[Unit]
Description=My Application
After=network.target
Requires=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/start.sh
ExecStop=/opt/myapp/bin/stop.sh
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5s
StandardOutput=journal
StandardError=journal
Environment=APP_ENV=production
EnvironmentFile=/etc/myapp/env

[Install]
WantedBy=multi-user.target
```

```bash
# After creating/modifying unit files:
systemctl daemon-reload          # Reload systemd config
systemctl enable --now myapp     # Enable and start
```

### 16.3 journalctl — System Logs

```bash
# View all logs:
journalctl                           # All logs (oldest first)
journalctl -r                        # Reverse (newest first)
journalctl -f                        # Follow (live logs)
journalctl -n 50                     # Last 50 lines
journalctl -n 100 -f                 # Last 100 then follow

# Filter by unit:
journalctl -u nginx                  # Logs for nginx
journalctl -u nginx -f               # Follow nginx logs
journalctl -u nginx --since "1 hour ago"
journalctl -u nginx.service -u mysql.service  # Multiple units

# Filter by time:
journalctl --since "2025-01-15 10:00:00"
journalctl --since "1 hour ago" --until "30 min ago"
journalctl --since today
journalctl --since yesterday

# Filter by priority:
journalctl -p err                    # Errors only
journalctl -p warning                # Warnings and above
journalctl -p 0..3                   # emerg, alert, crit, err

# Filter by kernel/boot:
journalctl -k                        # Kernel messages only
journalctl -b                        # Current boot logs
journalctl -b -1                     # Previous boot logs
journalctl --list-boots              # All recorded boots

# Disk usage:
journalctl --disk-usage              # How much space logs use
journalctl --vacuum-size=500M        # Keep only 500MB of logs
journalctl --vacuum-time=30d         # Delete logs older than 30 days
```

### 16.4 Runlevels and Targets

```bash
# systemd targets (replace old runlevels):
# poweroff.target  = runlevel 0
# rescue.target    = runlevel 1
# multi-user.target = runlevel 3 (no GUI)
# graphical.target = runlevel 5 (with GUI)
# reboot.target    = runlevel 6

systemctl get-default                     # Current default target
systemctl set-default multi-user.target   # Set default (no GUI)
systemctl set-default graphical.target    # Set default (with GUI)
systemctl isolate rescue.target           # Switch to rescue mode now
```

---


## 17. ⚙️ Process Management

### 17.1 Viewing Processes

```bash
# ps — process snapshot:
ps                      # Processes in current terminal
ps aux                  # ALL processes (BSD syntax) — most common
ps aux | grep nginx     # Find specific process
ps -ef                  # All processes (full format)
ps -u alice             # Processes owned by alice
ps -p 1234              # Process with specific PID
ps --sort=-%cpu         # Sort by CPU usage (descending)
ps --sort=-%mem         # Sort by memory usage

# top — real-time process monitor:
top                     # Interactive process viewer
top -u alice            # Show only alice's processes
top -p 1234,5678        # Monitor specific PIDs

# htop — improved top (install separately):
htop                    # Color-coded, mouse-enabled process viewer

# pgrep / pidof — find PIDs:
pgrep nginx             # Get PID(s) of nginx
pgrep -u alice          # All PIDs for alice
pidof nginx             # PID of nginx (exact name match)
```

### 17.2 Process States

| State | Symbol | Meaning |
|-------|:------:|---------|
| Running | `R` | Actively using CPU |
| Sleeping (interruptible) | `S` | Waiting for event (can be woken) |
| Sleeping (uninterruptible) | `D` | Waiting for I/O (cannot be interrupted) |
| Stopped | `T` | Suspended (Ctrl+Z) |
| Zombie | `Z` | Finished but parent hasn't acknowledged |

### 17.3 Signals and killing processes

```bash
# kill — send signal to process:
kill 1234                # Send SIGTERM (15) — graceful stop
kill -9 1234             # Send SIGKILL — force kill (cannot be ignored)
kill -15 1234            # SIGTERM (graceful)
kill -1 1234             # SIGHUP — reload config
kill -19 1234            # SIGSTOP — pause process
kill -18 1234            # SIGCONT — resume paused process

# killall — kill by name:
killall nginx            # Kill all processes named nginx
killall -9 nginx         # Force kill
killall -u alice         # Kill all alice's processes

# pkill — kill by pattern:
pkill nginx              # Kill matching process name
pkill -9 -u alice        # Force kill all alice's processes
pkill -f "python app.py" # Kill by full command match

# Common signals:
# SIGTERM (15) → Ask process to terminate gracefully
# SIGKILL (9)  → Force kill — always works, no cleanup
# SIGHUP (1)   → Hangup — daemons reload config on this
# SIGINT (2)   → Interrupt (Ctrl+C)
# SIGSTOP (19) → Pause process
# SIGCONT (18) → Resume paused process
```

### 17.4 Background and Foreground Jobs

```bash
command &               # Run command in background
Ctrl + Z                # Suspend (pause) current foreground job
jobs                    # List background/suspended jobs
fg                      # Bring most recent job to foreground
fg %2                   # Bring job #2 to foreground
bg                      # Resume suspended job in background
bg %2                   # Resume job #2 in background
disown %1               # Remove job from shell's job table

# nohup — run command immune to hangup:
nohup ./script.sh &     # Keeps running after logout
nohup ./script.sh > output.log 2>&1 &  # With output redirect
```

### 17.5 Process Priority (nice / renice)

```bash
# nice value range: -20 (highest priority) to 19 (lowest)
# Default nice value: 0

# Start process with specific priority:
nice -n 10 ./heavy-script.sh     # Lower priority (be nice to others)
nice -n -10 ./critical.sh        # Higher priority (needs root for negative)

# Change priority of running process:
renice -n 5 -p 1234              # Change PID 1234 to nice 5
renice -n 10 -u alice            # Change all of alice's processes
renice -n -5 -p 1234             # Raise priority (root only)

# View nice values:
ps aux --sort=ni                 # Sort by nice value
top                              # NI column shows nice value
```

### 17.6 /proc — Process Information

```bash
ls /proc/                        # Each number = a PID directory
cat /proc/1/status               # Status of PID 1 (systemd/init)
cat /proc/1/cmdline              # Command line of PID 1
cat /proc/cpuinfo                # CPU details
cat /proc/meminfo                # Memory details
cat /proc/uptime                 # Uptime in seconds
cat /proc/loadavg                # Load averages (1, 5, 15 min)
cat /proc/net/if_inet6           # IPv6 interface info
cat /proc/sys/kernel/hostname    # Current hostname
```

---

## 18. 🧠 Memory & CPU Management

### 18.1 Memory Information

```bash
free -h                             # Memory summary
cat /proc/meminfo                   # Detailed memory info
vmstat -s                           # Memory stats

# Fields explained (free -h):
# total = total RAM
# used = used RAM
# free = completely free RAM
# shared = tmpfs/shared memory
# buff/cache = disk cache (can be freed if needed)
# available = memory actually available for new processes
```

### 18.2 Checking CPU Info

```bash
lscpu                               # CPU architecture and details
cat /proc/cpuinfo                   # Detailed per-core CPU info
nproc                               # Number of processing units
mpstat -P ALL 1                     # Per-CPU utilization
top                                 # CPU + process monitor

# CPU temperature (needs lm-sensors):
sensors                             # Temperature readings
sensors-detect                      # Detect sensor chips
```

### 18.3 Memory Management

```bash
# Clear page cache (safe to run):
sync && echo 1 > /proc/sys/vm/drop_caches    # Clear page cache
sync && echo 2 > /proc/sys/vm/drop_caches    # Clear dentries and inodes
sync && echo 3 > /proc/sys/vm/drop_caches    # Clear all

# OOM (Out of Memory) Killer:
dmesg | grep -i "oom"               # Check if OOM killer fired
dmesg | grep "Killed process"       # What was killed
cat /proc/<PID>/oom_score           # OOM score for process (higher = more likely killed)

# Adjust OOM score for critical process:
echo -1000 > /proc/<PID>/oom_score_adj    # Never kill this process
echo 1000 > /proc/<PID>/oom_score_adj     # Kill this first
```

---

## 19. 📋 Linux Logs & Monitoring

### 19.1 Key Log Files

| Log File | Contents |
|----------|---------|
| `/var/log/syslog` | General system messages (Debian/Ubuntu) |
| `/var/log/messages` | General system messages (RHEL/CentOS) |
| `/var/log/auth.log` | Auth events: SSH, sudo, login (Debian/Ubuntu) |
| `/var/log/secure` | Auth events (RHEL/CentOS) |
| `/var/log/kern.log` | Kernel messages |
| `/var/log/dmesg` | Boot + hardware messages |
| `/var/log/cron` | Cron job logs |
| `/var/log/maillog` | Mail server logs |
| `/var/log/nginx/` | Nginx access + error logs |
| `/var/log/apache2/` | Apache logs |
| `/var/log/mysql/` | MySQL logs |
| `/var/log/audit/audit.log` | Audit daemon logs (auditd) |

```bash
# Read logs:
cat /var/log/syslog
tail -f /var/log/syslog              # Live monitoring
tail -n 100 /var/log/auth.log        # Last 100 lines
grep "Failed" /var/log/auth.log      # Find failed logins
grep "error" /var/log/nginx/error.log | tail -50

# dmesg — kernel ring buffer:
dmesg                                # All kernel messages
dmesg | tail -50                     # Last 50 kernel messages
dmesg | grep -i error                # Errors only
dmesg -T                             # With human-readable timestamps
dmesg -w                             # Follow mode
dmesg --level=err,crit               # Filter by level
```

### 19.2 logrotate — Log Rotation

```bash
# Config files:
cat /etc/logrotate.conf              # Global config
ls /etc/logrotate.d/                 # Per-application configs

# Example /etc/logrotate.d/nginx:
# /var/log/nginx/*.log {
#     daily
#     missingok
#     rotate 14
#     compress
#     delaycompress
#     notifempty
#     sharedscripts
#     postrotate
#         nginx -s reopen
#     endscript
# }

# Test logrotate config:
logrotate -d /etc/logrotate.conf     # Debug/dry run
logrotate -f /etc/logrotate.d/nginx  # Force rotation now
```

### 19.3 System Monitoring Tools

```bash
# top — built-in process monitor:
top
# Keys: q=quit, k=kill, r=renice, M=sort by mem, P=sort by CPU
# 1=toggle CPU cores, f=fields, u=filter by user

# vmstat — virtual memory statistics:
vmstat 1 10              # Update every 1 sec, 10 times
vmstat -s                # Memory statistics summary
vmstat -d                # Disk statistics

# iostat — CPU and disk I/O:
iostat 1 5               # Every 1 sec, 5 times
iostat -x 1              # Extended disk stats
iostat -h                # Human-readable

# sar — system activity reporter:
sar 1 5                  # CPU usage every 1 sec
sar -r 1 5               # Memory usage
sar -b 1 5               # I/O statistics
sar -n DEV 1 5           # Network stats
sar -q 1 5               # Load averages and queue
sar -A 1 1               # All stats

# mpstat — multi-processor statistics:
mpstat 1 5               # CPU stats per processor
mpstat -P ALL 1          # Stats for all CPUs

# free — memory usage:
free -h                  # Human-readable
free -s 2                # Refresh every 2 seconds
```

---

## 20. 💾 Disk & Storage Management

### 20.1 Disk Usage and Space

```bash
# df — disk filesystem usage:
df -h                    # Human-readable sizes
df -H                    # SI units (1000-based, not 1024)
df -hT                   # Include filesystem type
df -h /home              # Space info for specific mount
df -i                    # Inode usage (not just space)

# du — directory/file usage:
du -sh /var/log          # Total size of directory (human-readable)
du -sh *                 # Size of each item in current directory
du -h --max-depth=1 /    # One level deep from root
du -ah /etc | sort -rh | head -20  # Largest files/dirs, sorted

# Find largest files:
find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null
du -a / 2>/dev/null | sort -rn | head -20
```

### 20.2 Disk Partitions

```bash
# View disks and partitions:
lsblk                    # Tree view of block devices
lsblk -f                 # Include filesystem type and UUIDs
fdisk -l                 # List all partitions
fdisk -l /dev/sda        # Specific disk
parted -l                # More detailed partition info
blkid                    # Block device UUIDs and types

# Partition tool — fdisk (MBR/DOS):
fdisk /dev/sdb           # Open disk for partitioning
# Inside fdisk: p=print, n=new, d=delete, t=type, w=write, q=quit

# Partition tool — parted (supports GPT and MBR):
parted /dev/sdb
# parted> mklabel gpt
# parted> mkpart primary ext4 1MiB 100%
# parted> quit

# gdisk — for GPT partitions:
gdisk /dev/sdb
```

### 20.3 Filesystems

```bash
# Create filesystem:
mkfs.ext4 /dev/sdb1              # Format as ext4
mkfs.xfs /dev/sdb1               # Format as XFS
mkfs.btrfs /dev/sdb1             # Format as Btrfs
mkfs.fat -F 32 /dev/sdb1         # Format as FAT32
mkfs.ntfs /dev/sdb1              # Format as NTFS

# Check/repair filesystem:
fsck /dev/sdb1                   # Check filesystem (unmounted!)
fsck -y /dev/sdb1                # Auto-answer yes to repairs
fsck.ext4 /dev/sdb1              # Ext4 specific check
e2fsck -f /dev/sdb1              # Force check ext4
xfs_repair /dev/sdb1             # Repair XFS filesystem
```

### 20.4 Mounting and Unmounting

```bash
# Mount:
mount /dev/sdb1 /mnt/data                      # Basic mount
mount -t ext4 /dev/sdb1 /mnt/data             # Specify type
mount -o ro /dev/sdb1 /mnt/data               # Mount read-only
mount -o rw,noexec /dev/sdb1 /mnt/data        # Multiple options
mount -t nfs 192.168.1.10:/share /mnt/nfs     # NFS mount
mount -t tmpfs tmpfs /mnt/ramdisk -o size=512m # RAM disk

# Unmount:
umount /mnt/data                # Unmount by mountpoint
umount /dev/sdb1                # Unmount by device
umount -f /mnt/data             # Force unmount
umount -l /mnt/data             # Lazy unmount (when busy)

# View current mounts:
mount                           # All current mounts
mount | grep sdb1               # Specific device
cat /proc/mounts                # Kernel's view of mounts
findmnt                         # Tree view of mounts
findmnt /mnt/data               # Specific mountpoint info
```

### 20.5 /etc/fstab — Persistent Mounts

```bash
cat /etc/fstab
# Format: device  mountpoint  fstype  options  dump  pass

# Example entries:
# /dev/sda1            /           ext4    defaults       0  1
# UUID=abc-123         /home       ext4    defaults       0  2
# /dev/sdb1            /mnt/data   xfs     defaults,nofail 0  2
# 192.168.1.10:/share  /mnt/nfs    nfs     defaults       0  0
# tmpfs                /tmp        tmpfs   size=1G,noexec 0  0

# Test fstab entries without rebooting:
mount -a                # Mount all filesystems in /etc/fstab

# Get UUID for fstab:
blkid /dev/sdb1         # Shows UUID
lsblk -f                # Shows UUIDs in tree view
```


### 20.6 Swap Space

```bash
# View swap:
swapon --show              # Current swap usage
free -h                    # Shows swap in memory overview

# Create and enable a swap file:
fallocate -l 2G /swapfile  # Create 2GB swap file
chmod 600 /swapfile        # Secure it
mkswap /swapfile           # Format as swap
swapon /swapfile           # Activate swap

# Add to /etc/fstab for persistence:
echo '/swapfile none swap sw 0 0' >> /etc/fstab

# Enable/disable swap:
swapon -a                  # Enable all swap in /etc/fstab
swapoff -a                 # Disable all swap
swapoff /swapfile          # Disable specific swap

# Swappiness (how aggressively kernel uses swap):
cat /proc/sys/vm/swappiness          # Current value (default: 60)
sysctl vm.swappiness=10              # Temporary change
echo 'vm.swappiness=10' >> /etc/sysctl.conf  # Permanent
```
---

## 21. 💾 Advanced Disk Management — fdisk, Partitions & Filesystems

### 21.1 Understanding Partition Types

| Type | Description | Use case |
|------|-------------|---------|
| **Primary** | Max 4 per disk (MBR) | Bootable, OS partitions |
| **Extended** | Container for logical partitions | Workaround 4-partition limit |
| **Logical** | Lives inside extended partition | Data, home, swap |
| **GPT** | No limit, modern standard | All modern systems |

```
MBR Disk (max 4 primary):
  sda1 → Primary (/)
  sda2 → Primary (/boot)
  sda3 → Extended (container)
    sda5 → Logical (/home)
    sda6 → Logical (swap)
    sda7 → Logical (/data)
```

### 21.2 fdisk — Complete Command Reference

```bash
# Open disk for partitioning (⚠️ DESTRUCTIVE — backup first!):
fdisk /dev/sdb

# fdisk interactive menu:
m     # Help — show all commands
p     # Print partition table (view current partitions)
n     # New partition
d     # Delete partition
t     # Change partition type
l     # List known partition types
a     # Toggle bootable flag
w     # Write and exit (SAVES CHANGES)
q     # Quit WITHOUT saving
```

**Step-by-step: Create Primary + Extended + Logical partitions:**

```bash
fdisk /dev/sdb

# Create Primary partition (sdb1):
Command: n
Partition type: p         # p = primary
Partition number: 1
First sector: [Enter]     # Accept default
Last sector: +5G          # 5GB primary partition

# Create Primary partition (sdb2):
Command: n
Partition type: p
Partition number: 2
First sector: [Enter]
Last sector: +10G

# Create Extended partition (sdb3) — container:
Command: n
Partition type: e         # e = extended
Partition number: 3
First sector: [Enter]
Last sector: [Enter]      # Use remaining disk space

# Create Logical partition inside extended (sdb5):
Command: n
Partition type: l         # l = logical (auto inside extended)
First sector: [Enter]
Last sector: +5G

# Create another Logical partition (sdb6):
Command: n
# (type l is auto-selected for logical)
First sector: [Enter]
Last sector: +2G          # Swap partition

# Set type for swap partition:
Command: t
Partition number: 6
Hex code: 82              # 82 = Linux swap  (83 = Linux, 8e = LVM)

# View partition table:
Command: p

# Write to disk:
Command: w                # ← THIS ACTUALLY SAVES ALL CHANGES
```

### 21.3 Creating Filesystems (mkfs)

```bash
# After partitioning, format with filesystem:
mkfs.ext4 /dev/sdb1              # ext4 (most common)
mkfs.xfs /dev/sdb2               # XFS (RHEL default, good for large files)
mkfs.btrfs /dev/sdb3             # Btrfs (snapshots, RAID)
mkfs.fat -F 32 /dev/sdb4         # FAT32 (USB drives, Windows compat)
mkfs.vfat /dev/sdb4              # FAT32 (same)
mkswap /dev/sdb6                 # Swap partition
swapon /dev/sdb6                 # Activate swap

# mkfs options:
mkfs.ext4 -L "DataDisk" /dev/sdb1       # Set volume label
mkfs.ext4 -b 4096 /dev/sdb1            # 4096 byte block size
mkfs.ext4 -m 1 /dev/sdb1              # Reserve only 1% for root (vs default 5%)
mkfs.ext4 -j /dev/sdb1               # With journal

# Tune ext4 after creation:
tune2fs -L "DataDisk" /dev/sdb1        # Set/change label
tune2fs -l /dev/sdb1                   # List filesystem info
tune2fs -c 30 /dev/sdb1               # Check every 30 mounts
tune2fs -m 2 /dev/sdb1               # Change reserved space to 2%
```

### 21.4 /etc/fstab — Permanent Mounts

```bash
cat /etc/fstab
```

```
# Format:
# <device>  <mountpoint>  <type>  <options>  <dump>  <pass>
#
# device:  /dev/sdb1 or UUID=xxx or LABEL=xxx
# dump:    0=no backup, 1=backup (legacy field)
# pass:    0=no check, 1=root first, 2=other FS

# Examples:
UUID=abc-123-def   /             ext4   defaults            0  1
UUID=xyz-456-ghi   /home         ext4   defaults,noatime    0  2
/dev/sdb1          /mnt/data     xfs    defaults,nofail     0  2
/dev/sdb6          none          swap   sw                  0  0
192.168.1.10:/share /mnt/nfs    nfs    defaults,_netdev    0  0
tmpfs              /tmp          tmpfs  size=1G,noexec      0  0

# Mount options:
# defaults   = rw,suid,dev,exec,auto,nouser,async
# noatime    = Don't update access time (faster reads)
# nofail     = Don't fail boot if device missing
# ro         = Read only
# rw         = Read-write
# noexec     = No execute
# nosuid     = Ignore SUID bits
# _netdev    = Network device (wait for network before mounting)
# errors=remount-ro  = Remount read-only on errors
```

```bash
# Test fstab before rebooting:
mount -a             # Mount all fstab entries
mount -fav           # Dry run (-f = fake)

# Get UUID for fstab:
blkid /dev/sdb1
# /dev/sdb1: UUID="abc-123-def" TYPE="ext4"
```


---


## 22. 🗂️ Inodes — Understanding the Linux Filesystem Internals

### 22.1 What is an Inode?

An **inode** (index node) is a data structure that stores **metadata** about a file — everything **except** the filename and file content.

```
Filename  →  Inode Number  →  Inode (metadata)  →  Data Blocks
```

**Inode stores:**
- File type (regular, directory, symlink, etc.)
- File permissions (rwxr-xr-x)
- Owner UID and Group GID
- File size
- Timestamps (access, modify, change)
- Number of hard links
- Pointers to data blocks on disk

**Inode does NOT store:**
- The filename (stored in directory entries)
- The file content (stored in data blocks)

### 22.2 Inode Commands

```bash
# View inode number:
ls -li file.txt                        # -i flag shows inode number
stat file.txt                          # Full inode metadata

# Check inode usage (filesystems have limited inodes!):
df -i                                  # Inode usage per filesystem
df -ih                                 # Human-readable inode usage

# Find files by inode number:
find / -inum 12345

# Inode count when creating filesystem:
mkfs.ext4 -N 1000000 /dev/sdb1         # Set specific inode count
mkfs.ext4 -i 4096 /dev/sdb1           # 1 inode per 4096 bytes
tune2fs -l /dev/sda1 | grep -i inode   # View inode info for ext4
```

### 22.3 Hard Links and Inodes

```bash
# Hard links share the same inode:
ln file.txt hardlink.txt
ls -li file.txt hardlink.txt
# Both show SAME inode number — they are the same file!

# The inode link count increases:
stat file.txt           # Nlinks: 2 (original + 1 hardlink)

# Deleting a file just reduces the link count:
rm file.txt             # Nlinks: 1 — data still accessible via hardlink!
rm hardlink.txt         # Nlinks: 0 — data blocks freed

# Hard link limitations:
# ❌ Cannot cross filesystem boundaries
# ❌ Cannot link to directories (normally)
# ✅ Same inode = same permissions and ownership
```

### 22.4 Soft Links (Symbolic Links) and Inodes

```bash
# Soft link gets its OWN inode — just stores target path:
ln -s /etc/nginx/nginx.conf ~/nginx.conf
ls -li /etc/nginx/nginx.conf ~/nginx.conf
# DIFFERENT inode numbers!

stat ~/nginx.conf
# File: nginx.conf -> /etc/nginx/nginx.conf   ← shows target
# Size: 20  (just the length of the path string)

# Soft link can cross filesystems:
ln -s /mnt/nfs/data /opt/data     # ✅ Works across filesystems

# Broken symlink (target deleted):
ln -s /tmp/deleted.txt mylink.txt
rm /tmp/deleted.txt
ls -la mylink.txt                  # Shows link, target shown in RED
cat mylink.txt                     # ERROR: No such file or directory
find / -type l -xtype l            # Find broken symlinks
```

---

## 23. 💡 LVM — Logical Volume Management

### 23.1 LVM Concepts

```
Physical Disks/Partitions (PV)
         ↓
    Volume Group (VG)    ← Pool of storage
         ↓
   Logical Volumes (LV) ← Virtual partitions (flexible size)
         ↓
     Filesystem (ext4, xfs, etc.)
```

### 23.2 LVM Commands

```bash
# Physical Volumes (PV):
pvcreate /dev/sdb /dev/sdc         # Initialize disks as PVs
pvdisplay                          # Display PV info
pvs                                # Summary of PVs
pvremove /dev/sdb                  # Remove PV

# Volume Groups (VG):
vgcreate datavg /dev/sdb /dev/sdc  # Create VG from PVs
vgdisplay datavg                   # Display VG info
vgs                                # Summary of VGs
vgextend datavg /dev/sdd           # Add PV to VG
vgreduce datavg /dev/sdd           # Remove PV from VG
vgremove datavg                    # Delete VG

# Logical Volumes (LV):
lvcreate -L 10G -n datalv datavg   # Create 10GB LV
lvcreate -l 100%FREE -n datalv datavg   # Use all free space
lvcreate -l 50%VG -n datalv datavg      # 50% of VG
lvdisplay datavg/datalv            # Display LV info
lvs                                # Summary of LVs

# Format and mount:
mkfs.ext4 /dev/datavg/datalv
mkdir /mnt/data
mount /dev/datavg/datalv /mnt/data

# Add to /etc/fstab:
echo '/dev/datavg/datalv /mnt/data ext4 defaults 0 2' >> /etc/fstab

# Extend LV (online!):
lvextend -L +5G /dev/datavg/datalv          # Add 5GB
lvextend -l +100%FREE /dev/datavg/datalv    # Add all free space
# Resize filesystem after extending:
resize2fs /dev/datavg/datalv                # ext4
xfs_growfs /mnt/data                         # xfs (use mountpoint!)

# Shrink LV (⚠️ risky — backup first!):
umount /mnt/data
e2fsck -f /dev/datavg/datalv               # Must check first
resize2fs /dev/datavg/datalv 8G            # Shrink filesystem to 8GB
lvreduce -L 8G /dev/datavg/datalv          # Then shrink LV
mount /dev/datavg/datalv /mnt/data

# Remove LV:
umount /mnt/data
lvremove /dev/datavg/datalv

# LVM Snapshots:
lvcreate -s -L 2G -n datalv_snap /dev/datavg/datalv   # Create snapshot
mount -o ro /dev/datavg/datalv_snap /mnt/snap          # Mount snapshot
lvremove /dev/datavg/datalv_snap                        # Remove snapshot
```

---

---

## 24. 🔒 RAID — Redundant Array of Independent Disks

### 24.1 RAID Levels Explained

| RAID | Name | Min Disks | Parity | Fault Tolerance | Read Speed | Write Speed |
|------|------|:---------:|:------:|:--------------:|:----------:|:-----------:|
| **0** | Striping | 2 | None | ❌ None | ⚡ Best | ⚡ Best |
| **1** | Mirroring | 2 | None | ✅ N-1 disks | Fast | Moderate |
| **5** | Striping+Parity | **3** | Distributed | ✅ 1 disk | Fast | Moderate |
| **6** | Double Parity | 4 | Double | ✅ 2 disks | Fast | Slower |
| **10** | Stripe+Mirror | 4 | Mirror | ✅ 1 per pair | ⚡ Best | Fast |

### 24.2 RAID-5 — How It Works

```
RAID-5 with 3 disks:

Disk 1    Disk 2    Disk 3
  A1        A2       Ap    ← Ap = parity of A1+A2
  B1        Bp       B2    ← Bp = parity of B1+B2
  Cp        C1       C2    ← Cp = parity of C1+C2

If Disk 1 fails → A2 + Ap can reconstruct A1 (XOR)
Minimum 3 disks | Usable = (N-1) × disk_size
```

### 24.3 RAID-5 Implementation with mdadm

```bash
# Install mdadm:
yum install mdadm -y

# Prepare disks (optional — create partitions first):
fdisk /dev/sdb   # Create partition, type fd (Linux RAID autodetect)
fdisk /dev/sdc
fdisk /dev/sdd

# Create RAID-5 array:
mdadm --create /dev/md0 \
    --level=5 \
    --raid-devices=3 \
    /dev/sdb1 /dev/sdc1 /dev/sdd1

# Monitor creation progress (takes time for large disks):
cat /proc/mdstat
watch -n 2 cat /proc/mdstat        # Auto-refresh every 2 seconds

# View RAID details:
mdadm --detail /dev/md0

# Format and use the RAID device:
mkfs.ext4 /dev/md0
mkdir /mnt/raid5
mount /dev/md0 /mnt/raid5

# Save RAID configuration:
mdadm --detail --scan >> /etc/mdadm/mdadm.conf   # RHEL
mdadm --detail --scan >> /etc/mdadm.conf          # Ubuntu

# Persistent mount (add to /etc/fstab):
echo '/dev/md0 /mnt/raid5 ext4 defaults,nofail 0 2' >> /etc/fstab

# Add spare disk:
mdadm /dev/md0 --add /dev/sde1

# Simulate disk failure and verify recovery:
mdadm /dev/md0 --fail /dev/sdb1              # Mark disk as failed
mdadm --detail /dev/md0                      # See degraded state
mdadm /dev/md0 --remove /dev/sdb1            # Remove failed disk
mdadm /dev/md0 --add /dev/sdf1              # Add replacement disk
# Watch reconstruction:
cat /proc/mdstat

# Stop/remove RAID:
umount /mnt/raid5
mdadm --stop /dev/md0
mdadm --remove /dev/md0
# Zero superblock to clean disks:
mdadm --zero-superblock /dev/sdb1 /dev/sdc1 /dev/sdd1
```

---

## 25. 📦 Package Management

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


## 33. 🌐 DNS Server Setup — named.conf, Record Types, Zones

### 33.1 DNS Concepts

```
DNS Resolution order on Linux:
1. /etc/hosts           (local file)
2. /etc/resolv.conf     (DNS servers to query)
3. DNS Server           (recursive lookup)

# Check resolution order:
cat /etc/nsswitch.conf | grep hosts
# hosts: files dns myhostname
```

### 33.2 /etc/resolv.conf — Client DNS Config

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

### 33.3 DNS Record Types

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

### 33.4 Setting Up BIND DNS Server

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

### 34.1 Installing and Configuring dhcpd

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

### 35.1 Importance of Time Sync

Accurate time is critical for: logs correlation, SSL certificates, Kerberos auth, cron jobs, distributed systems, databases.

### 35.2 chrony (Modern — RHEL 7+, Ubuntu 20.04+)

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

### 35.3 ntpd (Older)

```bash
yum install ntp -y
cat /etc/ntp.conf
# server pool.ntp.org iburst
systemctl enable --now ntpd
ntpstat                       # Sync status
ntpq -p                       # Peer table
```

### 35.4 timedatectl (systemd time management)

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

### 36.1 Samba Overview

Samba allows Linux to share files/printers with **Windows** clients using the **SMB/CIFS** protocol.

```bash
# Install:
yum install samba samba-client samba-common -y   # RHEL
apt install samba samba-common smbclient cifs-utils -y  # Ubuntu
```

### 36.2 Complete smb.conf

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

### 36.3 Samba Setup Steps

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

### 37.1 NFS — Network File System

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

### 37.2 Samba — SMB/CIFS (Windows-compatible sharing)

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

### 38.1 Apache httpd Configuration

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

### 39.1 sudo — Superuser Do

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

### 39.2 visudo — Safe Sudoers Editor

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

## 40. 🔒 Linux Security & Hardening

### 40.1 Security Audit Tools

```bash
# lynis — security auditing:
lynis audit system              # Full system audit
lynis audit system --quick      # Quick scan

# chkrootkit — rootkit detection:
chkrootkit                      # Scan for rootkits

# rkhunter — rootkit hunter:
rkhunter --check                # Scan system
rkhunter --update               # Update database

# auditd — kernel audit system:
systemctl start auditd
auditctl -l                     # List active audit rules
auditctl -a always,exit -F path=/etc/passwd -F perm=wa  # Audit passwd changes
ausearch -f /etc/passwd         # Search audit logs for file

# fail2ban — brute force protection:
systemctl status fail2ban
fail2ban-client status          # Overview of all jails
fail2ban-client status sshd     # SSH jail status
fail2ban-client set sshd unbanip 10.0.0.5  # Unban IP
```

### 40.2 SELinux (RHEL/CentOS)

```bash
# SELinux status:
getenforce                      # Enforcing / Permissive / Disabled
sestatus                        # Detailed status

# Modes:
setenforce 1                    # Set Enforcing (temporary)
setenforce 0                    # Set Permissive (temporary)

# Permanent change (/etc/selinux/config):
# SELINUX=enforcing
# SELINUX=permissive
# SELINUX=disabled

# Context:
ls -Z file.txt                  # View SELinux context
ps -eZ | grep nginx             # Process context
chcon -t httpd_sys_content_t /var/www/html/  # Change context
restorecon -Rv /var/www/html/   # Restore default context

# Boolean settings:
getsebool -a                    # All booleans
setsebool -P httpd_can_network_connect on   # Allow nginx to connect to network

# Troubleshooting:
ausearch -m avc -ts recent      # Recent SELinux denials
sealert -a /var/log/audit/audit.log  # Analyze and suggest fixes
```

### 40.3 AppArmor (Ubuntu/Debian)

```bash
# AppArmor status:
aa-status                       # Status and loaded profiles
apparmor_status                 # Same

# Profile modes:
aa-enforce /etc/apparmor.d/usr.sbin.nginx   # Enforce mode
aa-complain /etc/apparmor.d/usr.sbin.nginx  # Complain mode (log only)
aa-disable /etc/apparmor.d/usr.sbin.nginx   # Disable profile

# Reload:
apparmor_parser -r /etc/apparmor.d/usr.sbin.nginx
```

### 40.4 System Hardening Checklist

```bash
# 1. Keep system updated:
apt update && apt upgrade -y

# 2. Disable unnecessary services:
systemctl disable bluetooth
systemctl disable cups         # Printing service

# 3. Secure SSH (see section 13.4)

# 4. Configure firewall (see section 12)

# 5. Secure kernel parameters (/etc/sysctl.conf):
# Disable IP forwarding (if not a router):
net.ipv4.ip_forward = 0
# Ignore ICMP broadcasts:
net.ipv4.icmp_echo_ignore_broadcasts = 1
# Enable SYN flood protection:
net.ipv4.tcp_syncookies = 1
# Ignore bogus ICMP responses:
net.ipv4.icmp_ignore_bogus_error_responses = 1
# Apply changes:
sysctl -p

# 6. Remove unnecessary packages:
apt autoremove --purge

# 7. Set correct file permissions:
chmod 644 /etc/passwd
chmod 640 /etc/shadow
chmod 644 /etc/group

# 8. Check for SUID/SGID files:
find / -perm /4000 -type f 2>/dev/null   # SUID files
find / -perm /2000 -type f 2>/dev/null   # SGID files

# 9. Lock unused user accounts:
passwd -l sync
passwd -l news
# Or remove login shell:
usermod -s /sbin/nologin sync

# 10. Enable auditd:
systemctl enable --now auditd
```
---

## 41. 🔐 GRUB2 Password — Recovery When Password Forgotten

### 41.1 Reset Root Password via GRUB

```bash
# When you forget root password:

# Step 1: Reboot the system
# Step 2: At GRUB menu, press 'e' to edit the selected entry
# Step 3: Find the line starting with 'linux' or 'linux16'
# Step 4: At end of that line, remove 'rhgb quiet' and add:
#         rd.break        (RHEL/CentOS)
#         init=/bin/bash  (Ubuntu/Debian)
# Step 5: Press Ctrl+X or F10 to boot
```

**For RHEL/CentOS (rd.break method):**
```bash
# Now in emergency shell — root filesystem mounted read-only at /sysroot
mount -o remount,rw /sysroot    # Remount as read-write
chroot /sysroot                 # Change root to actual system
passwd root                     # Set new root password
touch /.autorelabel             # Relabel SELinux contexts
exit                            # Exit chroot
exit                            # Exit shell → system reboots
```

**For Ubuntu/Debian:**
```bash
# Add to GRUB: rw init=/bin/bash
# After boot:
mount -o remount,rw /           # Already rw
passwd root
exec /sbin/init                 # Or just reboot -f
```

### 41.2 GRUB2 Password Protection

```bash
# Protect GRUB menu from editing:
grub2-setpassword                          # Set GRUB password (RHEL)
# Ubuntu:
grub-mkpasswd-pbkdf2                       # Generate hash

# Add to /etc/grub.d/40_custom:
cat >> /etc/grub.d/40_custom << 'EOF'
set superusers="admin"
password_pbkdf2 admin <HASH FROM ABOVE>
EOF

# Regenerate GRUB config:
grub2-mkconfig -o /boot/grub2/grub.cfg    # RHEL (BIOS)
grub2-mkconfig -o /boot/efi/EFI/centos/grub.cfg  # RHEL (UEFI)
update-grub                                # Ubuntu
```

### 41.3 /etc/rc.local — Legacy Startup Scripts

```bash
# /etc/rc.local runs at end of boot process (all targets reached):
cat /etc/rc.local
```

```bash
#!/bin/bash
# /etc/rc.local — Commands run after system startup

# Mount additional drives:
mount /dev/sdb1 /mnt/data

# Start custom service:
/opt/myapp/start.sh &

# Set kernel parameters:
echo 1 > /proc/sys/net/ipv4/ip_forward

# Custom network rules:
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

exit 0
```

```bash
# Enable rc.local (it's disabled by default on modern systemd):
chmod +x /etc/rc.local
systemctl enable rc-local
systemctl start rc-local
systemctl status rc-local
```


> 💡 **Modern alternative:** Create a proper systemd service unit file instead of using rc.local. rc.local is legacy and may not work on all distributions.


---

## 42. 🔄 Backup & Recovery

### 42.1 rsync — Efficient Backup

```bash
# Basic sync:
rsync -avz /source/ /destination/          # Local sync
rsync -avz /source/ user@remote:/dest/     # Remote backup
rsync -avz user@remote:/source/ /local/    # Remote to local

# Options:
# -a  = archive (recursive + preserve permissions/times/symlinks)
# -v  = verbose
# -z  = compress during transfer
# -P  = show progress + partial files
# --delete = delete extra files in destination (mirror)
# --exclude = exclude pattern
# -n / --dry-run = simulate without making changes
# --bwlimit = bandwidth limit (KB/s)

# Backup with exclusions:
rsync -avz --exclude='*.log' --exclude='/tmp/' /opt/app/ /backup/app/

# Mirror (exact copy — deletes extras in dest):
rsync -avz --delete /opt/app/ /backup/app/

# Show progress:
rsync -avzP /large/dir/ /backup/

# Incremental backup with hardlinks:
rsync -avz --link-dest=/backup/prev/ /source/ /backup/new/
```

### 42.2 tar for Backups

```bash
# Full backup with timestamp:
tar -czf /backup/home_$(date +%Y%m%d).tar.gz /home/

# Backup and verify:
tar -czf /backup/etc.tar.gz /etc/
tar -tzf /backup/etc.tar.gz            # List to verify

# Incremental backup:
tar -czf /backup/inc_$(date +%Y%m%d).tar.gz \
    --newer-mtime="1 week ago" /home/  # Files modified in last week

# Backup to remote via SSH:
tar -czf - /opt/app/ | ssh user@remote "cat > /backup/app_$(date +%Y%m%d).tar.gz"
```

### 42.3 dd — Disk Cloning

```bash
# Clone entire disk:
dd if=/dev/sda of=/dev/sdb bs=4M status=progress  # Clone sda to sdb

# Create disk image:
dd if=/dev/sda of=/backup/sda.img bs=4M status=progress

# Compressed disk image:
dd if=/dev/sda bs=4M | gzip > /backup/sda.img.gz

# Restore image to disk:
gunzip -c /backup/sda.img.gz | dd of=/dev/sda bs=4M status=progress

# Clone just a partition:
dd if=/dev/sda1 of=/backup/sda1.img bs=4M

# Wipe disk (overwrite with zeros):
dd if=/dev/zero of=/dev/sdb bs=4M status=progress
```

### 42.4 Backup Script Example

```bash
#!/bin/bash
# Automated Backup Script

BACKUP_DIR="/backup"
SOURCE_DIRS="/etc /home /opt/app"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30
LOG="/var/log/backup.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"
}

mkdir -p "$BACKUP_DIR"

for dir in $SOURCE_DIRS; do
    name=$(echo "$dir" | tr '/' '_')
    backup_file="$BACKUP_DIR/${name}_${DATE}.tar.gz"
    
    log "Backing up $dir → $backup_file"
    if tar -czf "$backup_file" "$dir" 2>/dev/null; then
        log "SUCCESS: $backup_file ($(du -sh "$backup_file" | cut -f1))"
    else
        log "ERROR: Failed to backup $dir"
    fi
done

# Cleanup old backups:
log "Cleaning up backups older than $RETENTION_DAYS days"
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
log "Backup complete"
```

---

## 43. 🚀 Performance Tuning

### 43.1 CPU Performance

```bash
# CPU governor (affects power/performance balance):
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
# Options: performance, powersave, ondemand, conservative

# Set performance governor:
cpupower frequency-set -g performance
# Or:
echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Disable CPU power management (for high-perf servers):
tuned-adm profile throughput-performance    # RHEL
tuned-adm profile latency-performance
tuned-adm active                            # Current profile
```

### 43.2 Memory Performance

```bash
# Tune virtual memory:
echo 'vm.swappiness=10' >> /etc/sysctl.conf        # Reduce swap usage
echo 'vm.dirty_ratio=15' >> /etc/sysctl.conf       # Dirty pages threshold
echo 'vm.dirty_background_ratio=5' >> /etc/sysctl.conf

# Huge pages (for databases):
echo 'vm.nr_hugepages=1024' >> /etc/sysctl.conf
cat /proc/meminfo | grep Huge                      # Check huge pages

sysctl -p   # Apply all sysctl changes
```

### 43.3 Network Performance

```bash
# TCP tuning (/etc/sysctl.conf):
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.core.netdev_max_backlog = 65535
net.ipv4.tcp_fin_timeout = 15
net.ipv4.tcp_keepalive_time = 300
net.ipv4.tcp_max_tw_buckets = 400000
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216

sysctl -p   # Apply
```

### 43.4 Disk I/O Performance

```bash
# Check I/O scheduler:
cat /sys/block/sda/queue/scheduler
# Options: none, mq-deadline, kyber, bfq

# Set I/O scheduler:
echo mq-deadline > /sys/block/sda/queue/scheduler

# Check disk read speed:
hdparm -t /dev/sda            # Read speed test
hdparm -Tt /dev/sda           # Buffered + cached read

# fio — professional disk benchmark:
fio --name=test --rw=randread --bs=4k --iodepth=32 --runtime=30 --filename=/dev/sda

# noatime mount option (reduce disk writes):
# /dev/sda1 /home ext4 defaults,noatime 0 2
```

### 43.5 ulimit — User Resource Limits

```bash
ulimit -a                      # Show all limits
ulimit -n 65535                # Max open files (temporary)
ulimit -u 65535                # Max user processes
ulimit -c unlimited            # Unlimited core dump size

# Permanent limits (/etc/security/limits.conf):
# Format: <domain> <type> <item> <value>
# * soft nofile 65535
# * hard nofile 65535
# * soft nproc  65535
# * hard nproc  65535
# www-data soft nofile 100000
# www-data hard nofile 100000

cat /proc/sys/fs/file-max      # System-wide max open files
echo 'fs.file-max = 2097152' >> /etc/sysctl.conf
```

---

## 44. 📝 Text Processing — grep, awk, sed

### 44.1 grep — Search Text

```bash
grep "error" /var/log/syslog          # Basic search
grep -i "error" /var/log/syslog       # Case-insensitive
grep -r "password" /etc/              # Recursive search
grep -n "error" file.txt              # Show line numbers
grep -c "error" file.txt              # Count matching lines
grep -v "info" file.log               # Invert — lines NOT matching
grep -w "err" file.log                # Whole word match
grep -l "error" /var/log/*.log        # Only list filenames
grep -L "error" /var/log/*.log        # Files NOT containing match
grep -A 3 "ERROR" file.log            # 3 lines After match
grep -B 3 "ERROR" file.log            # 3 lines Before match
grep -C 3 "ERROR" file.log            # 3 lines Context (before + after)
grep -m 5 "error" file.log            # Only first 5 matches

# Extended regex:
grep -E "error|warning|critical" file.log      # OR
grep -E "^[0-9]{4}-[0-9]{2}" file.log          # Date pattern
egrep "error|warning" file.log                 # Same as grep -E

# Fixed strings (faster for plain text):
grep -F "exact.string" file.txt
fgrep "exact.string" file.txt
```

### 44.2 awk — Pattern Processing

```bash
# Basic usage:
awk '{print $1}' file.txt              # Print 1st column
awk '{print $1, $3}' file.txt          # Print 1st and 3rd columns
awk '{print NR, $0}' file.txt          # Print line number + line
awk 'NR==5' file.txt                   # Print line 5
awk 'NR>=5 && NR<=10' file.txt         # Print lines 5-10

# Field separator:
awk -F: '{print $1}' /etc/passwd       # Use : as separator
awk -F, '{print $2}' data.csv          # CSV column 2
awk -F'\t' '{print $3}' data.tsv       # Tab-separated

# Conditions:
awk '$3 > 1000' /etc/passwd            # UID > 1000
awk '/nginx/ {print}' /var/log/syslog  # Lines matching pattern
awk '$5 == "root"' file.txt            # Exact match on field 5

# Math and calculations:
awk '{sum += $3} END {print "Total:", sum}' data.txt   # Sum column
awk 'END {print NR}' file.txt          # Count lines
awk '{count++} END {print count}' file.txt

# Built-in variables:
# NR = current record (line) number
# NF = number of fields in current record
# FS = field separator (default: whitespace)
# OFS = output field separator
# $0 = entire line, $1 = field 1, $NF = last field

# Formatting:
awk '{printf "%-10s %5.2f\n", $1, $2}' data.txt  # Formatted output

# Practical examples:
awk -F: '$3 >= 1000 {print $1}' /etc/passwd        # List regular users
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head  # Top IPs
df -h | awk 'NR>1 {print $5, $6}' | sort -rn      # Disk usage sorted
```

### 44.3 sed — Stream Editor

```bash
# Basic substitution:
sed 's/old/new/' file.txt              # Replace first occurrence per line
sed 's/old/new/g' file.txt            # Replace ALL occurrences
sed 's/old/new/gi' file.txt           # Global, case-insensitive
sed 's/old/new/2' file.txt            # Replace 2nd occurrence only

# In-place editing:
sed -i 's/old/new/g' file.txt         # Edit file in place
sed -i.bak 's/old/new/g' file.txt     # Edit + create .bak backup

# Delete lines:
sed '/pattern/d' file.txt             # Delete lines matching pattern
sed '5d' file.txt                     # Delete line 5
sed '5,10d' file.txt                  # Delete lines 5-10
sed '/^$/d' file.txt                  # Delete empty lines
sed '/^#/d' file.txt                  # Delete comment lines

# Print specific lines:
sed -n '5p' file.txt                  # Print line 5
sed -n '5,10p' file.txt               # Print lines 5-10
sed -n '/pattern/p' file.txt          # Print matching lines

# Insert/append lines:
sed '5i\New line here' file.txt       # Insert before line 5
sed '5a\New line here' file.txt       # Append after line 5
sed '/pattern/a\New text' file.txt    # Append after matching line

# Practical examples:
sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sed '/^#/d;/^$/d' /etc/nginx/nginx.conf    # Remove comments and blank lines
sed 's/[[:space:]]*$//' file.txt            # Remove trailing whitespace
```

### 44.4 Other Text Tools

```bash
# sort:
sort file.txt                         # Alphabetical sort
sort -r file.txt                      # Reverse sort
sort -n file.txt                      # Numeric sort
sort -k2 file.txt                     # Sort by 2nd column
sort -t: -k3 -n /etc/passwd           # Sort passwd by UID (3rd field)
sort -u file.txt                      # Sort + remove duplicates

# uniq:
uniq file.txt                         # Remove consecutive duplicates
uniq -c file.txt                      # Count occurrences
uniq -d file.txt                      # Only show duplicates
sort file.txt | uniq -c | sort -rn    # Word/line frequency

# cut:
cut -d: -f1 /etc/passwd               # Field 1 with : delimiter
cut -d, -f2,4 data.csv                # Fields 2 and 4
cut -c1-10 file.txt                   # Characters 1-10

# tr:
echo "Hello" | tr 'a-z' 'A-Z'         # Lowercase to uppercase
cat file.txt | tr -d '\r'             # Remove carriage returns
cat file.txt | tr -s ' '             # Squeeze multiple spaces

# wc:
wc -l file.txt                        # Line count
wc -w file.txt                        # Word count
wc -c file.txt                        # Byte count
wc -m file.txt                        # Character count

# xargs:
find . -name "*.log" | xargs rm -f           # Delete found files
cat hosts.txt | xargs -I{} ping -c1 {}       # Ping each host
ls *.txt | xargs -P 4 gzip                   # Parallel gzip (4 jobs)
```

---


## 45. 📜 Shell Scripting

### 45.1 Script Basics

```bash
#!/bin/bash
# Shebang line — tells OS which interpreter to use
# #!/bin/sh   → POSIX sh (more portable)
# #!/bin/bash → bash (more features)
# #!/usr/bin/env bash → finds bash in PATH (portable)

# Make script executable:
chmod +x script.sh
./script.sh              # Run script

# Run without execute permission:
bash script.sh
sh script.sh
source script.sh         # Run in current shell (shares variables)
```

### 45.2 Variables and Input

```bash
#!/bin/bash

# Variables:
name="Alice"
age=30
echo "Name: $name, Age: $age"

# Command substitution:
today=$(date +%Y-%m-%d)
files=$(ls /etc/*.conf | wc -l)
echo "Today: $today, Config files: $files"

# User input:
read -p "Enter your name: " username
read -s -p "Enter password: " pass   # -s = silent (no echo)
echo ""
echo "Hello, $username!"

# Script arguments:
echo "Script: $0"
echo "First arg: $1"
echo "All args: $@"
echo "Arg count: $#"
```

### 45.3 Conditionals

```bash
#!/bin/bash

# if/elif/else:
if [ $age -gt 18 ]; then
    echo "Adult"
elif [ $age -eq 18 ]; then
    echo "Just turned adult"
else
    echo "Minor"
fi

# Test operators:
# -eq  equal           -ne  not equal
# -lt  less than       -le  less or equal
# -gt  greater than    -ge  greater or equal
# -z   empty string    -n   non-empty string
# =    string equal    !=   string not equal
# -f   file exists     -d   directory exists
# -e   path exists     -r   readable
# -w   writable        -x   executable
# -s   file not empty  -L   is symbolic link

# File tests:
if [ -f "/etc/nginx/nginx.conf" ]; then
    echo "Nginx config exists"
fi

if [ -d "/opt/app" ]; then
    echo "App directory exists"
else
    mkdir -p /opt/app
fi

# String tests:
if [ "$name" = "Alice" ]; then
    echo "Hello Alice!"
fi

if [ -z "$name" ]; then
    echo "Name is empty!"
fi

# [[ ]] — bash extended test (supports regex, &&, ||):
if [[ "$name" == Al* ]]; then
    echo "Name starts with Al"
fi

if [[ $age -gt 18 && $name == "Alice" ]]; then
    echo "Adult Alice!"
fi

# Ternary-style:
[ $age -gt 18 ] && echo "Adult" || echo "Minor"
```

### 45.4 Loops

```bash
#!/bin/bash

# for loop:
for i in 1 2 3 4 5; do
    echo "Number: $i"
done

for i in {1..10}; do
    echo "Item $i"
done

for i in $(seq 1 5 100); do   # seq start step end
    echo "Step: $i"
done

for file in /etc/*.conf; do
    echo "Processing: $file"
done

# C-style for loop:
for ((i=0; i<10; i++)); do
    echo "i = $i"
done

# while loop:
count=0
while [ $count -lt 5 ]; do
    echo "Count: $count"
    ((count++))
done

# Read file line by line:
while IFS= read -r line; do
    echo "Line: $line"
done < /etc/hosts

# until loop:
until [ $count -ge 5 ]; do
    echo "Count: $count"
    ((count++))
done
```

### 45.5 Functions

```bash
#!/bin/bash

# Define function:
greet() {
    local name=$1              # local = function-scoped variable
    echo "Hello, $name!"
    return 0
}

# Call function:
greet "Alice"
greet "Bob"

# Function with return value:
get_users() {
    cat /etc/passwd | cut -d: -f1
}
users=$(get_users)

# More complex function:
check_service() {
    local service=$1
    if systemctl is-active --quiet "$service"; then
        echo "✅ $service is running"
        return 0
    else
        echo "❌ $service is not running"
        return 1
    fi
}

check_service nginx
check_service mysql
```

### 45.6 Error Handling

```bash
#!/bin/bash

# Exit on error:
set -e              # Exit script if any command fails
set -u              # Exit on undefined variable
set -o pipefail     # Catch errors in pipes
set -euo pipefail   # All three combined (recommended for scripts)

# Check exit status:
if ! cp /etc/hosts /backup/; then
    echo "ERROR: Failed to backup hosts file" >&2
    exit 1
fi

# Trap errors:
trap 'echo "Error on line $LINENO"' ERR
trap 'cleanup' EXIT        # Run cleanup function on exit

cleanup() {
    rm -f /tmp/tmpfile
    echo "Cleanup done"
}

# Error message and exit:
error_exit() {
    echo "ERROR: $1" >&2
    exit 1
}

[ -f "/etc/nginx/nginx.conf" ] || error_exit "Nginx config not found!"
```

### 45.7 Practical Script Examples

```bash
#!/bin/bash
# System Health Check Script

set -euo pipefail

THRESHOLD_CPU=80
THRESHOLD_MEM=85
THRESHOLD_DISK=90
LOG="/var/log/health-check.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"
}

check_cpu() {
    local cpu_usage
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    if (( $(echo "$cpu_usage > $THRESHOLD_CPU" | bc -l) )); then
        log "WARNING: CPU usage is ${cpu_usage}%"
    else
        log "OK: CPU usage is ${cpu_usage}%"
    fi
}

check_memory() {
    local mem_usage
    mem_usage=$(free | awk '/^Mem/ {printf "%.0f", $3/$2 * 100}')
    if [ "$mem_usage" -gt "$THRESHOLD_MEM" ]; then
        log "WARNING: Memory usage is ${mem_usage}%"
    else
        log "OK: Memory usage is ${mem_usage}%"
    fi
}

check_disk() {
    while IFS= read -r line; do
        local usage mount
        usage=$(echo "$line" | awk '{print $5}' | tr -d '%')
        mount=$(echo "$line" | awk '{print $6}')
        if [ "$usage" -gt "$THRESHOLD_DISK" ]; then
            log "WARNING: Disk $mount is ${usage}% full"
        fi
    done < <(df -h | tail -n +2)
}

check_services() {
    for service in nginx mysql sshd; do
        if systemctl is-active --quiet "$service"; then
            log "OK: $service is running"
        else
            log "CRITICAL: $service is not running!"
        fi
    done
}

log "=== Health Check Started ==="
check_cpu
check_memory
check_disk
check_services
log "=== Health Check Complete ==="
```
---

---

## 46. ⏰ Scheduling Tasks — Cron & At

### 46.1 cron — Recurring Jobs

```bash
# Edit crontab:
crontab -e              # Edit current user's crontab
crontab -l              # List current user's crontab
crontab -r              # Remove current user's crontab
crontab -u alice -e     # Edit alice's crontab (root only)
crontab -u alice -l     # View alice's crontab

# System crontabs:
cat /etc/crontab        # System crontab (includes username field)
ls /etc/cron.d/         # Drop-in cron files
ls /etc/cron.hourly/    # Scripts run hourly
ls /etc/cron.daily/     # Scripts run daily
ls /etc/cron.weekly/    # Scripts run weekly
ls /etc/cron.monthly/   # Scripts run monthly
```

**Crontab Syntax:**

```
* * * * * command
│ │ │ │ │
│ │ │ │ └── Day of week (0-7, 0=Sunday, 7=Sunday)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)

Special characters:
*  = every value
,  = list of values:  1,3,5
-  = range:           1-5
/  = step:            */5 (every 5 units)
```

```bash
# Crontab examples:
# Run every minute:
* * * * * /opt/check.sh

# Run every 5 minutes:
*/5 * * * * /opt/healthcheck.sh

# Run at 2:30 AM daily:
30 2 * * * /opt/backup.sh

# Run at 6 AM Monday-Friday:
0 6 * * 1-5 /opt/morning-report.sh

# Run on 1st of every month at midnight:
0 0 1 * * /opt/monthly-cleanup.sh

# Run every Sunday at 3 AM:
0 3 * * 0 /opt/weekly-backup.sh

# Redirect output:
*/5 * * * * /opt/check.sh >> /var/log/check.log 2>&1

# Special strings (instead of 5 asterisks):
@reboot   /opt/start.sh          # Run once at startup
@daily    /opt/daily.sh          # Same as 0 0 * * *
@weekly   /opt/weekly.sh         # Same as 0 0 * * 0
@monthly  /opt/monthly.sh        # Same as 0 0 1 * *
@hourly   /opt/hourly.sh         # Same as 0 * * * *
```

### 46.2 at — One-Time Scheduled Jobs

```bash
# Schedule a one-time command:
at 10:30                         # Type commands, Ctrl+D to save
at 10:30 tomorrow                # Tomorrow at 10:30
at 2:00 AM July 25               # Specific date
at now + 2 hours                 # Relative time
at now + 30 minutes

# Example:
echo "/opt/backup.sh" | at 2:00 AM
at midnight <<< "/opt/cleanup.sh"

# View/manage at jobs:
atq                              # List pending jobs
at -l                            # Same as atq
atrm 5                           # Remove job #5
at -c 5                          # Show contents of job #5

# Enable/disable at for users:
cat /etc/at.allow                # Users allowed to use at
cat /etc/at.deny                 # Users denied at access
```

### 46.3 systemd Timers (Modern Alternative)

```bash
# List timers:
systemctl list-timers            # All active timers
systemctl list-timers --all      # Including inactive

# Example timer unit (/etc/systemd/system/backup.timer):
# [Unit]
# Description=Daily Backup Timer
#
# [Timer]
# OnCalendar=daily
# Persistent=true
#
# [Install]
# WantedBy=timers.target

systemctl enable --now backup.timer
```
---

## 47. ⚡ Quick Reference Cheat Sheet

### 📁 Files & Directories

| Command | Description |
|---------|-------------|
| `ls -lah` | List all files with details + human sizes |
| `find / -name "*.conf"` | Find files by name |
| `cp -r src/ dest/` | Copy directory recursively |
| `rm -rf dir/` | Force delete directory |
| `tar -czf a.tar.gz dir/` | Create compressed archive |
| `tar -xzf a.tar.gz` | Extract archive |
| `ln -s target link` | Create symbolic link |

### 🔐 Permissions

| Command | Description |
|---------|-------------|
| `chmod 755 file` | rwxr-xr-x |
| `chmod 644 file` | rw-r--r-- |
| `chmod +x script.sh` | Make executable |
| `chown user:group file` | Change owner and group |
| `chown -R user /dir` | Recursive ownership change |

### 👤 Users

| Command | Description |
|---------|-------------|
| `useradd -m -s /bin/bash alice` | Create user with home |
| `passwd alice` | Set password |
| `usermod -aG sudo alice` | Add to sudo group |
| `userdel -r alice` | Delete user + home |
| `id alice` | Show user info |

### ⚙️ Processes

| Command | Description |
|---------|-------------|
| `ps aux` | All running processes |
| `top` / `htop` | Live process monitor |
| `kill -9 <PID>` | Force kill |
| `killall nginx` | Kill by name |
| `jobs` | List background jobs |
| `nohup cmd &` | Run immune to hangup |

### 💾 Disk

| Command | Description |
|---------|-------------|
| `df -h` | Disk space usage |
| `du -sh dir/` | Directory size |
| `lsblk` | List block devices |
| `mount /dev/sdb1 /mnt` | Mount device |
| `fdisk -l` | List partitions |

### 🌐 Networking

| Command | Description |
|---------|-------------|
| `ip addr` | Show IP addresses |
| `ip route` | Show routing table |
| `ss -tuln` | All listening ports |
| `ping -c4 host` | Test connectivity |
| `dig google.com` | DNS lookup |
| `curl -I http://host` | HTTP headers |

### 📦 Packages

| APT (Debian) | YUM/DNF (RHEL) |
|-------------|----------------|
| `apt update` | `dnf update` |
| `apt install pkg` | `dnf install pkg` |
| `apt remove pkg` | `dnf remove pkg` |
| `apt search pkg` | `dnf search pkg` |
| `dpkg -l` | `rpm -qa` |

### 🔧 Services

| Command | Description |
|---------|-------------|
| `systemctl start nginx` | Start service |
| `systemctl stop nginx` | Stop service |
| `systemctl restart nginx` | Restart |
| `systemctl enable nginx` | Start at boot |
| `systemctl status nginx` | Check status |
| `journalctl -u nginx -f` | Follow logs |

### 📝 Text Processing

| Command | Description |
|---------|-------------|
| `grep -r "text" /dir` | Recursive search |
| `awk '{print $2}' f` | Print column 2 |
| `sed 's/old/new/g' f` | Replace text |
| `tail -f /var/log/syslog` | Follow log file |
| `sort \| uniq -c` | Count occurrences |
| `wc -l file` | Count lines |

### 🔒 Security

| Command | Description |
|---------|-------------|
| `ufw allow 22` | Allow SSH (Ubuntu) |
| `firewall-cmd --add-service=http --permanent` | Allow HTTP (RHEL) |
| `ssh-keygen -t ed25519` | Generate SSH key |
| `ssh-copy-id user@host` | Copy key to server |
| `fail2ban-client status sshd` | Check SSH jail |
| `lynis audit system` | Security audit |

### 🏥 Quick Health Check

```bash
# One-liner system health summary:
echo "=== CPU ===" && top -bn1 | grep "Cpu(s)"
echo "=== Memory ===" && free -h
echo "=== Disk ===" && df -h | grep -v tmpfs
echo "=== Load ===" && uptime
echo "=== Failed Services ===" && systemctl --failed
echo "=== Last Logins ===" && last | head -5
```

---

> 💡 **Study Tip:** Practice these commands on a live Linux system or VM. Theory without hands-on practice won't stick!

> 🌟 **Golden Rule:** Always test changes on non-production systems first. For critical changes, take snapshots/backups before starting.

> 🔑 **Admin Mindset:** Document everything you do. Future-you (and your teammates) will thank you.

---

*📘 Made with ❤️ for Linux learners and system administrators — from zero to production-ready administration.*


