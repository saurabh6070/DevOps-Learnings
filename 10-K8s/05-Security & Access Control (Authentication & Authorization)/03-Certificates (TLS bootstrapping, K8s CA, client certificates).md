# 📜 Kubernetes Certificates — TLS Bootstrapping, K8s CA & Client Certificates


## 🎯 Usage — What Certificates Are For

> 🔒 A **certificate** ensures two things:
> 1. **Encryption** — the data being transferred is encrypted, so it can't be read by eavesdroppers
> 2. **Identity verification** — the server is proven to be who it claims to be

In Kubernetes, certificates are used everywhere: **API server ↔ kubelet**, **etcd peer communication**, **kubectl ↔ API server (client certs)**, and **TLS bootstrapping** for new nodes joining the cluster.

```bash
# Typical starting point — checking what certs your cluster already uses
ls /etc/kubernetes/pki/
```

---

## 🔑 Encryption Fundamentals

### 🔁 Symmetric Encryption

- Uses a **single key** to both encrypt and decrypt data
- Sender encrypts data with the key, then sends **both the encrypted data and the key** to the receiver
- ⚠️ **Weakness:** if a sniffer intercepts the key in transit, they can decrypt everything
- 🚫 Not secure on its own for key exchange over an open network

### 🔐 Asymmetric Encryption

Uses **two keys**:

| Key | 🔑 Role |
|---|---|
| 🔓 Public Key | Like a public lock — can be shared freely |
| 🔒 Private Key | Kept secret, never shared |

**Two possible flows:**
- ✅ Encrypt with **Public Key** → Decrypt with **Private Key** (preferred — used for confidential data sent *to* the key owner)
- ⚠️ Encrypt with **Private Key** → Decrypt with **Public Key** (used for **signing/verification**, not confidentiality — since the public key is shared, anyone can decrypt it)

> 💡 **Rule of thumb:** You can never encrypt and decrypt with the *same* key in asymmetric encryption — one key always does the opposite job of the other.

### ⚙️ Final Implementation — Hybrid Approach

- 🤝 **Asymmetric encryption** is used just to **securely exchange a symmetric key**
- 🔁 **All further communication** then uses **symmetric encryption** (faster, since only one key is needed)

This hybrid model is exactly how **TLS/HTTPS** works.

---

## 🐧 SSH Keys — Linux Analogy

A great way to understand public/private key pairs before diving into Kubernetes certs:

```bash
# Generate a public/private key pair
ssh-keygen
```

| File (in `~/.ssh/`) | 📝 Purpose |
|---|---|
| 🔒 `id_rsa` | Private key of this user — never share |
| 🔓 `id_rsa.pub` | Public key / public lock of this user |
| 📋 `authorized_keys` | Stores all public keys allowed to access **this** user |

### 🔐 Securing Access

- 🚪 Lock down access to a Linux machine, allowing entry **only via public-key authentication**
- 🎯 To grant another user access:
  - ❌ Share your private key (insecure, don't do this), **or**
  - ✅ Add **their public key** to your `authorized_keys` file

---

## 🏗️ Generating Keys & Certificates (OpenSSL)

### 1️⃣ Generate a Private Key

```bash
openssl genrsa -out my-bank.key 1024
```

> 📛 Naming convention: private keys are typically named `*.key` or `*-key.pem`

### 2️⃣ Generate a Public Key

```bash
openssl rsa -in my-bank.key -pubout > mybank.pem
```

> 📛 Naming convention: public keys/certs are typically named `*.crt` or `*.pem`

### 3️⃣ Generate a CSR (Certificate Signing Request)

```bash
openssl req -new -key my-bank.key -out my-bank.csr \
  -subj "/C=US/ST=CA/O=MyOrg, Inc./CN=mydomain.com"
```

| CSR Field | Meaning |
|---|---|
| `/C` | 🌍 Country |
| `/ST` | 🗺️ State |
| `/O` | 🏢 Organization |
| `/CN` | 🏷️ Common Name (domain or entity identity) |

---

## 🌍 How Browsers Trust Certificates

- 🗂️ Every browser ships with the **public keys of all Trusted Certificate Authorities (CAs)** pre-installed
- ✍️ A CA signs a certificate using **its own Private Key**
- ✅ The browser validates a website by checking if the **CA's Public Key** matches the signature on the certificate
- ❌ If it doesn't match (or isn't from a trusted CA) → browser shows a security warning

```text
                 ┌────────────────────┐
                 │   Trusted CA        │
                 │  (Public Key baked  │
                 │   into browsers)    │
                 └─────────┬───────────┘
                           │ signs
                           ▼
                 ┌────────────────────┐
                 │  Website Certificate│
                 └────────────────────┘
```

---

## ☸️ Kubernetes Certificate Authority (CA)

### 🧰 Common Tools for Certificate Creation

| Tool | 🧩 Notes |
|---|---|
| 🔧 OpenSSL | Most common, manual, fine-grained control |
| ⚡ CFSSL | Cloudflare's PKI/TLS toolkit — often used for automation |
| 🚀 EASYRSA | Simplified CLI wrapper around OpenSSL |

### 🏛️ Root Certificate

> 📌 The **Root Certificate** is configured on the **Certificate Authority servers** — this is the trust anchor for the entire cluster's PKI.

### 🔨 Step 1 — Create the CA's Private Key & Self-Signed Certificate

```bash
# 1. Create CA Private Key
openssl genrsa -out ca.key 1024

# 2. Create CSR for the CA
openssl req -new -key ca.key -out ca.csr -subj "/CN=KUBERNETES-CA"

# 3. Self-sign the certificate using the CA's own private key
openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt
```

> 🏗️ This `ca.crt` + `ca.key` pair becomes the **root of trust** for the entire Kubernetes cluster — every other component certificate gets signed by this CA.

---

## 👤 Generating Client Certificates (e.g., Admin User)

```bash
# 1. Generate the admin's private key
openssl genrsa -out admin.key 2048

# 2. Create a CSR for the admin user
openssl req -new -key admin.key -out admin.csr -subj "/CN=kube-admin"

# 3. Sign the CSR using the Kubernetes CA (ca.crt + ca.key)
openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -out admin.crt
```

> 🔁 **The same pattern applies to every Kubernetes component** — API server, kubelet, scheduler, controller-manager, etcd, etc. Each gets its own key + CSR + CA-signed certificate.

### 🧩 Typical Kubernetes Certificates Signed by the CA

| Component | 🏷️ Common Name (CN) Pattern |
|---|---|
| 👑 kube-admin (client) | `CN=kube-admin` |
| ⚙️ kube-scheduler | `CN=system:kube-scheduler` |
| 🎛️ kube-controller-manager | `CN=system:kube-controller-manager` |
| 🌐 API Server | `CN=kube-apiserver` |
| 🖥️ kubelet (per node) | `CN=system:node:<node-name>` |
| 🗄️ etcd | `CN=etcd-server` / `CN=etcd-peer` |

---

## 🔍 Inspecting & Debugging Certificates

### 📖 View a Certificate in Text Format

```bash
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout
```

This reveals:
- 🌐 All **DNS names / SANs** covered by the certificate
- 🏛️ The **Issuer** (which CA signed it)
- ⏳ **Validity period** (Not Before / Not After)

### 📋 View System Logs for a Service

```bash
journalctl -u etcd.service -l
```

### 🐳 When `kubectl` Commands Aren't Working

```bash
# Check container logs via docker
docker logs <container-id>

# Or via crictl (containerd/CRI-O runtimes)
crictl ps -a
crictl logs <container-id>
```

> 💡 TLS/certificate misconfigurations often manifest as `kubectl` hanging or throwing `x509: certificate signed by unknown authority` — checking API server and etcd logs is usually the fastest path to the root cause.

---

## ✅ Quick Reference Cheat Sheet

```bash
# Generate private key
openssl genrsa -out <name>.key 2048

# Generate CSR
openssl req -new -key <name>.key -out <name>.csr -subj "/CN=<common-name>"

# Self-sign (for CA/root cert only)
openssl x509 -req -in <name>.csr -signkey <name>.key -out <name>.crt

# Sign with an existing CA (for all other certs)
openssl x509 -req -in <name>.csr -CA ca.crt -CAkey ca.key -out <name>.crt

# Extract public key from a private key
openssl rsa -in <name>.key -pubout > <name>.pem

# Inspect a certificate
openssl x509 -in <path-to-cert>.crt -text -noout

# Check service logs
journalctl -u <service-name>.service -l
```

| Step | Command Flag | Purpose |
|---|---|---|
| 1️⃣ | `genrsa` | Generate private key |
| 2️⃣ | `req -new` | Create CSR |
| 3️⃣ | `x509 -req -signkey` | Self-sign (CA only) |
| 4️⃣ | `x509 -req -CA -CAkey` | Sign using existing CA |
| 5️⃣ | `x509 -text -noout` | Inspect a certificate |

---

## 🧹 Best Practices

- 🔒 **Never share private keys** — treat `*.key` files like passwords
- ⏳ **Track certificate expiry** — expired certs are a leading cause of cluster outages
  ```bash
  openssl x509 -enddate -noout -in /etc/kubernetes/pki/apiserver.crt
  ```
- 🔁 **Automate rotation** where possible (`kubeadm certs renew`, cert-manager, etc.)
- 🏛️ **Protect the CA private key (`ca.key`)** above all else — compromise of this key compromises the entire cluster's trust chain
- 📛 **Use meaningful CNs** (`system:node:<name>`, `system:kube-scheduler`) to align with Kubernetes RBAC subject matching
- 🧪 **Test with `openssl x509 -text -noout`** before rolling out any new certificate to production
- 📋 **Centralize logs** (`journalctl`, `crictl logs`) for faster TLS-issue diagnosis

---

📚 **References:** Kubernetes official documentation on PKI Certificates and Requirements, TLS Bootstrapping, and Certificate Management with `kubeadm`.
