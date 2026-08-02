# 👤 Users, Groups, and Basic Security

Covers user and group administration, password policies, and essential Linux security concepts.

## 11. 👤 User & Group Management

Linux security begins with controlled access to the system. Users and groups define who can log in, what they can access, and how privileges are separated.

### 11. 🔹 1 User Accounts

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

### 11. 🔹 2 Creating and Managing Users

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

### 11. 🔹 3 Password Policy — /etc/shadow

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

### 11. 🔹 4 Group Management

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

### 11. 🔹 5 sudo — Privilege Escalation

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

### 11. 🔹 6 Key User Files

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

### 12. 🔹 1 UID — User ID

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

### 12. 🔹 2 GID — Group ID

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

### 12. 🔹 3 root User Special Properties

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

### 12. 🔹 4 Convert Root User ↔ Normal User

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

### 13. 🔹 1 /etc/passwd — User Account Database

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

### 13. 🔹 2 /etc/shadow — Encrypted Password Storage

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

### 14. 🔹 1 Traditional Runlevels (/etc/inittab)

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

### 14. 🔹 2 Switching Between GUI and CLI (Modern systemd)

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

### 14. 🔹 3 Runlevel-to-Target Mapping

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
