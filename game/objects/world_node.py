from dataclasses import dataclass
from game.objects.node import Node
from buildings.objects.resource_building import ResourceBuilding
from buildings.objects.production_building import ProductionBuilding
from buildings.objects.technology_building import TechnologyBuilding


@dataclass
class WorldNode(Node):

    player = None
    resource_buildings: list[ResourceBuilding]
    production_buildings: list[ProductionBuilding]
    technology_buildings: list[TechnologyBuilding]

    def set_player(self, player):
        self.player = player

    