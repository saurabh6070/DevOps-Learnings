Master-Plane Upgrade and Worker-Plane Upgrade (Sequential kubeadm release bumps)




001 -> POD Eviction time is set in Kube-Controller. Default value is 5 minutes.
This is the time after which Master considers any POD as dead if the POD is not come into running state.

002 -> Incase of OS Upgrade, check if all the PODs in that node are part of ReplicaSet, ReplicationController, etc and how many replicase of this PODs there in other nodes.
The best option incase of OS-Upgarde is to drain the Nod i.e. gracefully move all PODs from this node to other nodes. Also, need to cordon this node until OS Upgrade is completed to avod scheduling of any other POD in this Node.
		kubectl drain node01
		kubectl cordon node01
After OS Upgrade :-
		kubectl uncordon node01


001 -> While draining nodes, this issue can be seen :-
* cannot delete DaemonSet-managed Pods (use --ignore-daemonsets to ignore)
	Solution :-
	kubectl drain node01 --ignore-daemonsets
* error: unable to drain node "node01" due to error:cannot delete Pods declare no controller (use --force to override): default/hr-app, continuing command... 
This issue arises when any pod which is not part of replication contrller/replicasaSet is present on Node that needs to be drained out.
	Solution :- 
	kubectl drain node01 --ignore-daemonsets --force


001 -> Kubernetes Version :- Example - v 1.11.3 (Here, 1 -Major, 11 - Minor, 3 -> Patch)

002 -> Version of almost all component of K8 will be same as kubernetes cluster :-
API-Server, Comtroller-Manager, Scheduler, Kubelet, Kube-Proxy, Kubectl all have same version as that of k8 cluster.
But Etcd Cluster, CoreDNS will have different version.
The Release Notes explains in detail about the changes/modifications.



001 -> At any stage of Upgrade in K8, Kube-API Server version should not be lower than other components in the cluster. (say Version X= v1.10)
Version of Controller-Manager and Kube-Scheduler can be only one version less than the version of Kube-API Server. (X-1, i.e. v1.9 or 1.10)
Version of Kubelet and Kube-Proxy can be only two version less than the version of Kube-AP Server. (X-2, i.e. v1.8 or 1.9 or 1.10)

002 -> Only latest three version of K8 are supported.
If the latest version v1.15 is the latest version, then the supported versions are v1.13 or v1.14 or v1.15
In case of Upgrade, need to upgrade one version at a time, not recommended to skip any version for upgrade.

003 -> Upgrade Commands for Master-Node :-
cat /etc/*release* (If its Ubuntu follow instructions for Ubuntu)
apt-get upgrade -y kubeadm=1.12.0-00
kubeadm upgrade apply v1.13.4
kubectl node list (Version of each node is also displayed. This version is the version of kubelet installed in the node.)
apt-get upgrade -y kubelet=1.12.0-00
sysctl restart kubelet
kubectl node list (version of kubelet in each Master will be upgraded to newer version)
kubeadm upgrade apply v1.12.0
kubeadm upgrade plan (Lists current/latest version of Kubeadm, Control-Plan components, Etcd and CoreDNS)

004 -> Upggrade Commands for Worker-Node :-
kubectl drain node-01
apt-get upgrade -y kubeadm=1.12.0-00
apt-get upgrade -y kubelet=1.12.0-00
kubeadm upgrade node config --kubelet-version v1.12.0
systemctl restart kubelet
kubectl uncordon node-01


004 -> To check the version of the cluster :-
kubectl get nodes
All Master/Worker must be on same version in the output and this version is the Cluster Version.


005 -> To check number of applications hosted :-
Add total number of Deployment Object + ReplicaSet Object , etc (but not add PODs since they are cretaed by these other object)


006 -> To check what can be the latest version to upgrade for kubeadm :-
sudo kubeadm upgrade plan



002 -> Backup of Resource Configs :-
kubectl get all --all-namespaces -o yaml > Backup_all_namepsaces.yaml

