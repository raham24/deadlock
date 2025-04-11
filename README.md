# Create a virtual environment
python -m venv vessel-env

# Activate the virtual environment (on Windows)
# vessel-env\Scripts\activate

# Activate the virtual environment (on macOS/Linux)
# source vessel-env/bin/activate

# Install required packages
pip install click colorama

# Install your package in development mode
pip install -e .