# 🗂️ Kubernetes Scheduler: Internals, Custom Configurations & Troubleshooting

## 📘 Overview

The **Kubernetes Scheduler (kube-scheduler)** is a control-plane component responsible for assigning Pods to Nodes. It watches for newly created Pods that have no Node assigned and selects the best Node for them to run on, based on resource requirements, constraints, and scoring policies.

This note covers three connected areas:
- 🧭 Manually scheduling a Pod (bypassing/assisting the scheduler)
- ⚙️ How the scheduler works internally (its pipeline)
- 🛠️ Creating and using custom schedulers
- 🚑 Troubleshooting unscheduled Pods and scheduler-related issues

---

## 🧭 1. Scheduling a Pod Manually on a Node

Kubernetes allows you to bypass the scheduler entirely by directly specifying the target Node in the Pod's YAML definition.

### ✍️ How to do it
In the Pod's YAML file, under the `spec` section, add the `nodeName` field:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  nodeName: Node001
  containers:
  - image: nginx
    name: nginx
```

> 💡 **Note:** When `nodeName` is set, the scheduler is skipped completely — the Pod is directly bound to the specified node by the Kubelet on that node.

---

## 🚨 2. What Happens When the Scheduler Is Not Running?

If **no scheduler is running** in the `kube-system` namespace, newly created Pods will not get assigned to any Node.

### 🔍 Symptoms
- Pod status remains stuck in **`Pending`** state.
- Running `kubectl describe pod <pod-name>` shows **no Node assigned**.

### 🛠️ Ways to Fix / Work Around This

**Method 1 — Manually assign a Node in YAML**
Use the `nodeName` field as shown in Section 1 above.

**Method 2 — Bind the Pod using a `curl` command**
If a Pod is already stuck in `Pending` due to the scheduler being down, you can manually bind it to a node using the Kubernetes API's `Binding` object:

```bash
curl --header "Content-Type:application/json" \
     --request POST \
     --data '{"apiVersion":"v1", "kind": "Binding", ....}' \
     http://$SERVER/api/v1/namespaces/default/$PODNAME/binding/
```

> ⚠️ This directly creates a `Binding` object via the API server, simulating what the scheduler would normally do.

---

## ⚙️ 3. Custom Scheduler Configuration

Kubernetes supports running **multiple schedulers** simultaneously within a single cluster — useful when different workloads need different scheduling logic.

### 🏗️ Creating a Custom Scheduler
- Multiple schedulers can be deployed on the Master node using a YAML file (deployed as a static Pod or Deployment).
- Each custom scheduler must be given a **unique name**.

### 📄 Assigning a Pod to a Custom Scheduler
To test/use a custom scheduler, specify its name in the Pod's `schedulerName` field instead of the default `default-scheduler`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  schedulerName: my-scheduler
  containers:
  - image: nginx
    name: nginx
```

### 🔎 Useful Commands for Verification

**Check scheduling events:**
```bash
kubectl get events -o wide
```

**View logs of a custom scheduler:**
```bash
kubectl logs my-scheduler -n kube-system
```

> 🧪 **Hands-on Practice:** Try this out in the K8s Lab exercises referenced in Lectures #79 and #80.

---

## 🧠 4. Kubernetes Scheduler Internals (Scheduling Pipeline)

The scheduler processes each Pod through a well-defined internal pipeline before it is finally bound to a Node.

### 🔄 Scheduling Steps

| Step | Description |
|------|-------------|
| 📥 **Queue** | Newly created Pods are placed into a scheduling queue. |
| 🔀 **Scheduling Queue (Queue Sort)** | Pods are sorted based on their **priority**. |
| 🧹 **Filtering** | Nodes that **don't have sufficient resources** (or don't meet constraints) are filtered out. |
| 🎯 **Scoring** | Remaining eligible Nodes are **scored** based on the free capacity/space that would remain if the Pod is deployed there. |
| 🔗 **Binding** | The Pod is finally **bound to the Node with the highest score**. |

### 🔌 Plugins & Extension Points
- Each of the steps above (Queue Sort, Filtering, Scoring, Binding, etc.) is implemented using **multiple plugins**.
- At every step, there is a corresponding **Extension Point** — a hook where custom plugins can be attached to modify or extend the default behavior of that step.

### 🧵 Multiple Schedulers vs. Scheduler Profiles

Running multiple independent schedulers in the same cluster introduces challenges:
- ⚔️ **Race conditions** may occur when multiple schedulers try to schedule the same Pod.
- 🧩 Each scheduler requires its **own process, lifecycle, and binary**, increasing operational overhead.

**✅ Solution: Scheduler Profiles**
From **Kubernetes release 1.18** onward, **Scheduler Profiles** were introduced. This feature allows you to define **multiple scheduling profiles within a single scheduler binary/process**, eliminating the need to run separate scheduler instances — and thereby avoiding race conditions and reducing operational complexity.

---

## 🚑 5. Troubleshooting Scheduler-Related Issues

When Pods are behaving unexpectedly, it's important to identify **which control-plane component** is responsible before troubleshooting.

### 🩺 Diagnostic Guide

| Symptom | Likely Cause | Where to Check |
|---------|-------------|-----------------|
| ❌ Pod is **not being assigned any Node** | Issue lies with the **Scheduler** | Since kube-scheduler runs as a **static Pod**, inspect its manifest at:<br>`/etc/kubernetes/manifests/` |
| ❌ Pod is **not scaling to the desired number of replicas** | Issue lies with the **Controller Manager** | Since kube-controller-manager runs as a **static Pod**, inspect its manifest at:<br>`/etc/kubernetes/manifests/` |

> 🧭 **Key takeaway:** Both the Scheduler and Controller Manager typically run as **static Pods** on the control-plane node. Their configuration files live in `/etc/kubernetes/manifests/`, and editing/restarting them involves modifying these manifest files directly (the Kubelet will auto-restart the static Pod when the manifest changes).

---

## ✅ Quick Recap

- 🧭 You can manually assign a Pod to a Node using `nodeName`, or bind it via a `curl`-based API call if the scheduler is down.
- ⚙️ Custom schedulers can be created and assigned to specific Pods using `schedulerName`.
- 🧠 The scheduler follows a pipeline: **Queue → Queue Sort → Filtering → Scoring → Binding**, with plugins and extension points at each stage.
- 🧵 **Scheduler Profiles** (since v1.18) solve the problems of running multiple standalone schedulers.
- 🚑 Unscheduled Pods → check the **Scheduler**; Pods not scaling → check the **Controller Manager**. Both are static Pods configurable via `/etc/kubernetes/manifests/`.
