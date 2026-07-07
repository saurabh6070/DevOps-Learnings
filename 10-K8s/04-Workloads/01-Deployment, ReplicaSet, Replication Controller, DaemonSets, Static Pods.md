Deployment, ReplicaSet, Replication Controller, DaemonSets, Static Pods



Each object in K8 belongs to one particular api class. 
Deployment, Service, ReplicaSet belongs to apiVersion= apps/v1

Different object has a different use-case that’s why these objects are grouped in different api class.

Metadata is data about data. Name and label of any K8 Object are present in Metadata.





6. Deployment Sets
  6.1. Create one deployment of nginx with replica=3
  6.2. Whenever dpeloyemtn sets is created, replicaset is also created implicitly with same name as that of deployment sets.
  6.3. No doubt, we can create 3 separate pods with same label without using Deployment set. But if we do 
	i. Kubectl get deploy -n nginx
	ii. Kubectl get pods --show-labels -n nginx
	Output : will contain label of all pods. Here, you can see hash-label is also generated which is random and unique label (pod-template-hash)for any deployment. This will distinguish pods created from deployment sets with other pods, even if they were explicitly given same labels in pods templates.


001 -> To filter pods with particular label :-
		kubectl get pods --selector app=MyPod
		
002 -> ReplicaSet uses labels and selectors to bind pods to the ReplicaSet.
		For health-check of Pods under ReplicaSet, it uses labels.
		Any pod created manually with the same labels mentioned in Selector-section of ReplicaSet comes under Health-check of this ReplicaSet.
		All the labels in Selector-Section of ReplicaSet must match with the pod in order to bind with each other. In case, label present in ReplicaSet atch with not-required pods, then we must create extra label in selector field of ReplicaSet to ensure difference in labels of extra-pod with this ReplicaSet.



001 -> Create yml file from command for Deployment :-
		kubectl create deployment blue --image=nginx --replicas=3 -o yaml
		kubectl create deployment blue --image=nginx --replicas=3 -o yaml > blue.yml

002 -> DaemonSet, ReplicaSet are very similar in Yaml Definition File. Only one change is the kind.




001 -> DaemonSets are the object which gets created as a single Pod in all the Nodes which are added in the K8 cluster and removes the Pods from the Nodes which are removed from the K8 Cluster.
These Pods can be used for Log-Capture, Monitoring.
Example :- kube-proxy, kube-flannel, Weavenet (for Networking).

002 --> Post K8 v1.12, it uses deafult-scheduler, Node-Affinity to deploy Daemon-Set Pods in each node.

003 ->  kubectl get daemonsets
		kubectl get ds -n kube-system


001 -> kubectl create deployment elasticsearch -n kube-system --image=k8s.gcr.io/fluentd-elasticsearch:1.20 --dry-run=client -o yaml > fluentd.yaml
		then edit this file and change the kind from Deployment to DaemonSets. The structure of Daemon-Set and Deployment is same.


001 -> Static Pods are the Pods which gets created automatically by kubelet when the yml files of these Pods are placed in the Pod-Manifest-Path of kubelet. Generally path is :- /etc/kubernetes/manifests .
To know the path, in Master-Node run :-
			cat /var/lib/kubelet/config.yml | grep staticPodPath
All the yml files for Pod only (Not applicable to Deployment, ReplicaSet, etc) will get created, if it is placed in this path. To create these Pods in the Worker, kubelet of this worker don't even need API-Server, Scheduler, ETCD, Controller.

002 -> ETCD, API-Server, Controller-Manager, Scheduler etc are types of Static-Pods.


003 -> Static-Pods created by Kubelet whereas Daemon-Sets created by Kube API-Server (DaemonSet Controller)
Static Pods deploy control plane components whereas DaemonSets deploy Monitoring Agents, Logging Agents on Nodes.
Both of them ignored by kube-scheduler.
Static Pods gets deployed on Control=Plane/Master-Node. Daemon-Sets gets deployed on all Nodes ncluding Master and Worker.
The spec of a static Pod cannot refer to other API objects (e.g., ServiceAccount, ConfigMap, Secret, etc).
Static pods do not support ephemeral containers.

004 -> To create Static Pods :-
kubectl run static-busybox --image=nginx --dry-run=client -o yaml --command -- sleep 1000 > /etc/kubernetes/manifests/staticpod.yaml


005 -> File Name for Static Pods :- cat /var/lib/kubelet/config.yaml | staticPodPath
This path can be different for each node in a cluster. So, this way we can add any specific static POD for any node.


001 -> kubectl run static-busybox --image=busybox --restart=Never --dry-run=client -o yaml --commmand -- sleep 1000
(Command should be in the end always)




Deployment :-
9. 001 -> Rollout Status
		kubectl get deploy
		kubectl rollout status deployment/myapp-deployment
		kubectl rollout history deployment/myapp-deployment
		
002 -> Deployment Strategy :-
			* Recreate
					-> Delete all Older Pods, then create Pods with new image
					-> Application experience Down-time
			* Rolling-Update
					-> Delete pods one-by-one while creating Pods with the new image at the same time.
					-> Application don't experience downtime.
					-> In this case, new replica-set is created where the number of pods in the new replica-set is increaing one-by-one and at the same time number of pods in old-replica-set is decreasing one-by-one.
					-> Check parameters to set in sepc of deployment for Rolling-Update

003 -> To check deployment strategy :-
		kubectl describe deploy myapps | grep -i strategyType

004 -> To rollout a change :-
		kubectl get deploy
		kubectl rollout undo deploymentName
		kubectl get replicasets
		
		
005 -> To set new image to Deployment Object :-
		kubectl set image deployment/Dep_name container_name=new_image_name
		kubectl set image deployment/myapp-deployment nginx=nginx:1.9.1
