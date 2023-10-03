"""User model for simple illustration of ORM"""
from dataclasses import dataclass


@dataclass
class User:
    """Simple User Class"""

    name: str
    fullname: str
    id: int = None
