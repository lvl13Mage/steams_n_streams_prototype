import json
from pprint import pprint

from buildings.services.building_game_config import BuildingGameConfig
from buildings.objects.resource_building import ResourceBuilding
from buildings.objects.production_building import ProductionBuilding
from buildings.objects.technology_building import TechnologyBuilding
from buildings.objects.building_list import BuildingList
from resources.objects.resource import ResourceCollection

class BuildingHelper:

    def get_initial_buildings(building_type):
        building_config = BuildingGameConfig()
        buildings = None
        match building_type:
            case 'resource_building':
                buildings = BuildingList()
                buildings._type = ResourceBuilding
                for building_id, building_data in building_config.list_buildings(building_type).items():
                    buildings.add(BuildingHelper.get_resource_building(building_id, 0, building_data))
            case 'production_building':
                buildings = BuildingList()
                buildings._type = ProductionBuilding
                for building_id, building_data in building_config.list_buildings(building_type).items():
                    buildings.add(BuildingHelper.get_production_building(building_id, 0, building_data))
            case 'technology_building':
                buildings = BuildingList()
                buildings._type = TechnologyBuilding
                for building_id, building_data in building_config.list_buildings(building_type).items():
                    buildings.add(BuildingHelper.get_technology_building(building_id, 0, building_data))
        return buildings
    
    def get_resource_building(building_id, building_level, building_data = None):
        if building_data is None:
            building_data = BuildingGameConfig().get_building('resource_building', building_id)
        level_data = building_data['levels'][str(building_level)]
        return ResourceBuilding(
            id=building_id,
            name=building_data['name'],
            cost=ResourceCollection().setResources(**level_data['cost']),
            production_time=level_data['production_time'],
            resource_production=ResourceCollection().setResources(**level_data['production']),
            building_level=building_level
        )

    def get_production_building(building_id, building_level, building_data = None):
        if building_data is None:
            building_data = BuildingGameConfig().get_building('production_building', building_id)
        level_data = building_data['levels'][str(building_level)]
        return ProductionBuilding(
            id=building_id,
            name=building_data['name'],
            cost=ResourceCollection().setResources(**level_data['cost']),
            production_time=level_data['production_time'],
            building_level=building_level
        )
    
    def get_technology_building(building_id, building_level, building_data = None):
        if building_data is None:
            building_data = BuildingGameConfig().get_building('technology_building', building_id)
        level_data = building_data['levels'][str(building_level)]
        return TechnologyBuilding(
            id=building_id,
            name=building_data['name'],
            cost=ResourceCollection().setResources(**level_data['cost']),
            production_time=level_data['production_time'],
            building_level=building_level
        )