# 📊 Kubernetes Resource Quotas 🆕 (Namespace-Level Restrictions)

## 1. 📦 What is a ResourceQuota?

A **ResourceQuota** is a Kubernetes API object, scoped at the **Namespace level**, that limits the **aggregate resource consumption** of all objects (mostly Pods) within that namespace.

- It doesn't limit a *single* Pod — that's the job of **LimitRange**.
- It limits the **sum total** across **all Pods/objects in the namespace**.
- Once a quota is applied, every Pod created in that namespace **must specify** `requests`/`limits` (if the quota tracks compute resources) — otherwise the Pod creation is **rejected**.

Think of it like a "budget" assigned to a team (namespace) — no matter how many people (Pods) are in the team, they all must collectively stay within the budget.

---

## 2. ❓ Why Do We Need ResourceQuotas?

| Problem Without Quota | Solved By Quota |
|---|---|
| One team/namespace can consume all cluster CPU/Memory | Caps total CPU/Memory per namespace |
| Unlimited number of Pods/Services/PVCs can be created | Caps object counts |
| No fairness across multi-tenant clusters | Enforces fair-share resource allocation |
| Noisy-neighbor problem | Isolates blast radius to one namespace |

---

## 3. 🔑 Key Concepts

### 3.1 🎯 Scope
- Applied **per Namespace**.
- A namespace can have **multiple ResourceQuota objects** (each targeting different resources/scopes).
- Total values across all quota objects in that namespace get summed and enforced.

### 3.2 🚧 What Can Be Restricted?

| Category | Examples |
|---|---|
| **Compute Resources** | `requests.cpu`, `limits.cpu`, `requests.memory`, `limits.memory` |
| **Storage Resources** | `requests.storage`, `persistentvolumeclaims`, storage-class-specific quotas |
| **Object Count** | `pods`, `services`, `configmaps`, `secrets`, `replicationcontrollers`, `services.loadbalancers`, `services.nodeports` |
| **Extended Resources** | `requests.nvidia.com/gpu` (custom/device resources) |

### 3.3 🔍 Quota Scopes (Advanced Filtering)
Quotas can be restricted further using **scopes**, so they apply only to a subset of Pods:

| Scope | Meaning |
|---|---|
| `Terminating` | Pods with `activeDeadlineSeconds >= 0` |
| `NotTerminating` | Pods without `activeDeadlineSeconds` |
| `BestEffort` | Pods with **no** requests/limits set (Best-Effort QoS) |
| `NotBestEffort` | Pods with at least one request/limit set |
| `PriorityClass` | Pods matching a specific `PriorityClass` (via `scopeSelector`) |
| `CrossNamespacePodAffinity` | Pods using cross-namespace pod affinity/anti-affinity |

---

## 4. ⚙️ How Enforcement Works

1. Admin creates a `ResourceQuota` object in a namespace.
2. Kubernetes **admission controller** (`ResourceQuota`) intercepts every new object creation request in that namespace.
3. It checks: *"If I allow this object, will the namespace exceed any quota?"*
4. If **yes** → request is **rejected** with an error like:
   ```
   Error from server (Forbidden): pods "myapp" is forbidden: exceeded quota:
   compute-quota, requested: limits.cpu=500m, used: limits.cpu=2, limited: limits.cpu=2
   ```
5. If **no** → object is created, and quota's `status.used` is updated.

⚠️ **Important:** If a `ResourceQuota` restricts `requests.cpu` / `requests.memory` / `limits.cpu` / `limits.memory`, then **every Pod created afterward MUST explicitly declare those values** — Kubernetes cannot enforce a quota against an "unbounded" Pod.

---

## 5. 🟢 Basic YAML Examples

### 5.1 📝 Example 1 — Simple Compute Quota

Restrict total CPU & Memory usage for namespace `dev`.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: dev
spec:
  hard:
    requests.cpu: "4"          # total CPU requested across all pods
    requests.memory: 8Gi        # total memory requested across all pods
    limits.cpu: "8"             # total CPU limit across all pods
    limits.memory: 16Gi         # total memory limit across all pods
```

Apply it:
```bash
kubectl apply -f compute-quota.yaml
kubectl describe resourcequota compute-quota -n dev
```

---

### 5.2 📝 Example 2 — Object Count Quota

Restrict the **number** of objects that can be created in a namespace.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: object-count-quota
  namespace: dev
spec:
  hard:
    pods: "10"
    services: "5"
    services.loadbalancers: "2"
    services.nodeports: "0"       # disallow NodePort services
    configmaps: "10"
    secrets: "10"
    persistentvolumeclaims: "4"
    replicationcontrollers: "5"
```

---

### 5.3 📝 Example 3 — Pod Failing Without Requests/Limits

If a quota exists on `requests.cpu`, this Pod **will be rejected**:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: no-limit-pod
  namespace: dev
spec:
  containers:
  - name: nginx
    image: nginx
    # ❌ No resources.requests/limits defined -> Rejected due to ResourceQuota
```

Correct version:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: with-limit-pod
  namespace: dev
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      requests:
        cpu: "250m"
        memory: "256Mi"
      limits:
        cpu: "500m"
        memory: "512Mi"
```

---

## 6. 🟡 Intermediate YAML Examples

### 6.1 💾 Storage Quota

Restrict PVC count and total storage requested, per StorageClass.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: storage-quota
  namespace: dev
spec:
  hard:
    requests.storage: 50Gi
    persistentvolumeclaims: "10"
    gold.storageclass.storage.k8s.io/requests.storage: 20Gi
    gold.storageclass.storage.k8s.io/persistentvolumeclaims: "4"
    bronze.storageclass.storage.k8s.io/requests.storage: 30Gi
```

> Format: `<storage-class-name>.storageclass.storage.k8s.io/<resource>`

---

### 6.2 📉 Quota With BestEffort Scope

Limit only Pods that have **no** requests/limits set (QoS class `BestEffort`).

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: besteffort-quota
  namespace: dev
spec:
  scopes:
  - BestEffort
  hard:
    pods: "5"
```

### 6.3 📈 Quota With NotBestEffort Scope (Guaranteed/Burstable Pods)

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: notbesteffort-quota
  namespace: dev
spec:
  scopes:
  - NotBestEffort
  hard:
    pods: "20"
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
```

---

## 7. 🔴 Advanced YAML Examples

### 7.1 🏆 Quota Scoped by PriorityClass (`scopeSelector`)

Only apply quota to Pods with `priorityClassName: high-priority`.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: high-priority-quota
  namespace: prod
spec:
  hard:
    pods: "10"
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
  scopeSelector:
    matchExpressions:
    - operator: In
      scopeName: PriorityClass
      values: ["high-priority"]
```

Companion low-priority restriction:

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: low-priority-quota
  namespace: prod
spec:
  hard:
    pods: "5"
    requests.cpu: "2"
    requests.memory: 4Gi
  scopeSelector:
    matchExpressions:
    - operator: In
      scopeName: PriorityClass
      values: ["low-priority"]
```

> This pattern is used to **guarantee capacity for critical workloads** while capping low-priority/batch workloads.

---

### 7.2 🎮 Quota for Extended Resources (GPUs)

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: gpu-quota
  namespace: ml-team
spec:
  hard:
    requests.nvidia.com/gpu: "4"
    limits.nvidia.com/gpu: "4"
```

---

### 7.3 🧩 Multiple ResourceQuota Objects in Same Namespace (Combined Enforcement)

You can split concerns into multiple quota objects — Kubernetes enforces **all of them simultaneously**.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
  namespace: prod
spec:
  hard:
    requests.cpu: "20"
    requests.memory: 40Gi
    limits.cpu: "40"
    limits.memory: 80Gi
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: object-counts
  namespace: prod
spec:
  hard:
    pods: "50"
    services: "20"
    secrets: "30"
    configmaps: "30"
    persistentvolumeclaims: "15"
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: terminating-quota
  namespace: prod
spec:
  scopes:
  - Terminating
  hard:
    pods: "10"
    requests.cpu: "5"
```

---

### 7.4 🏢 Full Enterprise-Style Multi-Tenant Setup

Combining **ResourceQuota + LimitRange** (best practice — quota alone forces every pod to declare resources, LimitRange provides sane defaults so devs aren't forced to calculate manually).

```yaml
# 1. Namespace
apiVersion: v1
kind: Namespace
metadata:
  name: team-alpha
---
# 2. ResourceQuota - namespace-wide caps
apiVersion: v1
kind: ResourceQuota
metadata:
  name: team-alpha-quota
  namespace: team-alpha
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "30"
    services: "10"
    persistentvolumeclaims: "10"
    requests.storage: 100Gi
---
# 3. LimitRange - default requests/limits per container (avoids rejection)
apiVersion: v1
kind: LimitRange
metadata:
  name: team-alpha-limits
  namespace: team-alpha
spec:
  limits:
  - type: Container
    default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "250m"
      memory: "256Mi"
    max:
      cpu: "2"
      memory: "2Gi"
    min:
      cpu: "100m"
      memory: "128Mi"
```

> With this combo: if a Pod doesn't declare resources, **LimitRange auto-injects defaults**, and **ResourceQuota** validates the totals against the namespace budget.

---

## 8. 🔎 Checking Quota Status

```bash
# List all quotas in a namespace
kubectl get resourcequota -n dev

# Detailed view (used vs hard limit)
kubectl describe resourcequota compute-quota -n dev
```

Sample output:
```
Name:            compute-quota
Namespace:       dev
Resource         Used   Hard
--------         ----   ----
limits.cpu       1500m  8
limits.memory    2Gi    16Gi
requests.cpu     750m   4
requests.memory  1Gi    8Gi
```

---

## 9. ✅ Best Practices

1. ✅ Always pair **ResourceQuota** with **LimitRange** — otherwise Pods without explicit requests/limits will fail to schedule.
2. ✅ Use **separate quota objects** for compute, storage, and object-counts for clarity.
3. ✅ Use `scopeSelector` with `PriorityClass` to protect critical workloads in multi-tenant clusters.
4. ✅ Monitor quota usage (`kubectl describe resourcequota`) to catch teams approaching their limits before failures occur.
5. ✅ Start with generous limits and tighten gradually based on observed usage (avoid Day-1 outages).
6. ✅ Combine with **Namespace-per-team** patterns for real multi-tenancy isolation.
7. ⚠️ Remember: ResourceQuota **does not** limit a single Pod's resource usage — that's LimitRange's job. Quota only caps the **namespace total**.

---

## 10. 📋 Quick Reference Cheat-Sheet

| kubectl Command | Purpose |
|---|---|
| `kubectl get resourcequota -n <ns>` | List quotas |
| `kubectl describe resourcequota <name> -n <ns>` | View used vs hard |
| `kubectl apply -f quota.yaml` | Create/update quota |
| `kubectl delete resourcequota <name> -n <ns>` | Remove quota |
| `kubectl explain resourcequota.spec` | Field reference |

---

## 11. 🏁 Summary

- **ResourceQuota** = Namespace-level guardrail on total resource consumption (compute, storage, object counts).
- Enforced via the **ResourceQuota admission controller** at object-creation time.
- Can be scoped further using `scopes` / `scopeSelector` (BestEffort, PriorityClass, Terminating, etc.).
- Should **always be paired with LimitRange** for smooth developer experience.
- Essential for **multi-tenant clusters**, preventing noisy-neighbor problems, and enforcing fair-share resource governance.
