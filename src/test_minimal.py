#!/usr/bin/env python3
"""Minimal test to verify PyInstaller basics work"""

import sys
import os
print(f"Python version: {sys.version}")
print(f"Executable: {sys.executable}")
print(f"Frozen: {hasattr(sys, '_MEIPASS')}")
if hasattr(sys, '_MEIPASS'):
    print(f"MEIPASS: {sys._MEIPASS}")
print(f"CWD: {os.getcwd()}")
print("Basic Python functionality works!")

try:
    import webview
    print("✓ webview imported successfully")
    print(f"webview version: {webview.__version__}")
except Exception as e:
    print(f"✗ webview import failed: {e}")
    import traceback
    traceback.print_exc()

input("Press Enter to exit...")
