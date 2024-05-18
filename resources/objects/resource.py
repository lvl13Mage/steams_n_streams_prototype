import types
import json
from sqlalchemy import TypeDecorator, Text
from dataclasses import dataclass

@dataclass
class Resource:
    name: str
    quantity = 0

    def add(self, amount):
        self.quantity += amount

    def consume(self, amount):
        if self.quantity >= amount:
            self.quantity -= amount
            return True
        return False

@dataclass
class ResourceCollection:
    coal = Resource('Coal')
    water = Resource('Water')
    copper = Resource('Copper')
    aetherum = Resource('Aetherum')

    def setResources(self, *, coal, water, copper, aetherum):
        if coal is not None: self.coal.quantity = int(coal)
        if water is not None: self.water.quantity = int(water)
        if copper is not None: self.copper.quantity = int(copper)
        if aetherum is not None: self.aetherum.quantity = int(aetherum)
        return self
    
    def toJson(self):
        return json.dumps({
            'coal': self.coal.quantity,
            'water': self.water.quantity,
            'copper': self.copper.quantity,
            'aetherum': self.aetherum.quantity
        })
    
    def fromJson(json_data):
        print(json_data)
        data = json.loads(json_data)
        return ResourceCollection().setResources(**data)

    def __add__(self, other):
        return ResourceCollection().setResources(
            coal = self.coal.quantity + other.coal.quantity,
            water = self.water.quantity + other.water.quantity,
            copper = self.copper.quantity + other.copper.quantity,
            aetherum = self.aetherum.quantity + other.aetherum.quantity)
    
    def __sub__(self, other):
        return ResourceCollection().setResources(
            coal = self.coal.quantity - other.coal.quantity,
            water = self.water.quantity - other.water.quantity,
            copper = self.copper.quantity - other.copper.quantity,
            aetherum = self.aetherum.quantity - other.aetherum.quantity)
    
    def __mul__(self, factor=1):
        assert isinstance(factor, (int, float)), 'Multiplication factor must be an integer or float number'
        return ResourceCollection().setResources(
            coal = int(self.coal.quantity * factor),
            water = int(self.water.quantity * factor),
            copper = int(self.copper.quantity * factor),
            aetherum = int(self.aetherum.quantity * factor))
    
    def __repr__(self) -> str:
        return f"ResourceCollection(coal={self.coal.quantity}, water={self.water.quantity}, copper={self.copper.quantity}, aetherum={self.aetherum.quantity})"
    
class JSONEncodedResourceCollection(TypeDecorator):
    """Stores and retrieves JSON as ResourceCollection."""
    impl = Text

    def process_bind_param(self, value: ResourceCollection, dialect):
        if value is not None:
            # Convert ResourceCollection to JSON string
            return JSONEncodedResourceCollection.valueToJson(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            # Convert JSON string back to ResourceCollection
            return JSONEncodedResourceCollection.valueFromJson(value)
        return value
    
    @staticmethod
    def valueToJson(value: ResourceCollection):
        print(value.coal)
        return value.toJson()
    
    @staticmethod
    def valueFromJson(value):
        print(value)
        return ResourceCollection.fromJson(value)