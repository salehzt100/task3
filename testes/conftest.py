from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import pytest
from fastapi.testclient import  TestClient

from app.models import Base
from core import settings
from main import app

SQLALCHEMY_TEST_DATABASE_URL = settings.SQLALCHEMY_TEST_DATABASE_URI


test_engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)


@pytest.fixture(scope="session")
def tables():
    Base.metadata.create_all(test_engine)
    yield
    # Drop all tables with cascade to avoid foreign key constraints issue
    Base.metadata.drop_all(test_engine)
    with test_engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS roles CASCADE"))
        conn.commit()

@pytest.fixture
def get_test_db(tables):
    """Returns a sqlalchemy session, and after the test tears down everything properly."""
    connection = test_engine.connect()
    transaction = connection.begin()  # Start transaction
    session = Session(bind=connection)

    try:
        yield session
    finally:
        session.rollback()  # Ensure rollback
        connection.close()



def test_database_connection(get_test_db):
    session = get_test_db  # Get the test session from fixture
    try:
        result = session.execute(text("SELECT * FROM users"))  # Wrap query in text()

        print(result.fetchall())
        assert result  # Check if the query returns 1
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")
@pytest.fixture
def t_client():
    # app.dependency_overrides[get_db] = get_test_db
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mzg3ODYxMDEsInN1YiI6Im11amFkaWQifQ.i3NErCsBbzUkV4ZQq3mJ_XgtKJiszx45uui6eD4TgXQ"
    yield TestClient(app, headers={"Authorization": f"Bearer {token}"})





# from typing import Generator
#
# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from core.config import settings
#
# # A separate TEST DB URI
# SQLALCHEMY_TEST_DATABASE_URL = settings.SQLALCHEMY_TEST_DATABASE_URI
#
# # Create a new engine for the test database
# engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
#
# # Create a test SessionLocal
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# @pytest.fixture(scope="function")
# def get_test_db():
#     """
#     Create a new database session for each test and roll it back after the test.
#     """
#     connection = engine.connect()
#     transaction = connection.begin()
#     session = TestingSessionLocal(bind=connection)
#
#     yield session
#
#     session.close()
#     transaction.rollback()
#     connection.close()
#
