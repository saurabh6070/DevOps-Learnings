# ☸️ Kubernetes + 🐙 Ceph Storage — Setup, CSI Controller & PVC Integration

## 📘 1. What is Ceph?

**Ceph** is a distributed, software-defined storage system that provides:

| Interface | Icon | Type | K8s Usage |
|---|---|---|---|
| **RBD** (RADOS Block Device) | 🧱 | Block storage | `ReadWriteOnce` PVCs (databases, single-pod disks) |
| **CephFS** | 📁 | File storage (POSIX) | `ReadWriteMany` PVCs (shared storage across pods) |
| **RGW** (RADOS Gateway) | 🌐 | Object storage (S3/Swift compatible) | Buckets via `ObjectBucketClaim` |

### 🧩 Core Ceph Components

| Component | Icon | Role |
|---|---|---|
| **MON** (Monitor) | 🗺️ | Maintains cluster map & quorum (needs odd number, e.g. 3, 5) |
| **OSD** (Object Storage Daemon) | 💽 | Actually stores data on a disk; one OSD per disk/partition |
| **MGR** (Manager) | 📊 | Cluster metrics, dashboard, orchestration modules |
| **MDS** (Metadata Server) | 🗂️ | Required only for CephFS — manages file metadata |
| **RGW** (Gateway) | 🌐 | Optional — provides S3/Swift object API |

---

## 🏗️ 2. Setting Up a Ceph Cluster From Scratch (using `cephadm`)

> 💡 `cephadm` is the official, modern way to bootstrap and manage a Ceph cluster (containerized daemons, no manual package juggling).

### ✅ Step 1 — Prerequisites (on all nodes)

```bash
# 🐧 Ubuntu/Debian based nodes
sudo apt update && sudo apt install -y docker.io python3 lvm2 chrony
sudo systemctl enable --now docker
```

- 🖥️ At least 3 nodes recommended (1 admin/bootstrap node + others as MON/OSD hosts)
- 💽 Each OSD node needs at least one **raw, unformatted disk/block device**
- 🌐 Passwordless SSH between nodes (cephadm manages remote nodes via SSH)
- ⏰ Time sync (chrony/ntp) across all nodes — Ceph is sensitive to clock drift

### ✅ Step 2 — Install `cephadm` on the bootstrap node

```bash
curl --silent --remote-name --location https://github.com/ceph/ceph/raw/quincy/src/cephadm/cephadm
chmod +x cephadm
sudo ./cephadm add-repo --release quincy
sudo ./cephadm install
```

### ✅ Step 3 — Bootstrap the Cluster 🚀

```bash
sudo cephadm bootstrap --mon-ip <MONITOR_NODE_IP>
```

This single command:
- 🗺️ Creates the first **MON** + **MGR** daemon
- 🔑 Generates cluster SSH key & config (`/etc/ceph/ceph.conf`, keyring)
- 📊 Enables the **Ceph Dashboard** (prints URL + admin credentials)

### ✅ Step 4 — Add More Hosts to the Cluster

```bash
# Copy SSH key to each new node
ssh-copy-id -f -i /etc/ceph/ceph.pub root@<NODE_IP>

# Register the host in the cluster
ceph orch host add <NODE_NAME> <NODE_IP>
```

### ✅ Step 5 — Add OSDs (the actual storage disks) 💽

```bash
# List available raw disks across the cluster
ceph orch device ls

# Add ALL available devices as OSDs automatically
ceph orch apply osd --all-available-devices

# OR add a specific disk on a specific host
ceph orch daemon add osd <NODE_NAME>:/dev/sdb
```

### ✅ Step 6 — Verify Cluster Health 🩺

```bash
ceph -s
```
Look for: `health: HEALTH_OK` ✅

### ✅ Step 7 — Create Pools & Enable Interfaces

**🧱 For RBD (Block Storage):**
```bash
ceph osd pool create rbdpool 128
rbd pool init rbdpool
```

**📁 For CephFS (File Storage):**
```bash
ceph fs volume create cephfs
# This auto-creates the needed data + metadata pools and an MDS daemon
```

---

## 🔌 3. Integrating Ceph with Kubernetes

There are **two common approaches** 🛣️:

| Approach | Icon | Description |
|---|---|---|
| **A. External Ceph + `ceph-csi`** | 🔗 | Ceph cluster runs outside K8s (as set up above); K8s connects via the CSI driver |
| **B. Rook-Ceph Operator** | 🐙⚙️ | Ceph is deployed **inside** K8s itself and fully managed by the Rook operator (CRDs) |

This guide focuses on **Approach A** (external Ceph cluster + `ceph-csi`), since we just built the cluster manually above.

---

## ⚙️ 4. Deploying the Ceph-CSI Controller & Node Plugins

The **CSI (Container Storage Interface) driver** is what lets Kubernetes talk to Ceph.

### 🧩 CSI Architecture

```
        ☸️ Kubernetes API
               │
   ┌───────────┼─────────────────┐
   ▼                             ▼
🎛️ csi-rbdplugin-provisioner   📁 csi-cephfsplugin-provisioner
   (Deployment, central          (Deployment, central
    control-plane component:      control-plane component:
    Create/Delete/Attach volumes) Create/Delete volumes)
   │                             │
   ▼                             ▼
🖥️ csi-rbdplugin (DaemonSet)   🖥️ csi-cephfsplugin (DaemonSet)
   Runs on every node,            Runs on every node,
   mounts RBD volume              mounts CephFS volume
   into the Pod                  into the Pod
```

- **Provisioner** 🎛️ = a `Deployment` — talks to Ceph MONs to create/delete RBD images or CephFS subvolumes when PVCs are created/deleted.
- **Node plugin** 🖥️ = a `DaemonSet` — runs on every worker node, performs the actual mount/unmount into the Pod.

### ✅ Step 1 — Get Ceph Cluster Info

```bash
ceph mon dump          # 🗺️ get MON IPs
ceph auth get-key client.admin   # 🔑 get admin key
ceph fsid              # 🆔 get cluster FSID
```

### ✅ Step 2 — Create `ceph-csi-config` ConfigMap 🗺️

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ceph-csi-config
  namespace: ceph-csi
data:
  config.json: |-
    [
      {
        "clusterID": "<CEPH_CLUSTER_FSID>",
        "monitors": [
          "10.0.0.11:6789",
          "10.0.0.12:6789",
          "10.0.0.13:6789"
        ]
      }
    ]
```

### ✅ Step 3 — Create the Ceph Admin Secret 🔐

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: csi-rbd-secret
  namespace: ceph-csi
stringData:
  userID: admin
  userKey: "<ceph-auth-get-key-output>"
```

### ✅ Step 4 — Deploy Ceph-CSI Driver (RBD example) 🚀

```bash
# 📥 Clone the official ceph-csi repo manifests
git clone https://github.com/ceph/ceph-csi.git
cd ceph-csi/deploy/rbd/kubernetes

# 🎛️ Deploy the RBD provisioner (Deployment) + node plugin (DaemonSet) + RBAC
kubectl apply -f csi-provisioner-rbac.yaml
kubectl apply -f csi-nodeplugin-rbac.yaml
kubectl apply -f csi-rbdplugin-provisioner.yaml
kubectl apply -f csi-rbdplugin.yaml
```

✅ Verify:
```bash
kubectl get pods -n ceph-csi
# Expect: csi-rbdplugin-provisioner-xxxx (Deployment, e.g. 3 replicas)
#         csi-rbdplugin-<node1/2/3>      (DaemonSet, 1 per node)
```

---

## 🏷️ 5. Creating the StorageClass (Dynamic Provisioning via Ceph)

### 🧱 RBD (Block) StorageClass

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ceph-rbd-sc
provisioner: rbd.csi.ceph.com
parameters:
  clusterID: "<CEPH_CLUSTER_FSID>"
  pool: rbdpool
  imageFeatures: layering
  csi.storage.k8s.io/provisioner-secret-name: csi-rbd-secret
  csi.storage.k8s.io/provisioner-secret-namespace: ceph-csi
  csi.storage.k8s.io/node-stage-secret-name: csi-rbd-secret
  csi.storage.k8s.io/node-stage-secret-namespace: ceph-csi
reclaimPolicy: Delete
allowVolumeExpansion: true
```

### 📁 CephFS (File) StorageClass

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ceph-cephfs-sc
provisioner: cephfs.csi.ceph.com
parameters:
  clusterID: "<CEPH_CLUSTER_FSID>"
  fsName: cephfs
  csi.storage.k8s.io/provisioner-secret-name: csi-cephfs-secret
  csi.storage.k8s.io/provisioner-secret-namespace: ceph-csi
  csi.storage.k8s.io/node-stage-secret-name: csi-cephfs-secret
  csi.storage.k8s.io/node-stage-secret-namespace: ceph-csi
reclaimPolicy: Delete
```

---

## 📋 6. Creating the PVC (Dynamic Provisioning)

### 🧱 PVC using RBD (ReadWriteOnce — e.g., a database)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: rbd-pvc
spec:
  storageClassName: ceph-rbd-sc
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

### 📁 PVC using CephFS (ReadWriteMany — shared across pods)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: cephfs-pvc
spec:
  storageClassName: ceph-cephfs-sc
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
```

---

## 📦 7. Using the PVC in a Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-ceph-storage
spec:
  containers:
    - name: app
      image: nginx
      volumeMounts:
        - mountPath: "/data"
          name: ceph-storage
  volumes:
    - name: ceph-storage
      persistentVolumeClaim:
        claimName: rbd-pvc     # or cephfs-pvc for shared storage
```

✅ Once applied:
- The `csi-rbdplugin-provisioner` 🎛️ talks to Ceph MONs and creates an RBD image in `rbdpool`
- The `csi-rbdplugin` DaemonSet 🖥️ on the scheduled node mounts it into the Pod at `/data`
- PVC status → `Bound` 🔗

---

## 🩺 8. Verification & Troubleshooting Commands

```bash
kubectl get sc                          # 🏷️ list storage classes
kubectl get pvc                         # 📋 check PVC status (should be Bound 🔗)
kubectl get pv                          # 💾 check auto-created PV
kubectl describe pvc rbd-pvc            # 🔍 debug binding issues
kubectl get pods -n ceph-csi            # 🎛️ check provisioner/node-plugin health
ceph -s                                 # 🩺 overall Ceph cluster health
ceph osd tree                           # 💽 OSD status/layout
rbd ls rbdpool                          # 🧱 list RBD images created by PVCs
```

---

## 🎯 9. Quick Recap

| Step | Icon | Action |
|---|---|---|
| 1 | 🏗️ | Bootstrap Ceph cluster with `cephadm` |
| 2 | 🗺️➕💽 | Add MON hosts + OSD disks |
| 3 | 🧱📁 | Create pools (RBD) / CephFS volume |
| 4 | ⚙️ | Deploy `ceph-csi` provisioner (Deployment) + node plugin (DaemonSet) |
| 5 | 🗺️🔐 | Create ConfigMap (cluster info) + Secret (auth key) |
| 6 | 🏷️ | Create StorageClass pointing to `rbd.csi.ceph.com` / `cephfs.csi.ceph.com` |
| 7 | 📋 | Create PVC referencing the StorageClass |
| 8 | 📦 | Mount PVC into Pod — done! ✅ |

> 💡 **Note:** For an all-in-Kubernetes alternative (Ceph deployed *inside* the cluster and managed via CRDs), consider **Rook-Ceph** ⚙️🐙 — it automates most of the manual `cephadm` steps above using Kubernetes-native operators.
