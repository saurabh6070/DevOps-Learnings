# ☸️ Kubernetes: Static Provisioning, Dynamic Provisioning, and Storage Class

## 🧷 1. Static Provisioning

In **Static Provisioning**, the Cluster Administrator manually creates the storage in advance. 🛠️

**Flow:**
1. ☁️ Create the actual volume on the storage backend (e.g., a disk on AWS/GCP/Azure, or an NFS share).
2. 💾 Create a **Persistent Volume (PV)** in Kubernetes that points to this pre-created storage.
3. 📋 Create a **Persistent Volume Claim (PVC)** that binds to the PV.
4. 📦 Use the PVC in a **Pod** definition.

**Diagram:**
```
Remote Storage (manually created)
        │
        ▼
Persistent Volume (PV) ──bind──▶ Persistent Volume Claim (PVC) ──▶ Pod
```

### 📄 Example: Static Provisioning YAML

**💾 Persistent Volume:**
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-static-demo
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  gcePersistentDisk:
    pdName: my-precreated-gce-disk
    fsType: ext4
```

**📋 Persistent Volume Claim:**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-static-demo
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

**📦 Pod using the PVC:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-static-demo
spec:
  containers:
    - name: app
      image: nginx
      volumeMounts:
        - mountPath: "/data"
          name: static-storage
  volumes:
    - name: static-storage
      persistentVolumeClaim:
        claimName: pvc-static-demo
```

> ⚠️ **Drawback:** The Admin has to manually pre-create volumes on the remote storage/cloud every time a new PV is needed — not scalable for large/dynamic environments.

---

## ⚡ 2. Dynamic Provisioning

**Dynamic Provisioning** removes the need to manually pre-create storage. Volumes are created **on-demand**, automatically, at the time a PVC is created — using a **Storage Class**. 🚀

**Flow:**
1. 🏷️ Define a **Storage Class** with a provisioner (internal or external).
2. 📋 Create a **PVC** referencing that Storage Class.
3. 🤖 Kubernetes automatically provisions the volume on the backend AND creates the PV for you.
4. 📦 Use the PVC in a Pod.

**Diagram:**
```
StorageClass (provisioner defined)
        │
        ▼
PVC (references storageClassName) ──auto-creates──▶ PV + Remote Volume
        │
        ▼
       Pod
```

---

## 🏷️ 3. Storage Class

> **001 ✅** -> Storage Class is used to provision volumes on any other platform. Some of the storage classes have their internal provisioners like Portworx. In case of Storage Class, there is **no need to create any volume on remote Cloud** and **no need to create a Persistent Volume on Kubernetes**. Only the **Storage Class**, **Persistent Volume Claim**, and **Pod Definition** need to be applied.

So with Storage Class based (Dynamic) provisioning, you only apply **3 objects**:
1. 🏷️ StorageClass
2. 📋 PersistentVolumeClaim
3. 📦 Pod

Kubernetes + the provisioner handle creating the PV and the actual disk/volume behind the scenes.

### 002 📄 -> Storage Class Definition YAML

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: google-storage
provisioner: kubernetes.io/gce-pd
```

### 🧪 Full Working Example (Dynamic Provisioning using Storage Class)

**🏷️ Step 1: StorageClass**
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: google-storage
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard
  fstype: ext4
reclaimPolicy: Delete
volumeBindingMode: Immediate
```

**📋 Step 2: PersistentVolumeClaim (referencing the Storage Class)**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-dynamic-demo
spec:
  storageClassName: google-storage
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

**📦 Step 3: Pod using the PVC**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-dynamic-demo
spec:
  containers:
    - name: app
      image: nginx
      volumeMounts:
        - mountPath: "/data"
          name: dynamic-storage
  volumes:
    - name: dynamic-storage
      persistentVolumeClaim:
        claimName: pvc-dynamic-demo
```

> ✅ **Notice:** No PV is defined here — the PVC's `storageClassName: google-storage` triggers the `kubernetes.io/gce-pd` provisioner to automatically create the disk on GCP **and** the matching PV in Kubernetes.

---

## 🔌 4. Common Provisioners (examples)

| Icon | Provisioner | Platform |
|---|---|---|
| 🟦 | `kubernetes.io/gce-pd` | Google Cloud Persistent Disk |
| 🟧 | `kubernetes.io/aws-ebs` | AWS EBS |
| 🟦 | `kubernetes.io/azure-disk` | Azure Disk |
| ⬜ | `kubernetes.io/no-provisioner` | Local volumes (manual, no dynamic provisioning) |
| 🟪 | `pxd.portworx.com` | Portworx (internal provisioner) |

---

## ⚖️ 5. Static vs Dynamic Provisioning — Summary

| Aspect | 🧷 Static Provisioning | ⚡ Dynamic Provisioning (Storage Class) |
|---|---|---|
| Volume creation | Manual, done in advance on remote storage | Automatic, on-demand via provisioner |
| PV creation | Manual (Admin creates it) | Automatic (created by provisioner) |
| Objects to apply | PV + PVC + Pod | StorageClass + PVC + Pod |
| Scalability | 🔴 Low — needs pre-planning | 🟢 High — scales with demand |
| Use case | Predictable, fixed storage needs | On-demand, cloud-native, elastic storage needs |

---

## 🎯 Quick Recap
- 🧷 **Static** = You do the manual work (volume + PV) upfront.
- ⚡ **Dynamic** = Storage Class + provisioner does the work for you.
- 🏷️ **Storage Class** = The bridge that enables Dynamic Provisioning — no manual PV or cloud volume needed, just apply **StorageClass + PVC + Pod**. ✅
