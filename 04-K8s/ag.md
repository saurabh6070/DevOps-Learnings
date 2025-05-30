🛠️ 1. Create a Private Key and Certificate Signing Request (CSR)
🔧 Generate a Private Key

    openssl genrsa -out my-user.key 2048
📝 Generate a CSR
This will generate a request with a subject (/CN=my-user/O=dev-team).

    openssl req -new -key my-user.key -out my-user.csr -subj "/CN=my-user/O=dev-team"
CN=my-user is the Common Name, representing the user identity.
O=dev-team is the Organization, used for RBAC group bindings.

📦 2. Create a Kubernetes CertificateSigningRequest (CSR) Object

🔄 Encode the CSR in Base64

    cat my-user.csr | base64 | tr -d '\n'
📄 Create a CSR Manifest
Save the following YAML as my-user-csr.yaml:

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

🚀 3. Submit the CSR to Kubernetes

    kubectl apply -f my-user-csr.yaml
✅ 4. Approve the CSR

    kubectl certificate approve my-user-csr
📥 5. Retrieve the Signed Certificate

kubectl get csr my-user-csr -o jsonpath='{.status.certificate}' | base64 -d > my-user.crt
Now you have:
my-user.key: Private key
my-user.crt: Signed certificate

📁 6. Create a Custom kubeconfig Using Your Certificate

🧱 Collect Required Info
You need:

Kubernetes cluster CA certificate (can get from /etc/kubernetes/pki/ca.crt or from an existing kubeconfig)

Cluster API endpoint URL

🔐 Add CA Cert (optional step to extract it)

    kubectl config view --raw -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' | base64 -d > ca.crt
🧾 Build a kubeconfig

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
Replace:
<API_SERVER_ENDPOINT> with your cluster’s endpoint (e.g., https://192.168.1.100:6443)

🔄 7. Test Your Access

Try running:
kubectl get pods

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