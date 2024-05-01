from dataclasses import dataclass
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData, TypeDecorator, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, registry
import json

from resources.objects.resource import JSONEncodedResourceCollection, ResourceCollection
from buildings.objects.resource_building import JSONEncodedResourceBuildingList
from buildings.objects.production_building import JSONEncodedProductionBuildingList
from buildings.objects.technology_building import JSONEncodedTechnologyBuildingList
from buildings.services.building_game_config import BuildingGameConfig
from buildings.services.building_helper import BuildingHelper

@dataclass
class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    resources = Column(JSONEncodedResourceCollection)
    community_id = Column(Integer, ForeignKey('community.id'))
    community = relationship('Community', back_populates='community', foreign_keys=[community_id], uselist=False)
    world_nodes = Column(Text)
    game_session = Column(Integer)

    # implicit communit node attached to player
    resource_buildings = Column(JSONEncodedResourceBuildingList)
    production_buildings = Column(JSONEncodedProductionBuildingList)
    technology_buildings = Column(JSONEncodedTechnologyBuildingList)

    def create_new_player(communit_id, name):
        return Player(
            name=name,
            resources=ResourceCollection(),
            community_id=communit_id,
            resource_buildings=BuildingHelper.get_initial_buildings('resource_building'),
            production_buildings=BuildingHelper.get_initial_buildings('production_building'),
            technology_buildings=BuildingHelper.get_initial_buildings('technology_building')
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