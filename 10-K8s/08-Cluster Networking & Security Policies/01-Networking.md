Networking (Core K8s networking principles, Pod-to-Pod, Pod-to-Service)




002 -> If a POD is connected with a database, then it should be connected using credential of DB (IP/Service-Name, Username, Password).
If the POD/Deploy is describe, then these credentials can be seen in ENV Variable section of a POD. The name of the variable of POD should map with the DB_service credentials. 
		ENV Variable Name in Pod						Service-Credentials
				DB_Host										Service-Name
				DB_User										Service-Username
				DB_Password									Service-AuthPassword

003 -> While troubleshoting make sure PODS atstus is 1/1 and all the sevices must have Endpoint mapped to the of desired PODs.
				
