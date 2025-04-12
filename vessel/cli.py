import os
import subprocess
import click

def detect_project_type(project_path):
    package_json_path = os.path.join(project_path, "package.json")
    pubspec_path = os.path.join(project_path, "pubspec.yaml")

    if os.path.exists(pubspec_path):
        return "flutter"
    elif os.path.exists(package_json_path):
        try:
            with open(package_json_path) as f:
                package_data = f.read()
                # Looser match to detect react in either dependencies or devDependencies
                if "react" in package_data:
                    return "react"
                else:
                    return "node"
        except Exception as e:
            print("⚠️ Failed to read package.json:", e)
            return "node"
    else:
        return "unknown"


@click.group()
def cli():
    pass

@cli.command()
@click.argument('project_path')
def build(project_path):
    abs_path = os.path.abspath(project_path)
    project_type = detect_project_type(abs_path)
    
    print(f"📁 Project path: {abs_path}")
    print(f"🔍 Detected project type: {project_type}")

    if project_type in ["node", "react"]:
        try:
            subprocess.run(["node", "generate-docker.js", abs_path], check=True)
            print("✅ Dockerfile generated for", project_type)
        except subprocess.CalledProcessError as e:
            print("❌ Failed to generate Dockerfile:", e)
    elif project_type == "flutter":
        try:
            subprocess.run(["python3", "generate-flutter.py", abs_path], check=True)
            print("✅ Dockerfile generated for Flutter project")
        except subprocess.CalledProcessError as e:
            print("❌ Failed to generate Flutter Dockerfile:", e)
    else:
        print("❌ Unsupported or unknown project type.")
