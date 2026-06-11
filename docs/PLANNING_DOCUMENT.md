# Python Interactive Learning App - Implementation Plan

## 1. OBJECTIVE

Build a terminal-based Python learning application that guides non-technical business school students through the fundamentals of programming via an AI-like conversational interface. The app teaches:
- Python basics (syntax, variables, data types, control flow, functions)
- Pseudo-code thinking (breaking problems into logical steps)
- Programming theory (why code matters, how to think like a programmer)
- Security awareness (passphrase creation, data protection concepts)

Students access the app via SSH on a shared Linux server. The app creates a `.pylearn` file in their home directory for session persistence. Authentication is educational — students create a passphrase they can inspect and understand.

## 2. CONTEXT SUMMARY

### Target Users
- Business school students with minimal technical background
- Access via web terminal (browser-based SSH client) or direct SSH
- One shared Linux server with individual user accounts

### Key Components
- **Entry Point:** `run.py` — simple launcher script
- **Core Engine:** Session manager with scripted conversational tutor
- **User Data:** `.pylearn/` directory in student's home (persistent storage)
- **Curriculum:** Structured lessons with branching dialogue and exercises
- **Documentation:** Inline code comments for future student developers

### Technical Stack
- **Language:** Python 3.10+
- **UI Framework:** Rich (for beautiful terminal output)
- **Architecture:** Single-file modules, modular design for extensibility

### Security Considerations (Educational)
- Passphrases stored as hashed values (teaches why we hash, not store plain text)
- No real sensitive data stored — focus is on demonstrating security concepts
- Code is fully inspectable — students can see how authentication works
- `.pylearn` directory permissions set to user-only (chmod 700)

## 3. APPROACH OVERVIEW

**Scripted Conversational Tutor** — Pre-written branching dialogue that guides students through lessons. This approach:
- Requires no external API keys or dependencies
- Provides consistent, predictable learning experience
- Can be extended with AI features later
- Allows non-interactive testing via CLI

**Session Persistence** — `~/.pylearn/` directory per user containing:
- `profile.json` — user info and hashed passphrase
- `progress.json` — current lesson and completion status
- `answers.json` — recorded answers to exercises

**Structured Curriculum Flow:**
1. Welcome & Setup → Create name and passphrase
2. Introduction to Programming → Why code matters for business
3. Pseudo-code Thinking → Breaking problems into steps
4. Python Basics → Hello World, syntax, variables
5. Data Types → Strings, numbers, booleans
6. Operators → Math, comparison, logical
7. Control Flow → If/else statements
8. Loops → For and while loops
9. Functions → Writing reusable code
10. Mini-project → Build a simple business calculator

## 4. IMPLEMENTATION STEPS

### Step 1: Project Structure & Core Dependencies
**Goal:** Set up the project skeleton with all necessary files and dependencies.

**Method:**
- Create `requirements.txt` with `rich` library
- Create `run.py` — simple launcher that imports and starts the app
- Create `pylearn/` package directory
- Add `__init__.py` to make it a package

**Files Created:**
- `requirements.txt`
- `run.py`
- `pylearn/__init__.py`

---

### Step 2: User Profile & Passphrase System
**Goal:** Handle user registration with name and passphrase creation. Educational focus on WHY we hash passphrases.

**Method:**
- Create `pylearn/auth.py` module
- Implement `UserProfile` class with methods for:
  - `create_profile(name, passphrase)` — first-time setup, hash passphrase
  - `authenticate(passphrase)` — verify against stored hash
  - `save()` and `load()` — JSON serialization to `~/.pylearn/profile.json`
- Hash using `hashlib.sha256` (with salt for educational realism)
- Include educational comments explaining WHY we hash (never store plain text)
- Create `~/.pylearn/` directory with mode 0o700 (user-only access)

**Files Created:**
- `pylearn/auth.py`

---

### Step 3: Session Manager & Progress Tracking
**Goal:** Track student progress through lessons and store their answers.

**Method:**
- Create `pylearn/session.py` module
- Implement `SessionManager` class:
  - `start_session(user_profile)` — initialize or resume session
  - `get_current_lesson()` — return current position in curriculum
  - `record_answer(lesson_id, question_id, answer)` — store to `answers.json`
  - `advance_lesson()` — move to next lesson
  - `get_progress()` — return completion percentage
- Store progress in `~/.pylearn/progress.json`

**Files Created:**
- `pylearn/session.py`

---

### Step 4: Rich Terminal UI Components
**Goal:** Create reusable terminal UI elements for beautiful, accessible output.

**Method:**
- Create `pylearn/ui.py` module with `TerminalUI` class
- Implement helper methods:
  - `print_header(text)` — styled section headers
  - `print_body(text)` — standard text with word wrap
  - `print_code(code)` — syntax-highlighted code blocks
  - `print_question(text, options)` — multiple choice with numbered options
  - `print_success(message)` — green success messages
  - `print_error(message)` — red error messages
  - `print_progress_bar(current, total)` — visual progress indicator
  - `clear_screen()` — clean terminal for fresh lesson
  - `pause(message)` — "Press Enter to continue"

**Files Created:**
- `pylearn/ui.py`

---

### Step 5: Curriculum Data Structure
**Goal:** Define the structured lesson content in a modular, extensible format.

**Method:**
- Create `pylearn/curriculum.py` module
- Define `Lesson` and `Question` dataclasses:
  - `Lesson`: id, title, content, questions[], next_lesson_id
  - `Question`: id, text, type (multiple_choice/free_text/code), options[], hint
- Create lesson content as structured data
- Implement `Curriculum` class with:
  - `get_lesson(lesson_id)` — retrieve lesson by ID
  - `get_next_lesson(current_id)` — navigate forward
  - `get_lesson_count()` — total lessons for progress calculation

**Files Created:**
- `pylearn/curriculum.py`

---

### Step 6: Conversational Tutor Engine
**Goal:** Create the AI-like interaction flow that guides students through lessons.

**Method:**
- Create `pylearn/tutor.py` module
- Implement `Tutor` class with conversational methods:
  - `welcome()` — opening message and setup prompt
  - `introduce_lesson(lesson)` — present lesson content
  - `ask_question(question)` — display question and collect input
  - `evaluate_answer(question, answer)` — check correctness, provide feedback
  - `provide_hint(question)` — give hints on request
  - `encourage()` — motivational messages for incorrect answers
  - `summarize()` — lesson wrap-up with key takeaways
- Include AI-like personality: encouraging, patient, uses plain language
- Branch dialogue based on student performance

**Files Created:**
- `pylearn/tutor.py`

---

### Step 7: Main Application Entry Point
**Goal:** Wire everything together in `run.py` with proper initialization and error handling.

**Method:**
- Update `run.py` to:
  - Check for Python version compatibility
  - Initialize `TerminalUI`
  - Check for existing `~/.pylearn/profile.json`
  - Route to new user registration or returning user authentication
  - Start the `Tutor` session loop
  - Handle graceful exit with progress save
- Add `main()` function as entry point
- Include proper try/except for clean error messages

**Files Updated:**
- `run.py`

---

### Step 8: Documentation & Code Comments
**Goal:** Add comprehensive inline documentation for future developers.

**Method:**
- Add docstrings to all classes and public methods
- Include type hints throughout
- Add module-level docstrings explaining purpose
- Create inline comments for complex logic
- Add a `CONTRIBUTING.md` explaining how to extend the curriculum
- Include "Developer Notes" sections explaining security concepts

**Files Created:**
- `CONTRIBUTING.md`
- Updates to all Python modules

---

### Step 9: Non-Interactive Testing Mode
**Goal:** Enable CLI testing of the app without interactive input.

**Method:**
- Add `--test` flag to `run.py`
- Implement test mode that:
  - Creates a temporary user profile
  - Runs through all lessons programmatically
  - Validates output formatting
  - Reports any errors
- Add `test_runner.py` script for automated validation

**Files Created:**
- `test_runner.py`

---

### Step 10: Curriculum Content - Full Lessons
**Goal:** Write the actual lesson content for all modules.

**Method:**
- Populate `curriculum.py` with full lesson content:
  1. **Welcome & Setup** — Introduction, profile creation with passphrase
  2. **What is Programming?** — Why code matters, thinking like a computer
  3. **Pseudo-code** — Breaking problems into steps, flowcharts
  4. **Python Setup** — Hello World, syntax basics
  5. **Variables & Data Types** — Strings, numbers, booleans
  6. **Operators** — Math, comparison, logical
  7. **Control Flow** — If/else statements
  8. **Loops** — For and while loops
  9. **Functions** — Writing and calling functions
  10. **Mini-project** — Build a simple business calculator (ROI)

**Files Updated:**
- `pylearn/curriculum.py`

---

## 5. TESTING AND VALIDATION

### Success Criteria

1. **Launch Test:** `python run.py` starts without errors and displays welcome message
2. **New User Flow:** First-time user can create profile with name and passphrase, proceed through first lesson
3. **Passphrase Inspection:** User can view `profile.json` and see hashed passphrase (not plain text)
4. **Returning User Flow:** Existing user authenticates with passphrase and resumes from saved progress
5. **Lesson Navigation:** User can progress through all 10 lessons
6. **Answer Recording:** Answers are correctly saved to `answers.json`
7. **Progress Persistence:** Exiting and re-running preserves lesson position
8. **Non-Interactive Mode:** `python test_runner.py` runs without hanging or errors
9. **Terminal Output:** Rich formatting displays correctly (headers, code blocks, colors)

### Validation Commands

```bash
# Interactive testing (manual)
python run.py

# Non-interactive validation
python test_runner.py

# Check progress file
cat ~/.pylearn/progress.json

# Check profile (see hashed passphrase)
cat ~/.pylearn/profile.json
```

### Edge Cases to Test

- Empty passphrase input
- Invalid lesson navigation
- Corrupted `.pylearn` file recovery
- Terminal resize handling
- Rapid input handling
- Permission denied for `.pylearn` directory

---

## 6. FILE STRUCTURE (FINAL)

```
/workspace/project/
├── run.py                      # Entry point
├── requirements.txt            # Dependencies
├── CONTRIBUTING.md             # Developer docs
├── test_runner.py              # Non-interactive test script
└── pylearn/
    ├── __init__.py             # Package init
    ├── auth.py                 # User authentication (educational)
    ├── session.py              # Progress tracking
    ├── ui.py                   # Terminal UI components
    ├── curriculum.py           # Lesson content & structure
    ├── tutor.py                # Conversational engine
    └── config.py               # App configuration
```

---

## 7. ALTERNATIVE CONSIDERATIONS

**Python is the right choice** for this project because:
- Excellent beginner-friendliness with readable syntax
- Rich ecosystem for terminal UI (Rich/Textual/Prompt_toolkit)
- Industry-standard for business analytics and automation
- Large community and learning resources

**Alternative considered: JavaScript/Node.js**
- Would require separate runtime on server
- Less natural for business-focused students (Python is more relevant for data/analytics)
- Not rejected, but Python provides better long-term value for the curriculum

**Alternative considered: Web-based UI (React/Flask)**
- More complex infrastructure
- Loses the "authentic terminal experience" feel
- Good for scale, but adds deployment complexity
- Recommended: Keep terminal-based, add web SSH client separately if needed
