from fastapi import APIRouter, Response, Depends
from sqlalchemy.orm import Session
import json

from player.objects.player import Player
from player.objects.community import Community
from game.objects.community_node import CommunityNode
from api.database import get_db

router = APIRouter()

@router.get("/debug/player/{name_or_id}")
def get_player(response: Response, name_or_id: str, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.name == name_or_id).first()
    response.headers["Content-Type"] = "application/json"
    print(player.resources.coal.quantity)
    print("coal building level", player.resource_buildings[0].building_level)
    print(player.technology_buildings)
    print(player.production_buildings)
    print(player.resource_buildings)
    return "{ 'name': 'test'}"

@router.get("/debug/community/{name_or_id}")
def get_community(response: Response, name_or_id: str, db: Session = Depends(get_db)):
    community = db.query(Community).filter(Community.id == name_or_id).first()
    print(community in db.dirty)
    response.headers["Content-Type"] = "application/json"
    response_data = {}
    for player in community.community_players:
        response_data[player.id] = player.name
    return json.dumps(response_data)