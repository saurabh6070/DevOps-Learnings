# 🐳 ECS, EKS, and Lambda

## Amazon ECS
ECS is AWS’s fully managed container orchestration service for running Docker containers.

## Amazon EKS
EKS is AWS’s managed Kubernetes service for running Kubernetes-based applications.

## AWS Lambda
Lambda runs code in response to events without managing servers.

## When to Use What
- ECS: simpler container workloads in AWS
- EKS: teams already using Kubernetes
- Lambda: event-driven and short-lived workloads

## Common Patterns
- Fargate for serverless containers
- Lambda with API Gateway for APIs
- EKS for large-scale container platforms

## Exam Notes
- Lambda is serverless compute; ECS and EKS are container orchestration services.
- Choose based on operational model, portability, and workload shape.
