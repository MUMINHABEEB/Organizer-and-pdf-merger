import sys
print("=== STARTING DEBUG TEST ===")
print("About to import webview...")

try:
    import webview
    print("✓ webview imported successfully")
    
    print("Creating simple window...")
    window = webview.create_window('Test Window', html='<h1>Hello World!</h1>')
    
    print("Starting webview...")
    webview.start(debug=True)
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
