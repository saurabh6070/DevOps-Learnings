ETCD: Administration, Backup, and Restore (The backbone of CKA cluster recovery exams)





002 -> To install etcdctl :-
		apt-get install etcd-client
			
	   
003 -> To check value of secrets stored in etcd-server,
	--> ETCDCTL=3 etcdctl --cacert=/etc/kubernetes/pki/etcd/ca.cert --cert=/etc/kubernetes/pki/etcd/server.cert --key=/etc/kubernetes/pki/etcd/server.key get /registry/secrets/default/my-secret
	--> ETCDCTL=3 etcdctl --cacert=/etc/kubernetes/pki/etcd/ca.cert --cert=/etc/kubernetes/pki/etcd/server.cert --key=/etc/kubernetes/pki/etcd/server.key get /registry/secrets/default/my-secret | hexdump -C
	Output :- In the output of above command, we can see jumbled information, but the key value of secret in the decoded format can be seen, even we have stored the data in secret in decoded format. That means, by default the data in etcd-server is stored in decoded format.
	
004 -> To view, what is configured in API_Server for this storing secret in etcd-server :-
		ps -aux | grep kube-api | grep "encryption-provider-config" 
			Output = Blank, no output
		cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep "encryption-provider-config"
					Output = Blank, no output
	This implies encryption at rest in etcd-server is not applied in the config of api-server.

005 -> To recreate all the secrets again with the same configuration :-
		kubectl get secrets --all-namespaces -o json | kubectl replace -f -
		



003 -> Backup of ETCD Cluster :-
* ETCD is deployed on all Master Nodes/ Control Plane Nodes.
* Describe ETCD Pods to get the path where it is storing all the data. Generally it is, /var/lib/data/
* Take backup of ETCD Cluster :-
ETCDCTL_API=3 etcdctl snapshot save snapshot.db --endpoints=https://127.0.0.1:2379 --cacert=/etc/etcd/ca.crt --cert=/etc/etcd/etcd-server.crt --key=/etc/etcd/etcd-server.key
ETCDCTL_API=3 etcdctl snapshot status snapshot.db  --endpoints=https://127.0.0.1:2379 --cacert=/etc/etcd/ca.crt --cert=/etc/etcd/etcd-server.crt --key=/etc/etcd/etcd-server.key
ls (Output -> snapshot.db)

004 -> To restore ETCD Cluster from DB Backup File :-
* Stop API-Server
service kube-apiserver stop
* Restore etcd data from DB Backup :-
ETCDCTL_API=3 etcdctl snapshot restore snapshot.db --data-dir  /var/lib/etcd-from-backup/  --endpoints=https://127.0.0.1:2379 --cacert=/etc/etcd/ca.crt --cert=/etc/etcd/etcd-server.crt --key=/etc/etcd/etcd-server.key
* Change the path of etcd from /var/lib/etcd/ to /var/lib/etcd-from-backup/
 -> cat /etc/kubernetes/manifests/etcd.yaml| grep -i hostpath -A 1 | grep -i var
      path: /var/lib/etcd/
 -> vi /etc/kubernetes/manifests/etcd.yaml
 -> cat /etc/kubernetes/manifests/etcd.yaml| grep -i hostpath -A 1 | grep -i var
      path: /var/lib/etcd-from-backup/
* Delete the POD for etcd
kubectl delete pod -n kube-system etcd-controlplane
* To check the process :-
watch "crictl ps | grep etcd"
* Also, after this kube-scheduler, kube-controller-manager also restarts.
* systemctl daemon-reload
* service etcd restart
* NOTE :- If changing the data-dir path to new path in etcd.yaml file, then need to change the path in the volumeMounts as well to new path. Though, it is not needed to make these two changes.
Only one change in hostpath is needed.



005 -> ETCDCTL :-
* etcdctl is a command line client for etcd.
In all our Kubernetes Hands-on labs, the ETCD key-value database is deployed as a static pod on the master. The version used is v3.
To make use of etcdctl for tasks such as back up and restore, make sure that you set the ETCDCTL_API to 3.
You can do this by exporting the variable ETCDCTL_API prior to using the etcdctl client. This can be done as follows:
export ETCDCTL_API=3
* On the Master Node:
For example, if you want to take a snapshot of etcd, use:
etcdctl snapshot save -h and keep a note of the mandatory global options.
Since our ETCD database is TLS-Enabled, the following options are mandatory:
--cacert                                                verify certificates of TLS-enabled secure servers using this CA bundle
--cert                                                    identify secure client using this TLS certificate file
--endpoints=[127.0.0.1:2379]          This is the default as ETCD is running on master node and exposed on localhost 2379.
--key                                                      identify secure client using this TLS key file
* Similarly use the help option for snapshot restore to see all available options for restoring the backup.
etcdctl snapshot restore -h



006 -> ETCD path :-
cat /etc/kubernetes/manifests/etcd.yaml | grep -i data-dir


001 -> To get the clusters defined in kubeconfig :-
kubectl config get-clusters 


002 -> To change defualt to any cluster :-
kubectl config use-context cluster1
	-> To check how many nodes assigned to cluster1 :-
kubectl get nodes


003 -> To check if ETCD used is stack ETCD or External ETCD :-
* Login to Control-Plane using ssh
* Check if any pod in the kube-system deployed with the name as etcd
* If yes, then it is stack ETCD (Internal) otherwise it is Extrnal ETCD.


004 -> To check the IP of ETCD-Cluster,
* Describe POD kube-api-server and grep for "etcd-servers" or "2379", the IP mentioned with this port must be IP of etcd. We described API-Server becuase API-Server communicates with all the PODs.


005 -> To check the datadir of External-ETCD Server :-
* ssh in to the External ETCD-Server :-
student-node ~ ➜  ssh 192.36.3.6
* Check the path of data-dir in the process of etcd :-
etcd-server ~ ➜  ps -ef | grep -i etcd
Output :-
etcd         810       1  0 17:54 ?        00:01:13 /usr/local/bin/etcd --name etcd-server --data-dir=/var/lib/etcd-data --cert-file=/etc/etcd/pki/etcd.pem --key-file=/etc/etcd/pki/etcd-key.pem --peer-cert-file=/etc/etcd/pki/etcd.pem --peer-key-file=/etc/etcd/pki/etcd-key.pem --trusted-ca-file=/etc/etcd/pki/ca.pem --peer-trusted-ca-file=/etc/etcd/pki/ca.pem --peer-client-cert-auth --client-cert-auth --initial-advertise-peer-urls https://192.36.3.6:2380 --listen-peer-urls https://192.36.3.6:2380 --advertise-client-urls https://192.36.3.6:2379 --listen-client-urls https://192.36.3.6:2379,https://127.0.0.1:2379 --initial-cluster-token etcd-cluster-1 --initial-cluster etcd-server=https://192.36.3.6:2380 --initial-cluster-state new
root        1158    1038  0 19:26 pts/0    00:00:00 grep -i etcd

006 -> To check the members in External-ETCD Server :-
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 --cacert=/etc/etcd/pki/ca.pem --cert=/etc/etcd/pki/etcd.pem --key=/etc/etcd/pki/etcd-key.pem member list
Output :- Only 1 Member with IP :- 192.36.3.6
56a6cbd855a43a08, started, etcd-server, https://192.36.3.6:2380, https://192.36.3.6:2379, false
