# Vessel

A Flask-based API server that integrates with GitHub and Pensar.dev for repository scanning and analysis.

## Overview

Vessel is a backend service that provides API endpoints for:

- Retrieving GitHub repository information
- Managing pull request data
- Dispatching security scans through Pensar.dev

## Prerequisites

- Python 3.x
- pip (Python package manager)
- Pensar.dev API key

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd vessel
```

2. Create and activate a virtual environment:

```bash
cd flask_server
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the following variables in `.env`:
     ```
     GITHUB_API_URL=https://api.github.com
     GITHUB_TOKEN=your_github_token
     ```

## Running the Server

1. Activate the virtual environment (if not already activated):

```bash
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

2. Start the Flask server:

```bash
python server.py
```

The server will start on `http://localhost:5000` by default.

## API Endpoints

### 1. Get Repository ID

- **Endpoint**: `/api/repo/id`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "github_url": "https://github.com/owner/repo"
  }
  ```
- **Response**: Repository ID and metadata

### 2. Get Pull Request URL

- **Endpoint**: `/api/repo/pull`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "github_url": "https://github.com/owner/repo",
    "pull_number": 123
  }
  ```
- **Response**: Pull request URL

### 3. Dispatch Scan

- **Endpoint**: `/api/repo/scan`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "apiKey": "your_pensar_api_key",
    "repoId": "repository_id",
    "eventType": "scan_type",
    "pullRequest": "pr_url",
    "targetBranch": "branch_name",
    "apiUrl": "optional_api_url"
  }
  ```
- **Response**: Scan queue status

## Error Handling

The API includes error handling for:

- 404 Not Found
- 500 Internal Server Error
- Invalid GitHub URLs
- API request failures

## Security

- API keys and tokens should be stored in the `.env` file
- Never commit the `.env` file to version control
- Use HTTPS for all API communications

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
