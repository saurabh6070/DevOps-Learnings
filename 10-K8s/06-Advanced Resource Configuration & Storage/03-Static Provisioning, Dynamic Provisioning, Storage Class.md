001 -> Storage Class is used to provision volumes on any other platform. Some of the storage classes have their internal provisioners like portworx.
In case of Storage class, no need to create any volume on remote Cloud and even no need to create Persistent-Volume on Kubernetes.
Only, Storage-Class, Persistent-Volume Claim and Pod Definition needs to be applied.


002 -> Storage-Class Definition yaml file :-
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
	name: google-storage
provisioner: kubernetes.io/gce-pd


003 -> Yaml file for Persistent Volume Claim :-
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

