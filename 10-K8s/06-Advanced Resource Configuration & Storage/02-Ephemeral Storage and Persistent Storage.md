# 💽 Ephemeral Storage vs Persistent Storage in Kubernetes

---

## 📖 1. Overview

Kubernetes offers different ways to provide storage to Pods and containers, broadly grouped into two categories:

- ⚡ **Ephemeral Storage** — tied to the lifecycle of the Pod; data is lost when the Pod is deleted or rescheduled
- 🗄️ **Persistent Storage** — exists independently of the Pod's lifecycle; data survives Pod restarts, deletions, and rescheduling

Choosing the right storage type depends on whether the application needs data to survive beyond the life of a single Pod.

---

## ⚡ 2. Ephemeral Storage

### 2.1 📌 What is Ephemeral Storage?

Ephemeral storage is **temporary** storage that exists only as long as the Pod it belongs to is running. Once the Pod is deleted, restarted on a different node, or crashes and is rescheduled, the data stored in ephemeral volumes is **permanently lost**.

**🔑 Key characteristics:**
- 🔗 Bound to the Pod's lifecycle
- 🚫 Not suitable for critical or long-term data
- 🤝 Useful for scratch space, caching, or sharing data between containers in the same Pod
- ⚙️ Simple to configure — no external provisioning required

**🧩 Common types of ephemeral storage:**
- 📂 `emptyDir`
- 🖥️ `hostPath`
- ⚙️ `configMap`
- 🔐 `secret`
- 💿 `downwardAPI`

---

### 2.2 📂 EmptyDir

`emptyDir` is a temporary directory created **when a Pod is assigned to a node**, and it exists **as long as that Pod runs on that node**.

**🔑 Key characteristics:**
- 📁 Starts out empty — hence the name `emptyDir`
- 🤝 All containers within the same Pod can read from and write to the same `emptyDir` volume, making it useful for sharing files between containers
- 💾 Can be backed by the node's disk, or by memory (`medium: Memory`) for faster, RAM-based storage
- ❌ Data is **permanently deleted** when the Pod is removed from the node — whether the Pod is deleted, evicted, or crashes irrecoverably
- 🔄 Data **survives container restarts** within the same Pod (but not Pod deletion)

**🎯 Common use cases:**
- 🗃️ Temporary scratch space for computations
- 🔀 Sharing data/files between multiple containers in the same Pod (sidecar patterns)
- 🧠 Checkpointing long computations for recovery from crashes (within the same Pod)

---

### 2.3 🖥️ HostPath

`hostPath` mounts a file or directory **from the host node's filesystem** directly into a Pod. Unlike `emptyDir`, the data isn't necessarily cleared when the Pod is deleted — it depends on what happens to the underlying host path.

**🔑 Key characteristics:**
- 📍 Mounts an existing path on the **node**, not a Kubernetes-managed volume
- ⚠️ Data persists on that specific node, but if the Pod is rescheduled to a **different node**, the data won't follow it — making it unreliable for true persistence across the cluster
- 🔓 Can pose security risks since it gives Pods access to the host filesystem
- 🛠️ Supports an optional `type` field (`Directory`, `File`, `DirectoryOrCreate`, `FileOrCreate`, etc.) to validate what should exist at the path before mounting

**🎯 Common use cases:**
- 📊 Accessing node-level resources (e.g., Docker internals, node logs)
- 🧰 Running node-monitoring or node-level agents (e.g., DaemonSets)

**📄 Example YAML — Using HostPath:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hostpath-example-linux
spec:
  os:
    name: linux
  nodeSelector:
    kubernetes.io/os: linux
  containers:
  - name: example-container
    image: registry.k8s.io/test-webserver
    volumeMounts:
    - mountPath: /foo
      name: example-volume
      readOnly: true
  volumes:
  - name: example-volume
    # mount /data/foo, but only if that directory already exists
    hostPath:
      path: /data/foo   # directory location on host
      type: Directory   # this field is optional
```

**🔍 Breakdown of the example:**
- 🐧 `os.name: linux` and `nodeSelector` ensure the Pod is scheduled onto a Linux node
- 📦 The container `example-container` mounts the volume `example-volume` at `/foo` inside the container, in **read-only** mode
- 🗂️ The volume `example-volume` uses `hostPath` to point to `/data/foo` on the host node
- ✅ The `type: Directory` field tells Kubernetes to only mount the path if `/data/foo` **already exists** as a directory on the host — if not, the Pod will fail to start

---

## 🗄️ 3. Persistent Storage

### 3.1 📌 What is Persistent Storage?

Persistent storage provides data that **outlives the Pod**. Even if a Pod is deleted, crashes, or is rescheduled to a different node, the data remains intact and can be reattached to a new Pod.

**🔑 Key characteristics:**
- 🔄 Decoupled from the Pod's lifecycle
- 🌐 Data can be reattached across different Pods and nodes
- 🏗️ Backed by external or networked storage systems (cloud disks, NFS, SAN, etc.)
- 🔒 Suitable for databases, stateful applications, and any data that must survive restarts

**🧩 Core building blocks:**
- 🧱 **PersistentVolume (PV)**
- 📝 **PersistentVolumeClaim (PVC)**
- 🏷️ **StorageClass**

---

### 3.2 🧱 PersistentVolume (PV)

A **PersistentVolume** is a piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned using a StorageClass. It exists as a **cluster resource**, independent of any individual Pod.

**🔑 Key characteristics:**
- ⚙️ Provisioned either **statically** (manually by an admin) or **dynamically** (automatically via a StorageClass)
- 🌍 Represents actual storage infrastructure — e.g., AWS EBS, Azure Disk, GCE Persistent Disk, NFS
- ♻️ Has its own lifecycle, separate from any Pod that uses it
- 🗂️ Defines access modes such as `ReadWriteOnce`, `ReadOnlyMany`, `ReadWriteMany`

---

### 3.3 📝 PersistentVolumeClaim (PVC)

A **PersistentVolumeClaim** is a request for storage made by a user/application. It binds to a matching PersistentVolume based on requested size, access modes, and storage class.

**🔑 Key characteristics:**
- 🙋 Acts as a "claim ticket" that Pods use to request storage
- 🔗 Once bound to a PV, the PVC can be mounted into a Pod like any other volume
- 📏 Specifies requirements: storage size, access mode, and (optionally) a StorageClass

---

### 3.4 🏷️ StorageClass

A **StorageClass** defines the "classes" of storage available (e.g., SSD vs HDD, fast vs slow) and enables **dynamic provisioning** of PersistentVolumes on demand.

**🔑 Key characteristics:**
- ⚡ Automatically provisions a PV when a matching PVC is created
- 🎛️ Encapsulates parameters like provisioner type, reclaim policy, and volume binding mode
- 🏭 Removes the need for administrators to manually pre-provision storage

---

## ⚖️ 4. Ephemeral vs Persistent Storage — Comparison

| Aspect | ⚡ Ephemeral Storage | 🗄️ Persistent Storage |
|---|---|---|
| 🔗 Lifecycle | Tied to the Pod | Independent of the Pod |
| 💾 Data survival | Lost on Pod deletion/reschedule | Survives Pod deletion/reschedule |
| ⚙️ Setup complexity | Simple, no external provisioning | Requires PV, PVC, and/or StorageClass |
| 🎯 Use case | Scratch space, caching, sidecar sharing | Databases, stateful apps, critical data |
| 🧩 Examples | `emptyDir`, `hostPath`, `configMap`, `secret` | `PersistentVolume`, `PersistentVolumeClaim` |
| 🌐 Node portability | Usually tied to a single node | Can move across nodes (network-backed storage) |
