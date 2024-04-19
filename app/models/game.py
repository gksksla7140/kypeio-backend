from enum import Enum
from .player import Player
from typing import Dict


class Game:
    def __init__(self, host_id: str, game_id: str):
        self.host_id = host_id
        self.game_id = game_id
        self.players: Dict[str, Player] = {}
        self.players_progress: Dict[str, int] = {}

    def add_player(self, player: Player) -> bool:
        if player.player_id in self.players:
            return False
        self.players[player.player_id] = player
        self.players_progress[player.player_id] = 0
        return True

    def get_player(self, player_id: str) -> Player:
        if player_id not in self.players:
            return None
        return self.players[player_id]

    def remove_player(self, player_id: str) -> bool:
        if player_id not in self.players:
            return False
        self.players.pop(player_id)
        self.players_progress.pop(player_id)
        return True

    def is_game_empty(self):
        return len(self.players) == 0

    def update_progress(self, player_id: str, typedCount: int) -> bool:
        if player_id not in self.players:
            return False
        self.players_progress[player_id] = typedCount
        return True
