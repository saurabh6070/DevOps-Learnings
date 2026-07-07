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
