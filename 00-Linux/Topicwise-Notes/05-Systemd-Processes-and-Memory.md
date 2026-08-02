# Systemd, Processes, Memory, and Logs

> Extracted from [00-Linux/01-Introduction.md](../01-Introduction.md)
>
> Covers source sections 16-19 from the original Linux introduction note.

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
