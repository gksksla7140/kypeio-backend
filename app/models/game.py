from .player import Player
from typing import Dict
from app.errors import PlayerIdAlreadyExistsError, PlayerIdNotExistsError


class Game:
    def __init__(self, host_id: str, game_id: str):
        self.host_id = host_id
        self.game_id = game_id
        self.players: Dict[str, Player] = {host_id: Player(host_id)}
        self.players_progress: Dict[str, str] = {}

    async def add_player(self, player: Player):
        if player.player_id in self.players:
            raise PlayerIdAlreadyExistsError(player.player_id, self.game_id)
        self.players[player.player_id] = player
        self.players_progress[player.player_id] = ""

        await self.broadcast_progress()
        await self.broadcast_text(f"Player {player.player_id} joined the game")

    async def remove_player(self, player_id: str):
        if player_id not in self.players:
            raise PlayerIdNotExistsError(player_id, self.game_id)
        self.players.pop(player_id)
        self.players_progress.pop(player_id)

        await self.broadcast_progress()
        await self.broadcast_text(f"Player {player_id} has left the game")

    async def add_websocket_to_player(self, player_id: str, websocket):
        if player_id not in self.players:
            raise PlayerIdNotExistsError(player_id, self.game_id)
        self.players[player_id].websocket = websocket
        self.broadcast_text(f"Player {player_id} is ready!")

    async def type_character(self, player_id: str, character: str):
        if player_id not in self.players:
            raise PlayerIdNotExistsError(player_id, self.game_id)

        self.players_progress[player_id] = (
            self.players_progress.get(player_id, "") + character
        )
        await self.broadcast_progress()

    async def broadcast_progress(self):
        for player in self.players.values():
            if player.websocket:
                await player.websocket.send_json(self.players_progress)

    async def broadcast_text(self, message: str):
        for player in self.players.values():
            if player.websocket:
                await player.websocket.send_text(message)
