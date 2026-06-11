"""
PyLearn - Python Interactive Learning Application

A terminal-based learning application that guides non-technical business school
students through Python fundamentals via an AI-like conversational interface.

Architecture Overview:
    PyLearn follows a modular architecture with clear separation of concerns:

    - auth.py: User authentication with educational passphrase hashing
    - session.py: Session and progress tracking
    - ui.py: Terminal UI components using Rich library
    - curriculum.py: Lesson content and structure
    - tutor.py: Conversational learning engine
    - config.py: Application configuration

Usage:
    Run the application with: python run.py

    For new users, the app will guide you through creating a profile and
    then walk you through interactive lessons.

    For returning users, your progress is automatically saved and you
    can continue from where you left off.

Example:
    >>> from pylearn import Tutor
    >>> from pylearn.ui import TerminalUI
    >>> ui = TerminalUI()
    >>> tutor = Tutor(ui)
    >>> tutor.run()

Security Note:
    This is an educational application demonstrating security concepts.
    Passphrases are hashed using SHA-256 for learning purposes.
    Do not use this code for production authentication systems.
"""

__version__ = "1.0.0"
__author__ = "PyLearn Team"
__license__ = "MIT"

# Core components - main entry points
from pylearn.auth import UserProfile, profile_exists, get_current_profile
from pylearn.session import SessionManager, get_session_manager
from pylearn.ui import TerminalUI
from pylearn.curriculum import Curriculum, get_curriculum, Lesson, Question
from pylearn.tutor import Tutor, create_tutor
from pylearn.config import (
    APP_NAME,
    APP_VERSION,
    ensure_pylearn_dir,
    is_test_mode,
    set_test_mode,
)

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__license__",
    # Authentication
    "UserProfile",
    "profile_exists",
    "get_current_profile",
    # Session management
    "SessionManager",
    "get_session_manager",
    # User Interface
    "TerminalUI",
    # Curriculum
    "Curriculum",
    "get_curriculum",
    "Lesson",
    "Question",
    # Tutor
    "Tutor",
    "create_tutor",
    # Configuration
    "APP_NAME",
    "APP_VERSION",
    "ensure_pylearn_dir",
    "is_test_mode",
    "set_test_mode",
]