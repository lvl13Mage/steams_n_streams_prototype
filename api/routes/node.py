from fastapi import APIRouter, Response, Query, Depends
from sqlalchemy.orm import Session
import json

from player.objects.player import Player
from player.objects.community import Community
from game.objects.community_node import CommunityNode
from game.objects.node import Node
from game.objects.edge import Edge
from api.database import get_db

router = APIRouter()

router.prefix = "/node"
router.tags = ["node"]

@router.put("/migrate-nodes")
def migrate_nodes(response: Response, db: Session = Depends(get_db)):
    # load config/map.json
    with open("config/map.json") as f:
        map = json.load(f)
    # Create a Node object for each point and the index of the point in the list is the id of the Node object.
    for i, point in enumerate(map["points"]):
        node = Node()
        node.id = i+1
        node.pos_x = point[0]
        node.pos_y = point[1]
        db.add(node)
    db.commit()
    # Create an Edge object for each edge in the list.
    for edge in map["edges"]:
        edge_obj = Edge()
        edge_obj.node_id_a = edge[0]+1
        edge_obj.node_id_b = edge[1]+1
        edge_obj.weight = 1
        db.add(edge_obj)
    db.commit()
    # Create a CommunityNode object for each Node object
    for node in db.query(Node).all():
        community_node = CommunityNode()
        community_node.node_id = node.id
        community_node.map_id = 1
        db.add(community_node)
    db.commit()
    response.headers["Content-Type"] = "application/json"
    return json.dumps("migrated nodes")