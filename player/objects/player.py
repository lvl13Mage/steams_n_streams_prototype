from dataclasses import dataclass, field
from sqlalchemy import Column, Integer, String, ForeignKey, Text, TypeDecorator
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
import json
from typing import TYPE_CHECKING

from resources.objects.resource import JSONEncodedResourceCollection, ResourceCollection
from buildings.objects.resource_building import JSONEncodedResourceBuildingList
from buildings.objects.production_building import JSONEncodedProductionBuildingList
from buildings.objects.technology_building import JSONEncodedTechnologyBuildingList
from buildings.services.building_helper import BuildingHelper

if TYPE_CHECKING:
    from player.objects.community import Community

class Player(Base):
    __tablename__ = 'player'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    community_id: Mapped[int] = mapped_column(ForeignKey('community.id'), init=False)
    community: Mapped['Community'] = relationship(back_populates='community_players')
    resources: Mapped[str] = mapped_column(Text, default_factory=JSONEncodedResourceCollection)
    world_nodes: Mapped[str] = mapped_column(Text, default='') 
    game_session: Mapped[int] = mapped_column(default=0)
    resource_buildings: Mapped[str] = mapped_column(Text, default_factory=JSONEncodedResourceBuildingList, repr=False)
    production_buildings: Mapped[str] = mapped_column(Text, default_factory=JSONEncodedResourceBuildingList, repr=False)
    technology_buildings: Mapped[str] = mapped_column(Text, default_factory=JSONEncodedResourceBuildingList, repr=False)

    @staticmethod
    def create_new_player(community, name):
        print('Creating new player...')
        resources = JSONEncodedResourceCollection.valueJson(
            value=ResourceCollection()
        )
        resource_buildings = JSONEncodedResourceBuildingList.valueJsonList(
            value=BuildingHelper.get_initial_buildings('resource_building')
        )
        production_buildings = JSONEncodedProductionBuildingList.valueJsonList(
            value=BuildingHelper.get_initial_buildings('production_building')
        )
        technology_buildings = JSONEncodedTechnologyBuildingList.valueJsonList(
            value=BuildingHelper.get_initial_buildings('technology_building')
        )

        return Player(
            name=name,
            resources=resources,
            community=community,
            resource_buildings=resource_buildings,
            production_buildings=production_buildings,
            technology_buildings=technology_buildings
        )

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