"""Interface for Repository Pattern Usage."""
from abc import ABC, abstractmethod
from typing import List


class Repo(ABC):
    """Abstract Interface. Methods must be implemented."""

    @abstractmethod
    def create_user(self, user_info):
        """Create a user and persist in database."""

    @abstractmethod
    def get_user(self, user_email) -> dict:
        """Get persisted user from database."""

    @abstractmethod
    def get_users(self) -> List[dict]:
        """Get all persisted users from database."""
