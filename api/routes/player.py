from fastapi import APIRouter, Response
import json

from database import session
from player.objects.player import Player
from player.objects.community import Community
from game.objects.community_node import CommunityNode

router = APIRouter()

@router.get("/player/{name_or_id}")
def get_player(response: Response, name_or_id: str):
    player = session.query(Player).filter(Player.name == name_or_id).first()
    response.headers["Content-Type"] = "application/json"
    print(player.resources.coal.quantity)
    print("coal building level", player.resource_buildings[0].building_level)
    return "{ 'name': 'test'}"

@router.post("/community")
def create_community(response: Response):
    community_node = CommunityNode()
    session.add(community_node)
    session.commit()
    community = Community()
    session.add(community)
    session.commit()
    community_node.setCommunity(community.id)
    session.add(community_node)
    session.commit()
    response.headers["Content-Type"] = "application/json"
    return json.dumps(community.id)

@router.post("/player/{name}")
def create_player(response: Response, name: str):
    community = session.query(Community).where(Community.id == 1).first()
    player = Player.create_new_player(community, name)
    session.add(player)
    session.commit()
    response.headers["Content-Type"] = "application/json"
    return json.dumps(player.id)