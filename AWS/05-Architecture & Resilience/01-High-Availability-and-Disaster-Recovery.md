# ♻️ High Availability and Disaster Recovery

## Core Concepts
- High Availability (HA): reduce downtime and keep services available
- Fault Tolerance: continue working even if a component fails
- Disaster Recovery (DR): recover from a major outage or regional failure
- RPO: how much data loss is acceptable
- RTO: how quickly recovery must happen

## AWS Resilience Patterns
- Multi-AZ deployment for databases and critical services
- Cross-region replication for backup and recovery readiness
- Load balancing across multiple instances
- Auto Scaling to handle traffic bursts

## DR Strategies
- Backup and Restore
- Pilot Light
- Warm Standby
- Multi-Site Active/Active

## Exam Notes
- Multi-AZ improves availability, not necessarily disaster recovery alone.
- Cross-region design is important for true DR planning.
