"""
User Authentication Module

This module handles user registration and authentication using hashed passphrases.
It serves an educational purpose: demonstrating WHY we hash passwords rather than
storing them in plain text.

Security Concepts Taught:
    1. Plain text passwords are dangerous - if someone accesses the file,
       they have ALL passwords
    2. Hashing is one-way - you can verify a password but can't reverse it
    3. Salting prevents rainbow table attacks (pre-computed hash lookup tables)
    4. Even if someone gets the hash, they can't easily determine the original passphrase

Storage Location:
    User profiles are stored in ~/.pylearn/profile.json with restricted
    permissions (600) to prevent other users on shared servers from accessing data.

Example:
    >>> from pylearn.auth import UserProfile, profile_exists
    >>> # Check if user exists
    >>> if profile_exists():
    ...     profile = UserProfile.load()
    ... else:
    ...     profile = UserProfile.create_profile("Alice", "mypassword123")
    >>> # Authenticate
    >>> profile.authenticate("mypassword123")
    True

Warning:
    This implementation uses SHA-256 for educational purposes.
    Production systems should use bcrypt, scrypt, or argon2.
"""

import hashlib
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# Path to store user data in their home directory
PYLEARN_DIR = Path.home() / ".pylearn"
PROFILE_FILE = PYLEARN_DIR / "profile.json"


def _get_salt(name: str) -> str:
    """
    Generate a salt based on the user's name.
    
    In production systems, salts are randomly generated and stored alongside
    the password hash. Here we use a deterministic salt based on the username
    for educational simplicity - this demonstrates the concept without requiring
    complex random number generation.
    
    Note: Real applications use os.urandom(16) for cryptographically secure salts.
    """
    # Use a fixed prefix + username to create a predictable salt for learning
    return f"pylearn_salt_v1_{name.lower().strip()}"


def _hash_passphrase(passphrase: str, salt: str) -> str:
    """
    Hash a passphrase using SHA-256 with a salt.
    
    This demonstrates the concept of password hashing:
    - Hashing is one-way: can't reverse to get original
    - Salt prevents pre-computed attack tables
    - Same input always produces same output (for verification)
    
    Note: Production systems use bcrypt, scrypt, or argon2 for stronger hashing.
    SHA-256 is used here for educational clarity.
    """
    # Combine salt and passphrase, then hash
    combined = f"{salt}{passphrase}".encode('utf-8')
    return hashlib.sha256(combined).hexdigest()


@dataclass
class UserProfile:
    """
    Represents a user's profile with their name and hashed passphrase.
    
    This class demonstrates secure user management practices:
    - Never stores plain text passphrases
    - Uses hashing for verification
    - Persists data to JSON for portability
    
    Attributes:
        name: The user's display name
        passphrase_hash: The SHA-256 hash of their passphrase (with salt)
        salt: The salt used for hashing (stored for verification)
        created_at: When the profile was created
    """
    name: str
    passphrase_hash: str
    salt: str
    created_at: str = field(default_factory=lambda: str(os.times().elapsed))
    
    def authenticate(self, passphrase: str) -> bool:
        """
        Verify if the provided passphrase matches the stored hash.
        
        This is the core of password verification:
        1. Hash the provided passphrase with the same salt
        2. Compare the result with the stored hash
        3. If they match, the passphrase is correct
        
        Args:
            passphrase: The passphrase to verify
            
        Returns:
            True if passphrase matches, False otherwise
        """
        computed_hash = _hash_passphrase(passphrase, self.salt)
        return computed_hash == self.passphrase_hash
    
    def to_dict(self) -> dict:
        """Convert profile to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "passphrase_hash": self.passphrase_hash,
            "salt": self.salt,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "UserProfile":
        """Create a UserProfile from a dictionary (reverse of to_dict)."""
        return cls(
            name=data["name"],
            passphrase_hash=data["passphrase_hash"],
            salt=data["salt"],
            created_at=data.get("created_at", "0")
        )
    
    def save(self) -> None:
        """
        Save the profile to JSON file.
        
        This writes to ~/.pylearn/profile.json. The file contains the hashed
        passphrase, NOT the plain text version. This is intentional - we want
        students to see that even if someone reads this file, they can't
        easily determine the original passphrase.
        
        Security Note: The directory permissions are set to 0o700 (user-only)
        to prevent other users on the shared server from reading your data.
        """
        _ensure_pylearn_dir()
        
        with open(PROFILE_FILE, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        # Set restrictive permissions (user-only access)
        # This prevents other users on the shared server from accessing your data
        os.chmod(PROFILE_FILE, 0o600)
    
    @classmethod
    def load(cls) -> Optional["UserProfile"]:
        """
        Load an existing profile from JSON file.
        
        Returns:
            UserProfile instance if file exists, None otherwise
        """
        if not PROFILE_FILE.exists():
            return None
        
        try:
            with open(PROFILE_FILE, 'r') as f:
                data = json.load(f)
            return cls.from_dict(data)
        except (json.JSONDecodeError, KeyError):
            # Corrupted profile file
            return None
    
    @classmethod
    def create_profile(cls, name: str, passphrase: str) -> "UserProfile":
        """
        Create a new user profile with hashed passphrase.
        
        This is the registration process:
        1. Take the user's name and passphrase
        2. Generate a salt (using name for educational simplicity)
        3. Hash the passphrase with the salt
        4. Store the name, hash, and salt (NOT the plain passphrase!)
        
        Args:
            name: The user's display name
            passphrase: The passphrase they chose
            
        Returns:
            A new UserProfile instance
        """
        salt = _get_salt(name)
        passphrase_hash = _hash_passphrase(passphrase, salt)
        
        profile = cls(
            name=name,
            passphrase_hash=passphrase_hash,
            salt=salt
        )
        profile.save()
        return profile


def _ensure_pylearn_dir() -> None:
    """
    Ensure the ~/.pylearn directory exists with correct permissions.
    
    This creates the directory if it doesn't exist and sets permissions
    to 0o700 (owner read/write/execute only). This is crucial for
    security on a shared server - it prevents other users from reading
    your learning progress and profile data.
    """
    if not PYLEARN_DIR.exists():
        PYLEARN_DIR.mkdir(parents=True, exist_ok=True)
        # Restrict permissions to user only
        os.chmod(PYLEARN_DIR, 0o700)


def profile_exists() -> bool:
    """Check if a user profile already exists."""
    return PROFILE_FILE.exists()


def get_current_profile() -> Optional[UserProfile]:
    """Load and return the current user profile if it exists."""
    return UserProfile.load()