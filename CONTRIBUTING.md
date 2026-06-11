# Contributing to PyLearn

Thank you for your interest in contributing to PyLearn! This document provides
guidelines and instructions for developers who want to extend or improve the application.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Adding New Lessons](#adding-new-lessons)
3. [Coding Standards](#coding-standards)
4. [Testing](#testing)
5. [Security Considerations](#security-considerations)

## Project Structure

```
pylearn/
├── __init__.py      # Package exports and version info
├── auth.py          # User authentication (educational hashing)
├── config.py       # Application configuration
├── curriculum.py   # Lesson content and structure
├── session.py      # Progress tracking and session management
├── tutor.py        # Conversational learning engine
└── ui.py           # Terminal UI components using Rich
```

## Adding New Lessons

To add a new lesson to the curriculum:

### Step 1: Create the lesson content

Edit `pylearn/curriculum.py` and add a new `Lesson` object in the `_build_curriculum()` method:

```python
# Example: Adding a new lesson
new_lesson = Lesson(
    id="my_new_lesson",           # Unique identifier (snake_case)
    title="My New Lesson",        # Display title
    content="""Your lesson content here.
    Can include multiple paragraphs and even code examples:
    
    ```python
    print("Hello!")
    ```
    """,
    questions=[
        Question(
            id="nl1",             # Unique question ID
            text="What does this do?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            options=[
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            correct_answer="B",
            hint="Think about the code.",
            explanation="Explanation of the correct answer."
        )
    ],
    next_lesson_id="existing_next_lesson",  # ID of next lesson
    estimated_minutes=5
)
```

### Step 2: Update the previous lesson's `next_lesson_id`

Link the previous lesson to your new one:

```python
# In the previous lesson:
previous_lesson = Lesson(
    id="previous_lesson",
    # ... content ...
    next_lesson_id="my_new_lesson"  # Point to your new lesson
)
```

### Step 3: Add lesson takeaways

Update `_get_lesson_takeaways()` in `tutor.py`:

```python
takeaway_map = {
    # ... existing entries ...
    "my_new_lesson": [
        "Key point 1",
        "Key point 2",
        "Key point 3"
    ]
}
```

## Question Types

Available question types in `QuestionType`:
- `MULTIPLE_CHOICE` - Select from A, B, C, D options
- `FREE_TEXT` - Free-form text answer
- `CODE_COMPLETION` - Complete missing code
- `CODE_EXPLANATION` - Explain what code does

## Coding Standards

### Python Style
- Follow PEP 8 guidelines
- Use snake_case for variable and function names
- Use PascalCase for class names
- Maximum line length: 88 characters (Black default)

### Documentation
- All modules must have module-level docstrings
- All classes must have docstrings with Attributes section
- All public methods must have docstrings
- Include type hints where beneficial

### Example:
```python
def calculate_roi(gain: float, cost: float) -> float:
    """
    Calculate Return on Investment (ROI).
    
    Args:
        gain: The gain from the investment
        cost: The original cost of the investment
    
    Returns:
        The ROI as a percentage (e.g., 20.0 for 20%)
    
    Raises:
        ValueError: If cost is zero or negative
    
    Example:
        >>> calculate_roi(1200, 1000)
        20.0
    """
    if cost <= 0:
        raise ValueError("Cost must be positive")
    return ((gain - cost) / cost) * 100
```

## Testing

### Running Tests
```bash
python test_runner.py
```

### Writing Tests
- Test each module independently
- Use temporary directories for file operations
- Mock user input for interactive features

### Test Coverage Goals
- Core functionality: 100%
- Edge cases: 90%+
- Error handling: 80%+

## Security Considerations

This is an **educational** application demonstrating security concepts.
If you modify authentication-related code:

### Do:
- Use strong hashing algorithms (bcrypt, scrypt, argon2) in production
- Implement rate limiting for login attempts
- Store salt separately from hashes in production
- Use secure random number generation for salts

### Don't:
- Use SHA-256 for production passwords (it's too fast/fast to brute)
- Store plain text passwords ever
- Log sensitive information
- Hardcode secrets in source code

## Extension Ideas

Here are some ideas for extending PyLearn:

1. **More Lessons**: Add lessons on files, exceptions, OOP, libraries
2. **Adaptive Learning**: Track difficulty and adjust question difficulty
3. **Code Exercises**: Add interactive code execution
4. **Progress Badges**: Award badges for completing sections
5. **Export Progress**: Generate PDF certificates
6. **Multiple Users**: Add admin dashboard for teachers
7. **AI Integration**: Connect to LLM for personalized feedback

## Getting Help

If you have questions:
1. Read the module docstrings - they're comprehensive
2. Check existing lessons for patterns
3. Run `test_runner.py` to understand expected behavior

## License

By contributing to PyLearn, you agree that your contributions will be
licensed under the MIT License.