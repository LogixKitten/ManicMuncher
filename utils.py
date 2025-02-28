import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for development and PyInstaller."""
    if getattr(sys, 'frozen', False):  # Running as a compiled .exe
        base_path = sys._MEIPASS  # Temporary extraction folder used by PyInstaller
    else:
        base_path = os.path.abspath(".")  # Normal path in development

    return os.path.join(base_path, relative_path)