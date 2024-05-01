import json
from sqlalchemy import TypeDecorator, Text
from dataclasses import dataclass

from buildings.objects.building import Building
from buildings.services.building_game_config import BuildingGameConfig
from resources.objects.resource import ResourceCollection

@dataclass
class TechnologyBuilding(Building):
    building_level: int

    def toJson(self):
        return json.dumps({
            'id': self.id,
            'building_level': self.building_level
        })
    
    def fromJson(resource_json):
        building_data = json.loads(resource_json)
        buildingGameConfig = BuildingGameConfig()
        building = buildingGameConfig.get_building('technology_building', building_data['id'])
        id = building_data['id']
        level = building_data['building_level']
        level_data = building["levels"][str(level)]
        return TechnologyBuilding(
            id=id,
            name=building['name'],
            cost=ResourceCollection.fromJson(level_data['cost']),
            production_time=level_data['production_time'],
            building_level=level
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
            return JSONEncodedTechnologyBuildingList.valueToJsonList(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return JSONEncodedTechnologyBuildingList.valueFromJsonList(value)
        return value
    
    @staticmethod
    def valueToJsonList(value: list[TechnologyBuilding]):
        return json.dumps([building.toJson() for building in value])
    
    @staticmethod
    def valueFromJsonList(value: str):
        buildings_data = json.loads(value)
        buildingList = []
        for building_data in buildings_data:
            buildingGameConfig = BuildingGameConfig()
            building = buildingGameConfig.get_building('technology_building', building_data['id'])
            id = building_data['id']
            level = building_data['building_level']
            level_data = building["levels"][str(level)]
            buildingList.append(TechnologyBuilding(
                id=id,
                name=building['name'],
                cost=ResourceCollection().setResources(**level_data['cost']),
                production_time=level_data['production_time'],
                building_level=level
            ))
        return buildingList