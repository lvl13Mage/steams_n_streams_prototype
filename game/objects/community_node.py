from dataclasses import dataclass
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, registry

from game.objects.node import Node

@dataclass
class CommunityNode(Node, Base):
    __tablename__ = 'community_node'
    id = Column(Integer, primary_key=True)
    community_id = Column(Integer, ForeignKey('community.id'), nullable=True)
    community = relationship('Community', back_populates='community_node', foreign_keys=[community_id], uselist=False)

    def create_new_community_node():
        return CommunityNode()