# 🛠️ Kubelet Troubleshooting

> **Section:** Kubernetes Networking
> **Topic:** Systemd Logs & Container Runtime Socket Connectivity Issues

---

## 📌 Overview

Kubelet is the primary "node agent" that runs on every node in a Kubernetes cluster. It communicates with the container runtime (via the **CRI socket**) to create/manage containers, and it talks to the API server to receive Pod specs. When something goes wrong on a node — Pods stuck in `Pending`/`ContainerCreating`, a node showing `NotReady`, or networking not coming up — the kubelet (and the components around it) is almost always the first place to look.

Troubleshooting kubelet issues generally falls into two buckets, depending on **how the control plane was deployed**:

1. Control-plane components running as **static Pods** (typical `kubeadm` setup)
2. Control-plane components running as **systemd services**

---

## 🧩 1. Control-Plane Deployed as Pods (kubeadm setup)

When `kubeadm` is used to bootstrap the cluster, components like `kube-apiserver`, `kube-controller-manager`, and `kube-scheduler` run as **static Pods** inside the `kube-system` namespace on the control-plane node.

### ✅ Check Pod Status

```bash
kubectl get pods -n kube-system
```

This lists all control-plane and system Pods (API server, scheduler, controller-manager, etcd, kube-proxy, CoreDNS, etc.) along with their current status (`Running`, `CrashLoopBackOff`, `Pending`, etc.).

### 📄 Check Pod Logs

```bash
kubectl logs kube-apiserver-master -n kube-system
```

This pulls logs directly from the specified static Pod — useful for spotting crash reasons, certificate errors, port-binding failures, or connectivity issues to etcd.

> 💡 **Tip:** Replace `kube-apiserver-master` with the actual Pod name from `kubectl get pods -n kube-system` (the suffix is usually the node's hostname).

---

## ⚙️ 2. Control-Plane Deployed as systemd Services

Some clusters (especially ones set up manually / "the hard way") run control-plane components as native **systemd services** instead of Pods. In this case, `kubectl` can't help you check status, since the API server itself may be down — you need to go directly to the OS-level service manager.

### 🖥️ On the Master (Control-Plane) Node

```bash
service kube-apiserver status
service kube-controller-manager status
service kube-scheduler status
```

These confirm whether each control-plane component is active, failed, or stopped at the OS level.

### 🖥️ On the Worker Node

```bash
service kubelet status
service kube-proxy status
```

Since `kubelet` and `kube-proxy` run on **every node** (master and worker), checking their status on worker nodes tells you whether the node can register with the cluster and whether Pod networking/service routing (`kube-proxy`) is functioning.

### 📄 Check Logs via journalctl

```bash
sudo journalctl -u kube-apiserver
```

`journalctl -u <service-name>` pulls systemd logs for that specific unit. Swap `kube-apiserver` for any other service name to inspect it:

```bash
sudo journalctl -u kubelet
sudo journalctl -u kube-proxy
sudo journalctl -u kube-controller-manager
sudo journalctl -u kube-scheduler
```

> 💡 **Tip:** Add `-f` to follow logs live (`sudo journalctl -u kubelet -f`), or `--since "10 min ago"` to narrow the time window when debugging a recent failure.

---

## 🔌 3. Container Runtime Socket Connectivity Issues

A very common source of kubelet failures is the kubelet being unable to reach the **container runtime** (containerd, CRI-O, Docker via cri-dockerd, etc.) through its **CRI (Container Runtime Interface) socket**.

### 🔍 Common Symptoms

- Node stuck in `NotReady` state
- kubelet logs show errors like:
  - `Failed to connect to container runtime`
  - `context deadline exceeded`
  - `rpc error: code = Unavailable`
- Pods stuck in `ContainerCreating`

### 📂 Default CRI Socket Paths

| Runtime | Default Socket Path |
|---|---|
| containerd | `unix:///run/containerd/containerd.sock` |
| CRI-O | `unix:///var/run/crio/crio.sock` |
| Docker (via cri-dockerd) | `unix:///run/cri-dockerd.sock` |

### 🧪 How to Diagnose

```bash
# Check kubelet's configured container runtime endpoint
cat /var/lib/kubelet/kubeadm-flags.env

# Check kubelet service status
sudo systemctl status kubelet

# Follow kubelet logs live
sudo journalctl -u kubelet -f

# Verify the runtime socket file actually exists
ls -l /run/containerd/containerd.sock

# Verify the runtime service itself is healthy
sudo systemctl status containerd
```

### ✅ Common Fixes

- Restart the container runtime, then the kubelet:
  ```bash
  sudo systemctl restart containerd
  sudo systemctl restart kubelet
  ```
- Ensure `--container-runtime-endpoint` (or the kubeadm-generated flag) points to the **correct** socket path.
- Confirm the socket file has the right permissions and isn't stale after a runtime crash/reinstall.
- Check for cgroup driver mismatches between kubelet and the runtime (`systemd` vs `cgroupfs`) — a frequent cause of silent node registration failures.

---

## 🧭 4. General Troubleshooting Checklist

- [ ] `kubectl get nodes` — is the node `Ready`?
- [ ] `kubectl get pods -n kube-system` — are all system Pods `Running`?
- [ ] `sudo systemctl status kubelet` — is the kubelet service active?
- [ ] `sudo journalctl -u kubelet -f` — any repeating errors in the logs?
- [ ] `sudo systemctl status containerd` (or relevant runtime) — is the runtime healthy?
- [ ] Does the CRI socket path in kubelet's config match the runtime's actual socket?
- [ ] Any certificate expiry issues (common on older clusters)?

---

## 📝 Quick Reference — Command Cheat Sheet

| Purpose | Command |
|---|---|
| List control-plane Pods | `kubectl get pods -n kube-system` |
| View static Pod logs | `kubectl logs <pod-name> -n kube-system` |
| Check API server (systemd) | `service kube-apiserver status` |
| Check controller-manager (systemd) | `service kube-controller-manager status` |
| Check scheduler (systemd) | `service kube-scheduler status` |
| Check kubelet (worker node) | `service kubelet status` |
| Check kube-proxy (worker node) | `service kube-proxy status` |
| View systemd logs for a unit | `sudo journalctl -u <service-name>` |
| Follow logs live | `sudo journalctl -u kubelet -f` |
| Restart kubelet | `sudo systemctl restart kubelet` |

---

## 🎯 Key Takeaways

- Always identify **how the control plane was deployed** (Pods vs systemd) before choosing your troubleshooting approach.
- `kubectl` commands only work if the API server is reachable — when it isn't, drop to `service`/`systemctl` and `journalctl` on the node itself.
- Most "node NotReady" issues trace back to either the **kubelet service** or its connection to the **container runtime socket**.
- Always cross-check the CRI socket path configured in kubelet against the runtime's actual socket location.
