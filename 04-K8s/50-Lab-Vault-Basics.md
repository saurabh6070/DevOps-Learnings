# 🛡️ HashiCorp Vault on K3s Kubernetes - Development Demo
This guide demonstrates how to deploy HashiCorp Vault in development mode on a K3s (lightweight Kubernetes) cluster using Helm. It also covers injecting secrets into a Kubernetes Pod using Vault Agent Injector.

### 📦 1. Prerequisites
a. Kubernetes cluster (K3s used here) <br>
b. kubectl CLI <br>
c. helm CLI <br>


### 🚀 2. Install Vault with Helm (Dev Mode)
⚠️ Dev mode is insecure and should only be used for testing/learning purposes.


```
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
```
#### Install Vault in dev mode

```
helm install vault hashicorp/vault --set "server.dev.enabled=true"

#Verify installation:

helm ls
helm status vault
kubectl get pods
```
 
### 🔌 3. Connect to Vault Pod

```
kubectl exec -it vault-0 -- sh
vault status
```
Expected Output:
```
Seal Type       shamir
Initialized     true
Sealed          false
Storage Type    inmem
Version         1.19.0
```


### 🔐 4. Store and Retrieve a Secret
Inside the Vault pod:
```
vault kv put secret/hello foo=bar
vault kv get secret/hello
```

Expected Output:
```
Key    Value
foo    bar
```

### ⚙️ 5. Enable Kubernetes Auth Method
Inside the Vault pod:

```
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


### 📜 6. Create Vault Policy
Save this as /tmp/myapp-policy.hcl:

```
# myapp-policy.hcl
path "secret/data/hello" {
  capabilities = ["read"]
}
```
Write the policy and role:

```
vault policy write myapp-policy /tmp/myapp-policy.hcl

vault write auth/kubernetes/role/myapp-role \
  bound_service_account_names=myapp-sa \
  bound_service_account_namespaces=default \
  policies=myapp-policy \
  ttl=1h
```

### 🔧 7. Define Kubernetes Resources
#### sa.yml - ServiceAccount
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: default

#Apply the service account:

kubectl apply -f sa.yml
```

#### pod.yml - Pod Definition with Vault Injection
```
apiVersion: v1
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

### 📁 8. Validate Secret Injection
List the injected secret:

```
kubectl exec -it myapp -- ls /vault/secrets

#View the secret:

kubectl exec -it myapp -- cat /vault/secrets/hello
```

Expected Output:

```
data: map[foo:bar]
```

### 📊 9. Confirm Pod Structure

```
kubectl describe pod myapp
```

Check that the Vault Agent and Init Containers are running and that the annotation status is injected.

### 🧪 10. Inside Pod - File System Check
```
kubectl exec -it myapp -- bash
df -kh
Check for /vault/secrets mount with injected content.
```

### ✅ 11. Conclusion
In summary, we have: <br>
    1. Deployed Vault in dev mode via Helm <br>
    2. Stored and retrieved a secret <br>
    3. Enabled Kubernetes auth in Vault <br>
    4. Defined policy and role for service account <br>
    5. Created service account and pod with Vault Agent Injector <br>
    6. Verified secrets injected into a live pod <br>
This demonstrates a complete, end-to-end Vault workflow on Kubernetes. <br>
 <br>

### 👋 12. Wrap-Up
Next time, we can explore production-grade Vault setup with TLS, auto-unseal, persistent storage, dynamic secrets, and secret rotation. But for now, this lab gives you the core building blocks. Thank you and see you in the next session!



<br><br><br><br><br>

Complete Logs for this Lab Setup can be taken for reference from below link :-
https://drive.google.com/drive/u/5/folders/1nJgsQwxAV7Peb7BrfXC979VCppIyyvNd

