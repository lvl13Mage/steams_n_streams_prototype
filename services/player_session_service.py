import time

from sqlalchemy.orm import Session
from player.objects.player import Player
from player.objects.community import Community


class PlayerSessionService:
    @staticmethod
    def get_player(db: Session, player_id_or_name):
        if isinstance(player_id_or_name, int):
            player = db.query(Player).where(Player.id == player_id_or_name).first()
        else:
            player = db.query(Player).where(Player.name == player_id_or_name).first()
        return player
    @staticmethod
    def create_player(db: Session, community_id, name):
        community = db.query(Community).where(Community.id == community_id).first()
        player = Player.create_new_player(community, name)
        print("create new player player object resource buildings", player.resource_buildings)
        db.add(player)
        db.commit()
        return player

    @staticmethod
    def update_resources(db: Session, player_id):
        player = PlayerSessionService.get_player(db, player_id)
        current_time = int(time.time())
        last_updated = player.last_updated

        for resource_building in player.resource_buildings:
            production_start_time = resource_building.production_start_time
            production_time_left = 0
            if not production_start_time <= last_updated:
                production_time_left = production_start_time - last_updated
            time_diff = current_time - last_updated - production_time_left
            if time_diff > 0:
                resource_production = resource_building.get_production(time_diff)
                player.resources += resource_production
        player.last_updated = current_time
        db.commit()
