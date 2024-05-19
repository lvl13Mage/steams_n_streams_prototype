from fastapi import APIRouter, Response, Query
import json
import time

from database import session
from player.objects.player import Player
from player.objects.community import Community
from game.objects.community_node import CommunityNode
from resources.objects.resource import ResourceCollection
from buildings.services.building_helper import BuildingHelper
from buildings.objects.building import Building
from buildings.objects.resource_building import ResourceBuilding
from buildings.objects.production_building import ProductionBuilding
from buildings.objects.technology_building import TechnologyBuilding
from typing import Union

from services.player_session_service import PlayerSessionService

router = APIRouter()

router.prefix = "/player"
router.tags = ["player"]

@router.get("/{name_or_id}")
def get_player(response: Response, name_or_id: str):
    player = PlayerSessionService.get_player(name_or_id)
    PlayerSessionService.update_resources(player.id)
    response.headers["Content-Type"] = "application/json"
    print(player.resources.coal.quantity)
    print("coal building level", player.resource_buildings[0].building_level)
    return "{ 'name': 'test'}"

@router.post("/create")
def create_player(response: Response, name: str, community_id: int):
    player = PlayerSessionService.create_player(community_id, name)
    PlayerSessionService.update_resources(player.id)
    response.headers["Content-Type"] = "application/json"
    return json.dumps(player.id)

@router.post("/building/list")
def get_building_list(response: Response, player_id: int, building_type: str = Query(default=None, pattern=r"resource_building|production_building|technology_building")):
    player = PlayerSessionService.get_player(player_id)
    PlayerSessionService.update_resources(player.id)

    if building_type:
        match building_type:
            case "resource_building":
                response.headers["Content-Type"] = "application/json"
                return player.resource_buildings.to_json()
            case "production_building":
                response.headers["Content-Type"] = "application/json"
                return player.production_buildings.to_json()
            case "technology_building":
                response.headers["Content-Type"] = "application/json"
                return player.technology_buildings.to_json()
    response.headers["Content-Type"] = "application/json"
    return {
        'resource_buildings': json.loads(player.resource_buildings.to_json()),
        'production_buildings': json.loads(player.production_buildings.to_json()),
        'technology_buildings': json.loads(player.technology_buildings.to_json())
    }

@router.post("/building/upgrade")
def construct_building(response: Response, player_id: int, building_type: str, building_id: int):
    player = PlayerSessionService.get_player(player_id)
    PlayerSessionService.update_resources(player.id)
    buildings = None
    match building_type:
        case "resource_building":
            buildings = player.resource_buildings
        case "production_building":
            buildings = player.production_buildings
        case "technology_building":
            buildings = player.technology_buildings
    if not buildings:
        return "Building not found"
    current_building: Union[ResourceBuilding, ProductionBuilding, TechnologyBuilding] = buildings[building_id-1]
    if current_building.production_start_time >= player.last_updated:
        return "Building is already in construction"
    print("building level before upgrade", current_building.building_level)
    building_level = int(current_building.building_level)
    current_building.building_level = building_level + 1
    print("building level after upgrade", current_building.building_level)
    current_building.production_start_time = int(time.time())
    print("production starting time", current_building.production_start_time)
    print("resources before cost", player.resources)
    print("cost", player.resource_buildings[building_id-1].cost)
    player.resources -= player.resource_buildings[building_id-1].cost
    print("resources after cost", player.resources)
    player.last_updated = int(time.time())
    print("player resource building", player.resource_buildings[building_id-1])
    # Replace the updated building in the list
    buildings[building_id - 1] = current_building

    print(player in session.dirty)
    session.add(player)
    session.query(Player).filter(Player.id == player.id).update({Player.resource_buildings: player.resource_buildings, Player.production_buildings: player.production_buildings, Player.technology_buildings: player.technology_buildings, Player.resources: player.resources, Player.last_updated: player.last_updated})
    print(player in session.dirty)
    print(player.resource_buildings)
    session.commit()
    print(player in session.dirty)
    response.headers["Content-Type"] = "application/json"
    return json.dumps({building.id: building.building_level for building in buildings})