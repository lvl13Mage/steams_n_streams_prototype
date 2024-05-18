from fastapi import APIRouter, Response
import json

from database import session
from player.objects.player import Player
from player.objects.community import Community
from game.objects.community_node import CommunityNode

router = APIRouter()

@router.get("/debug/player/{name_or_id}")
def get_player(response: Response, name_or_id: str):
    player = session.query(Player).filter(Player.name == name_or_id).first()
    response.headers["Content-Type"] = "application/json"
    print(player.resources.coal.quantity)
    print("coal building level", player.resource_buildings[0].building_level)
    print(player.technology_buildings)
    print(player.production_buildings)
    print(player.resource_buildings)
    return "{ 'name': 'test'}"