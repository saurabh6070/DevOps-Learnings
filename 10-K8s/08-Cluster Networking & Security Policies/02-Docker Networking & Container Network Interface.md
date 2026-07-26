# 🐳 Docker Networking & Container Network Interface (CNI)

Understanding how Docker networks containers — and the CNI standard that Kubernetes builds on top of — is essential background before diving into Kubernetes pod networking.

---

## 🔌 1. Docker Container Networking Modes

When you run a container, Docker lets you choose **how** it connects to the network. There are three main options:

### 🚫 None
- The container is **not attached to any network** at all.
- It **cannot communicate** with the host or with any other container.

```bash
docker run --network=none nginx
```

---

### 🖥️ Host
- The container **shares the host's network stack directly**.
- A service running on **port 80 inside the container** is exposed on the **host's IP on port 80** — with **no port-forwarding** required.

⚠️ **Limitation:** Because the container uses the host's ports directly, **you cannot run two instances of the same container** (or any two containers listening on the same port) on the same host — they'd conflict on the port.

```bash
docker run --network=host nginx
```

---

### 🌉 Bridge (Default)
Docker creates an **internal private network** that the Docker host and all its containers attach to.

- Docker calls this network the **"bridge"** network.
- On the host, this shows up as an interface named **`docker0`** (visible via `ip a`).
- Think of the bridge as: an **interface** to the Docker host, but a **virtual switch** connecting all the containers (namespaces) on that host.
- The `docker0` interface on the host is assigned the **gateway IP** of this bridge network.

```bash
docker run --network=bridge nginx
```

#### 🔍 Inspecting the Bridge Network in Action

When a container is created, Docker creates a **network namespace** for it — exactly like manually creating namespaces with `ip netns add`.

**1️⃣ View the namespace created for the container:**
```bash
ip netns
```
➡️ Output: `b3165c10a92b` — the namespace ID Docker created for the container.

**2️⃣ Find the host-side end of the veth pair (attached to the bridge):**
```bash
ip link | grep master | grep docker0
```
➡️ Output: `vethbb1c343@if7` — the **Docker-host end** of the virtual cable connecting the container to `docker0`.

**3️⃣ Find the container-side end of the veth pair:**
```bash
ip -n b3165c10a92b link
```
➡️ Output: `eth0@if8` — the **container end** of the same virtual cable.

**4️⃣ Check the container's assigned IP:**
```bash
ip -n b3165c10a92b addr
```
➡️ Output: the IP address Docker assigned to the container for bridge-network communication.

> 🔗 `if7` and `if8` are **two ends of the same veth pair** — one plugged into the Docker host (attached to `docker0`), and the other plugged into the container's namespace (as `eth0`). This is the same veth-pair pattern used when manually connecting network namespaces.

---

## 🚪 2. Port Mapping / Port Forwarding

By default, a service exposed on **port 80 inside a container** is only reachable **within** the Docker bridge network. To make it reachable from **outside** on a different port (e.g., `8080`), Docker uses **port mapping**:

```bash
docker run -p 8080:80 nginx
```

Any traffic hitting **port 8080 on the host** gets forwarded to **port 80 inside the container** — Docker implements this exactly the same way we did manually earlier with `iptables` DNAT rules.

### 🧾 Comparing the iptables Rules

**Manual port-forwarding rule (done earlier ourselves):**
```bash
iptables -t nat -A PREROUTING --dport 80 --to-destination 192.168.15.2:80 -j DNAT
```

**Rule Docker creates internally:**
```bash
iptables -t nat -A DOCKER --dport 8080 --to-destination 192.168.15.2:80 -j DNAT
```

### 👀 Viewing Docker's NAT Routing Rules
```bash
iptables -nvL -t nat
```
➡️ Shows all the IP routing / NAT rules Docker has created.

---

## 📐 3. Container Network Interface (CNI)

### 📖 What is CNI?
**CNI (Container Network Interface)** is a **set of standards** that define:
- How networking **programs** (called **plugins**) should be developed to solve container networking challenges.
- How a **container runtime** should invoke these plugins.

> 🧩 The "**bridge**" networking approach discussed above is itself implemented as a **CNI plugin** in the CNI world.

CNI defines a clear **division of responsibilities** between the container runtime and the plugins.

---

### 🏗️ Responsibilities of the Container Runtime
*(In our examples, the container runtime is **Docker**)*

- 📦 Must **create the network namespace** for the container.
- 🔎 Must **identify which network** the container should attach to.
- ▶️ Must **invoke the network plugin** (e.g., bridge) when a container is **added**.
- ⏹️ Must **invoke the network plugin** when a container is **deleted**.
- 📄 Must provide the network configuration in a defined **JSON format**.

---

### 🔧 Responsibilities of the Plugins

- 🖥️ Must support standard **command-line actions**: `ADD` / `DEL` / `CHECK`.
- 📥 Must accept parameters like **container ID**, **network namespace**, etc.
- 🏷️ Must **manage IP address assignment** to pods/containers.
- 📤 Must **return results** in a specific, standardized format.

---

### 🧰 Built-in & Third-Party CNI Plugins

**Plugins that ship with CNI:**

| Category | 🔌 Plugins |
|---|---|
| Networking | Bridge, IPVLAN, MACVLAN, Windows plugin |
| IPAM (IP Address Management) | Host-Local, DHCP |

**Popular third-party CNI plugins:**

| 🌐 Weave | 🌐 Flannel | 🌐 Cilium | 🌐 VMware NSX | 🌐 Calico | 🌐 Infoblox |
|---|---|---|---|---|---|

➡️ All of these plugins implement the **CNI standard**, allowing container runtimes to use them interchangeably.

---

### ⚠️ Important: Docker Does NOT Use CNI!

Despite the bridge concept being similar, **Docker does not implement the CNI standard**.

Instead, Docker has its **own** networking standard called:

> 🏷️ **CNM — Container Network Model**

---

## ☸️ 4. How Kubernetes Uses CNI

Since Kubernetes needs a standardized way to plug in networking solutions, it relies on **CNI**, not Docker's native networking.

### 🔄 The Flow

1. When Kubernetes creates a Docker container for a pod, it creates it with **no network attached**:

   ```bash
   docker run --network=none nginx
   ```

2. Kubernetes then **invokes the configured CNI plugin** to handle all the actual network setup (assigning IP, attaching to bridge, etc.):

   ```bash
   bridge add 2e34dcf43 /var/run/2e34dcf43
   ```

> 💡 In other words: Kubernetes deliberately **skips Docker's own networking (CNM)** and instead hands off networking responsibility entirely to a **CNI plugin** (like Calico, Flannel, Weave, Cilium, etc.), which follows the standardized ADD/DEL/CHECK interface.

---

## 📚 5. Summary Cheat Sheet

| Concept | 🔑 Key Point |
|---|---|
| `none` network | Container fully isolated, no networking |
| `host` network | Shares host's network stack — no port mapping, but port conflicts possible |
| `bridge` network | Default; private internal network via `docker0`, containers connected via veth pairs |
| Port Mapping | Host port → container port via `iptables` DNAT rules |
| CNI | Standard defining plugin interface for container networking |
| Container Runtime (CNI role) | Creates namespace, identifies network, invokes plugin on add/delete |
| Plugin (CNI role) | Supports ADD/DEL/CHECK, assigns IPs, returns structured results |
| CNM | Docker's own (non-CNI) networking model |
| Kubernetes + Docker | Creates container with `--network=none`, then CNI plugin does the rest |

> 🎓 **Key takeaway:** Docker's bridge networking is a great way to *understand* container networking concepts (namespaces, veth pairs, bridges) — but Kubernetes doesn't rely on Docker's built-in networking (CNM). Instead, it uses the vendor-neutral **CNI** standard, letting you plug in networking solutions like Calico, Flannel, Weave, or Cilium.
