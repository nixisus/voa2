# PyLearn

Python Interactive Learning Application - A terminal-based learning app for business school students.

## Quick Start

```bash
pip install rich
python run.py
```

## What is PyLearn?

PyLearn is an interactive terminal application that teaches Python programming to non-technical business students. It features:

- **11 Structured Lessons** - From basics to building a business calculator
- **Interactive Quizzes** - Immediate feedback and hints
- **Progress Tracking** - Your work is saved automatically
- **Educational Security** - Learn why we hash passwords (not just how)

## Project Structure

```
pylearn/
├── __init__.py      # Package exports
├── auth.py          # User authentication (educational hashing)
├── config.py        # Application configuration
├── curriculum.py    # Lesson content and structure
├── session.py       # Progress tracking
├── tutor.py         # Conversational learning engine
└── ui.py            # Terminal UI components
```

## Documentation

See the `docs/` folder for development documentation:
- `PLANNING_DOCUMENT.md` - Original project specification
- `CONVERSATION_LOG.md` - How this project was built with AI

## Running Tests

```bash
python test_runner.py
```

## Requirements

- Python 3.10+
- Rich library (`pip install rich`)