import os
import click
from colorama import init, Fore, Style

# Import functions from other modules using updated package structure
from vessel.analyzer import analyze_react_project
from vessel.docker.generator import generate_dockerfile
from vessel.docker.setup import ensure_docker_available
from vessel.nginx.generator import generate_nginx_config

# Initialize colorama
init()

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Vessel - Production deployment made simple for React applications."""
    pass

@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--output", "-o", default="./vessel-output", help="Output directory for generated files")
def build(project_path, output):
    """Build Docker configuration for a React project."""
    # Convert to absolute path for clarity in output
    abs_path = os.path.abspath(project_path)
    
    click.echo(f"{Fore.BLUE}Starting Vessel build process for: {abs_path}{Style.RESET_ALL}")
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output):
        os.makedirs(output)
    
    # Step 1: Analyze the project
    click.echo(f"{Fore.YELLOW}Analyzing project structure...{Style.RESET_ALL}")
    project_info = analyze_react_project(abs_path)
    
    if not project_info:
        click.echo(f"{Fore.RED}Error: This doesn't appear to be a valid React project.{Style.RESET_ALL}")
        return
    
    # Step 2: Generate Dockerfile
    click.echo(f"{Fore.YELLOW}Generating Dockerfile...{Style.RESET_ALL}")
    dockerfile_path = os.path.join(output, "Dockerfile")
    generate_dockerfile(project_info, dockerfile_path)
    
    # Step 3: Generate Nginx configuration
    click.echo(f"{Fore.YELLOW}Generating Nginx configuration...{Style.RESET_ALL}")
    nginx_path = os.path.join(output, "nginx.conf")
    generate_nginx_config(project_info, nginx_path)
    
    # Output success message
    click.echo(f"{Fore.GREEN}Build complete! Files generated in {output}{Style.RESET_ALL}")
    click.echo(f"{Fore.GREEN}Your React project is ready for production deployment.{Style.RESET_ALL}")

@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--port", "-p", default=80, help="Port to expose the application on")
def deploy(project_path, port):
    """Deploy a React application to a production-ready Docker container."""
    abs_path = os.path.abspath(project_path)
    
    click.echo(f"{Fore.BLUE}Starting Vessel deployment for: {abs_path}{Style.RESET_ALL}")
    
    # Check if Docker is available and set it up if needed
    if not ensure_docker_available():
        click.echo(f"{Fore.RED}Docker setup failed. Cannot proceed with deployment.{Style.RESET_ALL}")
        return
    
    # More deployment steps would go here
    # For now, we'll just show that Docker is ready
    click.echo(f"{Fore.GREEN}Docker is ready for deployment.{Style.RESET_ALL}")
    click.echo(f"{Fore.YELLOW}(Actual deployment functionality coming soon){Style.RESET_ALL}")

if __name__ == "__main__":
    cli()