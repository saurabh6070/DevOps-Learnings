# 🛡️ HashiCorp Vault on K3s Kubernetes - Development Demo
This guide demonstrates how to deploy HashiCorp Vault in development mode on a K3s (lightweight Kubernetes) cluster using Helm. It also covers injecting secrets into a Kubernetes Pod using Vault Agent Injector.

### 📦 1. Prerequisites
a. Kubernetes cluster (K3s used here) <br>
b. kubectl CLI <br>
c. helm CLI <br>


### 🚀 2. Install Vault with Helm (Dev Mode)
⚠️ Dev mode is insecure and should only be used for testing/learning purposes.


```bash
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
```
#### Install Vault in dev mode

```bash
helm install vault hashicorp/vault --set "server.dev.enabled=true"

#Verify installation:

helm ls
helm status vault
kubectl get pods
```
 
### 🔌 3. Connect to Vault Pod

```bash
kubectl exec -it vault-0 -- sh
vault status
```
Expected Output:
```bash
Seal Type       shamir
Initialized     true
Sealed          false
Storage Type    inmem
Version         1.19.0
```


### 🔐 4. Store and Retrieve a Secret
Inside the Vault pod:
```bash
vault kv put secret/hello foo=bar
vault kv get secret/hello
```

Expected Output:
```bash
Key    Value
foo    bar
```

### ⚙️ 5. Enable Kubernetes Auth Method
Inside the Vault pod:

```bash
vault auth enable kubernetes

# Set Kubernetes auth config
VAULT_SA_TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
K8S_HOST="https://${KUBERNETES_PORT_443_TCP_ADDR}:443"
cat /var/run/secrets/kubernetes.io/serviceaccount/ca.crt > /tmp/ca.crt

vault write auth/kubernetes/config \
  token_reviewer_jwt="$VAULT_SA_TOKEN" \
  kubernetes_host="$K8S_HOST" \
  kubernetes_ca_cert=@/tmp/ca.crt
```


📜 6. Create Vault Policy
Save this as /tmp/myapp-policy.hcl:

```bash
# myapp-policy.hcl
path "secret/data/hello" {
  capabilities = ["read"]
}
```
Write the policy and role:

```bash
vault policy write myapp-policy /tmp/myapp-policy.hcl

vault write auth/kubernetes/role/myapp-role \
  bound_service_account_names=myapp-sa \
  bound_service_account_namespaces=default \
  policies=myapp-policy \
  ttl=1h
```

🔧 7. Define Kubernetes Resources
#### sa.yml - ServiceAccount
```apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: default

#Apply the service account:

kubectl apply -f sa.yml
```

#### pod.yml - Pod Definition with Vault Injection
```apiVersion: v1
kind: Pod
metadata:
  name: myapp
  annotations:
    vault.hashicorp.com/agent-inject: "true"
    vault.hashicorp.com/role: "myapp-role"
    vault.hashicorp.com/agent-inject-secret-hello: "secret/data/hello"
spec:
  serviceAccountName: myapp-sa
  containers:
  - name: app
    image: nginx

#Deploy the pod:
kubectl apply -f pod.yml
```

📁 8. Validate Secret Injection
List the injected secret:

bash
Copy
Edit
kubectl exec -it myapp -- ls /vault/secrets
View the secret:

bash
Copy
Edit
kubectl exec -it myapp -- cat /vault/secrets/hello
Expected Output:

json
Copy
Edit
data: map[foo:bar]
📊 9. Confirm Pod Structure
bash
Copy
Edit
kubectl describe pod myapp
Check that the Vault Agent and Init Containers are running and that the annotation status is injected.

🧪 10. Inside Pod - File System Check
bash
Copy
Edit
kubectl exec -it myapp -- bash
df -kh
Check for /vault/secrets mount with injected content.
