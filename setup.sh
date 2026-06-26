#!/usr/bin/env bash
set -e
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -d "$ROOT_DIR/.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$ROOT_DIR/.venv"
fi

echo "Activating virtual environment..."
source "$ROOT_DIR/.venv/bin/activate"

echo "Installing Python dependencies from requirements.txt..."
python3 -m pip install --upgrade pip
python3 -m pip install -r "$ROOT_DIR/requirements.txt"

cat <<'EOF'

SETUP NOTES:
- A virtual environment has been created at .venv
- To activate it manually: source .venv/bin/activate
- After installing Python packages, authenticate with Google Cloud and Earth Engine:

  1) Install/initialize gcloud and authenticate:
     gcloud init
     gcloud auth login
     gcloud auth application-default login

  2) Authenticate Earth Engine (if using ee Python CLI):
     earthengine authenticate

- For GCS/BigQuery access, ensure your Google account has necessary IAM roles and that you set the default project:
     gcloud config set project YOUR_PROJECT_ID

EOF
