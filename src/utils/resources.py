import os, sys

# Resource path helpers for dev and PyInstaller frozen builds.

def _base_dir():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS  # type: ignore[attr-defined]
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def resource_path(*parts: str) -> str:
    """Return an absolute path for a resource under src/resources.
    parts: path components relative to resources root.
    """
    root = os.path.abspath(os.path.join(_base_dir(), "resources"))
    return os.path.join(root, *parts)


def image_path(name: str) -> str:
    return resource_path("images", name)


def ensure_exists(path: str) -> bool:
    return os.path.exists(path)
