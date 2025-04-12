# test_vessel.py

import os
import shutil
import sys
from colorama import Fore, Style

# Add the project directory to the path
sys.path.insert(0, os.path.abspath('.'))

# Import functions to test
from vessel.analyzer import analyze_react_project
from vessel.docker.generator import generate_dockerfile
from vessel.nginx.generator import generate_nginx_config

def test_analyzer(test_path):
    """Test the analyzer functionality."""
    print(f"Testing analyzer with path: {test_path}")
    project_info = analyze_react_project(test_path)
    
    if project_info:
        print(f"{Fore.GREEN}✓ Analyzer detected a React project{Style.RESET_ALL}")
        print(f"  Project name: {project_info.get('name', 'Unknown')}")
        print(f"  Build command: {project_info.get('build_command', 'Unknown')}")
        print(f"  Build output: {project_info.get('build_output', 'Unknown')}")
        return project_info
    else:
        print(f"{Fore.RED}✗ Analyzer did not detect a React project{Style.RESET_ALL}")
        return None

def test_docker_generator(project_info, output_dir):
    """Test the Docker generator functionality."""
    print("\nTesting Docker generator")
    
    dockerfile_path = os.path.join(output_dir, 'Dockerfile')
    result = generate_dockerfile(project_info, dockerfile_path)
    
    if result and os.path.exists(dockerfile_path):
        print(f"{Fore.GREEN}✓ Dockerfile generated successfully{Style.RESET_ALL}")
        print(f"  Created: {dockerfile_path}")
        
        # Check the file content
        with open(dockerfile_path, 'r') as f:
            content = f.read()
            if 'FROM node:' in content and 'FROM nginx:' in content:
                print(f"{Fore.GREEN}✓ Dockerfile content looks valid{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ Dockerfile content may have issues{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Failed to generate Dockerfile{Style.RESET_ALL}")

def test_nginx_generator(project_info, output_dir):
    """Test the Nginx generator functionality."""
    print("\nTesting Nginx generator")
    
    nginx_path = os.path.join(output_dir, 'nginx.conf')
    result = generate_nginx_config(project_info, nginx_path)
    
    if result and os.path.exists(nginx_path):
        print(f"{Fore.GREEN}✓ Nginx configuration generated successfully{Style.RESET_ALL}")
        print(f"  Created: {nginx_path}")
        
        # Check the file content
        with open(nginx_path, 'r') as f:
            content = f.read()
            if 'listen 80;' in content and 'try_files $uri $uri/ /index.html;' in content:
                print(f"{Fore.GREEN}✓ Nginx configuration content looks valid{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ Nginx configuration content may have issues{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ Failed to generate Nginx configuration{Style.RESET_ALL}")

def run_tests():
    """Run all tests."""
    print(f"{Fore.BLUE}=======================================")
    print(f"    VESSEL BASIC FUNCTIONALITY TESTS")
    print(f"======================================={Style.RESET_ALL}")
    
    # Get a React project path to test
    while True:
        test_path = input("Enter the path to a React project (or 'q' to quit): ")
        if test_path.lower() == 'q':
            return
        
        if os.path.exists(test_path):
            break
        else:
            print(f"{Fore.RED}Path does not exist. Please enter a valid path.{Style.RESET_ALL}")
    
    # Create a temporary output directory
    output_dir = './vessel-test-output'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    try:
        # Test analyzer
        project_info = test_analyzer(test_path)
        if not project_info:
            print(f"{Fore.RED}Analyzer test failed. Stopping tests.{Style.RESET_ALL}")
            return
            
        # Test Docker generator
        test_docker_generator(project_info, output_dir)
        
        # Test Nginx generator
        test_nginx_generator(project_info, output_dir)
        
        # Final report
        print(f"\n{Fore.BLUE}=======================================")
        print(f"    TEST SUMMARY")
        print(f"======================================={Style.RESET_ALL}")
        print(f"Output files are available in: {output_dir}")
        print(f"You can inspect these files to verify they meet your requirements.")
        
    finally:
        # Cleanup option
        keep_files = input("\nKeep generated test files? [y/N]: ")
        if keep_files.lower() != 'y':
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
                print(f"Test output directory removed.")

if __name__ == "__main__":
    run_tests()