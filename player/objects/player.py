from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, String, ForeignKey, Text, TypeDecorator
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
import json
from typing import TYPE_CHECKING

from resources.objects.resource import JSONEncodedResourceCollection, ResourceCollection
from buildings.objects.building_list import JSONBuildingListType, BuildingList
from buildings.services.building_helper import BuildingHelper

# just for typehinting
if TYPE_CHECKING:
    from player.objects.community import Community

class Player(Base):
    __tablename__ = 'player'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    community_id: Mapped[int] = mapped_column(ForeignKey('community.id'), init=False)
    community: Mapped['Community'] = relationship(back_populates='community_players')
    resources: Mapped['ResourceCollection'] = mapped_column(JSONEncodedResourceCollection)
    resource_buildings: Mapped['BuildingList'] = mapped_column(JSONBuildingListType, repr=False)
    production_buildings: Mapped['BuildingList'] = mapped_column(JSONBuildingListType, repr=False)
    technology_buildings: Mapped['BuildingList'] = mapped_column(JSONBuildingListType, repr=False)
    world_nodes: Mapped[str] = mapped_column(Text, default='') 
    game_session: Mapped[int] = mapped_column(default=0)

    @staticmethod
    def create_new_player(community, name):
        print('Creating new player...')
        resources = ResourceCollection()
        resource_buildings = BuildingHelper.get_initial_buildings('resource_building')
        production_buildings = BuildingHelper.get_initial_buildings('production_building')
        technology_buildings = BuildingHelper.get_initial_buildings('technology_building')
        return Player(
            name=name,
            resources=resources,
            community=community,
            resource_buildings=resource_buildings,
            production_buildings=production_buildings,
            technology_buildings=technology_buildings
        )
    
    def __repr__(self):
        return {
            'id': self.id,
            'name': self.name,
            'community_id': self.community_id,
            'resources': self.resources,
            'world_nodes': self.world_nodes,
            'game_session': self.game_session,
            'resource_buildings': self.resource_buildings,
            'production_buildings': self.production_buildings,
            'technology_buildings': self.technology_buildings
        }

# typedecorator to return list of players consisting of ids
class JSONEncodedPlayerList(TypeDecorator):
    impl = Text

    def process_bind_param(self, value: list[Player], dialect):
        if value is not None:
            return json.dumps([player.id for player in value])
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            player_ids = json.loads(value)
            return [Player(id=id) for id in player_ids]
        return value