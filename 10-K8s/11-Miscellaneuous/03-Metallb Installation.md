# 🌐 MetalLB Installation Guide (Kubernetes)

> A complete, structured guide to installing and configuring **MetalLB** — a load-balancer implementation for bare-metal Kubernetes clusters.

---

## 📖 1. What is MetalLB?

Kubernetes does not provide a native implementation of network load balancers (**Services of type `LoadBalancer`**) for bare-metal clusters. Cloud providers (AWS, GCP, Azure) offer this out of the box, but on-prem/bare-metal clusters do not.

**MetalLB** fills this gap by:
- 🔗 Assigning external IP addresses to `LoadBalancer` type Services
- 📡 Advertising those IPs to the network using **Layer 2 (ARP/NDP)** or **BGP**
- ⚙️ Working seamlessly with kube-proxy / CNI plugins

---

## ✅ 2. Prerequisites

Before installing MetalLB, ensure the following:

| Requirement | Details |
|---|---|
| 🖥️ Cluster Type | Bare-metal or on-prem Kubernetes cluster |
| ☸️ Kubernetes Version | v1.13.0 or later |
| 🌐 Network Access | A pool of unused IP addresses on your LAN |
| 🚫 kube-proxy Mode | Must **not** be in strict ARP disabled state (see below) |
| 🔌 CNI Compatibility | Flannel, Calico, Cilium, Weave — all supported (check mode compatibility) |
| 🔑 Cluster Access | `kubectl` configured with admin access |

### ⚠️ Enable Strict ARP (Required for kube-proxy in IPVS mode)

```bash
kubectl edit configmap -n kube-system kube-proxy
```

Set:
```yaml
strictARP: true
```

Or apply directly:
```bash
kubectl get configmap kube-proxy -n kube-system -o yaml | \
sed -e "s/strictARP: false/strictARP: true/" | \
kubectl apply -f - -n kube-system
```

---

## 📦 3. Installation Methods

MetalLB can be installed via **Manifest**, **Helm**, or **kubectl kustomize**. Choose one method.

### 🅰️ Method 1: Install via Kubernetes Manifest

```bash
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.8/config/manifests/metallb-native.yaml
```

> 🔎 Replace `v0.14.8` with the [latest stable release](https://github.com/metallb/metallb/releases).

### 🅱️ Method 2: Install via Helm

```bash
# Add the MetalLB Helm repository
helm repo add metallb https://metallb.github.io/metallb
helm repo update

# Create a dedicated namespace
kubectl create namespace metallb-system

# Install MetalLB
helm install metallb metallb/metallb -n metallb-system
```

### 🅲️ Method 3: Install via Kustomize

```bash
kubectl apply -k github.com/metallb/metallb/config/native?ref=v0.14.8
```

---

## 🔍 4. Verify Installation

Check that all MetalLB pods are running:

```bash
kubectl get pods -n metallb-system
```

Expected output:
```
NAME                          READY   STATUS    RESTARTS   AGE
controller-6d4c9d8f9c-xxxxx   1/1     Running   0          1m
speaker-xxxxx                 1/1     Running   0          1m
speaker-yyyyy                 1/1     Running   0          1m
```

- 🧠 **controller** → Handles IP address assignment
- 📢 **speaker** (DaemonSet) → Advertises assigned IPs on each node

---

## ⚙️ 5. Configure MetalLB

MetalLB requires two Custom Resources: an **IPAddressPool** and an **L2Advertisement** (or **BGPAdvertisement**).

### 🧩 5.1 Define an IP Address Pool

Create `ipaddresspool.yaml`:

```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: first-pool
  namespace: metallb-system
spec:
  addresses:
    - 192.168.1.240-192.168.1.250
```

Apply it:
```bash
kubectl apply -f ipaddresspool.yaml
```

### 🧭 5.2 Layer 2 Mode (Simplest — ARP/NDP based)

Create `l2advertisement.yaml`:

```yaml
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: l2-advert
  namespace: metallb-system
spec:
  ipAddressPools:
    - first-pool
```

Apply it:
```bash
kubectl apply -f l2advertisement.yaml
```

> 💡 **Layer 2 mode** is easiest to set up — no router configuration required. Best for small/home labs and simple on-prem setups.

### 🛰️ 5.3 BGP Mode (Advanced — for production networks)

Create `bgpadvertisement.yaml`:

```yaml
apiVersion: metallb.io/v1beta1
kind: BGPPeer
metadata:
  name: sample-peer
  namespace: metallb-system
spec:
  myASN: 64500
  peerASN: 64501
  peerAddress: 192.168.1.1
---
apiVersion: metallb.io/v1beta1
kind: BGPAdvertisement
metadata:
  name: bgp-advert
  namespace: metallb-system
spec:
  ipAddressPools:
    - first-pool
```

Apply it:
```bash
kubectl apply -f bgpadvertisement.yaml
```

> 💡 **BGP mode** offers true load balancing across nodes and is recommended for production-grade networks with BGP-capable routers.

---

## 🧪 6. Test MetalLB with a Sample Service

Deploy a test application and expose it via `LoadBalancer`:

```bash
kubectl create deployment nginx-demo --image=nginx
kubectl expose deployment nginx-demo --port=80 --type=LoadBalancer
```

Check the assigned external IP:

```bash
kubectl get svc nginx-demo
```

Expected output:
```
NAME         TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)        AGE
nginx-demo   LoadBalancer   10.96.10.20    192.168.1.240    80:31234/TCP   10s
```

✅ If an `EXTERNAL-IP` from your defined pool appears (not `<pending>`), MetalLB is working correctly.

---

## 🛠️ 7. Troubleshooting

| Issue | Possible Cause | Fix |
|---|---|---|
| 🔴 `EXTERNAL-IP` stuck at `<pending>` | No IPAddressPool/Advertisement configured | Apply pool + advertisement CRs |
| 🔴 IP not reachable | Strict ARP not enabled | Re-check kube-proxy configmap |
| 🔴 Speaker pods crashing | Port conflicts or RBAC issues | Check `kubectl logs -n metallb-system` |
| 🔴 Duplicate IP on network | Overlapping IP pool with DHCP range | Choose a reserved, unused IP range |
| 🔴 BGP session not established | Peer ASN/IP mismatch | Verify router BGP config matches `BGPPeer` |

Check logs for debugging:
```bash
kubectl logs -n metallb-system -l app=metallb,component=speaker
kubectl logs -n metallb-system -l app=metallb,component=controller
```

---

## 🗑️ 8. Uninstall MetalLB

### Via Manifest
```bash
kubectl delete -f https://raw.githubusercontent.com/metallb/metallb/v0.14.8/config/manifests/metallb-native.yaml
```

### Via Helm
```bash
helm uninstall metallb -n metallb-system
kubectl delete namespace metallb-system
```

---

## 📌 9. Quick Reference Summary

| Step | Command |
|---|---|
| 1️⃣ Enable strict ARP | `kubectl edit configmap -n kube-system kube-proxy` |
| 2️⃣ Install MetalLB | `kubectl apply -f metallb-native.yaml` |
| 3️⃣ Verify pods | `kubectl get pods -n metallb-system` |
| 4️⃣ Create IP pool | `kubectl apply -f ipaddresspool.yaml` |
| 5️⃣ Create advertisement | `kubectl apply -f l2advertisement.yaml` |
| 6️⃣ Test | `kubectl expose deployment ... --type=LoadBalancer` |

---

## 📚 10. References

- 🔗 Official Docs: https://metallb.universe.tf/
- 🔗 GitHub Repo: https://github.com/metallb/metallb
- 🔗 Release Notes: https://github.com/metallb/metallb/releases

---

> 📝 **Note:** Always match the MetalLB version to your Kubernetes cluster's compatibility matrix before installing in production.
