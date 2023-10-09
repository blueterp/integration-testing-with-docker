from repo_interface import Repo

class InMemoryRepo(Repo):
    def __init__(self, data=None):
        if not data:
            self.data = dict()
        self.data = data

    def create_user(self, user_info):
        self.data[user_info["email"]] = user_info
        return 

    def get_user(self, user_email):
        return self.data[user_email]
    
    def get_users(self):
        return self.data
    