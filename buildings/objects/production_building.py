import json
from sqlalchemy import TypeDecorator, Text
from dataclasses import dataclass

from buildings.objects.building import Building
from buildings.services.building_game_config import BuildingGameConfig
from resources.objects.resource import ResourceCollection

@dataclass
class ProductionBuilding(Building):
    building_level: int
    
    def toJson(self):
        return json.dumps({
            'id': self.id,
            'building_level': self.building_level
        })
    
    def fromJson(resource_json):
        building_data = json.loads(resource_json)
        buildingGameConfig = BuildingGameConfig()
        building = buildingGameConfig.get_building('production_building', building_data['id'])
        id = building_data['id']
        level = building_data['building_level']
        level_data = building["levels"][str(level)]
        return ProductionBuilding(
            id=id,
            name=building['name'],
            cost=ResourceCollection.fromJson(level_data['cost']),
            production_time=level_data['production_time'],
            building_level=level
        )
    
class JSONEncodedProductionBuilding(TypeDecorator):
    impl = Text

    def process_bind_param(self, value: ProductionBuilding, dialect):
        return value.toJson()

    def process_result_value(self, value, dialect):
        return ProductionBuilding.fromJson(value)

class JSONEncodedProductionBuildingList(TypeDecorator):
    impl = Text

    def process_bind_param(self, value: list[ProductionBuilding], dialect):
        if value is not None:
            return JSONEncodedProductionBuildingList.valueToJsonList(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return JSONEncodedProductionBuildingList.valueFromJsonList(value)
        return value
    
    @staticmethod
    def valueToJsonList(value: list[ProductionBuilding]):
        return json.dumps([building.toJson() for building in value])
    
    @staticmethod
    def valueFromJsonList(value: str):
        buildings_data = json.loads(value)
        return [ProductionBuilding.fromJson(building) for building in buildings_data]