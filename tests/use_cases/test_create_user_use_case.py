"""Unit tests for use cases"""

import pytest
from repository.in_memory_repo import InMemoryRepo
from models.user import User
from use_cases.use_cases import create_user, get_user


@pytest.fixture(name="repo")
def fixture_repo():
    """Provides fake repo that complies with repo interface"""
    return InMemoryRepo()


@pytest.fixture(name="user")
def fixture_user():
    """Provides single user for use in testing use cases"""
    return User("blueterp@gmail.com", "Jonathan Howarth")


def test_create_non_existing_user(repo, user):
    """Verifies use case persists user in fake repo"""
    create_user(user, repo)
    assert repo.data.get("blueterp@gmail.com") == user.as_dict()


def test_get_existing_user(repo, user):
    """Verifies get user use case returns a user"""
    repo.create_user({"email": "blueterp@gmail.com", "fullname": "Jonathan Howarth"})
    assert get_user("blueterp@gmail.com", repo) == user


if __name__ == "__main__":
    pytest.main()
