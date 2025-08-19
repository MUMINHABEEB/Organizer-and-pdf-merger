#!/bin/bash

# This script builds the AI Automation Suite executable using PyInstaller.

# Navigate to the source directory
cd ../src

# Create a build directory if it doesn't exist
mkdir -p build

# Use PyInstaller to create the executable
pyinstaller --onefile --name "AI_Automation_Suite" app.py

# Move the generated executable to the build directory
mv dist/AI_Automation_Suite ../scripts/

# Clean up unnecessary files
rm -rf build dist __pycache__ *.spec

echo "Executable built successfully and moved to the scripts directory."