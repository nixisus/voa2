#!/usr/bin/env python3
"""
PyLearn Test Runner

This script provides non-interactive testing of the PyLearn application.
It's designed for automated validation without requiring user input.

Usage:
    python test_runner.py

This will:
    - Create a temporary user profile
    - Run through all lessons programmatically
    - Validate output formatting
    - Report any errors
    - Clean up temporary data

Exit Codes:
    0 - All tests passed
    1 - Test failure(s)
    2 - Setup/installation error
"""

import os
import sys
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch
from io import StringIO


def setup_test_environment():
    """Set up test environment with temporary PyLearn directory."""
    # Create temporary home directory for testing
    test_home = tempfile.mkdtemp()
    
    # Set environment variables to use test home
    os.environ["HOME"] = test_home
    os.environ["PYLEARN_TEST_MODE"] = "1"
    
    return test_home


def cleanup_test_environment(test_home):
    """Clean up test environment."""
    if os.path.exists(test_home):
        shutil.rmtree(test_home)
    os.environ.pop("PYLEARN_TEST_MODE", None)


def mock_input(prompts_and_responses):
    """
    Create a mock input function that returns predefined responses.
    
    Args:
        prompts_and_responses: Dict of prompt substrings to responses
        
    Returns:
        A function that returns appropriate responses
    """
    responses = iter(prompts_and_responses)
    
    def mock_input_func(prompt=""):
        try:
            response = next(responses)
            print(f"INPUT: {response}")
            return response
        except StopIteration:
            return ""
    
    return mock_input_func


def test_curriculum_structure():
    """Test that the curriculum is properly structured."""
    print("\n" + "=" * 50)
    print("TEST: Curriculum Structure")
    print("=" * 50)
    
    from pylearn.curriculum import get_curriculum
    
    curriculum = get_curriculum()
    
    # Check lesson count
    count = curriculum.get_lesson_count()
    print(f"Total lessons: {count}")
    assert count == 10, f"Expected 10 lessons, got {count}"
    
    # Check all lessons have required fields
    for lesson in curriculum.get_all_lessons():
        print(f"  - {lesson.id}: {lesson.title}")
        assert lesson.id, "Lesson missing ID"
        assert lesson.title, "Lesson missing title"
        assert lesson.content, "Lesson missing content"
        assert lesson.next_lesson_id is not None or lesson.id == "mini_project", \
            f"Lesson {lesson.id} missing next_lesson_id"
    
    print("✓ Curriculum structure is valid")
    return True


def test_lesson_navigation():
    """Test that lessons can be navigated correctly."""
    print("\n" + "=" * 50)
    print("TEST: Lesson Navigation")
    print("=" * 50)
    
    from pylearn.curriculum import get_curriculum
    
    curriculum = get_curriculum()
    first = curriculum.get_first_lesson()
    
    print(f"First lesson: {first.id}")
    assert first.id == "welcome", f"Expected first lesson to be 'welcome', got {first.id}"
    
    # Navigate through all lessons
    current = first
    lesson_count = 0
    while current:
        lesson_count += 1
        print(f"  {lesson_count}. {current.title}")
        current = curriculum.get_next_lesson(current.id)
    
    print(f"Total lessons navigated: {lesson_count}")
    assert lesson_count == 10, f"Expected 10 lessons, navigated {lesson_count}"
    
    print("✓ Lesson navigation works correctly")
    return True


def test_user_profile_creation():
    """Test user profile creation with hashed passphrase."""
    print("\n" + "=" * 50)
    print("TEST: User Profile Creation")
    print("=" * 50)
    
    from pylearn.auth import UserProfile, profile_exists
    
    # Create a test profile
    name = "TestUser"
    passphrase = "testpass123"
    
    profile = UserProfile.create_profile(name, passphrase)
    
    print(f"Created profile for: {profile.name}")
    print(f"Hash length: {len(profile.passphrase_hash)}")
    
    # Verify profile was created
    assert profile_exists(), "Profile file was not created"
    assert profile.name == name, "Name not stored correctly"
    
    # Verify passphrase hashing
    assert profile.passphrase_hash != passphrase, "Passphrase not hashed!"
    assert len(profile.passphrase_hash) == 64, "SHA-256 hash should be 64 chars"
    
    # Verify authentication
    assert profile.authenticate(passphrase), "Correct passphrase failed"
    assert not profile.authenticate("wrongpass"), "Wrong passphrase accepted"
    
    print("✓ User profile creation works correctly")
    return True


def test_session_manager():
    """Test session management and progress tracking."""
    print("\n" + "=" * 50)
    print("TEST: Session Manager")
    print("=" * 50)
    
    from pylearn.session import SessionManager, get_session_manager
    
    session = SessionManager()
    
    # Test session start
    session.start_session("TestUser")
    print("Session started")
    
    # Test lesson advancement
    session.advance_lesson("welcome")
    session.advance_lesson("what_is_programming")
    session.advance_lesson("pseudocode")
    
    completed = session.get_completed_lessons()
    print(f"Completed lessons: {completed}")
    assert len(completed) == 3, f"Expected 3 completed, got {len(completed)}"
    
    # Test answer recording
    session.record_answer("welcome", "w1", "B", True)
    session.record_answer("welcome", "w2", "C", False)
    
    answers = session.get_lesson_answers("welcome")
    print(f"Answers recorded: {len(answers)}")
    assert len(answers) == 2, f"Expected 2 answers, got {len(answers)}"
    
    # Test progress calculation
    progress = session.get_progress(total_lessons=10)
    print(f"Progress: {progress * 100:.0f}%")
    assert progress == 0.3, f"Expected 30% progress, got {progress * 100:.0f}%"
    
    print("✓ Session manager works correctly")
    return True


def test_ui_components():
    """Test UI component rendering."""
    print("\n" + "=" * 50)
    print("TEST: UI Components")
    print("=" * 50)
    
    from pylearn.ui import TerminalUI
    from rich.syntax import Syntax
    
    ui = TerminalUI()
    
    # Test code syntax highlighting
    code = 'print("Hello, World!")'
    syntax = Syntax(code, "python", theme="monokai")
    print(f"Syntax object created: {type(syntax).__name__}")
    
    # Test that methods don't raise errors
    try:
        ui.print_header("Test Header")
        ui.print_subheader("Test Subheader")
        ui.print_body("Test body text")
        ui.print_code("x = 1 + 2")
        ui.print_question("Test question?", ["A", "B", "C", "D"])
        ui.print_success("Success!")
        ui.print_error("Error!")
        ui.print_info("Info!")
        ui.print_hint("This is a hint")
        ui.print_encouragement("You can do it!")
        ui.print_divider()
        ui.print_key_points(["Point 1", "Point 2"])
        print("✓ All UI methods executed without errors")
    except Exception as e:
        print(f"✗ UI method failed: {e}")
        return False
    
    print("✓ UI components work correctly")
    return True


def test_authentication_flow():
    """Test the full authentication flow."""
    print("\n" + "=" * 50)
    print("TEST: Authentication Flow")
    print("=" * 50)
    
    from pylearn.auth import UserProfile, profile_exists, UserProfile
    
    # Create profile
    name = "Alice"
    passphrase = "securepass456"
    
    profile = UserProfile.create_profile(name, passphrase)
    print(f"Created profile for {name}")
    
    # Verify profile exists
    assert profile_exists(), "Profile should exist"
    
    # Load profile
    loaded = UserProfile.load()
    assert loaded is not None, "Failed to load profile"
    assert loaded.name == name, "Loaded name doesn't match"
    
    # Verify passphrase
    assert loaded.authenticate(passphrase), "Passphrase verification failed"
    assert not loaded.authenticate("wrong"), "Wrong passphrase accepted"
    
    # Show what the hash looks like
    print(f"\nStored hash (first 32 chars): {loaded.passphrase_hash[:32]}...")
    print("Note: This is a SHA-256 hash, not the actual passphrase!")
    
    print("✓ Authentication flow works correctly")
    return True


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "=" * 60)
    print("  PyLearn Test Suite")
    print("=" * 60)
    
    # Setup
    test_home = setup_test_environment()
    print(f"Test environment: {test_home}")
    
    tests = [
        ("Curriculum Structure", test_curriculum_structure),
        ("Lesson Navigation", test_lesson_navigation),
        ("User Profile Creation", test_user_profile_creation),
        ("Session Manager", test_session_manager),
        ("UI Components", test_ui_components),
        ("Authentication Flow", test_authentication_flow),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed, None))
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"✗ {name} failed: {e}")
    
    # Cleanup
    cleanup_test_environment(test_home)
    
    # Report
    print("\n" + "=" * 60)
    print("  Test Results Summary")
    print("=" * 60)
    
    passed_count = 0
    for name, passed, error in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {status}: {name}")
        if error:
            print(f"         Error: {error}")
        if passed:
            passed_count += 1
    
    print("=" * 60)
    print(f"  {passed_count}/{len(results)} tests passed")
    print("=" * 60)
    
    return passed_count == len(results)


def main():
    """Main entry point."""
    print("PyLearn Test Runner")
    print("=" * 50)
    print("This script tests the PyLearn application without")
    print("requiring interactive user input.\n")
    
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except ImportError as e:
        print(f"\nError: Missing dependency - {e}")
        print("Make sure Rich is installed: pip install rich")
        sys.exit(2)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()