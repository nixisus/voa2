"""
Curriculum Module

This module defines the structured lesson content for the PyLearn curriculum.
It uses dataclasses to create a type-safe, extensible lesson structure.

Curriculum Structure:
    - Each lesson has an ID, title, content, questions, and a next lesson ID
    - Questions can be multiple choice, free text, or code evaluation
    - The curriculum is designed to be extended by future developers

Lesson Flow:
    welcome -> what_is_programming -> pseudocode -> hello_world ->
    variables -> data_types -> operators -> control_flow -> loops ->
    functions -> mini_project

Extending the Curriculum:
    To add new lessons, create a new Lesson object with:
    1. Unique ID
    2. Title
    3. Content (can include code examples)
    4. Questions list
    5. next_lesson_id (or None for last lesson)

Example:
    >>> from pylearn.curriculum import get_curriculum
    >>> curriculum = get_curriculum()
    >>> lesson = curriculum.get_lesson("variables")
    >>> print(lesson.title)
    'Variables: Storing Information'
    >>> print(f"Questions: {len(lesson.questions)}")
    'Questions: 2'

Note:
    The curriculum uses a global singleton pattern via get_curriculum()
    to ensure the same curriculum instance is used throughout the app.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Callable


class QuestionType(Enum):
    """Types of questions supported in the curriculum."""
    MULTIPLE_CHOICE = "multiple_choice"
    FREE_TEXT = "free_text"
    CODE_COMPLETION = "code_completion"
    CODE_EXPLANATION = "code_explanation"


@dataclass
class Question:
    """
    Represents a question within a lesson.
    
    Attributes:
        id: Unique identifier for this question
        text: The question text
        question_type: Type of question (multiple choice, free text, etc.)
        options: For multiple choice, the available answers
        correct_answer: The correct answer (or correct answer key for verification)
        hint: Optional hint shown if the student is stuck
        explanation: Explanation shown after answering
    """
    id: str
    text: str
    question_type: QuestionType = QuestionType.MULTIPLE_CHOICE
    options: List[str] = field(default_factory=list)
    correct_answer: Optional[str] = None
    hint: Optional[str] = None
    explanation: Optional[str] = None
    
    def check_answer(self, answer: str) -> bool:
        """
        Check if the provided answer is correct.
        
        Args:
            answer: The student's answer
            
        Returns:
            True if correct, False otherwise
        """
        if self.correct_answer is None:
            return False
        
        # Normalize for comparison
        normalized_answer = answer.strip().lower()
        normalized_correct = self.correct_answer.strip().lower()
        
        # For multiple choice, compare the option letter
        if self.question_type == QuestionType.MULTIPLE_CHOICE:
            # Accept either the letter (A, B, C) or the actual text
            if normalized_answer.upper() in ['A', 'B', 'C', 'D']:
                return normalized_answer.upper() == normalized_correct.upper()
        
        return normalized_answer == normalized_correct


@dataclass
class Lesson:
    """
    Represents a single lesson in the curriculum.
    
    Attributes:
        id: Unique identifier for this lesson
        title: The lesson title
        content: Main lesson content (can include code examples)
        questions: List of questions for this lesson
        next_lesson_id: ID of the next lesson (None if this is the last lesson)
        estimated_minutes: How long the lesson typically takes
    """
    id: str
    title: str
    content: str
    questions: List[Question] = field(default_factory=list)
    next_lesson_id: Optional[str] = None
    estimated_minutes: int = 5
    
    def get_question_by_id(self, question_id: str) -> Optional[Question]:
        """Get a specific question by its ID."""
        for q in self.questions:
            if q.id == question_id:
                return q
        return None


class Curriculum:
    """
    Manages the complete curriculum and lesson navigation.
    
    This class provides:
    - Access to lessons by ID
    - Navigation to next/previous lessons
    - Progress tracking helpers
    """
    
    def __init__(self):
        """Initialize the curriculum with all lessons."""
        self._lessons: List[Lesson] = []
        self._lesson_map: dict = {}
        self._build_curriculum()
    
    def _build_curriculum(self) -> None:
        """
        Build the complete curriculum structure.
        
        This method defines all lessons and their relationships.
        Extend this method to add new lessons to the curriculum.
        """
        # Lesson 0: Welcome & Setup
        welcome = Lesson(
            id="welcome",
            title="Welcome to PyLearn",
            content="""Welcome to PyLearn! In this lesson, you'll learn how programming can help your business career and set up your first Python environment.""",
            questions=[
                Question(
                    id="w1",
                    text="Why are business professionals learning to code?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "To replace their jobs with automation",
                        "To better understand and collaborate with technical teams",
                        "To become software engineers",
                        "To avoid working with spreadsheets"
                    ],
                    correct_answer="B",
                    hint="Think about communication and collaboration in modern businesses.",
                    explanation="Business professionals learn coding to communicate better with technical teams, automate repetitive tasks, and make data-driven decisions."
                ),
                Question(
                    id="w2",
                    text="What will you create in this course?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "A social media platform",
                        "A video game",
                        "A business calculator",
                        "A web browser"
                    ],
                    correct_answer="C",
                    hint="Think about practical tools for business decisions.",
                    explanation="You'll build a business calculator that can compute ROI, profit margins, and other useful metrics!"
                )
            ],
            next_lesson_id="what_is_programming",
            estimated_minutes=3
        )
        
        # Lesson 1: What is Programming?
        what_is_programming = Lesson(
            id="what_is_programming",
            title="What is Programming?",
            content="""Programming is the art of telling a computer what to do. Think of it like writing a recipe - you provide step-by-step instructions that someone (or something) follows to achieve a result.

Why should business professionals care?

1. Automation: Computers never get tired of repetitive tasks
2. Data Analysis: Code helps you analyze large datasets quickly
3. Communication: Understanding code helps you work better with technical teams
4. Problem Solving: Programming teaches structured thinking

Computers are literal - they do exactly what you tell them, not what you meant to tell them. This is both a feature and a challenge!""",
            questions=[
                Question(
                    id="p1",
                    text="What does it mean that computers are 'literal'?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "Computers speak other languages",
                        "Computers follow instructions exactly as written, even if the result is unintended",
                        "Computers are very precise in their calculations",
                        "Computers don't use metaphors"
                    ],
                    correct_answer="B",
                    hint="Think about what happens when instructions are ambiguous.",
                    explanation="Computers execute code exactly as written. If your instructions are unclear, the computer will still follow them - leading to unexpected results!"
                ),
                Question(
                    id="p2",
                    text="Which of these is a benefit of learning programming for business?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "You'll become a full-time software developer",
                        "You can automate spreadsheets with thousands of rows",
                        "You won't need to use Excel anymore",
                        "You'll be able to build mobile apps"
                    ],
                    correct_answer="B",
                    hint="Think about repetitive tasks in business.",
                    explanation="Programming excels at automating repetitive tasks. Processing thousands of spreadsheet rows that would take hours manually can be done in seconds with code!"
                )
            ],
            next_lesson_id="pseudocode",
            estimated_minutes=5
        )
        
        # Lesson 2: Pseudo-code
        pseudocode = Lesson(
            id="pseudocode",
            title="Thinking in Pseudo-code",
            content="""Before writing actual code, programmers often use pseudo-code - plain English descriptions of what the code should do.

Pseudo-code helps you:
- Break down complex problems into simple steps
- Plan your code before worrying about syntax
- Share your ideas with non-programmers

Example: Making a cup of coffee

Pseudo-code:
1. Boil water
2. If coffee machine needs filtering:
   - Insert filter
3. Add coffee grounds to filter
4. Pour hot water through machine
5. Wait for coffee to finish brewing
6. Pour coffee into cup

Notice how each step is simple and clear? That's the power of pseudo-code!""",
            questions=[
                Question(
                    id="ps1",
                    text="What is the main purpose of pseudo-code?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "To write code that runs faster",
                        "To plan and structure code before actual implementation",
                        "To replace programming languages",
                        "To make code look more professional"
                    ],
                    correct_answer="B",
                    hint="Think about planning before doing.",
                    explanation="Pseudo-code is a planning tool. It helps you think through the logic before getting caught up in syntax details."
                ),
                Question(
                    id="ps2",
                    text="Convert this to pseudo-code: Calculate the total price including tax",
                    question_type=QuestionType.FREE_TEXT,
                    hint="Think about the steps: get price, get tax rate, calculate tax, add to price.",
                    explanation="Your answer should include: 1) Get the item price, 2) Get the tax rate, 3) Multiply price by tax rate to get tax amount, 4) Add tax to price for total."
                )
            ],
            next_lesson_id="hello_world",
            estimated_minutes=8
        )
        
        # Lesson 3: Hello World
        hello_world = Lesson(
            id="hello_world",
            title="Your First Python Code",
            content="""Time to write your first Python code! In programming, it's tradition to start with "Hello, World!" - a simple program that displays text.

Here's your first Python program:

```python
print("Hello, World!")
```

Let's break it down:
- `print()` is a function that displays output
- The text inside quotes is called a string
- Strings can use single ' or double " quotes

Try it yourself! The console is waiting for you.""",
            questions=[
                Question(
                    id="hw1",
                    text="What does the print() function do?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "Sends a document to a printer",
                        "Displays output on the screen",
                        "Saves data to a file",
                        "Creates a new variable"
                    ],
                    correct_answer="B",
                    hint="Think about what you see when you run a print statement.",
                    explanation="print() displays output to the screen (or console). It's one of the most basic and useful functions in programming!"
                ),
                Question(
                    id="hw2",
                    text="Which of these is a valid Python print statement?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "print(Hello)",
                        "print 'Hello'",
                        "print(\"Hello\")",
                        "print Hello"
                    ],
                    correct_answer="C",
                    hint="Python requires parentheses for function calls.",
                    explanation="In Python, print() requires parentheses and the text must be in quotes. Option C is the correct Python syntax."
                )
            ],
            next_lesson_id="variables",
            estimated_minutes=5
        )
        
        # Lesson 4: Variables
        variables = Lesson(
            id="variables",
            title="Variables: Storing Information",
            content="""Variables are like labeled boxes where you store information. In Python, you create a variable by giving it a name and a value.

```python
# Creating variables
product_name = "Widget Pro"
price = 29.99
quantity = 100
in_stock = True
```

Rules for variable names:
- Must start with a letter or underscore
- Can contain letters, numbers, underscores
- Case-sensitive (price and Price are different)
- Can't use Python keywords (like print, if, for)

Best practices:
- Use descriptive names: `total_price` not `tp`
- Use underscores to separate words: `shipping_cost`
- Be consistent with naming style""",
            questions=[
                Question(
                    id="v1",
                    text="Which variable name follows Python conventions?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "2ndProduct",
                        "product-name",
                        "product_name",
                        "product name"
                    ],
                    correct_answer="C",
                    hint="Think about what characters are allowed in Python variable names.",
                    explanation="Python variables use underscores to separate words (snake_case). They can't start with numbers, contain hyphens, or have spaces."
                ),
                Question(
                    id="v2",
                    text="What type of data does this store? quantity = 42",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "String",
                        "Boolean",
                        "Integer (whole number)",
                        "Float (decimal)"
                    ],
                    correct_answer="C",
                    hint="Is 42 a whole number or a decimal?",
                    explanation="42 is a whole number, making it an integer. Numbers with decimals (like 42.5) are called floats."
                )
            ],
            next_lesson_id="data_types",
            estimated_minutes=8
        )
        
        # Lesson 5: Data Types
        data_types = Lesson(
            id="data_types",
            title="Understanding Data Types",
            content="""Python has several built-in data types. Understanding them helps you work with data correctly.

Common Data Types:

Strings (str): Text data
```python
name = "Acme Corp"
message = 'Hello, World!'
```

Integers (int): Whole numbers
```python
age = 25
year = 2024
```

Floats (float): Decimal numbers
```python
price = 19.99
temperature = 98.6
```

Booleans (bool): True or False
```python
is_active = True
has_discount = False
```

You can check a variable's type with type():
```python
type(price)  # Returns: <class 'float'>
```""",
            questions=[
                Question(
                    id="dt1",
                    text="What data type is the value True?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "String",
                        "Integer",
                        "Boolean",
                        "Float"
                    ],
                    correct_answer="C",
                    hint="Think about yes/no or on/off values.",
                    explanation="True and False are boolean values. They're used for conditions and logical operations."
                ),
                Question(
                    id="dt2",
                    text="What type is '3.14'?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "Integer",
                        "String",
                        "Float",
                        "Boolean"
                    ],
                    correct_answer="C",
                    hint="Does it have a decimal point?",
                    explanation="3.14 has a decimal point, making it a float (floating-point number). Without the decimal, it would be an integer."
                )
            ],
            next_lesson_id="operators",
            estimated_minutes=7
        )
        
        # Lesson 6: Operators
        operators = Lesson(
            id="operators",
            title="Operators: Doing Math and Comparisons",
            content="""Operators let you perform calculations and make comparisons.

Mathematical Operators:
```python
a = 10
b = 3

a + b    # Addition: 13
a - b    # Subtraction: 7
a * b    # Multiplication: 30
a / b    # Division: 3.333...
a // b   # Integer division: 3
a % b    # Modulo (remainder): 1
a ** b   # Power: 1000
```

Comparison Operators (return True or False):
```python
x = 5
y = 10

x == y   # Equal: False
x != y   # Not equal: True
x < y    # Less than: True
x > y    # Greater than: False
x <= y   # Less or equal: True
x >= y   # Greater or equal: False
```

Logical Operators:
```python
True and False   # False
True or False    # True
not True         # False
```""",
            questions=[
                Question(
                    id="op1",
                    text="What is 17 % 5? (The modulo operator returns the remainder)",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "2",
                        "3",
                        "3.4",
                        "12"
                    ],
                    correct_answer="B",
                    hint="Divide 17 by 5. What remainder is left?",
                    explanation="17 ÷ 5 = 3 with remainder 2. So 17 % 5 = 2. Modulo is useful for checking if a number is even/odd!"
                ),
                Question(
                    id="op2",
                    text="What does 8 // 3 return?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "2.66",
                        "2",
                        "3",
                        "2.67"
                    ],
                    correct_answer="B",
                    hint="Integer division ignores the decimal part.",
                    explanation="Integer division (//) returns only the whole number part, discarding any remainder. 8 // 3 = 2 (not 2.66)."
                )
            ],
            next_lesson_id="control_flow",
            estimated_minutes=8
        )
        
        # Lesson 7: Control Flow (If/Else)
        control_flow = Lesson(
            id="control_flow",
            title="Making Decisions: If Statements",
            content="""Control flow lets your program make decisions based on conditions.

If Statements:
```python
temperature = 72

if temperature > 80:
    print("It's hot outside!")
elif temperature > 60:
    print("Nice weather!")
else:
    print("It's cold outside!")
```

Key concepts:
- `if` - checks the first condition
- `elif` - checks additional conditions (optional)
- `else` - runs if no conditions matched (optional)
- Indentation matters! Python uses indentation to define code blocks

Comparison reminder:
- `==` checks equality (is it the same?)
- `=` assigns a value (set it to this)

Common mistake: Using = when you mean ==""",
            questions=[
                Question(
                    id="cf1",
                    text="What will this code print?
x = 5
if x > 10:
    print("Big")
else:
    print("Small")",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "Big",
                        "Small",
                        "Big Small",
                        "Nothing"
                    ],
                    correct_answer="B",
                    hint="Is 5 greater than 10?",
                    explanation="5 is NOT greater than 10, so the first condition is False. The else block runs, printing 'Small'."
                ),
                Question(
                    id="cf2",
                    text="What's wrong with: if x = 10:",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "Nothing, it's correct",
                        "Should be 'if x == 10:'",
                        "x should be capitalized",
                        "Parentheses are required"
                    ],
                    correct_answer="B",
                    hint="What does = do vs == ?",
                    explanation="'=' assigns a value, while '==' checks equality. Using '=' in a condition will assign instead of compare!"
                )
            ],
            next_lesson_id="loops",
            estimated_minutes=10
        )
        
        # Lesson 8: Loops
        loops = Lesson(
            id="loops",
            title="Repeating Actions: Loops",
            content="""Loops let you repeat code multiple times without writing it over and over.

For Loop - when you know how many times to repeat:
```python
# Print numbers 1 to 5
for i in range(1, 6):
    print(i)
```

While Loop - when you don't know in advance:
```python
count = 0
while count < 5:
    print(count)
    count = count + 1
```

Loop control:
- `break` - exit the loop immediately
- `continue` - skip to the next iteration

Example - finding the first product over $100:
```python
prices = [50, 75, 120, 90, 150]
for price in prices:
    if price > 100:
        print(f"Found: ${price}")
        break
```""",
            questions=[
                Question(
                    id="lp1",
                    text="How many times will this loop run?
for i in range(1, 4):
    print(i)",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "2",
                        "3",
                        "4",
                        "Infinite"
                    ],
                    correct_answer="B",
                    hint="range(1, 4) produces: 1, 2, 3",
                    explanation="range(1, 4) generates numbers 1, 2, 3. That's 3 iterations, printing 1, 2, and 3."
                ),
                Question(
                    id="lp2",
                    text="What does the 'break' statement do?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "Pauses the program",
                        "Exits the loop immediately",
                        "Skips the current iteration",
                        "Restarts the loop"
                    ],
                    correct_answer="B",
                    hint="Think about stopping vs skipping.",
                    explanation="'break' exits the loop completely, stopping all further iterations. 'continue' skips only the current iteration."
                )
            ],
            next_lesson_id="functions",
            estimated_minutes=10
        )
        
        # Lesson 9: Functions
        functions = Lesson(
            id="functions",
            title="Functions: Reusable Code Blocks",
            content="""Functions are reusable blocks of code that perform specific tasks.

Defining a function:
```python
def greet(name):
    '''Greet someone by name'''
    print(f"Hello, {name}!")
```

Calling a function:
```python
greet("Alice")  # Prints: Hello, Alice!
greet("Bob")    # Prints: Hello, Bob!
```

Functions can return values:
```python
def calculate_tax(price, rate):
    '''Calculate tax on a price'''
    tax = price * rate
    return tax

total_tax = calculate_tax(100, 0.08)  # Returns 8
```

Why use functions?
1. Avoid repeating code
2. Make code easier to read
3. Easier to test and debug
4. Can be reused in different programs""",
            questions=[
                Question(
                    id="fn1",
                    text="What keyword is used to define a function in Python?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "function",
                        "def",
                        "func",
                        "define"
                    ],
                    correct_answer="B",
                    hint="Think of 'define' shortened.",
                    explanation="'def' is short for 'define'. It's used to create (define) functions in Python."
                ),
                Question(
                    id="fn2",
                    text="What does the 'return' statement do?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "Prints output to the screen",
                        "Exits the function and sends back a value",
                        "Restarts the function",
                        "Pauses the function"
                    ],
                    correct_answer="B",
                    hint="Think about getting a result from a function.",
                    explanation="'return' exits the function and sends a value back to wherever the function was called. Without it, functions return None."
                )
            ],
            next_lesson_id="mini_project",
            estimated_minutes=10
        )
        
        # Lesson 10: Mini Project - Business Calculator
        mini_project = Lesson(
            id="mini_project",
            title="Mini Project: Business Calculator",
            content="""Congratulations! You've made it to the final lesson. Now let's build something useful!

Your challenge: Create a simple ROI (Return on Investment) calculator.

The formula for ROI is:
ROI = (Gain from Investment - Cost of Investment) / Cost of Investment × 100

Example:
- Cost: $1,000
- Gain: $1,200
- ROI = (1200 - 1000) / 1000 × 100 = 20%

Try building this calculator step by step:

```python
# Step 1: Get input
cost = float(input("Enter investment cost: "))
gain = float(input("Enter gain from investment: "))

# Step 2: Calculate ROI
roi = (gain - cost) / cost * 100

# Step 3: Display result
print(f"Your ROI is: {roi}%")
```

Congratulations on completing PyLearn! You've learned the fundamentals of Python programming. Keep practicing!""",
            questions=[
                Question(
                    id="mp1",
                    text="If you invest $500 and get back $750, what's your ROI?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "25%",
                        "50%",
                        "75%",
                        "150%"
                    ],
                    correct_answer="B",
                    hint="ROI = (750 - 500) / 500 × 100",
                    explanation="ROI = (750 - 500) / 500 × 100 = 250 / 500 × 100 = 50%. You made 50% profit on your investment!"
                ),
                Question(
                    id="mp2",
                    text="What did you learn in this course? (Select all that apply)",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options=[
                        "Basic Python syntax and data types",
                        "How to write functions and use loops",
                        "How to make decisions with if/else statements",
                        "All of the above"
                    ],
                    correct_answer="D",
                    hint="Think about all the topics covered.",
                    explanation="You learned all of these! Python basics, variables, data types, operators, control flow, loops, and functions."
                )
            ],
            next_lesson_id=None,  # End of curriculum
            estimated_minutes=15
        )
        
        # Add all lessons to the curriculum
        self._lessons = [
            welcome,
            what_is_programming,
            pseudocode,
            hello_world,
            variables,
            data_types,
            operators,
            control_flow,
            loops,
            functions,
            mini_project
        ]
        
        # Build lookup map
        self._lesson_map = {lesson.id: lesson for lesson in self._lessons}
    
    def get_lesson(self, lesson_id: str) -> Optional[Lesson]:
        """
        Get a lesson by its ID.
        
        Args:
            lesson_id: The unique identifier of the lesson
            
        Returns:
            The Lesson object, or None if not found
        """
        return self._lesson_map.get(lesson_id)
    
    def get_next_lesson(self, current_id: str) -> Optional[Lesson]:
        """
        Get the next lesson after the current one.
        
        Args:
            current_id: The current lesson's ID
            
        Returns:
            The next Lesson, or None if this is the last lesson
        """
        current = self._lesson_map.get(current_id)
        if current and current.next_lesson_id:
            return self._lesson_map.get(current.next_lesson_id)
        return None
    
    def get_first_lesson(self) -> Optional[Lesson]:
        """Get the first lesson in the curriculum."""
        if self._lessons:
            return self._lessons[0]
        return None
    
    def get_lesson_count(self) -> int:
        """Get the total number of lessons."""
        return len(self._lessons)
    
    def get_lesson_index(self, lesson_id: str) -> int:
        """
        Get the index of a lesson (0-based).
        
        Args:
            lesson_id: The lesson ID to find
            
        Returns:
            The lesson's position, or -1 if not found
        """
        for i, lesson in enumerate(self._lessons):
            if lesson.id == lesson_id:
                return i
        return -1
    
    def get_all_lessons(self) -> List[Lesson]:
        """Get all lessons in order."""
        return self._lessons.copy()


# Global curriculum instance
_curriculum = None


def get_curriculum() -> Curriculum:
    """Get the global curriculum instance."""
    global _curriculum
    if _curriculum is None:
        _curriculum = Curriculum()
    return _curriculum