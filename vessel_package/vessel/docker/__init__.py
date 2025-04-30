# Import key functions to make them available at the package level
from .generator import generate_dockerfile
from .setup import ensure_docker_available, is_docker_installed, is_docker_running

__all__ = ['generate_dockerfile', 'ensure_docker_available', 'is_docker_installed', 'is_docker_running']