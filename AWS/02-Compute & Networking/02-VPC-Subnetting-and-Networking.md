# 🌐 VPC, Subnetting, and Networking

## 🧠 What is a VPC?
A Virtual Private Cloud (VPC) is an isolated private network inside AWS where you can launch your resources such as EC2 instances, RDS databases, load balancers, and private services. It gives you full control over your network environment inside the AWS cloud.

A VPC is important because it allows you to design a secure and structured network architecture without needing to maintain physical networking hardware.

---

## 🏗️ VPC Core Components

### 1. VPC
The VPC is the main network boundary for your AWS resources. It defines the overall IP address range for the network.

### 2. Subnets
A subnet is a segment of the VPC IP range. Subnets are used to divide the VPC into smaller network zones.

Common subnet types:
- Public subnet: has a route to an Internet Gateway
- Private subnet: does not have direct internet access

### 3. Route Tables
Route tables define how traffic flows from subnets to destinations such as the internet, other subnets, or VPN connections.

### 4. Internet Gateway (IGW)
An Internet Gateway allows resources in a public subnet to communicate with the internet.

### 5. NAT Gateway
A NAT Gateway allows instances in private subnets to access the internet for updates and outbound traffic without exposing them directly to the public internet.

### 6. Security Groups
Security Groups act as virtual firewalls for individual EC2 instances or other resources.
- They are stateful
- They control inbound and outbound traffic
- They work at the instance level

### 7. Network ACLs (NACLs)
Network ACLs are stateless firewalls that operate at the subnet level.
- They evaluate traffic before it enters or leaves a subnet
- They can allow or deny traffic using rules
- They are more basic than Security Groups but provide subnet-level control

---

## 🧩 Public vs Private Subnets

### 🌐 Public Subnet
A public subnet is used for resources that must be reachable from the internet, such as:
- web servers
- load balancers
- bastion hosts

These subnets usually have a route to an Internet Gateway.

### 🔒 Private Subnet
A private subnet is used for internal resources that should not be directly exposed to the internet, such as:
- application servers
- databases
- internal services

These resources often use NAT Gateway for outbound internet access.

---

## 🔢 CIDR and IP Planning
CIDR blocks define the IP address range of a VPC or subnet.

Examples:
- 10.0.0.0/16
- 172.31.0.0/16
- 192.168.1.0/24

### Important points
- The VPC CIDR must be large enough for future growth
- Subnets must not overlap with each other
- Careful IP planning avoids routing issues later

---

## 🗺️ VPC Networking Diagram
```text
Internet
   │
   ▼
 Internet Gateway
   │
   ▼
   VPC
 ┌───────────────┬───────────────┐
 │ Public Subnet │ Private Subnet│
 │ Web / ALB     │ App / DB      │
 └───────────────┴───────────────┘
        │                 │
        │                 └── NAT Gateway --> Internet
        └── Route Table --> Internet Gateway
```

This diagram shows the common pattern where public resources communicate with the internet while private resources stay internal and use NAT for outbound traffic.

---

## 🔁 Routing and Traffic Flow
Route tables determine where traffic is sent.

### Common routes
- local route: traffic within the VPC
- default route 0.0.0.0/0: traffic to the internet
- custom routes: traffic to peered VPCs, VPNs, or on-premises networks

### Example flow
1. A user sends a request to a web server in a public subnet.
2. The request passes through the Internet Gateway.
3. The web server responds.
4. An application server in a private subnet reaches the internet only through NAT Gateway.

---

## 🔐 Security in VPC
Security inside a VPC is managed using several layers.

### Security Groups
- attached to instances
- stateful
- allow or deny traffic based on rules

### Network ACLs
- attached to subnets
- stateless
- evaluated as a list of allow/deny rules

### Key difference
- Security Groups are instance-level protection
- NACLs provide subnet-level protection

A common design is:
- Security Groups for application-level traffic control
- NACLs for broader subnet-level filtering

---

## 🔗 VPC Connectivity Options
AWS offers different ways to connect VPCs and external networks.

### VPC Peering
Used to connect two VPCs privately.

### VPN Connection
Used to connect an on-premises network to AWS over a secure tunnel.

### AWS Direct Connect
Provides a dedicated network connection from on-premises to AWS.

### Gateway Endpoint / Interface Endpoint
Used to access AWS services privately without sending traffic over the public internet.

---

## ✅ Best Practices
- Place web-facing resources in public subnets
- Keep databases and internal services in private subnets
- Use NAT Gateway for private instances that need outbound internet access
- Restrict access with Security Groups and NACLs
- Use careful CIDR planning to avoid overlapping ranges
- Monitor flow logs for troubleshooting and security analysis

---

## 📝 Exam Notes
- A VPC is an isolated virtual network inside AWS.
- Public subnets have internet access; private subnets do not.
- Security Groups are stateful and instance-level.
- NACLs are stateless and subnet-level.
- NAT Gateway enables private subnets to reach the internet securely.
- CIDR planning is important for network design and future scalability.
