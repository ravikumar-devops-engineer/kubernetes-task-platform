# kubernetes-task-platform
A Kubernetes task automation and platform management project.

To start the application port forward is needed for kind cluster.
kubectl port-forward -n ingress-nginx service/ingress-nginx-controller 8080:80


To check the taints for the nodes
$ kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints
NAME                         TAINTS
prod-cluster-control-plane   [map[effect:NoSchedule key:node-role.kubernetes.io/control-plane]]
prod-cluster-worker          <none>
prod-cluster-worker2         <none>
prod-cluster-worker3         [map[effect:NoSchedule key:workload value:database]]
prod-cluster-worker4         <none>

