# 🚀 Kubernetes Cluster Maintenance & Upgrades

> 📘 **Topic:** Master-Plane and Worker-Plane Upgrades (Sequential `kubeadm` Release Bumps)
> 🎯 **Audience:** Students learning Kubernetes cluster administration
> 📂 **Category:** Cluster Administration & Maintenance

---

## 📑 Table of Contents

1. [⏱️ POD Eviction Timeout](#️-pod-eviction-timeout)
2. [🖥️ Node OS Upgrades — Drain & Cordon](#️-node-os-upgrades--drain--cordon)
3. [⚠️ Common Drain Errors & Fixes](#️-common-drain-errors--fixes)
4. [🔢 Understanding Kubernetes Versioning](#-understanding-kubernetes-versioning)
5. [📊 Version Skew Policy](#-version-skew-policy)
6. [📦 Supported Versions & Upgrade Rules](#-supported-versions--upgrade-rules)
7. [👑 Upgrading the Master Node](#-upgrading-the-master-node)
8. [🔧 Upgrading Worker Nodes](#-upgrading-worker-nodes)
9. [✅ Verifying Cluster Version](#-verifying-cluster-version)
10. [📈 Counting Hosted Applications](#-counting-hosted-applications)
11. [🔍 Checking Available Upgrade Versions](#-checking-available-upgrade-versions)
12. [💾 Backing Up Resource Configurations](#-backing-up-resource-configurations)
13. [📝 Quick Recap](#-quick-recap)

---

## ⏱️ POD Eviction Timeout

- The **POD eviction timeout** is configured in the **`kube-controller-manager`**.
- ⌛ **Default value:** `5 minutes`
- This is the amount of time the **Master (control plane)** waits before it considers a POD as **dead**, if that POD has not returned to a `Running` state.

> 💡 **Why it matters:** This setting directly affects how quickly Kubernetes reacts to node failures — too short a timeout can cause unnecessary POD rescheduling, while too long a timeout delays recovery.

---

## 🖥️ Node OS Upgrades — Drain & Cordon

When performing an **OS upgrade** on a node, follow this checklist:

1. ✅ Check whether all PODs on that node are managed by a **ReplicaSet**, **ReplicationController**, or similar controller.
2. ✅ Confirm how many replicas of those PODs are running on **other nodes** (to avoid downtime).
3. 🚧 **Drain the node** — this gracefully evicts and reschedules all PODs onto other nodes.
4. 🔒 **Cordon the node** — this prevents the scheduler from placing any *new* PODs on it while maintenance is in progress.

### Commands

```bash
# Gracefully move all PODs off the node
kubectl drain node01

# Mark node as unschedulable (prevents new POD scheduling)
kubectl cordon node01

# --- Perform OS Upgrade here ---

# After the OS Upgrade is complete, make the node schedulable again
kubectl uncordon node01
```

> 📌 **Best Practice:** Always **drain** before an OS upgrade to avoid disrupting running workloads, and **cordon** to stop new workloads from landing on a node under maintenance.

---

## ⚠️ Common Drain Errors & Fixes

While draining nodes, you may run into the following issues 👇

### ❌ Error 1: DaemonSet-managed Pods

```
cannot delete DaemonSet-managed Pods (use --ignore-daemonsets to ignore)
```

✅ **Solution:**
```bash
kubectl drain node01 --ignore-daemonsets
```

### ❌ Error 2: Pods with no controller

```
error: unable to drain node "node01" due to error:
cannot delete Pods declare no controller (use --force to override): default/hr-app, continuing command...
```

🔎 **Cause:** This happens when a POD on the node is **not managed** by any controller (like a ReplicaSet or ReplicationController) — i.e., it's a standalone/bare POD.

✅ **Solution:**
```bash
kubectl drain node01 --ignore-daemonsets --force
```

> ⚠️ **Caution:** Using `--force` will delete standalone PODs permanently since they have no controller to recreate them.

---

## 🔢 Understanding Kubernetes Versioning

Kubernetes uses a **three-part version number**:

```
v1.11.3
 │  │  └── Patch version
 │  └───── Minor version
 └──────── Major version
```

| Segment | Example | Meaning |
|---------|---------|---------|
| **Major** | `1` | Major release / breaking changes |
| **Minor** | `11` | New features, backward-compatible |
| **Patch** | `3` | Bug fixes, security patches |

---

## 📊 Version Skew Policy

Most core components share the **same version** as the Kubernetes cluster itself:

- 🧩 `kube-apiserver`
- 🧩 `kube-controller-manager`
- 🧩 `kube-scheduler`
- 🧩 `kubelet`
- 🧩 `kube-proxy`
- 🧩 `kubectl`

However, some components are **versioned independently**:

- 🗄️ **Etcd Cluster**
- 🌐 **CoreDNS**

> 📖 Always check the **Release Notes** for detailed information on version-specific changes and modifications.

### 🎯 Version Skew Rules (Golden Rule)

At any point during an upgrade, the **`kube-apiserver`** must always be the **highest** version in the cluster — no component should ever be *ahead* of it.

Let **X** = version of `kube-apiserver` (e.g., `v1.10`)

| Component | Allowed Version Range |
|-----------|------------------------|
| **kube-apiserver** | `X` (e.g., `v1.10`) |
| **kube-controller-manager** & **kube-scheduler** | `X` or `X-1` (e.g., `v1.9` or `v1.10`) |
| **kubelet** & **kube-proxy** | `X`, `X-1`, or `X-2` (e.g., `v1.8`, `v1.9`, or `v1.10`) |

> 🧠 **Memory tip:** The further a component is from the API Server in the control flow, the more version lag it's allowed to have.

---

## 📦 Supported Versions & Upgrade Rules

- ✅ Kubernetes officially supports only the **latest three minor versions**.
  - Example: If `v1.15` is the latest release → supported versions are `v1.13`, `v1.14`, and `v1.15`.
- ⛔ **Do not skip versions** when upgrading — always upgrade **one minor version at a time**.
  - E.g., to go from `v1.12` → `v1.14`, you must upgrade `v1.12 → v1.13 → v1.14`.

---

## 👑 Upgrading the Master Node

> 🧭 First, check your OS type before proceeding (example below is for Ubuntu/Debian-based systems using `apt-get`).

```bash
# Step 1: Check OS release info
cat /etc/release

# Step 2: Upgrade kubeadm to the target version
apt-get upgrade -y kubeadm=1.12.0-00

# Step 3: Apply the upgrade plan using kubeadm
kubeadm upgrade apply v1.13.4

# Step 4: View node list & versions (kubelet version per node)
kubectl node list

# Step 5: Upgrade kubelet
apt-get upgrade -y kubelet=1.12.0-00

# Step 6: Restart kubelet service
systemctl restart kubelet

# Step 7: Confirm kubelet version is upgraded on all Master nodes
kubectl node list

# Step 8: Apply kubeadm upgrade (if repeating for a specific version)
kubeadm upgrade apply v1.12.0

# Step 9: Check the current & latest available versions
kubeadm upgrade plan
```

> 📋 `kubeadm upgrade plan` lists the **current/latest version** of:
> - Kubeadm
> - Control Plane components
> - Etcd
> - CoreDNS

---

## 🔧 Upgrading Worker Nodes

```bash
# Step 1: Drain the worker node (move workloads off it)
kubectl drain node-01

# Step 2: Upgrade kubeadm on the worker node
apt-get upgrade -y kubeadm=1.12.0-00

# Step 3: Upgrade kubelet on the worker node
apt-get upgrade -y kubelet=1.12.0-00

# Step 4: Update the kubelet configuration to the new version
kubeadm upgrade node config --kubelet-version v1.12.0

# Step 5: Restart kubelet service
systemctl restart kubelet

# Step 6: Uncordon the node to allow scheduling again
kubectl uncordon node-01
```

> 🔁 **Order matters:** Always **drain → upgrade → uncordon** for each worker node, one at a time, to maintain high availability.

---

## ✅ Verifying Cluster Version

```bash
kubectl get nodes
```

- 🖥️ All **Master** and **Worker** nodes should show the **same version** in the output.
- 📌 This uniform version represents the **overall Cluster Version**.

---

## 📈 Counting Hosted Applications

To determine the number of applications hosted on a cluster:

> ➕ **Total = Deployment objects + ReplicaSet objects + (other controller objects...)**

⚠️ **Important:** Do **not** count individual **PODs** separately — PODs are created *by* these higher-level objects (Deployments, ReplicaSets, etc.), so counting them too would result in double-counting.

---

## 🔍 Checking Available Upgrade Versions

To check what is the latest version available to upgrade `kubeadm` to:

```bash
sudo kubeadm upgrade plan
```

---

## 💾 Backing Up Resource Configurations

Before performing any upgrade or major change, it's a best practice to **back up all resource configs** across the entire cluster:

```bash
kubectl get all --all-namespaces -o yaml > Backup_all_namespaces.yaml
```

> 🛡️ **Why:** This backup ensures you have a full snapshot of all cluster resources (across every namespace) that can be used to restore or audit configurations if something goes wrong during the upgrade.

---

## 📝 Quick Recap

| ✅ Task | 🛠️ Command |
|---------|-------------|
| Drain a node | `kubectl drain <node> --ignore-daemonsets --force` |
| Cordon a node | `kubectl cordon <node>` |
| Uncordon a node | `kubectl uncordon <node>` |
| Check upgrade plan | `kubeadm upgrade plan` |
| Apply upgrade | `kubeadm upgrade apply <version>` |
| Check cluster version | `kubectl get nodes` |
| Backup all resources | `kubectl get all --all-namespaces -o yaml > backup.yaml` |

### 🎓 Key Takeaways
- 🕐 Default POD eviction timeout = **5 minutes**.
- 🧩 Always **drain + cordon** before OS upgrades, then **uncordon** after.
- 📈 `kube-apiserver` version must **never** be lower than any other control plane component.
- 🚫 Never **skip** a minor version during upgrades.
- 💾 Always take a **backup** before upgrading!

---

*📚 End of notes — practice these commands in a test cluster before applying them in production!*
