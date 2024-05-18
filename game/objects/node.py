from dataclasses import dataclass, field
from database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

@dataclass
class Node(Base):
    __tablename__ = 'node'
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    pos_x: Mapped[int] = mapped_column(nullable=False, init=False)
    pos_y: Mapped[int] = mapped_column(nullable=False, init=False)