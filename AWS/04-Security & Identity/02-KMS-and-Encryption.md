# 🛡️ KMS and Encryption

## What is KMS?
AWS Key Management Service (KMS) is used to create, manage, and rotate encryption keys.

## Encryption Options
- Server-side encryption: AWS encrypts data at rest for you
- Client-side encryption: the application encrypts before sending data to AWS
- Envelope encryption: a data key is encrypted by a master key

## Common AWS Services Using KMS
- S3
- EBS
- RDS
- Redshift

## Key Management Concepts
- Customer Managed Keys (CMKs)
- AWS-managed keys
- Key policies and aliases
- Automatic key rotation

## Exam Notes
- Encryption protects data confidentiality and supports compliance requirements.
- KMS is often used for central key management across multiple AWS services.
