# Vessel

Vessel is a command-line tool that simplifies deploying React applications to production environments. It automatically generates optimized Docker configurations and Nginx settings, creating production-ready deployments with a single command.

## Features

- One-command deployment of React applications
- Production-optimized Nginx configuration
- Docker-based containerization for consistency
- Automatic Docker installation in WSL environments
- Performance optimization with gzip compression and caching
- Security headers and best practices included by default

## Installation

```bash
# Create a virtual environment
python -m venv vessel-env

# Activate the virtual environment
# On Windows:
vessel-env\Scripts\activate
# On macOS/Linux:
source vessel-env/bin/activate

# Install
pip install -e .
```

## Usage

### Generate Docker Configuration

```bash
vessel build /path/to/react-project
```

This analyzes your React project and generates a Dockerfile and Nginx configuration in the `./vessel-output` directory.

### Deploy a React Application

```bash
vessel deploy /path/to/react-project
```

This builds and deploys your React application to a Docker container, making it available at http://localhost:80 by default.

For custom port:

```bash
vessel deploy /path/to/react-project --port 3000
```

### Manage Deployments

List all deployed applications:

```bash
vessel list
```

Stop a running application:

```bash
vessel stop [container-name]
```

## Why Vessel?

Deploying React applications to production environments typically requires specialized knowledge of Docker, Nginx configuration, performance optimization, and security best practices. Vessel bridges this gap by automating these technical details, letting you focus on building features rather than configuring deployment infrastructure.

## Note

This repository also includes a flask server for querying the Pensar API for vulnerability scans