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
    production_start_time: int

    def get_production(self, time_difference):
        time_delta = time_difference / 3600
        return self.resource_production * time_delta

    def toJson(self):
        return json.dumps({
            'id': self.id,
            'building_level': self.building_level,
            'production_start_time': self.production_start_time
        })
    
    def fromJson(resource_json):
        building_data = json.loads(resource_json)
        buildingGameConfig = BuildingGameConfig()
        building = buildingGameConfig.get_building('resource_building', building_data['id'])
        id = building_data['id']
        level = building_data['building_level']
        level_data = building["levels"][str(level)]
        cost = ResourceCollection().setResources(**buildingGameConfig.get_building('resource_building', id)['levels'][str(level+1)]['cost']) if str(level+1) in building['levels'] else None
        return ResourceBuilding(
            id=id,
            name=building['name'],
            cost=cost,
            production_time=level_data['production_time'],
            building_level=level,
            resource_production=ResourceCollection().setResources(**level_data['production']),
            production_start_time=building_data['production_start_time']
        )
    
class JSONEncodedResourceBuilding(TypeDecorator):
    impl = Text

    def process_bind_param(self, value: ResourceBuilding, dialect):
        return value.toJson()

    def process_result_value(self, value, dialect):
        return ResourceBuilding.fromJson(value)