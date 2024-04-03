from .player import Player
from typing import Dict


class Game:
    def __init__(self, host_id: str, game_id: str):
        self.host_id = host_id
        self.game_id = game_id
        self.players: Dict[str, Player] = {}
        self.players_progress: Dict[str, str] = {}

    def add_player(self, player: Player):
        if player.player_id in self.players:
            raise ValueError("Player already in game")
        self.players[player.player_id] = player
        self.players_progress[player.player_id] = ""

    def remove_player(self, player_id: str):
        if player_id not in self.players:
            raise ValueError("Player not in game")
        self.players.pop(player_id)
        self.players_progress.pop(player_id)

    def type_character(self, player_id: str, character: str):
        if player_id not in self.players:
            raise ValueError("Player not in game")

        self.players_progress[player_id] = self.players_progress.get(player_id, "") + character
        self.broadcast()

    async def broadcast(self):
        for player in self.players.values():
            if player.websocket:
                await player.websocket.send_json(self.players_progress)
