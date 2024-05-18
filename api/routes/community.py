from fastapi import APIRouter, Response, Query
import json

from database import session
from player.objects.player import Player
from player.objects.community import Community
from game.objects.community_node import CommunityNode

router = APIRouter()

router.prefix = "/community"
router.tags = ["community"]

@router.get("/{name_or_id}")
def get_community(response: Response, name_or_id: str):
    if name_or_id.isdigit():
        community = session.query(Community).filter(Community.id == name_or_id).first()
    else:
        community = session.query(Community).filter(Community.name == name_or_id).first()
    response.headers["Content-Type"] = "application/json"
    response_data = {}
    for player in community.community_players:
        response_data[player.id] = player.name
    return json.dumps(response_data)

@router.post("/create")
def create_community(response: Response, name: str):
    community_name = Query(name)
    community = Community()
    session.add(community)
    session.commit()
    response.headers["Content-Type"] = "application/json"
    return json.dumps(community.id)

@router.post("/select-node")
def select_node(response: Response, community_id: int, community_node_id: int):
    community = session.query(Community).where(Community.id == community_id).first()
    community_node = session.query(CommunityNode).where(CommunityNode.id == community_node_id).first()
    community_node.setCommunity(community.id)
    session.add(community_node)
    session.commit()
    response.headers["Content-Type"] = "application/json"
    return json.dumps(community_node.id)