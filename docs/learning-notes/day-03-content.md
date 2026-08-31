# Day 03 — Kubernetes Configuration

## 1. ConfigMap

ConfigMap stores non-sensitive application configuration.

Examples:
- APP_ENV
- LOG_LEVEL
- APP_NAME
- Application URLs

Create:
```bash
kubectl apply -f configmap.yaml
Check:
kubectl get configmap -n task-platform
kubectl describe configmap <name> -n task-platform
Use ConfigMap as Environment Variables
envFrom:
  - configMapRef:
      name: backend-config
ConfigMap → Pod → Environment Variable
2. Secrets
Secrets are used for sensitive configuration such as:
Passwords
API keys
Tokens
Credentials
Example:
apiVersion: v1
kind: Secret
metadata:
  name: backend-secret
type: Opaque
stringData:
  API_KEY: "demo-api-key"
Use in Deployment:
envFrom:
  - secretRef:
      name: backend-secret
Kubernetes Secret values are base64-encoded by default, not automatically encrypted just because they are Secrets.
Never commit real credentials to GitHub.
3. ConfigMap/Secret Update Behavior
When ConfigMap or Secret is injected as an environment variable:
ConfigMap/Secret
      ↓
Pod starts
      ↓
Environment Variable
Changing the ConfigMap/Secret does NOT automatically update the environment variable inside an existing container.
Restart the Deployment:
kubectl rollout restart deployment/backend -n task-platform
Then the new Pod receives the updated value.
4. ConfigMap as Volume
ConfigMaps can also be mounted as files.
ConfigMap
   ↓
Volume
   ↓
Pod
Mounted ConfigMap files can be updated by Kubernetes, but the application must re-read/reload the file to use the new value.
5. Service ClusterIP
A Kubernetes Service provides stable networking for Pods.
Frontend
   ↓
Backend Service
   ↓
Backend Pods
Check Services:
kubectl get svc -n task-platform
A normal Service gets a stable ClusterIP.
Example:
backend-service → 10.x.x.x:5000
Pods may change IP addresses, but the Service provides a stable endpoint.
6. Service Discovery
Inside the cluster, applications can communicate using the Service name instead of Pod IP.
Example:
http://backend-service:5000
Kubernetes DNS resolves the Service name to its ClusterIP.
7. Headless Service
A Headless Service uses:
clusterIP: None
It does not provide a normal ClusterIP.
It is commonly used with StatefulSets to provide stable network identities.
StatefulSet
   ↓
Headless Service
   ↓
mongodb-0
mongodb-1
mongodb-2
8. Important Commands
kubectl get configmap -n task-platform
kubectl get secrets -n task-platform
kubectl get svc -n task-platform
kubectl describe svc <service> -n task-platform
kubectl get endpoints -n task-platform
kubectl get endpointslice -n task-platform
kubectl rollout restart deployment/backend -n task-platform
