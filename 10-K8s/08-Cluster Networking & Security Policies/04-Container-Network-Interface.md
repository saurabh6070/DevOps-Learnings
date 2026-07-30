# 🌐 Container Network Interface (CNI)

> **Kubernetes Networking Series**

---

## 📖 What is CNI?

**CNI (Container Network Interface)** is a set of **standards** that define how networking programs — called **plugins** — should be developed to solve networking challenges inside a container runtime environment.

- CNI specifies **how plugins should be developed**.
- CNI specifies **how the container runtime should invoke those plugins**.
- The **Bridge** program (commonly used to set up container networking) is itself an example of a **CNI plugin**.

In short: CNI is the *contract* between the container runtime and the networking plugin — it doesn't do the networking itself, it just defines the rules both sides must follow.

---

## 🧩 CNI Responsibilities

CNI splits responsibilities between two parties: the **Container Runtime** and the **Plugin**.

### 🐳 Responsibilities of the Container Runtime
*(In this context, the Container Runtime is Docker)*

| # | Responsibility |
|---|-----------------|
| 1 | Create the **network namespace** for the container |
| 2 | Identify **which network** the container must attach to |
| 3 | **Invoke the network plugin** (e.g., bridge) when a container is **added** |
| 4 | **Invoke the network plugin** (e.g., bridge) when a container is **deleted** |
| 5 | Provide the network configuration in **JSON format** |

### 🔌 Responsibilities of the Plugin

| # | Responsibility |
|---|-----------------|
| 1 | Support command-line arguments: **`ADD`**, **`DEL`**, **`CHECK`** |
| 2 | Accept parameters such as **container ID**, **network namespace**, etc. |
| 3 | **Manage IP address assignment** to Pods |
| 4 | **Return results** in a specific, standardized format |

---

## 🛠️ Types of CNI Plugins

### 📦 Built-in / Standard Plugins
CNI ships with a set of plugins out of the box, including:
- **Bridge**
- **IPVLAN**
- **MACVLAN**
- A plugin for **Windows**
- IPAM (IP Address Management) plugins like **Host-Local** and **DHCP**

### 🏢 Third-Party Plugins
Several vendors and open-source projects provide their own CNI-compliant plugins:
- **Weave**
- **Flannel**
- **Cilium**
- **VMware NSX**
- **Calico**
- **Infoblox**
- ...and others

✅ All of these plugins (and the container runtimes that use them) implement the **CNI standard**, which is what makes them interoperable with Kubernetes.

---

## ⚔️ Docker vs CNI: The CNM Difference

> ⚠️ **Important:** Docker does **not** natively use CNI.

- Docker has its **own** networking standard called **CNM (Container Network Model)**.
- Since Kubernetes requires CNI-compliant behavior, it works around Docker's native networking rather than using it directly.

### How Kubernetes Handles This with Docker

1. When Kubernetes creates a Docker container, it creates it with **no networking** attached:
   ```bash
   docker run --network=none nginx
   ```
2. Kubernetes then **invokes the configured CNI plugin** to handle the actual network setup, equivalent to:
   ```bash
   bridge add <container-id> /var/run/<container-id>
   ```

This way, Docker only handles container creation, while **CNI plugins take full ownership of networking** — satisfying Kubernetes' CNI requirements even though Docker itself speaks CNM.

---

## 🔍 Verifying Cluster Networking on a Node

### 1️⃣ Find the Node's Internal IP
Used for cluster (node-to-node) connectivity:
```bash
kubectl get no -o wide
```
Look at the **`INTERNAL-IP`** column for the node you're inspecting.

### 2️⃣ Match the Internal IP to a Network Interface
Check the host's interfaces to find which one holds that Internal-IP (and note its MAC address):
```bash
ip address show eth0
```

### 3️⃣ Identify the CNI Bridge Interface
If **containerd** is the container runtime, the bridge interface created on the host will typically have an IP like `xxx.x.x.1` and is usually named **`cni0`**.

You can confirm this manually via `ip a`, or take the quick route:
```bash
ip address show type bridge
```
✅ The output should show only the **`cni0`** interface.

---

## 🩺 Checking Control Plane Component Ports

Use `netstat` to confirm which ports key control plane services are listening on:

```bash
# Kube-scheduler
netstat -npl | grep -i scheduler
# → Output: 10259

# etcd
netstat -npl | grep -i etcd
# → Output: 2379, 2381
```

| Component | Port(s) |
|------------|---------|
| 🗓️ kube-scheduler | `10259` |
| 🗄️ etcd | `2379`, `2381` |

---

## 📝 Quick Recap

- **CNI** = standard defining how container runtimes and networking plugins talk to each other.
- Runtime handles namespaces + invoking plugins; **plugins handle IP assignment + ADD/DEL/CHECK**.
- CNI has both **built-in** (bridge, IPVLAN, MACVLAN) and **third-party** (Calico, Flannel, Cilium, Weave) plugins.
- **Docker uses CNM, not CNI** — Kubernetes works around this by disabling Docker's networking and invoking the CNI plugin directly.
- Use `kubectl get no -o wide`, `ip a`, and `ip address show type bridge` to trace cluster networking on a node.
- Use `netstat -npl` to verify which ports control plane components (scheduler, etcd) are listening on.
