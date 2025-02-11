from fastapi import Header
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings
from testes.conftest import test_engine

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base class

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# db.py or database.py

"""
from fastapi import Header
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings
from testes.conftest import test_engine

SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocalTest = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)

# Create a declarative base class

def get_db(x_env: str = Header(None)):
    if x_env == "test":
        db = SessionLocalTest()
    else:
        db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# db.py or database.py



"""

