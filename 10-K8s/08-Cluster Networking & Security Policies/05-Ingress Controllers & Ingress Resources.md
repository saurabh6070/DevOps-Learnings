Ingress Controllers & Ingress Resources 🆕 (Layer 7 routing fundamentals)





11. 
001 -> Kubernetes Setup for a website having page1 (URL-1) and page2 (URL-2):-
		page1 will be served by Pod1, and when the traffic increases, same kind of Pod will increase automatically. To forward traffic to multiple containers, need to have one Load-Balancer-1 as well.
		page1 will be served by Pod2, and when the traffic increases, same kind of Pod will increase automatically. To forward traffic to multiple containers, need to have one Load-Balancer-2 as well.
		Also, need to implement security for https request only, i.e. need to implement SSL at any level.
		All of this becomes more complicated with the number of diffreent pages increases and also from the security point of view.
	Another method is to use Ingress which can balance load based on the type of traffic among multiple Pod and SSL can be implement on Ingress for security.
	
002 -> Ingress can be termed as Layer-7 Load-Balancer in Kubernetes.
		Even with Ingress, we still need to expose it to outside world using Service like NodePort or using CloudNative LB like AWS App LB.

003 -> Ingress can be understood to be deployed in two steps :-
		Step 1:- Ingress Controller
					Ingress is deployed as Supporter Solution (Reverse-Proxy or Load-Balancer solution) like Nginx, HA-Proxy, Traefic, Contour, Istio, etc.
					Ingress Controller is not deployed default. Need to create it manually.
		Step 2:- Resources
					Configuration involves defining route, configuring SSL certificates, etc. The set of rules are known as Ingress-Resources.
					Ingress resources are created using definition files similar like Pod creation, Service creation, etc.
					
004 -> Yaml-File for Ingress-Controller
						apiVersion: extensions/v1beta1
						kind: Deployment
						metadata:
							name: nginx-ingress-controller
						spec:
							replicas: 1
							selector:
								matchLabels:
									name: nginx-ingress
							template:
								metadata:
									labels:
										name: nginx-ingress
								spec:
									containers:
										- name: nginx-ingress-controller
										  image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.21.0
										  args: 
											- /nginx-ingress-controller																		######## Extra: This command is passed to start ingress service inside pod once pod comes up.
											- --configmap=$(POD_NAMESPACE)/nginx-configuration
										  env:
											- name: POD_NAME
											  valueFrom:
												fieldRef:
													fieldPath: metadata.name
											- name: POD_NAMESPACE
											  valueFrom:
												fieldRef:	
													fieldPath: metadata.namespace
										  ports:
											- name: http
											  containerPort: 80
											- name: https
											  containerPort: 443

005 -> Yaml file for Service to expose Ingress-Controller outside
						apiVersion: v1
						kind: Service
						metadata:
							name: nginx-service
						spec:
							type: NodePort
							ports:
								- port: 80
								  targetPort: 80
								  protocol: TCP
								  name: http
								- port: 443
								  targetPort: 443
								  protocol: TCP
								  name: https
							selector:
								name: nginx-ingress

006 -> Apart from Ingress-Controller, need to create following objects:
						* ConfigMap :- To configure many parametrrs like Error-Log-Path, Keep-Alive (Health-check of Pods to serve traffic), SSL.
										In order to decouple these data from Ingress-Controller, need to create ConfigMap to pass as an object for configuration.
						* ServiceAccount, Role, RoleBinding :- Ingress-Controller needs a ServiceAccount with right set of permissions to monitor pods status to send traffic nsed cluster and other related tasks.
						* Service  :- To expose service to outside.
						
007 -> Ingress-Resources are set of rules or confugrations that are applied on Ingress-Controller.

008 -> Yaml file for Ingress Resources based on URL(Path) :-
						apiVersion: extensions/v1beta1
						kind: Ingress
						metadata:
							name: ingress-wear-watch
						spec:
							rules:
								- http:
									paths:
									 - path: /wear
									   backend:
										serviceName: wear-service
										servicePort: 80
									 - path: /watch
									   backend:
										serviceName: watch-service
										servicePort: 80

009 -> Yaml file for Ingress-Resources based on Domain-Name :-
						apiVersion: extensions/v1beta1
						kind: Ingress
						metadata:
							name: ingress-wear
						spec:
							backend:
								serviceName: wear-service
								servicePort: 80

010 -> Yaml file for Ingress-Resource based on Domain-Names or Host-Names
						apiVersion: extensions/v1beta1
						kind: Ingress
						metadata:
							name: ingress-wear-watch
						spec:
							rules:
									- host: wear.my-online-store.com
									  http:
										paths:
											- backend:
												serviceName: wear-service
												servicePort: 80
									- host:
										paths:
											- backend:
												serviceName: watch-service
												servicePort: 80




************************************************************************************************************************************************************



Lecture-231 

001 -> For Ingress, following changes are there in newer versions of K8 :-
		i.  old_value -->> 						apiVersion: extensions/v1beta1
												kind: Ingress
												metadata:
													name: ingress-wear-watch
												spec:
													rules:
															- http:
																paths:
																- path: /wear
																  backend:
																		serviceName: wear-service
																		servicePort: 80
																- path: /watch
																  backend:
																		serviceName: watch-service
																		servicePort: 80
			new_value -->> 						apiVersion: networking.k8s.io/v1
												kind: Ingress
												metadata:
													name: ingress-wear-watch
												spec:
													rules:
															- http:
																paths:
																- path: /wear
																  pathType: Prefix
																  backend:
																		service: 
																			name: wear-service
																			port:
																				number: 80
																- path: /watch
																  pathType: Prefix
																  backend:
																		service: 
																			name: watch-service
																			port:
																				number: 80

002 -> Imperative method to create an Ingress Resource :-
						kubectl create ingress <ingress-name> -- rule="host/path=service:port"
						kubectl create ingress ingress-test -- rule="wear.my-online-store.com/wear*=wear-service:80"




************************************************************************************************************************************************************



Lecture-234 

001 -> kubectl get ingress -A
		In the output, for host if it is mentioned *, then All host can access the Service.
		The host entry defines the domain name that users use to reach the application. Here, * means user belong to any domain can access application using this ingress.

002 -> kubectl describe ingress ingress-wear-watch -n app-space
		If the match request is not match with any of the valid requests, then it goes to default-backend mentioned in the ingress resource.

003 -> If in the ingress resource, we want to change any path, then we can use command :-
		kubectl edit ingress ingress-wear-watch -n app-space
	Just after editing the ingress file, no need to delete any resource, service will automatically be redirected to new path.

004 -> To Deploy ingress, we need a service and deployment object which is mapped with the service (Pod of Deployment Object is connected with service)
				kubectl get deploy -n critical-space
					Name=webapp-pay
				kubectl get svc -n critical-space
					Name=pay-service
					Port=8282
					Type=ClusterIP
	To create ingress rule eith above details :-
			kubectl create ingress -h
			kubectl create ingress ingress-pay -n critical-space --rule="/pay=pay-service:8282"
			kubectl edit ingress ingress-apy -n critical-space
					Enter two lines below in the metadata section in the last:-
							annotations:
							nginx.ingress.kubernetes.io/rewrite-target: /




************************************************************************************************************************************************************



Lecture-236 

001 -> kubectl create namespace ingress-space
		kubectl create configmap nginx-configuration -n ingress-space
		kubectl create serviceaccount ingress-serviceaccount -n ingress-space
		kubectl get roles -n ingress-space
		kubectl get rolebindings -n ingress-space
		kubectl get deploy -n ingress-space (Output = ingress-controller)
		kubectl expose deploy ingress-controller -n ingress-space --name=ingress --port=80 --target-port=80 --type=NodePort
		kubectl get svc -n ingress-space (Output :- Port= 80:32741/TCP)
		kubectl edit svc ingress -n ingress-space (Change nodePort from 32741 to 30080)
		kubectl get svc -n app-space
		kubectl create ingress -n app-space ingress-wear-watch --rule="/wear=wear-service:8080" --rule="/watch:video-service:8080"
		kubectl edit ingress ingress-wear-watch 0n app-space
					Enter three lines below in the netadata section in the last:-
							annotations:
								nginx.ingress.kubernetes.io/rewrite-target: /
								nginx.ingress.kubernetes.io/ssl-rediret: "false"
