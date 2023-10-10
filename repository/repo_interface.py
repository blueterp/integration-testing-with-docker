from abc import ABC, abstractmethod
from typing import List


class Repo(ABC):
    @abstractmethod
    def create_user(self, user_info):
        pass

    @abstractmethod
    def get_user(self, user_email) -> dict:
        pass

    @abstractmethod
    def get_users(self) -> List[dict]:
        pass
