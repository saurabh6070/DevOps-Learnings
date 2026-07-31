# 🔒 Security, Automation, and Backup

## 1. Linux Security Foundations

Linux security is built on multiple layers: permissions, authentication, service hardening, firewalls, auditing, and monitoring.

### Important security tools

```bash
lynis audit system
chkrootkit
rkhunter --check
auditctl -l
auditctl -a always,exit -F path=/etc/passwd -F perm=wa
```

### SELinux and AppArmor

```bash
getenforce
sestatus
setenforce 0
setenforce 1
aa-status
```

SELinux and AppArmor are mandatory access control systems. They restrict what processes can do, even if the user has broad permissions.

## 2. Hardening Checklist

A hardened Linux system should:

- keep the OS updated
- disable unnecessary services
- secure SSH configuration
- configure a firewall
- enforce strong file permissions
- review logs and audit events
- limit root access and use sudo carefully

### Example hardening commands

```bash
apt update && apt upgrade -y
systemctl disable bluetooth
systemctl disable cups
chmod 644 /etc/passwd
chmod 640 /etc/shadow
chmod 644 /etc/group
```

## 3. Shell Scripting

Shell scripts are used to automate routine system tasks.

```bash
#!/bin/bash
set -euo pipefail
for i in 1 2 3; do
    echo "Number: $i"
done
```

### Example: basic system health check

```bash
#!/bin/bash
set -euo pipefail

df -h | head
free -h
ps aux --sort=-%cpu | head -10
```

### Error handling in scripts

```bash
#!/bin/bash
set -euo pipefail

if [ ! -f /etc/hosts ]; then
    echo "hosts file missing" >&2
    exit 1
fi
```

## 4. Scheduling Tasks

### Cron

Cron is used for recurring tasks.

```bash
crontab -e
crontab -l
crontab -r
```

Example cron expression:

```text
*/5 * * * * /opt/check.sh
30 2 * * * /opt/backup.sh
```

### at

`at` schedules one-time jobs.

```bash
at now + 5 minutes
at 10:30 tomorrow
```

## 5. GRUB Recovery and Legacy Startup Scripts

If the root password is lost, GRUB can be used to enter recovery mode.

### GRUB recovery concept

1. Reboot and press `e` at the GRUB menu.
2. Edit the kernel line.
3. Add `rd.break` or `init=/bin/bash` depending on the distro.
4. Remount the filesystem and reset the password.

### Legacy rc.local

```bash
chmod +x /etc/rc.local
systemctl enable rc-local
```

Modern systems prefer a proper `systemd` service unit over `rc.local`.

## 6. Backup and Recovery

Backups are essential for system recovery and business continuity.

### rsync

```bash
rsync -avz /source/ /backup/
rsync -avz --delete /source/ /backup/
```

### tar

```bash
tar -czf backup.tar.gz /etc /home
```

### dd

```bash
dd if=/dev/sda of=/backup/sda.img bs=4M status=progress
```

### Backup script example

```bash
#!/bin/bash
BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/etc_$DATE.tar.gz" /etc
```

## 7. Performance Tuning and Resource Limits

```bash
sysctl -a
sysctl -w net.ipv4.ip_forward=1
ulimit -a
ulimit -n 65535
```

`sysctl` configures kernel parameters, while `ulimit` controls shell and process limits.

## 8. Practical Labs

- Create a shell script that checks disk usage and prints warnings.
- Schedule a backup with cron and verify that it runs.
- Review the security posture of a Linux VM using `lynis` or a manual checklist.
- Practice recovery steps for a failed service using `systemctl` and `journalctl`.
- Create a backup of `/etc` and restore it into a test directory.
