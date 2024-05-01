from dataclasses import dataclass, field
from database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.objects.community_node import CommunityNode
    from player.objects.player import JSONEncodedPlayerList, Player

class Community(Base):
    __tablename__ = 'community'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    #community_node_id: Mapped[int] = mapped_column(ForeignKey('community_node.id'), nullable=True)
    community_node: Mapped['CommunityNode'] = relationship(back_populates='community', init=False)
    community_players: Mapped[list['Player']] = relationship(back_populates='community', init=False)


    def create_new_community():
        return Community()