# Optional helper to install project dependencies
if (Test-Path .venv/Scripts/Activate.ps1) { . .venv/Scripts/Activate.ps1 }
python -m pip install --upgrade pip
pip install -r requirements.txt
