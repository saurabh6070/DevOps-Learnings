# 📘 Kubernetes Storage Deep Dive with Ceph

## 🔧 1. Introduction
Kubernetes supports two major types of storage:
 - **Ephemeral Storage**: Temporary, tied to Pod lifecycle.
 - **Persistent Storage**: Long-lived, independent of Pod lifecycle.

We will also explore **Ceph Storage** integration with Kubernetes, including coupling and decoupling approaches, with YAML examples.

---

## ⚡ 2. Ephemeral Storage
Ephemeral storage exists only as long as the Pod exists.

### 🔹 Types
 - **EmptyDir**: Temporary storage created when Pod is scheduled. Deleted when Pod ends.
 - **ConfigMap**: Stores configuration data as key-value pairs.
 - **Secret**: Stores sensitive data securely.

### 🔹 Example: EmptyDir Deployment

#### 📦 What is `emptyDir`?

- `emptyDir` is a **temporary scratch disk** created fresh when a Pod is scheduled onto a node.
- It lives **inside the Pod's lifecycle** — created when the Pod starts, deleted when the Pod is removed.
- All **containers inside the same Pod** can read and write to it — they share it like roommates sharing a shelf.
- **Different Pods never share an `emptyDir`** — each Pod gets its own private copy.

```yaml
volumes:
  - name: shared-data
    emptyDir: {}          # empty scratch disk, lives and dies with the Pod
```

---

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-with-emptydir
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        volumeMounts:
        - name: emptydirvolume
          mountPath: /data1
      - name: ubuntu
        image: ubuntu
        volumeMounts:
        - name: emptydirvolume
          mountPath: /data2/
      volumes:
      - name: emptydirvolume
        emptyDir: {}
```

#### 🔄 What Happens with `replicas: 3`?

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3             # ← 3 Pods will be created
  template:
    spec:
      volumes:
      - name: scratch
        emptyDir: {}      # ← each Pod gets its OWN copy of this
      containers:
      - name: app
        image: my-app:1.0
        volumeMounts:
        - name: scratch
          mountPath: /tmp/data
```

#### What you actually get:

```
Deployment: my-app
│
├── Pod-1 (Node A)
│     └── emptyDir: /tmp/data  ← Pod-1's private disk
│
├── Pod-2 (Node B)
│     └── emptyDir: /tmp/data  ← Pod-2's private disk (DIFFERENT from Pod-1)
│
└── Pod-3 (Node C)
      └── emptyDir: /tmp/data  ← Pod-3's private disk (DIFFERENT from Pod-1 & 2)
```

> ✅ Each Pod gets its **own independent** `emptyDir`
> ❌ It is **NOT shared** across replicas

---

#### 👥 Containers in the Same Pod = Roommates Sharing the Same Disk

If your Pod has **multiple containers**, they **all share the same `emptyDir`**:

```yaml
spec:
  volumes:
  - name: shared-scratch
    emptyDir: {}
  containers:
  - name: writer
    image: writer-app:1.0
    volumeMounts:
    - name: shared-scratch
      mountPath: /data/out        # writes files here
  - name: reader
    image: reader-app:1.0
    volumeMounts:
    - name: shared-scratch
      mountPath: /data/in         # reads the same files
```

```
Pod-1
├── container: writer  → writes to /data/out
└── container: reader  → reads from /data/in
          ↕ (same emptyDir — they share it like roommates)
```

This is the classic **sidecar pattern** — e.g., one container writes logs, another ships them.

---

#### ✅ Quick Reference: What `emptyDir` Is and Is Not

| Statement | True / False |
|---|---|
| `emptyDir` is created when a Pod starts | ✅ True |
| `emptyDir` is deleted when a Pod is deleted | ✅ True |
| Containers in the **same Pod** share an `emptyDir` | ✅ True |
| Data in `emptyDir` survives a **container restart** (not Pod restart) | ✅ True |
| `emptyDir` is shared across **Pods in the same Deployment** | ❌ False |
| `replicas: 3` means 3 Pods share one `emptyDir` | ❌ False |
| `emptyDir` persists after the Pod is deleted | ❌ False |

---

#### 💡 When to Use `emptyDir`

| Use Case | Example |
|---|---|
| Temporary scratch space | Unpacking a zip, processing a file |
| Sharing data between sidecar containers | Log writer + log shipper in same Pod |
| Caching that doesn't need to persist | Downloaded model weights, compiled assets |
| Init container hands data to main container | Setup scripts writing config to `/config` |

---

#### ⚠️ When NOT to Use `emptyDir`

| Scenario | Use Instead |
|---|---|
| Data must survive Pod restarts | `PersistentVolumeClaim (PVC)` |
| Data must be shared across multiple Pods / replicas | `PVC with ReadWriteMany` or a shared storage solution |
| Data must survive node failures | `PVC` backed by network storage (EBS, NFS, etc.) |

---



## 📦 3. Persistent Storage
 - Persistent storage survives Pod restarts and rescheduling.

### 🔹 Core Concepts
 - Persistent Volume (PV): Defines storage capacity and backend.
 - Persistent Volume Claim (PVC): Pod requests storage by claim.
 - StorageClass: Enables dynamic provisioning of PVs.

### 🔹 Example: HostPath PVC example (PV + PVC + Pod yaml files below)


```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: local-pv
spec:
  capacity:
    storage: 5Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /mnt/data
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: local-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-using-pvc
spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - mountPath: "/usr/share/nginx/html"
      name: storage
  volumes:
  - name: storage
    persistentVolumeClaim:
      claimName: local-pvc
```

In the PersistentVolume spec, you have:

```yaml
hostPath:
  path: /mnt/data
```
  
 - This means the storage is coming directly from the node’s local filesystem at /mnt/data.
 - Kubernetes mounts that directory from the node into the Pod, so the Pod sees it as persistent storage.

#### 🔹 Important Notes
 - HostPath volumes are tied to the specific node where the Pod is scheduled.
 - If the Pod is rescheduled to another node, the data will not follow — because it’s bound to the local disk path of the original node.
 - This makes HostPath useful for testing or single-node clusters, but not recommended for production workloads.



### 🔹 Example: AWS EBS PVC example (Dynamic Provisioning, PV + PVC + Pod yaml files below)

 - Amazon Elastic Block Store (EBS) provides persistent block storage volumes for use with EC2 instances. In Kubernetes, EBS can be integrated as a PersistentVolume backend, allowing Pods to use durable cloud storage.

```yaml

## Step-1 : Install AWS EBS CSI driver:
kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-1.38"
kubectl get pods -n kube-system -l app.kubernetes.io/name=aws-ebs-csi-driver


## Step-2 : Create StorageClass (gp3):
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
allowVolumeExpansion: true
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer
parameters:
  type: gp3


## Step-3 : Create PVC:
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ebs-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: gp3


## Step-4 : Use PVC in Deployment:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pvdeploy
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mypv
  template:
    metadata:
      labels:
        app: mypv
    spec:
      containers:
      - name: shell
        image: centos
        command: ["/bin/bash", "-c", "sleep 10000"]
        volumeMounts:
        - name: mypd
          mountPath: "/tmp/persistent"
      volumes:
      - name: mypd
        persistentVolumeClaim:
          claimName: ebs-pvc
```


#### 🔹 Key Points
 - EBS volumes are zonal: they exist in a single Availability Zone. Pods must run in the same zone as the volume.
 - Dynamic provisioning: Kubernetes can automatically create/delete EBS volumes when PVCs are requested, using the AWS EBS CSI driver.
 - If an AWS cluster is managed manually, you need to install the CSI drivers as described above. In the case of managed control planes such as EKS, AKS, or GKE, there is no need to install CSI drivers manually, because they are already running in the backend and work without additional setup. - StorageClasses define the type of EBS volume (e.g., gp2, gp3, io1).
 - PVCs request storage from these StorageClasses, and Kubernetes provisions volumes accordingly.

---

## 📘 4. Kubernetes Storage Provisioning

---

### 4.1. Static Provisioning of Storage

In the first scenario (above example of emptyDir), the cluster administrator manually creates the Persistent Volume (PV) beforehand.
The administrator defines and provisions the storage resource explicitly.
After that, the user creates a Persistent Volume Claim (PVC).
Kubernetes then binds the PVC to an already available PV that matches the requirements.

### ✅ Key Points

- PV creation is manual and done in advance.
- Storage resources are pre-provisioned by the administrator.
- PVC simply requests and binds to an existing PV.
- This approach is called **Static Provisioning** because volumes already exist before they are requested.

---

### 4.2. Dynamic Provisioning of Storage

- In the second scenario (above example of EBS PVC), the administrator does not create any Persistent Volume (PV) manually.
- The user directly creates a Persistent Volume Claim (PVC).
- Kubernetes automatically provisions a PV on-demand based on the request.
- This is made possible through a **StorageClass**, which defines how storage should be dynamically created.

### ✅ Key Points

- No manual PV creation is required.
- PVC triggers automatic PV provisioning.
- The StorageClass acts as a template/configuration, specifying:
  - Provisioner type (e.g., AWS EBS, Azure Disk, etc.)
  - Storage parameters
- The dynamically created PV is automatically bound to the PVC.


---

## 📘 5. StorageClass and Provisioning Comparison

---

### 5.1. Role of StorageClass

A StorageClass is primarily used in dynamic provisioning.
It provides Kubernetes with instructions on:
- Which storage backend to use
- How to create the storage volume dynamically

Without a StorageClass, dynamic provisioning cannot happen.

---

## 5.2. Comparison: Static vs Dynamic Provisioning

| Aspect                | Static Provisioning                | Dynamic Provisioning               |
|-----------------------|------------------------------------|-------------------------------------|
| PV Creation           | Manual (by administrator)          | Automatic (by Kubernetes)           |
| Storage Timing        | Pre-provisioned                    | On-demand                           |
| StorageClass Required | No                                 | Yes                                 |
| Flexibility           | Limited                            | High                                |
| Operational Effort    | Higher (manual management)         | Lower (automated)                   |

---

## 5.3. Summary

- Static provisioning involves manual creation of storage resources before they are used.
- Dynamic provisioning automates storage creation using StorageClass, reducing administrative effort and improving scalability.
- StorageClass is typically defined only when dynamic provisioning is required, as it enables Kubernetes to automatically manage the storage lifecycle.


---

## 🗄️ 6. Ceph Storage Integration

### 🔹 What is Ceph?
 - Ceph is a distributed storage system providing:
 - Block storage (RBD).
 - Object storage (Ceph Object Gateway).
 - File storage (CephFS).
 - It is highly scalable and fault-tolerant.


## 🛠️ 7. Setting up Ceph Cluster in AWS
 - To use Ceph with Kubernetes:
 - Provision 3 EC2 instances (recommended for quorum).
 - Install Ceph packages (ceph, ceph-mon, ceph-osd, ceph-mgr).
 - Configure Ceph monitors and OSDs across the 3 nodes.
 - Verify cluster health:
```bash
ceph -s
```

## 🔄 8. Using Ceph in Kubernetes

### 🔹 Coupling Mode
PV directly references Ceph storage backend (tight coupling). Pod template specifies Ceph details.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ceph-secret
type: kubernetes.io/rbd
data:
  key: <base64-encoded-ceph-key>
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: ceph-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  rbd:
    monitors:
      - 10.0.0.1:6789
      - 10.0.0.2:6789
      - 10.0.0.3:6789
    pool: kube
    image: ceph-image
    user: admin
    secretRef:
      name: ceph-secret
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ceph-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-ceph-coupled
spec:
  containers:
  - name: app
    image: ubuntu
    volumeMounts:
    - mountPath: "/data"
      name: ceph-storage
  volumes:
  - name: ceph-storage
    persistentVolumeClaim:
      claimName: ceph-pvc
```

### 🔹 Decoupling Mode
Use StorageClass to abstract Ceph details. PVCs request storage dynamically without knowing backend.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ceph-secret
type: kubernetes.io/rbd
data:
  key: <base64-encoded-ceph-key>
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ceph-sc
provisioner: kubernetes.io/rbd
parameters:
  monitors: 10.0.0.1:6789,10.0.0.2:6789,10.0.0.3:6789
  pool: kube
  user: admin
  secretRef: ceph-secret
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ceph-pvc-decoupled
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: ceph-sc
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-ceph-decoupled
spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - mountPath: "/usr/share/nginx/html"
      name: ceph-storage
  volumes:
  - name: ceph-storage
    persistentVolumeClaim:
      claimName: ceph-pvc-decoupled
```
