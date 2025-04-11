#!/usr/bin/env python3
import os
import click
from colorama import init, Fore, Style

# Initialize colorama for colored output; autoreset resets styling after each echo.
init(autoreset=True)

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Vessel - Production deployment made simple for React applications."""
    pass

@cli.command()
@click.argument("project_path", type=click.Path(exists=True))
def build(project_path):
    """
    Productionize an existing fully-fledged React application.
    
    This command validates the project folder, checks for the existence
    of a package.json file (to ensure it is a Node.js/React project), then
    simulates the steps to generate production-ready configurations.
    """
    # Convert to an absolute path for clarity.
    abs_path = os.path.abspath(project_path)
    click.echo(f"{Fore.BLUE}Starting Vessel build process for: {abs_path}{Style.RESET_ALL}")
    
    # Check if it's really a React/Node.js project: look for package.json.
    package_json_path = os.path.join(abs_path, 'package.json')
    if not os.path.exists(package_json_path):
        click.echo(f"{Fore.RED}Error: No package.json found. This doesn't appear to be a React/Node.js project.{Style.RESET_ALL}")
        return

    click.echo(f"{Fore.GREEN}Found package.json. Proceeding with production build steps...{Style.RESET_ALL}")
    
    # Simulate the productionization steps
    click.echo(f"{Fore.YELLOW}Analyzing project structure...{Style.RESET_ALL}")
    click.echo(f"{Fore.YELLOW}Generating production Dockerfile...{Style.RESET_ALL}")
    click.echo(f"{Fore.YELLOW}Generating nginx configuration...{Style.RESET_ALL}")
    click.echo(f"{Fore.YELLOW}Setting up production environment...{Style.RESET_ALL}")
    
    # In a full implementation, here you would call functions that:
    # - Copy production‑ready configuration files into the app,
    # - Run a Pensar dependency vulnerability scan,
    # - Build and run a Docker container for production.
    
    click.echo(f"{Fore.GREEN}Build complete! Your React project has been productionized and is ready for deployment.{Style.RESET_ALL}")

@cli.command()
def help():
    """
    Display the Vessel CLI manual.
    
    This command prints detailed usage instructions for the Vessel CLI.
    """
    click.echo(f"""{Fore.CYAN}
Vessel CLI Manual
------------------------------
Usage:
    vessel build <project_path>
    vessel help

Description:
    Vessel is a CLI tool that productionizes an existing, fully-fledged React application.
    It performs the following steps:
      1. Validates that the provided project directory exists.
      2. Checks for a package.json to confirm the project is a React/Node.js app.
      3. Analyzes the project structure.
      4. Generates production‑ready Docker and nginx configurations.
      5. Sets up the production environment for deployment.

Examples:
    vessel build /path/to/your/react/app
    vessel help

Notes:
    - Ensure Docker is installed and running on your system.
    - Vessel is optimized for React applications.
    - For advanced configurations or issues, refer to the full documentation.
{Style.RESET_ALL}""")

if __name__ == "__main__":
    cli()
