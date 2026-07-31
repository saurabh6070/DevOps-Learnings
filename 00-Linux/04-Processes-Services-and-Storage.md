# ⚙️ Processes, Services, and Storage

## 1. Process Management

A process is a running instance of a program. Linux provides several tools to inspect, manage, and control processes.

### View processes

```bash
ps
ps aux
ps -ef
ps -u alice
top
htop
```

### Process states

| State | Meaning |
|---|---|
| R | Running |
| S | Sleeping |
| D | Waiting for I/O |
| T | Stopped |
| Z | Zombie |

### Signals and process control

```bash
kill 1234
kill -15 1234          # graceful termination
kill -9 1234           # force kill
killall nginx
pkill -f python
```

### Background and foreground jobs

```bash
sleep 100 &
jobs
fg %1
bg %1
nohup ./script.sh > output.log 2>&1 &
```

### Priority management

```bash
nice -n 10 ./heavy-script.sh
renice -n 5 -p 1234
```

Nice values range from `-20` (high priority) to `19` (low priority). Only root can raise priority with a negative nice value.

## 2. Systemd and Service Management

Modern Linux systems use `systemd` to manage services. This replaces older runlevels.

### Service commands

```bash
systemctl status nginx
systemctl start nginx
systemctl stop nginx
systemctl restart nginx
systemctl reload nginx
systemctl enable nginx
systemctl disable nginx
systemctl mask nginx
systemctl unmask nginx
```

### systemd targets

| Previous runlevel | systemd target |
|---|---|
| 0 | `poweroff.target` |
| 1 | `rescue.target` |
| 3 | `multi-user.target` |
| 5 | `graphical.target` |
| 6 | `reboot.target` |

### Example unit file

```ini
[Unit]
Description=My App
After=network.target

[Service]
ExecStart=/opt/myapp/start.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

### journalctl

```bash
journalctl -u nginx
journalctl -f
journalctl -b
journalctl --since "1 hour ago"
journalctl -p err
```

## 3. Memory, CPU, and Logs

### Memory and CPU

```bash
free -h
cat /proc/meminfo
lscpu
nproc
cat /proc/cpuinfo
```

### Monitoring commands

```bash
top
htop
vmstat 1 5
mpstat -P ALL 1
```

### Important log locations

| File | Purpose |
|---|---|
| `/var/log/syslog` | General system logs |
| `/var/log/auth.log` | Authentication events |
| `/var/log/secure` | Red Hat security/auth logs |
| `/var/log/kern.log` | Kernel messages |
| `/var/log/cron` | Cron job logs |
| `/var/log/nginx/` | Web server logs |

```bash
tail -f /var/log/syslog
dmesg
dmesg | grep -i error
```

## 4. Disk and Filesystem Management

### Check disk usage

```bash
df -h
du -sh /var/log
lsblk
blkid
```

### Create and check filesystems

```bash
mkfs.ext4 /dev/sdb1
mkfs.xfs /dev/sdb2
fsck /dev/sdb1
```

### Mount and unmount

```bash
mount /dev/sdb1 /mnt/data
umount /mnt/data
```

### Persistent mounts with fstab

```bash
cat /etc/fstab
mount -a
```

A mount entry in `/etc/fstab` makes storage available automatically after boot. The format is:

```text
<device> <mountpoint> <filesystem> <options> <dump> <pass>
```

### Swap

```bash
swapon --show
fallocate -l 2G /swapfile
mkswap /swapfile
swapon /swapfile
```

## 5. Inodes and Filesystem Internals

An inode stores metadata about a file such as ownership, permissions, size, timestamps, and pointers to the data blocks.

```bash
ls -li file.txt
stat file.txt
df -i
```

- Inodes do not store the filename itself.
- The filename is stored in the directory entry.
- Filesystems have a limited number of inodes.

## 6. LVM and RAID

### LVM concepts

- PV = Physical Volume
- VG = Volume Group
- LV = Logical Volume

```bash
pvcreate /dev/sdb
vgcreate datavg /dev/sdb
lvcreate -L 10G -n datalv datavg
mkfs.ext4 /dev/datavg/datalv
mount /dev/datavg/datalv /mnt/data
```

### RAID-5

RAID-5 provides fault tolerance with parity and requires at least three disks.

```bash
mdadm --create /dev/md0 --level=5 --raid-devices=3 /dev/sdb1 /dev/sdc1 /dev/sdd1
cat /proc/mdstat
```

## 7. Practical Labs

- Run `ps`, `top`, and `htop` and identify which processes are consuming resources.
- Start and stop a service with `systemctl` and review the resulting logs.
- Mount a test partition and make it persistent through `/etc/fstab`.
- Inspect inode usage and compare it with disk usage.
- Create a simple LVM layout or a RAID-5 array in a lab environment.
