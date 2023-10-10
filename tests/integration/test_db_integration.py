import pytest
from time import sleep
import os
import subprocess
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from repository.orm_repo import ORMRepo, User as DBUser
from use_cases.use_cases import create_user, get_user
from models.user import User
from repository.models import mapper_registry


def wait_for_logs(command, message):
    try:
        logs = subprocess.run(command.split(" "), cwd=os.getcwd(), capture_output=True)
        return message in logs.stdout.decode("utf-8")
    except Exception as e:
        return False


@pytest.fixture(scope="session")
def db_service(docker_services, docker_ip):
    """Ensure that database service is up and responsive."""
    port = docker_services.port_for("postgres_db", 5432)
    host = docker_ip
    docker_services.wait_until_responsive(
        timeout=10.0,
        pause=0.1,
        check=lambda: wait_for_logs(
            "docker container logs PostgresCont",
            "database system is ready to accept connections",
        ),
    )
    sleep(0.5)
    return f"{host}:{port}"


@pytest.fixture(scope="session")
def engine(db_service):
    engine = create_engine(
        f"postgresql+psycopg2://postgres:postgres123@{db_service}/postgres"
    )
    mapper_registry.metadata.create_all(engine)
    yield engine


@pytest.fixture(scope="function")
def users():
    yield [
        DBUser(email="squidward@gmail.com", fullname="Squidward Tentacles"),
        DBUser(email="ehkrabs@gmail.com", fullname="Eugene H. Krabs"),
    ]


@pytest.fixture(scope="function")
def session(engine, users):
    DBsession = sessionmaker(engine)
    session = DBsession()
    with session:
        session.bulk_save_objects(users)
        session.commit()
    yield session
    with session:
        session.query(DBUser).delete()
        session.commit()


@pytest.fixture(scope="session")
def repo(engine):
    return ORMRepo(engine)


@pytest.mark.integration
def test_add_user(session, repo):
    squidward, krabs = [
        {"email": "squidward2@gmail.com", "fullname": "Squidward2 Tentacles"},
        {"email": "ehkrabs2@gmail.com", "fullname": "Eugene2 H. Krabs"},
    ]
    create_user(User(**squidward), repo)
    create_user(User(**krabs), repo)
    with session:
        result = session.query(DBUser).all()
        assert len(result) == 4


@pytest.mark.integration
def test_get_user(repo, session):
    harry = DBUser(email="harry@gmail.com", fullname="Harry Potter")
    with session:
        session.add(harry)
        session.commit()

    user = get_user("harry@gmail.com", repo)
    assert user == User(**{"email": "harry@gmail.com", "fullname": "Harry Potter"})
