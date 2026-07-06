Certificates (TLS bootstrapping, K8s CA, client certificates)





001 -> Certificate is used to ensure that the data being transferred is encrypted and the server is who it says it is.

002 -> Symmetric Encryption :-
Uses single key to encrypt and decrypt the data. Sender first encrypt the data using this key. Then, sends encrypted data along with this key to Reciever.
But in this case, sniffer can get this key and decrypt this data as well. So, Symmetric Encryption is not much secure, since it is sending key to Reciever over network.

003 -> Assymmetric Encryption :-
It uses two keys :- Public Key (can be treated as a Public Lock) and a Private Key.
It can be termed as safe encryption since two different keys are used to encrypt and decrypt data.
Two Possible Case :-
* Public key can be used to encrypt the data and Private key can be used to decrypt the data.
* Private key can be used to encrypt the data and Public key can be used to decrypt the data. But, here the concern is that Public-Key is shared publically. So, anyone can decrypt data which is encrypted using Private-Key.
Here, in brief, Any one key can be used to encrypt and other key can be used to decrypt the data. We cannot encryt and decrypt the data with the same key. And, it is preferred to encrypt data with Public-Key and encrypt with Private-Key.



004 -> Linux details for .ssh folder for secure access :-
* ssh-keygen (command to generate public and private key)
Here, Public-key is id_rsa.pub and Private-key is id_rsa
* All files in .ssh folder :-
id_rsa					-> Private-key of this user
id_rsa.pub 				-> Public key/ Public-lock of this user
authorized_keys			-> stores all the Public-Key / Public-Lock for this user
* To secure access to any linux machine, we generally lock the access from outside by all means. Just, we enable access through Public-Keys / Public-Lock.
* To grant any user access to this user, we can either give private key to the other user or we can take public key of the other user and store it in authorized_keys of this user. Then also, other user can access into this user securely.


005 -> To generate Private-Key :-
openssl genrsa -out my-bank.key 1024
Generally Private key naming is of the format :- *.key or *-key.pem
To generate Public-Key :-
openssl rsa -in my-bank.key -pubout > mybank.pem
Generally Public key naming is of the format :- *.crt or *.pem



006 -> Final Implementation :-
To send symmetric key, we use Asymmetric Encryption.
All further communication is done via Symmetric-Encryption.


007 -> To generate a CSR (Certificate Signing Request) :-
openssl req -new -key my-bank.key -out my-bank.csr -subj "/C=US/ST=CA/O=MyOrg, Inc./CN=mydomain.com"


008 -> Inside all browsers, Public keys of all Trusted Certificate Authority are present.
CA uses their Private Key to sign any certificate. If the Public key which is used to sign matches with its Public Key, then only the Website is validated.




001 -> Root Certificate configured on the Certificate-Authority servers.


001 -> Some tools for Certificate creation are :-
OpenSSL, CFSSL, EASYRSA.


002 -> Certificate Creation in K8 :-
* Public-Key, Certificates for CA
openssl genrsa -out ca.key 1024																										(Create Private Key)
openssl req -new -key ca.key -out ca.csr -subj "/CN=KUBERNETES-CA"                                                                  (Create CSR)
openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt                                                                            (Self Signed Certificate using own Private key generated in 1st step)
* Generating Admin (Client) Certificates :-
openssl genrsa -out admin.key 2048
openssl req -new -key admin.key -out admin.csr -subj "/CN=kube-admin"
openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -out admin.crt          													(Certificate signed by CA using ca.crt and ca.key)

Same goes for all the component in Kubernetes.



001 -> To open any certificate in text-format :-
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout
This command will open the certificate in text format and it includes all DNS names of this server, Issuer and Validity of this Certificate.


002 -> To view system logs of any service :-
journalctl -u etcd.service -l


003 -> Incase kubcetl commands not working, then we can check the logs using docker logs command or using crictl ps -a/crictl logs containerID.

