# 🌐 Linux Networking Fundamentals (Kubernetes Networking Prerequisites)

Before diving into Kubernetes CNI plugins and pod networking, it's essential to understand how **Linux handles networking at the host level** — IP forwarding, routing, DNS resolution, network namespaces, virtual links, and bridges. Kubernetes networking is built entirely on top of these Linux primitives.

---

## 🔀 1. IP Forwarding

By default, a Linux machine does **not** forward packets between network interfaces — it behaves like an end host, not a router.

### 📴 Check / Default State
By default, IP forwarding is **disabled** (`0`).

### ✅ Enable IP Forwarding
To allow a Linux machine to forward packets from one interface to another (i.e., act like a router):

```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
```

> 💡 This is exactly how a Kubernetes node routes traffic between pods, containers, and external networks.

---

## 🛠️ 2. Essential `ip` Commands

These are the bread-and-butter commands for inspecting and configuring Linux networking.

| Command | 📝 Purpose |
|---|---|
| `ip link` | List network interfaces |
| `ip addr` | Show IP addresses assigned to interfaces |
| `ip addr add 192.168.1.10/24 dev eth0` | Assign an IP address to an interface |
| `ip route` | Display the routing table |
| `ip route add 192.168.1.0/24 via 192.168.2.1` | Add a static route via a gateway |

---

## 📖 3. DNS Resolution Order

### 🔍 How Name Resolution Works
When resolving a domain name, Linux first checks the **local hosts file**:

```
/etc/hosts
```

If no match is found there, it falls back to the **configured DNS server**.

### ⚙️ Changing the Resolution Order
This lookup order is **not fixed** — it's controlled by:

```
/etc/nsswitch.conf
```

**Default order:**
```
hosts: files dns
```
➡️ Checks `/etc/hosts` (**files**) first, then **DNS**.

**To reverse the order** (check DNS first, then the hosts file):
```
hosts: dns files
```

### 🗂️ DNS Server Configuration
On a DNS server, domain name entries are stored in:

```
/etc/resolv.conf
```

### 🏷️ Common DNS Record Types

| Record | 📌 Purpose |
|---|---|
| **A-Record** | Maps a domain name to an **IPv4** address |
| **AAAA-Record** | Maps a domain name to an **IPv6** address |
| **CNAME** | An **alias** pointing to another domain name |

---

## 🧪 4. Network Namespaces (netns)

A **network namespace** is an isolated network stack — its own interfaces, routes, and ARP table — commonly used to simulate separate hosts (and the foundation of how containers get network isolation).

### ➕ Create Network Namespaces
```bash
ip netns add red
ip netns add blue
```

### 📋 List Network Namespaces
```bash
ip netns
```

---

## 🔎 5. Inspecting Namespaces vs the Host

### 🖧 Interfaces (`ip link`)

**On the host:**
```bash
ip link
```

**Inside a namespace:**
```bash
ip netns exec red ip link
# or equivalently
ip -n red link
```

> ⚠️ **Output:** The host's real interfaces are **not visible** inside the namespace — only the **loopback interface** appears. This is the same isolation behavior containers rely on.

---

### 📇 ARP Table

**On the host:**
```bash
arp -s
```
➡️ Output: ARP entries are visible.

**Inside a namespace:**
```bash
ip netns exec red arp
```
➡️ Output: **Blank** (empty — nothing has been configured yet).

---

### 🗺️ Routing Table

**On the host:**
```bash
route
```
➡️ Output: Route entries are visible.

**Inside a namespace:**
```bash
ip netns exec red route
```
➡️ Output: **Blank** (no routes configured yet).

---

## 🔗 6. Connecting Two Namespaces Directly (veth Pair)

To let two namespaces talk to each other, create a **virtual Ethernet (veth) pair** — think of it as a virtual patch cable with one end in each namespace.

### 1️⃣ Create the Virtual Link & Attach to Namespaces
```bash
ip link add veth-red type peer name veth-blue
ip link set veth-red netns red
ip link set veth-blue netns blue
```

### 2️⃣ Assign IP Addresses to Each End
```bash
ip -n red addr add 192.168.15.1 dev veth-red
ip -n blue addr add 192.168.15.2 dev veth-blue
```

### 3️⃣ Bring the Virtual Links Up
```bash
ip -n red link set veth-red up
ip -n blue link set veth-blue up
```

### 4️⃣ Test Connectivity
```bash
ip netns exec red ping 192.168.15.2
```

### 5️⃣ Verify ARP Entries
```bash
ip netns exec red arp
```

> 💡 This point-to-point veth pair only works for **two** namespaces. For **three or more**, you need a virtual switch (bridge) — see next section.

---

## 🌉 7. Connecting Multiple Namespaces via a Virtual Switch (Bridge)

For connecting **more than two** namespaces, Linux provides a **virtual bridge** — acting like a switch that all namespaces plug into.

### 1️⃣ Create a Linux Bridge (on the Host)
```bash
ip link add v-net-0 type bridge
```

### 2️⃣ Enable (Bring Up) the Bridge
```bash
ip link set dev v-net-0 up
```

### 3️⃣ Verify Bridge Status
```bash
ip link
```

### 4️⃣ Attach Namespaces to the Bridge

Each namespace needs a veth pair where **one end goes into the namespace** and the **other end attaches to the bridge**.

First, remove the old point-to-point link (only one end needs deleting — the other end auto-deletes):
```bash
ip -n red link del veth-red
```

Create new veth pairs — one leg for the namespace, one leg for the bridge:
```bash
ip link add veth-red type veth peer name veth-red-br
ip link add veth-blue type veth peer name veth-blue-br
```

Move each namespace-side leg into its namespace:
```bash
ip link set veth-red netns red
ip link set veth-blue netns blue
```

Attach each bridge-side leg to the bridge (`v-net-0`) as its master:
```bash
ip link set veth-red-br master v-net-0
ip link set veth-blue-br master v-net-0
```

Assign IPs inside each namespace:
```bash
ip -n red addr add 192.168.15.1 dev veth-red
ip -n blue addr add 192.168.15.2 dev veth-blue
```

Bring the namespace-side interfaces up:
```bash
ip -n red link set veth-red up
ip -n blue link set veth-blue up
```

### 5️⃣ Test Connectivity (First Attempt)
```bash
ping 192.168.15.1
```
➡️ ❌ **Output: Ping does not work** — the bridge itself has no IP address yet, so the host can't reach the namespace network.

### 6️⃣ Assign an IP to the Bridge Itself
```bash
ip addr add 192.168.15.5/24 dev v-net-0
```

### 7️⃣ Test Connectivity Again
```bash
ping 192.168.15.1
```
➡️ ✅ **Output: Ping now works!**

> 📌 The bridge's IP (`192.168.15.5/24`) — along with the namespace IPs in the same subnet (e.g., `192.168.1.20`) — now becomes visible in the host's `ip link` / `ip addr` output.

### 8️⃣ Route Between Namespaces via the Bridge
To let one namespace reach the other's subnet through the bridge as gateway:
```bash
ip netns exec blue ip route add 192.168.1.0/24 via 192.168.15.5
```

Test:
```bash
ping 192.168.15.3
```
➡️ ⚠️ **Output:** Ping still doesn't fully succeed, but the "network unreachable" message **no longer appears** — routing is now correctly configured, just needs further completion.

---

## 🌍 8. Enabling Internet Access for Namespaces (NAT)

To let a namespace reach **external networks/IPs**, the host must perform **NAT (masquerading)** so outside networks see traffic as coming from the host, not the internal namespace.

### 🛡️ Enable NAT (Masquerade) on the Host
```bash
iptables -t nat -A POSTROUTING -s 192.168.15.0/24 -j MASQUERADE
```

### 🧭 Connect a Namespace to the Internet (e.g., Google DNS 8.8.8.8)

**Attempt without a default route:**
```bash
ip netns exec blue ping 8.8.8.8
```
➡️ ❌ Output: Ping does not work.

**Check current routes:**
```bash
ip netns exec blue route
```

**Add a default route via the bridge:**
```bash
ip netns exec blue route add default via 192.168.15.5
```

**Retry:**
```bash
ip netns exec blue ping 8.8.8.8
```
➡️ ✅ Output: Ping now works!

---

## 🚪 9. Port Forwarding — Exposing a Namespace to the Internet

To allow **incoming** internet traffic to reach a service running inside a namespace (e.g., a web server on port 80), configure **DNAT (Destination NAT)** / port forwarding on the host:

```bash
iptables -t nat -A PREROUTING --dport 80 --to-destination 192.168.15.2:80 -j DNAT
```

➡️ This forwards incoming traffic on port `80` from the host to `192.168.15.2:80` inside the namespace.

---

## 📚 10. Summary — Why This Matters for Kubernetes

| Concept | 🔗 Kubernetes Parallel |
|---|---|
| IP Forwarding | Nodes route traffic between pods |
| Network Namespaces | Each **pod** gets its own network namespace |
| veth Pairs | Connects a pod's namespace to the node's root namespace |
| Linux Bridge | Similar role to CNI bridge plugins connecting multiple pods |
| NAT / Masquerade | How pods reach the internet (e.g., `iptables MASQUERADE` rules set by kube-proxy/CNI) |
| Port Forwarding (DNAT) | Conceptually similar to Kubernetes **Services** and `NodePort` |

> 🎓 **Key takeaway:** Kubernetes networking (pods, Services, CNI plugins) is essentially an automated, large-scale orchestration of these exact same Linux primitives — namespaces, veth pairs, bridges, routes, and iptables rules.
