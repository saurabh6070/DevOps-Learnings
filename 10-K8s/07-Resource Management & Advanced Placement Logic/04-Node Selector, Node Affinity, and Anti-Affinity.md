# ☸️ Kubernetes Pod Scheduling: NodeSelector, Node Affinity & Anti-Affinity

A practical guide to controlling **which nodes your pods land on** in Kubernetes.

---

## 📌 1. Overview

| Feature | 🎯 Purpose | 🧩 Flexibility |
|---|---|---|
| **nodeSelector** | Simple key-value node matching | ⭐ Basic |
| **Node Affinity** | Advanced, expressive node matching | ⭐⭐⭐ Advanced |
| **Pod Affinity / Anti-Affinity** | Schedule pods relative to *other pods* | ⭐⭐⭐ Advanced |

All three help the Kubernetes scheduler decide **where** a pod should run based on node labels (or pod co-location rules).

---

## 🏷️ 2. Node Labels — The Foundation

Everything starts with labeling nodes:

```bash
kubectl label nodes node-1 disktype=ssd
kubectl label nodes node-2 environment=production
kubectl get nodes --show-labels
```

---

## 🎯 3. nodeSelector — The Simple Way

`nodeSelector` is the simplest form of node selection — a plain key-value match.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-ssd
spec:
  containers:
  - name: nginx
    image: nginx
  nodeSelector:
    disktype: ssd
```

✅ **Pros**
- 🟢 Easy to write and understand
- 🟢 Great for simple use cases (e.g., "only run on SSD nodes")

❌ **Cons**
- 🔴 No support for `OR`, `NOT`, or ranges
- 🔴 No "soft" preference — it's all or nothing (pod stays `Pending` if no match)

---

## 🧠 4. Node Affinity — The Smarter Way

Node Affinity is a more expressive version of `nodeSelector`, supporting complex rules and **soft (preferred)** vs **hard (required)** scheduling.

### 🔑 Types

| Type | ⚙️ Behavior |
|---|---|
| `requiredDuringSchedulingIgnoredDuringExecution` | 🔒 **Hard rule** — must be satisfied to schedule the pod |
| `preferredDuringSchedulingIgnoredDuringExecution` | 🌤️ **Soft rule** — scheduler tries, but not mandatory |

> 💡 "IgnoredDuringExecution" means: if node labels change *after* the pod is running, the pod is **not evicted**.

### 🔒 Required Example (Hard Rule)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-required-affinity
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd
            - nvme
  containers:
  - name: nginx
    image: nginx
```

### 🌤️ Preferred Example (Soft Rule)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-preferred-affinity
spec:
  affinity:
    nodeAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 80
        preference:
          matchExpressions:
          - key: environment
            operator: In
            values:
            - production
  containers:
  - name: nginx
    image: nginx
```

⚖️ `weight` (1–100) determines priority when multiple soft rules exist — higher weight = stronger preference.

### 🧮 Supported Operators

| Operator | 📝 Meaning |
|---|---|
| `In` | Label value is in the list |
| `NotIn` | Label value is NOT in the list |
| `Exists` | Key exists (value ignored) |
| `DoesNotExist` | Key does not exist |
| `Gt` | Greater than (numeric) |
| `Lt` | Less than (numeric) |

---

## 🤝 5. Pod Affinity — Co-locate Pods

Schedules pods **close to** other pods (e.g., same node/zone as a related pod, like an app and its cache).

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - cache
        topologyKey: kubernetes.io/hostname
  containers:
  - name: web-app
    image: nginx
```

🗺️ `topologyKey` defines the "domain" of co-location:
- `kubernetes.io/hostname` → same node
- `topology.kubernetes.io/zone` → same availability zone

---

## 🚫 6. Pod Anti-Affinity — Spread Pods Apart

The opposite of pod affinity — **avoid** placing pods together. Commonly used for **high availability** 🌐 (spreading replicas across nodes/zones so one node failure doesn't kill your whole app).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - web-app
            topologyKey: kubernetes.io/hostname
      containers:
      - name: web-app
        image: nginx
```

✅ This ensures **no two `web-app` pods share the same node** — one pod per node, guaranteed.

### 🌤️ Soft Anti-Affinity (Preferred)

```yaml
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - web-app
              topologyKey: topology.kubernetes.io/zone
```

📍 Prefers spreading pods across **zones**, but won't block scheduling if it's not possible.

---

## ⚡ 7. Quick Comparison Cheat Sheet

| Feature | 🔧 Config Field | 🎯 Targets | 🔒 Hard | 🌤️ Soft |
|---|---|---|---|---|
| nodeSelector | `spec.nodeSelector` | Node labels | ✅ (only mode) | ❌ |
| Node Affinity | `spec.affinity.nodeAffinity` | Node labels | ✅ | ✅ |
| Pod Affinity | `spec.affinity.podAffinity` | Other pods' labels | ✅ | ✅ |
| Pod Anti-Affinity | `spec.affinity.podAntiAffinity` | Other pods' labels | ✅ | ✅ |

---

## 🛠️ 8. Handy Commands

```bash
# 🏷️ Label a node
kubectl label nodes <node-name> key=value

# ❌ Remove a label
kubectl label nodes <node-name> key-

# 🔍 View node labels
kubectl get nodes --show-labels

# 📋 Describe pod scheduling decisions
kubectl describe pod <pod-name>

# 🚦 Check why a pod is Pending
kubectl get events --field-selector involvedObject.name=<pod-name>
```

---

## 💡 9. Best Practices

- ✅ Prefer **`preferred...`** over `required...` unless you truly need a hard constraint — hard rules can leave pods stuck `Pending`.
- ✅ Use **Pod Anti-Affinity** for stateless replica spreading across nodes/zones (HA).
- ✅ Use **Node Affinity** instead of `nodeSelector` for anything beyond trivial matching.
- ⚠️ Avoid overly strict `requiredDuringScheduling` rules combined with anti-affinity in small clusters — pods may fail to schedule if there aren't enough nodes.
- 🧪 Always test scheduling rules with `kubectl describe pod` to confirm placement matches intent.

---

## 📚 10. Summary

- 🎯 **nodeSelector** → simplest, exact-match only
- 🧠 **Node Affinity** → smarter, supports `In/NotIn/Exists`, hard & soft rules
- 🤝 **Pod Affinity** → keep related pods together
- 🚫 **Pod Anti-Affinity** → spread pods apart for resilience & HA

> 🧭 Rule of thumb: Use **nodeSelector** for simple cases, **Node Affinity** for flexible node targeting, and **Pod Anti-Affinity** for spreading replicas across failure domains.
