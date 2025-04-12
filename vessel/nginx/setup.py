import os
import subprocess
import logging
from colorama import Fore, Style

def is_nginx_installed():
    """Check if Nginx is installed and available."""
    try:
        subprocess.run(['nginx', '-v'], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def is_nginx_running():
    """Check if Nginx service is running."""
    try:
        # Different ways to check if nginx is running based on the system
        if os.path.exists('/usr/bin/systemctl'):
            # For systemd-based systems
            result = subprocess.run(['systemctl', 'is-active', 'nginx'], 
                                   capture_output=True, text=True, check=False)
            return result.stdout.strip() == 'active'
        else:
            # Alternative check using process existence
            result = subprocess.run(['pgrep', 'nginx'], 
                                  capture_output=True, check=False)
            return result.returncode == 0
    except subprocess.SubprocessError:
        return False

def setup_nginx_ubuntu():
    """Set up Nginx on Ubuntu/Debian based systems."""
    
    print(f"{Fore.YELLOW}Nginx not detected. Setting up Nginx...{Style.RESET_ALL}")
    
    try:
        # Update package index
        print("Updating package index...")
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        
        # Install Nginx
        print("Installing Nginx...")
        subprocess.run(['sudo', 'apt', 'install', '-y', 'nginx'], check=True)
        
        # Start Nginx service
        print("Starting Nginx service...")
        subprocess.run(['sudo', 'systemctl', 'start', 'nginx'], check=True)
        
        # Enable Nginx to start at boot
        print("Enabling Nginx to start at boot...")
        subprocess.run(['sudo', 'systemctl', 'enable', 'nginx'], check=True)
        
        # Verify the installation
        print("Verifying Nginx installation...")
        subprocess.run(['nginx', '-v'], check=True)
        
        print(f"{Fore.GREEN}Nginx has been successfully installed!{Style.RESET_ALL}")
        return True
        
    except subprocess.SubprocessError as e:
        print(f"{Fore.RED}Error setting up Nginx: {str(e)}{Style.RESET_ALL}")
        print("Please install Nginx manually by following the instructions at: https://nginx.org/en/docs/install.html")
        return False

def ensure_nginx_available():
    """
    Ensure Nginx is installed and running.
    Returns True if Nginx is available, False otherwise.
    """
    if not is_nginx_installed():
        # Detect system type and install accordingly
        if os.path.exists('/etc/debian_version'):
            return setup_nginx_ubuntu()
        else:
            print(f"{Fore.RED}Automated Nginx installation is only supported on Debian/Ubuntu systems.{Style.RESET_ALL}")
            print("Please install Nginx manually following instructions at: https://nginx.org/en/docs/install.html")
            return False
    
    if not is_nginx_running():
        print(f"{Fore.YELLOW}Nginx is installed but not running. Starting Nginx service...{Style.RESET_ALL}")
        try:
            if os.path.exists('/usr/bin/systemctl'):
                subprocess.run(['sudo', 'systemctl', 'start', 'nginx'], check=True)
            else:
                subprocess.run(['sudo', 'service', 'nginx', 'start'], check=True)
            print(f"{Fore.GREEN}Nginx service started successfully.{Style.RESET_ALL}")
            return True
        except subprocess.SubprocessError:
            print(f"{Fore.RED}Failed to start Nginx service. Please start it manually.{Style.RESET_ALL}")
            return False
    
    return True