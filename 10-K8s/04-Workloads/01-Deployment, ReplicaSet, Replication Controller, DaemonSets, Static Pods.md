# Kubernetes Workloads: Deployments, ReplicaSets, DaemonSets & Static Pods

## 🧭 1. API Groups & Metadata — Quick Notes

Each object in Kubernetes belongs to one particular API class/group.
`Deployment`, `Service`, `ReplicaSet` belong to `apiVersion: apps/v1`.

Different objects have different use-cases — that's why these objects are grouped into different API classes.

**Metadata** is data about data. The **name** and **label** of any Kubernetes object are present in `metadata`.

---

## 🚀 2. Deployment Sets

### 2.1 Creating a Deployment

Create one deployment of nginx with `replicas=3`.

Whenever a Deployment is created, a **ReplicaSet is also created implicitly**, with the same name as that of the Deployment (plus a suffix).

We could, of course, create 3 separate Pods with the same label without using a Deployment. But if we do:

```bash
kubectl get deploy -n nginx
kubectl get pods --show-labels -n nginx
```

The output will contain the labels of all Pods. Here, you can see a **hash-label** is also generated — a random and unique label (`pod-template-hash`) for any Deployment. This distinguishes Pods created from a Deployment from other Pods, even if those other Pods were explicitly given the same labels in their Pod templates.

**Filter pods with a particular label:**

```bash
kubectl get pods --selector app=MyPod
```

---

### 2.2 ReplicaSet: Labels & Selectors

- A ReplicaSet uses **labels and selectors** to bind Pods to itself.
- For health-checking Pods under a ReplicaSet, it uses labels.
- Any Pod created manually with the same labels mentioned in the **Selector** section of a ReplicaSet comes under the health-check of that ReplicaSet.
- All the labels in the Selector section of a ReplicaSet must match the Pod in order to bind with each other.
- In case the labels present in a ReplicaSet match Pods that are **not** meant to be part of it, we must add an extra label in the selector field of the ReplicaSet to ensure a difference in labels from that extra Pod.

---

### 2.3 Generating YAML from Commands

**Create a YAML file from a command for a Deployment:**

```bash
kubectl create deployment blue --image=nginx --replicas=3 -o yaml
kubectl create deployment blue --image=nginx --replicas=3 -o yaml > blue.yml
```

> DaemonSet and ReplicaSet are very similar in their YAML definition files — the only change needed is the `kind`.

---

## 🛰️ 3. DaemonSets

### 3.1 What is a DaemonSet?

DaemonSets are objects that get created as a **single Pod on every Node** added to the Kubernetes cluster, and get **removed automatically** from Nodes that are removed from the cluster.

These Pods are commonly used for:
- Log capture
- Monitoring

**Examples:** `kube-proxy`, `kube-flannel`, Weavenet (for networking).

---

### 3.2 Scheduling Behavior

Post Kubernetes **v1.12**, DaemonSets use the **default-scheduler** and **Node-Affinity** to deploy DaemonSet Pods on each node.

---

### 3.3 Useful Commands

```bash
kubectl get daemonsets
kubectl get ds -n kube-system
```

---

### 3.4 Creating a DaemonSet

```bash
kubectl create deployment elasticsearch -n kube-system --image=k8s.gcr.io/fluentd-elasticsearch:1.20 --dry-run=client -o yaml > fluentd.yaml
```

Then edit this file and change the `kind` from `Deployment` to `DaemonSet`. The structure of a DaemonSet and a Deployment is the same.

---

## 📌 4. Static Pods

### 4.1 What is a Static Pod?

Static Pods are Pods that get created **automatically by the kubelet** when the YAML files of these Pods are placed in the **Pod Manifest Path** of the kubelet. The path is generally:

```
/etc/kubernetes/manifests
```

To find the path, on the Master Node run:

```bash
cat /var/lib/kubelet/config.yml | grep staticPodPath
```

Any YAML file placed in this path will get created — but **only for Pods**, not for Deployments, ReplicaSets, etc. To create these Pods on a worker, the kubelet of that worker doesn't even need the API Server, Scheduler, etcd, or Controller Manager.

---

### 4.2 Static Pods as Control Plane Components

`etcd`, `kube-apiserver`, `kube-controller-manager`, `kube-scheduler`, etc. are all types of Static Pods.

---

### 4.3 Static Pods vs DaemonSets

| Aspect | Static Pods | DaemonSets |
|---|---|---|
| **Created by** | Kubelet | Kube API Server (DaemonSet Controller) |
| **Typical purpose** | Deploy control plane components | Deploy monitoring/logging agents on nodes |
| **Scheduler** | Ignored by kube-scheduler | Ignored by kube-scheduler |
| **Deployed on** | Control Plane / Master Node | All Nodes (including Master and Worker) |
| **API object references** | Spec cannot refer to other API objects (ServiceAccount, ConfigMap, Secret, etc.) | Can reference other API objects |
| **Ephemeral containers** | Not supported | Supported |

---

### 4.4 Creating Static Pods

```bash
kubectl run static-busybox --image=nginx --dry-run=client -o yaml --command -- sleep 1000 > /etc/kubernetes/manifests/staticpod.yaml
```

**File name / path for Static Pods:**

```bash
cat /var/lib/kubelet/config.yaml | staticPodPath
```

This path can be different for each node in a cluster, so this is how you can add a node-specific static Pod.

```bash
kubectl run static-busybox --image=busybox --restart=Never --dry-run=client -o yaml --command -- sleep 1000
```

> Note: The `command` flag should always be placed at the end.

---

## 🔄 5. Deployment Rollouts & Strategies

### 5.1 Rollout Status

```bash
kubectl get deploy
kubectl rollout status deployment/myapp-deployment
kubectl rollout history deployment/myapp-deployment
```

---

### 5.2 Deployment Strategies

- **Recreate**
  - Deletes all older Pods, then creates Pods with the new image.
  - Application experiences downtime.

- **Rolling-Update**
  - Deletes Pods one-by-one while creating Pods with the new image at the same time.
  - Application doesn't experience downtime.
  - A new ReplicaSet is created where the number of Pods in the new ReplicaSet increases one-by-one, while the number of Pods in the old ReplicaSet decreases one-by-one at the same time.
  - Check the relevant parameters to set in the `spec` of a Deployment for Rolling-Update.

**Check the deployment strategy:**

```bash
kubectl describe deploy myapps | grep -i strategyType
```

---

### 5.3 Rolling Out a Change / Rollback

```bash
kubectl get deploy
kubectl rollout undo deploymentName
kubectl get replicasets
```

---

### 5.4 Setting a New Image

```bash
kubectl set image deployment/Dep_name container_name=new_image_name
kubectl set image deployment/myapp-deployment nginx=nginx:1.9.1
```

---

## ❤️ 6. Self-Healing Applications

Kubernetes supports self-healing applications through **ReplicaSets** and **Replication Controllers**. The replication controller helps ensure that a Pod is **re-created automatically** when the application within the Pod crashes. It helps ensure enough replicas of the application are running at all times.

Kubernetes provides additional support to check the health of applications running within Pods and take necessary actions through **Liveness** and **Readiness Probes**.
