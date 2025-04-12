import os
import click
import subprocess
from colorama import init, Fore, Style
import shutil

# Import functions from other modules
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
    click.echo(f"\nTo deploy your project, run: {Fore.CYAN}vessel deploy {project_path}{Style.RESET_ALL}")

@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--port", "-p", default=80, help="Port to expose the application on")
@click.option("--name", "-n", default="", help="Name for the Docker container")
def deploy(project_path, port, name):
    """Deploy a React application to a production-ready Docker container."""
    abs_path = os.path.abspath(project_path)
    
    click.echo(f"{Fore.BLUE}Starting Vessel deployment for: {abs_path}{Style.RESET_ALL}")
    
    # Check if Docker is available and set it up if needed
    click.echo(f"{Fore.YELLOW}Checking Docker availability...{Style.RESET_ALL}")
    if not ensure_docker_available():
        click.echo(f"{Fore.RED}Docker setup failed. Cannot proceed with deployment.{Style.RESET_ALL}")
        return
    
    # Analyze the project to get info
    project_info = analyze_react_project(abs_path)
    if not project_info:
        click.echo(f"{Fore.RED}Error: This doesn't appear to be a valid React project.{Style.RESET_ALL}")
        return
    
    # Set container name if not provided
    if not name:
        name = project_info.get('name', 'react-app').lower().replace(' ', '-')
    
    # Create a temporary directory for Docker files
    temp_dir = os.path.join(abs_path, 'vessel-tmp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # Generate Docker files
    try:
        # Generate Dockerfile
        dockerfile_path = os.path.join(temp_dir, "Dockerfile")
        generate_dockerfile(project_info, dockerfile_path)
        
        # Generate Nginx config
        nginx_path = os.path.join(temp_dir, "nginx.conf")
        generate_nginx_config(project_info, nginx_path)
        
        # Copy files to project directory for building
        click.echo(f"{Fore.YELLOW}Preparing deployment files...{Style.RESET_ALL}")
        shutil.copy2(dockerfile_path, os.path.join(abs_path, "Dockerfile"))
        shutil.copy2(nginx_path, os.path.join(abs_path, "nginx.conf"))
        
        # Build Docker image
        click.echo(f"{Fore.YELLOW}Building Docker image...{Style.RESET_ALL}")
        subprocess.run(
            ['docker', 'build', '-t', f"{name}-image", abs_path],
            check=True
        )
        
        # Check if a container with the same name already exists
        result = subprocess.run(
            ['docker', 'ps', '-a', '--filter', f"name={name}", '--format', '{{.Names}}'],
            capture_output=True,
            text=True
        )
        
        if name in result.stdout:
            click.echo(f"{Fore.YELLOW}Container '{name}' already exists. Removing it...{Style.RESET_ALL}")
            subprocess.run(['docker', 'rm', '-f', name], check=True)
        
        # Run the container
        click.echo(f"{Fore.YELLOW}Starting container on port {port}...{Style.RESET_ALL}")
        subprocess.run(
            ['docker', 'run', '-d', '--name', name, '-p', f"{port}:80", 
             '--restart', 'unless-stopped', f"{name}-image"],
            check=True
        )
        
        click.echo(f"{Fore.GREEN}Deployment successful!{Style.RESET_ALL}")
        click.echo(f"{Fore.GREEN}Your React app is now running at: {Fore.CYAN}http://localhost:{port}{Style.RESET_ALL}")
        
    except subprocess.SubprocessError as e:
        click.echo(f"{Fore.RED}Deployment failed: {str(e)}{Style.RESET_ALL}")
    finally:
        # Clean up temporary files
        try:
            if os.path.exists(os.path.join(abs_path, "Dockerfile")):
                os.remove(os.path.join(abs_path, "Dockerfile"))
            if os.path.exists(os.path.join(abs_path, "nginx.conf")):
                os.remove(os.path.join(abs_path, "nginx.conf"))
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        except Exception as e:
            click.echo(f"{Fore.YELLOW}Warning: Could not clean up temporary files: {str(e)}{Style.RESET_ALL}")

@cli.command()
@click.argument("name", required=False)
def stop(name):
    """Stop a running Vessel container."""
    # Check if Docker is available
    if not ensure_docker_available():
        click.echo(f"{Fore.RED}Docker is not available. Cannot stop containers.{Style.RESET_ALL}")
        return
    
    if not name:
        # List running Vessel containers and let the user choose
        click.echo(f"{Fore.YELLOW}Listing running Vessel containers...{Style.RESET_ALL}")
        result = subprocess.run(
            ['docker', 'ps', '--format', '{{.Names}}'],
            capture_output=True,
            text=True
        )
        
        containers = result.stdout.strip().split('\n')
        if not containers or containers[0] == '':
            click.echo(f"{Fore.YELLOW}No running containers found.{Style.RESET_ALL}")
            return
        
        click.echo(f"{Fore.CYAN}Running containers:{Style.RESET_ALL}")
        for i, container in enumerate(containers, 1):
            click.echo(f"{i}. {container}")
        
        choice = click.prompt("Enter the number of the container to stop (or 'q' to quit)", type=str)
        if choice.lower() == 'q':
            return
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(containers):
                name = containers[index]
            else:
                click.echo(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")
                return
        except ValueError:
            click.echo(f"{Fore.RED}Invalid input.{Style.RESET_ALL}")
            return
    
    # Stop the selected container
    try:
        click.echo(f"{Fore.YELLOW}Stopping container {name}...{Style.RESET_ALL}")
        subprocess.run(['docker', 'stop', name], check=True)
        click.echo(f"{Fore.GREEN}Container {name} stopped successfully.{Style.RESET_ALL}")
    except subprocess.SubprocessError as e:
        click.echo(f"{Fore.RED}Failed to stop container: {str(e)}{Style.RESET_ALL}")

@cli.command()
def list():
    """List all Vessel-deployed applications."""
    # Check if Docker is available
    if not ensure_docker_available():
        click.echo(f"{Fore.RED}Docker is not available. Cannot list containers.{Style.RESET_ALL}")
        return
    
    # Get all containers
    try:
        result = subprocess.run(
            ['docker', 'ps', '-a', '--format', '{{.Names}}\t{{.Status}}\t{{.Ports}}'],
            capture_output=True,
            text=True,
            check=True
        )
        
        containers = result.stdout.strip().split('\n')
        if not containers or containers[0] == '':
            click.echo(f"{Fore.YELLOW}No containers found.{Style.RESET_ALL}")
            return
        
        click.echo(f"{Fore.CYAN}{'Container Name':<20} {'Status':<30} {'Ports':<30}{Style.RESET_ALL}")
        click.echo("-" * 80)
        
        for container in containers:
            if container:
                parts = container.split('\t')
                if len(parts) >= 3:
                    name, status, ports = parts[0], parts[1], parts[2]
                    status_color = Fore.GREEN if "Up" in status else Fore.RED
                    click.echo(f"{name:<20} {status_color}{status:<30}{Style.RESET_ALL} {ports:<30}")
                
    except subprocess.SubprocessError as e:
        click.echo(f"{Fore.RED}Failed to list containers: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    cli()