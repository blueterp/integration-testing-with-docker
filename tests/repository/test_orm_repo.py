"""Unit tests for ORM repo that complies with repo interface"""

import pytest
from sqlalchemy import exc, create_engine, select
from sqlalchemy.orm import sessionmaker
from repository.models import User, mapper_registry
from repository.orm_repo import ORMRepo


@pytest.fixture(scope="session", name="url")
def fixture_url():
    """Single point for configuring url to SQLAlchemy engine"""
    return "sqlite+pysqlite:///:memory:"


@pytest.fixture(scope="function", name="engine")
def fixture_engine(url):
    """Creates and drops tables, provides engine for connecting to SQLAlchemy DB"""
    engine = create_engine(url)
    mapper_registry.metadata.create_all(engine)
    yield engine
    mapper_registry.metadata.drop_all(engine)


@pytest.fixture(scope="function", name="repo")
def fixture_repo(engine):
    """SQLAlchemy repository that complies with repository interface"""
    return ORMRepo(engine=engine)


@pytest.fixture(name="session")
def fixture_session(engine):
    """Fixture for making single session connecting to DB"""
    DBSession = sessionmaker(engine)
    return DBSession()


def test_add_new_user_to_db(repo, session):
    """Verifies added user is persisted"""
    user_info = {"email": "john.doe@domain.com", "fullname": "John Doe"}
    repo.create_user(user_info)
    with session:
        stored_user = session.execute(
            select(User).where(User.email == "john.doe@domain.com")
        )
        assert stored_user.first()[0].email == "john.doe@domain.com"


def test_add_new_user_where_already_exists(session, repo):
    """Verifies added user does not persist if email is not unique"""
    user_info = {"email": "john.doe@domain.com", "fullname": "John Doe"}
    user = User(**user_info)
    with pytest.raises(exc.IntegrityError):
        with session:
            session.add(user)
            session.commit()
        repo.create_user(user_info)


def test_get_user(session, repo):
    """Verifies retreval of user"""
    with session:
        session.add(User(email="john.doe@domain.com", fullname="John Doe"))
        session.commit()

    user = repo.get_user("john.doe@domain.com")
    assert user == {"email": "john.doe@domain.com", "fullname": "John Doe"}


def test_get_all_users(session, repo):
    """Verifies retreval of all users"""
    users = [
        {"email": "john.doe@domain.com", "fullname": "John Doe"},
        {"email": "jane.doe@domain.com", "fullname": "Jane Doe"},
    ]

    with session:
        _ = [session.add(User(**user)) for user in users]
        session.commit()

    retrieved_users = repo.get_users()
    assert len(retrieved_users) == 2
    for user in retrieved_users:
        del user["id"]
    assert retrieved_users == users


if __name__ == "__main__":
    pytest.main()
