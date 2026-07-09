# ☸️ Kubernetes: Requests, Limits & LimitRange

## 📘 1. What are Requests & Limits?

| Term | Icon | Meaning |
|---|---|---|
| **Request** | 📥 | The **minimum** guaranteed amount of CPU/Memory a container is given. Used by the Scheduler 🧭 to decide which Node has enough room. |
| **Limit** | 🚧 | The **maximum** amount of CPU/Memory a container is **allowed** to use. Container is throttled (CPU) or killed/OOMKilled (Memory) if it crosses this. |

### 📄 Example: Pod with Requests & Limits

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: webapp-color
spec:
  containers:
    - name: webapp-color
      image: kodekloud/webapp-color
      resources:
        requests:
          memory: "1Gi"
          cpu: "1"
        limits:
          memory: "2Gi"
          cpu: "2"
```

---

## 🧮 2. CPU Units

> **002 →** `CPU=1` means **1000m** (millicores). ⚙️
> The **minimum** value of CPU that can be assigned to a Pod is **0.1**, which is equivalent to **100m**.

| CPU Value | Icon | Millicore Equivalent |
|---|---|---|
| `1` | 🟢 | `1000m` (1 full vCPU/core) |
| `0.5` | 🟡 | `500m` (half a core) |
| `0.1` | 🔵 | `100m` ⬅️ minimum assignable CPU |

---

## 💾 3. Memory Units

> **002 →** `Memory=256Mi` is equivalent to **268435456** bytes, or approximately **268M**.

### 📏 003 → Memory Conversions

| Unit | Icon | Type | Bytes |
|---|---|---|---|
| **1G** (Gigabyte) | 🟦 | Decimal (SI) | 1,000,000,000 bytes |
| **1M** (Megabyte) | 🟦 | Decimal (SI) | 1,000,000 bytes |
| **1K** (Kilobyte) | 🟦 | Decimal (SI) | 1,000 bytes |
| **1Gi** (Gibibyte) | 🟩 | Binary (IEC) | 1,073,741,824 bytes |
| **1Mi** (Mebibyte) | 🟩 | Binary (IEC) | 1,048,576 bytes |
| **1Ki** (Kibibyte) | 🟩 | Binary (IEC) | 1,024 bytes |

> ⚠️ **Tip:** `G`/`M`/`K` (decimal, SI) ≠ `Gi`/`Mi`/`Ki` (binary, IEC). Always double-check which one is used in your manifests — `256M` and `256Mi` are **not** the same value!

---

## 🧪 4. The Four Request/Limit Cases

> **004 →**

| # | Case | Icon | Behavior |
|---|---|---|---|
| 1 | **No Request, No Limit** | 🚫🚫 | ⚠️ Even **one Pod** can consume **all** the resources of the Node — risky, can starve other Pods. |
| 2 | **No Request, Limit Defined** | 🚫📥 / 🚧 | Kubernetes sets `Request = Limit` automatically. |
| 3 | **Request Defined, Limit Defined** | 📥🚧 | Resources are **strictly capped** for the Pod, even if more is available on the Node. |
| 4 | **Request Defined, No Limit** | 📥 ✅ | ⭐ **Best Practice.** Limit is effectively infinite ♾️ — Pod can burst and use spare Node capacity, **but** if a new Pod is scheduled and needs resources, the Request guarantee is honored and the "greedy" Pod is squeezed back down. |

### 🗺️ Visual Summary

```
Case 1: [No Req | No Limit] ────▶ 🐘 Pod can eat the WHOLE node
Case 2: [No Req | Limit=X ] ────▶ 📌 Request auto-set = Limit (X)
Case 3: [Req=A  | Limit=B ] ────▶ 🔒 Capped strictly between A and B
Case 4: [Req=A  | No Limit] ────▶ 🚀 Can burst up to node capacity, but
                                     guaranteed at least A always
```

---

## 🏷️ 5. LimitRange

> **005 →** `LimitRange` is an object which is applied at the **Namespace** 📛 level.

| Field | Icon | Meaning |
|---|---|---|
| `default` | 🚧 | → **defaultLimit** — Limit applied automatically if container doesn't specify one |
| `defaultRequest` | 📥 | → **defaultRequest** — Request applied automatically if container doesn't specify one |
| `max` | ⬆️ | → **maximumRequest** — Highest value any container's request/limit can be set to |
| `min` | ⬇️ | → **minimumRequest** — Lowest value any container's request/limit can be set to |

### 📄 Example: LimitRange for CPU

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: cpu-resource-constraint
  namespace: dev
spec:
  limits:
    - type: Container
      default:            # 🚧 defaultLimit
        cpu: "500m"
      defaultRequest:      # 📥 defaultRequest
        cpu: "300m"
      max:                 # ⬆️ maximumRequest
        cpu: "1"
      min:                 # ⬇️ minimumRequest
        cpu: "100m"
```

### 📄 Example: LimitRange for Memory

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: memory-resource-constraint
  namespace: dev
spec:
  limits:
    - type: Container
      default:
        memory: "512Mi"
      defaultRequest:
        memory: "256Mi"
      max:
        memory: "1Gi"
      min:
        memory: "128Mi"
```

> 🔎 **Note:** `LimitRange` only applies its defaults at **object creation time**. Changing a `LimitRange` does **not** retroactively affect already-running Pods. 🕑

---

## ✏️ 6. Editing Existing Pods & Deployments

> **007 →** We **cannot edit** specifications of an existing Pod, **except** for the following fields: ✅

```
spec.containers[*].image
spec.initContainers[*].image
spec.activeDeadlineSeconds
spec.tolerations
```

🚫 Everything else (like `resources.requests`/`resources.limits`) is **immutable** once the Pod is created.

### 🅰️ Option i — `kubectl edit pod` (quick, but tricky)

```bash
# 1️⃣ Try editing directly — opens in vi editor
kubectl edit pod webapp

# ❌ Saving fails for non-editable fields — a temp copy of your edits is saved:
#    e.g. /tmp/kubectl-edit-ccvrq.yaml

# 2️⃣ Delete the old pod
kubectl delete pod webapp

# 3️⃣ Create a new pod using your edited temp file
kubectl create -f /tmp/kubectl-edit-ccvrq.yaml
```

### 🅱️ Option ii — Export → Edit → Recreate (safer, more explicit)

```bash
# 1️⃣ Export current Pod spec to a YAML file
kubectl get pod webapp -o yaml > my-new-pod.yaml

# 2️⃣ Edit the exported file with vi (or any editor)
vi my-new-pod.yaml

# 3️⃣ Delete the existing pod
kubectl delete pod webapp

# 4️⃣ Create a new pod from the edited file
kubectl create -f my-new-pod.yaml
```

### 🚀 Editing Deployments (much easier!) 😌

With **Deployments** 📦🔁, you can freely edit **any** field/property in the Pod template. Since the Pod template is a **child spec** of the Deployment, Kubernetes will automatically:
1. 🗑️ Delete the old Pod(s)
2. ✨ Create new Pod(s) with the updated spec

```bash
kubectl edit deployment my-deployment
```

✅ No manual delete/recreate dance needed — the Deployment controller handles the rollout for you.

---

## 🎯 7. Quick Recap

| Concept | Icon | Key Takeaway |
|---|---|---|
| Request | 📥 | Minimum guaranteed resources — used for scheduling |
| Limit | 🚧 | Maximum allowed resources — enforced at runtime |
| CPU unit | ⚙️ | `1 CPU = 1000m`; minimum assignable = `100m` |
| Memory unit | 💾 | `Mi/Gi/Ki` = binary (1024-based); `M/G/K` = decimal (1000-based) |
| 4 Cases | 🧪 | No Req/No Limit ⚠️, No Req/Limit 📌, Req+Limit 🔒, Req only ⭐(best) |
| LimitRange | 🏷️ | Namespace-level defaults: `default`, `defaultRequest`, `max`, `min` |
| Editing Pods | ✏️ | Only `image`, `activeDeadlineSeconds`, `tolerations` are editable directly — else delete & recreate |
| Editing Deployments | 🚀 | Fully editable — `kubectl edit deployment` handles rollout automatically |
