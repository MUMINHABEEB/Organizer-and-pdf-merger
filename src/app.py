from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import os
import sys
from gui.main_window import MainWindow
import traceback

def resource_path(relative):
    """Get absolute path to resource (works for dev and PyInstaller)."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)

# If running as a frozen exe, set CWD to the exe directory
if getattr(sys, "frozen", False):
    os.chdir(os.path.dirname(sys.executable))

def main():
    # High-DPI for crisp UI
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # Optional icon (add assets/app.ico to use)
    icon_path = resource_path(os.path.join("assets", "app.ico"))
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Install a global exception hook to capture startup/runtime errors in the packaged app
    def _exception_hook(exctype, value, tb):
        try:
            base_dir = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
            logs_dir = os.path.join(base_dir, "logs")
            os.makedirs(logs_dir, exist_ok=True)
            log_path = os.path.join(logs_dir, "app_crash.log")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write("\n=== Unhandled exception ===\n")
                traceback.print_exception(exctype, value, tb, file=f)
        except Exception:
            pass
        try:
            # Also print to stderr for console/terminal visibility
            traceback.print_exception(exctype, value, tb)
            QMessageBox.critical(None, "Application Error", f"An unexpected error occurred.\nDetails were logged to 'logs\\app_crash.log'.\n\n{value}")
        except Exception:
            pass

    sys.excepthook = _exception_hook

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()