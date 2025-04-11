import os
import logging

def generate_nginx_config(project_info, output_path):
    """
    Generate an Nginx configuration for the React project.
    
    Args:
        project_info (dict): Project information from analyzer
        output_path (str): Where to save the Nginx config
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create an optimized Nginx config for single-page React apps
        nginx_content = """server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;
    
    # Enable gzip compression
    gzip on;
    gzip_comp_level 5;
    gzip_min_length 256;
    gzip_proxied any;
    gzip_vary on;
    gzip_types
        application/javascript
        application/json
        application/x-javascript
        text/css
        text/javascript
        text/plain;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
    
    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
}
"""
            
        # Write to file
        with open(output_path, 'w') as f:
            f.write(nginx_content)
            
        return True
        
    except Exception as e:
        logging.error(f"Error generating Nginx config: {str(e)}")
        return False