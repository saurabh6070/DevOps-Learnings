# 🐧 Linux Fundamentals

## 1. What is Linux?

Linux is a Unix-like operating system built around the Linux kernel. It is one of the most important platforms in modern IT because it powers servers, desktops, cloud systems, containers, and embedded devices.

Strictly speaking:

- Linux = kernel
- GNU/Linux = kernel + GNU userland tools + shell + applications

### Why Linux is important

- Free and open source
- Secure and stable
- Easy to automate
- Extremely scalable
- Widely used in DevOps, cloud, and enterprise environments

### Popular distributions

| Family | Examples | Package manager |
|---|---|---|
| Debian/Ubuntu | Ubuntu, Debian, Kali, Mint | apt / dpkg |
| Red Hat family | RHEL, Rocky, AlmaLinux, CentOS, Fedora | yum / dnf / rpm |
| SUSE | openSUSE, SLES | zypper |
| Arch | Arch Linux, Manjaro | pacman |

> Ubuntu is beginner-friendly, while RHEL-based distributions are common in enterprise and server environments.

## 2. Linux Architecture

Linux is organized in layers:

```text
User Space
  ├── Applications (nginx, vim, python)
  ├── Shell (bash, zsh)
  └── Libraries

Kernel Space
  ├── Process Management
  ├── Memory Management
  ├── File System Management
  └── Device/Network Management

Hardware
  ├── CPU
  ├── RAM
  ├── Disk
  └── NIC / peripherals
```

### Key layers

| Layer | Purpose |
|---|---|
| Hardware | Physical devices and resources |
| Kernel | Core OS that controls hardware and processes |
| Libraries | Shared functions used by applications |
| Shell | Command interpreter used by users |
| Applications | Programs such as editors, web servers, and databases |

### Common shells

- bash: default shell on most Linux systems
- sh: minimal POSIX shell
- zsh: advanced shell with many features
- fish: user-friendly shell

## 3. Linux Filesystem Hierarchy

Linux uses a single root filesystem, signified by `/`. Everything is organized under that root.

```text
/
├── bin/      Essential user commands
├── boot/     Bootloader and kernel files
├── dev/      Device files
├── etc/      System configuration files
├── home/     User home folders
├── lib/      Shared libraries
├── media/    Removable media mount points
├── mnt/      Temporary mount points
├── opt/      Optional software
├── proc/     Kernel/process information (virtual FS)
├── root/     Root user's home directory
├── run/      Runtime data
├── srv/      Service data
├── sys/      Kernel/device virtual info
├── tmp/      Temporary files
├── usr/      User applications and libraries
└── var/      Logs, spool, caches, variable data
```

### Important directories

| Directory | Use |
|---|---|
| `/etc` | System configuration |
| `/home` | User personal directories |
| `/var/log` | System and service logs |
| `/tmp` | Temporary files |
| `/usr` | Installed programs and libraries |
| `/proc` | Live kernel and process data |
| `/dev` | Device files |
| `/boot` | Boot-related files |

## 4. Essential Linux Commands

### Navigation and listing

```bash
pwd
ls
ls -l
ls -la
cd /path/to/dir
cd ~
cd ..
```

### Help and file location

```bash
man ls
ls --help
which ls
whereis ls
type ls
```

### System information

```bash
uname -a
uname -r
cat /etc/os-release
hostnamectl
uptime
w
```

### Date and time

```bash
date
date +"%Y-%m-%d %H:%M:%S"
timedatectl
timedatectl set-timezone Asia/Kolkata
```

## 5. Practical Labs

- Check the OS version and kernel version of your machine.
- Explore `/etc`, `/var`, `/home`, `/proc`, and `/dev`.
- Compare `ls`, `ls -l`, and `ls -la`.
- Practice `cd`, `pwd`, `uname`, and `hostnamectl`.
- Read `/etc/os-release` and `/etc/hostname`.
