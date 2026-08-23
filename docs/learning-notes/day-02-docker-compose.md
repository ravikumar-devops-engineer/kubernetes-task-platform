# Day 02 — Docker Compose & Container Networking

## Objective

Replace manually created Docker containers and Docker networks with Docker Compose.

The goal was to understand:

- Docker Compose
- Multi-container applications
- Container networking
- Service discovery
- Docker DNS
- ports vs expose
- depends_on
- Healthchecks
- Container-to-container communication
- Troubleshooting

---

## Application Architecture

text
                    Docker Compose
                         |
                  Docker Network
                         |
          +--------------+--------------+
          |                             |
          v                             v
     Frontend                        Backend
       Nginx                          Flask
        :80                           :5000
          |
          v
     Host :8080
Docker Compose
Created:
docker-compose.yml
Docker Compose allows multiple related containers, networks, dependencies and configurations to be defined and managed from a single YAML file.
The application contains two services:
frontend
backend
Backend Service
The backend is built from:
application/backend/Dockerfile
It runs Flask on:
0.0.0.0:5000
The backend port is exposed internally:
expose:
  - "5000"
The backend is not directly published to the host.
Frontend Service
The frontend uses Nginx.
Nginx listens on:
80
The port is published to the host:
ports:
  - "8080:80"
This means:
Host :8080
    |
    v
Container :80
The application can therefore be accessed using:
http://localhost:8080
Docker Compose Service Discovery
The backend service is defined as:
backend:
Because of Docker Compose DNS/service discovery, the frontend can reach the backend using:
backend:5000
instead of:
localhost:5000
Important Concept
Inside the frontend container:
localhost
means the frontend container itself.
It does not refer to the backend container.
Therefore:
localhost:5000    ❌
backend:5000      ✅
ports vs expose
ports
Example:
ports:
  - "8080:80"
Publishes the container port to the host.
Host:8080
    |
    v
Container:80
expose
Example:
expose:
  - "5000"
Makes the port available for communication between containers without publishing it to the host.
Frontend
   |
   v
backend:5000
depends_on
Basic configuration:
depends_on:
  - backend
This controls the startup order of services.
However:
depends_on by itself does not guarantee that the application is ready.
A container can be running while the application inside it is still starting.
Healthcheck
A healthcheck was added to the backend:
healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"]
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 5s
The frontend waits for the backend to become healthy:
depends_on:
  backend:
    condition: service_healthy
Flow
Start Backend
     |
     v
Healthcheck
     |
     +---- Unhealthy
     |       |
     |       v
     |     Wait
     |
     +---- Healthy
             |
             v
        Start Frontend
This is better than relying only on startup order.
Container-to-Container Connectivity
Entered the frontend container:
docker exec -it task-frontend sh
Then tested:
wget -qO- http://backend:5000/health
If the response is:
{"status":"healthy"}
it confirms that:
Frontend container
       |
       v
Docker DNS
       |
       v
backend
       |
       v
Port 5000
       |
       v
Flask
is working correctly.
Application Testing
Frontend:
curl http://localhost:8080/
Health:
curl http://localhost:8080/health
Backend:
curl http://localhost:8080/backend
Tasks API:
curl http://localhost:8080/api/tasks
Important Docker Compose Commands
Start and build:
docker compose up --build
Start in background:
docker compose up -d --build
Check services:
docker compose ps
Stop and remove Compose resources:
docker compose down
View logs:
docker compose logs
View backend logs:
docker compose logs backend
Follow logs:
docker compose logs -f
Troubleshooting Approach
If the frontend cannot communicate with the backend:
Check whether both containers are running.
Check whether both services are on the same Docker network.
Verify the backend service name.
Test DNS resolution of backend.
Test connectivity to backend:5000.
Verify Flask is listening on 0.0.0.0.
Verify port 5000.
Check backend logs.
Check Nginx configuration.
Check Docker Compose configuration.
Check backend healthcheck status.
Useful commands:
docker compose ps
docker compose logs backend
docker network ls
docker inspect task-backend
docker inspect task-frontend
Key Learnings
Docker Compose
Multi-container application management
Docker networks
Container DNS
Service discovery
Container-to-container communication
ports
expose
depends_on
Healthchecks
Application readiness
Nginx reverse proxy
Docker troubleshooting
Difference between container startup and application readiness
Day 02 Outcome
Successfully converted the manually managed frontend and backend containers into a Docker Compose application.
The application can now be started using:
docker compose up -d --build
and the architecture is:
                    Docker Compose
                         |
                  Docker Network
                         |
          +--------------+--------------+
          |                             |
          v                             v
      Frontend                       Backend
       Nginx                          Flask
        :80                           :5000
          |
          v
     localhost:8080
The frontend communicates with the backend using Docker service discovery:
backend:5000
and the backend healthcheck ensures that the frontend does not depend only on container startup order.