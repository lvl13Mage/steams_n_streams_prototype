from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import Mutable
from database.base import CustomBase
from buildings.objects.building_list import JSONBuildingListType, BuildingList
from resources.objects.resource import JSONEncodedResourceCollection, ResourceCollection

BuildingList.associate_with(JSONBuildingListType)
ResourceCollection.associate_with(JSONEncodedResourceCollection)

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
