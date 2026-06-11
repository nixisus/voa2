"""
Configuration Module

This module contains application configuration settings.
All configuration is centralized here for easy modification.

Design Decisions:
    - All settings are module-level constants for easy access
    - Functions are provided for path management
    - Test mode support for automated testing
    - Educational security settings (not production-ready)

Configuration Categories:
    - Application Info: Name, version, description
    - Storage Paths: Where user data is stored
    - Terminal Settings: UI dimensions
    - Security Settings: File permissions (educational)
    - Tutor Settings: Encouragement messages, colors

Example:
    >>> from pylearn.config import APP_NAME, APP_VERSION
    >>> print(f"Running {APP_NAME} v{APP_VERSION}")
    'Running PyLearn v1.0.0'
    >>> from pylearn.config import ensure_pylearn_dir
    >>> ensure_pylearn_dir()  # Creates ~/.pylearn if needed

Environment Variables:
    PYLEARN_TEST_MODE - Set to "1", "true", or "yes" to enable test mode

Note:
    This is a simple educational app. In production applications,
    configuration would typically be loaded from environment variables
    or external config files with validation.
"""

import os
from pathlib import Path


# Application info
APP_NAME = "PyLearn"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Interactive Python Learning Application"


# Storage paths
HOME_DIR = Path.home()
PYLEARN_DIR = HOME_DIR / ".pylearn"
PROFILE_FILE = PYLEARN_DIR / "profile.json"
PROGRESS_FILE = PYLEARN_DIR / "progress.json"
ANSWERS_FILE = PYLEARN_DIR / "answers.json"


# Terminal settings
DEFAULT_WIDTH = 80
MAX_WIDTH = 120
MIN_WIDTH = 60


# Curriculum settings
DEFAULT_START_LESSON = "welcome"
ENABLE_HINTS = True
ENABLE_SKIP = True


# Security settings (educational)
# Note: These are for educational demonstration, not production security
HASH_ALGORITHM = "sha256"
SALT_PREFIX = "pylearn_salt_v1_"
DIRECTORY_PERMISSIONS = 0o700
FILE_PERMISSIONS = 0o600


# Tutor personality settings
ENCOURAGEMENT_MESSAGES = {
    "correct": [
        "Excellent! You've got it!",
        "Perfect! That's exactly right!",
        "Great job! You understand this concept!",
        "Wonderful! You're doing amazing!",
        "That's correct! Keep up the great work!",
        "Exactly right! You're a natural!",
        "Brilliant! You've mastered this!",
    ],
    "incorrect": [
        "Not quite, but that's okay! Let's try again.",
        "That's not it, but don't worry - learning takes practice!",
        "Close! Let me help you understand this better.",
        "That's okay! Mistakes help us learn.",
        "Not to worry - let's work through this together.",
    ]
}


# Colors (Rich library color names)
COLORS = {
    "header": "cyan",
    "success": "green",
    "error": "red",
    "warning": "yellow",
    "info": "blue",
    "hint": "yellow",
    "encouragement": "magenta",
    "code": "monokai",  # Syntax theme
}


def get_pylearn_dir() -> Path:
    """Get or create the PyLearn data directory."""
    if not PYLEARN_DIR.exists():
        PYLEARN_DIR.mkdir(parents=True, exist_ok=True)
        os.chmod(PYLEARN_DIR, DIRECTORY_PERMISSIONS)
    return PYLEARN_DIR


def ensure_pylearn_dir() -> None:
    """Ensure the PyLearn directory exists with correct permissions."""
    get_pylearn_dir()


def is_test_mode() -> bool:
    """Check if running in test mode."""
    return os.environ.get("PYLEARN_TEST_MODE", "").lower() in ("1", "true", "yes")


def set_test_mode(enabled: bool = True) -> None:
    """Enable or disable test mode."""
    os.environ["PYLEARN_TEST_MODE"] = "1" if enabled else ""