Kubelet Troubleshooting (Systemd logs, container runtime socket connectivity issues)




001 -> If control-plane components deployed as a POD using kubeadm, check status of the PODs :-
			kubectl get pods -n kube-system
Check Logs :-
			kubectl logs kube-apiserver-master -n kube-system

002 -> If control-plane components deployed as a service, run commands on master node to check status :-
			service kube-apiserver status
			service kube-controller-manager status
			service kube-scheduler status
If control-plane components deployed as a service, run commands on worker node to check status :-
			service kubelet status
			service kube-proxy status
Check Logs :-
			sudo journalctl -u kube-apiserver
				
