from fastapi import APIRouter, Response, Depends, Query
from sqlalchemy.orm import Session
import json
import time

from player.objects.player import Player
from player.objects.community import Community
from game.objects.community_node import CommunityNode
from resources.objects.resource import ResourceCollection
from buildings.services.building_helper import BuildingHelper
from buildings.objects.building import Building
from buildings.objects.resource_building import ResourceBuilding
from buildings.objects.production_building import ProductionBuilding
from buildings.objects.technology_building import TechnologyBuilding
from api.database import get_db
from typing import Union



from services.player_session_service import PlayerSessionService

router = APIRouter()

router.prefix = "/player"
router.tags = ["player"]

@router.get("/{name_or_id}")
def get_player(response: Response, name_or_id: str, db: Session = Depends(get_db)):
    player = PlayerSessionService.get_player(db, name_or_id)
    print("player resources before update", player.resources)
    PlayerSessionService.update_resources(db, player.id)
    print("player resources after update", player.resources)
    response.headers["Content-Type"] = "application/json"
    print("player repr", json.loads(str(player.resource_buildings)))
    return {
        'id': player.id,
        'name': player.name,
        'community_id': player.community_id,
        'resources': json.loads(str(player.resources)),
        'resource_buildings': json.loads(str(player.resource_buildings)),
        'production_buildings': json.loads(str(player.production_buildings)),
        'technology_buildings': json.loads(str(player.technology_buildings))
    }

@router.post("/create")
def create_player(response: Response, name: str, community_id: int, db: Session = Depends(get_db)):
    player = PlayerSessionService.create_player(db, community_id, name)
    print("player resource buildings", player.resource_buildings)
    PlayerSessionService.update_resources(db, player.id)
    response.headers["Content-Type"] = "application/json"
    return json.dumps(player.id)

@router.post("/building/list")
def get_building_list(response: Response, player_id: int, building_type: str = Query(default=None, pattern=r"resource_building|production_building|technology_building"), db: Session = Depends(get_db)):
    player = PlayerSessionService.get_player(db, player_id)
    PlayerSessionService.update_resources(db, player.id)

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
def construct_building(response: Response, player_id: int, building_type: str, building_id: int, db: Session = Depends(get_db)):
    player = PlayerSessionService.get_player(db, player_id)
    PlayerSessionService.update_resources(db, player.id)
    
    # Get the building list based on the building type
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
    # Get the building to be upgraded
    current_building: Union[ResourceBuilding, ProductionBuilding, TechnologyBuilding] = buildings[building_id-1]

    # Check if the building is already in construction
    if current_building.production_start_time >= player.last_updated:
        return "Building is already in construction"
    # Check if the player has enough resources
    print("resources before check", player.resources)
    print("building cost", player.resource_buildings[building_id-1].cost)
    if player.resources < player.resource_buildings[building_id-1].cost:
        return "Not enough resources"
    print("resources after check", player.resources)
    
    # Upgrade the building
    building_level = int(current_building.building_level)
    current_building.building_level = building_level + 1
    current_building.production_start_time = int(time.time())
    player.resources -= player.resource_buildings[building_id-1].cost
    player.last_updated = int(time.time())

    # Replace the updated building in the list
    buildings[building_id - 1] = current_building
    # Save the updated player object
    db.add(player)
    db.commit()
    print(player in db.dirty)
    response.headers["Content-Type"] = "application/json"
    return json.dumps({building.id: building.building_level for building in buildings})