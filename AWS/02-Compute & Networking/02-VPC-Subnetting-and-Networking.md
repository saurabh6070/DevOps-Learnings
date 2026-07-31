# 🌐 VPC, Subnetting, and Networking

## What is a VPC?
A VPC is a private, isolated virtual network in AWS where you deploy your resources.

## Core Components
- VPC: the overall virtual network
- Subnets: segmentation inside the VPC
- Route Tables: control where network traffic goes
- Internet Gateway: allows public internet access
- NAT Gateway: allows private resources to reach the internet securely
- Security Groups: stateful firewall at the instance level
- Network ACLs: stateless firewall at the subnet level

## Public vs Private Subnets
- Public subnets have a route to an Internet Gateway
- Private subnets do not expose workloads directly to the internet

## Important Concepts
- CIDR blocks define the IP range of the network
- Default route 0.0.0.0/0 is used for internet-bound traffic
- VPC peering connects two VPCs privately
- Gateway endpoints and interface endpoints help reach AWS services without internet

## Best Practices
- Keep web servers in public subnets and databases in private subnets
- Use Network ACLs only when you need subnet-level control
- Monitor flow logs for troubleshooting and security analysis

## Exam Notes
- Security Groups are stateful; NACLs are stateless.
- NAT Gateway is used for outbound internet access from private subnets.
