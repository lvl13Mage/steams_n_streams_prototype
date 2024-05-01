from dataclasses import dataclass
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, registry

from player.objects.player import JSONEncodedPlayerList

@dataclass
class Community(Base):
    __tablename__ = 'community'
    id = Column(Integer, primary_key=True)
    community_node_id = Column(Integer, ForeignKey('community_node.id'))
    community_node = relationship('CommunityNode', back_populates='community', foreign_keys=[community_node_id], uselist=False)
    community_players = Column(JSONEncodedPlayerList)

    def create_new_community(communit_node_id):
        return Community(
            community_node_id=communit_node_id,
            community_players=[]
        )