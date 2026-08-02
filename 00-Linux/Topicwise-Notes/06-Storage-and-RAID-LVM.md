# Storage, Filesystems, Inodes, LVM, and RAID

> Extracted from [00-Linux/01-Introduction.md](../01-Introduction.md)
>
> Covers source sections 20-24 from the original Linux introduction note.

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
