from fastapi import APIRouter, Response, Query, Depends
from sqlalchemy.orm import Session
import json

from player.objects.player import Player
from player.objects.community import Community
from game.objects.community_node import CommunityNode
from api.database import get_db

router = APIRouter()

router.prefix = "/community"
router.tags = ["community"]

@router.get("/{name_or_id}")
def get_community(response: Response, name_or_id: str, db: Session = Depends(get_db)):
    if name_or_id.isdigit():
        community = db.query(Community).filter(Community.id == name_or_id).first()
    else:
        community = db.query(Community).filter(Community.name == name_or_id).first()
    response.headers["Content-Type"] = "application/json"
    response_data = {}
    for player in community.community_players:
        response_data[player.id] = player.name
    return json.dumps(response_data)

@router.post("/create")
def create_community(response: Response, name: str, db: Session = Depends(get_db)):
    community_name = Query(name)
    community = Community()
    db.add(community)
    db.commit()
    response.headers["Content-Type"] = "application/json"
    return json.dumps(community.id)

@router.post("/select-node")
def select_node(response: Response, community_id: int, community_node_id: int, db: Session = Depends(get_db)):
    community = db.query(Community).where(Community.id == community_id).first()
    community_node = db.query(CommunityNode).where(CommunityNode.id == community_node_id).first()
    community_node.setCommunity(community.id)
    db.add(community_node)
    db.commit()
    response.headers["Content-Type"] = "application/json"
    return json.dumps(community_node.id)