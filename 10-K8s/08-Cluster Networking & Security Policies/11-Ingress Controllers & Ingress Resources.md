# 🚦 Ingress Controllers & Ingress Resources (Layer 7 Routing)

Ingress brings **Layer 7 (HTTP/HTTPS) load balancing** to Kubernetes — routing traffic based on URL paths, hostnames, and handling SSL — without needing a separate cloud load balancer for every single service.

---

## ❓ 1. The Problem Ingress Solves

Imagine a website with two pages — **Page 1** (`URL-1`) and **Page 2** (`URL-2`) — each served by a different set of pods:

- 🌐 **Page 1** → served by **Pod1** (and scales out automatically as traffic increases).
- 🌐 **Page 2** → served by **Pod2** (and scales out automatically as traffic increases).

### 😫 Without Ingress
- Each page's pods need **their own Load Balancer** to distribute traffic (Load-Balancer-1 for Page1, Load-Balancer-2 for Page2).
- 🔐 SSL/HTTPS needs to be configured **separately, at every layer**.
- 📈 As the number of pages/services **grows**, this setup becomes increasingly **complex, expensive, and hard to secure** — every new service needs its own external load balancer and its own SSL configuration.

### ✅ With Ingress
- A **single entry point** balances traffic to the correct backend service **based on the type of request** (path or hostname).
- 🔒 **SSL/TLS termination** can be centralized and implemented **once, at the Ingress layer**, instead of per-service.

---

## 🧭 2. What Is Ingress?

> 📖 **Ingress = Layer 7 Load Balancer for Kubernetes.**

- It understands **HTTP/HTTPS** — meaning it can route based on **URL paths** and **hostnames/domain names**, not just IP/port like a Layer 4 load balancer.
- ⚠️ **Important:** Ingress **does not replace** the need to expose something to the outside world — you **still need** to expose the Ingress itself using a **Service** (like `NodePort`) or a **cloud-native load balancer** (like an AWS Application Load Balancer).

```
Internet ──▶ [NodePort / Cloud LB] ──▶ Ingress Controller ──▶ Service A / Service B / Service C
```

---

## 🏗️ 3. Ingress Is Deployed in Two Steps

### 🥇 Step 1 — Ingress Controller
- An Ingress Controller is a **supporting solution** — essentially a **reverse-proxy / load-balancer** application — deployed as pods in the cluster.
- Popular Ingress Controller implementations: **NGINX**, **HAProxy**, **Traefik**, **Contour**, **Istio**, etc.
- ⚠️ **Not deployed by default** — a Kubernetes cluster has **no** Ingress Controller out of the box. You must **manually deploy** one.

### 🥈 Step 2 — Ingress Resources
- Once a controller exists, you define **Ingress Resources** — the actual **rules/configuration**: which paths or hosts route to which backend service, SSL certificate settings, etc.
- Ingress Resources are created via **definition files (YAML)**, the same way you create Pods, Services, or Deployments.

---

## 📄 4. Deploying an Ingress Controller (NGINX Example)

### 🧾 4.1 Ingress Controller Deployment YAML

```yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-ingress-controller
spec:
  replicas: 1
  selector:
    matchLabels:
      name: nginx-ingress
  template:
    metadata:
      labels:
        name: nginx-ingress
    spec:
      containers:
        - name: nginx-ingress-controller
          image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.21.0
          args:
            - /nginx-ingress-controller                              # 🏁 Command to start the ingress service once the pod is up
            - --configmap=$(POD_NAMESPACE)/nginx-configuration
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          ports:
            - name: http
              containerPort: 80
            - name: https
              containerPort: 443
```

### 🌍 4.2 Exposing the Ingress Controller (Service)

The controller pods need to be reachable from outside the cluster — exposed via a `Service`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
      name: http
    - port: 443
      targetPort: 443
      protocol: TCP
      name: https
  selector:
    name: nginx-ingress
```

### 🧰 4.3 Additional Supporting Objects Required

Beyond the Deployment and Service above, a fully functional Ingress Controller setup also needs:

| 🧩 Object | 🎯 Purpose |
|---|---|
| **ConfigMap** | Configures parameters like **error log path**, **keep-alive** (health-checking pods to know if they can serve traffic), and **SSL** settings — decoupled from the controller's own definition, passed in as a separate configuration object. |
| **ServiceAccount + Role + RoleBinding** | Grants the Ingress Controller the **permissions** it needs to monitor pod status, route traffic correctly, and perform other cluster-level tasks. |
| **Service** | Exposes the Ingress Controller to the outside world (as shown above). |

---

## 📐 5. Ingress Resources — Defining Routing Rules

> 📖 **Ingress Resources** are the set of **rules/configurations** applied on top of an Ingress Controller — they tell it *how* to route incoming requests.

### 🛣️ 5.1 Path-Based Routing

Route based on the **URL path** — e.g., `/wear` goes to one service, `/watch` goes to another:

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-wear-watch
spec:
  rules:
    - http:
        paths:
          - path: /wear
            backend:
              serviceName: wear-service
              servicePort: 80
          - path: /watch
            backend:
              serviceName: watch-service
              servicePort: 80
```

### 🎯 5.2 Single Backend (No Rules — Catch-All)

If there's only **one** backend service and no path/host-based splitting is needed, you can skip `rules` entirely and just define a default backend:

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-wear
spec:
  backend:
    serviceName: wear-service
    servicePort: 80
```

### 🌐 5.3 Domain/Host-Based Routing

Route based on the **hostname** in the request (e.g., `wear.my-online-store.com` vs `watch.my-online-store.com`) — useful when multiple applications share the same Ingress Controller but serve different domains:

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-wear-watch
spec:
  rules:
    - host: wear.my-online-store.com
      http:
        paths:
          - backend:
              serviceName: wear-service
              servicePort: 80
    - host: watch.my-online-store.com
      http:
        paths:
          - backend:
              serviceName: watch-service
              servicePort: 80
```

---

## 🆕 6. Newer Kubernetes API Changes for Ingress

Newer Kubernetes versions changed the Ingress API — moving from `extensions/v1beta1` to `networking.k8s.io/v1`, with a few structural changes.

### 🔄 6.1 Old vs New Syntax

**🕰️ Old (`extensions/v1beta1`):**
```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-wear-watch
spec:
  rules:
    - http:
        paths:
          - path: /wear
            backend:
              serviceName: wear-service
              servicePort: 80
          - path: /watch
            backend:
              serviceName: watch-service
              servicePort: 80
```

**🆕 New (`networking.k8s.io/v1`):**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wear-watch
spec:
  rules:
    - http:
        paths:
          - path: /wear
            pathType: Prefix
            backend:
              service:
                name: wear-service
                port:
                  number: 80
          - path: /watch
            pathType: Prefix
            backend:
              service:
                name: watch-service
                port:
                  number: 80
```

### 📋 6.2 Key Differences

| 🕰️ Old (`extensions/v1beta1`) | 🆕 New (`networking.k8s.io/v1`) |
|---|---|
| `backend.serviceName` | `backend.service.name` |
| `backend.servicePort` | `backend.service.port.number` |
| No `pathType` required | ✅ **`pathType` is now required** (e.g., `Prefix`, `Exact`, `ImplementationSpecific`) |

---

## ⌨️ 7. Imperative Method — Creating an Ingress Resource

Instead of writing a full YAML file, you can create an Ingress Resource directly via `kubectl`:

```bash
kubectl create ingress <ingress-name> --rule="host/path=service:port"
```

**Example:**
```bash
kubectl create ingress ingress-test --rule="wear.my-online-store.com/wear*=wear-service:80"
```

---

## 🔍 8. Inspecting & Managing Ingress Resources

### 📋 8.1 Listing Ingress Resources Across All Namespaces

```bash
kubectl get ingress -A
```

- 🌟 If the `HOSTS` column shows **`*`**, it means **any host/domain** can access the service through that Ingress — i.e., no specific hostname restriction is applied.
- The **host entry** defines the **domain name** users must use to reach the application; `*` means users from **any domain** can reach it via this Ingress.

### 🔬 8.2 Describing an Ingress Resource

```bash
kubectl describe ingress ingress-wear-watch -n app-space
```

➡️ If an incoming request **doesn't match** any of the defined rules (paths/hosts), it's routed to the **default backend** specified in the Ingress resource (if configured).

### ✏️ 8.3 Editing an Existing Ingress Resource

To change a path (or any other rule) in an existing Ingress:

```bash
kubectl edit ingress ingress-wear-watch -n app-space
```

> ✅ **No need to delete and recreate anything** — as soon as the edit is saved, traffic is **automatically redirected** according to the updated configuration.

---

## 🧪 9. Practical Walkthrough — Creating an Ingress for an Existing App

Before creating an Ingress rule, you need an existing **Deployment** and **Service** that are already linked (the Service's selector matches the Deployment's pod labels):

```bash
kubectl get deploy -n critical-space
# Name = webapp-pay

kubectl get svc -n critical-space
# Name = pay-service
# Port = 8282
# Type = ClusterIP
```

### ➕ 9.1 Create the Ingress Rule

```bash
kubectl create ingress -h    # 🆘 view help/usage for the imperative create command

kubectl create ingress ingress-pay -n critical-space --rule="/pay=pay-service:8282"
```

### 🏷️ 9.2 Add Annotations (e.g., Rewrite Target)

```bash
kubectl edit ingress ingress-pay -n critical-space
```

Add the following under the `metadata` section:
```yaml
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
```

> 💡 The **`rewrite-target`** annotation is an NGINX-Ingress-specific setting that **rewrites the incoming path** before forwarding it to the backend service — commonly used so the backend service always receives requests at `/` regardless of the original Ingress path (e.g., `/pay` → forwarded internally as `/`).

---

## 🏁 10. Full End-to-End Setup Walkthrough

This section walks through **manually building an entire Ingress Controller setup from scratch** — namespace, supporting objects, controller, exposing it, and finally creating an application-facing Ingress Resource.

```bash
# 1️⃣ Create a dedicated namespace for Ingress components
kubectl create namespace ingress-space

# 2️⃣ Create the ConfigMap for controller configuration
kubectl create configmap nginx-configuration -n ingress-space

# 3️⃣ Create the ServiceAccount for the controller's permissions
kubectl create serviceaccount ingress-serviceaccount -n ingress-space

# 4️⃣ Verify Roles & RoleBindings exist (created as part of controller setup)
kubectl get roles -n ingress-space
kubectl get rolebindings -n ingress-space

# 5️⃣ Confirm the Ingress Controller Deployment is present
kubectl get deploy -n ingress-space
# Output: ingress-controller

# 6️⃣ Expose the Ingress Controller Deployment via a Service
kubectl expose deploy ingress-controller -n ingress-space \
  --name=ingress --port=80 --target-port=80 --type=NodePort

# 7️⃣ Check the auto-assigned NodePort
kubectl get svc -n ingress-space
# Output: Port = 80:32741/TCP

# 8️⃣ (Optional) Change the NodePort to a specific desired port
kubectl edit svc ingress -n ingress-space
# Change nodePort from 32741 to 30080

# 9️⃣ Check the application's existing Service (that Ingress will route to)
kubectl get svc -n app-space

# 🔟 Create the Ingress Resource with multiple path-based rules
kubectl create ingress -n app-space ingress-wear-watch \
  --rule="/wear=wear-service:8080" \
  --rule="/watch=video-service:8080"

# 1️⃣1️⃣ Edit the Ingress to add helpful annotations
kubectl edit ingress ingress-wear-watch -n app-space
```

Add the following under the `metadata` section:
```yaml
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
```

> 🏷️ **`ssl-redirect: "false"`** disables NGINX's default behavior of automatically redirecting all HTTP traffic to HTTPS — useful in test/dev environments where SSL isn't yet configured.

---

## 📚 11. Summary Cheat Sheet

| Concept | 🔑 Key Point |
|---|---|
| Ingress | Layer 7 (HTTP/HTTPS) load balancer / smart router for Kubernetes |
| Still needs exposure | Ingress itself must be exposed via NodePort / Cloud LB |
| Ingress Controller | The actual proxy software (NGINX, HAProxy, Traefik, etc.) — not installed by default |
| Ingress Resource | YAML rules defining path/host-based routing on top of a controller |
| Path-based routing | Different paths (`/wear`, `/watch`) → different backend services |
| Host-based routing | Different domains (`wear.site.com`, `watch.site.com`) → different services |
| `pathType` | Required field in newer API (`networking.k8s.io/v1`) |
| `*` under HOSTS | Ingress accepts requests from **any** domain |
| No matching rule | Falls back to the **default backend** |
| Editing Ingress | `kubectl edit ingress` — no need to delete/recreate, updates apply live |
| `rewrite-target` annotation | Rewrites the request path before forwarding to backend |
| `ssl-redirect` annotation | Controls whether HTTP is force-redirected to HTTPS |
| Supporting objects needed | ConfigMap, ServiceAccount, Role, RoleBinding, Service |

> 🎓 **Key takeaway:** Ingress separates *how traffic is routed* (Ingress Resources — paths/hosts/SSL rules) from *what actually processes it* (the Ingress Controller — NGINX, HAProxy, etc.), giving you a single, centralized, Layer 7-aware entry point instead of a tangle of per-service load balancers.
