# 🗄️ S3 and Storage Classes

## What is S3?
Amazon S3 is AWS’s object storage service used for storing files, backups, logs, media, and static web content.

## Key Concepts
- Bucket: top-level container for objects
- Object: file plus metadata
- Versioning: keeps multiple versions of an object
- Lifecycle Rules: move or expire objects automatically
- Encryption: server-side and client-side options available

## Common Storage Classes
- Standard: general-purpose, frequently accessed data
- Intelligent-Tiering: automatically moves data between access tiers
- Standard-IA: infrequent access, lower cost
- One Zone-IA: lower cost, single AZ durability
- Glacier: archival storage with long retrieval times

## S3 Use Cases
- Static website hosting
- Backup and disaster recovery
- Media storage
- Data lakes and analytics workloads

## Exam Notes
- S3 is designed for durability and high availability.
- Use lifecycle policies to reduce storage cost over time.
