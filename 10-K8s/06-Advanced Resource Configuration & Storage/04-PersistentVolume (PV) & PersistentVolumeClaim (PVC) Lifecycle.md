# ☸️ Kubernetes: PersistentVolume (PV) & PersistentVolumeClaim (PVC) Lifecycle 🆕 (Bound/Reclaim Policies)

## 📘 1. Overview

- 💾 **PersistentVolume (PV)** — A piece of storage in the cluster, provisioned either manually (Static) or dynamically (using a Storage Class).
- 📋 **PersistentVolumeClaim (PVC)** — A request for storage made by a user/Pod. It "claims" a PV that matches its requirements (size, access mode, storage class, etc.).
- 📦 A **Pod** consumes storage by referencing a PVC in its volume definition.

---

## 🔄 2. PV/PVC Lifecycle Stages

```
🅿️ Provisioning ──▶ 🔗 Binding ──▶ 📦 Using ──▶ 🗑️ Releasing ──▶ ♻️ Reclaiming
```

| Stage | Icon | Description |
|---|---|---|
| Provisioning | 🅿️ | PV is created — **Static** (manually) or **Dynamic** (via StorageClass) |
| Binding | 🔗 | A PVC is matched & bound 1:1 to a suitable PV |
| Using | 📦 | Pod mounts the PVC as a volume and reads/writes data |
| Releasing | 🗑️ | PVC is deleted, but PV still holds the data |
| Reclaiming | ♻️ | Based on `persistentVolumeReclaimPolicy` → Retain / Delete / Recycle |

---

## 🔗 3. Binding — PVC ↔ PV (`Bound` state)

Kubernetes binds a PVC to a PV when:
- ✅ The PV's capacity is **≥** the PVC's requested storage
- ✅ The `accessModes` match
- ✅ The `storageClassName` matches (or both are explicitly set to `""`)
- ✅ Optionally, an explicit `volumeName` (PVC side) or `claimRef` (PV side) is used to **force a 1:1 binding**

Once bound, the PVC/PV pair moves to the **`Bound`** ✅ status — visible via:
```bash
kubectl get pvc
kubectl get pv
```

### 🔒 Explicit 1:1 Binding Example

> **002 →** YAML file for Persistent Volume Claim (binds explicitly to `foo-pv` via `volumeName`):

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: foo-pvc
  namespace: foo
spec:
  storageClassName: ""   # 🚫 Empty string must be explicitly set, otherwise default StorageClass will be used
  volumeName: foo-pv
```

> **003 →** YAML file for Persistent Volume (binds explicitly to `foo-pvc` via `claimRef`):

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: foo-pv
spec:
  storageClassName: ""
  claimRef:
    name: foo-pvc
    namespace: foo
```

🔎 **Note:** Using `volumeName` (in PVC) + `claimRef` (in PV) together guarantees this PVC binds to **exactly this PV**, and no other PVC/PV can steal the binding.

---

## 🖴 4. HostPath Example — Full PV + PVC + Pod Flow

### 💾 Step 1 — Create the PersistentVolume (HostPath)

> **004 →** YAML file for Persistent Volume with HostPath:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-log
spec:
  capacity:
    storage: 100Mi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain      # ♻️ Reclaim Policy
  hostPath:
    path: /pv/log
```

### 📋 Step 2 — Create the PersistentVolumeClaim

> **005 →** YAML file for Persistent Volume Claim:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: claim-log-1
spec:
  volumeName: pv-log
  resources:
    requests:
      storage: 50Mi
  accessModes:
    - ReadWriteMany
```

➡️ Since `volumeName: pv-log` is explicitly set, this PVC will **directly bind** 🔗 to `pv-log` (as long as capacity & access modes are compatible).

### 📦 Step 3 — Create the Pod using the PVC

> **006 →** YAML file for Pod using the PVC:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hostpath-example-linux
spec:
  containers:
    - name: webapp
      image: kodekloud/event-simulator
      volumeMounts:
        - mountPath: /log
          name: myvol
          readOnly: true
  volumes:
    - name: myvol
      persistentVolumeClaim:
        claimName: claim-log-1
```

✅ At this point:
- `pv-log` → **Bound** 🔗 to `claim-log-1`
- `claim-log-1` → **Bound** 🔗, mounted read-only 🔒 at `/log` inside the Pod

---

## ⚠️ 5. Deletion Behavior — PVC Stuck in Terminating

> **007 →** If a Pod is attached to a PVC, and we try to delete the PVC, then the PVC will get **stuck in a `Terminating` ⏳ state** and the terminal will hang.
>
> ✅ **Fix:** Delete the **Pod** 📦 first.
> 👉 Once the Pod is deleted, the PVC will also get deleted.
> 👉 Depending on the **Reclaim Policy** defined on the PV:
> - If policy = `Retain` 🛡️ → PV moves to **`Released`** 🟡 state (data is preserved, but PV is not automatically reusable).

### 🧭 Deletion Flow Diagram

```
📦 Pod (using PVC) ──try delete PVC──▶ ⏳ PVC stuck in Terminating (hangs)
        │
        ▼ (Fix: delete Pod first)
🗑️ Pod deleted ──▶ 🗑️ PVC deleted ──▶ ♻️ Reclaim Policy applied on PV
                                              │
                        ┌─────────────────────┼─────────────────────┐
                        ▼                     ▼                     ▼
                  🛡️ Retain              🔥 Delete               🔄 Recycle
              PV → "Released" 🟡      PV & underlying        (deprecated)
              data kept, needs        storage deleted 🚫       wipes data,
              manual cleanup/reuse                              PV reusable
```

---

## ♻️ 6. Reclaim Policies Explained

| Policy | Icon | Behavior |
|---|---|---|
| **Retain** | 🛡️ | PV is **not deleted** — moves to `Released` 🟡 state. Data stays intact. Admin must manually clean up & re-create the PV to reuse it. |
| **Delete** | 🔥 | PV **and** the underlying storage (cloud disk, etc.) are **automatically deleted** 🚫 when the PVC is deleted. Common default for dynamically provisioned volumes. |
| **Recycle** | 🔄 *(Deprecated)* | Basic scrub (`rm -rf`) of volume data, then PV becomes available again for a new claim. ⚠️ No longer recommended — use Dynamic Provisioning instead. |

---

## 📊 7. PV/PVC Status Reference

| Status | Icon | Meaning |
|---|---|---|
| Available | 🟢 | PV is free, not yet bound to any PVC |
| Bound | 🔗 | PV is bound to a PVC (or vice versa) |
| Released | 🟡 | PVC deleted, but PV (with `Retain` policy) still holds data, not yet available for reuse |
| Failed | 🔴 | Automatic reclamation failed |
| Terminating | ⏳ | Deletion requested but blocked — usually because a Pod is still using the PVC |

---

## 🎯 8. Quick Recap

- 🔗 **Bound** = PVC successfully matched & linked to a PV (via matching criteria or explicit `volumeName`/`claimRef`).
- 📦 A Pod using a PVC **blocks PVC deletion** — always delete the Pod first.
- ♻️ **Reclaim Policy** decides what happens to the PV after its PVC is deleted:
  - 🛡️ `Retain` → PV → `Released`, data safe, manual action needed.
  - 🔥 `Delete` → PV & storage wiped automatically.
  - 🔄 `Recycle` → deprecated, avoid using.
