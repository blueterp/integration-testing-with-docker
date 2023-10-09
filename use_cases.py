from repo_interface import Repo
from user import User

def create_user(user, repo:Repo):
    user_info = user.as_dict()
    repo.create_user(user_info)

def get_user(email:str, repo:Repo):
    user_info = repo.get_user(email)
    return User(**user_info)
