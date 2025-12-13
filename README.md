# Backend Hello World

A simple Python backend application that exposes a "Hello World" endpoint using FastAPI.

## Requirements

- Python 3.12
- Docker (for containerized deployment)
- Docker Hub account (for publishing)

## Project Structure

```
Backend_HelloWorld/
├── src/
│   ├── __init__.py
│   └── main.py          # Main FastAPI application
├── tests/
│   ├── __init__.py
│   └── test_main.py     # Unit tests
├── Dockerfile           # Docker configuration
├── .dockerignore       # Docker ignore file
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## API Endpoint

- **GET /** → Returns `{"message": "Hello World"}`

## Local Development Setup

### 1. Create and activate virtual environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the application

```powershell
python -m uvicorn src.main:app --host 0.0.0.0 --port 80
```

### 4. Test locally

```powershell
# Using curl
curl http://localhost

# Or visit in browser
# http://localhost
```

### 5. Run tests

```powershell
pytest tests/
```

## Docker Deployment

### 1. Build Docker image

```powershell
docker build -t backend_helloworld:latest .
```

### 2. Run container locally

```powershell
# Run on port 80
docker run -p 80:80 backend_helloworld:latest

# Or run on different port (e.g., 8080)
docker run -p 8080:80 backend_helloworld:latest
```

### 3. Test container

```powershell
# If running on port 80
curl http://localhost

# If running on port 8080
curl http://localhost:8080
```

### 4. Publish to Docker Hub

```powershell
# Login to Docker Hub
docker login

# Tag the image with your Docker Hub username
docker tag backend_helloworld:latest YOUR_USERNAME/backend_helloworld:latest

# Push to Docker Hub
docker push YOUR_USERNAME/backend_helloworld:latest
```

### 5. Pull and run from Docker Hub

```powershell
# Pull the image
docker pull YOUR_USERNAME/backend_helloworld:latest

# Run the container
docker run -p 80:80 YOUR_USERNAME/backend_helloworld:latest
```

## Docker Commands Quick Reference

```powershell
# List running containers
docker ps

# Stop a container
docker stop CONTAINER_ID

# Remove a container
docker rm CONTAINER_ID

# List images
docker images

# Remove an image
docker rmi backend_helloworld:latest

# View container logs
docker logs CONTAINER_ID
```

## Notes

- The application runs on port 80 inside the container
- Use `-p HOST_PORT:80` to map to a different host port
- Virtual environment (venv) is only for local development
- Docker is used for production deployment
- Always use the `latest` tag for the Docker image
