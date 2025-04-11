import os
import logging

def generate_dockerfile(project_info, output_path):
    """
    Generate a Dockerfile for the plain React project.
    
    Args:
        project_info (dict): Project information from analyzer
        output_path (str): Where to save the Dockerfile
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Determine Node version (could be improved to detect from package.json)
        node_version = "16-alpine"
        build_output = project_info.get('build_output', 'build')
        
        # Create Dockerfile content for a standard React app
        dockerfile_content = f"""# Build stage
FROM node:{node_version} AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/{build_output} /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""
        
        # Write to file
        with open(output_path, 'w') as f:
            f.write(dockerfile_content)
            
        return True
        
    except Exception as e:
        logging.error(f"Error generating Dockerfile: {str(e)}")
        return False