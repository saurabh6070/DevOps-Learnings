PersistentVolume (PV) & PersistentVolumeClaim (PVC) Lifecycle 🆕 (Bound/Reclaim policies)



002 -> Yaml file for Persistent-Volume Claim :-
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: foo-pvc
  namespace: foo
spec:
  storageClassName: "" # Empty string must be explicitly set otherwise default StorageClass will be set
  volumeName: foo-pv
  


003 -> Yaml file for Persustent Volume :-
apiVersion: v1
kind: PersistentVolume
metadata:
  name: foo-pv
spec:
  storageClassName: ""
  claimRef:
    name: foo-pvc
    namespace: foo


004 -> Yaml file for Persistent Volume with Hostpath :-
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-log
spec:
  capacity:
   storage: 100Mi
  accessModes:
   - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  hostPath:
      path: /pv/log


005 -> Yaml file for Persistent Volume Claim :-
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: claim-log-1
spec:
  volumeName: pv-log
  resources:
    requests: 
      storage: 50Mi
  accessModes: 
  - ReadWriteMany
  
  

006 -> Yaml file for Persistent Volume with POD :-
apiVersion: v1
kind: Pod
metadata:
  name: hostpath-example-linux
spec:
  containers:
  - name: webapp
    image: kodekloud/event-simulator
    volumeMounts:
    - mountPath: /log
      name: myvol
      readOnly: true
  volumes:
  - name: myvol
	persistentVolumeClaim:
		claimName: claim-log-1



007 -> If a POD is attached to pvc, and we try to delete PVC, then the PVC will stuck in a Terminating state and the terminal is hanged.
In this case, deletethe pod as well. The the pvc will also be deleted after the pod is deleted.
Depending upon the reclaim-policy in pv, the pv will be in "Released" state, if the policy is defined as "Retain".

