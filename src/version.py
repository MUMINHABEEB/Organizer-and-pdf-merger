"""Version management for AI Automation Suite"""

__version__ = "0.1.0"
__app_name__ = "AI Automation Suite"
__publisher__ = "Ramidos"

# Update server configuration (for future auto-updates)
UPDATE_CHECK_URL = "https://your-domain.com/api/version-check"
DOWNLOAD_BASE_URL = "https://your-domain.com/downloads/"

def get_version_info():
    """Get current version information"""
    return {
        "version": __version__,
        "app_name": __app_name__,
        "publisher": __publisher__
    }

def parse_version(version_string):
    """Parse version string into comparable tuple"""
    return tuple(map(int, version_string.split('.')))

def is_newer_version(current, remote):
    """Check if remote version is newer than current"""
    return parse_version(remote) > parse_version(current)
