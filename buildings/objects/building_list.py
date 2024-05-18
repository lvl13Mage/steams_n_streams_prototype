from dataclasses import dataclass
from sqlalchemy import TypeDecorator, Text
import json

from buildings.objects.production_building import ProductionBuilding
from buildings.objects.resource_building import ResourceBuilding
from buildings.objects.technology_building import TechnologyBuilding

@dataclass
class BuildingList:
    _items = None
    _type = None
    _allowed_types = (ResourceBuilding, ProductionBuilding, TechnologyBuilding)

    def add(self, item):
        if not isinstance(item, self._allowed_types):
            raise TypeError("Item must be an instance of ResourceBuilding, ProductionBuilding, or TechnologyBuilding")
        
        if not self._items:
            self._type = type(item)  # Set the type with the first item
            self._items = []
        elif type(item) != self._type:
            raise TypeError(f"All items must be of type {self._type.__name__}")
        
        self._items.append(item)

    def remove(self, item):
        self._items.remove(item)

    def to_json(self):
        type_name = None
        items = []
        if self._items:
            type_name = self._type.__name__
            items = [{'id': b.id, 'building_level': b.building_level} for b in self._items]
        return json.dumps({
            'type': type_name,
            'buildings': items
        })
    
    @staticmethod
    def from_json(json_data):
        data = json.loads(json_data)
        building_list = BuildingList()
        if not data['type']:
            return building_list
        building_list._type = globals()[data['type']]
        for building_data in data['buildings']:
            building = building_list._type.fromJson(json.dumps(building_data))
            building_list.add(building)
        return building_list

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return str(self._items)
    
class JSONBuildingListType(TypeDecorator):
    impl = Text

    def process_bind_param(self, value: BuildingList, dialect):
        return value.to_json()

    def process_result_value(self, value, dialect):
        return BuildingList.from_json(value) if value else None