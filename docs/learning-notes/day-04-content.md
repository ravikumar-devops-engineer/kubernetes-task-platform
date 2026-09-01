# Day 04 — Kubernetes Storage, StatefulSets & Scheduling

## 1. Persistent Volume (PV)

A PersistentVolume is storage available to the Kubernetes cluster.

```text
Pod → PVC → PV → Storage
PV exists independently of a Pod.
2. Persistent Volume Claim (PVC)
PVC is a request for storage made by an application.
Example:
resources:
  requests:
    storage: 1Gi
Check:
kubectl get pvc -n task-platform
kubectl get pv
Important:
Pod can be deleted while PVC remains.
A new Pod can mount the same PVC.
Storage behavior depends on the StorageClass and reclaim policy.
3. StorageClass
StorageClass defines how Kubernetes dynamically provisions storage.
Check:
kubectl get storageclass
Example:
standard
In Kind, the default StorageClass commonly uses:
rancher.io/local-path
4. StatefulSet
StatefulSet is used for stateful applications that require:
Stable Pod identity
Stable network identity
Persistent storage
Ordered Pod creation/deletion
Example:
mongodb-0
mongodb-1
mongodb-2
Unlike Deployment Pods, StatefulSet Pods have stable names.
Deployment:
backend-7d8f9
backend-5c9ab
StatefulSet:
mongodb-0
mongodb-1
mongodb-2
5. volumeClaimTemplates
volumeClaimTemplates automatically creates a PVC for each StatefulSet Pod.
Example:
volumeClaimTemplates:
  - metadata:
      name: mongodb-data
    spec:
      accessModes:
        - ReadWriteOnce
      storageClassName: standard
      resources:
        requests:
          storage: 1Gi
With 3 replicas:
mongodb-0 → mongodb-data-mongodb-0
mongodb-1 → mongodb-data-mongodb-1
mongodb-2 → mongodb-data-mongodb-2
Each Pod gets its own storage.
6. StatefulSet + Headless Service
A StatefulSet commonly works with a Headless Service:
clusterIP: None
This provides stable network identity for StatefulSet Pods.
Conceptually:
mongodb-0.mongodb
mongodb-1.mongodb
mongodb-2.mongodb
Kubernetes Scheduling
7. Kubernetes Scheduler
The kube-scheduler decides which node should run a Pod.
Basic flow:
Pod created
    ↓
Scheduler
    ↓
Find suitable nodes
    ↓
Filter
    ↓
Score
    ↓
Select node
8. CPU & Memory Requests
Requests tell Kubernetes how much resource the Pod requires for scheduling.
Example:
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
CPU:
1000m = 1 CPU
500m  = 0.5 CPU
100m  = 0.1 CPU
The scheduler primarily uses resource requests when deciding whether a node can accommodate a Pod.
9. CPU & Memory Limits
Limits define the maximum resources a container is allowed to use.
Example:
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"

  limits:
    cpu: "500m"
    memory: "256Mi"
Simple understanding:
Request → used for scheduling
Limit   → maximum resource usage
10. Pending Pod Troubleshooting
If a Pod is stuck in:
Pending
first check:
kubectl describe pod <pod-name> -n task-platform
Look at:
Events:
Example:
Insufficient cpu
This means the scheduler cannot find a suitable node with enough allocatable CPU to satisfy the Pod's request.
Possible solutions:
Reduce resource request if appropriate
Add more nodes
Increase node resources
Check scheduling constraints
11. Node Labels
Labels can be assigned to nodes.
Example:
kubectl label node prod-cluster-worker2 workload=backend
Check:
kubectl get nodes --show-labels
Labels can be used to control Pod placement.
12. nodeSelector
nodeSelector is a simple way to schedule a Pod only on nodes with a specific label.
Example:
nodeSelector:
  workload: backend
Flow:
Pod
 ↓
nodeSelector
 ↓
workload=backend
 ↓
Matching node
If no node has the required label:
Pod → Pending
13. Taints & Tolerations
Taints are applied to nodes to prevent normal Pods from being scheduled there.
Example:
kubectl taint nodes prod-cluster-worker3 workload=database:NoSchedule
Now Pods without the matching toleration cannot be scheduled there.
Toleration
A Pod can tolerate a matching taint:
tolerations:
  - key: workload
    operator: Equal
    value: database
    effect: NoSchedule
Important:
A toleration allows a Pod to run on a tainted node. It does NOT force the Pod to run there.
Taint Effects
NoSchedule
New Pods without a matching toleration are not scheduled.
PreferNoSchedule
Scheduler tries to avoid the node but it is a soft preference.
NoExecute
Prevents new Pods and can evict existing Pods that don't tolerate the taint.
14. nodeSelector vs Taints/Tolerations
nodeSelector
Answers:
Where can my Pod run?
Example:
nodeSelector:
  workload: backend
Taint
Answers:
Which Pods should NOT run on this node?
Toleration
Answers:
Which Pods are allowed to tolerate this node's taint?
For dedicated nodes, they can be combined:
Node:
  label → workload=database
  taint → workload=database:NoSchedule

Database Pod:
  nodeSelector → workload=database
  toleration → workload=database
15. Node Affinity
Node affinity is a more flexible alternative to nodeSelector.
Example:
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
            - key: disk
              operator: In
              values:
                - ssd
This requires the Pod to run on a node with:
disk=ssd
Required vs Preferred
requiredDuringSchedulingIgnoredDuringExecution
Hard requirement.
Must match
   ↓
Otherwise Pod remains Pending
preferredDuringSchedulingIgnoredDuringExecution
Soft preference.
Prefer matching node
        ↓
If unavailable
        ↓
Another suitable node can be selected
Remember:
required  = MUST
preferred = SHOULD
16. Pod Anti-Affinity
Pod anti-affinity controls Pod placement based on other Pods.
It is useful for High Availability.
Example:
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
            - key: app
              operator: In
              values:
                - frontend
        topologyKey: kubernetes.io/hostname
This can prevent multiple replicas from being placed on the same node.
Without anti-affinity:
worker1
 ├── frontend-1
 ├── frontend-2
 └── frontend-3
With anti-affinity:
worker1 → frontend-1
worker2 → frontend-2
worker3 → frontend-3
This improves availability if a node fails.
17. Node Affinity vs Pod Anti-Affinity
Node Affinity
Based on node labels.
Pod → Node label
Example:
Run on SSD nodes
Pod Anti-Affinity
Based on other Pods.
Pod → Other Pods
Example:
Don't place frontend replicas on the same node.
Important Commands
kubectl get pv
kubectl get pvc -n task-platform
kubectl get storageclass

kubectl get statefulset -n task-platform
kubectl get pods -o wide -n task-platform

kubectl get nodes
kubectl get nodes --show-labels

kubectl describe pod <pod> -n task-platform
kubectl describe node <node>

kubectl taint nodes <node> key=value:NoSchedule
kubectl taint nodes <node> key=value:NoSchedule-