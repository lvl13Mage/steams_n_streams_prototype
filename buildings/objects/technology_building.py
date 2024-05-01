import json
from sqlalchemy import TypeDecorator, Text
from dataclasses import dataclass

from buildings.objects.building import Building
from buildings.services.building_game_config import BuildingGameConfig
from resources.objects.resource import ResourceCollection

@dataclass
class TechnologyBuilding(Building):

    def toJson(self):
        return json.dumps({
            'id': self.id,
            'building_level': self.building_level
        })
    
    def fromJson(json):
        building_data = json.loads(json)
        building = BuildingGameConfig.get_building('technology_building', building_data['id'])
        id = building_data['id']
        level = building_data['building_level']
        level_data = building["level"][level]
        return TechnologyBuilding(
            id,
            building['name'],
            ResourceCollection.fromJson(level_data['cost']),
            level_data['production_time'],
            level
        )
    
class JSONEncodedTechnologyBuilding(TypeDecorator):
    impl = Text

    def process_bind_param(self, value: TechnologyBuilding, dialect):
        return value.toJson()

    def process_result_value(self, value, dialect):
        return TechnologyBuilding.fromJson(value)

class JSONEncodedTechnologyBuildingList(TypeDecorator):
    impl = Text

    def process_bind_param(self, value: list[TechnologyBuilding], dialect):
        if value is not None:
            return self.valueJsonList(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return self.valueFromJsonList(value)
        return value
    
    def valueJsonList(value: list[TechnologyBuilding]):
        return json.dumps([building.toJson() for building in value])
    
    def valueFromJsonList(value: str):
        buildings_data = json.loads(value)
        return [TechnologyBuilding.fromJson(building) for building in buildings_data]