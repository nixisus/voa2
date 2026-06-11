"""
Session Management Module

This module handles tracking student progress through lessons and storing
their answers to exercises. It manages session state persistence across
multiple app invocations.

Key Concepts:
1. Session state - remembering where you are in the curriculum
2. Answer recording - tracking student responses for review
3. Progress calculation - showing how far they've come
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# File paths within ~/.pylearn directory
PYLEARN_DIR = Path.home() / ".pylearn"
PROGRESS_FILE = PYLEARN_DIR / "progress.json"
ANSWERS_FILE = PYLEARN_DIR / "answers.json"


@dataclass
class SessionProgress:
    """
    Tracks the user's progress through the curriculum.
    
    Attributes:
        current_lesson_id: ID of the lesson they're currently on
        completed_lessons: List of completed lesson IDs
        started_at: When the session first began
        last_activity: Timestamp of last activity
    """
    current_lesson_id: str = "welcome"
    completed_lessons: list = field(default_factory=list)
    started_at: str = field(default_factory=lambda: str(os.times().elapsed))
    last_activity: str = field(default_factory=lambda: str(os.times().elapsed))
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "current_lesson_id": self.current_lesson_id,
            "completed_lessons": self.completed_lessons,
            "started_at": self.started_at,
            "last_activity": self.last_activity
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SessionProgress":
        """Create from dictionary."""
        return cls(
            current_lesson_id=data.get("current_lesson_id", "welcome"),
            completed_lessons=data.get("completed_lessons", []),
            started_at=data.get("started_at", "0"),
            last_activity=data.get("last_activity", "0")
        )


@dataclass 
class AnswerRecord:
    """
    Records a student's answer to a question.
    
    Attributes:
        lesson_id: Which lesson this answer belongs to
        question_id: Which specific question
        answer: The student's answer
        is_correct: Whether the answer was correct
        timestamp: When the answer was given
    """
    lesson_id: str
    question_id: str
    answer: str
    is_correct: bool
    timestamp: str = field(default_factory=lambda: str(os.times().elapsed))


class SessionManager:
    """
    Manages the user's learning session, including progress tracking
    and answer recording.
    
    This class handles:
    - Loading and saving progress to progress.json
    - Recording answers to answers.json
    - Tracking which lessons have been completed
    - Calculating progress percentage
    """
    
    def __init__(self):
        """Initialize session manager and load existing progress if available."""
        self._progress: Optional[SessionProgress] = None
        self._answers: list = []
        self._load_data()
    
    def _load_data(self) -> None:
        """Load progress and answers from disk."""
        # Load progress
        if PROGRESS_FILE.exists():
            try:
                with open(PROGRESS_FILE, 'r') as f:
                    self._progress = SessionProgress.from_dict(json.load(f))
            except (json.JSONDecodeError, KeyError):
                self._progress = None
        
        if self._progress is None:
            self._progress = SessionProgress()
        
        # Load answers
        if ANSWERS_FILE.exists():
            try:
                with open(ANSWERS_FILE, 'r') as f:
                    answers_data = json.load(f)
                    self._answers = [
                        AnswerRecord(
                            lesson_id=a["lesson_id"],
                            question_id=a["question_id"],
                            answer=a["answer"],
                            is_correct=a["is_correct"],
                            timestamp=a.get("timestamp", "0")
                        )
                        for a in answers_data
                    ]
            except (json.JSONDecodeError, KeyError):
                self._answers = []
    
    def _save_progress(self) -> None:
        """Save progress to disk."""
        if self._progress is None:
            return
            
        self._progress.last_activity = str(os.times().elapsed)
        
        _ensure_pylearn_dir()
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(self._progress.to_dict(), f, indent=2)
        os.chmod(PROGRESS_FILE, 0o600)
    
    def _save_answers(self) -> None:
        """Save all answers to disk."""
        _ensure_pylearn_dir()
        answers_data = [
            {
                "lesson_id": a.lesson_id,
                "question_id": a.question_id,
                "answer": a.answer,
                "is_correct": a.is_correct,
                "timestamp": a.timestamp
            }
            for a in self._answers
        ]
        with open(ANSWERS_FILE, 'w') as f:
            json.dump(answers_data, f, indent=2)
        os.chmod(ANSWERS_FILE, 0o600)
    
    def start_session(self, user_name: str) -> None:
        """
        Initialize or resume a learning session.
        
        Args:
            user_name: The user's name (used for personalization)
        """
        # If no existing progress, start fresh
        if self._progress is None or self._progress.current_lesson_id == "welcome":
            self._progress = SessionProgress()
        self._save_progress()
    
    def get_current_lesson(self) -> str:
        """
        Get the ID of the current lesson.
        
        Returns:
            The lesson ID the user should continue with
        """
        if self._progress is None:
            return "welcome"
        return self._progress.current_lesson_id
    
    def get_completed_lessons(self) -> list:
        """Get list of completed lesson IDs."""
        if self._progress is None:
            return []
        return self._progress.completed_lessons.copy()
    
    def advance_lesson(self, lesson_id: str) -> None:
        """
        Move to the next lesson.
        
        Args:
            lesson_id: The ID of the lesson to mark as current
        """
        if self._progress is None:
            self._progress = SessionProgress()
        
        # Add to completed if not already there
        if lesson_id not in self._progress.completed_lessons:
            self._progress.completed_lessons.append(lesson_id)
        
        # Set as current
        self._progress.current_lesson_id = lesson_id
        self._save_progress()
    
    def set_current_lesson(self, lesson_id: str) -> None:
        """
        Set the current lesson without marking previous as complete.
        
        Args:
            lesson_id: The ID of the current lesson
        """
        if self._progress is None:
            self._progress = SessionProgress()
        self._progress.current_lesson_id = lesson_id
        self._save_progress()
    
    def record_answer(
        self,
        lesson_id: str,
        question_id: str,
        answer: str,
        is_correct: bool
    ) -> None:
        """
        Record a student's answer to a question.
        
        This stores their response so they can review it later and
        so we can track their understanding.
        
        Args:
            lesson_id: Which lesson the question belongs to
            question_id: Which specific question
            answer: The student's answer
            is_correct: Whether the answer was correct
        """
        record = AnswerRecord(
            lesson_id=lesson_id,
            question_id=question_id,
            answer=answer,
            is_correct=is_correct
        )
        self._answers.append(record)
        self._save_answers()
    
    def get_lesson_answers(self, lesson_id: str) -> list:
        """
        Get all recorded answers for a specific lesson.
        
        Args:
            lesson_id: The lesson to get answers for
            
        Returns:
            List of AnswerRecord objects for that lesson
        """
        return [a for a in self._answers if a.lesson_id == lesson_id]
    
    def get_progress(self, total_lessons: int) -> float:
        """
        Calculate progress as a percentage.
        
        Args:
            total_lessons: Total number of lessons in the curriculum
            
        Returns:
            Progress as a float between 0.0 and 1.0
        """
        if self._progress is None or total_lessons == 0:
            return 0.0
        
        completed = len(self._progress.completed_lessons)
        return completed / total_lessons
    
    def get_completion_count(self) -> int:
        """Get the number of completed lessons."""
        if self._progress is None:
            return 0
        return len(self._progress.completed_lessons)


def _ensure_pylearn_dir() -> None:
    """Ensure the ~/.pylearn directory exists with correct permissions."""
    pylearn_dir = Path.home() / ".pylearn"
    if not pylearn_dir.exists():
        pylearn_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(pylearn_dir, 0o700)


def get_session_manager() -> SessionManager:
    """Get or create a session manager instance."""
    return SessionManager()