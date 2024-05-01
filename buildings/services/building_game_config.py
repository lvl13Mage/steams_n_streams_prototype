import json

class BuildingGameConfig:
    config: str
    
    def __init__(self):
        self.config = json.loads(open('config/buildings.json').read())

    def get_building(self, building_type, building_id):
        return self.config['buildings'][building_type][building_id]
    
    def list_buildings(self, building_type):
        return self.config['buildings'][building_type]
    
    def get_config(self):
        return self.config