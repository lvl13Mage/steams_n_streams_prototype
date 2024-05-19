from dataclasses import dataclass, field
from database.models import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

# just for typehinting
if TYPE_CHECKING:
    from player.objects.community import Community
    from game.objects.node import Node

@dataclass
class CommunityNode(Base):
    __tablename__ = 'community_node'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    #pos_x: Mapped[int] = mapped_column(nullable=False, init=True)
    #pos_y: Mapped[int] = mapped_column(nullable=False, init=True)
    node_id: Mapped[int] = mapped_column(ForeignKey('node.id'), nullable=False, init=False)
    node: Mapped['Node'] = relationship(init=False)
    map_id: Mapped[int] = mapped_column(nullable=False, init=False)
    community_id: Mapped[int] = mapped_column(ForeignKey('community.id'), nullable=True, init=False)
    community: Mapped['Community'] = relationship(back_populates='community_node', init=False)

    @staticmethod
    def create_new_community_node():
        return CommunityNode()
    
    def setCommunity(self, community_id):
        self.community_id = community_id