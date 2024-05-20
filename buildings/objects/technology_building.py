import json
from sqlalchemy import TypeDecorator, Text
from dataclasses import dataclass

from buildings.objects.building import Building
from buildings.services.building_game_config import BuildingGameConfig
from resources.objects.resource import ResourceCollection

@dataclass
class TechnologyBuilding(Building):
    building_level: int
    production_start_time: int

    def toJson(self):
        return json.dumps({
            'id': self.id,
            'building_level': self.building_level,
            'production_start_time': self.production_start_time
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
            cost=ResourceCollection().setResources(**level_data['cost']),
            production_time=level_data['production_time'],
            building_level=level,
            production_start_time=building_data['production_start_time']
        )
    
    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'cost': json.loads(str(self.cost)),
            'building_level': self.building_level,
            'production_start_time': self.production_start_time
        })
    
class JSONEncodedTechnologyBuilding(TypeDecorator):
    impl = Text

    def process_bind_param(self, value: TechnologyBuilding, dialect):
        return value.toJson()

    def process_result_value(self, value, dialect):
        return TechnologyBuilding.fromJson(value)