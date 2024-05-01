from dataclasses import dataclass, field
from database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

from game.objects.node import Node

# just for typehinting
if TYPE_CHECKING:
    from player.objects.community import Community

class CommunityNode(Node, Base):
    __tablename__ = 'community_node'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    community_id: Mapped[int] = mapped_column(ForeignKey('community.id'), nullable=True, init=False)
    community: Mapped['Community'] = relationship(back_populates='community_node', init=False)

    @staticmethod
    def create_new_community_node():
        return CommunityNode()
    
    def setCommunity(self, community_id):
        self.community_id = community_id