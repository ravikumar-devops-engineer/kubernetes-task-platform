# Kubernetes Task Platform

## Goal
Replace manually created Docker containers and Docker networks with **Docker Compose**.

### Key Concepts Learned
- Docker Compose
- Multi-container applications
- Container networking
- Service discovery
- Docker DNS
- Ports vs Expose
- `depends_on`
- Healthchecks
- Container-to-container communication
- Troubleshooting
- Application Architecture

---

## Application Architecture

Docker Compose | Docker Network
+--------------+--------------+
|              |
v              v
Frontend       Backend
Nginx          Flask
:80            :5000
v
Host :8080


### Docker Compose Setup
- **File:** `docker-compose.yml`
- Defines multiple services, networks, dependencies, and configurations.

---

## Services

### Backend Service
- Built from: `application/backend/Dockerfile`
- Runs Flask on: `0.0.0.0:5000`
- Exposed internally:
  ```yaml
  expose:
    - "5000"


Not published to host.

Frontend Service
Uses Nginx

Listens on port 80

Published to host:

ports:
  - "8080:80"

Access via: http://localhost:8080

Service Discovery
Backend defined as:

yaml
backend:
Frontend reaches backend using:

Code
backend:5000
Important: Inside frontend container, localhost refers to itself, not backend.

Ports vs Expose
Ports
yaml
ports:
  - "8080:80"
Publishes container port to host.
Host:8080 → Container:80

Expose
yaml
expose:
  - "5000"
Makes port available for inter-container communication (not published to host).

depends_on
yaml
depends_on:
  - backend
Controls startup order.
⚠️ Does not guarantee app readiness.

Healthcheck
Backend healthcheck:

yaml
healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"]
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 5s
Frontend waits for backend:

yaml
depends_on:
  backend:
    condition: service_healthy
Connectivity Test
Inside frontend container:

bash
docker exec -it task-frontend sh
wget -qO- http://backend:5000/health
Response:

json
{"status":"healthy"}
Application Testing
Frontend:

bash
curl http://localhost:8080/
curl http://localhost:8080/health
Backend:

bash
curl http://localhost:8080/backend
curl http://localhost:8080/api/tasks
Docker Compose Commands
Start & build:

bash
docker compose up --build
Start in background:

bash
docker compose up -d --build
Check services:

bash
docker compose ps
Stop & remove:

bash
docker compose down
Logs:

bash
docker compose logs
docker compose logs backend
docker compose logs -f
Troubleshooting Checklist
Are both containers running?

Are both services on the same network?

Verify backend service name.

Test DNS resolution (backend).

Test connectivity to backend:5000.

Ensure Flask listens on 0.0.0.0.

Check backend logs.

Check Nginx config.

Check Docker Compose config.

Check backend healthcheck status.

Useful commands:

bash
docker compose ps
docker compose logs backend
docker network ls
docker inspect task-backend
docker inspect task-frontend
Key Learnings
Docker Compose

Multi-container management

Docker networks & DNS

Service discovery

Container-to-container communication

Ports vs Expose

depends_on vs Healthchecks

Application readiness

Nginx reverse proxy

Docker troubleshooting

Difference between container startup vs app readiness

Outcome (Day 02)
Successfully converted manually managed containers into a Docker Compose application.
Start with:

bash
docker compose up -d --build
Architecture:

Code
Docker Compose | Docker Network
+--------------+--------------+
|              |
v              v
Frontend       Backend
Nginx          Flask
:80            :5000
   v
localhost:8080
Frontend communicates with backend using:

Code
backend:5000
Backend healthcheck ensures frontend waits until backend is ready.