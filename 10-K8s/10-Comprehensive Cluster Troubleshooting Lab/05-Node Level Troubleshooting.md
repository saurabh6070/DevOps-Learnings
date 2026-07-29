# 🖥️ Node Level Troubleshooting in Kubernetes

> **Section:** Kubernetes Networking → Cluster Troubleshooting
> **Focus:** Diagnosing and resolving CPU, Memory, and Disk pressure conditions on Nodes

---

## 📌 1. Why Node-Level Troubleshooting Matters

Every Pod in a Kubernetes cluster ultimately runs on a **Node**, and every Node is a finite pool of resources (CPU, memory, disk, PIDs). When a Node runs low on any of these resources, the **kubelet** protects the Node itself (and the workloads on it) by marking the Node with a **pressure condition** and, if needed, **evicting Pods**.

If you don't understand these conditions, you'll misdiagnose symptoms like:
- Pods stuck in `Pending` or `Evicted`
- Sudden Pod terminations with no application error
- Nodes marked `NotReady`
- Networking issues that are actually resource-starvation issues in disguise (e.g., kubelet or CNI plugin can't get CPU cycles to maintain node health/network routes)

Understanding node pressure is therefore a **prerequisite skill** before you troubleshoot networking issues — a Node under pressure can *look* like a network problem (dropped connections, DNS timeouts, slow kube-proxy updates) when the real cause is resource starvation.

---

## 🧠 2. How the Kubelet Monitors Node Health

The **kubelet** runs a background process called the **Node Problem Detector / eviction manager**, which periodically checks resource usage against configured thresholds and reports the results as **Node Conditions** — visible via:

```bash
kubectl describe node <node-name>
```

Under the `Conditions` section, you'll see entries like:

```
Type                 Status  Reason                       Message
----                 ------  ------                       -------
MemoryPressure       False   KubeletHasSufficientMemory   kubelet has sufficient memory available
DiskPressure          False   KubeletHasNoDiskPressure     kubelet has no disk pressure
PIDPressure           False   KubeletHasSufficientPID      kubelet has sufficient PID available
Ready                 True    KubeletReady                 kubelet is posting ready status
```

When `Status` flips to `True` for any pressure condition, the kubelet begins taking corrective action — including evicting Pods to reclaim resources.

---

## 🔥 3. The Three (Plus One) Pressure Conditions

### 💻 3.1 CPU Pressure

> **Note:** Unlike memory and disk, Kubernetes does **not** have a formal `CPUPressure` node condition. CPU is a *compressible* resource — the kernel's CFS scheduler simply throttles CPU-hungry processes instead of killing them. However, "CPU pressure" is still a very real, commonly discussed troubleshooting scenario, so it's covered here for completeness.

**Symptoms of CPU pressure:**
- High `CPU throttling` metrics (`container_cpu_cfs_throttled_periods_total`)
- Slow application response times
- Node `Ready` but workloads sluggish
- `kubectl top node` shows CPU usage near 100%

**How to check:**
```bash
kubectl top node <node-name>
kubectl top pod --all-namespaces --sort-by=cpu
```

**Common causes:**
- Missing or misconfigured Pod **CPU requests/limits**, causing "noisy neighbor" Pods to starve others
- Too many Pods scheduled on one Node (poor bin-packing)
- Node instance type undersized for the workload
- A runaway process (e.g., infinite loop, memory leak causing GC thrashing)

**Fixes:**
- Set appropriate **resource requests and limits** on all Pods
- Use **`ResourceQuota`** and **`LimitRange`** at the namespace level
- Enable **Horizontal Pod Autoscaler (HPA)** to scale workloads out
- Enable **Cluster Autoscaler** to add Nodes when CPU is consistently saturated
- Use **taints/tolerations** or **node affinity** to isolate CPU-intensive workloads

---

### 🧮 3.2 Memory Pressure (`MemoryPressure`)

**What it means:** Available memory on the Node has dropped below the configured eviction threshold.

**Default eviction threshold:**
```
memory.available < 100Mi
```
(configurable via kubelet flag `--eviction-hard`)

**How to check:**
```bash
kubectl describe node <node-name> | grep -A5 "MemoryPressure"
kubectl top node <node-name>
free -h                       # run directly on the node
```

**Symptoms:**
- Node condition `MemoryPressure=True`
- Pods evicted with reason `Evicted` and message `The node was low on resource: memory`
- OOMKilled containers (`kubectl describe pod` → `Last State: Terminated, Reason: OOMKilled`)
- Node becomes sluggish; system daemons (kubelet, container runtime) may also be starved

**Kubelet's eviction behavior when MemoryPressure = True:**
1. Stops scheduling new **BestEffort** Pods on that Node
2. Evicts Pods in this priority order:
   - `BestEffort` (no requests/limits set) — evicted first
   - `Burstable` (usage exceeding requests) — evicted next
   - `Guaranteed` (requests == limits) — evicted only as a last resort
3. Within the same QoS class, Pods using the most memory relative to their request are evicted first

**Common causes:**
- Memory leaks in application code
- No memory `limits` set → one Pod consumes all available memory
- Too many Pods packed onto a small Node
- Large in-memory caches or batch jobs without limits

**Fixes:**
- Always set `resources.requests.memory` and `resources.limits.memory`
- Use **Vertical Pod Autoscaler (VPA)** to right-size requests/limits automatically
- Investigate and patch memory leaks (use `kubectl top pod`, profiling tools)
- Add more Nodes / larger instance types, or enable Cluster Autoscaler
- Set namespace-level `LimitRange` defaults so no Pod is ever "unbounded"

---

### 💾 3.3 Disk Pressure (`DiskPressure`)

**What it means:** The Node's filesystem (root or imagefs) is running low on space or inodes.

**Default eviction thresholds:**
```
nodefs.available   < 10%
imagefs.available  < 15%
nodefs.inodesFree  < 5%
```

**How to check:**
```bash
kubectl describe node <node-name> | grep -A5 "DiskPressure"
df -h                          # disk space, run on the node
df -i                          # inode usage, run on the node
du -sh /var/lib/kubelet/*      # find what's eating space
du -sh /var/lib/docker/* # or /var/lib/containerd/*
```

**Symptoms:**
- Node condition `DiskPressure=True`
- Node marked as **unschedulable** for new Pods
- Existing Pods evicted to free disk space
- `kubectl` errors like `ImagePullBackOff` (no space to pull new images)
- `ephemeral-storage` limit breaches causing eviction with reason `Evicted — Ephemeral storage usage exceeds the limit`

**Common causes:**
- Accumulated **unused container images** on the Node
- Excessive **container logs** (no log rotation) filling `/var/log`
- Large **emptyDir** volumes or application writes without cleanup
- Orphaned volumes or crash-loop containers writing core dumps repeatedly
- Small disk allocated to worker Node relative to workload needs

**Fixes:**
- Enable/verify **kubelet garbage collection** (`--image-gc-high-threshold`, `--image-gc-low-threshold`)
- Configure **container log rotation** (`containerLogMaxSize`, `containerLogMaxFiles` in kubelet config)
- Set `resources.limits.ephemeral-storage` on Pods
- Regularly prune unused images: `crictl rmi --prune` or `docker image prune`
- Move heavy write workloads to dedicated **PersistentVolumes** instead of node-local disk
- Resize the Node's disk or use a storage-optimized instance type

---

### 🧩 3.4 PID Pressure (`PIDPressure`) — Bonus Condition

Often grouped with the above three, PID pressure occurs when a Node runs out of available **process IDs**, usually due to **fork bombs** or misbehaving containers spawning excessive processes.

```bash
kubectl describe node <node-name> | grep -A5 "PIDPressure"
```

**Fix:** Set `pod-max-pids` kubelet setting, and use resource-conscious base images/process managers.

---

## 🔍 4. Step-by-Step Node Troubleshooting Workflow

```
1. kubectl get nodes
   → Identify which node(s) show NotReady or SchedulingDisabled

2. kubectl describe node <node-name>
   → Check the "Conditions" block for Pressure=True
   → Check "Allocatable" vs "Allocated resources" section
   → Check "Events" at the bottom for eviction/GC events

3. kubectl top node <node-name>
   → Quick view of live CPU/Memory usage % (requires metrics-server)

4. kubectl get pods --all-namespaces -o wide --field-selector spec.nodeName=<node-name>
   → See all pods scheduled to the troubled node

5. kubectl get events --field-selector involvedObject.kind=Node --all-namespaces
   → View recent node-related events cluster-wide

6. SSH into the node (if accessible) for OS-level checks:
   - top / htop            → CPU & memory
   - free -h                → memory
   - df -h && df -i         → disk space & inodes
   - journalctl -u kubelet -f   → live kubelet logs
   - systemctl status kubelet   → is kubelet healthy?

7. Check container runtime health:
   - crictl ps               → running containers
   - crictl info              → runtime status
   - systemctl status containerd (or docker)
```

---

## 🧾 5. Reading `kubectl describe node` Output Effectively

Key sections to inspect:

| Section | What to Look For |
|---|---|
| **Conditions** | Any condition with `Status: True` other than `Ready` |
| **Capacity / Allocatable** | Total resources vs what's actually schedulable |
| **Allocated resources** | % of CPU/memory already requested by scheduled Pods |
| **Events** | `Evicted`, `NodeHasDiskPressure`, `NodeHasMemoryPressure`, `FreeDiskSpaceFailed`, `ImageGCFailed` |
| **Taints** | Kubernetes auto-applies taints like `node.kubernetes.io/memory-pressure:NoSchedule` when a condition fires |

**Auto-applied taints during pressure:**

| Condition | Taint Applied |
|---|---|
| MemoryPressure | `node.kubernetes.io/memory-pressure:NoSchedule` |
| DiskPressure | `node.kubernetes.io/disk-pressure:NoSchedule` |
| PIDPressure | `node.kubernetes.io/pid-pressure:NoSchedule` |
| NotReady | `node.kubernetes.io/not-ready:NoExecute` |
| Unreachable | `node.kubernetes.io/unreachable:NoExecute` |

These taints automatically prevent (or evict) Pods without any manual intervention — the scheduler and kubelet handle this natively.

---

## 🌐 6. Why This Matters for Kubernetes *Networking*

Node pressure conditions frequently masquerade as networking problems:

- **DiskPressure** → CNI plugin binaries/config can fail to write, or container runtime can't pull the CNI image → Pods stuck in `ContainerCreating` with network setup errors.
- **MemoryPressure** → `kube-proxy` or CNI daemonset pods (e.g., Calico, Cilium) get **OOMKilled**, breaking iptables/eBPF rule updates → intermittent Pod-to-Pod connectivity failures.
- **CPU pressure** → `kube-proxy` falls behind on syncing iptables/IPVS rules → stale Service endpoints → connections routed to dead Pods.
- **PIDPressure** → Networking sidecars (e.g., Envoy in a service mesh) fail to spawn worker threads.

**Rule of thumb:** Before deep-diving into DNS, CNI, or Service routing issues, always rule out node resource pressure first with `kubectl describe node`.

---

## 🛠️ 7. Useful Commands Cheat Sheet

```bash
# Node-level overview
kubectl get nodes -o wide
kubectl describe node <node-name>
kubectl top node

# Resource pressure specific
kubectl get nodes -o json | jq '.items[].status.conditions'
kubectl describe node <node-name> | grep -E "Pressure|Ready"

# Find evicted pods
kubectl get pods --all-namespaces --field-selector=status.phase=Failed
kubectl get pods --all-namespaces | grep Evicted

# Cleanup evicted pods (they don't self-delete)
kubectl get pods --all-namespaces --field-selector=status.phase=Failed \
  -o json | kubectl delete -f -

# Check kubelet configuration for eviction thresholds
cat /var/lib/kubelet/config.yaml | grep -A10 evictionHard

# Node-side OS diagnostics
df -h; df -i; free -h; top
journalctl -u kubelet -n 100 --no-pager
```

---

## ⚠️ 8. Common Pitfalls Students Should Know

- ❌ Forgetting that **CPU is compressible** (throttled, not evicted) while **memory/disk are incompressible** (Pods get killed/evicted).
- ❌ Not setting `requests`/`limits`, letting one Pod monopolize a Node.
- ❌ Ignoring `Evicted` Pods lingering in `kubectl get pods` — they consume etcd/API server resources and clutter dashboards until manually deleted.
- ❌ Assuming a `NotReady` Node is a networking-only issue without first checking pressure conditions.
- ❌ Not enabling **metrics-server**, which is required for `kubectl top` to work at all.
- ❌ Confusing **soft eviction thresholds** (grace period before eviction) with **hard eviction thresholds** (immediate eviction).

---

## ✅ 9. Quick Summary Table

| Condition | Resource | Compressible? | Kubelet Action | Key Command |
|---|---|---|---|---|
| CPU Pressure (informal) | CPU | ✅ Yes | Throttles processes (CFS) | `kubectl top node` |
| `MemoryPressure` | Memory | ❌ No | Evicts Pods (BestEffort → Burstable → Guaranteed) | `kubectl describe node` |
| `DiskPressure` | Disk / inodes | ❌ No | Garbage collects images, evicts Pods, blocks scheduling | `df -h`, `df -i` |
| `PIDPressure` | Process IDs | ❌ No | Blocks scheduling, may evict | `kubectl describe node` |

---

## 📚 10. Key Takeaways

1. Node conditions (`MemoryPressure`, `DiskPressure`, `PIDPressure`) are surfaced via `kubectl describe node` and drive automatic Pod eviction and taints.
2. CPU has no formal pressure condition — it's throttled, not evicted, because it's a compressible resource.
3. Kubelet evicts Pods in QoS order: **BestEffort → Burstable → Guaranteed**.
4. Always set resource `requests` and `limits` to prevent noisy-neighbor issues and make eviction behavior predictable.
5. Node pressure is a common **root cause hiding behind networking symptoms** — check node health before chasing CNI/DNS/Service bugs.
6. Use `kubectl top`, `describe node`, node-side OS tools (`df`, `free`, `journalctl`), and cluster autoscaling/VPA/HPA together as a complete troubleshooting and prevention toolkit.

---

*End of topic: Node Level Troubleshooting 🆕*
