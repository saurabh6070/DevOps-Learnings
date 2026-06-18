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
        - name: emptyDirVolume
          mountPath: /data1
      - name: ubuntu
        image: ubuntu
        volumeMounts:
        - name: emptyDirVolume
          mountPath: /data2/
      volumes:
      - name: emptyDirVolume
        emptyDir: {}
```

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


## 🗄️ 4. Ceph Storage Integration

### 🔹 What is Ceph?
 - Ceph is a distributed storage system providing:
 - Block storage (RBD).
 - Object storage (Ceph Object Gateway).
 - File storage (CephFS).
 - It is highly scalable and fault-tolerant.


## 🛠️ 5. Setting up Ceph Cluster in AWS
 - To use Ceph with Kubernetes:
 - Provision 3 EC2 instances (recommended for quorum).
 - Install Ceph packages (ceph, ceph-mon, ceph-osd, ceph-mgr).
 - Configure Ceph monitors and OSDs across the 3 nodes.
 - Verify cluster health:
```bash
ceph -s
```

## 🔄 6. Using Ceph in Kubernetes

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
