from fastapi import APIRouter, Response, Query
import json

from database import session
from player.objects.player import Player
from player.objects.community import Community
from game.objects.community_node import CommunityNode

router = APIRouter()

router.prefix = "/player"
router.tags = ["player"]

@router.get("/{name_or_id}")
def get_player(response: Response, name_or_id: str):
    player = session.query(Player).filter(Player.name == name_or_id).first()
    response.headers["Content-Type"] = "application/json"
    print(player.resources.coal.quantity)
    print("coal building level", player.resource_buildings[0].building_level)
    return "{ 'name': 'test'}"

@router.post("/create")
def create_player(response: Response, name: str, community_id: int):
    community = session.query(Community).where(Community.id == community_id).first()
    player = Player.create_new_player(community, name)
    session.add(player)
    session.commit()
    response.headers["Content-Type"] = "application/json"
    return json.dumps(player.id)

@router.post("/building/list")
def get_building_list(response: Response, player_id: int, building_type: str = Query(default=None, pattern=r"resource_building|production_building|technology_building")):
    player = session.query(Player).filter(Player.id == player_id).first()
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