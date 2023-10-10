"""
Use cases (following clean architecture styel) for interacting with domain 
objects and persistent storage
"""

from repository.repo_interface import Repo
from models.user import User


def create_user(user: User, repo: Repo):
    """Create user in database."""
    user_info = user.as_dict()
    repo.create_user(user_info)


def get_user(email: str, repo: Repo):
    """Get user from database."""
    user_info = repo.get_user(email)
    return User(**user_info)
