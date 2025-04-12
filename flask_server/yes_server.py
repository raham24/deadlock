from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

app = Flask(__name__)

# Configuration
GITHUB_API_TOKEN = os.getenv('GITHUB_API_TOKEN')
PENSAR_API_KEY = os.getenv('PENSAR_API_KEY')
PENSAR_API_URL = "https://api.pensar.dev/ci/scan/dispatch"

@app.route('/trigger-scan', methods=['POST'])
def trigger_scan():
    # Get data from request
    data = request.json
    
    if not data or not all(k in data for k in ['owner', 'repo', 'prNumber', 'targetBranch']):
        return jsonify({"error": "Missing required fields"}), 400
    
    owner = data['owner']
    repo = data['repo']
    pr_number = data['prNumber']
    target_branch = data['targetBranch']
    
    try:
        # Get repository ID from GitHub API
        repo_response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}",
            headers={
                "Authorization": f"token {GITHUB_API_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
        )
        repo_response.raise_for_status()
        repo_data = repo_response.json()
        repo_id = repo_data['id']
        
        # Construct pull request URL
        pull_request_url = f"https://github.com/{owner}/{repo}/pull/{pr_number}"
        
        # Send request to Pensar API
        pensar_payload = {
            "repoId": repo_id,
            "apiKey": PENSAR_API_KEY,
            "targetBranch": target_branch,
            "actionRunId": 1,  # As per your example
            "pullRequest": pull_request_url,
            "eventType": "pull-request"
        }
        
        pensar_response = requests.post(
            PENSAR_API_URL,
            json=pensar_payload
        )
        pensar_response.raise_for_status()
        
        return jsonify({
            "success": True,
            "repoId": repo_id,
            "pullRequest": pull_request_url,
            "pensarResponse": pensar_response.json()
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": str(e),
            "details": e.response.json() if hasattr(e, 'response') and e.response else None
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))

