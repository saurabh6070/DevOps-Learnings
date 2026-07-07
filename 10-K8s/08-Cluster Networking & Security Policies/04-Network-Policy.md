Network-Policy (Ingress/Egress isolation rules)



apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-http-https-ingress
  namespace: default
spec:
  podSelector: {}
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 80
    - protocol: TCP
      port: 443
  policyTypes:
  - Ingress



apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-egress-to-ip-range
  namespace: default
spec:
  podSelector: {}
  egress:
  - to:
    - ipBlock:
        cidr: 192.168.1.0/24
  policyTypes:
  - Egress


Default Deny: Kubernetes allows all traffic by default, but when you apply a NetworkPolicy, any traffic that isn’t explicitly allowed is denied.

To use NetworkPolicies, your Kubernetes cluster must have a network plugin that supports them. Common network plugins like Calico, Cilium, or Weave provide support for NetworkPolicies. If you're using a network plugin that doesn't support NetworkPolicies, they won’t have any effect.

