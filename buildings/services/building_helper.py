import json
from pprint import pprint

from buildings.services.building_game_config import BuildingGameConfig
from buildings.objects.resource_building import ResourceBuilding
from buildings.objects.production_building import ProductionBuilding
from buildings.objects.technology_building import TechnologyBuilding
from resources.objects.resource import ResourceCollection

class BuildingHelper:

    def get_initial_buildings(building_type):
        buildings = []
        if building_type == 'resource_building':
            for building_id, building_data in BuildingGameConfig().list_buildings(building_type).items():
                buildings.append(ResourceBuilding(
                    id=building_id,
                    name=building_data['name'],
                    cost=ResourceCollection().setResources(**building_data['levels']['0']['cost']),
                    production_time=building_data['levels']['0']['production_time'],
                    resource_production=ResourceCollection().setResources(**building_data['levels']['0']['production']),
                    building_level=0
                ))
        elif building_type == 'production_building':
            for building_id, building_data in BuildingGameConfig().list_buildings(building_type).items():
                buildings.append(ProductionBuilding(
                    id=building_id,
                    name=building_data['name'],
                    cost=ResourceCollection().setResources(**building_data['levels']['0']['cost']),
                    production_time=building_data['levels']['0']['production_time'],
                    building_level=0
                ))
        elif building_type == 'technology_building':
            for building_id, building_data in BuildingGameConfig().list_buildings(building_type).items():
                buildings.append(TechnologyBuilding(
                    id=building_id,
                    name=building_data['name'],
                    cost=ResourceCollection().setResources(**building_data['levels']['0']['cost']),
                    production_time=building_data['levels']['0']['production_time'],
                    building_level=0
                ))
        return buildings