from fastapi import WebSocket
from typing import Dict

from app.models import game
from .models import Game, Player


class GameManager:
    def __init__(self):
        self.games: Dict[str, Game] = {}

    def create_game(self, host_id: str, game_id: str) -> str:
        if game_id in self.games:
            raise ValueError("Game ID already exists")
        self.games[game_id] = Game(host_id, game_id)
        return game_id

    def add_player_to_game(self, game_id: str, player: Player):
        if game_id not in self.games:
            raise ValueError("Game does not exist")
        self.games[game_id].add_player(player)

    def remove_player_from_game(self, game_id: str, player_id: str):
        if game_id not in self.games:
            raise ValueError("Game does not exist")
        self.games[game_id].remove_player(player_id)

    def get_player_states_for_game(self, game_id: str) -> Dict[str, str]:
        if game_id in self.games:
            return {player_id: player.progress for player_id, player in self.games[game_id].players.items()}
        return {}

    async def broadcast_to_game(self, game_id: str):
        if game_id not in self.games:
            raise ValueError("Game does not exist")
        await self.games[game_id].broadcast()