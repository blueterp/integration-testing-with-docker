import pytest
from in_memory_repo import InMemoryRepo
from user import User
from use_cases import create_user, get_user

@pytest.fixture
def repo():
    return InMemoryRepo()

@pytest.fixture
def user():
    return User("blueterp@gmail.com", "Jonathan Howarth")

def test_create_non_existing_user(repo, user):
    create_user(user, repo)
    assert repo.data.get("blueterp@gmail.com") == user.as_dict()


def test_get_existing_user(repo, user):
    repo.create_user({"email":"blueterp@gmail.com", "fullname":"Jonathan Howarth"})
    assert get_user("blueterp@gmail.com", repo) == user


if __name__ == "__main__":
    pytest.main()