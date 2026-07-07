Metrics Server & cAdvisor (Resource usage profiling)




001 -> Kuberenets don't come with built-in solution to monitor/analyse Pods/Nodes Resources or metrics.
For this we need Open-Source tools such as Metrics-Server, Prometheus, Elastic-Stack, Datadog, Dynatrace.

002 -> Metrics-Server is an in-memory metrics server i.e. It doesnt store any data on the disk. It doesnt provide historical data because of this reason.

003 -> To install metrics-server :-
Minikube :- minikube addons enable metrics-server
Others :- git clone https://github.com/kubernetes-incubator/metrics-server
Main :- git clone https://github.com/kodekloudhub/kubernetes-metrics-server.git
		cd kubernetes-metrics-server
		kubectl create -f .

004 -> There is compnent in kubelet which is known as C-Advisor(Contianer-Advisor) which gives container metrics information from kubelet to Metrics-Server. at real-time.

005 -> To monitor Node CPU/Memory Consumption :-
		kubectl top node
	   To monitor Pod CPU/Memory Consumption :-
		kubectl top pods

006 -> Logs after installng metrics-server in Step-3.
* kubectl top node
error: metrics not available yet
* kubectl top node
NAME           CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
controlplane   324m         0%     1146Mi          0%        
node01         263m         0%     295Mi           0%  
* kubectl top pods
NAME       CPU(cores)   MEMORY(bytes)   
elephant   15m          31Mi            
lion       1m           18Mi            
rabbit     112m         252Mi

