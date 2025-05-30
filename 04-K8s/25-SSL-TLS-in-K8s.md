# SSL/TLS and CSR Flow in Kubernetes

## 🔐 1. Authentication vs Authorization in Kubernetes

### 🧾 Authentication
- **Definition:** Verifies *who you are*.
- **Examples:** 
  - Client certificates
  - Bearer tokens (e.g., ServiceAccount tokens)
  - OIDC tokens
  - Username/password

### ✅ Authorization
- **Definition:** Determines *what you can do*.
- **Mechanisms:**
  - RBAC (Role-Based Access Control)
  - ABAC (Attribute-Based Access Control)
  - Webhook authorization

---

## 🔑 2. Symmetric vs Asymmetric Cryptography

### Symmetric Key
- Same key for encryption and decryption.
- Fast but insecure at scale.

### Asymmetric Key
- Uses a key pair:
  - **Private key** (secret)
  - **Public key** (shared)
- Used in TLS/SSL and digital signatures.

---

## 📄 3. Certificates in Kubernetes

- Used for securing:
  - API server
  - kubelets
  - kube-proxy
  - Ingress controllers (HTTPS)
- X.509 certificates signed by a CA.

---


## 📘 4. TLS/SSL Certificate Usage in Kubernetes

This document provides a comprehensive overview of where and why TLS/SSL certificates are used in Kubernetes communication.



### 🔐 Authentication and Encryption with TLS in Kubernetes

Kubernetes uses **TLS certificates** for secure encrypted communication and mutual authentication between components.


### 📌 Certificate Usage by Component

| Communication                        | Server Cert | Client Cert | Notes                                  |
|-------------------------------------|-------------|-------------|----------------------------------------|
| `kubectl` → API Server              | ✅          | ✅ (optional) | Often uses client cert or token        |
| API Server → etcd                   | ✅          | ✅          | Mutual TLS required                    |
| API Server → Kubelet                | ✅          | ❌          | TLS for encryption, server cert only   |
| Kubelet → API Server                | ❌          | ✅          | Client cert used                       |
| Controller Manager → API Server    | ❌          | ✅          | Authenticated via client cert          |
| Scheduler → API Server             | ❌          | ✅          | Authenticated via client cert          |
| etcd ↔ etcd (peer communication)   | ✅          | ✅          | Mutual TLS for clustering              |
| Ingress Controller → External User | ✅          | ❌          | HTTPS (public TLS)                     |
| API Server → Webhook               | ✅          | ❌          | Webhook must present trusted TLS cert  |


### 🧠 Explanation of Components

### 1. **API Server**
- Central hub of the control plane.
- Uses server certificates for HTTPS.
- Requires client certificates from internal components (kubelet, scheduler, etc.)

### 2. **Kubelet**
- Requires client certificates to authenticate to API server.
- Has a server cert for API server to connect securely.

### 3. **etcd**
- Secured by mutual TLS.
- Each etcd peer and client must present valid certificates.

### 4. **Controller Manager & Scheduler**
- Authenticate using client certs to the API server.

### 5. **Ingress Controller**
- Serves external traffic via HTTPS using public TLS certificates.

### 6. **Webhooks**
- Must use a trusted CA-signed server certificate for the API server to connect securely.

---


## 5. Keys, Certificates and Applying certificate

### 🛠️ 1. Create a Private Key and Certificate Signing Request (CSR) 

#### 🔧 Generate a Private Key

openssl genrsa -out my-user.key 2048

### 📝 Generate a CSR This will generate a request with a subject (/CN=my-user/O=dev-team).

    openssl req -new -key my-user.key -out my-user.csr -subj "/CN=my-user/O=dev-team"
    CN=my-user is the Common Name, representing the user identity. O=dev-team is the Organization, used for RBAC group bindings.

### 📦 2. Create a Kubernetes CertificateSigningRequest (CSR) Object

#### 🔄 Encode the CSR in Base64

    cat my-user.csr | base64 | tr -d '\n'

#### 📄 Create a CSR Manifest Save the following YAML as my-user-csr.yaml:

    apiVersion: certificates.k8s.io/v1
    kind: CertificateSigningRequest
    metadata:
      name: my-user-csr
    spec:
      request: <BASE64_CSR_HERE>
      signerName: kubernetes.io/kube-apiserver-client
      usages:
        - client auth

Replace <BASE64_CSR_HERE> with the base64-encoded string from the previous step.

### 🚀 3. Submit the CSR to Kubernetes

    kubectl apply -f my-user-csr.yaml

### ✅ 4. Approve the CSR

    kubectl certificate approve my-user-csr

### 📥 5. Retrieve the Signed Certificate

    kubectl get csr my-user-csr -o jsonpath='{.status.certificate}' | base64 -d > my-user.crt Now you have: my-user.key: Private key my-user.crt: Signed certificate

### 📁 6. Create a Custom kubeconfig Using Your Certificate

#### 🧱 Collect Required Info You need:

Kubernetes cluster CA certificate (can get from /etc/kubernetes/pki/ca.crt or from an existing kubeconfig)

Cluster API endpoint URL

#### 🔐 Add CA Cert (optional step to extract it)

    kubectl config view --raw -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' | base64 -d > ca.crt

#### 🧾 Build a kubeconfig

    kubectl config set-credentials my-user \
      --client-certificate=my-user.crt \
      --client-key=my-user.key


    kubectl config set-cluster my-cluster \
      --server=https://<API_SERVER_ENDPOINT> \
      --certificate-authority=ca.crt \
      --embed-certs=true


    kubectl config set-context my-user-context \
      --cluster=my-cluster \
      --user=my-user

    kubectl config use-context my-user-context

Replace: <API_SERVER_ENDPOINT> with your cluster’s endpoint (e.g., https://192.168.1.100:6443)

### 🔄 7. Test Your Access

Try running: kubectl get pods

Note : If access is denied, make sure your user (CN=my-user) has correct RBAC permissions.

Example RBAC RoleBinding:

    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: my-user-binding
    roleRef:
      kind: ClusterRole
      name: view
      apiGroup: rbac.authorization.k8s.io
    subjects:
    - kind: User
      name: my-user
      apiGroup: rbac.authorization.k8s.io

