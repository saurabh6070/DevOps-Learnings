# 🗂️ Kubernetes — ConfigMaps, Secrets, Secret Manager & Vault

---

## 📑 Table of Contents

1. [ConfigMaps](#1-configmaps)
   - 1.1 [What is a ConfigMap?](#11-what-is-a-configmap)
   - 1.2 [Creating a ConfigMap](#12-creating-a-configmap)
   - 1.3 [Use Case 1 — ConfigMap Mounted as a Volume File](#13-use-case-1--configmap-mounted-as-a-volume-file)
   - 1.4 [Use Case 2 — ConfigMap as Environment Variable](#14-use-case-2--configmap-as-environment-variable)
   - 1.5 [Use Case 3 — All Keys as Environment Variables](#15-use-case-3--all-keys-as-environment-variables)
   - 1.6 [Use Case 4 — ConfigMap in a Deployment](#16-use-case-4--configmap-in-a-deployment)
2. [Secrets](#2-secrets)
   - 2.1 [What is a Secret?](#21-what-is-a-secret)
   - 2.2 [Creating a Secret](#22-creating-a-secret)
   - 2.3 [Use Case 1 — Secret Mounted as a Volume](#23-use-case-1--secret-mounted-as-a-volume)
   - 2.4 [Use Case 2 — Secret as Environment Variable](#24-use-case-2--secret-as-environment-variable)
   - 2.5 [Use Case 3 — Secret in a Deployment (DB Credentials)](#25-use-case-3--secret-in-a-deployment-db-credentials)
   - 2.6 [Use Case 4 — ImagePullSecret (Private Registry)](#26-use-case-4--imagepullsecret-private-registry)
3. [ConfigMap vs Secret — Comparison](#3-configmap-vs-secret--comparison)
4. [Limitations of Native Kubernetes Secrets](#4-limitations-of-native-kubernetes-secrets)
5. [AWS Secrets Manager — External Secret Storage](#5-aws-secrets-manager--external-secret-storage)
   - 5.1 [What is AWS Secrets Manager?](#51-what-is-aws-secrets-manager)
   - 5.2 [ESO — External Secrets Operator](#52-eso--external-secrets-operator)
   - 5.3 [Installing ESO](#53-installing-eso)
   - 5.4 [SecretStore — Connect ESO to AWS Secrets Manager](#54-secretstore--connect-eso-to-aws-secrets-manager)
   - 5.5 [ExternalSecret — Pull from AWS Secrets Manager](#55-externalsecret--pull-from-aws-secrets-manager)
6. [HashiCorp Vault — Dynamic Secret Management](#6-hashicorp-vault--dynamic-secret-management)
   - 6.1 [What is Vault?](#61-what-is-vault)
   - 6.2 [Vault vs Kubernetes Secrets vs AWS Secrets Manager](#62-vault-vs-kubernetes-secrets-vs-aws-secrets-manager)
   - 6.3 [Installing Vault on Kubernetes](#63-installing-vault-on-kubernetes)
   - 6.4 [Vault Configuration — Step by Step](#64-vault-configuration--step-by-step)
   - 6.5 [ESO — SecretStore for Vault](#65-eso--secretstore-for-vault)
   - 6.6 [ExternalSecret — Pull from Vault](#66-externalsecret--pull-from-vault)
   - 6.7 [Use the ESO-created Secret in a Pod](#67-use-the-eso-created-secret-in-a-pod)
7. [Secret Management — Defence in Depth](#7-secret-management--defence-in-depth)
8. [Summary](#8-summary)

---

## 🗂️ 1. ConfigMaps

### 🔹 1.1 What is a ConfigMap?

A **ConfigMap** is a Kubernetes object used to store **non-sensitive configuration data** as key-value pairs. It decouples configuration from the container image — so the same image can be used across environments (dev, staging, prod) with different configs.

**ConfigMaps are used for:**
- Application configuration files (`.conf`, `.yaml`, `.properties`)
- Environment-specific settings (database hosts, feature flags, log levels)
- Command-line arguments passed to containers
- Any configuration data that does **not** contain passwords or credentials

> ⚠️ **Never store passwords, tokens, or certificates in a ConfigMap.** ConfigMaps are stored in etcd without any encoding or encryption. Use **Secrets** for sensitive data.

---

### 🔹 1.2 Creating a ConfigMap

**Method 1 — From a literal value:**

```bash
kubectl create configmap mymap --from-literal=sample.conf="This is my configuration file."

# Verify
kubectl get configmap mymap
kubectl describe configmap mymap
```

**Method 2 — From a file:**

```bash
# Create the config file
echo "This is my configuration file." > sample.conf

# Create ConfigMap from the file
kubectl create configmap mymap --from-file=sample.conf

# Verify
kubectl get configmap mymap -o yaml
```

**Method 3 — Declarative YAML manifest:**

```yaml
# configmap-mymap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mymap
  namespace: default
data:
  # ── Single-line values ─────────────────────────────────────
  APP_ENV: "production"
  LOG_LEVEL: "info"
  DB_HOST: "postgres.default.svc.cluster.local"

  # ── Multi-line config file ─────────────────────────────────
  sample.conf: |
    This is my configuration file.
    db_host=localhost
    db_port=5432
    log_level=info
```

```bash
kubectl apply -f configmap-mymap.yaml
kubectl get configmap mymap -o yaml
```

---

### 🔹 1.3 Use Case 1 — ConfigMap Mounted as a Volume File

Mount a ConfigMap key as an actual **file** inside the container at a specified path. The container reads it just like a regular file on disk.

**`sample.conf`:**
```
This is my configuration file.
```

**`configmap-mymap.yaml`:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mymap
data:
  sample.conf: |
    This is my configuration file.
```

**`pod-configmap-volume.yaml`:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myvolconfig2
spec:
  containers:
  - name: c1
    image: ubuntu
    command: ["/bin/bash", "-c", "while true; do echo Hello; sleep 5; done"]
    volumeMounts:
    - name: testconfigmap
      mountPath: "/tmp/config"        # ConfigMap files appear here
  volumes:
  - name: testconfigmap
    configMap:
      name: mymap                     # Name of the ConfigMap
      items:
      - key: sample.conf              # Key in the ConfigMap
        path: sample.conf             # Filename inside the mountPath
```

```bash
kubectl apply -f configmap-mymap.yaml
kubectl apply -f pod-configmap-volume.yaml

# Verify the file is mounted correctly inside the container
kubectl exec -it myvolconfig2 -- cat /tmp/config/sample.conf
# Output: This is my configuration file.
```

> 💡 **How it works:** Kubernetes creates a file at `/tmp/config/sample.conf` inside the container. The file contents are the value of the `sample.conf` key from the ConfigMap. If the ConfigMap is updated, the file inside the running Pod is also updated automatically (within ~60 seconds).

---

### 🔹 1.4 Use Case 2 — ConfigMap as Environment Variable

Inject a specific ConfigMap key as an **environment variable** inside the container.

**`sample.conf`:**
```
This is my configuration file.
```

**`pod-configmap-env.yaml`:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myvolconfig
spec:
  containers:
  - name: c1
    image: ubuntu
    command: ["/bin/bash", "-c", "while true; do echo Hello; sleep 5; done"]
    env:
    - name: MYENV                     # Environment variable name in container
      valueFrom:
        configMapKeyRef:
          name: mymap                 # ConfigMap name
          key: sample.conf            # Key to inject
```

```bash
kubectl apply -f pod-configmap-env.yaml

# Verify the environment variable is set inside the container
kubectl exec -it myvolconfig -- env | grep MYENV
# Output: MYENV=This is my configuration file.
```

> ⚠️ **Key difference from volume mount:** When ConfigMap data is injected as an **environment variable**, changes to the ConfigMap are **NOT automatically reflected** in running Pods. The Pod must be restarted to pick up new values. Volume-mounted ConfigMaps update automatically.

---

### 🔹 1.5 Use Case 3 — All Keys as Environment Variables

Inject **all keys** from a ConfigMap as environment variables at once using `envFrom`:

**`pod-configmap-envfrom.yaml`:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myvolconfig-envfrom
spec:
  containers:
  - name: c1
    image: ubuntu
    command: ["/bin/bash", "-c", "while true; do echo Hello; sleep 5; done"]
    envFrom:
    - configMapRef:
        name: mymap                   # ALL keys from this ConfigMap become env vars
```

```bash
kubectl apply -f pod-configmap-envfrom.yaml

# All ConfigMap keys are now environment variables
kubectl exec -it myvolconfig-envfrom -- env | grep -E "APP_ENV|LOG_LEVEL|DB_HOST"
```

---

### 🔹 1.6 Use Case 4 — ConfigMap in a Deployment

Real-world usage — inject ConfigMap into a Deployment for a web application:

**`configmap-app-config.yaml`:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: default
data:
  APP_ENV: "production"
  LOG_LEVEL: "warn"
  MAX_CONNECTIONS: "100"
  app.properties: |
    server.port=8080
    spring.datasource.url=jdbc:postgresql://db:5432/myapp
    logging.level.root=WARN
```

**`deployment-with-configmap.yaml`:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: webapp
        image: webapp:1.2.3
        ports:
        - containerPort: 8080

        # ── Inject specific keys as env vars ──────────────────
        env:
        - name: APP_ENV
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: APP_ENV
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: LOG_LEVEL

        # ── Mount config file into container ──────────────────
        volumeMounts:
        - name: app-properties
          mountPath: /app/config
          readOnly: true

      volumes:
      - name: app-properties
        configMap:
          name: app-config
          items:
          - key: app.properties
            path: app.properties
```

```bash
kubectl apply -f configmap-app-config.yaml
kubectl apply -f deployment-with-configmap.yaml

# Verify
kubectl exec -it <webapp-pod> -- cat /app/config/app.properties
kubectl exec -it <webapp-pod> -- env | grep APP_ENV
```

---

## 🔐 2. Secrets

### 🔹 2.1 What is a Secret?

A **Secret** is a Kubernetes object used to store **sensitive data** such as passwords, OAuth tokens, SSH keys, TLS certificates, and API keys. Secrets are similar to ConfigMaps but are intended for confidential information.

> ⚠️ **Important security note:** Kubernetes Secrets are **Base64-encoded, NOT encrypted by default**. Anyone with access to the namespace can decode them trivially. For production security, always use [Encryption at Rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) + [External Secrets (Section 5 & 6)](#5-aws-secrets-manager--external-secret-storage).

```bash
# Base64 encoding is trivially reversible
echo -n "mypassword123" | base64
# Output: bXlwYXNzd29yZDEyMw==

echo -n "bXlwYXNzd29yZDEyMw==" | base64 -d
# Output: mypassword123   ← fully readable ❌
```

---

### 🔹 2.2 Creating a Secret

**Method 1 — From files:**

```bash
# Create the credential files
echo -n "root" > username.txt
echo -n "mypassword123" > password.txt

# Create Secret from files
kubectl create secret generic mysecret \
  --from-file=username.txt \
  --from-file=password.txt

# Verify (values are base64 encoded in output)
kubectl get secret mysecret -o yaml
```

**Method 2 — From literal values:**

```bash
kubectl create secret generic mysecret \
  --from-literal=username=root \
  --from-literal=password=mypassword123
```

**Method 3 — Declarative YAML (values must be Base64-encoded):**

```bash
# Encode your values first
echo -n "root" | base64           # cm9vdA==
echo -n "mypassword123" | base64  # bXlwYXNzd29yZDEyMw==
```

```yaml
# secret-mysecret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
  namespace: default
type: Opaque                        # Generic secret type
data:
  username.txt: cm9vdA==            # base64("root")
  password.txt: bXlwYXNzd29yZDEyMw== # base64("mypassword123")
```

```bash
kubectl apply -f secret-mysecret.yaml

# Decode and verify
kubectl get secret mysecret -o jsonpath='{.data.username\.txt}' | base64 -d
# Output: root
```

---

### 🔹 2.3 Use Case 1 — Secret Mounted as a Volume

Mount a Secret as **files** inside the container. Each key becomes a separate file in the mounted directory.

**`username.txt`:**
```
root
```

**`password.txt`:**
```
mypassword123
```

**`pod-secret-volume.yaml`:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myvolsecret
spec:
  containers:
  - name: c1
    image: centos
    command: ["/bin/bash", "-c", "while true; do echo Hello; sleep 5; done"]
    volumeMounts:
    - name: testsecret
      mountPath: "/tmp/mysecret"     # Secret files appear here
      readOnly: true                 # Best practice — mount secrets read-only
  volumes:
  - name: testsecret
    secret:
      secretName: mysecret           # Name of the Secret object
```

```bash
kubectl apply -f secret-mysecret.yaml
kubectl apply -f pod-secret-volume.yaml

# Verify files are mounted inside the container
kubectl exec -it myvolsecret -- ls /tmp/mysecret/
# Output: password.txt  username.txt

kubectl exec -it myvolsecret -- cat /tmp/mysecret/username.txt
# Output: root

kubectl exec -it myvolsecret -- cat /tmp/mysecret/password.txt
# Output: mypassword123
```

> 💡 **How it works:** Kubernetes decodes the Base64 values and writes them as plain-text files inside the container. Each Secret key becomes a file — `username.txt` and `password.txt` appear as actual files at `/tmp/mysecret/`.

---

### 🔹 2.4 Use Case 2 — Secret as Environment Variable

Inject a specific Secret key as an **environment variable** inside the container:

**`pod-secret-env.yaml`:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mysecret-env-pod
spec:
  containers:
  - name: c1
    image: centos
    command: ["/bin/bash", "-c", "while true; do echo Hello; sleep 5; done"]
    env:
    - name: DB_USERNAME               # Env var name in the container
      valueFrom:
        secretKeyRef:
          name: mysecret              # Secret name
          key: username.txt           # Key to inject
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: mysecret
          key: password.txt
```

```bash
kubectl apply -f pod-secret-env.yaml

# Verify — the value is decoded automatically by Kubernetes
kubectl exec -it mysecret-env-pod -- env | grep DB_
# Output:
# DB_USERNAME=root
# DB_PASSWORD=mypassword123
```

---

### 🔹 2.5 Use Case 3 — Secret in a Deployment (DB Credentials)

Real-world usage — inject database credentials into a Deployment:

**`secret-db-creds.yaml`:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  namespace: default
type: Opaque
stringData:                           # stringData = no manual base64 needed
  DB_HOST: "postgres.default.svc.cluster.local"
  DB_PORT: "5432"
  DB_NAME: "payments"
  DB_USER: "payments_user"
  DB_PASSWORD: "SuperSecret123!"
```

**`deployment-with-secret.yaml`:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payments-app
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: payments
  template:
    metadata:
      labels:
        app: payments
    spec:
      containers:
      - name: payments
        image: payments-app:1.2.3
        ports:
        - containerPort: 8080

        # ── Inject all Secret keys as env vars ────────────────
        envFrom:
        - secretRef:
            name: db-credentials

        # ── Or inject specific keys ───────────────────────────
        # env:
        # - name: DB_PASSWORD
        #   valueFrom:
        #     secretKeyRef:
        #       name: db-credentials
        #       key: DB_PASSWORD

        resources:
          limits:
            cpu: "500m"
            memory: "256Mi"
          requests:
            cpu: "100m"
            memory: "128Mi"
```

```bash
kubectl apply -f secret-db-creds.yaml
kubectl apply -f deployment-with-secret.yaml

# Verify env vars in running pod
kubectl exec -it <payments-pod> -- env | grep DB_
```

---

### 🔹 2.6 Use Case 4 — ImagePullSecret (Private Registry)

Use a Secret to authenticate with a **private container registry** (e.g., Docker Hub private, AWS ECR, GCR):

```bash
# Create Docker registry secret
kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=myuser \
  --docker-password=mypassword \
  --docker-email=myemail@example.com
```

**`pod-with-imagepullsecret.yaml`:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: private-image-pod
spec:
  imagePullSecrets:
  - name: regcred                     # Reference the registry secret
  containers:
  - name: app
    image: myprivaterepo/myapp:1.0.0  # Private image
    ports:
    - containerPort: 8080
```

```bash
kubectl apply -f pod-with-imagepullsecret.yaml
kubectl describe pod private-image-pod | grep -A5 "Events"
```

---

## 📊 3. ConfigMap vs Secret — Comparison

| 🔍 Aspect | 🗂️ ConfigMap | 🔐 Secret |
|---|---|---|
| **Purpose** | Non-sensitive configuration | Sensitive data (passwords, tokens, keys) |
| **Storage** | Plain text in etcd | Base64-encoded in etcd |
| **Encryption** | ❌ Not encrypted | ❌ Not encrypted by default (encode only) |
| **Volume mount** | ✅ Supported | ✅ Supported |
| **Env variable** | ✅ Supported | ✅ Supported |
| **Auto-update** | ✅ Volume mounts auto-update | ✅ Volume mounts auto-update |
| **Size limit** | 1 MB | 1 MB |
| **Use for** | App config, feature flags, connection strings | DB passwords, API keys, TLS certs, tokens |
| **Safe to Git** | ✅ Generally safe | ❌ Never commit — use ESO instead |

---

## ⚠️ 4. Limitations of Native Kubernetes Secrets

Understanding the limitations of native Secrets is essential before choosing a secret management strategy:

| ⚠️ Limitation | 💥 Impact |
|---|---|
| **Base64 encoded, not encrypted** | Anyone with `kubectl get secret` can decode the value in seconds |
| **Stored in etcd without encryption (default)** | etcd backup = all secrets exposed in plaintext |
| **Namespace-level access** | Anyone with namespace access can read all secrets in that namespace |
| **RBAC alone is insufficient** | Even with `get secret` blocked, sidechannel access via env vars and volume mounts exists |
| **No automatic rotation** | Leaked credentials remain valid until manually changed |
| **No audit trail** | Cannot tell who read a secret or when |
| **Cannot be safely committed to Git** | GitOps workflows cannot include Secret manifests safely |
| **No versioning** | No history of what the secret value was before |

> 💡 **The GitOps Problem:** You want to store all Kubernetes manifests in Git for GitOps (ArgoCD, Flux). But you **cannot commit a Secret manifest to Git** — the Base64-encoded value is trivially decoded and your credentials become public. This is the exact gap that **External Secrets Operator (ESO)** solves.

---

## ☁️ 5. AWS Secrets Manager — External Secret Storage

### 🔹 5.1 What is AWS Secrets Manager?

**AWS Secrets Manager** is a fully managed service for storing, rotating, and retrieving secrets such as database credentials, API keys, and TLS certificates. It provides:

- ✅ **Encryption at rest** using AWS KMS
- ✅ **Automatic rotation** of credentials (RDS passwords, IAM keys)
- ✅ **Fine-grained IAM access control**
- ✅ **Full audit trail** via AWS CloudTrail
- ✅ **Versioning** — access previous secret values

---

### 🔹 5.2 ESO — External Secrets Operator

**External Secrets Operator (ESO)** is a Kubernetes operator that bridges the gap between Kubernetes and external secret management systems. It:

1. Watches `ExternalSecret` custom resource objects in Kubernetes
2. Fetches the actual secret values from the external system (AWS Secrets Manager, Vault, GCP Secret Manager, Azure Key Vault)
3. Creates and maintains native Kubernetes `Secret` objects automatically

```
┌──────────────────────────────────────────────────────────────────────┐
│                  ESO Architecture                                    │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Git Repo (safe to commit ✅)                                        │
│  └── ExternalSecret manifest                                         │
│      (only references the secret path — no actual values)            │
│               ↓                                                      │
│       ESO Controller (running in cluster)                            │
│               ↓  authenticates via IAM / OIDC                        │
│       AWS Secrets Manager / Vault / GCP Secret Manager               │
│               ↓  fetches actual secret value                         │
│       Native K8s Secret (auto-created and kept in sync)              │
│               ↓                                                      │
│       Pod reads it as env var or volume mount                        │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

### 🔹 5.3 Installing ESO

```bash
# Add the ESO Helm repo
helm repo add external-secrets https://charts.external-secrets.io
helm repo update

# Install ESO into the cluster
helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets \
  --create-namespace \
  --set installCRDs=true

# Verify installation
kubectl get pods -n external-secrets
kubectl get crds | grep external-secrets.io
```

---

### 🔹 5.4 SecretStore — Connect ESO to AWS Secrets Manager

A **SecretStore** defines the connection details and authentication for ESO to reach the external secret backend.

**Option A — Using IAM Role (IRSA on EKS — recommended):**

```yaml
# secretstore-aws.yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
  namespace: default
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: eso-sa              # SA with IRSA annotation
```

**ServiceAccount with IRSA annotation:**
```yaml
# serviceaccount-eso.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: eso-sa
  namespace: default
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/ESO-SecretsManager-Role
```

**Option B — Using AWS access keys (for testing only):**

```yaml
# secret-aws-creds.yaml
apiVersion: v1
kind: Secret
metadata:
  name: aws-credentials
  namespace: default
type: Opaque
stringData:
  access-key: "AKIAIOSFODNN7EXAMPLE"
  secret-access-key: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
---
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
  namespace: default
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        secretRef:
          accessKeyIDSecretRef:
            name: aws-credentials
            key: access-key
          secretAccessKeySecretRef:
            name: aws-credentials
            key: secret-access-key
```

```bash
kubectl apply -f serviceaccount-eso.yaml
kubectl apply -f secretstore-aws.yaml

# Verify SecretStore is Ready
kubectl get secretstore -n default
# STATUS should show: Valid
```

---

### 🔹 5.5 ExternalSecret — Pull from AWS Secrets Manager

First, create your secret in AWS Secrets Manager:

```bash
# Create the secret in AWS (run once)
aws secretsmanager create-secret \
  --name "payment-app/db-credentials" \
  --region us-east-1 \
  --secret-string '{"username":"payments_user","password":"SuperSecret123!"}'
```

Then create the ExternalSecret manifest (safe to commit to Git ✅):

```yaml
# externalsecret-aws.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials-aws
  namespace: default
spec:
  refreshInterval: "1h"               # Auto-sync every hour

  secretStoreRef:
    name: aws-secrets-manager         # Reference the SecretStore
    kind: SecretStore

  target:
    name: db-credentials-k8s          # Name of the K8s Secret to create
    creationPolicy: Owner              # ESO owns and manages this Secret

  data:
  # ── Pull specific fields from the AWS secret ──────────────
  - secretKey: DB_USERNAME             # Key in the K8s Secret
    remoteRef:
      key: payment-app/db-credentials  # AWS Secret name
      property: username               # JSON field in the AWS Secret

  - secretKey: DB_PASSWORD
    remoteRef:
      key: payment-app/db-credentials
      property: password
```

```bash
kubectl apply -f externalsecret-aws.yaml

# ESO pulls from AWS and auto-creates the K8s Secret
kubectl get externalsecret -n default
kubectl get secret db-credentials-k8s -n default

# Check the synced secret
kubectl get secret db-credentials-k8s -o jsonpath='{.data.DB_PASSWORD}' | base64 -d
```

---

## 🔑 6. HashiCorp Vault — Dynamic Secret Management

### 🔹 6.1 What is Vault?

**HashiCorp Vault** is an open-source, enterprise-grade secret management system that goes beyond simple secret storage. Its key differentiator is **dynamic secrets** — generating short-lived, automatically expiring credentials on demand.

**Vault capabilities:**
- ✅ **Static secrets** — store and retrieve secrets (like AWS Secrets Manager)
- ✅ **Dynamic secrets** — generate short-lived AWS IAM users, DB credentials, TLS certs on demand
- ✅ **Encryption as a Service** — encrypt/decrypt data without storing it
- ✅ **PKI** — act as a Certificate Authority
- ✅ **Fine-grained policies** — path and capability-based access control
- ✅ **Audit logging** — every secret access logged with full metadata

---

### 🔹 6.2 Vault vs Kubernetes Secrets vs AWS Secrets Manager

| 🔍 Aspect | 🔐 K8s Secrets | ☁️ AWS Secrets Manager | 🔑 HashiCorp Vault |
|---|---|---|---|
| **Encryption at rest** | ❌ No (by default) | ✅ Yes (KMS) | ✅ Yes |
| **Dynamic secrets** | ❌ No | ❌ No | ✅ Yes |
| **Auto rotation** | ❌ No | ✅ Yes (for supported services) | ✅ Yes |
| **Audit trail** | ❌ Limited | ✅ CloudTrail | ✅ Full audit log |
| **Multi-cloud** | ✅ Cluster-wide | ❌ AWS only | ✅ Any cloud / on-prem |
| **Fine-grained policies** | ✅ RBAC | ✅ IAM | ✅ Path-based policies |
| **Short-lived credentials** | ❌ No | ❌ No | ✅ Yes (core feature) |
| **Cost** | Free | Paid per secret | Open source (free) / Enterprise |
| **GitOps safe** | ❌ No | ✅ With ESO | ✅ With ESO |

---

### 🔹 6.3 Installing Vault on Kubernetes

**Option A — Vault on Kubernetes via Helm:**

```bash
# Add HashiCorp Helm repo
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update

# Install Vault in dev mode (testing only)
helm install vault hashicorp/vault \
  --namespace vault \
  --create-namespace \
  --set "server.dev.enabled=true"

# Verify
kubectl get pods -n vault
kubectl get svc -n vault
```

**Option B — Vault on EC2 (as a system service):**

```bash
# Install Vault binary on Ubuntu EC2
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vault

# Start in dev mode (testing only)
vault server -dev -dev-root-token-id="root"
```

> ⚠️ **Dev mode** starts Vault with all data in-memory — data is lost on restart. For production, use [Integrated Storage (Raft)](https://developer.hashicorp.com/vault/docs/configuration/storage/raft) with proper HA configuration.

---

### 🔹 6.4 Vault Configuration — Step by Step

```bash
# Step 1: Set Vault address and login
export VAULT_ADDR='http://127.0.0.1:8200'
vault login root
# Output: Token, accessor, policies, lease duration

# Step 2: Enable the KV v2 secrets engine
vault secrets enable -path=secret kv-v2
# This creates the path: secret/ in Vault

# Step 3: Store your secrets in Vault
vault kv put secret/payment-app/db-credentials \
  username="payments_user" \
  password="SuperSecret123!"

# Step 4: Verify the secret is stored
vault kv get secret/payment-app/db-credentials

# Step 5: Enable Kubernetes auth method
vault auth enable kubernetes

# Step 6: Configure Kubernetes auth (run from inside the cluster or with kubeconfig)
vault write auth/kubernetes/config \
  kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443"

# Step 7: Create a Vault policy for ESO
vault policy write eso-payment-policy - <<EOF
path "secret/data/payment-app/*" {
  capabilities = ["read"]
}
EOF

# Step 8: Create a Kubernetes auth role for ESO ServiceAccount
vault write auth/kubernetes/role/eso-payment-role \
  bound_service_account_names=eso-sa \
  bound_service_account_namespaces=default \
  policies=eso-payment-policy \
  ttl=1h
```

---

### 🔹 6.5 ESO — SecretStore for Vault

```yaml
# secretstore-vault.yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: default
spec:
  provider:
    vault:
      server: "http://vault.vault.svc.cluster.local:8200"   # Vault service URL
      path: "secret"                                         # KV mount path
      version: "v2"                                          # KV version
      auth:
        kubernetes:
          mountPath: "kubernetes"                            # Vault auth mount
          role: "eso-payment-role"                           # Vault role name
          serviceAccountRef:
            name: eso-sa                                     # K8s ServiceAccount
```

```bash
kubectl apply -f secretstore-vault.yaml

# Verify SecretStore is connected
kubectl get secretstore vault-backend
# STATUS: Valid ✅
```

---

### 🔹 6.6 ExternalSecret — Pull from Vault

```yaml
# externalsecret-vault.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials-vault
  namespace: default
spec:
  refreshInterval: "1h"               # Auto-sync with Vault every hour

  secretStoreRef:
    name: vault-backend               # Reference to the Vault SecretStore
    kind: SecretStore

  target:
    name: db-credentials-k8s          # Name of the K8s Secret ESO will create
    creationPolicy: Owner

  data:
  # ── Pull username from Vault ───────────────────────────────
  - secretKey: DB_USERNAME
    remoteRef:
      key: payment-app/db-credentials  # Vault KV path (without "secret/data/" prefix)
      property: username               # Field inside the Vault secret

  # ── Pull password from Vault ───────────────────────────────
  - secretKey: DB_PASSWORD
    remoteRef:
      key: payment-app/db-credentials
      property: password
```

```bash
kubectl apply -f externalsecret-vault.yaml

# Verify ESO pulled from Vault and created the K8s Secret
kubectl get externalsecret db-credentials-vault
kubectl get secret db-credentials-k8s

# Confirm the values (Vault → ESO → K8s Secret → decoded)
kubectl get secret db-credentials-k8s -o jsonpath='{.data.DB_PASSWORD}' | base64 -d
# Output: SuperSecret123!
```

---

### 🔹 6.7 Use the ESO-created Secret in a Pod

The K8s Secret created by ESO is a **standard Kubernetes Secret** — use it exactly like any other Secret:

**`pod-with-vault-secret.yaml`:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: payments-pod
  namespace: default
spec:
  containers:
  - name: payments
    image: payments-app:1.2.3
    ports:
    - containerPort: 8080

    # ── Option A: Inject all keys as env vars ─────────────────
    envFrom:
    - secretRef:
        name: db-credentials-k8s       # Auto-created by ESO from Vault

    # ── Option B: Inject specific keys ────────────────────────
    # env:
    # - name: DB_PASSWORD
    #   valueFrom:
    #     secretKeyRef:
    #       name: db-credentials-k8s
    #       key: DB_PASSWORD

    # ── Option C: Mount as files ──────────────────────────────
    volumeMounts:
    - name: db-creds-volume
      mountPath: /app/secrets
      readOnly: true

  volumes:
  - name: db-creds-volume
    secret:
      secretName: db-credentials-k8s  # Auto-created by ESO from Vault
```

```bash
kubectl apply -f pod-with-vault-secret.yaml

# Verify env vars are populated from Vault via ESO
kubectl exec -it payments-pod -- env | grep DB_
# Output:
# DB_USERNAME=payments_user
# DB_PASSWORD=SuperSecret123!

# Verify file mount
kubectl exec -it payments-pod -- cat /app/secrets/DB_PASSWORD
# Output: SuperSecret123!
```

> ✅ **GitOps safe:** The `externalsecret-vault.yaml` file contains **only the Vault path reference** — never the actual secret value. It is completely safe to commit to Git. ESO handles fetching and syncing from Vault automatically.

---

## 🔒 7. Secret Management — Defence in Depth

```
┌──────────────────────────────────────────────────────────────────────┐
│           SECRET MANAGEMENT — DEFENCE IN DEPTH                       │
├────────┬─────────────────────────────────────────────────────────────┤
│ Layer  │ Control                                                      │
├────────┼─────────────────────────────────────────────────────────────┤
│   1    │ 🙈  .gitignore / .dockerignore → Never commit secret files  │
│   2    │ 🪝  GitLeaks Pre-commit Hook   → Block hardcoded secrets    │
│   3    │ 🔐  Kubernetes Secrets         → Never hardcode in manifests│
│   4    │ 🔑  RBAC on Secrets            → Least-privilege access     │
│   5    │ 🔒  Encryption at Rest         → Encrypt etcd secrets       │
│   6    │ ☁️  AWS Secrets Manager        → Managed, encrypted, rotated│
│   7    │ 🏛️  HashiCorp Vault            → Dynamic, short-lived creds │
│   8    │ 🤝  ESO (ExternalSecret)       → GitOps-safe secret sync    │
│   9    │ 🔄  Auto Rotation              → Secrets rotated on schedule│
│  10    │ 📝  Audit Logging              → Full trail of secret access│
└────────┴─────────────────────────────────────────────────────────────┘
```

| 🔢 Layer | 🛠️ Control | 🎯 What It Prevents |
|---|---|---|
| 1 | `.gitignore` / `.dockerignore` | Secret files committed to Git or baked into images |
| 2 | GitLeaks pre-commit | Hardcoded secrets in code, manifests, Dockerfiles |
| 3 | Kubernetes Secrets (not ConfigMap) | Plaintext passwords in ConfigMaps |
| 4 | RBAC on Secrets | Over-broad access to Secret objects |
| 5 | Encryption at rest | etcd backups exposing all secrets in plaintext |
| 6 | AWS Secrets Manager | Unmanaged, unrotated credentials in cloud environments |
| 7 | HashiCorp Vault | Long-lived static credentials — replaced with dynamic |
| 8 | ESO + ExternalSecret | Secret values committed to Git for GitOps workflows |
| 9 | Auto rotation | Stale credentials persisting after a potential compromise |
| 10 | Audit logging | Undetected unauthorized secret access |

---

## ✅ 8. Summary

| 🏷️ Topic | 💡 Key Takeaway |
|---|---|
| 🗂️ **ConfigMap** | Stores non-sensitive config as key-value pairs — never use for passwords |
| 📁 **ConfigMap Volume** | Mounts ConfigMap keys as files — auto-updates in running Pods |
| 🌍 **ConfigMap Env Var** | Injects specific keys as env vars — requires Pod restart to update |
| 🔐 **Secret** | Stores sensitive data Base64-encoded — NOT encrypted by default |
| 📁 **Secret Volume** | Mounts Secret keys as files — decoded to plaintext by Kubernetes |
| 🌍 **Secret Env Var** | Injects Secret keys as env vars — decoded automatically |
| 🐳 **ImagePullSecret** | Authenticates with private container registries |
| ⚠️ **K8s Secret Limits** | Base64 only, no encryption, no rotation, not safe for Git |
| 🤝 **ESO** | Bridges K8s and external secret backends — enables safe GitOps |
| ☁️ **AWS Secrets Manager** | Managed, encrypted, auto-rotating secrets on AWS |
| 🔑 **HashiCorp Vault** | Dynamic short-lived credentials — most powerful secret management option |
| 🔄 **Auto-sync** | ESO refreshes K8s Secrets from Vault/AWS on a configurable interval |
| ✅ **GitOps Safe** | ExternalSecret manifests (Vault/AWS paths only) are safe to commit to Git |

---
