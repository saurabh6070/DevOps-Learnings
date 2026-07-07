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








001 -> In a cluster of large number of nodes ETCD may be taken out from all the Master Nodes and can be deployed n separateset of nodes for High-Availability.

Lecture-241

001 -> Read request coming to any ETCD server is processed directly as it is consistent.
	Write request coming to ETCD will then be forwarded to Leader among the ETCD servers, then it will make changes and update the information to all other ETCD Servers and once Leader gets consent from all other ETCD for the update, then only change is appllied.
	Write is considered as success if more than 50% ETCD has been updated new data successfully.
	Quorum of 1 node is 1.
	Quorum of 2 node is 2.
	Quorum of 3 node is 2.
	Quorum of 4 node is 3.
	Quorum of 5 node is 3.
	
	
002 -> Leader-Election in ETCD is done using RAFT protocol.
	All the members in the ETCD will be given random time for sending request to all other ETCD servers for leader voting.
	None can say no if they get request.
	So the first one to complete the random time interval send the request to all other Members and it get promoted as a leader.
	After short interval of time, leader will update other member that it will continue to be as a role of a leader.

003 -> Install ETCD
				wget -q --https-only "https://github.com/coreos/etd/releases/download/v3.3.9/etcd-v3.3.9-linux-amd64.tar.gz"
				tar -xvf etcd-v3.3.9-linux-amd64.tar.gz
				mv etcd-v3.3.9-linux-amd64/etcd/* /usr/local/bin/
				mkdir -p /etc/etcd/ /var/lib/etcd/
				cp ca.pem kubernetes-key.pem kubernetes.pem /etc/etcd/

004 -> 	Run ETCD Commands :-
					export ETCDCTL_API=3
					etcdctl put name john
					etcdctl get name
					etcdctl get / --prefix --keys-only




Backup, Restore ETCD


01 - ETCD Backup :-

controlplane ~ ✖ kubectl get pods -n kube-system
NAME                                   READY   STATUS    RESTARTS   AGE
coredns-69f9c977-drl6v                 1/1     Running   0          20m
coredns-69f9c977-z2sl2                 1/1     Running   0          20m
etcd-controlplane                      1/1     Running   0          20m
kube-apiserver-controlplane            1/1     Running   0          20m
kube-controller-manager-controlplane   1/1     Running   0          20m
kube-proxy-mn5jk                       1/1     Running   0          20m
kube-scheduler-controlplane            1/1     Running   0          20m

controlplane ~ ➜  

controlplane ~ ➜  kubectl describe pod etcd-controlplane -n kube-system | grep -i crt
      --cert-file=/etc/kubernetes/pki/etcd/server.crt
      --peer-cert-file=/etc/kubernetes/pki/etcd/peer.crt
      --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
      --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt

controlplane ~ ➜  

controlplane ~ ➜  kubectl describe pod etcd-controlplane -n kube-system | grep -i url
Annotations:          kubeadm.kubernetes.io/etcd.advertise-client-urls: https://192.36.109.6:2379
      --advertise-client-urls=https://192.36.109.6:2379
      --initial-advertise-peer-urls=https://192.36.109.6:2380
      --listen-client-urls=https://127.0.0.1:2379,https://192.36.109.6:2379
      --listen-metrics-urls=http://127.0.0.1:2381
      --listen-peer-urls=https://192.36.109.6:2380

controlplane ~ ➜  

controlplane ~ ➜  

controlplane ~ ➜  

controlplane ~ ➜  kubectl describe pod etcd-controlplane -n kube-system | grep -i key
      --key-file=/etc/kubernetes/pki/etcd/server.key
      --peer-key-file=/etc/kubernetes/pki/etcd/peer.key

controlplane ~ ➜  

controlplane ~ ➜  controlplane ~ ✖ ETCDCTL_API=3 etcdctl snapshot save /opt/snapshot-pre-boot.db --endpoints=https://127.0.0.1:2379 --cacert=/etc/k
ubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key
Snapshot saved at /opt/snapshot-pre-boot.db

controlplane ~ ➜  

controlplane ~ ➜  

controlplane ~ ➜  ls -lrth /opt/snapshot-pre-boot.db
-rw-r--r-- 1 root root 2.4M Feb 16 18:45 /opt/snapshot-pre-boot.db

controlplane ~ ➜  

controlplane ~ ➜  


02 - ETCD Cluster Restore 

Restore ETCD using pem files on external ETCD-Server :-
student-node ~ ➜  ssh etcd-server
Welcome to Ubuntu 18.04.6 LTS (GNU/Linux 5.4.0-1106-gcp x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Fri Feb 16 19:25:55 2024 from 192.36.3.12

etcd-server ~ ➜  

etcd-server ~ ➜  

etcd-server ~ ➜  ps -ef | grep -i etcd
etcd         810       1  0 17:54 ?        00:01:32 /usr/local/bin/etcd --name etcd-server --data-dir=/var/lib/etcd-data --cert-file=/etc/etcd/pki/etcd.pem --key-file=/etc/etcd/pki/etcd-key.pem --peer-cert-file=/etc/etcd/pki/etcd.pem --peer-key-file=/etc/etcd/pki/etcd-key.pem --trusted-ca-file=/etc/etcd/pki/ca.pem --peer-trusted-ca-file=/etc/etcd/pki/ca.pem --peer-client-cert-auth --client-cert-auth --initial-advertise-peer-urls https://192.36.3.6:2380 --listen-peer-urls https://192.36.3.6:2380 --advertise-client-urls https://192.36.3.6:2379 --listen-client-urls https://192.36.3.6:2379,https://127.0.0.1:2379 --initial-cluster-token etcd-cluster-1 --initial-cluster etcd-server=https://192.36.3.6:2380 --initial-cluster-state new
root        1820    1657  0 19:52 pts/1    00:00:00 grep -i etcd

etcd-server ~ ➜  

etcd-server ~ ➜  
etcd-server ~ ➜  ETCDCTL_API=3 etcdctl snapshot save snapshot.db --endpoints=https://127.0.0.1:2379 --cacert=/etc/etcd/pki/ca.pem --cert=/etc/etcd/pki/etcd.pem --key=/etc/etcd/pki/etcd-key.pem
{"level":"info","ts":1708113274.7239923,"caller":"snapshot/v3_snapshot.go:119","msg":"created temporary db file","path":"snapshot.db.part"}
{"level":"info","ts":"2024-02-16T19:54:34.730Z","caller":"clientv3/maintenance.go:200","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":1708113274.7310839,"caller":"snapshot/v3_snapshot.go:127","msg":"fetching snapshot","endpoint":"https://127.0.0.1:2379"}
{"level":"info","ts":"2024-02-16T19:54:34.746Z","caller":"clientv3/maintenance.go:208","msg":"completed snapshot read; closing"}
{"level":"info","ts":1708113274.7543912,"caller":"snapshot/v3_snapshot.go:142","msg":"fetched snapshot","endpoint":"https://127.0.0.1:2379","size":"2.1 MB","took":0.030286889}
{"level":"info","ts":1708113274.7545128,"caller":"snapshot/v3_snapshot.go:152","msg":"saved","path":"snapshot.db"}
Snapshot saved at snapshot.db

etcd-server ~ ➜  

etcd-server ~ ➜  

etcd-server ~ ➜  

etcd-server ~ ➜  ETCDCTL_API=3 etcdctl snapshot restore cluster2.db --data-dir=/var/lib/etcd-data-new --endpoints=https://127.0.0.1:2379 --cacert=/etc/etcd/pki/ca.pem --cert=/etc/etcd/pki/etcd.pem --key=/etc/etcd/pki/etcd-key.pem
{"level":"info","ts":1708113334.217906,"caller":"snapshot/v3_snapshot.go:296","msg":"restoring snapshot","path":"cluster2.db","wal-dir":"/var/lib/etcd-data-new/member/wal","data-dir":"/var/lib/etcd-data-new","snap-dir":"/var/lib/etcd-data-new/member/snap"}
{"level":"info","ts":1708113334.2328916,"caller":"mvcc/kvstore.go:388","msg":"restored last compact revision","meta-bucket-name":"meta","meta-bucket-name-key":"finishedCompactRev","restored-compact-revision":8316}
{"level":"info","ts":1708113334.239284,"caller":"membership/cluster.go:392","msg":"added member","cluster-id":"cdf818194e3a8c32","local-member-id":"0","added-peer-id":"8e9e05c52164694d","added-peer-peer-urls":["http://localhost:2380"]}
{"level":"info","ts":1708113334.2856927,"caller":"snapshot/v3_snapshot.go:309","msg":"restored snapshot","path":"cluster2.db","wal-dir":"/var/lib/etcd-data-new/member/wal","data-dir":"/var/lib/etcd-data-new","snap-dir":"/var/lib/etcd-data-new/member/snap"}

etcd-server ~ ➜  

etcd-server ~ ➜  

etcd-server ~ ➜  ls /var/lib/etcd*
/var/lib/etcd-data:
member

/var/lib/etcd-data-new:
member

etcd-server ~ ➜  

etcd-server ~ ➜  vi /etc/systemd/system/etcd.service

etcd-server ~ ➜  

etcd-server ~ ➜  chown -R etcd:etcd /var/lib/etcd-data-new

etcd-server ~ ➜  

etcd-server ~ ➜  

etcd-server ~ ➜  ls /var/lib/etcd-data-new
member

etcd-server ~ ➜  

etcd-server ~ ➜  

etcd-server ~ ➜  ls -lrth /var/lib/etcd-data-new
total 4.0K
drwx------ 4 etcd etcd 4.0K Feb 16 19:55 member

etcd-server ~ ➜  systemctl daemon-reload 

etcd-server ~ ➜  

etcd-server ~ ➜  etcd-server ~ ➜   systemctl restart etcd

etcd-server ~ ➜  

etcd-server ~ ➜  

etcd-server ~ ➜   systemctl status etcd
● etcd.service - etcd key-value store
   Loaded: loaded (/etc/systemd/system/etcd.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2024-02-16 19:57:25 UTC; 8s ago
     Docs: https://github.com/etcd-io/etcd
 Main PID: 2968 (etcd)
    Tasks: 37 (limit: 251379)
   CGroup: /system.slice/etcd.service
           └─2968 /usr/local/bin/etcd --name etcd-server --data-dir=/var/lib/etcd-data-new --cert-file=/etc/etcd/pki/etcd.pem --k
ey-file=/etc/etcd/pki/etcd-key.pem --peer-cert-file=/etc/etcd/pki/etcd.pem --peer-key-file=/etc/etcd/pki/etcd-key.pem --trusted-c
a-file=/etc/etcd/pki/ca.pem --peer-trusted-ca-file=/etc/etcd/pki/ca.pem --peer-client-cert-auth --client-cert-auth --initial-adve
rtise-peer-urls https://192.36.3.6:2380 --listen-peer-urls https://192.36.3.6:2380 --advertise-client-urls https://192.36.3.6:237
9 --listen-client-urls https://192.36.3.6:2379,https://127.0.0.1:2379 --initial-cluster-token etcd-cluster-1 --initial-cluster et
cd-server=https://192.36.3.6:2380 --initial-cluster-state new

Feb 16 19:57:25 etcd-server etcd[2968]: raft2024/02/16 19:57:25 INFO: 8e9e05c52164694d became leader at term 2
Feb 16 19:57:25 etcd-server etcd[2968]: raft2024/02/16 19:57:25 INFO: raft.node: 8e9e05c52164694d elected leader 8e9e05c52164694d
 at term 2
Feb 16 19:57:25 etcd-server etcd[2968]: setting up the initial cluster version to 3.4
Feb 16 19:57:25 etcd-server etcd[2968]: ready to serve client requests
Feb 16 19:57:25 etcd-server etcd[2968]: ready to serve client requests
Feb 16 19:57:25 etcd-server etcd[2968]: published {Name:etcd-server ClientURLs:[https://192.36.3.6:2379]} to cluster cdf818194e3a
8c32
Feb 16 19:57:25 etcd-server etcd[2968]: set the initial cluster version to 3.4
Feb 16 19:57:25 etcd-server etcd[2968]: enabled capabilities for version 3.4
Feb 16 19:57:25 etcd-server etcd[2968]: serving client requests on 192.36.3.6:2379
Feb 16 19:57:25 etcd-server etcd[2968]: serving client requests on 127.0.0.1:2379

etcd-server ~ ➜  

