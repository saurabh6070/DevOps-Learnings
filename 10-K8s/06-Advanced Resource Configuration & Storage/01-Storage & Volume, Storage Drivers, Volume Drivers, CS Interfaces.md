001 -> Two types of drivers :-
* Storage Driver
* Volume Driver

002 -> Docker Filesystem :-
		* /var/lib/docker/
				aufs
				containers
				image
				volumes

003 -> Docker store images in layered architecture
		When a new image is uploaded in docker, it searches for any existing image matching to any layer of this new image. Then it will only store those upper layers of new image which don't exist in the docker images already. This saves time, space, efficiency for uploading and using the images.

004 -> Image layer is read only.
		Container layer is read write both.

005 -> Create volume in docker (Volume mount) :- Mounting volume created in /var/lib/docker/volumes/ path to any container is called Volume Mount.
			docker volume create data_volume
	Command is going to create the directory with the same name in the directory /var/lib/docker/volumes/data_volume
			docker run -v data_volume:/var/lib/mysql mysql
	Command creates a new container with the image mysql and the docker volume provisioned in first step is going to be mounted on the path /var/lib/mysql of the container.
	First command is not needed as the second command will create volume automatically if run without first command.

006 -> Bind mount :- Mounting any path in Host apart from /var/lib/docker/volumes/ to any container is called Bind Mount.
			docker run -v /data/mysql:/var/lib/mysql mysql
	Command is used to create a container using image mysql and directory /var/lib/mysql which will mount to /data/mysql of host.
			docker run --mount type=bind,source=/data/mysql,target=/var/lib/mysql mysql
	New method to attach volume of container with the host directory.

007 -> Docker uses storage-driver for layered architecture of images management.
Storage driver in docker are :- AUFS, ZFS, BTRFS, Device Mapper, Overlay, Overlay2.
The selection of Storage driver is dependent on the underlying OS. i.e. for Ubuntu default Storage driver is AUFS. Docker will choose the best storage driver automatically based on the underlying OS.

************************************************************************************************************************************************************



Lecture-184

001 -> Example for Volume drivers are :- Local, Convoy, gce-docker, Portworx, Azure File Storage, NetApp, RexRay.


002 -> Command to mount volume from AWS EBS to container :-
docker run -it --name mysql --volume-driver rexray/ebs --mount src=ebs-vol,target=/var/lib/mysql mysql

003 -> NOTE :- By default, docker will choose best available Storage-Driver if nothing is mentioned. Need to specify explicitly if user wants volume to mount with Volume-Driver using --volume-driver tag.


************************************************************************************************************************************************************



Lecture-185

001 -> CRI(Container Runtime Interface) is developed to extend support of Kubernetes with different Container Runtime like Docker, CRI-O, Rocket(RKT).
CNI(Container Networking Interface) is developed to extend support of Kubernetes with different netwrok solutions like flannel, Cilium , Weaveworks.
CSI(Container Storage Interface) is developed to extend support of Kubernetes with different storages solutions like portworx, Amazon EBS, Dell EMC, GlusterFS.

002 -> Flow
Kubernetes (with CSI) communicates with Storage Driver using Remote Procedure Calls(RPCs) to perform following actions on Remote Storages :-
* Create Volume :- should provision a new volume on the storage
* Delete Volume :- should decommission a volume
* Controller Publish Volume :- should make the volume available on a node

