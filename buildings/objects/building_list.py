from dataclasses import dataclass, field
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy import TypeDecorator, Text
import json
from typing import List, Union

from buildings.objects.production_building import ProductionBuilding
from buildings.objects.resource_building import ResourceBuilding
from buildings.objects.technology_building import TechnologyBuilding

@dataclass
class BuildingList(Mutable):
    _items: List[Union[ResourceBuilding, ProductionBuilding, TechnologyBuilding]] = field(default_factory=list)
    _type = Union[None, type]
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
        self.changed() # Notify SQLAlchemy that the list has been modified
        

    def remove(self, item):
        self._items.remove(item)
        self.changed() # Notify SQLAlchemy that the list has been modified

    def update(self, index, item):
        if not isinstance(item, self._allowed_types):
            raise TypeError("Item must be an instance of ResourceBuilding, ProductionBuilding, or TechnologyBuilding")
        
        if type(item) != self._type:
            raise TypeError(f"Item must be of type {self._type.__name__}")
        
        self._items[index] = item
        self.changed() # Notify SQLAlchemy that the list has been modified
        print("update", self._items)

    def to_json(self):
        type_name = None
        items = []
        if self._items:
            print("to_json_list", self._items)
            type_name = self._type.__name__
            items = [{'id': b.id, 'building_level': b.building_level, 'production_start_time': b.production_start_time} for b in self._items]
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
    
    def __setitem__(self, index, value):
        self.update(index, value)

    def __len__(self):
        return len(self._items)
    
    def __repr__(self):
        return json.dumps({
            'type': self._type.__name__ if self._type else None,
            'buildings': [json.loads(str(b)) for b in self._items]
        })
    
    @classmethod
    def coerce(cls, key, value):
        """Convert plain dict to BuildingList."""
        if not isinstance(value, cls):
            if isinstance(value, dict):
                return cls.from_json(json.dumps(value))
            return super().coerce(key, value)
        return value
    
class JSONBuildingListType(TypeDecorator):
    impl = Text

    def process_bind_param(self, value: BuildingList, dialect):
        return value.to_json()

    def process_result_value(self, value, dialect):
        return BuildingList.from_json(value) if value else None