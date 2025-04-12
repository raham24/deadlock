import os
import subprocess
import logging
import platform
from colorama import Fore, Style

    
def is_wsl2():
    """Check if running in Windows Subsystem for Linux 2."""
    try:
        # Use grep to check for "WSL2" in /proc/version
        result = subprocess.run(
            ['grep', '-q', 'WSL2', '/proc/version'], 
            capture_output=True, 
            check=False  # Don't raise exception on non-zero return code
        )
        # grep returns 0 (success) if the pattern is found
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def is_docker_installed():
    """Check if Docker is installed and available."""
    try:
        subprocess.run(['docker', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def is_docker_running():
    """Check if Docker daemon is running."""
    try:
        subprocess.run(['docker', 'info'], capture_output=True, check=True)
        return True
    except subprocess.SubprocessError:
        return False

def setup_docker_wsl():
    """Set up Docker in WSL environment."""
    
    print(f"{Fore.YELLOW}Docker not detected. Setting up Docker in WSL...{Style.RESET_ALL}")
    
    try:
        # Update package index
        print("Updating package index...")
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        
        # Install prerequisites
        print("Installing prerequisites...")
        subprocess.run([
            'sudo', 'apt', 'install', '-y', 
            'apt-transport-https', 'ca-certificates', 'curl', 
            'software-properties-common', 'gnupg'
        ], check=True)
        
        # Add Docker's official GPG key
        print("Adding Docker's GPG key...")
        result = subprocess.run(
            'curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg',
            shell=True, check=True
        )
        
        # Set up the stable Docker repository
        print("Setting up Docker repository...")
        result = subprocess.run(
            'echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null',
            shell=True, check=True
        )
        
        # Update the package index again
        print("Updating package index with Docker repository...")
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        
        # Install Docker CE
        print("Installing Docker CE...")
        subprocess.run([
            'sudo', 'apt', 'install', '-y', 
            'docker-ce', 'docker-ce-cli', 'containerd.io'
        ], check=True)
        
        # Start Docker service
        print("Starting Docker service...")
        subprocess.run(['sudo', 'service', 'docker', 'start'], check=True)
        
        # Verify the installation
        print("Verifying Docker installation...")
        subprocess.run(['docker', 'run', 'hello-world'], check=True)
        
        print(f"{Fore.GREEN}Docker has been successfully installed in WSL!{Style.RESET_ALL}")
        return True
        
    except subprocess.SubprocessError as e:
        print(f"{Fore.RED}Error setting up Docker: {str(e)}{Style.RESET_ALL}")
        print("Please install Docker manually following the instructions at: https://docs.docker.com/engine/install/ubuntu/")
        return False

def ensure_docker_available():
    """
    Ensure Docker is installed and running.
    Returns True if Docker is available, False otherwise.
    """
    # Check if running in WSL
    if not is_wsl2():
        if not is_docker_installed():
            print(f"{Fore.RED}Docker is not installed. Please install Docker to use Vessel.{Style.RESET_ALL}")
            print("Visit https://docs.docker.com/get-docker/ for installation instructions.")
            return False
        if not is_docker_running():
            print(f"{Fore.RED}Docker is installed but not running. Please start Docker daemon.{Style.RESET_ALL}")
            return False
        return True
    
    # If we're in WSL
    if not is_docker_installed():
        return setup_docker_wsl()
    
    if not is_docker_running():
        print(f"{Fore.YELLOW}Docker is installed but not running. Starting Docker service...{Style.RESET_ALL}")
        try:
            subprocess.run(['sudo', 'service', 'docker', 'start'], check=True)
            print(f"{Fore.GREEN}Docker service started successfully.{Style.RESET_ALL}")
            return True
        except subprocess.SubprocessError:
            print(f"{Fore.RED}Failed to start Docker service. Please start it manually.{Style.RESET_ALL}")
            return False
    
    return True