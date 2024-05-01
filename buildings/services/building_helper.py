import json

from buildings.services.building_game_config import BuildingGameConfig
from buildings.objects.resource_building import ResourceBuilding
from buildings.objects.production_building import ProductionBuilding
from buildings.objects.technology_building import TechnologyBuilding

class BuildingHelper:

    def get_initial_buildings(building_type):
        print('BuildingHelper.get_initial_buildings')
        print(building_type)
        buildings = []
        if building_type == 'resource_building':
            for building_id, building_data in BuildingGameConfig().list_buildings(building_type).items():
                print(building_data['name'])
                buildings.append(ResourceBuilding(
                    id=building_id,
                    name=building_data['name'],
                    cost=building_data['levels']['0']['cost'],
                    production_time=building_data['levels']['0']['production_time'],
                    resource_production=building_data['levels']['0']['production'],
                    building_level=0
                ))
        elif building_type == 'production_building':
            for building_id, building_data in BuildingGameConfig().list_buildings(building_type).items():
                buildings.append(ProductionBuilding(
                    id=building_id,
                    name=building_data['name'],
                    cost=building_data['levels']['0']['cost'],
                    production_time=building_data['levels']['0']['production_time'],
                    building_level=0
                ))
        elif building_type == 'technology_building':
            for building_id, building_data in BuildingGameConfig().list_buildings(building_type).items():
                buildings.append(TechnologyBuilding(
                    id=building_id,
                    name=building_data['name'],
                    cost=building_data['levels']['0']['cost'],
                    production_time=building_data['levels']['0']['production_time'],
                    building_level=0
                ))
        return buildings