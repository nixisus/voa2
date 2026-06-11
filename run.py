#!/usr/bin/env python3
"""
PyLearn - Python Interactive Learning Application

A terminal-based learning application that guides non-technical business school
students through Python fundamentals via an AI-like conversational interface.
"""

import sys

# Minimum Python version check
MIN_PYTHON_VERSION = (3, 10)


def check_python_version() -> None:
    """Verify Python version meets minimum requirements."""
    if sys.version_info < MIN_PYTHON_VERSION:
        sys.exit(
            f"PyLearn requires Python {'.'.join(map(str, MIN_PYTHON_VERSION))} or later. "
            f"You have Python {sys.version_info.major}.{sys.version_info.minor}."
        )


def main() -> None:
    """Initialize and run the PyLearn application."""
    check_python_version()
    
    # Import here to ensure version check passes first
    from pylearn import config
    from pylearn.tutor import Tutor
    from pylearn.ui import TerminalUI
    
    # Initialize the terminal UI
    ui = TerminalUI()
    
    # Start the interactive tutor session
    tutor = Tutor(ui)
    tutor.run()


if __name__ == "__main__":
    main()