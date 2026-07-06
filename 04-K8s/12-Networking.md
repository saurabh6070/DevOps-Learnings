# 🌐 Kubernetes Networking Deep Dive

## 📘 1. Controllers and Services Overview
Controllers in Kubernetes ensure the desired state of the cluster is maintained.

 - **Pod Creation**: The **kubelet** listens to requests and deploys Pods on nodes, guided by the scheduler.  
 - **Service Creation**: The **kube-proxy** listens to service requests and configures IPTables rules to enable communication.  
 - **Ingress Creation**: Requires an **Ingress Controller**. Functions like a Load Balancer, supports path/host-based routing, adds API Gateway features, and enterprise-level security.

---

## 🔧 2. Services in Kubernetes
Pods are ephemeral — their IPs change when recreated or scaled. Services provide a **stable endpoint** for Pod communication.

### 🔹 How Services Work
- Services map to **Endpoints** using label selectors.  
- An Endpoint object is automatically created with the same name as the Service.  
- Endpoints store the IPs of Pods serving that Service.  
- Service discovery ensures traffic is routed to the correct Pods.

---

## 📊 3. Types of Services

| Service Type | Ports | Scope | Notes |
|--------------|-------|-------|-------|
| **ClusterIP** | Port = Service port | Internal only | Default type. TargetPort = Pod port. |
| **NodePort** | Port = Service port | External access | NodePort range = 30000–32767. Optional; if not specified, Kubernetes assigns one. |
| **LoadBalancer** | Port = Service port | External access | Integrates with cloud provider load balancers. |

---

## 🗂️ 4. Service Examples

### ClusterIP Example

**Deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mydeployment
spec:
  replicas: 1
  selector:
    matchLabels:
      name: deployment
  template:
    metadata:
      labels:
        name: deployment
    spec:
      containers:
      - name: c00
        image: httpd
        ports:
        - containerPort: 80
```
**Service-ClusterIP.yaml**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: demoservice
spec:
  ports:
    - port: 80
      targetPort: 80
  selector:
    name: deployment
  type: ClusterIP
```

### NodePort Example

**Deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mydeployment
spec:
  replicas: 1
  selector:
    matchLabels:
      name: deployment
  template:
    metadata:
      labels:
        name: deployment
    spec:
      containers:
      - name: c00
        image: httpd
        ports:
        - containerPort: 80
```

**Service-NodePort.yaml**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: demoservice
spec:
  ports:
    - port: 80
      targetPort: 80
  selector:
    name: deployment
  type: NodePort
```

---

## ⚡ 5. Service IP Assignment

 - Pod IPs are assigned by CNI plugins (e.g., Weave Net).
 - Service IPs are assigned by kube-proxy.
 - Services are cluster-wide virtual objects — they don’t exist on nodes physically.
 - IPTables rules forward traffic from Service IP+Port to Pod IPs.
 - Check rules:

```bash
kubectl get pods -o wide
kubectl get svc
iptables -L -t nat | grep <service-name>
```

In the output, we can relate that any traffic which comes on the IP:port of the Service must be redirected to the IP of the Pod to which the service is mapped with.
Also, we can get the same result in the file -
```bash
cat /var/log/kube-proxy.log
```

 - Proxy modes:

```bash
kube-proxy --proxy-mode [userspace | iptables | ipvs]
(Default: iptables)
```

 - Service IP range:

```bash
kube-apiserver --service-cluster-ip-range ipNet
## Default: 10.0.0.0/24

ps aux | grep -i kube-api-server
## check for the parametr --service-cluster-ip-range in the output
```

---

## 🖥️ 6. Node and Pod Networking
### Node Network: Check internal IPs and masks.

```bash
kubectl get nodes
ip a
```

### Pod Network Range:

```bash
kubectl get all --all-namespaces
kubectl logs weave-net-<pod> -n kube-system | grep ipalloc-range
```

The IP-Range allocated to Pods(in kubelet) and IP-Range allocated to Services(in kube-api-server) must no overlap.

---

## 🗂️ 7. Namespaces and DNS

 - All objects in a namespace are grouped under a subdomain - namespace.
 - Services are grouped under subdomain - svc.
 - Accessing services:

   **Same namespace:**
   ```yaml
   curl http://service-name
   ```
   
    **Different namespace:** 
   ```yaml
   curl http://service-name.namespace-name
   ```
   
    **External:** 
   ```yaml
   curl http://service-name.namespace-name.svc.cluster.local
   ```

 - Example:
**Service:** job in namespace ola → job.ola.svc.cluster.local
**Pod:** testjob in namespace ola → 10-107-37-188.ola.pod.cluster.local

---

## 📡 8. CoreDNS

 - Before v1.12 → kube-dns. After v1.12 → CoreDNS.
 - CoreDNS runs as a Deployment with 2 Pods.
 - Config file: /etc/coredns/Corefile (mounted via ConfigMap). To check root domain/zone configured in CoreDNS :-
```bash
kubectl get pod -n kube-system | grep -i dns
kubectl get cm -n kube-system | grep -i dns
kubectl describe cm coredns-enfu2d -n kube-system
```
 - Every record falls under domain cluster.local.
 - CoreDNS service (kube-dns) IP is automatically added to /etc/resolv.conf of Pods.
 - Check DNS resolution:
```bash
host service-name
host service-name.default.svc.cluster.local
host 10-107-37-188
```

---

## 🔍 9. DNS Queries and nslookup

### From Pod:

```bash
kubectl exec podname -- nslookup myservice.namespacename
```

### Example:

```bash
kubectl exec -it hr -- nslookup mysql.payroll
```

### Output:

```bash
Name: mysql.payroll.svc.cluster.local
Address: 10.108.177.160
```
