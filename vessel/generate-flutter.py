import os
import sys

project_path = sys.argv[1] if len(sys.argv) > 1 else "."
dockerfile_path = os.path.join(project_path, "Dockerfile")

dockerfile_content = """
FROM cirrusci/flutter:stable

WORKDIR /app
COPY . .

RUN flutter pub get

CMD ["flutter", "run"]
""".strip()

with open(dockerfile_path, "w") as f:
    f.write(dockerfile_content)

print("✅ Flutter Dockerfile generated at", dockerfile_path)
