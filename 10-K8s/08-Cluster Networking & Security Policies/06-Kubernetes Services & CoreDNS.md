# 🧭 Kubernetes Services & CoreDNS

A **Service** is a stable networking abstraction that sits in front of a dynamic, ever-changing set of Pods. This guide covers the **three core Service types** (ClusterIP, NodePort, LoadBalancer), how **DNS resolution** works internally via **CoreDNS**, and practical patterns for **connecting apps to services** (like databases) and **troubleshooting** service connectivity.

---

## 🎯 1. Why Services Exist (Quick Recap)

- 🆔 Pods are **ephemeral** — they get new IPs every time they're recreated.
- 📈 A Deployment/ReplicaSet may run **multiple pod replicas**.
- ➡️ A **Service** provides a single **stable virtual IP (VIP)** and **DNS name** that automatically load-balances traffic across all healthy matching pods — so clients never need to track individual pod IPs.

---

## 🧩 2. Service Types

Kubernetes offers three primary Service types, each expanding accessibility outward — from **internal-only** to **fully external**.

### 🏠 2.1 ClusterIP (Default)

- 🔒 Exposes the Service on an **internal-only virtual IP**, reachable **only from within the cluster**.
- 🎯 Used for internal communication — e.g., a frontend pod talking to a backend pod, or an app talking to a database pod.
- 🚫 **Not accessible** from outside the cluster.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
    - port: 80
      targetPort: 8080
```

> 💡 If `type` is omitted entirely, Kubernetes defaults to `ClusterIP`.

---

### 🚪 2.2 NodePort

- 🌍 Exposes the Service on a **static port** (default range: **30000–32767**) on **every node's IP** in the cluster.
- 🔁 Internally, it **builds on top of ClusterIP** — a ClusterIP is still created, and the NodePort simply forwards external traffic into it.
- 📡 Accessible from **outside the cluster** via `<NodeIP>:<NodePort>`.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: NodePort
  selector:
    app: web
  ports:
    - port: 80          # ClusterIP port
      targetPort: 8080  # Pod port
      nodePort: 30080   # Exposed on every node
```

➡️ Access from outside: `curl http://<any-node-ip>:30080`

---

### ☁️ 2.3 LoadBalancer

- 🌐 Provisions an **external load balancer** (via the cloud provider — AWS ELB, GCP Load Balancer, Azure LB, etc.) that routes external traffic into the cluster.
- 🔁 Builds on top of **NodePort**, which itself builds on **ClusterIP** — so all three layers exist simultaneously under the hood.
- ✅ The standard way to expose a production service to the **public internet** on cloud-managed Kubernetes clusters.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: public-web-service
spec:
  type: LoadBalancer
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
```

> ⚠️ On **bare-metal / on-prem clusters** (with no cloud integration), `LoadBalancer` services stay in a **`<pending>`** external-IP state unless something like **MetalLB** is installed to provide the load-balancer functionality.

---

### 📊 2.4 Service Types Compared

| Type | 🔓 Accessible From | 🧱 Built On | 🎯 Typical Use Case |
|---|---|---|---|
| **ClusterIP** | Inside cluster only | — | Internal service-to-service traffic |
| **NodePort** | Outside cluster (via node IP + port) | ClusterIP | Dev/test external access, on-prem exposure |
| **LoadBalancer** | Public internet | NodePort → ClusterIP | Production external-facing apps (on cloud) |

---

## 🧾 3. How Services Track Pods: Endpoints

- A Service uses a **label selector** to find matching Pods (e.g., `app: backend`).
- Kubernetes maintains an **Endpoints** (or **EndpointSlice**) object listing the **current IPs of all matching, healthy Pods**.
- This list updates automatically as Pods scale up/down or are replaced — **the Service's VIP itself never changes**.

```bash
kubectl describe svc backend-service
# Look for:
# Endpoints: 10.244.1.5:8080, 10.244.2.7:8080
```

> ⚠️ **If a Service has no Endpoints listed, it cannot forward any traffic** — this is one of the most common causes of "service unreachable" issues (see Troubleshooting section below).

---

## 🌐 4. CoreDNS — Internal DNS Resolution

**CoreDNS** is the default DNS server running inside a Kubernetes cluster (as pods in `kube-system`), giving every Service (and optionally every Pod) a **resolvable DNS name**.

### 🏷️ 4.1 Service DNS Naming Convention

Every Service automatically gets a DNS record in the form:

```
<service-name>.<namespace>.svc.cluster.local
```

| Calling From | 📛 How to Reference the Service |
|---|---|
| Same namespace | `db-service` (short name) |
| Different namespace | `db-service.other-namespace` |
| Fully qualified (any namespace) | `db-service.other-namespace.svc.cluster.local` |

### ⚙️ 4.2 How Resolution Works Internally

1. Every Pod is configured (via its `/etc/resolv.conf`, injected by the kubelet) to use the **CoreDNS Service IP** as its DNS server.
2. Pod's `/etc/resolv.conf` also includes a **search path** so short names like `db-service` automatically expand to the full FQDN.
3. CoreDNS watches the Kubernetes API for Services/Pods and dynamically serves DNS records — **no manual DNS record management needed**.
4. The resolved name returns the Service's **ClusterIP** (stable VIP), not individual pod IPs.

```bash
# Inspect a pod's DNS config
kubectl exec -it <pod-name> -- cat /etc/resolv.conf
```

Example output:
```
nameserver 10.96.0.10
search default.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

### 🔎 4.3 Pod DNS Records (Optional)
CoreDNS can also resolve individual **Pod IPs** directly (less common), in the form:
```
<pod-ip-with-dashes>.<namespace>.pod.cluster.local
```

---

## 🔐 5. Real-World Pattern: Connecting an App to a Database via a Service

A very common real-world use case: an application Pod needs to connect to a **database** running as another Pod/Service in the cluster. Rather than hardcoding the database's Pod IP (which changes), the app should connect using the **Service's stable identity and credentials**:

| 🔑 Credential Type | 📌 What It Maps To |
|---|---|
| **Host** | Service name (or ClusterIP) of the database |
| **Username** | Database service's configured username |
| **Password** | Database service's configured auth password |

### 🧬 5.1 How This Appears in the Pod Spec

These values are typically injected into the application Pod as **environment variables**, where the **Pod's ENV variable name** should map to the **corresponding DB Service credential**:

| 🧾 ENV Variable Name (in App Pod) | 🎯 Maps To (DB Service Credential) |
|---|---|
| `DB_Host` | Service Name (e.g., `mysql-service`) |
| `DB_User` | Service Username |
| `DB_Password` | Service Auth Password |

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  containers:
  - name: web-app
    image: myapp:latest
    env:
    - name: DB_Host
      value: "mysql-service"
    - name: DB_User
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: username
    - name: DB_Password
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: password
```

### 🔍 5.2 Verifying Injected Credentials

These environment variables can always be verified by describing the running Pod or Deployment:

```bash
kubectl describe pod web-app
# Look under the "Environment:" section
```

> 💡 **Best practice:** Store `DB_User` / `DB_Password` in a **Secret** (as shown above) rather than plain values, and reference the **Service name** (not a hardcoded IP) for `DB_Host` — so it keeps working even if the database Pod is rescheduled.

---

## 🛠️ 6. Troubleshooting Service Connectivity

When an application or Service seems unreachable, follow this systematic checklist:

### ✅ 6.1 Pre-Checks
- 🟢 Confirm the Pod's status shows **`1/1` Running** (i.e., all containers in the pod are ready) — not `0/1`, `CrashLoopBackOff`, or `Pending`.
- 🔗 Confirm the Service has **Endpoints mapped** to the desired Pods (not empty).

### 🔬 6.2 Step-by-Step Troubleshooting Flow

**Step 1 — Try reaching the app directly:**
```bash
curl http://<web-service-ip>:<node-port>/
```
➡️ If this fails (e.g., "not reachable"), proceed to the next steps.

**Step 2 — Check whether the Service has Endpoints assigned:**
```bash
kubectl describe svc <svc-name> -n <namespace-name> | grep Endpoints
```
- ❌ **No IPs listed under `Endpoints`** → the Service isn't matching any Pods. This is a major red flag.

**Step 3 — Match the Service selector against Pod labels:**
- Compare the Service's `spec.selector` fields with the **labels** on the Pods that should be backing it.
- A mismatch here (e.g., `app: web` on the Service vs. `app: webapp` on the Pod) is one of the **most common causes** of a Service having zero Endpoints.

```bash
kubectl get svc <svc-name> -o yaml | grep -A3 selector
kubectl get pods --show-labels
```

**Step 4 — Check the Pod's status and logs:**
```bash
kubectl get pods -n <namespace-name>
kubectl logs <pod-name> -n <namespace-name>
```
- Look for crash loops, failed health checks, or application errors preventing the pod from serving traffic.

### 🧭 6.3 Troubleshooting Flow Summary

```
curl fails
   │
   ▼
Check Service → Endpoints empty? ──▶ Yes ──▶ Check Selector vs Pod Labels (mismatch?)
   │ No                                            │
   ▼                                                ▼
Check Pod status (1/1 Running?)             Fix selector/labels, re-check Endpoints
   │ No                                            
   ▼
Check Pod logs for errors / crash reasons
```

---

## 📚 7. Summary Cheat Sheet

| Concept | 🔑 Key Point |
|---|---|
| ClusterIP | Internal-only stable VIP; default Service type |
| NodePort | Exposes a static port on every node; built on ClusterIP |
| LoadBalancer | Provisions external cloud LB; built on NodePort → ClusterIP |
| Endpoints/EndpointSlice | Tracks live Pod IPs backing a Service |
| CoreDNS | Cluster DNS server resolving Service/Pod names to IPs |
| Service DNS format | `<service>.<namespace>.svc.cluster.local` |
| DB connection pattern | Use Service name + Secret-based credentials, not hardcoded pod IPs |
| Troubleshooting priority | Pod `1/1` status → Service Endpoints → Selector/Label match → Pod logs |

> 🎓 **Key takeaway:** ClusterIP, NodePort, and LoadBalancer form a layered hierarchy of exposure (internal → node-level → public), all backed by the same Endpoints mechanism. CoreDNS makes these Services discoverable by name instead of IP — and when troubleshooting connectivity, always work outward: **Pod readiness → Endpoints → Selector/label match → Pod logs.**
