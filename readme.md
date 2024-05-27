# Create project directory
mkdir my_fastapi_project
cd my_fastapi_project

# Create and activate virtual environment
python -m venv venv

# On macOS and Linux
source venv/bin/activate

# Create requirements.txt and install dependencies
echo "fastapi\nuvicorn\nrequests" > requirements.txt
pip install -r requirements.txt

# Create project structure
mkdir app
touch app/__init__.py
touch app/main.py

# Write FastAPI application code (add code to app/main.py)
