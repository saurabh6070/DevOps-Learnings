# 👑 Upgrading the Kubernetes Master (Control-Plane) Node

> **Kubernetes Cluster Maintenance Series**

---

## 📖 Overview

Upgrading a Kubernetes cluster is done **component by component**, in a specific order, using the `kubeadm` tool. The **Master (Control-Plane) Node** must always be upgraded **before** any Worker Nodes.

This guide covers **two methods** to upgrade the Master Node:
- ✅ **Method 1** — A detailed, real-world walkthrough (Ubuntu/Debian, `apt`) with full command output.
- ✅ **Method 2** — A concise, step-by-step checklist form of the same process.

> ⚠️ **Golden Rule:** You can only upgrade **one minor version at a time** (e.g., `v1.28.x → v1.29.x`), and `kubeadm` itself must always be upgraded **first**, before any other component.

---

## 🧭 Pre-Upgrade Checklist

| Step | Purpose |
|------|---------|
| 🔍 Check OS type/release | Confirms package manager & repo compatibility |
| 📦 Check available `kubeadm` versions | Ensures you upgrade to a valid, supported version |
| 🔒 Unhold pinned packages | `kubeadm`, `kubelet`, `kubectl` are usually version-pinned (`hold`) to prevent accidental upgrades |

---

## 🥇 Method 1: Full Walkthrough (Ubuntu/Debian with `apt`)

### 1️⃣ Update the Package Index

```bash
sudo apt update
```

### 2️⃣ Check Available `kubeadm` Versions

```bash
sudo apt-cache madison kubeadm
```

**Sample Output:**
```
kubeadm | 1.28.7-1.1 | https://pkgs.k8s.io/core:/stable:/v1.28/deb  Packages
kubeadm | 1.28.6-1.1 | https://pkgs.k8s.io/core:/stable:/v1.28/deb  Packages
kubeadm | 1.28.5-1.1 | https://pkgs.k8s.io/core:/stable:/v1.28/deb  Packages
kubeadm | 1.28.4-1.1 | https://pkgs.k8s.io/core:/stable:/v1.28/deb  Packages
kubeadm | 1.28.3-1.1 | https://pkgs.k8s.io/core:/stable:/v1.28/deb  Packages
kubeadm | 1.28.2-1.1 | https://pkgs.k8s.io/core:/stable:/v1.28/deb  Packages
kubeadm | 1.28.1-1.1 | https://pkgs.k8s.io/core:/stable:/v1.28/deb  Packages
kubeadm | 1.28.0-1.1 | https://pkgs.k8s.io/core:/stable:/v1.28/deb  Packages
```

### 3️⃣ Unhold, Install, and Re-Hold `kubeadm`

Since `kubeadm` is typically **held** (pinned) to prevent unintended upgrades, you must **unhold** it, install the target version, then **hold** it again:

```bash
sudo apt-mark unhold kubeadm && \
sudo apt-get update && sudo apt-get install -y kubeadm='1.28.7-*' && \
sudo apt-mark hold kubeadm
```

### 4️⃣ Verify the `kubeadm` Version

```bash
kubeadm version
```

**Output:**
```
kubeadm version: &version.Info{Major:"1", Minor:"28", GitVersion:"v1.28.7",
GitCommit:"c8dcb00be9961ec36d141d2e4103f85f92bcf291", GitTreeState:"clean",
BuildDate:"2024-02-14T10:39:01Z", GoVersion:"go1.21.7", Compiler:"gc", Platform:"linux/amd64"}
```

### 5️⃣ Check the Upgrade Plan

```bash
sudo kubeadm upgrade plan
```

**Output:**
```
[upgrade/config] Making sure the configuration is correct:
[upgrade/config] Reading configuration from the cluster...
[upgrade/config] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
[preflight] Running pre-flight checks.
[upgrade] Running cluster health checks
[upgrade] Fetching available versions to upgrade to
[upgrade/versions] Cluster version: v1.28.0
[upgrade/versions] kubeadm version: v1.28.7
[upgrade/versions] Target version: v1.28.7
[upgrade/versions] Latest version in the v1.28 series: v1.28.7

Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
COMPONENT   CURRENT       TARGET
kubelet     2 x v1.28.0   v1.28.7

Upgrade to the latest version in the v1.28 series:

COMPONENT                 CURRENT   TARGET
kube-apiserver            v1.28.0   v1.28.7
kube-controller-manager   v1.28.0   v1.28.7
kube-scheduler            v1.28.0   v1.28.7
kube-proxy                v1.28.0   v1.28.7
CoreDNS                   v1.10.1   v1.10.1
etcd                      3.5.9-0   3.5.10-0

You can now apply the upgrade by executing the following command:

        kubeadm upgrade apply v1.28.7
```

> 💡 **Note:** If a newer minor release exists (e.g., `v1.29.2`), `kubeadm upgrade plan` will detect it but **fall back to the latest patch of the current minor series** (`stable-1.28`) since minor-version jumps must be done one at a time.

Below the plan, `kubeadm` also reports the **API group config versions** and whether a **manual config upgrade** is required:

| API Group | Current Version | Preferred Version | Manual Upgrade Required |
|-----------|------------------|--------------------|---------------------------|
| `kubeproxy.config.k8s.io` | v1alpha1 | v1alpha1 | ❌ No |
| `kubelet.config.k8s.io` | v1beta1 | v1beta1 | ❌ No |

### 6️⃣ Apply the Upgrade

```bash
kubeadm upgrade apply v1.28.7
```

This upgrades the **control-plane components** (`kube-apiserver`, `kube-controller-manager`, `kube-scheduler`, `kube-proxy`, `etcd`, `CoreDNS`).

### 7️⃣ Check Node Status

```bash
kubectl get nodes
```

**Output:**
```
NAME           STATUS                     ROLES           AGE   VERSION
controlplane   Ready,SchedulingDisabled   control-plane   38m   v1.28.0
node01         Ready                      <none>          37m   v1.28.0
```

> 📌 Notice the control-plane node shows `SchedulingDisabled` — `kubeadm upgrade` automatically **cordons** the node during the upgrade, and the `kubelet` version is **still old** because kubelet must be upgraded **separately**.

### 8️⃣ Unhold, Install, and Re-Hold `kubelet` & `kubectl`

```bash
sudo apt-mark unhold kubelet kubectl && \
sudo apt-get update && sudo apt-get install -y kubelet='1.28.7-*' kubectl='1.28.7-*' && \
sudo apt-mark hold kubelet kubectl
```

> ⚠️ **Version matching tip:** Always install the **same target version** for `kubelet` and `kubectl` that you applied for `kubeadm` (e.g., both `1.28.7-*`) to avoid version-skew issues.

### 9️⃣ Reload systemd & Restart Kubelet

```bash
sudo systemctl daemon-reload
sudo systemctl restart kubelet
```

### 🔟 Verify Node Status Again

```bash
kubectl get nodes
```

**Output:**
```
NAME           STATUS                        ROLES           AGE   VERSION
controlplane   NotReady,SchedulingDisabled   control-plane   39m   v1.28.7
node01         Ready                         <none>          39m   v1.28.0
```

> 📌 The control-plane node briefly shows `NotReady` while `kubelet` restarts and re-registers — this is expected and temporary.

### 1️⃣1️⃣ Uncordon the Node

Once the node is healthy again, mark it schedulable so Pods can be placed on it:

```bash
kubectl uncordon controlplane
```

**Output:**
```
node/controlplane uncordoned
```

### 1️⃣2️⃣ Final Verification

```bash
kubectl get nodes
```

**Output:**
```
NAME           STATUS   ROLES           AGE   VERSION
controlplane   Ready    control-plane   39m   v1.28.7
node01         Ready    <none>          39m   v1.28.0
```

✅ The **control-plane node** is now fully upgraded to `v1.28.7` and back in `Ready` state, while `node01` (the worker) remains on the older version — ready for its own upgrade next.

---

## 🥈 Method 2: Quick Reference Checklist

A condensed version of the same upgrade flow, useful as a quick-reference cheat sheet.

### 🧭 Step 0 — Check OS Type First

Always confirm your OS/distro before choosing package-manager commands (this example uses `apt-get` for Ubuntu/Debian-based systems):

```bash
cat /etc/release
```

### 📋 Upgrade Steps

| Step | Command | Purpose |
|------|----------|---------|
| 1️⃣ | `apt-get upgrade -y kubeadm=1.12.0-00` | Upgrade `kubeadm` to the target version |
| 2️⃣ | `kubeadm upgrade apply v1.13.4` | Apply the upgrade plan via `kubeadm` |
| 3️⃣ | `kubectl node list` | View node list & current `kubelet` version per node |
| 4️⃣ | `apt-get upgrade -y kubelet=1.12.0-00` | Upgrade the `kubelet` package |
| 5️⃣ | `systemctl restart kubelet` | Restart the `kubelet` service to apply the update |
| 6️⃣ | `kubectl node list` | Confirm `kubelet` version is upgraded on all Master nodes |
| 7️⃣ | `kubeadm upgrade apply v1.12.0` | Re-apply `kubeadm upgrade` (if repeating for a specific version) |
| 8️⃣ | `kubeadm upgrade plan` | Check current & latest available versions |

### 📋 What `kubeadm upgrade plan` Shows

Running this command lists the current and latest available versions of:

- ⚙️ **Kubeadm**
- 🏛️ **Control Plane components**
- 🗄️ **Etcd**
- 🧭 **CoreDNS**

---

## 📝 Quick Recap

- Always upgrade the **Master (Control-Plane) Node before Worker Nodes**.
- Upgrade **one minor version at a time** — `kubeadm` must always be upgraded first.
- Typical package flow: **unhold → install target version → hold** (for `kubeadm`, `kubelet`, and `kubectl`).
- Order of operations: **upgrade `kubeadm` → `kubeadm upgrade plan` → `kubeadm upgrade apply` → upgrade & restart `kubelet` → `uncordon` the node**.
- `kubeadm upgrade apply` automatically **cordons** the control-plane node; remember to **`kubectl uncordon`** it once the upgrade completes.
- Use `kubectl get nodes` (or `kubectl node list` in the legacy checklist) throughout the process to track node **STATUS** and **VERSION**.
- `kubeadm upgrade plan` reports version details for **Kubeadm**, **Control Plane components**, **Etcd**, and **CoreDNS**, plus whether any component configs require **manual upgrading**.
- Always match `kubelet` and `kubectl` versions to the applied `kubeadm`/control-plane version to avoid version skew.
