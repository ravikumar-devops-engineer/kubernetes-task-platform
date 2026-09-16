# Kubernetes Task Platform

A hands-on Kubernetes project built using *Kind* to deploy and manage a multi-tier Task Platform application.

## Architecture

User → Ingress → Frontend → Backend → MongoDB → Persistent Storage

## Technologies

- Kubernetes
- Kind
- Docker
- YAML
- NGINX Ingress
- MongoDB

## Kubernetes Concepts

- Deployments & ReplicaSets
- Services
- ConfigMaps & Secrets
- Liveness & Readiness Probes
- Ingress
- PV / PVC / StorageClass
- StatefulSet
- Resource Requests & Limits
- Node Scheduling
- Taints & Tolerations
- HPA
- Rolling Updates & Rollbacks
- NetworkPolicy
- RBAC & ServiceAccount
- PodDisruptionBudget

## Troubleshooting

Practical scenarios covered:

- Pending Pods
- CrashLoopBackOff
- CPU/Memory issues
- Service connectivity
- Scheduling issues
- Storage/PVC issues
- Node maintenance

## Documentation

Hands-on learning notes are available in the docs/ directory.

## Future Improvements

- GitHub Actions CI/CD
- Prometheus & Grafana
- Centralized Logging
- Security Scanning
- Argo CD / GitOps
- TLS/HTTPS
- OpenShift Project

*Goal:* Build strong practical Kubernetes and DevOps skills through hands-on implementation and troubleshooting.