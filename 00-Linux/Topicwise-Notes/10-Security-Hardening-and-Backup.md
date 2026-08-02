# 🔒 Security Hardening, Backup, Performance, and Scripting

Covers hardening, backup, performance tuning, and shell scripting in Linux.

## 🔒 40. Linux Security & Hardening

Security hardening is the process of reducing risk by tightening access, monitoring activity, and limiting attack surfaces. These practices help protect Linux systems from misconfiguration, abuse, and common threats.

### 🔹 40.1 Security Audit Tools

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

### 🔹 40.2 SELinux (RHEL/CentOS)

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

### 🔹 40.3 AppArmor (Ubuntu/Debian)

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

### 🔹 40.4 System Hardening Checklist

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

## 🔐 41. GRUB2 Password — Recovery When Password Forgotten

### 🔹 41.1 Reset Root Password via GRUB

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

### 🔹 41.2 GRUB2 Password Protection

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

### 🔹 41.3 /etc/rc.local — Legacy Startup Scripts

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

## 🔄 42. Backup & Recovery

### 🔹 42.1 rsync — Efficient Backup

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

### 🔹 42.2 tar for Backups

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

### 🔹 42.3 dd — Disk Cloning

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

### 🔹 42.4 Backup Script Example

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

## 🚀 43. Performance Tuning

### 🔹 43.1 CPU Performance

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

### 🔹 43.2 Memory Performance

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

### 🔹 43.3 Network Performance

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

### 🔹 43.4 Disk I/O Performance

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

### 🔹 43.5 ulimit — User Resource Limits

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

## 📝 44. Text Processing — grep, awk, sed

### 🔹 44.1 grep — Search Text

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

### 🔹 44.2 awk — Pattern Processing

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

### 🔹 44.3 sed — Stream Editor

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

### 🔹 44.4 Other Text Tools

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

## 📜 45. Shell Scripting

### 🔹 45.1 Script Basics

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

### 🔹 45.2 Variables and Input

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

### 🔹 45.3 Conditionals

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

### 🔹 45.4 Loops

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

### 🔹 45.5 Functions

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

### 🔹 45.6 Error Handling

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

### 🔹 45.7 Practical Script Examples

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

## 📌 ⏰ 46. Scheduling Tasks — Cron & At

### 🔹 46.1 cron — Recurring Jobs

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

### 🔹 46.2 at — One-Time Scheduled Jobs

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

### 🔹 46.3 systemd Timers (Modern Alternative)

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

## ⚡ 47. Quick Reference Cheat Sheet

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
