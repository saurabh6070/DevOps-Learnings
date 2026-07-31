# 🔐 IAM and Access Control

## What is IAM?
IAM is the service used to control who can access AWS resources and what actions they can perform.

## Core IAM Components
- Users: human identities
- Groups: collections of users
- Roles: temporary permissions for AWS services or users
- Policies: JSON documents that grant or deny permissions
- Identity Federation: allows external identities to access AWS

## IAM Best Practices
- Follow the principle of least privilege
- Use roles instead of long-lived access keys for applications
- Enable MFA for privileged accounts
- Rotate credentials regularly

## Important Concepts
- Permission boundaries limit maximum permissions
- Service-linked roles are created by AWS services
- Access Analyzer can help identify unintended access

## Exam Notes
- Roles are preferred over embedding credentials in applications.
- IAM controls access at the identity layer.
