# Day 05 — HPA, Scheduling Troubleshooting & Rolling Updates

## 1. Horizontal Pod Autoscaler (HPA)

HPA automatically increases or decreases the number of Pod replicas based on resource utilization.

Example:

```yaml
minReplicas: 2
maxReplicas: 5

metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
Meaning:
Minimum replicas = 2
Maximum replicas = 5
CPU target       = 60%
Basic flow:
CPU usage increases
        ↓
HPA detects high utilization
        ↓
Increase replicas
        ↓
2 → 3 → 4 → 5
When load decreases:
CPU usage decreases
        ↓
HPA
        ↓
Decrease replicas
        ↓
5 → 4 → 3 → 2
Useful commands:
kubectl get hpa -n task-platform
kubectl describe hpa backend-hpa -n task-platform
kubectl top nodes
kubectl top pods -n task-platform
Important:
CPU-based HPA requires CPU resource requests to calculate utilization properly.
2. Scheduling Troubleshooting
When a Pod is stuck in Pending, don't immediately restart or delete it.
First check:
kubectl get pods -n task-platform
Then:
kubectl describe pod <pod-name> -n task-platform
Check the Events section.
Common scheduling problems:
Insufficient CPU/Memory
Insufficient cpu
The scheduler cannot find a node with enough available allocatable resources to satisfy the Pod's resource request.
Possible solutions:
Reduce resource requests if appropriate
Add another node
Increase node resources
Node Selector Mismatch
Example:
nodeSelector:
  workload: nonexistent
If no node has the required label:
Pod → Pending
Check:
kubectl get nodes --show-labels
Untolerated Taint
If a node has:
workload=database:NoSchedule
and the Pod doesn't have the matching toleration, the Pod cannot be scheduled there.
Check:
kubectl describe node <node-name>
Look for:
Taints:
Node Affinity Mismatch
If a Pod requires:
disk=ssd
but no suitable node has that label, the Pod remains Pending.
Check:
kubectl get nodes --show-labels
3. Scheduling Troubleshooting Flow
Pod Pending
    ↓
kubectl describe pod
    ↓
Check Events
    ↓
Identify scheduling reason
    ↓
Check resource requests
    ↓
Check node labels
    ↓
Check taints/tolerations
    ↓
Check node affinity
    ↓
Check topology constraints
    ↓
Fix the actual constraint
Important interview point:
Preemption cannot solve every Pending Pod. If the problem is a nodeSelector, affinity, taint, or other placement constraint, removing another Pod may not help.
4. Rolling Updates
Kubernetes Deployments normally use a RollingUpdate strategy.
Instead of deleting all old Pods at once, Kubernetes gradually replaces old Pods with new Pods.
Example:
Before:
v1 → v1

During:
v1 → v2
v1 → v1
v1 → v2

After:
v2 → v2
This helps achieve low/zero downtime during application updates.
5. RollingUpdate Configuration
Example:
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 0
    maxSurge: 1
maxUnavailable
Controls how many Pods can be unavailable during the update.
maxUnavailable: 0
Means Kubernetes should maintain all desired Pods as available during the rollout.
maxSurge
Controls how many additional Pods can temporarily be created above the desired replica count.
maxSurge: 1
Example with 2 replicas:
v1   v1

v1   v1   v2
          ↑
       extra Pod

v1   v2

v2   v2
6. Rolling Update Commands
Check rollout status:
kubectl rollout status deployment/backend -n task-platform
Check rollout history:
kubectl rollout history deployment/backend -n task-platform
Watch Pods:
kubectl get pods -n task-platform -l app=backend -w
7. Rollback
If a new deployment causes a problem, we can return to the previous revision.
Rollback:
kubectl rollout undo deployment/backend -n task-platform
Check status:
kubectl rollout status deployment/backend -n task-platform
Check history:
kubectl rollout history deployment/backend -n task-platform