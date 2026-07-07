RBAC (Declarative & Imperative Examples) (Roles, ClusterRoles, Bindings)





Namespace, Service-Account, Role, Role-Binding


Whenever a namespace is created, no role is present initially in that Namespace. But default Service-Account always gets created whenever namespace is created.


Service-Account is just like a user, that will be authorized by API-Server whenever any operation of listing/creation/deletion of any resource is performed on this namespace.

Role is a set of permissions which contains policies like level of access on resources where this role is used. Role can be created in any particular Namespace which can be assigned to any Service-Account. It can be assigned to multiple Service-Accounts. Scope of Role is at Namespace level. Role-Binding basically binds Role with Service-Account.

Scope of ClusterRole is at Cluster Level i.e. not related to any of the one Namespace. Cluster Role Binding basically binds Cluster Role with Service-Account.

001 -> List Service-Account
		kubectl get sa kube-scheduler -n kube-system
		kubectl get sa myscheduler -n kube-system


002 -> Create Config-Map from a file
		kubectl create configmap my-scheduler-config --from-file=/rootmy-scheduler-config.yaml -n kube-system
		kubectl get cm my-scheduler my-scheduler-config -n kube-system


003 -> List Cluster Role Binding
		kubectl get clusterrolebinding

Role/ Cluster-Role


A Role defines what actions a subject (user, service account, etc.) can perform on resources within a namespace.
A ClusterRole defines permissions at the cluster level (i.e., across all namespaces). It can be used for cluster-wide resources, such as nodes or namespaces.


apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: admin-role
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "create", "delete", "update"]



apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-admin-role
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["namespaces"]
  verbs: ["get", "list"]


Role-Binding/ Cluster Role-Binding



A RoleBinding binds a Role to one or more subjects, granting them the permissions defined in the role.
A ClusterRoleBinding binds a ClusterRole to a subject across the entire cluster. Unlike a RoleBinding, which is limited to a specific namespace, ClusterRoleBinding applies cluster-wide.


apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: admin-rolebinding
  namespace: default
subjects:
- kind: User
  name: "johndoe"
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: admin-role
  apiGroup: rbac.authorization.k8s.io


apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-rolebinding
subjects:
- kind: User
  name: "adminuser"
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-admin-role
  apiGroup: rbac.authorization.k8s.io


Service-Account




• Create the ServiceAccount:

apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-service-account


• Create a Role to Read Pods:

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]


• Create a RoleBinding:

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader-binding
  namespace: default
subjects:
- kind: ServiceAccount
  name: my-service-account
  namespace: default
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io


• Create a Pod that Uses the ServiceAccount:

apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  serviceAccountName: my-service-account
  containers:
  - name: nginx-container
    image: nginx


• Apply All Resources:

kubectl apply -f service-account.yaml
kubectl apply -f role.yaml
kubectl apply -f role-binding.yaml
kubectl apply -f pod.yaml

