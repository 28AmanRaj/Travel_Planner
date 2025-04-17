# #!/bin/bash
# # Update and install Python dependencies
# sudo apt update -y
# sudo apt install -y python3 python3-pip
# cd /home/ubuntu/LessonPlan-Generator
# pip3 install -r requirements.txt
# #pip3 install -r /home/ubuntu/LessonPlan-Generator/requirements.txt

#!/bin/bash!

# Update and install Python 3.12 and required packages
sudo apt update -y
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip

# Navigate to the deployment directory
DEPLOY_DIR=$(dirname "$0")/..
cd "$DEPLOY_DIR" || exit 1

# Log the current directory for debugging
echo "Current working directory: $(pwd)"
ls -l  # List files in the current directory for debugging

# Create a virtual environment using Python 3.12 if it doesn't exist
VENV_DIR="$DEPLOY_DIR/venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR using Python 3.12"
    python3.12 -m venv "$VENV_DIR"
    # Change ownership of the virtual environment to the current user
    sudo chown -R $(whoami):$(whoami) "$VENV_DIR"
else
    echo "Virtual environment already exists in $VENV_DIR"
    # Ensure the virtual environment is owned by the current user
    sudo chown -R $(whoami):$(whoami) "$VENV_DIR"
fi

# Activate the virtual environment
echo "Activating virtual environment"
source "$VENV_DIR/bin/activate"

# Verify Python version inside the virtual environment
echo "Using Python version:"
python --version

# Upgrade pip and install dependencies
echo "Upgrading pip and installing dependencies from requirements.txt"
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "requirements.txt not found in $(pwd)"
    deactivate
    exit 1
fi

# Deactivate the virtual environment
if command -v deactivate &> /dev/null; then
    echo "Deactivating virtual environment"
    deactivate
else
    echo "deactivate command not found. Skipping."
fi