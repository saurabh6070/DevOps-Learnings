K8s Scheduler Troubleshooting (Unscheduled pods, resource exhaustion evaluation)
K8s Scheduler Internals
Custom Scheduler Configurations






001 -> Scheduling a Pod manually on a node
		* In the Pod yml file manually we can write on which node, we want this pod to deploy.
		Under the spec section of Pod, write like -
				spec:
					nodeName: Node001
					containers:
					-	image: nginx
						name: nginx

002 -> If a scheduler not present in Namespace :- "kube-system", then the Pod status will be in "pending state", and in the pod describe, No node will be assigned to this pod. 
One method is given above to change in the yaml file in case of scheduler not working properly.
Another method is the curl command which can schedule the pod to a node, given that the node is in already in Pending state because of Scheduler not working properly.
	Curl Command :-
		curl --header "Content-Type:application/json" --request POST --data '{"apiVersion":"v1", "kind": "Binding", ....}' http://$SERVER/api/vi/namspaces/default/$PODNAME/binding/




001 -> Multiple schedulers can be created in Master using YAMl file. Take reference from this lecture to create Scheduler. In the Pod YAML file, give the name of the new scheduler instead of default-scheduler to schedule for testing.


002 -> kubectl get events -o wide

003 -> To view the scheduler logs, 
kubectl logs my-scheduler -n kube-system



003 -> If the issue is that POD is not being assigned any Node, then issue can be in the Scheduler. Since, it is a static POD, check the yml file of scheduler in /etc/kubernetes/manifests/
If the issue is that POD is not scaling to desired replica, then issue can be in the Controller-Manager. Since, it is a static POD, check the yml file of Controller-Manager in /etc/kubernetes/manifests/
