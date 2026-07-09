# Docker Storage & Kubernetes Interfaces

---

## 1. Docker Drivers

Docker uses two types of drivers to manage how data is stored and accessed:

- **Storage Driver** — manages the layered image filesystem
- **Volume Driver** — manages persistent data volumes

---

## 2. Docker Filesystem Layout

Docker's core filesystem lives at:

```
/var/lib/docker/
├── aufs
├── containers
├── image
└── volumes
```

---

## 3. Image Layers

### 3.1 Layered Architecture

Docker stores images using a **layered architecture**. When a new image is pushed, Docker checks whether any of its layers already match existing layers on the system. Only the new/upper layers that don't already exist are stored.

**Benefits:**
- Faster uploads
- Reduced storage usage
- Greater overall efficiency

### 3.2 Read/Write Permissions

| Layer Type | Access |
|---|---|
| Image layer | Read-only |
| Container layer | Read-write |

---

## 4. Mounting Data into Containers

### 4.1 Volume Mount

Mounting a volume created under `/var/lib/docker/volumes/` into a container is called a **Volume Mount**.

**Step 1 — Create the volume:**
```bash
docker volume create data_volume
```
> Creates a directory named `data_volume` inside `/var/lib/docker/volumes/`.

**Step 2 — Mount it to a container:**
```bash
docker run -v data_volume:/var/lib/mysql mysql
```
> Creates a container from the `mysql` image and mounts the volume above to `/var/lib/mysql` inside the container.

> 💡 **Note:** Step 1 isn't strictly necessary — if the volume doesn't exist, Step 2 creates it automatically.

### 4.2 Bind Mount

Mounting any host path **other than** `/var/lib/docker/volumes/` into a container is called a **Bind Mount**.

**Legacy syntax:**
```bash
docker run -v /data/mysql:/var/lib/mysql mysql
```
> Creates a container using the `mysql` image, mounting host directory `/data/mysql` to `/var/lib/mysql` in the container.

**Newer, preferred syntax:**
```bash
docker run --mount type=bind,source=/data/mysql,target=/var/lib/mysql mysql
```

---

## 5. Storage Drivers

Docker uses storage drivers to manage the layered image architecture.

**Common storage drivers:**
`AUFS` · `ZFS` · `BTRFS` · `Device Mapper` · `Overlay` · `Overlay2`

> The choice of driver depends on the underlying OS — for example, Ubuntu defaults to `AUFS`. Docker automatically selects the best-suited driver unless told otherwise.

---

## 6. Volume Drivers

### 6.1 Examples

`Local` · `Convoy` · `gce-docker` · `Portworx` · `Azure File Storage` · `NetApp` · `RexRay`

### 6.2 Mounting an AWS EBS Volume

```bash
docker run -it --name mysql --volume-driver rexray/ebs --mount src=ebs-vol,target=/var/lib/mysql mysql
```

### 6.3 Driver Selection

> 💡 **Note:** By default, Docker automatically picks the best available **storage driver** if none is specified. To use a specific **volume driver** instead, it must be explicitly declared using the `--volume-driver` flag.

---

## 7. Kubernetes Interfaces

Kubernetes uses three interfaces to extend support for different backends:

| Interface | Full Name | Purpose | Examples |
|---|---|---|---|
| **CRI** | Container Runtime Interface | Supports different container runtimes | Docker, CRI-O, Rocket (RKT) |
| **CNI** | Container Networking Interface | Supports different networking solutions | Flannel, Cilium, Weaveworks |
| **CSI** | Container Storage Interface | Supports different storage solutions | Portworx, Amazon EBS, Dell EMC, GlusterFS |

---

## 8. CSI Communication Flow

Kubernetes (via CSI) communicates with storage drivers using **Remote Procedure Calls (RPCs)** to perform operations on remote storage:

- **Create Volume** — provisions a new volume on the storage backend
- **Delete Volume** — decommissions an existing volume
- **Controller Publish Volume** — makes the volume available on a node
