kubectl get nodes -o wide
kubectl get ns
kubectl get pods -A -o wide
kubectl get pods -n <namespace> -o wide
kubectl top pods -A (List the CPU and memory usage of all pods)
kubectl describe pod <pod_name> -n <namespace> 
kubectl top pod <pod_name> -n <namespace> --containers (Display the CPU and Memory usage of Containers associated with the pod)
kubectl get services --all-namespaces
kubectl get deployments --all-namespaces
kubectl get cs ( Display the status of K8s Scheduler, Controller-Manager and ETCD )


kubectl get pods -n kube-system|grep calico
kubectl get pod -n <namespace_of_portworx>
kubectl get pods -o='custom-columns=PODS:.metadata.name,Images:.spec.containers[*].image' -A (List the Pods and respective Images with version details)
kubectl get pods --field-selector=status.phase!=Running --all-namespaces (List all the UnHealthy pods in the Cluster)
kubectl get pods --field-selector=status.phase=Running --all-namespaces (List all the pods in Running state )
kubectl get pods -o='custom-columns=PODS:.metadata.name,CONTAINERS:.spec.containers[*].name' -A (List all the pods along with their containers associated)
kubectl get endpoints (List all the Service Endpoints within the K8s cluster)
kubectl cluster-info  (Display the basic Cluster-Info )
kubectl logs <pod-name> -n <namespace>  (Display the pods logs )
kubectl get pod --template '{{.status.initContainerStatuses}}' --namespace=<namespace> <pod-name> (Display the status of InitContainer for a given pod)


To Check pod serving for any service :-

kubectl get svc <service-name> -n <namespace> -o yaml | grep -i selector

If selector is app=my-app, then pod serving for this service is ->

kubectl get pods -n <namespace> -l app=my-app


