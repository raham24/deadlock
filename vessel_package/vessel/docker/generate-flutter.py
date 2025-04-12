import os
import sys

project_path = sys.argv[1] if len(sys.argv) > 1 else "."
dockerfile_path = os.path.abspath(os.path.join(project_path, "Dockerfile"))

# Prevent writing outside of project root
if not dockerfile_path.startswith(os.path.abspath(os.getcwd())):
    raise ValueError("Unsafe Dockerfile path")

dockerfile_content = """
FROM cirrusci/flutter:stable

WORKDIR /app
COPY . .

RUN flutter pub get

CMD ["flutter", "run"]
""".strip()

with open(dockerfile_path, "w", encoding="utf-8") as f:
    f.write(dockerfile_content)

print("Flutter Dockerfile generated at", dockerfile_path)
