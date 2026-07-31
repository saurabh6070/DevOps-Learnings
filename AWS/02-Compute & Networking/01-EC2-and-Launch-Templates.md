# 🖥️ EC2 and Launch Templates

## What is EC2?
Amazon EC2 provides resizable virtual servers in the cloud. It is one of the most important AWS compute services.

## EC2 Basics
- Instance types are chosen based on CPU, memory, storage, and networking needs
- AMIs define the operating system and initial software package
- Security Groups act as virtual firewalls for EC2 instances
- Key Pairs are used for SSH access
- Elastic IPs provide static public IP addresses

## Storage Options
- Instance Store: temporary, ephemereal storage
- EBS: persistent block storage, suitable for databases and operating systems

## Launch Templates
Launch Templates are used to standardize the configuration of EC2 instances, including AMI, instance type, networking, and user data.

## Best Practices
- Use IAM roles instead of long-term access keys
- Attach EBS volumes for persistent storage
- Use Auto Scaling for resilience and availability

## Exam Notes
- EC2 is compute; S3 is object storage; EBS is block storage.
- Use the right instance family for the workload type.
