001 -> Taint is applied on a Node, while toleration is applied on Pod.
		If a taint is applied on a Node with specific key-value, then the pods which don't have toleration of the same key-value pairs, can never be scheduled on that Node.
				kubectl taint nodes node-name key=value:taint-effect
		Note :- taint-effect can have three values :- NoSchedule/PrefernoSchedule/NoExecute


001 -> kubectl taint node node01 spray=mortein:NoSchedule

002 -> kubectl run bee --image=nginx -o yaml > mypod.yaml (If use --dry-run=client, then no extra data will be present in yaml file)
	   vi mypod.yaml
	   
003 -> Some errors for taint in Pod.yaml file
kubectl apply -f mypod.yaml 
* The Pod "bee" is invalid: spec.tolerations[0].effect: Invalid value: "NoSchedule": effect must be 'NoExecute' when `tolerationSeconds` is set	   
* spec.tolerations[0].operator: Invalid value: core.Toleration{Key:"spray", Operator:"Exists", Value:"mortein", Effect:"NoSchedule", TolerationSeconds:(*int64)(0xc00ecf1088)}: value must be empty when `operator` is 'Exists'



001 -> Create yml file from command for Pod :-
		kubectl run bee --image=nginx --dry-run=client -o yaml
		kubectl run bee --image=nginx --dry-run=client -o yaml > bee.yml


002 -> To Remove Taint from Master Node :-
	Steps :-
			* kubectl describe node Node01
			* kubectl describe node Node01 | grep -i taint
				Output :-
								Taints :node-role.kubernetes.io/master:NoSchedule
			* kubectl taint node controlplane node-role.kubernetes.io/master:NoSchedule-
