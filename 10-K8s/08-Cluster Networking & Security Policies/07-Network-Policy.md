# 🛡️ Kubernetes NetworkPolicy — Ingress/Egress Isolation Rules

By default, Kubernetes networking is **completely open** — any pod can talk to any other pod, with no restrictions. A **NetworkPolicy** is how you introduce **firewall-like rules** at the pod level, controlling exactly which traffic is allowed **in** (ingress) and **out** (egress).

---

## 🔓 1. Default Behavior — Allow All

- 🌐 Out of the box, Kubernetes **allows all traffic** between all pods — there is no isolation whatsoever.
- 🚧 The moment you apply **any** `NetworkPolicy` that selects a pod, that pod becomes **isolated** for the direction(s) covered by that policy (`Ingress` and/or `Egress`).
- 🔒 **Default Deny principle:** once a NetworkPolicy applies to a pod, **any traffic not explicitly allowed by a rule is denied** — NetworkPolicies are purely **allow-list** based; there's no "deny" rule type.

> ⚠️ This is a critical mental model: NetworkPolicies don't add blocks on top of an open network — applying **one** policy to a pod flips that pod's traffic (for the matched direction) from **"allow everything"** to **"deny everything except what's explicitly permitted."**

---

## 🔌 2. Prerequisite: CNI Plugin Support

NetworkPolicy is just a **Kubernetes API object** — enforcing it is entirely the responsibility of the **CNI plugin**.

- ✅ **Supported by:** Calico, Cilium, Weave Net, and other policy-aware CNI plugins.
- ❌ **Not enforced by:** plugins that don't implement policy support (e.g., a basic Flannel-only setup) — in that case, applying a `NetworkPolicy` object will be **silently accepted by the API server but have zero effect** on actual traffic.

> 💡 Always confirm your cluster's CNI plugin supports NetworkPolicy **before** relying on it for security — otherwise you may have a false sense of protection.

---

## 🧱 3. Anatomy of a NetworkPolicy

Every `NetworkPolicy` object is built from four key parts:

| 🧩 Field | 📝 Purpose |
|---|---|
| `podSelector` | Which pods this policy **applies to** (the "protected" pods) |
| `policyTypes` | Whether this policy governs `Ingress`, `Egress`, or both |
| `ingress` | Rules describing **allowed incoming** traffic |
| `egress` | Rules describing **allowed outgoing** traffic |

> 🔎 An **empty `podSelector: {}`** matches **all pods** in the namespace.

---

## ⬇️ 4. Ingress Rule Example — Allow HTTP/HTTPS from Frontend Pods

This policy allows traffic **into** all pods in the `default` namespace, but **only** from pods labeled `role: frontend`, and **only** on ports `80` and `443`.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-http-https-ingress
  namespace: default
spec:
  podSelector: {}
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 80
    - protocol: TCP
      port: 443
  policyTypes:
  - Ingress
```

### 🔍 Breakdown

| Field | 📖 Meaning |
|---|---|
| `podSelector: {}` | Applies to **all pods** in the `default` namespace |
| `ingress.from.podSelector` | Only allow traffic **originating from pods** with label `role: frontend` |
| `ports` | Only allow **TCP port 80 (HTTP)** and **TCP port 443 (HTTPS)** |
| `policyTypes: [Ingress]` | This policy only governs **incoming** traffic — egress remains unaffected/open |

➡️ **Net effect:** Any pod in `default` namespace will **reject all incoming traffic** except HTTP/HTTPS requests coming specifically from `role: frontend` pods.

---

## ⬆️ 5. Egress Rule Example — Allow Traffic to a Specific IP Range

This policy allows traffic **leaving** pods in the `default` namespace only if it's headed to a specific external CIDR range.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-egress-to-ip-range
  namespace: default
spec:
  podSelector: {}
  egress:
  - to:
    - ipBlock:
        cidr: 192.168.1.0/24
  policyTypes:
  - Egress
```

### 🔍 Breakdown

| Field | 📖 Meaning |
|---|---|
| `podSelector: {}` | Applies to **all pods** in the `default` namespace |
| `egress.to.ipBlock.cidr` | Only allow **outbound traffic** destined for `192.168.1.0/24` |
| `policyTypes: [Egress]` | This policy only governs **outgoing** traffic — ingress remains unaffected/open |

➡️ **Net effect:** Pods in `default` namespace can **only send traffic** to hosts within `192.168.1.0/24` — all other outbound destinations are blocked.

---

## 🧭 6. Selector Types You Can Use in `from` / `to`

NetworkPolicy rules aren't limited to just pod labels or IP ranges — you can combine several selector types:

| Selector | 🎯 Matches |
|---|---|
| `podSelector` | Pods matching given labels **within the same namespace** |
| `namespaceSelector` | All pods in namespaces matching given labels |
| `ipBlock` | A CIDR range of IP addresses (with optional `except` sub-ranges) |

```yaml
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          env: production
    - podSelector:
        matchLabels:
          role: frontend
```
> 💡 When a rule combines `namespaceSelector` **and** `podSelector` in the **same** list item, it matches pods with that label **only within** namespaces matching that label. Listed as **separate items**, it's a logical **OR** (either condition allows traffic).

---

## 🚫 7. Common Pattern: Deny-All Policies

A frequently used starting point for hardening a namespace is a **default deny-all** policy — blocking everything, then selectively opening up what's needed.

### 🔒 7.1 Deny All Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```
➡️ No `ingress` rules specified = **nothing is allowed in**.

### 🔒 7.2 Deny All Egress
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Egress
```
➡️ No `egress` rules specified = **nothing is allowed out**.

### 🔒🔒 7.3 Deny All Ingress **and** Egress
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

> 🧠 **Best practice:** Start with a deny-all policy per namespace, then layer additional NetworkPolicies to **explicitly allow** only the traffic your applications actually need (least-privilege networking).

---

## 🧪 8. Important Real-World Gotcha: Don't Forget DNS!

If you apply a **deny-all egress** policy, pods will **also lose the ability to resolve DNS** (since DNS queries to CoreDNS are themselves outbound traffic) — breaking service discovery entirely.

✅ Always pair a deny-all egress policy with an explicit **allow rule for DNS** (typically UDP/TCP port `53` to the `kube-system` namespace running CoreDNS):

```yaml
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
```

---

## 🧾 9. Applying & Verifying NetworkPolicies

```bash
# 📥 Apply a policy
kubectl apply -f allow-http-https-ingress.yaml

# 📋 List policies in a namespace
kubectl get networkpolicy -n default

# 🔍 Inspect a specific policy
kubectl describe networkpolicy allow-http-https-ingress -n default
```

> ⚠️ `kubectl describe` will show you the rules, but it **won't tell you if your CNI plugin actually enforces them** — always test connectivity directly (e.g., `kubectl exec` + `curl`/`nc` from an allowed and a disallowed pod) to confirm real-world behavior.

---

## 📚 10. Summary Cheat Sheet

| Concept | 🔑 Key Point |
|---|---|
| Default cluster behavior | All traffic allowed between all pods |
| Once a NetworkPolicy applies | That pod's matched direction becomes **default deny** except explicit allows |
| `policyTypes` | Declares whether the policy governs `Ingress`, `Egress`, or both |
| `podSelector: {}` | Matches **all pods** in the namespace |
| `ipBlock` | Restrict traffic to/from specific CIDR ranges |
| `namespaceSelector` | Restrict traffic to/from pods in matching namespaces |
| Deny-all pattern | Empty `ingress`/`egress` list + matching `policyTypes` = block everything |
| DNS gotcha | Deny-all egress breaks DNS unless port 53 to `kube-system` is explicitly allowed |
| CNI requirement | Must use a **policy-aware** plugin (Calico, Cilium, Weave, etc.) — otherwise policies have **no effect** |

> 🎓 **Key takeaway:** NetworkPolicies are **allow-list only** — applying even one policy to a pod switches that traffic direction from fully open to default-deny-except-specified. They're purely declarative Kubernetes objects, so their real enforcement depends entirely on running a **policy-capable CNI plugin** — without one, your NetworkPolicy YAML is just inert configuration.
