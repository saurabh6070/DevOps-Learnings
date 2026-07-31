# ⚖️ Load Balancing and Auto Scaling

## Load Balancer Types
- Application Load Balancer (ALB): best for HTTP/HTTPS applications
- Network Load Balancer (NLB): best for TCP/UDP and high-performance workloads
- Classic Load Balancer: older option, mostly legacy use

## Key Concepts
- Target Groups define the backend instances or containers that receive traffic
- Health Checks monitor service health and remove unhealthy targets
- Path-based routing and host-based routing are common ALB features

## Auto Scaling Groups
Auto Scaling Groups help maintain the desired number of instances based on demand or health status.

## Scaling Policies
- Simple scaling
- Step scaling
- Target tracking scaling

## Exam Notes
- ALB works at Layer 7; NLB works at Layer 4.
- Auto Scaling improves availability and cost efficiency.
