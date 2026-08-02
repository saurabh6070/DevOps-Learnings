# ⌨️ Essential Commands and File Management

Covers the daily shell commands and file-management skills needed to work confidently in Linux.

## 4. ⌨️ Essential Linux Commands

Before managing files or systems, a Linux learner needs a reliable way to navigate the environment and inspect what is available. These commands form the everyday toolkit for working efficiently in the shell.

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
