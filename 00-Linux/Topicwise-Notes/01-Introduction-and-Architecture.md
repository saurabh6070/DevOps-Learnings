# 🐧 Introduction, Architecture, and Filesystem

Covers the essential ideas behind Linux, its architecture, and the filesystem hierarchy.

## 🐧 1. Introduction to Linux

Linux is the foundation of modern infrastructure because it powers servers, cloud platforms, containers, and many developer workstations. Understanding the basic idea of Linux is important before exploring commands, configuration files, or system administration tasks.

### 🔹 1.1 What is Linux?

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

#### ✨ An Operating System (OS):
> Manages CPU, memory, disk, and devices.
> Runs applications.
> Provides security and user management.
> Handles networking.

#### ✨ Examples of Operating Systems:
> Microsoft Windows
> macOS
> linux


### 🔹 1.2 Why Linux?

| Feature | Description |
|---------|-------------|
| 🆓 **Free & Open Source** | No licensing cost; source code freely available |
| 🔐 **Secure** | Strong permission model; less malware than Windows |
| 🏋️ **Stable & Reliable** | Servers run for years without reboots |
| ⚙️ **Customizable** | Modify kernel and every component |
| 📈 **Scalable** | Powers tiny Raspberry Pi to world's fastest supercomputers |
| 🌐 **Dominant in Cloud** | 90%+ of cloud workloads run on Linux |
| 🐳 **Container Native** | Docker, Kubernetes all built on Linux kernel features |

### 🔹 1.3 Popular Linux Distributions

| Family | Distributions | Package Manager |
|--------|--------------|----------------|
| **Debian** | Ubuntu, Debian, Kali, Linux Mint | `apt` / `dpkg` |
| **Red Hat** | RHEL, CentOS, Rocky Linux, Fedora, AlmaLinux | `yum` / `dnf` / `rpm` |
| **SUSE** | openSUSE, SLES | `zypper` / `rpm` |
| **Arch** | Arch Linux, Manjaro | `pacman` |
| **Independent** | Alpine, Gentoo, Slackware | varies |

> 💡 **Ubuntu** is most popular for beginners and cloud. **RHEL/CentOS** dominate enterprise environments.

### 🔹 1.4 Linux Kernel Version

```bash
# Check kernel version:
uname -r           # e.g., 6.1.0-21-amd64
uname -a           # Full system info
cat /proc/version  # Detailed kernel info
```

---

## 🖥️ 2. Linux Architecture

A Linux system is organized in layers, from hardware up to user applications. Knowing this structure helps explain why commands, services, and kernel features behave the way they do.

<img width="1408" height="768" alt="Gemini_Generated_Image_6nu6ez6nu6ez6nu6" src="https://github.com/user-attachments/assets/cb065270-3371-47b7-83c2-512e2d6c57ab" />



### 🔹 2.1 Key Layers

| Layer | Description |
|-------|-------------|
| **Hardware** | Physical components — CPU, RAM, disk, network card |
| **Kernel** | Core OS — manages hardware, processes, memory, filesystem |
| **System Libraries** | Standard functions (glibc) that programs call |
| **Shell** | Command interpreter — bash, zsh, sh, ksh, fish |
| **Applications** | User programs — nginx, vim, Python, MySQL |

### 🔹 2.2 Types of Shells

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

## 📂 3. Linux File System Hierarchy

The Linux filesystem is a single tree rooted at /, which makes paths and file organization predictable. Learning this hierarchy is essential for locating configuration files, logs, user data, and system resources.

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

### 🔹 3.1 Key Directories Explained

| Directory | Purpose | Examples |
|-----------|---------|---------|
| `/etc` | ALL system config files | `/etc/passwd`, `/etc/nginx/`, `/etc/ssh/` |
| `/var/log` | System and application logs | `/var/log/syslog`, `/var/log/nginx/` |
| `/proc` | Live kernel/process data | `/proc/cpuinfo`, `/proc/meminfo` |
| `/dev` | Device files | `/dev/sda` (disk), `/dev/null`, `/dev/tty` |
| `/home` | User personal directories | `/home/username/` |
| `/tmp` | Temp files — world-writable | Cleared on reboot |
| `/usr/local/bin` | User-installed binaries | Custom scripts, compiled software |

### 🔹 3.2 Absolute vs Relative Paths

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
