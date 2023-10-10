"""In memory repo that conforms to Repo Interface to demonstrate Repository Pattern"""
from repository.repo_interface import Repo


class InMemoryRepo(Repo):
    """Simple repository where data is stored in memory"""

    def __init__(self, data=None):
        self.data = {} if data is None else data

    def create_user(self, user_info):
        self.data[user_info["email"]] = user_info

    def get_user(self, user_email):
        return self.data[user_email]

    def get_users(self):
        return self.data
