# 📘 Kubernetes — Introduction: Architecture & Functions

---

## 📑 Table of Contents

- [☸️ 1. What is Kubernetes?](#what-is-kubernetes)
  - [🧩 1.1 The Problem it Solves](#11-the-problem-it-solves)
  - [⚖️ 1.2 Alternatives & Why Kubernetes Wins](#12-alternatives--why-kubernetes-wins)
- [🏗️ 2. Cluster Architecture](#2-cluster-architecture)
  - [🧠 2.1 Control Plane Components](#21-control-plane-components)
    - [kube-apiserver](#-kube-apiserver)
    - [etcd](#-etcd)
    - [kube-scheduler](#-kube-scheduler)
    - [kube-controller-manager](#-kube-controller-manager)
    - [cloud-controller-manager (optional)](#-cloud-controller-manager-optional)
  - [🖥️ 2.2 Node (Data Plane) Components](#22-node-data-plane-components)
    - [kubelet](#-kubelet)
    - [Multi-Master Notes](#multi-master-notes)
    - [kube-proxy](#-kube-proxy)
    - [Container Runtime](#-container-runtime)
  - [🧩 2.3 Cluster Add-ons](#23-cluster-add-ons)
- [☁️ 3. Turnkey & Hosted Solutions of K8s (Managed vs. Self-hosted)](#3-turnkey--hosted-solutions-of-k8s-managed-vs-self-hosted)

---

## ☸️ 1. What is Kubernetes?

Kubernetes (abbreviated **K8s** — because there are 8 letters between the "K" and "s") is an **open-source container orchestration platform** that automates the deployment, scaling, and operational management of containerized applications.

It was originally built by Google, and is now maintained by the **Cloud Native Computing Foundation (CNCF)**.

> **Simple mental model:** Think of Kubernetes as an operating system for your data center. Just like an OS manages processes on a single machine, Kubernetes manages containers across an entire cluster of machines.

---

### 🧩 1.1 The Problem it Solves

Running one container on one machine is easy. Running hundreds of containers across dozens of machines is not. Here's what breaks without an orchestrator:

| Challenge | Without K8s | With K8s |
|---|---|---|
| Container crashes | Manual restart required | Auto-restarted by kubelet |
| High traffic | Manually spin up containers | Auto-scales via HPA |
| Deploying updates | Downtime or manual coordination | Rolling updates, zero downtime |
| Service discovery | Hardcoded IPs | DNS-based service discovery |
| Resource allocation | Guesswork | Scheduler handles bin-packing |
| Configuration management | Files scattered across servers | ConfigMaps & Secrets in cluster |

---

### ⚖️ 1.2 Alternatives & Why Kubernetes Wins

| Tool | Strength | Limitation |
|---|---|---|
| **Docker Swarm** | Simple, fast setup | Limited ecosystem, fewer features |
| **Apache Mesos** | Handles multi-workload (non-container too) | Complex to operate |
| **HashiCorp Nomad** | Lightweight, works with VMs too | Smaller community |
| **Kubernetes** | Full-featured, cloud-native, CNCF-backed | Steeper learning curve |

**Why teams choose Kubernetes:**
- Massive community and ecosystem (Helm, Operators, service meshes)
- Native support on all major clouds (EKS, GKE, AKS)
- Extensible via **Custom Resource Definitions (CRDs)** and controllers
- Enterprise-grade RBAC, multi-tenancy, audit logging

---

## 🏗️ 2. Cluster Architecture

A Kubernetes cluster is made up of two logical layers:

- **Control Plane** — the brain; makes decisions, stores state, manages the cluster
- **Worker Nodes** — the muscle; run your actual containerized applications inside Pods


<img width="533" height="411" alt="k8s" src="https://github.com/user-attachments/assets/6587e70a-2d96-4c70-93e2-0ea597c41f14" />


---

### 🧠 2.1 Control Plane Components

#### 🔹 kube-apiserver

The **front door** of the entire Kubernetes cluster. Every interaction — from `kubectl` commands to internal controller loops — goes through the API server.

- Exposes the Kubernetes REST API
- Authenticates and authorizes every request
- Validates object manifests before persisting them to etcd
- **Horizontally scalable** — run multiple instances for HA

```bash
# All kubectl commands hit the API server
kubectl get pods  →  HTTP GET /api/v1/namespaces/default/pods
```

---

#### 🔹 etcd

A **distributed, consistent key-value store** that holds the entire state of your cluster — every object, every configuration, every secret.

- Built on the Raft consensus algorithm for strong consistency
- Only the API server communicates with etcd directly
- **Critical:** if etcd data is lost without a backup, your cluster state is gone

> ⚠️ **Instructor Tip:** Always set up automated etcd backups before running production workloads. Use `etcdctl snapshot save` on a schedule.

```bash
# Manually backup etcd
ETCDCTL_API=3 etcdctl snapshot save snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

---

#### 🔹 kube-scheduler

Watches for **newly created Pods that have no node assigned** and selects the best node to run them on.

The scheduler considers:
- **Resource requests vs. available capacity** (CPU, memory)
- **Node affinity / anti-affinity** rules
- **Taints and tolerations**
- **Data locality** (keep Pods near their data)
- **Deadlines and priority classes**

> The scheduler does NOT start Pods — it only decides *where* they should run. The kubelet on the selected node does the actual work.

---

#### 🔹 kube-controller-manager

Runs a set of **controller loops** as a single binary process. Each controller watches the cluster state and makes changes to drive it toward the desired state.

| Controller | Responsibility |
|---|---|
| **Node Controller** | Detects and responds when nodes go unreachable |
| **Job Controller** | Creates Pods for one-off batch tasks, tracks completion |
| **ReplicaSet Controller** | Ensures the correct number of Pod replicas are running |
| **Endpoints Controller** | Populates the Endpoints object (connects Services to Pods) |
| **ServiceAccount Controller** | Creates default service accounts in new namespaces |

> **Key concept:** Controllers follow a **reconciliation loop** — observe current state, compare to desired state, act to close the gap.

---

#### 🔹 cloud-controller-manager *(optional)*

Integrates Kubernetes with cloud-provider APIs. It runs only when Kubernetes is deployed on a cloud platform.

- Provisions **cloud load balancers** when a `Service` of type `LoadBalancer` is created
- Manages **cloud storage volumes**
- Updates node objects with cloud metadata (region, zone, instance type)

Supported providers include AWS, GCP, Azure, OpenStack, and more via vendor plugins.

---

### 🖥️ 2.2 Node (Data Plane) Components

Every worker node runs these three components:

#### 🔹 kubelet

The **primary agent** on each node. It communicates with the API server and ensures the containers described in PodSpecs are running and healthy.

- Watches for Pods assigned to its node
- Pulls container images and starts containers via the container runtime
- Reports node and Pod status back to the control plane
- Runs **liveness and readiness probes** to check container health

> The kubelet does NOT manage containers it did not create via Kubernetes (e.g., containers started with plain `docker run`).

##### Multi-Master Notes

**001 →** Kube API-Server talks to kubelet of each Worker.
- In case we have multiple Masters, then to which Kube API-Server does the kubelet talk?
- Kube API-Server works in **Active-Active** mode and processes requests coming from the kubelet independently.
- In case of multiple Kube API-Servers, a **Load Balancer** is created on top of these Kube API-Servers to balance traffic.

**002 →** Controller-Manager and Kube-Scheduler work in **Active-Standby** mode in case of multiple masters. A leader election is conducted among all the Controller-Managers/Schedulers, and it is checked every **15s** which one should be elected the Leader.

**003 →** ETCD works in **Active-Active** mode.
- The placement of the ETCD-Server can be on the same set of Master-Nodes on which the other control-plane components are deployed, or on a different set of Master-Nodes.
- Since ETCD only talks with the Kube API-Server, the IP-Address of ETCD is passed as an argument while setting up `kubeadm`.

---

#### 🔹 kube-proxy

A **network proxy** running on each node that maintains network rules to implement Kubernetes **Services**.

- Uses the OS packet filtering layer (e.g., iptables or IPVS) to route traffic
- Enables `ClusterIP`, `NodePort`, and `LoadBalancer` service types to function
- Not responsible for Pod-to-Pod networking — that's handled by the CNI plugin (e.g., Calico, Flannel)

---

#### 🔹 Container Runtime

The software that actually **executes containers** on the node. Kubernetes interfaces with runtimes via the **Container Runtime Interface (CRI)**.

Common runtimes:

| Runtime | Notes |
|---|---|
| **containerd** | Default runtime in most modern clusters (used by EKS, GKE) |
| **CRI-O** | Lightweight, built specifically for Kubernetes |
| **Docker Engine** | Deprecated as a K8s runtime since v1.24; use containerd instead |

---

### 🧩 2.3 Cluster Add-ons

Add-ons extend cluster capabilities beyond the base components. Most are deployed as Pods managed by Deployments or DaemonSets.

| Add-on | Purpose |
|---|---|
| **CoreDNS** | Provides cluster-wide DNS resolution for Services and Pods |
| **Kubernetes Dashboard** | Web UI for managing and monitoring cluster resources |
| **Metrics Server** | Collects resource usage (CPU/memory) — required by HPA |
| **Cluster Logging** | Centralized log collection (e.g., Fluentd → Elasticsearch) |
| **CNI Plugin** | Handles Pod networking (Calico, Flannel, Cilium, Weave) |

---

## ☁️ 3. Turnkey & Hosted Solutions of K8s (Managed vs. Self-hosted)

**001 → Turnkey Solutions (Hosted solution):**
- You Provision VMs
- You configure VMs
- You use scripts to Deploy Cluster
- You maintain VMs yourself
- Example: Kubernetes on AWS using KOPS, OpenShift, Cloud Foundry Container Runtime, VMware Cloud PKS, Vagrant

**002 → Hosted Solutions (Managed Solutions):**
- Kubernetes as a Service
- Provider provisions VMs
- Provider installs Kubernetes
- Provider maintains VMs
- Example: Google Container Engine (GKE), OpenShift (Online), Azure Kubernetes Service, Amazon Elastic Container Service for Kubernetes (EKS)
