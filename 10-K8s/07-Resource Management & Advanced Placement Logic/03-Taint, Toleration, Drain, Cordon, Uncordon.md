# ☸️ Kubernetes: Taint, Toleration, Drain, Cordon, Uncordon

These are the core mechanisms used to **control which Pods can/cannot be scheduled on which Nodes**, and to safely **take Nodes out of service** for maintenance.

| Concept | Applied On | Purpose |
|---|---|---|
| 🚫 **Taint** | Node | Repels Pods from the Node |
| ✅ **Toleration** | Pod | Allows a Pod to "tolerate" a Node's taint |
| 🔒 **Cordon** | Node | Marks Node unschedulable (existing Pods stay) |
| 🚿 **Drain** | Node | Evicts existing Pods + marks unschedulable |
| 🔓 **Uncordon** | Node | Marks Node schedulable again |

---

## 1. 🚫 Taints and Tolerations

### 1.1 📌 Core Concept

- **Taint** is applied on a **Node**.
- **Toleration** is applied on a **Pod**.
- If a taint is applied on a Node with a specific key-value pair, then **Pods that don't have a matching toleration** for that same key-value pair **can never be scheduled** on that Node.

> Taints and Tolerations **do not** tell a Pod to go to a particular node — they only **restrict** which nodes will **reject** the pod. Scheduling *preference* is controlled separately by **Node Affinity**. (Taint/Toleration = "keep out unless allowed"; Node Affinity = "pod prefers to go here.")

### 1.2 ⌨️ Command Syntax

```bash
kubectl taint nodes <node-name> <key>=<value>:<taint-effect>
```

Example:
```bash
kubectl taint node node01 spray=mortein:NoSchedule
```

This means: *"Node01 is now tainted with `spray=mortein`. Any Pod without a matching toleration will NOT be scheduled here."*

### 1.3 ⚡ Taint Effects

A taint's `effect` controls **what happens** to Pods that don't tolerate it:

| Effect | Meaning |
|---|---|
| 🟡 `NoSchedule` | New Pods **without** toleration will **not** be scheduled on the node. Existing Pods already running are **not evicted**. |
| 🟠 `PreferNoSchedule` | **Soft** version — scheduler **tries to avoid** placing Pods here, but **will place them if no other option exists**. |
| 🔴 `NoExecute` | New Pods without toleration won't be scheduled, **AND existing Pods without toleration are evicted immediately** (unless they tolerate it, optionally with `tolerationSeconds`). |

### 1.4 ➖ Removing a Taint

Append a **trailing `-`** to the taint expression to remove it.

```bash
kubectl taint node node01 spray=mortein:NoSchedule-
```

### 1.5 🔍 Viewing Taints on a Node

```bash
kubectl describe node node01
kubectl describe node node01 | grep -i taint
```

Sample output:
```
Taints:  node-role.kubernetes.io/master:NoSchedule
```

### 1.6 👑 Removing the Default Master/Control-Plane Taint

By default, the control-plane node is tainted so normal workload Pods aren't scheduled on it. To allow scheduling on it (common in single-node lab/test clusters):

```bash
# Step 1: Check node name
kubectl describe node Node01

# Step 2: Find the taint
kubectl describe node Node01 | grep -i taint
# Output: Taints: node-role.kubernetes.io/master:NoSchedule

# Step 3: Remove it (note trailing "-")
kubectl taint node controlplane node-role.kubernetes.io/master:NoSchedule-
```

> ⚠️ Newer Kubernetes versions (1.24+) may use `node-role.kubernetes.io/control-plane:NoSchedule` instead of `.../master:NoSchedule` — always check with `describe` first rather than assuming the key.

---

## 2. ✅ Toleration YAML

### 2.1 📝 Generating a Base Pod YAML

```bash
kubectl run bee --image=nginx -o yaml > mypod.yaml
```

- Without `--dry-run=client`, this command **actually creates the Pod** in the cluster (and also dumps YAML) — the Pod gets created live before you even edit the file.
- With `--dry-run=client`, the Pod is **not created** — only the YAML manifest is generated locally. This is the recommended way to get a clean template:

```bash
kubectl run bee --image=nginx --dry-run=client -o yaml
kubectl run bee --image=nginx --dry-run=client -o yaml > bee.yml
```

Then edit it:
```bash
vi mypod.yaml
```

### 2.2 🧩 Toleration Field Structure

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: bee
  labels:
    run: bee
spec:
  containers:
  - name: bee
    image: nginx
  tolerations:
  - key: "spray"
    operator: "Equal"
    value: "mortein"
    effect: "NoSchedule"
```

This Pod can now be scheduled on `node01` (tainted `spray=mortein:NoSchedule`), **but it is not guaranteed** to land there — toleration just removes the repulsion; it doesn't attract the pod. Other untainted nodes remain equally valid options for the scheduler.

### 2.3 ❌ Common Errors When Writing Tolerations

**🐞 Error 1 — `tolerationSeconds` set with wrong effect**

```
The Pod "bee" is invalid: spec.tolerations[0].effect: Invalid value: "NoSchedule":
effect must be 'NoExecute' when `tolerationSeconds` is set
```

**Cause:** `tolerationSeconds` is only valid when `effect: NoExecute`. It has no meaning for `NoSchedule`/`PreferNoSchedule` because those effects never evict a running pod — there's nothing to "time out."

❌ Wrong:
```yaml
tolerations:
- key: "spray"
  operator: "Equal"
  value: "mortein"
  effect: "NoSchedule"
  tolerationSeconds: 3600     # ❌ invalid with NoSchedule
```

✅ Fixed:
```yaml
tolerations:
- key: "spray"
  operator: "Equal"
  value: "mortein"
  effect: "NoExecute"
  tolerationSeconds: 3600     # ✅ valid — pod stays 3600s after taint applied, then evicted
```

---

**🐞 Error 2 — `value` set while `operator: Exists`**

```
spec.tolerations[0].operator: Invalid value: core.Toleration{Key:"spray", Operator:"Exists",
Value:"mortein", Effect:"NoSchedule", TolerationSeconds:(*int64)(0xc00ecf1088)}:
value must be empty when `operator` is 'Exists'
```

**Cause:** When `operator: Exists`, Kubernetes only checks whether the **key** exists on the node (matching **any** value, or no value at all) — so specifying a `value` is contradictory and rejected.

❌ Wrong:
```yaml
tolerations:
- key: "spray"
  operator: "Exists"
  value: "mortein"          # ❌ must be empty/omitted with Exists
  effect: "NoSchedule"
```

✅ Fixed (Option A — use `Exists`, drop the value):
```yaml
tolerations:
- key: "spray"
  operator: "Exists"
  effect: "NoSchedule"
```

✅ Fixed (Option B — use `Equal`, keep the value):
```yaml
tolerations:
- key: "spray"
  operator: "Equal"
  value: "mortein"
  effect: "NoSchedule"
```

### 2.4 🔧 Toleration Operators

| Operator | Behavior |
|---|---|
| `Equal` (default) | Key **and** value must match exactly |
| `Exists` | Only key must exist on the node's taint (value ignored / must be omitted) |

### 2.5 🌐 Tolerate All Taints (Wildcard)

```yaml
tolerations:
- operator: "Exists"
```
> Omitting `key` entirely along with `operator: Exists` tolerates **every** taint on **every** node. Use very carefully — typically only for DaemonSets that must run everywhere (e.g., monitoring/log agents).

### 2.6 🛰️ Real-World Example — DaemonSet Tolerating Control-Plane Taint

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-monitor
  namespace: kube-system
spec:
  selector:
    matchLabels:
      app: node-monitor
  template:
    metadata:
      labels:
        app: node-monitor
    spec:
      tolerations:
      - key: "node-role.kubernetes.io/control-plane"
        operator: "Exists"
        effect: "NoSchedule"
      - key: "node-role.kubernetes.io/master"
        operator: "Exists"
        effect: "NoSchedule"
      containers:
      - name: monitor
        image: monitoring-agent:latest
```

### 2.7 🧱 Multiple Taints on One Node

A node can carry multiple taints. A Pod must tolerate **every** taint on the node to be scheduled there (tolerating just one of several is not enough).

```bash
kubectl taint node node01 spray=mortein:NoSchedule
kubectl taint node node01 env=prod:NoExecute
```

```yaml
tolerations:
- key: "spray"
  operator: "Equal"
  value: "mortein"
  effect: "NoSchedule"
- key: "env"
  operator: "Equal"
  value: "prod"
  effect: "NoExecute"
  tolerationSeconds: 300
```

---

## 3. 🛠️ Cordon, Drain, and Uncordon

These commands manage **node maintenance** — used when you need to patch, upgrade, or decommission a node without disrupting the cluster.

### 3.1 🔒 Cordon — Mark Node Unschedulable

```bash
kubectl cordon <node-name>
```

- Marks the node as `SchedulingDisabled`.
- **No new Pods** will be scheduled on it.
- **Existing Pods keep running** — nothing is evicted.
- This is essentially the *manual, permanent* equivalent of what a `NoSchedule` taint achieves — except cordon is a simple on/off switch applied via the API (sets `spec.unschedulable: true`) rather than a keyed taint.

```bash
kubectl get nodes
# node01   Ready,SchedulingDisabled   <none>   10d   v1.28.0
```

### 3.2 🚿 Drain — Safely Evict All Pods

```bash
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
```

- Automatically **cordons** the node first (implicit).
- **Evicts** all Pods gracefully (respecting PodDisruptionBudgets, honoring `terminationGracePeriodSeconds`).
- Pods managed by a ReplicaSet/Deployment/StatefulSet are **rescheduled onto other nodes**.
- Standalone Pods (not backed by a controller) will **block drain** unless you add `--force` (they'll simply be deleted, not rescheduled, since nothing manages them).

| Flag | Purpose |
|---|---|
| `--ignore-daemonsets` | Required if DaemonSet pods exist (they can't be evicted/moved — this flag lets drain proceed anyway) |
| `--delete-emptydir-data` | Required if any pod uses `emptyDir` volumes (data will be lost) |
| `--force` | Also deletes standalone (unmanaged) Pods |
| `--grace-period=<seconds>` | Override the pod's termination grace period |

Typical maintenance flow:
```bash
kubectl drain node01 --ignore-daemonsets --delete-emptydir-data --force
# ... perform OS patching / kubelet upgrade / hardware maintenance ...
kubectl uncordon node01
```

### 3.3 🔓 Uncordon — Re-enable Scheduling

```bash
kubectl uncordon <node-name>
```

- Marks the node schedulable again (`SchedulingDisabled` flag removed).
- **Does NOT automatically move Pods back** — new Pods can now land here, but pods drained earlier were already rescheduled elsewhere and won't "return."

---

## 4. ⚖️ Cordon/Drain vs Taint/Toleration — When to Use Which

| Scenario | Use |
|---|---|
| Temporary node maintenance (patch, reboot, decommission) | `cordon` + `drain` + `uncordon` |
| Permanently dedicate nodes to specific workloads (e.g., GPU nodes, dedicated tenants) | `taint` + matching `toleration` |
| Protect control-plane from regular workloads | Default master/control-plane taint |
| Evict pods when a node becomes unhealthy automatically | Built-in `NoExecute` taints (`node.kubernetes.io/not-ready`, `node.kubernetes.io/unreachable`) applied automatically by the node controller |

> Note: `cordon`/`drain` are **manual, imperative, one-time operational actions**. `taint`/`toleration` are **declarative, persistent scheduling rules** that remain in effect until explicitly removed.

---

## 5. 🤖 Built-in / Automatic Taints (Good to Know)

Kubernetes automatically applies certain `NoExecute` taints without any manual `kubectl taint` command:

| Taint | Applied When |
|---|---|
| `node.kubernetes.io/not-ready` | Node's kubelet reports NotReady |
| `node.kubernetes.io/unreachable` | Node controller can't reach the node |
| `node.kubernetes.io/memory-pressure` | Node is under memory pressure |
| `node.kubernetes.io/disk-pressure` | Node is under disk pressure |
| `node.kubernetes.io/pid-pressure` | Node is running out of process IDs |
| `node.kubernetes.io/network-unavailable` | Node's network is not configured |
| `node.kubernetes.io/unschedulable` | Node is cordoned (`kubectl cordon`) |

Pods can tolerate transient node issues briefly using `tolerationSeconds`, e.g., the default Kubernetes-injected toleration allows pods ~300 seconds of grace on `not-ready`/`unreachable` before eviction — preventing mass rescheduling storms during brief network blips.

---

## 6. 📋 Full Command Cheat-Sheet

```bash
# --- Taint ---
kubectl taint nodes <node> key=value:NoSchedule           # Add taint
kubectl taint nodes <node> key=value:NoSchedule-           # Remove taint
kubectl describe node <node> | grep -i taint               # View taints

# --- Toleration (in Pod spec, no direct kubectl command) ---
# Add "tolerations:" block under spec in Pod/Deployment YAML

# --- Cordon / Drain / Uncordon ---
kubectl cordon <node>                                       # Disable scheduling
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data   # Evict pods safely
kubectl uncordon <node>                                     # Re-enable scheduling

# --- Generate Pod YAML without creating it ---
kubectl run <pod-name> --image=<image> --dry-run=client -o yaml > pod.yaml

# --- Check node status/schedulability ---
kubectl get nodes
```

---

## 7. ✅ Summary

- **Taint** (Node) + **Toleration** (Pod) → controls **which pods are allowed** on a node; toleration ≠ attraction, it only removes repulsion.
- Taint effects: `NoSchedule` (block new), `PreferNoSchedule` (soft block), `NoExecute` (block new + evict existing).
- `tolerationSeconds` is valid **only** with `NoExecute`.
- `value` must be **empty** when `operator: Exists`.
- Use `kubectl taint node <name> key=value:effect-` (trailing `-`) to remove a taint — including the default master/control-plane taint.
- **Cordon** = stop new scheduling (no eviction). **Drain** = cordon + evict all pods gracefully. **Uncordon** = re-allow scheduling.
- Use taints/tolerations for **persistent, declarative** node-dedication rules; use cordon/drain for **one-time, imperative maintenance** operations.
- Kubernetes auto-applies certain `NoExecute` taints (`not-ready`, `unreachable`, etc.) to handle unhealthy nodes automatically.
