# 🚀 Kubernetes Pod Issues & Troubleshooting Guide

## 📘 Topic: Common Pod Failures — CrashLoopBackOff, ImagePullBackOff, and Pending States

Pods are the smallest deployable units in Kubernetes, and they can fail for many different reasons — anywhere from a bad image name to insufficient cluster resources. As an engineer, knowing **how to identify, diagnose, and fix** these failures quickly is one of the most important day-to-day Kubernetes skills.

This guide covers the three most commonly seen Pod issues, their root causes, and step-by-step troubleshooting approaches.

---

## 🔍 How to Start Troubleshooting Any Pod Issue

Before diving into specific errors, always start with these two commands — they are the foundation of Pod debugging:

```bash
kubectl get pods -n <namespace>
kubectl describe pod <pod-name> -n <namespace>
```

- `kubectl get pods` → gives you the **current status** of the Pod (Running, Pending, CrashLoopBackOff, etc.)
- `kubectl describe pod` → gives you **Events**, **Reason**, and detailed condition history — this is where most of the answers live.

You can also check logs of the container inside the Pod:

```bash
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous   # for the last crashed container
```

---

## 🖼️ 1. ImagePullBackOff

### 🧩 What It Means
`ImagePullBackOff` occurs when Kubernetes is **unable to pull the container image** required to start the Pod. Kubernetes retries the pull with an exponential backoff delay — hence the name "BackOff."

### ⚠️ Common Causes
| Cause | Description |
|---|---|
| ❌ Image not found | The image used to deploy the Pod does not exist in the specified image repository |
| ✍️ Typo in image name/tag | Incorrect spelling of the image name or an invalid/non-existent tag (e.g., `myapp:latst` instead of `myapp:latest`) |
| 🔒 Private registry without credentials | The image is in a private repository, and no `imagePullSecrets` is configured |
| 🌐 Network/registry unreachable | The node cannot reach the container registry (DNS issue, firewall, proxy) |
| 🚫 Rate limiting | Registry (e.g., Docker Hub) is rate-limiting anonymous pulls |

### 🛠️ Troubleshooting Steps
1. Run `kubectl describe pod <pod-name>` and check the **Events** section for the exact error (e.g., `manifest unknown`, `unauthorized`, `not found`).
2. Verify the image name and tag are correct by trying to pull it manually:
   ```bash
   docker pull <image-name>:<tag>
   ```
3. Confirm the image actually exists in the repository (Docker Hub, ECR, GCR, ACR, etc.).
4. If it's a private registry, verify a Secret exists and is referenced correctly:
   ```bash
   kubectl get secret <secret-name> -n <namespace>
   ```
   And that it's attached in the Pod spec:
   ```yaml
   spec:
     imagePullSecrets:
       - name: my-registry-secret
   ```
5. Check node-level network connectivity to the registry.

### ✅ Solution
- Fix the image name/tag in the Deployment/Pod manifest.
- Create and attach the correct `imagePullSecrets` for private registries.
- Push the image to the repository if it is genuinely missing.
- Retry after resolving any registry rate-limit or network issue.

---

## 🔁 2. CrashLoopBackOff

### 🧩 What It Means
`CrashLoopBackOff` means the container **starts, then crashes repeatedly**, and Kubernetes keeps trying to restart it with an increasing backoff delay between attempts.

### ⚠️ Common Causes
| Cause | Description |
|---|---|
| 💥 Application error on startup | The app inside the container crashes due to a bug, missing config, or bad startup command |
| 🧠 OOMKilled | The Pod is terminated because it **ran out of memory** — this happens when the memory **limit** assigned to the Pod is **less than what the application actually requires** |
| ⚙️ Wrong command/entrypoint | Incorrect `CMD`/`ENTRYPOINT` causes the container process to exit immediately |
| 🔑 Missing environment variables/secrets | App fails to start because required config, secrets, or ConfigMaps aren't mounted |
| 🩺 Failing liveness probe | Kubernetes restarts the container because the liveness probe keeps failing |

### 🛠️ Troubleshooting Steps
1. Describe the Pod to check the **Last State**, **Reason**, and **Exit Code**:
   ```bash
   kubectl describe pod <pod-name>
   ```
   - If you see **`Terminated`** with reason **`OOMKilled`**, it confirms the Pod ran out of memory.
2. Check container logs (including the previous crashed instance) for stack traces or error messages:
   ```bash
   kubectl logs <pod-name> --previous
   ```
3. Check the exit code:
   - `Exit Code 0` → normal exit (probably a bad command with no long-running process)
   - `Exit Code 1` → application error
   - `Exit Code 137` → container was **killed (OOMKilled or SIGKILL)**
4. Review the resource `requests` and `limits` defined in the manifest:
   ```yaml
   resources:
     requests:
       memory: "128Mi"
       cpu: "250m"
     limits:
       memory: "256Mi"
       cpu: "500m"
   ```
5. Verify liveness/readiness probes aren't too aggressive (short timeout/low failure threshold).

### ✅ Solution
- **For OOMKilled:** increase the memory `limit` so it comfortably covers the application's actual memory requirement.
- Fix application bugs or startup commands causing the crash.
- Ensure required ConfigMaps, Secrets, and environment variables are correctly mounted.
- Tune liveness probe `initialDelaySeconds`, `timeoutSeconds`, and `failureThreshold` to realistic values.

---

## ⏳ 3. Pending State

### 🧩 What It Means
A Pod stuck in `Pending` state has been **accepted by the Kubernetes API server but has not yet been scheduled onto any Node** — or it has been scheduled but its containers haven't started yet.

### ⚠️ Common Causes
| Cause | Description |
|---|---|
| 📉 Insufficient resources | If a Pod cannot be assigned to a Node due to insufficient CPU/memory resources, the Pod stays in **Pending** state with reason **`FailedScheduling`** |
| 🏷️ Node affinity/selector mismatch | No node matches the `nodeSelector`, `affinity`, or `taints/tolerations` rules defined in the Pod spec |
| 📦 PersistentVolumeClaim not bound | The Pod is waiting on a PVC that hasn't been provisioned/bound yet |
| 🚧 No available nodes | Cluster autoscaler hasn't added new nodes yet, or all nodes are cordoned/unschedulable |

### 🛠️ Troubleshooting Steps
1. Describe the Pod and check the **Events** section:
   ```bash
   kubectl describe pod <pod-name>
   ```
   - Look for: `0/3 nodes are available: insufficient cpu/memory` → confirms **`FailedScheduling`** due to resource shortage.
2. Check overall cluster resource availability:
   ```bash
   kubectl describe nodes
   kubectl top nodes
   ```
3. Check if the Pod has any `nodeSelector`, `affinity`, or `tolerations` that no node satisfies.
4. Check the status of any PVCs referenced by the Pod:
   ```bash
   kubectl get pvc -n <namespace>
   ```

### ✅ Solution
- Reduce the Pod's resource `requests`, or add more/larger Nodes to the cluster (or enable Cluster Autoscaler).
- Correct any mismatched `nodeSelector`/`affinity`/`taints`-`tolerations` configuration.
- Ensure the StorageClass and PV/PVC are correctly provisioned and bound.
- Uncordon nodes or free up scheduling capacity if nodes are marked unschedulable.

---

## 📊 Quick Reference Table

| Status | Meaning | Primary Reason Shown | Typical Fix |
|---|---|---|---|
| 🖼️ **ImagePullBackOff** | Image can't be pulled | Image not found / auth failure | Fix image name/tag, add `imagePullSecrets` |
| 🔁 **CrashLoopBackOff** | Container keeps crashing & restarting | `OOMKilled`, app crash, bad exit code | Increase memory limits, fix app/startup issue |
| ⏳ **Pending** | Pod not yet scheduled | `FailedScheduling` | Free up resources, fix scheduling constraints |

---

## 🎯 Key Takeaways for Students

- ✅ Always start troubleshooting with `kubectl describe pod` — it's the single most useful command for Pod issues.
- ✅ **ImagePullBackOff** → problem with the image itself or registry access.
- ✅ **CrashLoopBackOff** → problem with the application or resource limits (especially memory → OOMKilled).
- ✅ **Pending** → problem with scheduling, usually due to insufficient cluster resources (`FailedScheduling`).
- ✅ `kubectl logs --previous` is essential for debugging crashed containers.
- ✅ Set realistic `requests` and `limits` to avoid both OOMKills and scheduling failures.

---

📝 *End of Topic — Pod Issues, Troubleshooting Steps & Solutions*
