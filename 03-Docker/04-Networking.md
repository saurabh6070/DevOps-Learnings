# 🌐 Linux Networking Fundamentals (Pre-requisite for Kubernetes Networking)

> 📘 **Why this topic matters:** Kubernetes networking is built entirely on top of core Linux networking primitives — IP forwarding, network namespaces, virtual Ethernet pairs, Linux bridges, and iptables NAT rules. Before you can understand how Pods talk to each other, or how a Service routes traffic, you need to understand how plain Linux does it first. This is exactly what CNI plugins (Flannel, Calico, Weave, etc.) automate under the hood.

---

## 📑 Table of Contents

1. [IP Forwarding](#-1-ip-forwarding)
2. [Basic Networking Commands](#-2-basic-networking-commands)
3. [DNS Resolution](#-3-dns-resolution)
4. [DNS Record Types](#-4-dns-record-types)
5. [Network Namespaces](#-5-network-namespaces)
6. [Connecting Namespaces with a Virtual Cable (veth pair)](#-6-connecting-two-namespaces-with-a-virtual-cable-veth-pair)
7. [Connecting Multiple Namespaces with a Virtual Switch (Linux Bridge)](#-7-connecting-multiple-namespaces-with-a-virtual-switch-linux-bridge)
8. [NAT and Internet Access for Namespaces](#-8-nat--internet-access-for-namespaces)
9. [Port Forwarding into a Namespace](#-9-port-forwarding-into-a-namespace)
10. [Docker Container Networking Modes](#-10-docker-container-networking-modes)
11. [How Docker Implements Bridge Networking Internally](#-11-how-docker-implements-bridge-networking-internally)
12. [Default Bridge Network (docker0) in Practice](#-12-default-bridge-network-docker0-in-practice)
13. [User-Defined Bridge Networks](#-13-user-defined-bridge-networks)
14. [Docker Port Mapping / Port Forwarding](#-14-docker-port-mapping--port-forwarding)
15. [Quick Reference: Key Commands](#-15-quick-reference-key-commands)

---

## 🔀 1. IP Forwarding

IP forwarding controls whether a Linux machine is allowed to **forward packets** from one network interface to another — essentially turning the machine into a router.

- 📍 **Config file (kernel parameter):** `/proc/sys/net/ipv4/ip_forward`
- 🔴 **Default value:** `0` (forwarding disabled)
- 🟢 **To enable forwarding:**

```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
```

> ⚠️ **Note:** This setting is critical in Kubernetes — every node must be able to forward traffic between the Pod network and other interfaces, which is why `net.ipv4.ip_forward=1` is a standard requirement on all K8s nodes.

---

## 🛠️ 2. Basic Networking Commands

These are the fundamental `ip` command building blocks used throughout Linux and container networking.

| Command | Purpose |
|---|---|
| `ip link` | List all network interfaces on the host |
| `ip addr` | Show IP addresses assigned to interfaces |
| `ip addr add 192.168.1.10/24 dev eth0` | Assign an IP address to an interface |
| `ip route` | Display the host's routing table |
| `ip route add 192.168.1.0/24 via 192.168.2.1` | Add a static route via a gateway |

---

## 🧭 3. DNS Resolution

When a system needs to resolve a domain name, it follows a defined **lookup order**:

1. 🗂️ First, it checks the local hosts file: **`/etc/hosts`**
2. 🌍 If not found there, it queries the **configured DNS server**

### 🔧 Changing the Lookup Order

This order is **not fixed** — it's configurable via:

📍 **`/etc/nsswitch.conf`**

```
# Default (checks local file first, then DNS)
hosts: files dns

# Reversed (checks DNS first, then local file)
hosts: dns files
```

### 📡 DNS Server Configuration

The actual DNS server addresses that the system queries are stored in:

📍 **`/etc/resolv.conf`**

---

## 📋 4. DNS Record Types

| Record | Description |
|---|---|
| 🅰️ **A-Record** | Maps a domain name to an **IPv4** address |
| 🔷 **AAAA-Record** | Maps a domain name to an **IPv6** address |
| 🔗 **CNAME** | An **alias** for another domain name |

---

## 📦 5. Network Namespaces

A **Network Namespace (NS)** provides an isolated network stack — its own interfaces, routing table, and ARP table — separate from the host and from other namespaces. This is the core Linux primitive that containers (and Kubernetes Pods) are built on.

### ➕ Creating Namespaces

```bash
ip netns add red
ip netns add blue
```

### 📃 Listing Namespaces

```bash
ip netns
```

### 🔌 Viewing Interfaces: Host vs Namespace

```bash
# Host interfaces
ip link

# Interfaces inside a namespace (two equivalent syntaxes)
ip netns exec red ip link
ip -n red link
```

> 💡 **Key behavior:** Interfaces inside a new namespace are completely isolated — the host's IPs are **not visible**. Only the **loopback interface** is present by default. This same isolation applies to containers.

### 🗺️ ARP Tables: Host vs Namespace

```bash
# Host ARP table → shows entries
arp -s

# Namespace ARP table → empty (isolated)
ip netns exec red arp
```

### 🛣️ Routing Tables: Host vs Namespace

```bash
# Host routing table → shows entries
route

# Namespace routing table → empty (isolated)
ip netns exec red route
```

---

## 🔗 6. Connecting Two Namespaces with a Virtual Cable (veth pair)

To let two namespaces talk directly to each other, you create a **veth (virtual Ethernet) pair** — think of it as a virtual patch cable with two ends.

### Step 1 — Create the veth pair and attach each end to a namespace

```bash
ip link add veth-red type peer name veth-blue
ip link set veth-red netns red
ip link set veth-blue netns blue
```

### Step 2 — Assign IP addresses to each end

```bash
ip -n red addr add 192.168.15.1 dev veth-red
ip -n blue addr add 192.168.15.2 dev veth-blue
```

### Step 3 — Bring both ends of the link up

```bash
ip -n red link set veth-red up
ip -n blue link set veth-blue up
```

### Step 4 — Test connectivity

```bash
ip netns exec red ping 192.168.15.2
```

### Step 5 — Verify ARP entries

```bash
ip netns exec red arp
```

> ⚠️ **Limitation:** A veth pair only connects **two** namespaces. To connect **three or more**, you need a virtual switch — see the next section.

---

## 🔀 7. Connecting Multiple Namespaces with a Virtual Switch (Linux Bridge)

When more than two namespaces need to communicate, a single veth pair per connection doesn't scale. Instead, create a **Linux bridge** — a virtual switch that all namespaces plug into.

### Step 1 — Create the bridge (on the host)

```bash
ip link add v-net-0 type bridge
```

### Step 2 — Bring the bridge up

```bash
ip link set dev v-net-0 up
```

### Step 3 — Verify bridge status

```bash
ip link
```

### Step 4 — Attach each namespace to the bridge

First remove the old direct veth link (deleting one end auto-deletes the other):

```bash
ip -n red link del veth-red
```

Then create new veth pairs — one end goes into the namespace, the other attaches to the bridge:

```bash
ip link add veth-red type veth peer name veth-red-br
ip link add veth-blue type veth peer name veth-blue-br

ip link set veth-red netns red
ip link set veth-red-br master v-net-0

ip link set veth-blue netns blue
ip link set veth-blue-br master v-net-0
```

Assign IPs and bring the namespace-side interfaces up:

```bash
ip -n red addr add 192.168.15.1 dev veth-red
ip -n blue addr add 192.168.15.2 dev veth-blue

ip -n red link set veth-red up
ip -n blue link set veth-blue up
```

### Step 5 — Give the bridge itself an IP (so the host can reach the namespaces)

```bash
ping 192.168.15.1      # ❌ fails — bridge has no IP yet

ip addr add 192.168.15.5/24 dev v-net-0

ping 192.168.15.1      # ✅ works now
```

> 💡 Once assigned, `192.168.15.5/24` (the bridge IP) becomes visible in the host's `ip link` output — along with any other IPs in the same subnet.

### Step 6 — Route between subnets via the bridge

```bash
ip netns exec blue ip route add 192.168.1.0/24 via 192.168.15.5

ping 192.168.15.3   # host is unreachable but no longer shows "unreachable" error
```

---

## 🌍 8. NAT & Internet Access for Namespaces

To let namespace traffic reach **external networks** (like the internet), the outside world needs to see traffic as coming from the **host**, not from an internal namespace IP. This requires **NAT (masquerading)**.

### 🔒 Enable NAT on the Host

```bash
iptables -t nat -A POSTROUTING -s 192.168.15.0/24 -j MASQUERADE
```

### 🌐 Connect a Namespace to the Internet (e.g., 8.8.8.8)

```bash
ip netns exec blue ping 8.8.8.8            # ❌ fails initially

ip netns exec blue route                  # inspect current routes

ip netns exec blue route add default via 192.168.15.5   # set default gateway

ip netns exec blue ping 8.8.8.8            # ✅ works now
```

---

## 🚪 9. Port Forwarding into a Namespace

To let **external/internet traffic reach a service running inside a namespace** (e.g., on port 80), configure **DNAT (Destination NAT)** / port forwarding on the host:

```bash
iptables -t nat -A PREROUTING --dport 80 --to-destination 192.168.15.2:80 -j DNAT
```

This tells the host: *"Any incoming traffic on port 80 should be redirected to `192.168.15.2:80` inside the namespace."*

---

## 🐳 10. Docker Container Networking Modes

When running a container, you choose one of the following networking modes:

### 🚫 None
The container is not attached to any network at all.
- ❌ Cannot communicate with the host
- ❌ Cannot communicate with other containers

### 🖥️ Host
The container shares the **host's network stack** directly.
- ✅ A service on container port 80 is exposed on the host's IP with **no port-forwarding needed**
- ⚠️ **Limitation:** Two containers of the same type (both listening on port 80) **cannot** run simultaneously on the same host, since they'd conflict on the same port

### 🌉 Bridge (default)
Docker creates an **internal private network** that the Docker host and all containers attach to.

- Docker calls this network the **"bridge"** network
- On the host, this appears in `ip a` as an interface named **`docker0`**
- `docker0` acts like:
  - An **interface** to the Docker host
  - A **switch** for all containers/namespaces on that host
- The IP assigned to `docker0` becomes the **gateway** for the bridge network

---

## 🔍 11. How Docker Implements Bridge Networking Internally

Every time a container is created, Docker automatically creates a **network namespace** for it — exactly like the manual `ip netns add` steps covered earlier.

### Inspecting Docker's Auto-Created Networking

```bash
# List namespaces → shows the container's auto-generated NS
ip netns
# Output: b3165c10a92b

# Find the host-side end of the veth pair attached to docker0
ip link | grep master | grep docker0
# Output: vethbb1c343@if7

# Find the container-side end of the veth pair
ip -n b3165c10a92b link
# Output: eth0@if8

# Check the container's assigned IP
ip -n b3165c10a92b addr
```

> 🔗 **How the pair connects:** `if7` and `if8` are two ends of the **same veth pair** — `if7` lives on the Docker host side (attached to `docker0`), and `if8` lives inside the container as `eth0`. This is precisely the veth-pair + bridge pattern from Section 7, just automated by Docker.

---

## 🌉 12. Default Bridge Network (`docker0`) in Practice

Section 10 introduced the **bridge** mode conceptually. Now let's see the default bridge — `docker0` — in action, and revisit it through the **namespace lens** from Sections 5–7: `docker0` is just a **Linux bridge**, and every container attached to it is just a **network namespace** connected via a **veth pair**, exactly as you built manually.

### 🔄 Communication Flows

- **Container → Internet:**

  ```
  Container A → docker0 → eth0 → Internet
  ```
  (This is the same MASQUERADE/NAT path from Section 8 — `docker0` plays the role of your `v-net-0` bridge, and Docker adds the NAT rule automatically.)

- **Container A → Container B (same bridge):**

  ```
  Container A → docker0 → Container B
  ```
  (Identical to the veth-pair-via-bridge flow from Section 7 — traffic never has to leave the host.)

### 🔍 Inspecting the Default Bridge

```bash
ip addr show                        # Check docker0 (e.g., 172.17.0.1)
docker network ls                   # Shows default networks
docker inspect bridge | grep Subnet
```

> 💡 `docker0`'s IP (e.g. `172.17.0.1`) is the **gateway** for the bridge network — same role as the `192.168.15.5/24` IP you assigned to `v-net-0` in Section 7, Step 5.

### 🚀 Running Containers on the Default Bridge

```bash
docker run -td --name contA alpine
docker run -td --name contB alpine

docker attach contA        # Check IP: likely 172.17.0.2
# Detach without stopping the container: Ctrl + P, then Ctrl + Q

docker attach contB        # Check IP: likely 172.17.0.3
```

### ❌ Known Limitation: No DNS on the Default Bridge

```bash
# Inside contA:
ping contB
```

This **fails** — the default `docker0` bridge network does **not support automatic DNS resolution** between containers by name. Containers can only reach each other by **IP address**, not by container name.

> ⚠️ This is exactly why the default bridge is rarely used in real deployments — and why Kubernetes relies on **CoreDNS** + Services instead of manual IP tracking. It's also why Docker introduced **user-defined bridge networks**, covered next.

---

## 🛠️ 13. User-Defined Bridge Networks

Custom (user-defined) bridge networks solve the default bridge's biggest weakness: they provide **built-in DNS resolution** by container name, plus **better isolation** between groups of containers.

| Feature | Default Bridge (`docker0`) | User-Defined Bridge |
|---|---|---|
| 🌉 Bridge type | Auto-created, single shared bridge | You create it, one per application/stack |
| 🔎 DNS by container name | ❌ Not supported | ✅ Supported out of the box |
| 🔒 Isolation | All containers share one flat network | Only containers on the same custom network can reach each other by default |
| 🧩 Underlying mechanism | Linux bridge + veth pairs (Sections 6 & 7) | Same Linux bridge + veth pair mechanism, just a **separate bridge interface** per network |

### 🛠️ Create and Inspect a Custom Bridge Network

```bash
# Create a new user-defined bridge network
docker network create my-bridge

# Inspect it — shows subnet, gateway, and connected containers
docker network inspect my-bridge
```

> 💡 **Under the hood:** `docker network create` does exactly what you did manually in Section 7 — it runs the equivalent of `ip link add <name> type bridge` and gives it its own gateway IP. Any container you attach with `docker run --network my-bridge ...` gets its own namespace + veth pair, connected to this new bridge — resolvable by container name via Docker's embedded DNS server.

---

## 🔁 14. Docker Port Mapping / Port Forwarding

If a container exposes a service on port 80, that service can be published to the **outside world on any host port** (e.g., `8080`) using **port mapping**.

Any traffic hitting the host on port `8080` gets forwarded to port `80` inside the container — using the exact same DNAT mechanism we configured manually in Section 9.

### ✋ Manual command (what we did ourselves):

```bash
iptables -t nat -A PREROUTING --dport 80 --to-destination 192.168.15.2:80 -j DNAT
```

### 🤖 Equivalent command Docker runs internally:

```bash
iptables -t nat -A DOCKER --dport 8080 --to-destination 192.168.15.2:80 -j DNAT
```

### 🔎 Viewing All Docker-Created NAT Rules

```bash
iptables -nvL -t nat
```

---

## ⚡ 15. Quick Reference: Key Commands

| Task | Command |
|---|---|
| 🔀 Enable IP forwarding | `echo 1 > /proc/sys/net/ipv4/ip_forward` |
| ➕ Create namespace | `ip netns add <name>` |
| 📃 List namespaces | `ip netns` |
| 🔌 Run command inside namespace | `ip netns exec <name> <cmd>` or `ip -n <name> <cmd>` |
| 🔗 Create veth pair | `ip link add <veth1> type peer name <veth2>` |
| 🌉 Create bridge | `ip link add <name> type bridge` |
| 🧷 Attach interface to bridge | `ip link set <iface> master <bridge>` |
| 🌍 Enable NAT (outbound) | `iptables -t nat -A POSTROUTING -s <subnet> -j MASQUERADE` |
| 🚪 Port forward (inbound) | `iptables -t nat -A PREROUTING --dport <port> --to-destination <ip:port> -j DNAT` |
| 🗺️ View DNS lookup order | `/etc/nsswitch.conf` |
| 📡 View configured DNS servers | `/etc/resolv.conf` |
| 🐳 List Docker networks | `docker network ls` |
| 🔎 Inspect a Docker network | `docker network inspect <name>` |
| 🛠️ Create user-defined bridge | `docker network create <name>` |
| 📎 Run container on a network | `docker run --network <name> ...` |

---

## ✅ Key Takeaways for Kubernetes Networking

- 🧩 **Pods = Network Namespaces.** Every Kubernetes Pod gets its own network namespace, just like `ip netns add`.
- 🌉 **CNI plugins = automated bridges + veth pairs.** What Flannel/Calico/Weave do under the hood is exactly Sections 6, 7, 11 & 12, automated across every node.
- 🔁 **kube-proxy = iptables/IPVS rules.** Service routing in Kubernetes is built on the same DNAT/MASQUERADE concepts from Sections 8 & 9.
- 🐳 **Docker's `docker0` bridge model** is the direct ancestor of how the Kubernetes Pod network operates on a single node.
- 📛 **CoreDNS solves the same gap as user-defined bridge networks.** Just as a custom Docker bridge (Section 13) gives you DNS-by-name instead of tracking raw IPs, Kubernetes' CoreDNS gives every Pod/Service a resolvable name instead of relying on ever-changing Pod IPs.

> 🎯 Master these Linux fundamentals first — once they're second nature, Kubernetes networking concepts (Pod-to-Pod communication, Services, CNI) will feel like a natural extension rather than new magic.
