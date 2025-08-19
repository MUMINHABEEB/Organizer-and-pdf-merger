#!/usr/bin/env python3
"""Quick test to see if webview imports work."""

import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Frozen: {hasattr(sys, '_MEIPASS')}")

try:
    import webview
    version = getattr(webview, '__version__', 'unknown')
    print(f"✓ webview imported successfully: {version}")
    
    # Check available GUI backends
    backends = []
    try:
        import webview.platforms.qt
        backends.append("qt")
    except:
        pass
    try:
        import webview.platforms.edgechromium
        backends.append("edgechromium")
    except:
        pass
    print(f"Available backends: {backends}")
    
except Exception as e:
    print(f"✗ webview import failed: {e}")
    import traceback
    traceback.print_exc()

print("Test complete.")
input("Press Enter to exit...")
