import os
import json
import logging

def analyze_python_project(project_path):
    """
    Analyze a plain Python project and gather information about its structure.
    
    Args:
        project_path (str): Path to the Python project
        
    Returns:
        dict: Project information or None if not a valid Python project
    """
    # Check for requirements.txt
    requirements_txt_path = os.path.join(project_path, 'requirements.txt')
    if not os.path.exists(requirements_txt_path):
        return None
    
    # Parse requirements.txt
    try:
        with open(requirements_txt_path, 'r') as f:
            requirements = f.readlines()
            
        # Gather basic project info
        project_info = {
            'name': os.path.basename(project_path),
            'path': project_path,
            'requirements': [req.strip() for req in requirements],
        }
        
        # Determine build command and output directory
        project_info['build_command'] = 'pip install -r requirements.txt'
        project_info['build_output'] = 'venv'  # Standard virtual environment directory
        
        return project_info
        
    except Exception as e:
        logging.error(f"Error analyzing project: {str(e)}")
        return None