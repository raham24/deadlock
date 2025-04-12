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
PENSAR_STATUS_URL = "https://api.pensar.dev/ci/scan/status"
PENSAR_ISSUES_URL = "https://api.pensar.dev/ci/scan/issues"


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


@app.route('/check-scan-status', methods=['POST'])
def check_scan_status():
    # Get data from request
    data = request.json

    if not data or 'scanId' not in data:
        return jsonify({"error": "Missing scanId"}), 400

    scan_id = data['scanId']

    try:
        # Send request to Pensar status API
        status_payload = {
            "scanId": scan_id,
            "apiKey": PENSAR_API_KEY
        }

        status_response = requests.post(
            PENSAR_STATUS_URL,
            json=status_payload
        )
        status_response.raise_for_status()

        return jsonify({
            "success": True,
            "scanId": scan_id,
            "statusResponse": status_response.json()
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": str(e),
            "details": e.response.json() if hasattr(e, 'response') and e.response else None
        }), 500


@app.route('/get-scan-issues', methods=['POST'])
def get_scan_issues():
    # Get data from request
    data = request.json

    if not data or 'scanId' not in data:
        return jsonify({"error": "Missing scanId"}), 400

    scan_id = data['scanId']

    try:
        # Send request to Pensar issues API
        issues_payload = {
            "scanId": scan_id,
            "apiKey": PENSAR_API_KEY
        }

        issues_response = requests.post(
            PENSAR_ISSUES_URL,
            json=issues_payload
        )
        issues_response.raise_for_status()

        return jsonify({
            "success": True,
            "scanId": scan_id,
            "issuesResponse": issues_response.json()
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": str(e),
            "details": e.response.json() if hasattr(e, 'response') and e.response else None
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

@app.route('/api/issues', methods=['GET'])
def get_issues():
    """Get all issues or filter by severity/category"""
    severity = request.args.get('severity')
    category = request.args.get('category')
    
    if severity:
        issues = issue_manager.get_issues_by_severity(severity)
    elif category:
        issues = issue_manager.get_issues_by_category(category)
    else:
        issues = issue_manager.get_all_issues()
    
    return jsonify({"issues": issues})

@app.route('/api/issues/report', methods=['GET'])
def get_issues_report():
    """Get a summary report of all issues"""
    report = issue_manager.generate_report()
    return jsonify(report)

@app.route('/api/issues', methods=['POST'])
def add_issue():
    """Add a new issue"""
    data = request.json
    
    try:
        issue = Issue(**data)
        issue_manager.add_issue(issue)
        return jsonify({"message": "Issue added successfully", "issue": issue.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/issues/bulk', methods=['POST'])
def add_issues_bulk():
    """Add multiple issues at once"""
    data = request.json
    
    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of issues"}), 400
    
    issue_manager.add_issues_from_list(data)
    return jsonify({"message": f"Added {len(data)} issues"}), 201

@app.route('/api/issues', methods=['DELETE'])
def clear_issues():
    """Clear all issues"""
    issue_manager.clear_issues()
    return jsonify({"message": "All issues cleared"}), 200

@app.route('/api/issues/save', methods=['POST'])
def save_issues():
    """Save issues to a file"""
    data = request.json
    filepath = data.get('filepath', 'issues.json')
    
    success = issue_manager.save_to_file(filepath)
    if success:
        return jsonify({"message": f"Saved issues to {filepath}"}), 200
    else:
        return jsonify({"error": "Failed to save issues"}), 500

@app.route('/api/issues/load', methods=['POST'])
def load_issues():
    """Load issues from a file"""
    data = request.json
    filepath = data.get('filepath', 'issues.json')
    
    success = issue_manager.load_from_file(filepath)
    if success:
        return jsonify({"message": f"Loaded issues from {filepath}", "count": len(issue_manager.issues)}), 200
    else:
        return jsonify({"error": f"Failed to load issues from {filepath}"}), 500
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
