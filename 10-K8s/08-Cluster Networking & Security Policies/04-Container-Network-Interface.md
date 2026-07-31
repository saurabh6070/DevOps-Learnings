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

## 📦 Networking Model of a Pod

Kubernetes networking is built on three fundamental rules that every CNI plugin must guarantee:

- 🆔 Every **Pod** must have its **own IP address**.
- 🤝 Every **Pod** must be able to **communicate with every other Pod on the same node**.
- 🌍 Every **Pod** must be able to **communicate with every other Pod on a different node — without NAT** (regardless of whether the two Pods' IP ranges are the same or different).

---

## ⚙️ How Kubelet Invokes the CNI Plugin

Whenever a container is **created** or **deleted**, `kubelet` follows a defined sequence to hand networking off to the CNI plugin:

1. **Kubelet reads its configuration file** to find the path of the CNI **configuration directory**.
   - This path is passed as an argument when kubelet is installed:
     ```bash
     --cni-conf-dir=/etc/cni/net.d
     ```
2. From the configuration file found in that directory, kubelet learns the path of the **CNI plugin binary** that will actually perform the networking tasks.
   - This is passed as:
     ```bash
     --cni-bin-dir=/etc/cni/bin
     ```
3. Kubelet then **executes the binary/script**, which handles IP address assignment, reachability, and namespace setup for the container — on both creation and deletion.
   - Example invocation:
     ```bash
     ./net-script.sh add container-name namespace
     ```

> 📌 **Note:** If multiple configuration files exist inside `/etc/cni/net.d/`, kubelet will always read the **first file in alphabetical order**.

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

## 🔧 Inspecting the Kubelet CNI Configuration

CNI plugin configuration is defined through parameters passed to the **kubelet config file**. Key parameters include:

```bash
--network-plugin=cni
--cni-bin-dir=/opt/cni/bin
--cni-conf-dir=/etc/cni/net.d
```

These can be verified by inspecting the running kubelet process:

```bash
ps -aux | grep -i kubelet
```

### 📁 Exploring the CNI Binary Directory

```bash
ls /opt/cni/bin
```
**Output:**
```
bridge, dhcp, flannel, host-local, ipvlan, loopback, macvlan,
portmap, ptp, sample, tuning, vlan, weave-ipam, weave-net, weave-plugin-2.2.1
```

### 📁 Exploring the CNI Config Directory

```bash
ls /etc/cni/net.d
```
**Output:**
```
10-bridge.conf
```

### 📄 Sample CNI Config File

```bash
cat /etc/cni/net.d/10-bridge.conf
```
**Output:**
```json
{
    "cniVersion": "0.2.0",
    "name": "mynet",
    "type": "bridge",
    "bridge": "cni0",
    "isGateway": "true",
    "isMasq": "true",
    "ipam": {
        "type": "host-local",
        "subnet": "10.22.0.0/16",
        "routes": [
            { "dst": "0.0.0.0/0" }
        ]
    }
}
```

> 📌 **Reminder:** If multiple files exist in `/etc/cni/net.d/`, kubelet reads only the **first one alphabetically**.

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

## 🛣️ Checking the Default Route Configured by a CNI

To trace which IP pool a CNI plugin has assigned for Pod networking:

1. **Check which CNI is in use:**
   ```bash
   ls /etc/cni/net.d/
   ```
2. **Inspect the CNI's Pods** to find the IP address pool used for Pod IP allocation. For example, with Weave:
   ```bash
   kubectl get pods -n kube-system | grep -i weave
   kubectl describe pod weave-net-qbfu43 -n kube-system | grep -i IPALLOC_RANGE
   ```
3. **Log in to the worker node** and run:
   ```bash
   route -n
   ```
   Identify the entry whose **destination** matches the IP-address pool found in step 2.
4. **Check the gateway** configured for that routing entry.

---

## 🎯 Checking Service & Pod IP Ranges

### 🧭 Service Cluster IP Range

Run this on the Master / Control-Plane node to find the CIDR range used for **Services** inside the cluster:

```bash
cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep ip-range
```
**Output:**
```
--service-cluster-ip-range=10.96.0.0/12
```

### 🔀 Kube-Proxy Mode

Check which proxy mode kube-proxy is using (e.g., **iptables**):

```bash
kubectl logs kube-proxy-bqzvv -n kube-system
```
**Output:**
```
I0220 13:20:30.411232  1 server_others.go:72] "Using iptables proxy"
```

### 📐 Kube-Proxy CIDR

```bash
kubectl get pods -n kube-system | grep -i kube-proxy
kubectl describe pod kube-proxy-bwtfb -n kube-system
```
The output shows the config is read from `/var/lib/kube-proxy/config.conf`, which is mounted from a **ConfigMap**:

```bash
kubectl get cm -n kube-system
kubectl describe cm kube-proxy -n kube-system | grep -i clusterCIDR
```
📝 Note down the CIDR — e.g., `10.240.0.0/16`.

---

## 🕸️ Weave-Net CNI Plugin

**Weave-Net** is a popular third-party CNI plugin that enables containers on **different nodes** to communicate with each other.

### 🧠 How Weave-Net Works

- Weave-Net deploys a **Weave-Agent** on every node in the cluster as part of its setup.
- Each agent **keeps track** of the IP addresses of every **Pod, Node, and Namespace** on its own node.
- Agents **share this information** with all other agents across the cluster.
- This lets every node's agent know exactly **where to send a packet** so it reaches the correct Pod.

### 📦 Packet Flow Between Pods on Different Nodes

When Pod-1 (on Node-1) sends a packet to Pod-2 (on Node-2):

```
Pod-1 (Node-1)
   → Weave-Agent on Node-1 encapsulates the packet
   → sent to Weave-Agent on Node-2
   → Node-2 decapsulates the packet
   → delivered to Pod-2 (Node-2)
```

### 🌐 Default IP Allocation

- Weave assigns the **`10.32.0.0/12`** range to the cluster by **default** for Pod IP allocation.
- A **different subnet** of this network is assigned to **each node** for allocating IPs to its own Pods.

### 🚀 Deploying Weave-Net

**Method 1 — Direct apply from the Weave Cloud service:**
```bash
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"
```
This deploys Weave-Net as a **Pod**, managed by a **DaemonSet**.

**Method 2 — Download and apply manually:**
```bash
wget https://github.com/weaveworks/weave/releases/download/v2.8.1/weave-daemonset-k8s.yaml
ls
# Output: weave-daemonset-k8s.yaml
```

### 🎛️ Customizing Weave-Net's IP Range

To make Weave-Net use the **same CIDR as kube-proxy's clusterCIDR** (instead of its default `10.32.0.0/12`):

1. Note the `clusterCIDR` value from the kube-proxy ConfigMap (see [Kube-Proxy CIDR](#-kube-proxy-cidr) above) — e.g., `10.240.0.0/16`.
2. Edit the downloaded `weave-daemonset-k8s.yaml` file.
3. For the container named **`weave`**, add an **`IPALLOC_RANGE`** environment variable set to that CIDR:

```yaml
containers:
  - name: weave
    command:
      - /home/weave/launch.sh
    env:
      - name: IPALLOC_RANGE
        value: 10.240.0.0/16
```

---

## 📝 Quick Recap

- **CNI** = standard defining how container runtimes and networking plugins talk to each other.
- Runtime handles namespaces + invoking plugins; **plugins handle IP assignment + ADD/DEL/CHECK**.
- Every **Pod** gets its own IP, can reach every Pod on its node, and can reach every Pod on other nodes **without NAT**.
- Kubelet finds the plugin via `--cni-conf-dir` and `--cni-bin-dir`, then invokes the binary for `add`/`del` operations.
- CNI has both **built-in** (bridge, IPVLAN, MACVLAN) and **third-party** (Calico, Flannel, Cilium, Weave) plugins.
- **Docker uses CNM, not CNI** — Kubernetes works around this by disabling Docker's networking and invoking the CNI plugin directly.
- Use `kubectl get no -o wide`, `ip a`, and `ip address show type bridge` to trace cluster networking on a node.
- Use `netstat -npl` to verify which ports control plane components (scheduler, etcd) are listening on.
- Use `route -n` on a worker node plus the CNI's `IPALLOC_RANGE` to trace the default Pod route.
- The **Service CIDR** comes from the kube-apiserver manifest (`--service-cluster-ip-range`); the **kube-proxy CIDR** comes from its ConfigMap.
- **Weave-Net** uses a per-node agent to encapsulate/decapsulate packets for cross-node Pod communication, and defaults to the `10.32.0.0/12` IP range unless overridden via `IPALLOC_RANGE`.
