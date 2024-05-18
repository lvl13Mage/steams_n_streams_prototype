from dataclasses import dataclass, field
from database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

# just for typehinting
if TYPE_CHECKING:
    from game.objects.node import Node

@dataclass
class Edge(Base):
    __tablename__ = 'edge'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    node_id_a: Mapped[int] = mapped_column(ForeignKey('node.id'), nullable=False, init=False)
    node_id_b: Mapped[int] = mapped_column(ForeignKey('node.id'), nullable=False, init=False)
    weight: Mapped[int] = mapped_column(nullable=False, init=False)
    node_a: Mapped['Node'] = relationship('Node', foreign_keys=[node_id_a], init=False)
    node_b: Mapped['Node'] = relationship('Node', foreign_keys=[node_id_b], init=False)
