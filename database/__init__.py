from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from database.base import CustomBase

Base = CustomBase

# Setup engine
def setup_database():
    engine = create_engine('mysql+mysqlconnector://bg:bg@localhost:3307/bg', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    ## Import models here to ensure they are known to Base
    from game.objects.community_node import CommunityNode
    from player.objects.player import Player
    from player.objects.community import Community
    from game.objects.node import Node
    from game.objects.edge import Edge
#
    print('Creating tables...')
    Base.metadata.create_all(engine)

    return session

session = setup_database()