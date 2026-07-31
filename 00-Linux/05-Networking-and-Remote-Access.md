# 🌐 Networking, SSH, and Remote Access

## 1. Networking Basics

Networking in Linux is about how systems communicate with each other over physical and logical links. A Linux machine can be part of a LAN, a WAN, or the Internet.

### LAN vs WAN

| Type | Description |
|---|---|
| LAN | Local Area Network, usually in one building or site |
| WAN | Wide Area Network, connecting systems over larger distances |
| MAN | Metropolitan Area Network |
| VLAN | Logical segmentation of a local network |

### OSI model

The OSI model is a conceptual model used to describe how network communication works.

```text
7 Application
6 Presentation
5 Session
4 Transport
3 Network
2 Data Link
1 Physical
```

Common examples:

- Layer 7: HTTP, DNS, SSH
- Layer 4: TCP, UDP
- Layer 3: IP, ICMP
- Layer 2: Ethernet, ARP
- Layer 1: Cables, fiber, wireless signals

## 2. Network Interfaces and Routing

```bash
ip addr
ip link show
ifconfig
ip route
route -n
```

### Configure interface IP temporarily

```bash
ip addr add 192.168.1.100/24 dev eth0
ip addr del 192.168.1.100/24 dev eth0
ip link set eth0 up
ip link set eth0 down
```

### Add a default gateway

```bash
ip route add default via 192.168.1.1
```

## 3. DNS, Hosts, and Name Resolution

Linux resolves hostnames using `/etc/hosts`, DNS servers, and NSS configuration.

```bash
cat /etc/hosts
cat /etc/resolv.conf
cat /etc/nsswitch.conf | grep hosts
```

### DNS tools

```bash
nslookup google.com
dig google.com
dig MX gmail.com
host google.com
```

### Example `/etc/hosts`

```text
127.0.0.1 localhost
192.168.1.10 server1.example.com server1
```

## 4. Network Configuration Files

### NetworkManager

```bash
nmcli general status
nmcli device status
nmcli con show
nmcli con up eth0
nmcli con mod eth0 ipv4.method manual
```

### Netplan (Ubuntu)

```bash
cat /etc/netplan/*.yaml
netplan apply
```

### ifcfg files (RHEL/CentOS)

```bash
cat /etc/sysconfig/network-scripts/ifcfg-eth0
```

### `/etc/network/interfaces` (older Debian/Ubuntu)

```ini
auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8 8.8.4.4
```

## 5. Network Diagnostics

```bash
ping google.com
ping -c 4 google.com
traceroute google.com
tracepath google.com
ss -tuln
ss -tulnp
netstat -tuln
curl -I http://example.com
```

These commands help verify connectivity, routing, listening ports, and web server reachability.

## 6. SSH and Remote Access

SSH is the standard secure way to access a Linux machine remotely. It also supports secure file transfer.

### Basic SSH usage

```bash
ssh user@hostname
ssh -p 2222 user@hostname
ssh user@192.168.1.100
```

### SSH keys

```bash
ssh-keygen -t ed25519 -C "alice@example.com"
ssh-copy-id user@hostname
```

### SCP and rsync

```bash
scp file.txt user@host:/tmp/
scp -r dir/ user@host:/tmp/
rsync -avz /local/ user@host:/remote/
```

### SFTP

```bash
sftp user@host
```

### SSH server config

```bash
sudo vim /etc/ssh/sshd_config
sudo sshd -t
sudo systemctl restart sshd
```

### Important sshd settings

- `Port 22` or a custom non-standard port
- `PermitRootLogin no`
- `PasswordAuthentication no`
- `PubkeyAuthentication yes`

## 7. Passwordless SSH

Passwordless SSH improves automation by allowing key-based authentication.

```bash
cat ~/.ssh/id_ed25519.pub | ssh user@host "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

### Important permissions

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/id_ed25519
```

## 8. Firewall and NAT

### firewalld

```bash
systemctl start firewalld
systemctl enable firewalld
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload
```

### ufw

```bash
ufw allow ssh
ufw allow 80/tcp
ufw enable
ufw status
```

### iptables

```bash
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -j DROP
```

### NAT concepts

- `SNAT`: changes the source IP of traffic, often used for Internet access from a private network.
- `DNAT`: changes the destination IP and port, commonly used for port forwarding.

```bash
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

IP forwarding is required when a Linux box acts as a router or NAT gateway.

```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
```

## 9. DHCP, NTP, and Samba

### DHCP

```bash
systemctl enable --now dhcpd
```

### NTP

```bash
chronyc tracking
systemctl enable --now chronyd
```

### Samba

```bash
smbclient -L //192.168.1.100 -U alice
```

Use Samba to share files with Windows clients over SMB/CIFS.

## 10. Practical Labs

- Configure a static IP address in a virtual machine.
- Test connectivity with `ping`, `traceroute`, and `curl`.
- Set up passwordless SSH between two Linux machines.
- Open a firewall port and verify it by testing from another host.
- Review `/etc/hosts` and `/etc/resolv.conf` and explain how name resolution works.
