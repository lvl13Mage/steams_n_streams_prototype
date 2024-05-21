from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from database.models import Base

DATABASE_URL = 'mysql+mysqlconnector://bg:bg@localhost:3307/bg'

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()