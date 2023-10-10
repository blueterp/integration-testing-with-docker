import pytest
from sqlalchemy import exc, create_engine, text, select
from sqlalchemy.orm import sessionmaker
from repository.models import User, mapper_registry
from repository.orm_repo import ORMRepo


@pytest.fixture(scope="session")
def url():
    return "sqlite+pysqlite:///:memory:"


@pytest.fixture(scope="function")
def engine(url):
    engine = create_engine(url)
    mapper_registry.metadata.create_all(engine)
    yield engine
    mapper_registry.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def repo(engine):
    return ORMRepo(engine=engine)


@pytest.fixture
def session(engine):
    DBSession = sessionmaker(engine)
    return DBSession()


def test_add_new_user_to_db(repo, session):
    user_info = {"email": "john.doe@domain.com", "fullname": "John Doe"}
    repo.create_user(user_info)
    with session:
        stored_user = session.execute(
            select(User).where(User.email == "john.doe@domain.com")
        )
        assert stored_user.first()[0].email == "john.doe@domain.com"


def test_add_new_user_where_already_exists(session, repo):
    user_info = {"email": "john.doe@domain.com", "fullname": "John Doe"}
    user = User(**user_info)
    with pytest.raises(exc.IntegrityError) as e:
        with session:
            session.add(user)
            session.commit()
        repo.create_user(user_info)


def test_get_user(session, repo):
    with session:
        session.add(User(email="john.doe@domain.com", fullname="John Doe"))
        session.commit()

    user = repo.get_user("john.doe@domain.com")
    assert user == {"email": "john.doe@domain.com", "fullname": "John Doe"}


def test_get_all_users(session, repo):
    users = [
        {"email": "john.doe@domain.com", "fullname": "John Doe"},
        {"email": "jane.doe@domain.com", "fullname": "Jane Doe"},
    ]

    with session:
        [session.add(User(**user)) for user in users]
        session.commit()

    retrieved_users = repo.get_users()
    assert len(retrieved_users) == 2
    for user in retrieved_users:
        del user["id"]
    assert retrieved_users == users


if __name__ == "__main__":
    pytest.main()
