import json
from sqlalchemy import TypeDecorator, Text
from dataclasses import dataclass

from buildings.objects.building import Building
from buildings.services.building_game_config import BuildingGameConfig
from resources.objects.resource import ResourceCollection

@dataclass
class ResourceBuilding(Building):
    building_level: int
    resource_production: ResourceCollection

    def get_production(self, current_time, last_update_time):
        time_delta = (current_time - last_update_time) / 3600
        return self.resource_production * time_delta
    
    def toJson(self):
        return json.dumps({
            'id': self.id,
            'building_level': self.building_level
        })
    
    def fromJson(resource_json):
        building_data = json.loads(resource_json)
        buildingGameConfig = BuildingGameConfig()
        building = buildingGameConfig.get_building('resource_building', building_data['id'])
        id = building_data['id']
        level = building_data['building_level']
        level_data = building["levels"][str(level)]
        return ResourceBuilding(
            id=id,
            name=building['name'],
            cost=ResourceCollection().setResources(**level_data['cost']),
            production_time=level_data['production_time'],
            building_level=level,
            resource_production=ResourceCollection().setResources(**level_data['production'])
        )
    
class JSONEncodedResourceBuilding(TypeDecorator):
    impl = Text

    def process_bind_param(self, value: ResourceBuilding, dialect):
        return value.toJson()

    def process_result_value(self, value, dialect):
        return ResourceBuilding.fromJson(value)
    
class JSONEncodedResourceBuildingList(TypeDecorator):
    impl = Text

    def process_bind_param(self, value: list[ResourceBuilding], dialect):
        if value is not None:
            return JSONEncodedResourceBuildingList.valueToJsonList(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return JSONEncodedResourceBuildingList.valueFromJsonList(value)
        return value
    
    @staticmethod
    def valueToJsonList(value: list[ResourceBuilding]):
        return json.dumps([building.toJson() for building in value])
    
    @staticmethod
    def valueFromJsonList(value):
        buildings_data = json.loads(value)
        return [ResourceBuilding.fromJson(building) for building in buildings_data]