# 📘 Kubernetes Imperative Commands Cheat Sheet (CKA Exam)

---

## 1. Pods

- Create Pod:  
  `kubectl run mypod --image=nginx`
- Export Pod YAML:  
  `kubectl run mypod --image=nginx --dry-run=client -o yaml > pod.yaml`

---


## 2. Deployments
- Create Deployment:
  `kubectl create --help`
  `kubectl create deployment --help`
  `kubectl create deployemt mydep --replicas=3 --image=busybox --dry-run=client`
  `kubectl create deployment mydep --image=nginx`
- Scale Deployment:  
  `kubectl scale deployment mydep --replicas=3`
- Export Deployment YAML:  
  `kubectl create deployment mydep --image=nginx --dry-run=client -o yaml > dep.yaml`

## 3. Services
- Expose Deployment as ClusterIP:  
  `kubectl expose deployment mydep --port=80 --target-port=80`
- Expose Deployment as NodePort:  
  `kubectl expose deployment mydep --port=80 --target-port=80 --type=NodePort`
- Create Service via command:  
  `kubectl create service nodeport mysvc --tcp=8080:8080 --node-port=30080`

## 4. ConfigMaps & Secrets
- Create ConfigMap from literal:  
  `kubectl create configmap myconfig --from-literal=key=value`
- Create ConfigMap from file:  
  `kubectl create configmap myconfig --from-file=config.txt`
- Create Secret from literal:  
  `kubectl create secret generic mysecret --from-literal=DB_PASS=passwd`
- Export Secret YAML:  
  `kubectl create secret generic mysecret --from-literal=DB_PASS=passwd --dry-run=client -o yaml > secret.yaml`

## 5. Namespaces
- Create Namespace:  
  `kubectl create namespace dev`
- Run Pod in Namespace:  
  `kubectl run mypod --image=nginx -n dev`

## 6. Scheduling
- Assign Pod to Node:  
  Add in Pod spec:  
  ```yaml
  spec:
    nodeName: node01

- Taint Node:
`kubectl taint nodes node01 key=value:NoSchedule`

- Remove Taint:
`kubectl taint nodes node01 key=value:NoSchedule-`

## 7. Resource Management
- Set Resource Requests/Limits in Pod:

  ```yaml
  resources:
  requests:
  	  cpu: "100m"
  	  memory: "128Mi"
  limits:
  	  cpu: "200m"
  	  memory: "256Mi"
## 8. DaemonSets
- Create DaemonSet from Deployment YAML:
`kubectl create deployment myds --image=nginx --dry-run=client -o yaml > ds.yaml` 
(then change kind: Deployment → kind: DaemonSet)

## 9. Jobs & CronJobs
- Create Job:
`kubectl create job myjob --image=busybox -- sleep 10`

- Create CronJob:
`kubectl create cronjob mycj --image=busybox --schedule="*/1 * * * *" -- sleep 10`

## 10. Rollouts
- Check Rollout Status:
`kubectl rollout status deployment/mydep`

- Undo Rollout:
`kubectl rollout undo deployment/mydep`

- Set New Image:
`kubectl set image deployment/mydep nginx=nginx:1.19`

## 11. Node Maintenance
- Drain Node:
`kubectl drain node01 --ignore-daemonsets --force`

- Cordon Node:
`kubectl cordon node01`

- Uncordon Node:
`kubectl uncordon node01`

## 12. Debugging
- Describe Pod:
`kubectl describe pod mypod`

- Logs:
`kubectl logs mypod`

- Exec into Pod:
`kubectl exec -it mypod -- /bin/sh`

- Events:
`kubectl get events -o wide`
