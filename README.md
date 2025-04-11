# Vessel

A command-line tool for deploying React applications to production environments.

## Development Setup

### Prerequisites
- Python 3.7+
- Docker (for testing deployment)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/vessel.git
cd vessel
```

2. Create and activate virtual environment
```bash
python -m venv vessel-env

# On Windows
vessel-env\Scripts\activate

# On macOS/Linux
source vessel-env/bin/activate
```

3. Install dependencies
```bash
pip install -e .
```

### Project Structure
```
vessel/
├── vessel/         # Main package
│   ├── __init__.py # Package initialization
│   └── cli.py      # Command-line interface
├── setup.py        # Package setup file
└── requirements.txt # Package dependencies
```

### Current Commands
```bash
# Build Docker configuration for a React project
vessel build /path/to/your/react-project
```

### Development Workflow
1. Make changes to the code
2. Test using `vessel build` command
3. Add new files to the package in setup.py if needed