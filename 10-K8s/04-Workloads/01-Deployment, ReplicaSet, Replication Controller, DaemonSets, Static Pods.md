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

