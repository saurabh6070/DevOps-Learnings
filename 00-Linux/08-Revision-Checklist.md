# 🧠 Linux Revision Checklist

Use this checklist when revising the Linux topics from the original long note.

## Core concepts

- [ ] Understand what Linux is and why it is widely used in servers and cloud environments
- [ ] Know the difference between the kernel, shell, libraries, and user applications
- [ ] Recognize the purpose of the main directories in the Linux filesystem
- [ ] Be able to navigate the filesystem with `pwd`, `ls`, `cd`, and `find`
- [ ] Understand absolute vs relative paths and the role of `.` and `..`

## File and command skills

- [ ] Create, edit, move, copy, and delete files and directories
- [ ] Use `cat`, `head`, `tail`, `less`, `grep`, `awk`, and `sed`
- [ ] Work with compression tools such as `gzip`, `zip`, and `tar`
- [ ] Create hard links and symbolic links and explain the difference
- [ ] Edit files with `vim` and understand basic modes and commands

## Identity, permissions, and shell

- [ ] Understand UID, GID, root, regular users, and groups
- [ ] Create and manage users and groups
- [ ] Use `chmod`, `chown`, and `chgrp` confidently
- [ ] Explain SUID, SGID, and sticky bit
- [ ] Understand ACLs and `umask`
- [ ] Work with shell variables, aliases, and startup files such as `.bashrc`

## Processes and services

- [ ] View processes with `ps`, `top`, and `htop`
- [ ] Send signals with `kill` and `killall`
- [ ] Start, stop, restart, enable, and disable services with `systemctl`
- [ ] Read logs with `journalctl`, `tail`, and `dmesg`
- [ ] Understand memory and CPU monitoring basics

## Storage and filesystems

- [ ] Check disk usage with `df` and `du`
- [ ] Understand mounting and `/etc/fstab`
- [ ] Describe inodes and why they matter
- [ ] Explain the purpose of LVM and RAID
- [ ] Know how to create and mount filesystems in a lab environment

## Networking and remote access

- [ ] Work with `ip`, `ip route`, `ping`, `traceroute`, and `ss`
- [ ] Understand DNS resolution through `/etc/hosts` and `/etc/resolv.conf`
- [ ] Configure or inspect networking through NetworkManager, Netplan, or ifcfg files
- [ ] Use SSH, SCP, rsync, and configure passwordless authentication
- [ ] Understand basic firewall concepts with `firewalld`, `ufw`, and `iptables`

## Administration and automation

- [ ] Install and remove software with `apt`, `dnf`, `yum`, and `rpm`
- [ ] Explain how Apache, NFS, Samba, DNS, and DHCP work in Linux
- [ ] Write simple shell scripts and use `set -euo pipefail`
- [ ] Schedule tasks with `cron` and `at`
- [ ] Practice backup and recovery using `rsync`, `tar`, and `dd`
- [ ] Review security hardening steps and basic SELinux/AppArmor concepts
