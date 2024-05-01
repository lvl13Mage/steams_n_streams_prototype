import database as db

from player.objects.player import Player
from player.objects.community import Community
from game.objects.community_node import CommunityNode

def create_new_player(player_name, player_password):
    session = db.setup_database()

    new_community_node = CommunityNode.create_new_community_node()
    session.add(new_community_node)
    session.commit()
    
    new_community = Community.create_new_community(new_community_node.id)
    session.add(new_community)
    session.commit()

    new_player = Player.create_new_player(new_community.id, player_name)
    session.add(new_player)
    session.commit()

if __name__ == "__main__":
    # Create a new player
    player_name = 'TestPlayer'
    player_password = 'TestPassword'
    create_new_player(player_name, player_password)
