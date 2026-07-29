# 📈 Horizontal Pod Autoscaler (HPA) — Kubernetes Notes

---

## 📘 1. What is HPA?

The **Horizontal Pod Autoscaler (HPA)** is a Kubernetes controller that automatically **increases or decreases the number of Pod replicas** in a Deployment, ReplicaSet, or StatefulSet based on observed **metrics** (CPU, memory, or custom/external metrics).

> 🔑 **Key Idea:** HPA scales **horizontally** (adds/removes Pods) — not to be confused with VPA (Vertical Pod Autoscaler), which scales **vertically** (adjusts CPU/memory of existing Pods).

---

## ⚙️ 2. How HPA Works (Architecture)

```
Metrics Server / Custom Metrics API
              │
              ▼
   HPA Controller (checks every 15s by default)
              │
              ▼
   Compares current metric vs target metric
              │
              ▼
   Calculates desired replica count
              │
              ▼
   Updates replicas field on Deployment/ReplicaSet/StatefulSet
```

### 🔄 Control Loop Steps
1. HPA controller polls metrics periodically (default: every **15 seconds**, controlled by `--horizontal-pod-autoscaler-sync-period`).
2. It fetches metrics from the **Metrics Server** (for CPU/memory) or **Custom/External Metrics APIs**.
3. It calculates the **desired replica count** using a scaling formula.
4. It updates the `replicas` field of the target workload.
5. The Deployment/ReplicaSet controller then creates or deletes Pods to match.

---

## 🧮 3. HPA Scaling Formula

```
desiredReplicas = ceil( currentReplicas × ( currentMetricValue / desiredMetricValue ) )
```

**Example:**
- Current Replicas = 4
- Current CPU usage = 80%
- Target CPU usage = 50%

```
desiredReplicas = ceil( 4 × (80 / 50) ) = ceil(6.4) = 7
```

---

## 🧩 4. Prerequisites

| Requirement | Purpose |
|---|---|
| 📊 **Metrics Server** | Required for CPU/memory-based autoscaling |
| 🎯 **Resource Requests** | Pods must define `resources.requests` (CPU/memory) — HPA calculates % based on requests |
| 🔌 **Custom Metrics Adapter** (optional) | Needed for custom/external metrics (e.g., Prometheus Adapter) |

> ⚠️ **Important:** Without `resource requests` defined on the container, CPU/memory-based HPA **will not work**.

---

## 📄 5. HPA API Versions

| API Version | Supports |
|---|---|
| `autoscaling/v1` | CPU utilization only |
| `autoscaling/v2` (stable, recommended) | CPU, Memory, Custom & External metrics, multiple metrics, scaling behavior |
| `autoscaling/v2beta2` | Deprecated (older clusters) |

---

## 📝 6. Sample HPA YAML (CPU-based)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: webapp-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: webapp-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
```

---

## 📝 7. Sample HPA YAML (CPU + Memory, Multiple Metrics)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: multi-metric-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-deployment
  minReplicas: 3
  maxReplicas: 15
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

> 📌 **Note:** When multiple metrics are defined, HPA calculates the desired replicas for **each metric** and picks the **highest** value.

---

## 🎯 8. Types of Metrics Supported

| Metric Type | Description | Example |
|---|---|---|
| 📦 **Resource** | Built-in CPU/Memory metrics | `cpu`, `memory` |
| 🧾 **Pods** | Custom metric averaged across Pods | requests-per-second per pod |
| 🌐 **Object** | Metric from a Kubernetes object | Ingress requests, queue length |
| 🛰️ **External** | Metric from outside the cluster | SQS queue length, Kafka lag |

---

## 🎛️ 9. Scaling Behavior (Advanced Control)

Kubernetes allows fine-tuning **scale-up/scale-down speed** using the `behavior` field:

```yaml
spec:
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Pods
          value: 4
          periodSeconds: 60
```

| Field | Purpose |
|---|---|
| ⏱️ `stabilizationWindowSeconds` | Prevents flapping by waiting before scaling down |
| 📉 `scaleDown` | Controls how fast Pods are removed |
| 📈 `scaleUp` | Controls how fast Pods are added |

---

## 🛠️ 10. Common `kubectl` Commands

| Command | Description |
|---|---|
| `kubectl autoscale deployment webapp --cpu-percent=60 --min=2 --max=10` | Create HPA imperatively |
| `kubectl get hpa` | List all HPAs |
| `kubectl describe hpa webapp-hpa` | View detailed HPA status & events |
| `kubectl get hpa webapp-hpa -o yaml` | View HPA YAML config |
| `kubectl delete hpa webapp-hpa` | Delete an HPA |
| `kubectl top pods` | View live CPU/memory usage (needs Metrics Server) |

---

## 🚦 11. HPA Status Fields

```bash
kubectl describe hpa webapp-hpa
```

| Field | Meaning |
|---|---|
| `Current Replicas` | Pods currently running |
| `Desired Replicas` | Target Pods calculated by HPA |
| `Min/Max Replicas` | Scaling boundaries |
| `Metrics` | Current vs target values |
| `Events` | Scaling actions history |

---

## ✅ 12. Best Practices

- ✅ Always set **resource requests** on containers.
- ✅ Set realistic **min/max replicas** to avoid over/under-provisioning.
- ✅ Use `autoscaling/v2` for flexibility (multi-metric support).
- ✅ Combine HPA with **Cluster Autoscaler** for node-level scaling.
- ✅ Use **stabilization windows** to prevent scaling flapping.
- ✅ Monitor with **Prometheus + Grafana** for custom metrics.
- ✅ Test scaling behavior under load (use tools like `hey`, `k6`, or `Apache Bench`).

---

## ⚠️ 13. Limitations & Gotchas

- ❌ HPA **cannot** scale StatefulSets with certain storage constraints smoothly (needs care with PVCs).
- ❌ Requires **Metrics Server** — won't work out of the box on some clusters.
- ❌ Sudden traffic spikes may cause **lag** since metrics are polled periodically (not instant).
- ❌ Scaling to `0` replicas is **not supported** natively (use KEDA for scale-to-zero).
- ❌ Works only with objects that support the `scale` subresource (Deployment, ReplicaSet, StatefulSet, ReplicationController).

---

## 🔍 14. HPA vs VPA vs Cluster Autoscaler

| Feature | HPA | VPA | Cluster Autoscaler |
|---|---|---|---|
| 📐 Scales | Number of Pods | Pod resource limits (CPU/mem) | Number of Nodes |
| 🎯 Trigger | Metrics (CPU/mem/custom) | Metrics (CPU/mem) | Pending unschedulable Pods |
| 🔁 Direction | Horizontal | Vertical | Node-level (Horizontal for nodes) |
| 🤝 Can combine? | Yes, with Cluster Autoscaler | Not recommended with HPA on same metric | Yes, with HPA |

---

## 🚀 15. HPA + KEDA (Event-Driven Autoscaling)

**KEDA (Kubernetes Event-Driven Autoscaler)** extends HPA to support:
- 📬 Scaling based on **message queue length** (Kafka, RabbitMQ, SQS)
- 🔽 **Scale-to-zero** capability
- 🔌 50+ built-in event source **scalers**

> KEDA works *by creating and managing an HPA object* behind the scenes — it doesn't replace HPA, it enhances it.

---

## 🧠 16. Quick Revision Summary

| Concept | Key Point |
|---|---|
| 📈 What | Auto-scales **Pod count** |
| 📊 Based on | CPU, Memory, Custom, External metrics |
| ⏱️ Sync interval | 15 seconds (default) |
| 🧩 Needs | Metrics Server + Resource Requests |
| 📄 API | `autoscaling/v2` (recommended) |
| 🎯 Target objects | Deployment, ReplicaSet, StatefulSet |
| 🚫 Not supported | Scale to zero (native) |

---

## 📚 17. Recommended Practice Tasks

1. 🧪 Deploy a sample app with CPU requests/limits set.
2. 📈 Create an HPA targeting 50% CPU utilization.
3. 🔥 Generate load using `kubectl run -i --tty load-generator --image=busybox -- /bin/sh -c "while true; do wget -q -O- http://<service>; done"`.
4. 👀 Observe scaling with `kubectl get hpa -w`.
5. 🧊 Reduce load and observe scale-down behavior.

---

> 💡 **Tip for Students:** Always test HPA in a lab/sandbox cluster with load-testing tools before relying on it in production — tune `stabilizationWindowSeconds` and thresholds based on real traffic patterns.
