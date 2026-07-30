# 🌐 Kubernetes Networking — Ports & CNI Fundamentals

> A quick-reference study guide covering the network ports used by Kubernetes components, Linux networking commands for troubleshooting, and how to inspect the CNI (Container Network Interface) plugin configured on your cluster.

---

## 📌 1. Kubernetes Component Ports

Every Kubernetes component listens on a specific port for communication. Knowing these ports is essential for troubleshooting connectivity issues, configuring firewalls, and understanding cluster architecture.

### 🎛️ 1.1 Master (Control Plane) Node Ports

| Component | Port | Purpose |
|---|---|---|
| 🔑 **kube-apiserver** | `6443` | Main entry point for all cluster communication (kubectl, components, etc.) |
| 🗄️ **etcd-server** (client) | `2379` | Used for communication with `kube-apiserver`. This is the primary port through which etcd connects with all other control-plane components |
| 🔁 **etcd-server** (peer) | `2380` | Used for replication/communication between `etcd` instances across multiple Master Nodes |
| 🧩 **kubelet API** | `10250` | Optional — only relevant if a kubelet is also running on the Master Node |
| 📅 **kube-scheduler** | `10259` | Exposes scheduler's health/metrics endpoint |
| 🎮 **kube-controller-manager** | `10257` | Exposes controller-manager's health/metrics endpoint |

### 🖥️ 1.2 Worker Node Ports

| Component | Port | Purpose |
|---|---|---|
| 🧩 **kubelet API** | `10250` | Allows the control plane to communicate with the kubelet on the worker node |
| 🚪 **NodePort Services** | `30000 - 32767` | Range of ports used when exposing a Service externally via type `NodePort` |

> 💡 **Tip:** Memorizing this table is extremely useful for both real-world troubleshooting and certification exams (like CKA), where port-related questions are common.

---

## 🛠️ 2. Linux Networking Commands (for Node-Level Troubleshooting)

These standard Linux commands help inspect and configure networking at the node/OS level — useful when diagnosing Kubernetes networking issues at their root.

| Command | What it Does |
|---|---|
| `ip link` | Shows all network interfaces (links) on the machine along with their state (UP/DOWN) |
| `ip addr` | Displays IP addresses assigned to each network interface |
| `ip addr add 192.168.1.10/24 dev eth0` | Manually assigns an IP address `192.168.1.10/24` to interface `eth0` |
| `ip route` | Displays the routing table of the node |
| `arp` | Displays the ARP (Address Resolution Protocol) table — maps IP addresses to MAC addresses |
| `netstat -plnt` | Lists all listening TCP ports along with the process (`-p`) that owns them |

> ⚠️ **Note:** The correct flag combination is `netstat -plnt` (process, listening, numeric, TCP) — double-check flag order/typos when running this on your terminal.

---

## 🔍 3. Checking Status of Control-Plane Components

You can verify whether specific Kubernetes components are running as processes on a node using `ps -aux` combined with `grep`:

```bash
ps -aux | grep -i kubelet
ps -aux | grep -i kube-scheduler
ps -aux | grep -i kube-proxy
ps -aux | grep -i kube-api
```

📖 **Why this matters:** In clusters set up **without kubeadm** (e.g., "the hard way") or when troubleshooting a broken control plane, components may run as native Linux processes/services rather than pods. These commands confirm whether the relevant binaries are actively running.

---

## 🔌 4. CNI (Container Network Interface) — Inspecting Plugins

The **CNI** is the specification and set of plugins responsible for configuring network interfaces in Linux containers, enabling pod-to-pod communication across the cluster.

### 📂 4.1 Locating Available CNI Binaries

All CNI-supported binaries are stored at:

```bash
ls /opt/cni/bin/
```

**Example Output:**

```
bandwidth  dhcp   firewall  host-device  ipvlan    macvlan  ptp  static  tuning  vrf
bridge     dummy  flannel   host-local   loopback  portmap  sbr  tap     vlan
```

📖 **What this means:** This directory contains all the plugin binaries available to CNI — including IPAM plugins (`host-local`, `dhcp`), main network plugins (`bridge`, `macvlan`, `ipvlan`, `flannel`, `ptp`), and meta/utility plugins (`portmap`, `bandwidth`, `firewall`, `tuning`, `vrf`).

### 🗂️ 4.2 Identifying Which CNI Plugin is Actively Configured

To check **which** CNI plugin the cluster is currently configured to use:

```bash
ls /etc/cni/net.d/
```

**Example Output I:**
```
10-flannel.conflist
```

**Example Output II:**
```
10-weave.conflist
```

📖 **What this means:** The `/etc/cni/net.d/` directory holds the active configuration file(s) that tell Kubernetes which CNI plugin to use for networking. The filename itself (e.g., `10-flannel.conflist`, `10-weave.conflist`) usually reveals the plugin in use — in these examples, **Flannel** and **Weave** respectively.

### 🧬 4.3 Inspecting the CNI Configuration File

To find the **exact type** of the network plugin being used, inspect the contents of the config file and look at the `"type"` field inside the `plugins` section:

```bash
cat /etc/cni/net.d/10-flannel.conflist
```

**Sample Output (from Lab):**

```json
{
  "name": "cbr0",
  "cniVersion": "0.3.1",
  "plugins": [
    {
      "type": "flannel",
      "delegate": {
        "hairpinMode": true,
        "isDefaultGateway": true
      }
    },
    {
      "type": "portmap",
      "capabilities": {
        "portMappings": true
      }
    }
  ]
}
```

### 🧩 4.4 Breaking Down the Configuration

| Field | Meaning |
|---|---|
| `name` | Logical name of the network — here, `cbr0` (custom bridge 0) |
| `cniVersion` | Version of the CNI specification being used |
| `plugins[0].type` | Main network plugin — here it's `flannel`, confirming Flannel is the CNI in use |
| `delegate.hairpinMode` | Allows a pod to communicate with itself via its own Service IP |
| `delegate.isDefaultGateway` | Configures the bridge as the default gateway for pod traffic |
| `plugins[1].type` | Chained plugin — here `portmap`, which handles hostPort ↔ podPort mappings |
| `capabilities.portMappings` | Enables the `portmap` plugin to handle port mapping capability requests |

> ✅ **Key Takeaway:** CNI plugins can be **chained** — Kubernetes applies each plugin listed in the `plugins` array in order, allowing features like IP assignment, bridging, and port mapping to be combined modularly.

---

## 🧠 5. Quick Recap

- 🔑 Control plane and worker components each listen on **well-defined ports** — know them for troubleshooting and exams.
- 🛠️ Use standard **Linux `ip`/`arp`/`netstat` commands** to debug node-level networking.
- 🔍 Use `ps -aux | grep` to confirm whether control-plane components are running as processes.
- 📂 `/opt/cni/bin/` → holds all **available** CNI plugin binaries.
- 🗂️ `/etc/cni/net.d/` → holds the **active** CNI configuration in use by the cluster.
- 🧬 Inspecting the `.conflist` file reveals the exact plugin `type` and how plugins are chained together.

---

### 📚 Suggested Next Topics
- Kubernetes Service Networking (ClusterIP, NodePort, LoadBalancer)
- kube-proxy modes (iptables vs IPVS)
- Pod-to-Pod Networking Model & CNI plugin comparison (Flannel vs Calico vs Weave vs Cilium)
