"""
Conversational Tutor Engine

This module implements the AI-like conversational interface that guides
students through the curriculum. It provides an encouraging, patient teaching
personality that adapts to student responses.

Design Philosophy:
1. Encouraging - celebrate successes, frame mistakes as learning
2. Patient - allow retries, provide hints when stuck
3. Conversational - use friendly language, personalize interactions
4. Structured - follow the curriculum while allowing some flexibility
"""

from typing import Optional, List
import random

from pylearn.auth import UserProfile, profile_exists, get_current_profile, UserProfile
from pylearn.curriculum import Curriculum, get_curriculum, Lesson, Question, QuestionType
from pylearn.session import SessionManager, get_session_manager
from pylearn.ui import TerminalUI


# Encouraging messages for correct answers
CORRECT_MESSAGES = [
    "Excellent! You've got it!",
    "Perfect! That's exactly right!",
    "Great job! You understand this concept!",
    "Wonderful! You're doing amazing!",
    "That's correct! Keep up the great work!",
    "Exactly right! You're a natural!",
    "Brilliant! You've mastered this!",
]

# Encouraging messages for incorrect answers
INCORRECT_MESSAGES = [
    "Not quite, but that's okay! Let's try again.",
    "That's not it, but don't worry - learning takes practice!",
    "Close! Let me help you understand this better.",
    "That's okay! Mistakes help us learn.",
    "Not to worry - let's work through this together.",
]

# Hint prompts
HINT_PROMPTS = [
    "Need a hint? Type 'hint' for some help.",
    "Stuck? Type 'hint' if you'd like a clue.",
    "Would you like a hint? Just type 'hint'.",
]


class Tutor:
    """
    The main conversational tutor that guides students through the curriculum.
    
    This class orchestrates the learning experience by:
    - Managing the welcome/setup flow for new users
    - Presenting lessons in a conversational manner
    - Evaluating student answers and providing feedback
    - Tracking progress and navigating through the curriculum
    """
    
    def __init__(self, ui: TerminalUI):
        """
        Initialize the tutor with UI components.
        
        Args:
            ui: TerminalUI instance for displaying content
        """
        self.ui = ui
        self.curriculum = get_curriculum()
        self.session = get_session_manager()
        self.user_profile: Optional[UserProfile] = None
        self.current_lesson: Optional[Lesson] = None
    
    def run(self) -> None:
        """Start the interactive tutoring session."""
        self.ui.clear_screen()
        self.ui.print_welcome()
        self.ui.pause()
        
        # Check for existing user
        if profile_exists():
            self._handle_returning_user()
        else:
            self._handle_new_user()
        
        # Start the lesson flow
        self._run_lessons()
        
        # Exit
        self.ui.print_goodbye(self.user_profile.name)
    
    def _handle_new_user(self) -> None:
        """Handle setup for a new user."""
        self.ui.clear_screen()
        self.ui.print_header("Let's get started!")
        
        # Get name
        self.ui.print_body("First, what's your name?")
        name = self.ui.get_input("Your name")
        while not name.strip():
            self.ui.print_error("Please enter your name.")
            name = self.ui.get_input("Your name")
        
        # Explain passphrase concept
        self.ui.print_body(
            f"Nice to meet you, {name}! Next, let's create a passphrase. "
            "A passphrase is like a password, but usually longer and more memorable."
        )
        self.ui.print_tip(
            "In real applications, your passphrase would be stored as a 'hash' - a scrambled version "
            "that can't be reversed. This way, even if someone accesses the file, "
            "they can't easily figure out your actual passphrase. We'll show you this in action!"
        )
        
        # Get passphrase
        self.ui.print_body("Create a passphrase (this is just for learning - not real security):")
        passphrase = self.ui.get_input("Your passphrase")
        while not passphrase.strip():
            self.ui.print_error("Please create a passphrase.")
            passphrase = self.ui.get_input("Your passphrase")
        
        # Create profile
        self.user_profile = UserProfile.create_profile(name, passphrase)
        
        self.ui.print_success(f"Welcome, {name}! Your profile is ready.")
        self.ui.pause()
    
    def _handle_returning_user(self) -> None:
        """Handle authentication for a returning user."""
        self.user_profile = get_current_profile()
        
        if self.user_profile is None:
            self.ui.print_error("Error loading profile. Starting fresh...")
            self._handle_new_user()
            return
        
        self.ui.clear_screen()
        self.ui.print_header(f"Welcome back, {self.user_profile.name}!")
        
        # Educational authentication - explain what's happening
        self.ui.print_body(
            "For this educational app, you don't need a password. "
            "Remember: your profile is stored in ~/.pylearn/profile.json "
            "and contains a HASH of your passphrase, not the actual text!"
        )
        self.ui.print_info("Let's verify by showing you the hash stored in your profile...")
        
        # Show them the hashed version (educational)
        self.ui.print_code(
            f'{{"name": "{self.user_profile.name}", '
            f'"passphrase_hash": "{self.user_profile.passphrase_hash[:32]}...", '
            f'"salt": "pylearn_salt_v1_{self.user_profile.name.lower()}"}}',
            language="json"
        )
        
        self.ui.print_tip(
            "See? The hash is a long string of random characters. Even if someone "
            "sees this, they can't easily reverse it to get your original passphrase."
        )
        
        # Start/resume session
        self.session.start_session(self.user_profile.name)
        self.ui.pause()
    
    def _run_lessons(self) -> None:
        """Run through all lessons in the curriculum."""
        current_id = self.session.get_current_lesson()
        
        # If at welcome (new user), start from first lesson
        if current_id == "welcome":
            current_id = self.curriculum.get_first_lesson().id
            self.session.set_current_lesson(current_id)
        
        while current_id:
            self.current_lesson = self.curriculum.get_lesson(current_id)
            
            if self.current_lesson is None:
                break
            
            self._present_lesson(self.current_lesson)
            
            # Move to next lesson
            next_lesson = self.curriculum.get_next_lesson(current_id)
            if next_lesson:
                current_id = next_lesson.id
                self.session.advance_lesson(current_id)
            else:
                break
    
    def _present_lesson(self, lesson: Lesson) -> None:
        """
        Present a single lesson to the student.
        
        Args:
            lesson: The lesson to present
        """
        self.ui.clear_screen()
        self.ui.print_header(lesson.title)
        self.ui.print_body(lesson.content)
        
        # Show progress
        total = self.curriculum.get_lesson_count()
        completed = self.session.get_completion_count()
        self.ui.print_progress_bar(completed, total, "Course Progress")
        
        if lesson.questions:
            self.ui.print_body(f"This lesson has {len(lesson.questions)} question(s).")
        self.ui.pause()
        
        # Present questions
        for question in lesson.questions:
            self._present_question(question)
        
        # Lesson summary
        self._present_lesson_summary(lesson)
    
    def _present_question(self, question: Question) -> None:
        """
        Present a single question and handle the response.
        
        Args:
            question: The question to present
        """
        self.ui.clear_screen()
        self.ui.print_subheader(f"Question: {question.id}")
        self.ui.print_question(question.text, question.options)
        
        # Show hint prompt
        if question.hint:
            hint_msg = random.choice(HINT_PROMPTS)
            self.ui.print_hint(hint_msg)
        
        # Get answer
        answer = self.ui.get_input("Your answer")
        
        # Handle special commands
        if answer.lower() == 'hint' and question.hint:
            self.ui.print_hint(question.hint)
            answer = self.ui.get_input("Your answer")
        
        if answer.lower() == 'skip':
            self.ui.print_info("Skipping this question.")
            return
        
        # Check answer
        is_correct = question.check_answer(answer)
        
        # Record answer
        self.session.record_answer(
            lesson_id=self.current_lesson.id,
            question_id=question.id,
            answer=answer,
            is_correct=is_correct
        )
        
        # Provide feedback
        if is_correct:
            self.ui.print_success(random.choice(CORRECT_MESSAGES))
        else:
            self.ui.print_encouragement(random.choice(INCORRECT_MESSAGES))
            if question.correct_answer:
                if question.question_type == QuestionType.MULTIPLE_CHOICE and question.options:
                    # Show which option was correct
                    idx = ord(question.correct_answer.upper()) - ord('A')
                    if 0 <= idx < len(question.options):
                        self.ui.print_info(f"The correct answer was: {question.options[idx]}")
                else:
                    self.ui.print_info(f"The correct answer was: {question.correct_answer}")
        
        # Show explanation
        if question.explanation:
            self.ui.print_body(question.explanation)
        
        self.ui.pause()
    
    def _present_lesson_summary(self, lesson: Lesson) -> None:
        """
        Present a summary at the end of a lesson.
        
        Args:
            lesson: The lesson that was just completed
        """
        self.ui.clear_screen()
        self.ui.print_header(f"Summary: {lesson.title}")
        
        self.ui.print_body(f"Great work completing '{lesson.title}'!")
        
        # Show key takeaways based on lesson
        takeaways = self._get_lesson_takeaways(lesson)
        self.ui.print_key_points(takeaways)
        
        # Show updated progress
        total = self.curriculum.get_lesson_count()
        completed = self.session.get_completion_count()
        self.ui.print_progress_bar(completed, total, "Your Progress")
        
        self.ui.pause()
    
    def _get_lesson_takeaways(self, lesson: Lesson) -> List[str]:
        """
        Get key takeaways for a lesson.
        
        Args:
            lesson: The lesson to get takeaways for
            
        Returns:
            List of takeaway strings
        """
        takeaway_map = {
            "welcome": [
                "Programming is a valuable skill for business professionals",
                "You'll build a real business calculator by the end",
                "Learning is incremental - take it one step at a time"
            ],
            "what_is_programming": [
                "Computers follow instructions exactly as written",
                "Programming automates repetitive tasks",
                "Understanding code helps collaboration with tech teams"
            ],
            "pseudocode": [
                "Pseudo-code helps plan before coding",
                "Break complex problems into simple steps",
                "Plain English descriptions reveal the logic"
            ],
            "hello_world": [
                "print() displays output to the screen",
                "Strings are text in quotes",
                "Python syntax is clean and readable"
            ],
            "variables": [
                "Variables store data for later use",
                "Use descriptive names: total_price, not tp",
                "Python variables use snake_case naming"
            ],
            "data_types": [
                "Strings hold text, numbers hold quantities",
                "Booleans represent True/False conditions",
                "Python automatically determines data types"
            ],
            "operators": [
                "Math operators: + - * / // % **",
                "Comparison operators return True or False",
                "Use == to compare, = to assign"
            ],
            "control_flow": [
                "if/else lets code make decisions",
                "elif handles multiple conditions",
                "Indentation defines code blocks in Python"
            ],
            "loops": [
                "for loops repeat a known number of times",
                "while loops repeat until a condition is met",
                "break exits early, continue skips to next iteration"
            ],
            "functions": [
                "Functions are reusable code blocks",
                "def creates a function, return sends back a value",
                "Functions make code organized and testable"
            ],
            "mini_project": [
                "ROI = (Gain - Cost) / Cost × 100",
                "You can combine all concepts learned!",
                "Congratulations on completing PyLearn!"
            ]
        }
        
        return takeaway_map.get(lesson.id, [
            "Practice makes progress!",
            "Review the concepts and try again.",
            "Every expert was once a beginner."
        ])


def create_tutor(ui: TerminalUI) -> Tutor:
    """Factory function to create a Tutor instance."""
    return Tutor(ui)