from abc import ABC, abstractmethod


class Repo(ABC):
    @abstractmethod
    def create_user(self, user_info):
        pass

    @abstractmethod
    def get_user(self, user_email):
        pass

    @abstractmethod
    def get_users(self):
        pass
