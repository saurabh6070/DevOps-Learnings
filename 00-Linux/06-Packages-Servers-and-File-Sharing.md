# 📦 Package Management, Servers, and File Sharing

## 1. Package Management Fundamentals

Linux distributions use package managers to install, upgrade, remove, and verify software. The package manager also handles dependencies and repositories.

### APT (Debian/Ubuntu)

```bash
apt update
apt upgrade
apt install nginx
apt remove nginx
apt purge nginx
apt search nginx
apt show nginx
apt list --installed
```

### DNF/YUM (RHEL/CentOS/Rocky)

```bash
dnf update
dnf install nginx
dnf remove nginx
dnf search nginx
dnf info nginx
dnf repolist
dnf history
```

### RPM

```bash
rpm -ivh package.rpm
rpm -Uvh package.rpm
rpm -e nginx
rpm -qa
rpm -qi nginx
rpm -ql nginx
rpm -qf /etc/nginx/nginx.conf
```

### Repository management

```bash
cat /etc/apt/sources.list
ls /etc/apt/sources.list.d/
ls /etc/yum.repos.d/
dnf config-manager --add-repo URL
```

## 2. Local Yum Repository Setup

A local repository can be used to serve RPM packages from a local directory or ISO mount.

```bash
yum install httpd createrepo -y
mkdir -p /var/www/html/repos/centos7/
mount /dev/cdrom /mnt/
cp -r /mnt/Packages/* /var/www/html/repos/centos7/
createrepo /var/www/html/repos/centos7/
systemctl enable --now httpd
```

Client-side config:

```bash
cat > /etc/yum.repos.d/local.repo << EOF
[local-base]
name=Local Repo
baseurl=http://192.168.1.10/repos/centos7/
enabled=1
gpgcheck=0
EOF
```

## 3. Web Server: Apache HTTPD

Apache is one of the most common web servers on Linux.

### Install Apache

```bash
apt install apache2 -y
systemctl enable --now apache2
```

For RHEL/CentOS:

```bash
yum install httpd -y
systemctl enable --now httpd
```

### Important paths

- `/etc/apache2/apache2.conf` (Ubuntu/Debian)
- `/etc/httpd/conf/httpd.conf` (RHEL/CentOS)
- `/var/www/html` by default for web content

### Test it

```bash
curl http://localhost
```

## 4. FTP and Repository Concepts

FTP and package repositories are historically important in Linux administration.

### vsftpd example

```bash
yum install vsftpd -y
systemctl enable --now vsftpd
```

A repository over FTP can be used for RPM package distribution when configured properly.

## 5. NFS and Samba File Sharing

### NFS

NFS allows Linux systems to share directories over the network.

```bash
apt install nfs-kernel-server
cat /etc/exports
exportfs -a
exportfs -r
systemctl enable --now nfs-kernel-server
```

Example export:

```text
/opt/shared 192.168.1.0/24(rw,sync,no_subtree_check)
```

Client mount:

```bash
mount -t nfs 192.168.1.10:/opt/shared /mnt/nfs
```

### Samba

Samba enables Linux file sharing with Windows clients using SMB/CIFS.

```bash
apt install samba samba-common-bin
systemctl enable --now smbd
```

Example share test:

```bash
smbclient -L //192.168.1.100 -U alice
```

## 6. DNS and DHCP Servers

### BIND DNS

```bash
apt install bind9 bind9utils -y
systemctl enable --now bind9
```

### DHCP server

```bash
apt install isc-dhcp-server -y
systemctl enable --now isc-dhcp-server
```

These services are commonly used in internal networks to provide name resolution and IP allocation.

## 7. Practical Labs

- Install a package with `apt` or `dnf` and verify it is present.
- Create a local repository and configure a client to use it.
- Deploy a simple Apache web server and verify it through `curl`.
- Create a basic NFS share and mount it from another machine.
- Configure a Samba share and connect to it from a Linux client.
