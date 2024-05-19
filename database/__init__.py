from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from database.models import Base

# Setup engine
def setup_database():
    engine = create_engine('mysql+mysqlconnector://bg:bg@localhost:3307/bg', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
#
    print('Creating tables...')
    Base.metadata.create_all(engine)

    return session

session = setup_database()