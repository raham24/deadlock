# Import key functions to make them available at the package level
from .generator import generate_nginx_config

__all__ = ['generate_nginx_config']