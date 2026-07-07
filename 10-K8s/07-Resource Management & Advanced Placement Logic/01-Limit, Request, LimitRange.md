002 -> CPU=1, means 1000m . Minimum value of CPU that can be assigned to Pod is 0.1 which is equivalent to 100m.
Memory=256 Mi is equivalent to 268435456 or equivalent to 268 M.


003 -> Memory Conversions :-
1G (Gigabyte) = 1,000,000,000 bytes
1M (Megabyte) = 1,000,000 bytes
1K (Kilobyte) = 1,000 bytes
1Gi (Gibibyte) = 1,073,741,824 bytes
1Mi (Mebibyte) = 1,048,576 bytes
1Ki (Kibibyte) = 1,024 bytes


004 -> Four Cases :-
		* No Request, No Limit :- In this case even one POD can consume all the resources of Node.
		* No Request, Limit Defined :- Request=Limit
		* Request Defined, limit Defined :- Resources will be limited to the POD even in th node resources are available.
		* Request Defined, No Limit :- Best Case. Limit is infinity, but if a new POD is scheduled to this Node, then it will be given resources definitely from the POD which is consuming the shole node resources.


005 -> LimitRange is an object which is applied at Namespace level. 
		default -> defaultLimit
		defaultRequest -> defaultRequest
		max -> maximumRequest
		min -> minimumRequest




007 -> We cannot edit specifications of an existing POD other than the below:-
spec.containers[*].image
spec.initContainers[*].image
spec.activeDeadlineSeconds
spec.tolerations
i. Run the kubectl edit pod <pod name> command.  This will open the pod specification in an editor (vi editor). Then edit the required properties. When you try to save it, you will be denied. This is because you are attempting to edit a field on the pod that is not editable.
A copy of the file with your changes is saved in a temporary location as shown above.
You can then delete the existing pod by running the command:
-->> kubectl delete pod webapp
Then create a new pod with your changes using the temporary file
-->> kubectl create -f /tmp/kubectl-edit-ccvrq.yaml
ii. The second option is to extract the pod definition in YAML format to a file using the command
-->> kubectl get pod webapp -o yaml > my-new-pod.yaml
Then make the changes to the exported file using an editor (vi editor). Save the changes
-->> vi my-new-pod.yaml
Then delete the existing pod
-->> kubectl delete pod webapp
Then create a new pod with the edited file
-->> kubectl create -f my-new-pod.yaml
Edit Deployments
With Deployments you can easily edit any field/property of the POD template. Since the pod template is a child of the deployment specification,  with every change the deployment will automatically delete and create a new pod with the new changes. So if you are asked to edit a property of a POD part of a deployment you may do that simply by running the command
-->> kubectl edit deployment my-deployment
