import database as db
from pprint import pprint

from player.objects.player import Player
from player.objects.community import Community
from game.objects.community_node import CommunityNode

def create_new_player(player_name, player_password):

    new_community_node = CommunityNode.create_new_community_node()
    session.add(new_community_node)
    session.commit()
    
    new_community = Community.create_new_community()
    session.add(new_community)
    session.commit()

    new_community_node.setCommunity(new_community.id)

    new_player = Player.create_new_player(new_community, player_name)
    session.add(new_player)
    session.commit()

if __name__ == "__main__":
    session = db.setup_database()
    # Create a new player
    player_name = 'TestPlayer'
    player_password = 'TestPassword'
    #create_new_player(player_name, player_password)

    # Mark Output
    print('######################')
    print('######################')
    print('######################')

    # Query the player
    player = session.query(Player).filter_by(name=player_name).first()
    print(player.name)

    # Query the community
    community = session.query(Community).filter_by(id=player.community_id).first()
    pprint(community.id)
    pprint(community.community_players)
    pprint(community.community_node)
