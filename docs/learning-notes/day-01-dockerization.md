# Day 01 — Application Development & Dockerization

## Objective

Build a simple frontend + backend application and containerize both applications using Docker.

## Application Architecture

```text
User / Browser
      |
      v
Frontend (Nginx)
      |
      | Reverse Proxy
      v
Backend (Flask)
      |
      v
REST APIs
Backend
Technology:
Python
Flask
Backend APIs:
GET /
GET /health
GET /api/tasks
The Flask application listens on:
0.0.0.0:5000
Using 0.0.0.0 is important inside a container because the application needs to accept connections from the container network.
Frontend
Technology:
HTML
JavaScript
Nginx
The frontend calls:
/api/tasks
instead of directly calling:
http://localhost:5000/api/tasks
This makes the application easier to deploy behind a reverse proxy and later in Kubernetes using Ingress.
Nginx Reverse Proxy
Nginx forwards backend requests to the Flask application.
Browser
   |
   | /api/tasks
   v
Nginx
   |
   | backend:5000
   v
Flask
Example Nginx configuration:
location /api/ {
    proxy_pass http://backend:5000;
}
Health endpoint:
location = /health {
    proxy_pass http://backend:5000/health;
}
Dockerfile
Example backend Dockerfile:
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
Dockerfile Concepts Learned
FROM
Defines the base image.
WORKDIR
Sets the working directory inside the container.
COPY
Copies files from the build context into the image.
RUN
Executes commands during image build time.
EXPOSE
Documents the port used by the application. It does not publish the port to the host.
CMD
Defines the default command executed when the container starts.
Docker Networking
A user-defined Docker network was created:
docker network create task-network
Both frontend and backend containers were attached to the same network.
The frontend can communicate with the backend using:
backend:5000
instead of:
localhost:5000
Important Concept
Inside a container:
localhost
refers to the current container itself.
It does not refer to another container.
Therefore:
localhost:5000    ❌
backend:5000      ✅
Troubleshooting
Problem
The frontend /api/tasks request was not working.
Cause
Nginx was receiving the request but did not have a reverse-proxy configuration to forward /api/tasks to the Flask backend.
Solution
Configured Nginx to forward:
/api/*
to:
backend:5000
API Testing
Test backend directly:
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/api/tasks
Test through Nginx:
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/backend
curl http://localhost:8080/api/tasks
Important Docker Commands
Build an image:
docker build -t task-platform-backend:1.0 .
Run a container:
docker run -d --name backend --network task-network task-platform-backend:1.0
List running containers:
docker ps
View container logs:
docker logs backend
Follow logs:
docker logs -f backend
Inspect a container:
docker inspect backend
List Docker networks:
docker network ls
Key Learnings
Application containerization
Dockerfile
Docker images
Docker containers
Docker image layers
Docker build cache
Docker networking
Container-to-container communication
Container DNS
Nginx reverse proxy
Backend health endpoint
Difference between localhost and a container/service name
Basic Docker troubleshooting
Day 01 Outcome
Successfully created and containerized a two-tier application consisting of:
Frontend
   |
   v
Nginx
   |
   v
Flask Backend
The application was tested through Docker networking and Nginx reverse proxying.