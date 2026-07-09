# 🗂️ Kubernetes — ConfigMaps, Secrets, Secret Manager & Vault

---

## 🗂️ 1. ConfigMaps

### 🔹 1.1 What is a ConfigMap?

A **ConfigMap** is a native Kubernetes API object whose sole purpose is to hold **non-sensitive configuration data** as simple key-value pairs, completely separate from your container image. This separation is one of the core ideas behind "twelve-factor" style applications: the same Docker image can be promoted from dev → staging → prod unchanged, while the *behaviour* of the application is controlled purely by the ConfigMap it is deployed alongside.

Typical things people put in a ConfigMap:

- Application configuration files (`.conf`, `.yaml`, `.properties`, `.ini`)
- Environment-specific settings such as database hostnames, feature flags, and log verbosity
- Command-line arguments or flags passed into a container's entrypoint
- Any piece of configuration data that is **not** a password, token, certificate, or other secret

> ⚠️ **Never store passwords, tokens, or certificates in a ConfigMap.** ConfigMaps are written into etcd completely unencoded and unencrypted — there is no protection at all, unlike Secrets which are at least Base64-encoded. Sensitive values always belong in a **Secret** (see Section 2).

The key mental model to keep is: ConfigMap = "what should my app do", Secret = "what should my app authenticate with".

---

### 🔹 1.2 Creating a ConfigMap

There are three equally valid ways to create a ConfigMap, and each is useful in different situations — quick testing, file-based configs, or fully declarative GitOps-style manifests.

**Method 1 — From a literal value:**

Useful for quick, one-off testing directly from the command line, without needing to create any file first.

```bash
kubectl create configmap mymap --from-literal=sample.conf="This is my configuration file."

# Verify
kubectl get configmap mymap
kubectl describe configmap mymap
```

**Method 2 — From a file:**

Useful when the configuration already exists as a real file on disk (e.g. an `nginx.conf` or `application.properties`) and you simply want Kubernetes to store its contents.

```bash
# Create the config file
echo "This is my configuration file." > sample.conf

# Create ConfigMap from the file
kubectl create configmap mymap --from-file=sample.conf

# Verify
kubectl get configmap mymap -o yaml
```

**Method 3 — Declarative YAML manifest:**

The preferred approach for GitOps workflows, since the manifest can be version-controlled, code-reviewed, and applied repeatably. Note how the `data` block can mix short single-line values with a whole multi-line file under one key using the YAML block-scalar (`|`) syntax.

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

One of the two main ways to consume a ConfigMap inside a Pod is to mount it as a **volume**, which makes each key appear as an actual **file** on the container's filesystem. The application simply reads it like any normal file — no special awareness of Kubernetes is required.

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

> 💡 **How it works:** Kubernetes creates a file at `/tmp/config/sample.conf` inside the container, whose contents are exactly the value of the `sample.conf` key from the ConfigMap. If the ConfigMap is later updated (`kubectl apply` with a new value), the file inside the *already-running* Pod is updated automatically as well — typically within about 60 seconds, since the kubelet periodically re-syncs mounted ConfigMap volumes. This makes volume mounts the right choice whenever an application can hot-reload its configuration from disk.

---

### 🔹 1.4 Use Case 2 — ConfigMap as Environment Variable

The second common way to consume a ConfigMap is to inject a single key as an **environment variable**, which is often simpler for applications that already read their configuration from `os.environ` / `process.env` style APIs.

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

> ⚠️ **Key difference from volume mount:** When ConfigMap data is injected as an **environment variable**, changes to the ConfigMap are **NOT automatically reflected** in already-running Pods — environment variables are set only once, at container start-up. To pick up new values, the Pod must be deleted/recreated or the Deployment rolled. This is the opposite behaviour of the volume-mount approach in 1.3, which does update automatically. Choose the mechanism based on whether your application can tolerate — or needs — that live-reload behaviour.

---

### 🔹 1.5 Use Case 3 — All Keys as Environment Variables

Rather than wiring up individual `env` entries one at a time, `envFrom` lets you inject **every key** in a ConfigMap as an environment variable in a single, compact block. This is convenient when a ConfigMap already models a full set of related settings.

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

Because `envFrom` maps every key to an identically-named environment variable, it works best when your ConfigMap keys already follow environment-variable naming conventions (e.g. `APP_ENV`, `LOG_LEVEL`) rather than filenames like `sample.conf`.

---

### 🔹 1.6 Use Case 4 — ConfigMap in a Deployment

Pulling the previous use cases together, a realistic production Deployment typically combines **both** mechanisms at once: specific keys injected as environment variables for values the application reads at start-up, and a full configuration file mounted as a volume for anything the application reads from disk.

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

With two replicas, both Pods read from the exact same `app-config` ConfigMap, guaranteeing configuration consistency across every instance of the Deployment.

---

## 🔐 2. Secrets

### 🔹 2.1 What is a Secret?

A **Secret** is Kubernetes's dedicated object type for storing **sensitive data** — passwords, OAuth tokens, SSH private keys, TLS certificates, API keys, and similar credentials. Structurally a Secret looks almost identical to a ConfigMap (same key-value shape, same consumption mechanisms), but it carries an important behavioural difference and an important limitation.

> ⚠️ **Important security note:** Kubernetes Secrets are **Base64-encoded, NOT encrypted, by default**. Base64 is an *encoding*, not an *encryption* algorithm — it has no key and no secrecy property whatsoever. Anyone with read access to the Secret object (via `kubectl`, the API, or an etcd backup) can decode it in a single command.

```bash
# Base64 encoding is trivially reversible
echo -n "mypassword123" | base64
# Output: bXlwYXNzd29yZDEyMw==

echo -n "bXlwYXNzd29yZDEyMw==" | base64 -d
# Output: mypassword123   ← fully readable ❌
```

This is precisely why Sections 4–6 exist: native Secrets are a starting point, not a complete secret-management solution.

---

### 🔹 2.2 Creating a Secret

Just like ConfigMaps, Secrets can be created imperatively from files or literals, or declaratively via YAML.

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

Fastest path for quick tests, since there's no need to create intermediate files first.

```bash
kubectl create secret generic mysecret \
  --from-literal=username=root \
  --from-literal=password=mypassword123
```

**Method 3 — Declarative YAML (values must be Base64-encoded):**

When writing a Secret manifest by hand under the `data` field, every value must already be Base64-encoded — Kubernetes does not encode it for you at this layer.

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

(Note that Section 2.5 later shows an alternative `stringData` field, which lets you skip the manual Base64 step entirely and write plain-text values directly.)

---

### 🔹 2.3 Use Case 1 — Secret Mounted as a Volume

Mounting a Secret as a volume makes each key appear as a separate **file** inside the container — and critically, Kubernetes automatically **decodes** the Base64 value first, so the application sees the real plaintext credential on disk, not the encoded form.

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

> 💡 **How it works:** Kubernetes decodes the Base64 values and writes them as plain-text files inside the container. Each Secret key becomes its own file — `username.txt` and `password.txt` appear as actual files under `/tmp/mysecret/`. Mounting `readOnly: true` is good practice so a compromised container process cannot tamper with the credential files.

---

### 🔹 2.4 Use Case 2 — Secret as Environment Variable

Just like ConfigMaps, a Secret key can be injected as a single **environment variable**, with Kubernetes automatically decoding the Base64 value for you.

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

As with ConfigMaps, environment-variable injection of a Secret is a one-time, start-up-only operation — updating the underlying Secret will not update an already-running container's environment.

---

### 🔹 2.5 Use Case 3 — Secret in a Deployment (DB Credentials)

A very common real-world scenario is passing a full set of database credentials into an application Deployment. Here the manifest uses `stringData` instead of `data`, which lets you write plain-text values directly — Kubernetes performs the Base64 encoding for you automatically when the object is stored.

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

Notice the manifest also sets CPU/memory `resources` — a good habit whenever you're defining a real application Deployment, independent of how the Secret itself is consumed.

---

### 🔹 2.6 Use Case 4 — ImagePullSecret (Private Registry)

Secrets aren't only for application credentials — a special-purpose Secret can also authenticate the **kubelet itself** when it needs to pull a container image from a **private registry** (Docker Hub private repos, AWS ECR, GCR, etc.).

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

Unlike the earlier use cases, `imagePullSecrets` is referenced at the **Pod spec** level (not inside a container's `env`/`volumeMounts`), because it is used by the kubelet during the image-pull phase, before the container process even starts.

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

The table makes clear that ConfigMaps and Secrets share almost identical *mechanics* (same consumption patterns, same 1 MB size ceiling, same auto-update behaviour for volume mounts) — the real difference is entirely about **intent and encoding**, not capability. This is exactly why it's so easy to misuse a ConfigMap for something sensitive: Kubernetes will happily let you, even though it offers none of a Secret's (limited) protections.

---

## ⚠️ 4. Limitations of Native Kubernetes Secrets

Understanding the limitations of native Secrets is essential before choosing a secret management strategy — this is the motivation for everything covered in Sections 5 and 6.

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

Two limitations deserve special attention: "RBAC alone is insufficient" means that even a well-locked-down cluster can leak secret values through a Pod that has the Secret mounted, since anyone who can `exec` into that Pod (or read its running environment) effectively has the same access as someone who ran `kubectl get secret`. And "no automatic rotation" means a single leaked credential — from a laptop, a log file, or a compromised CI pipeline — stays valid indefinitely unless a human notices and manually rotates it.

---

## ☁️ 5. AWS Secrets Manager — External Secret Storage

### 🔹 5.1 What is AWS Secrets Manager?

**AWS Secrets Manager** is a fully managed AWS service purpose-built for storing, rotating, and retrieving secrets such as database credentials, API keys, and TLS certificates — everything native Kubernetes Secrets lack, delivered as a managed service:

- ✅ **Encryption at rest** using AWS KMS
- ✅ **Automatic rotation** of credentials (RDS passwords, IAM keys)
- ✅ **Fine-grained IAM access control**
- ✅ **Full audit trail** via AWS CloudTrail
- ✅ **Versioning** — access previous secret values

Because it lives outside the cluster entirely, it also sidesteps the etcd-plaintext and no-audit-trail problems described in Section 4.

---

### 🔹 5.2 ESO — External Secrets Operator

**External Secrets Operator (ESO)** is the Kubernetes operator that bridges the gap between a cluster and an external secret management system like AWS Secrets Manager. Concretely, it:

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

The elegance of this design is that the **only** thing that ever touches Git is a path reference — the actual secret value never leaves the external system except to be materialized, at runtime, as a native Secret inside the cluster.

---

### 🔹 5.3 Installing ESO

ESO is installed like any other cluster operator, via its official Helm chart.

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

The `installCRDs=true` flag ensures the `SecretStore` and `ExternalSecret` custom resource definitions (used throughout the rest of this section) are registered with the cluster's API server as part of the install.

---

### 🔹 5.4 SecretStore — Connect ESO to AWS Secrets Manager

A **SecretStore** is the object that defines *how* ESO authenticates to and reaches an external secret backend — in this case, AWS Secrets Manager. There are two authentication approaches, suited to different environments.

**Option A — Using IAM Role (IRSA on EKS — recommended):**

The production-grade approach on EKS: ESO's ServiceAccount is bound to an IAM role via IRSA (IAM Roles for Service Accounts), so no static AWS credentials ever need to be stored in the cluster at all.

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

Simpler to set up for a quick proof-of-concept, but it reintroduces a static credential into the cluster (as a Secret) — which is exactly the kind of long-lived credential this whole architecture is trying to avoid. Use Option A in production.

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

With the SecretStore in place, the next step is to actually create the secret in AWS, and then tell ESO which fields to pull into the cluster.

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

Note `refreshInterval: "1h"` — ESO re-checks AWS Secrets Manager on this cadence and keeps the resulting `db-credentials-k8s` Secret in sync automatically, so a rotation performed in AWS eventually propagates into the cluster without any manual `kubectl apply`.

---

## 🔑 6. HashiCorp Vault — Dynamic Secret Management

### 🔹 6.1 What is Vault?

**HashiCorp Vault** is an open-source, enterprise-grade secret management system that goes a step further than either native Secrets or AWS Secrets Manager. Its standout differentiator is **dynamic secrets** — rather than just storing a static credential, Vault can *generate* short-lived, automatically expiring credentials on demand, on a per-request basis.

**Vault capabilities:**
- ✅ **Static secrets** — store and retrieve secrets (like AWS Secrets Manager)
- ✅ **Dynamic secrets** — generate short-lived AWS IAM users, DB credentials, TLS certs on demand
- ✅ **Encryption as a Service** — encrypt/decrypt data without storing it
- ✅ **PKI** — act as a Certificate Authority
- ✅ **Fine-grained policies** — path and capability-based access control
- ✅ **Audit logging** — every secret access logged with full metadata

The dynamic-secrets feature in particular means that even if a credential is somehow leaked, its blast radius is naturally bounded by its short TTL, rather than remaining valid forever like a traditional static password.

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

Reading across the rows, the progression is clear: native K8s Secrets provide the weakest guarantees, AWS Secrets Manager adds encryption/rotation/audit but is locked to AWS, and Vault adds dynamic, short-lived credentials on top while remaining cloud-agnostic — at the cost of needing to run and operate Vault itself (or pay for HashiCorp Cloud/Enterprise).

---

### 🔹 6.3 Installing Vault on Kubernetes

Vault can be run either as a workload inside the cluster it's protecting, or as an external service the cluster talks to.

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

Both options exist for good reason: running Vault inside Kubernetes (Option A) keeps everything in one place, while running it externally on EC2 (Option B) decouples Vault's own availability from the cluster it serves — useful if the cluster itself is one of the things Vault needs to protect access to.

---

### 🔹 6.4 Vault Configuration — Step by Step

Once Vault is running, it needs to be initialised, populated with secrets, and configured to trust the cluster's ServiceAccounts before ESO can use it.

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

Notice the layered access-control model here: the **policy** (Step 7) scopes what paths can be read at all, while the **role** (Step 8) scopes *which* Kubernetes ServiceAccount, in *which* namespace, is allowed to assume that policy — and for how long (`ttl=1h`). This is the path-based, fine-grained control referenced in the comparison table above.

---

### 🔹 6.5 ESO — SecretStore for Vault

Just as in Section 5.4 for AWS, ESO needs a `SecretStore` object to know how to reach Vault — but this time using Vault's own Kubernetes auth method rather than IAM/IRSA.

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

The `role: "eso-payment-role"` field ties this SecretStore directly back to the Vault role created in Step 8 of Section 6.4 — a mismatch here (wrong role name, wrong ServiceAccount) is the most common cause of a SecretStore failing to become `Valid`.

---

### 🔹 6.6 ExternalSecret — Pull from Vault

With the SecretStore connected, an `ExternalSecret` object pulls specific fields out of Vault and materialises them as a native Kubernetes Secret — structurally identical to the AWS example in Section 5.5, just pointed at Vault instead.

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

Notice the `remoteRef.key` value is written **without** the `secret/data/` prefix, even though that prefix appears in the Vault policy path from Section 6.4 — ESO's Vault provider adds the `data/` segment automatically for KV v2 mounts.

---

### 🔹 6.7 Use the ESO-created Secret in a Pod

The final step closes the loop: the K8s Secret that ESO created (`db-credentials-k8s`) is, at this point, a completely ordinary Kubernetes Secret — it can be consumed with exactly the same `envFrom`, `env`, or volume-mount mechanisms shown back in Section 2.

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

This is the payoff of the entire ESO + Vault architecture described across Section 6: the Pod spec, the ExternalSecret manifest, and everything else that lives in Git remain completely free of actual secret material, while the running Pod still ends up with the real, decoded credential available exactly where the application expects it.

---

## 🔒 7. Secret Management — Defence in Depth

No single control is sufficient on its own — secret management in a production Kubernetes environment is really a **layered** set of controls, each catching what the layer before it might miss.

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

Read top to bottom, the layers move from "before the secret ever reaches Git" (Layers 1–2), through "how the secret is stored and accessed inside the cluster" (Layers 3–5), to "how the secret is actually managed externally over its lifetime" (Layers 6–10). A mature setup implements all ten layers together rather than relying on any single one.

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

Taken together, this document traces a natural progression: start with **ConfigMaps** for non-sensitive configuration, move to native **Secrets** for anything sensitive while understanding their real limitations, and finally graduate to **ESO paired with AWS Secrets Manager or HashiCorp Vault** once GitOps, encryption at rest, rotation, and audit trails become requirements rather than nice-to-haves.
