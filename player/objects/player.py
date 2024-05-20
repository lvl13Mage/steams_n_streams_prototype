from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, String, ForeignKey, Text, TypeDecorator
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.mutable import Mutable
from database.models import Base
import json
import time
from typing import TYPE_CHECKING

from resources.objects.resource import JSONEncodedResourceCollection, ResourceCollection
from buildings.objects.building_list import JSONBuildingListType, BuildingList
from buildings.services.building_helper import BuildingHelper

# just for typehinting
if TYPE_CHECKING:
    from player.objects.community import Community

@dataclass
class Player(Base):
    __tablename__ = 'player'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    community_id: Mapped[int] = mapped_column(ForeignKey('community.id'), init=False)
    community: Mapped['Community'] = relationship(back_populates='community_players')
    resource_buildings: Mapped['BuildingList'] = mapped_column(JSONBuildingListType, default_factory=BuildingList)
    production_buildings: Mapped['BuildingList'] = mapped_column(JSONBuildingListType, default_factory=BuildingList)
    technology_buildings: Mapped['BuildingList'] = mapped_column(JSONBuildingListType, default_factory=BuildingList)
    resources: Mapped['ResourceCollection'] = mapped_column(JSONEncodedResourceCollection, default_factory=ResourceCollection)
    world_nodes: Mapped[str] = mapped_column(Text, default='') 
    game_session: Mapped[int] = mapped_column(default=0)
    last_updated: Mapped[int] = mapped_column(default=0, init=True)

    @staticmethod
    def create_new_player(community, name):
        print('Creating new player...')
        initial_resources = ResourceCollection().setResources(coal=500, water=500, copper=500, aetherum=500)
        last_updated = int(time.time())
        resource_buildings = BuildingHelper.get_initial_buildings('resource_building')
        production_buildings = BuildingHelper.get_initial_buildings('production_building')
        technology_buildings = BuildingHelper.get_initial_buildings('technology_building')
        player = Player(
            name=name,
            community=community,
            resources=initial_resources,
            resource_buildings=resource_buildings,
            production_buildings=production_buildings,
            technology_buildings=technology_buildings,
            last_updated=last_updated
        )
        return player
    
    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'community_id': self.community_id,
            'resources': str(self.resources),  # Convert to string
            'world_nodes': self.world_nodes,
            'game_session': self.game_session,
            'resource_buildings': str(self.resource_buildings),  # Convert to string
            'production_buildings': str(self.production_buildings),  # Convert to string
            'technology_buildings': str(self.technology_buildings)  # Convert to string
        })
    
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