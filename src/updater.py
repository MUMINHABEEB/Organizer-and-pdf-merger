"""Auto-update functionality for AI Automation Suite"""

import json
import requests
import threading
import webbrowser
from pathlib import Path
from src.version import __version__, UPDATE_CHECK_URL, get_version_info, is_newer_version

class UpdateChecker:
    def __init__(self):
        self.current_version = __version__
        self.update_available = False
        self.latest_version = None
        self.download_url = None
        self.release_notes = None
        
    def check_for_updates(self, callback=None, silent=True):
        """Check for updates in background thread"""
        def _check():
            try:
                response = requests.get(UPDATE_CHECK_URL, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    latest_version = data.get('latest_version')
                    if latest_version and is_newer_version(self.current_version, latest_version):
                        self.update_available = True
                        self.latest_version = latest_version
                        self.download_url = data.get('download_url')
                        self.release_notes = data.get('release_notes', 'New version available')
                        
                        if callback:
                            callback(self)
                        elif not silent:
                            self._show_update_notification()
                            
            except Exception as e:
                if not silent:
                    print(f"Update check failed: {e}")
                    
        thread = threading.Thread(target=_check, daemon=True)
        thread.start()
        
    def _show_update_notification(self):
        """Show update notification (you can customize this)"""
        message = f"""
        🎉 New version available!
        
        Current: v{self.current_version}
        Latest: v{self.latest_version}
        
        {self.release_notes}
        
        Would you like to download the update?
        """
        
        # For now, just print - you can integrate with your UI
        print(message)
        
    def download_update(self):
        """Open download page in browser"""
        if self.download_url:
            webbrowser.open(self.download_url)
            
    def get_update_info(self):
        """Get update information"""
        return {
            'update_available': self.update_available,
            'current_version': self.current_version,
            'latest_version': self.latest_version,
            'download_url': self.download_url,
            'release_notes': self.release_notes
        }
