from sqlalchemy.ext.declarative import declarative_base
from database.base import CustomBase

Base = CustomBase

# Import all your models here
from game.objects.community_node import CommunityNode
from player.objects.player import Player
from player.objects.community import Community
from game.objects.node import Node
from game.objects.edge import Edge

__all__ = [
    "Base",
    "CommunityNode",
    "Player",
    "Community",
    "Node",
    "Edge",
]
