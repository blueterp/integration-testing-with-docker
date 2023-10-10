"""User model for simple illustration of ORM"""
from dataclasses import dataclass, asdict


@dataclass
class User:
    """Simple User Class"""

    email: str
    fullname: str
    id: int = None

    def as_dict(self):
        """Converts Domain model to dictionary"""
        return asdict(self)
