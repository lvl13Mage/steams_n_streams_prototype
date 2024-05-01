from dataclasses import dataclass
from player.objects.player import Player
from player.objects.community import Community

@dataclass
class GameSession:
    player = Player
    community = Community
