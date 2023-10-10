from repository.repo_interface import Repo
from repository.models import User
from sqlalchemy.orm import Session
from sqlalchemy import select


class ORMRepo(Repo):
    def __init__(self, engine):
        self.engine = engine

    def create_user(self, user_info):
        session = Session(self.engine)
        user = User(**user_info)
        with session:
            session.add(user)
            session.commit()

    def get_user(self, user_email) -> dict:
        session = Session(self.engine)
        with session:
            res = session.execute(select(User).where(User.email == user_email)).first()[
                0
            ]
            user = {"email": res.email, "fullname": res.fullname}
        return user

    def get_users(self):
        session = Session(self.engine)
        with session:
            res = session.execute(select(User)).mappings()
            users = [user["User"].as_dict() for user in res]

        return users
