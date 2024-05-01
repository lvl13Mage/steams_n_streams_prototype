from dataclasses import dataclass
from resources.objects.resource import ResourceCollection

@dataclass
class Building:
    id: int
    name: str
    cost: ResourceCollection
    production_time: int