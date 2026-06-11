"""
Terminal UI Components Module

This module provides beautiful, accessible terminal output using the Rich library.
It creates a consistent visual language for the learning application.

Design Principles:
1. Clear hierarchy - headers, body text, and code are visually distinct
2. Accessibility - high contrast colors, readable fonts
3. Encouragement - positive messaging, gentle corrections
4. Engagement - progress bars, visual feedback
"""

from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.text import Text


class TerminalUI:
    """
    Provides consistent, beautiful terminal output for the learning app.
    
    This class wraps Rich console functionality to create a unified
    visual experience with:
    - Styled headers and panels
    - Syntax-highlighted code blocks
    - Progress indicators
    - Encouraging feedback messages
    """
    
    def __init__(self):
        """Initialize the Rich console for styled output."""
        self.console = Console()
    
    def clear_screen(self) -> None:
        """Clear the terminal screen for a fresh lesson."""
        self.console.clear()
    
    def print_header(self, text: str) -> None:
        """
        Print a styled section header.
        
        Args:
            text: The header text to display
        """
        panel = Panel(
            text,
            title="[bold cyan]PyLearn[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        )
        self.console.print(panel)
    
    def print_subheader(self, text: str) -> None:
        """
        Print a smaller subheader for lesson titles.
        
        Args:
            text: The subheader text
        """
        self.console.print(f"\n[bold bright_cyan]{text}[/bold bright_cyan]")
    
    def print_body(self, text: str, width: Optional[int] = None) -> None:
        """
        Print standard body text with word wrap.
        
        Args:
            text: The text to display
            width: Optional width for wrapping (defaults to terminal width)
        """
        if width is None:
            width = min(self.console.width - 4, 80)
        
        self.console.print(f"\n{text}\n")
    
    def print_code(self, code: str, language: str = "python") -> None:
        """
        Print syntax-highlighted code block.
        
        Args:
            code: The code to display
            language: The programming language for syntax highlighting
        """
        syntax = Syntax(code, language, theme="monokai", padding=(1, 2))
        self.console.print(syntax)
    
    def print_code_with_output(self, code: str, output: str) -> None:
        """
        Print code block followed by its output.
        
        Args:
            code: The code to display
            output: The expected output
        """
        syntax = Syntax(code, "python", theme="monokai", padding=(1, 2))
        self.console.print(syntax)
        if output:
            self.console.print(f"[dim]Output:[/dim] {output}")
    
    def print_question(
        self,
        question: str,
        options: Optional[List[str]] = None
    ) -> None:
        """
        Print a question with optional multiple choice options.
        
        Args:
            question: The question text
            options: Optional list of choices (will be lettered A, B, C...)
        """
        self.console.print(f"\n[bold yellow]? {question}[/bold yellow]\n")
        
        if options:
            for i, option in enumerate(options):
                letter = chr(65 + i)  # A, B, C, D...
                self.console.print(f"  [cyan]{letter}.[/cyan] {option}")
    
    def print_success(self, message: str) -> None:
        """
        Print a success/encouragement message in green.
        
        Args:
            message: The success message to display
        """
        self.console.print(f"[bold green]✓ {message}[/bold green]\n")
    
    def print_error(self, message: str) -> None:
        """
        Print an error message in red.
        
        Args:
            message: The error message to display
        """
        self.console.print(f"[bold red]✗ {message}[/bold red]\n")
    
    def print_info(self, message: str) -> None:
        """
        Print an informational message in blue.
        
        Args:
            message: The info message to display
        """
        self.console.print(f"[bold blue]ℹ {message}[/bold blue]\n")
    
    def print_hint(self, message: str) -> None:
        """
        Print a helpful hint in dim yellow.
        
        Args:
            message: The hint to display
        """
        self.console.print(f"[dim yellow]💡 Hint: {message}[/dim yellow]\n")
    
    def print_encouragement(self, message: str) -> None:
        """
        Print an encouraging message.
        
        Args:
            message: The encouragement to display
        """
        self.console.print(f"[bold magenta]{message}[/bold magenta]\n")
    
    def print_progress_bar(self, current: int, total: int, label: str = "Progress") -> None:
        """
        Print a visual progress bar.
        
        Args:
            current: Current progress value
            total: Total value (100%)
            label: Optional label for the progress bar
        """
        with Progress(
            TextColumn("[bold blue]{task.description}[/bold blue]"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            task = progress.add_task(label, total=total)
            progress.update(task, completed=current)
    
    def print_menu(self, options: List[str], title: str = "Menu") -> None:
        """
        Print a numbered menu of options.
        
        Args:
            options: List of option strings
            title: Optional title for the menu
        """
        self.console.print(f"\n[bold cyan]{title}:[/bold cyan]\n")
        for i, option in enumerate(options, 1):
            self.console.print(f"  [cyan]{i}.[/cyan] {option}")
    
    def pause(self, message: str = "Press Enter to continue...") -> None:
        """
        Pause and wait for user to press Enter.
        
        Args:
            message: The prompt to display
        """
        self.console.print(f"\n[dim]{message}[/dim]")
        input()
    
    def get_input(self, prompt: str = "> ") -> str:
        """
        Get input from the user.
        
        Args:
            prompt: The input prompt to display
            
        Returns:
            The user's input string
        """
        return input(prompt).strip()
    
    def get_choice(self, prompt: str, valid_choices: List[str]) -> str:
        """
        Get a single character choice from the user.
        
        Args:
            prompt: The prompt to display
            valid_choices: List of valid single-character choices
            
        Returns:
            The user's chosen character (uppercased)
        """
        valid_str = "/".join(v.upper() for v in valid_choices)
        while True:
            response = input(f"{prompt} ({valid_str}): ").strip().upper()
            if response in [c.upper() for c in valid_choices]:
                return response
            self.print_error(f"Please enter one of: {valid_str}")
    
    def print_divider(self) -> None:
        """Print a visual divider line."""
        self.console.print("\n" + "─" * 50 + "\n")
    
    def print_key_points(self, points: List[str]) -> None:
        """
        Print key points in a bulleted format.
        
        Args:
            points: List of key points to display
        """
        self.console.print("\n[bold]Key Points:[/bold]\n")
        for point in points:
            self.console.print(f"  [cyan]•[/cyan] {point}")
        self.console.print()
    
    def print_tip(self, tip: str) -> None:
        """
        Print a tip in a styled box.
        
        Args:
            tip: The tip text to display
        """
        panel = Panel(
            tip,
            title="[bold yellow]💡 Pro Tip[/bold yellow]",
            border_style="yellow",
            padding=(1, 2)
        )
        self.console.print(panel)
    
    def print_welcome(self) -> None:
        """Print the welcome banner."""
        welcome_text = """
[bold cyan]Welcome to PyLearn![/bold cyan]

Your interactive journey to learning Python programming.

I'll guide you through:
  • Python basics and syntax
  • How to think like a programmer
  • Real business applications

Don't worry if you've never coded before - we'll go step by step!
"""
        self.console.print(welcome_text)
    
    def print_goodbye(self, user_name: str) -> None:
        """
        Print a farewell message.
        
        Args:
            user_name: The user's name for personalization
        """
        goodbye = f"""
[bold cyan]Great work today, {user_name}![/bold cyan]

Your progress has been saved. When you return, you can pick up
right where you left off.

Keep practicing, and remember: every expert was once a beginner!
"""
        self.console.print(goodbye)