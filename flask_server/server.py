from flask import Flask, request, jsonify, send_from_directory
import os
import requests
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
GITHUB_API_URL = 'https://api.github.com'


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

@app.route('/api/repo/id', methods=['POST'])
def get_repository_id():
    data = request.json
    if not data or 'github_url' not in data:
        return jsonify({"error": "Github URL is required"}), 400
    github_url = data["github_url"]

    if 'github.com/' not in github_url:
        return jsonify({"error": "Invalid github URL"}), 400
    
    try:
        repo_path = github_url.split("github.com/")[1]
        repo_path = repo_path.split('#')[0].split('?')[0].rstrip('/')

        parts = repo_path.split("/")

        if len(parts) < 2:
            return jsonify({"error": "Invalid repository format"}), 400

        owner, repo = parts[0], parts[1]

        response = requests.get(f"{GITHUB_API_URL}/repos/{owner}/{repo}")
        response.raise_for_status()

        repo_data = response.json()
        repo_id = repo_data['id']

        return jsonify({
            "id": repo_id,
            "name": repo_data['name'],
            "owner": repo_data['owner']['login'],
            "url": repo_data['html_url']
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"GitHub API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
@app.route  
if __name__ == '__main__':
    app.run(debug=True)
