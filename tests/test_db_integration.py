import pytest
from time import sleep
import os
import subprocess
from sqlalchemy import text, create_engine, select
from sqlalchemy.orm import sessionmaker
# from models import Base, User
from models import mapper_registry, User

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
    # Base.metadata.create_all(engine)
    mapper_registry.metadata.create_all(engine)
    yield engine


@pytest.fixture(scope="function")
def users():
    yield [
        User(name="squidward", fullname="Squidward Tentacles"),
        User(name="ehkrabs", fullname="Eugene H. Krabs"),
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
        session.query(User).delete()
        session.commit()


@pytest.mark.integration
def test_db_initialization(session):
    with session:
        result = session.query(User).all()
        assert len(result) == 2


@pytest.mark.integration
def test_simple_connection(session):
    with session:
        result = session.execute(text("select 'hello world'"))
        assert result.all() == [("hello world",)]


@pytest.mark.integration
def test_add_user(session, users):
    squidward, krabs = [
        User(name="squidward2", fullname="Squidward2 Tentacles"),
        User(name="ehkrabs2", fullname="Eugene2 H. Krabs"),
    ]
    with session:
        session.add(squidward)
        session.add(krabs)
        session.commit()
        result = session.query(User).all()
        print(result)
        for user in result:
            print(user.name)
        print(result)
        assert len(result) == 4


@pytest.mark.integration
def test_dont_commit_add_user(session):
    harry = User(name="harry", fullname="Harry Potter")
    with session:
        session.add(harry)
        session.rollback()
        result = session.execute(select(User).where(User.name == "harry"))

        assert not result.scalars().all()


def test_simple():
    assert True
