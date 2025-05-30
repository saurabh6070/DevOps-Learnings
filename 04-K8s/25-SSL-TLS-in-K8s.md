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

## 🔐 4. TLS/SSL in Kubernetes

Common use cases:
- Secure API server communication
- Mutual TLS between nodes and control plane
- Secure ingress traffic with HTTPS

Kubernetes provides the `CertificateSigningRequest` (CSR) API for TLS certs.

---

## 📜 5. Approving a CSR in Kubernetes

### View Pending CSRs
#### kubectl get csr

### Approve Certificate
#### kubectl certificate approve <csr-name>

### Deny Certificate
#### kubectl certificate deny <csr-name>


---


## 📘 6. TLS/SSL Certificate Usage in Kubernetes

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
