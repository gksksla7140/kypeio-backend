from typing import Dict

from app.models import Game


class GameManager:
    def __init__(self):
        self.games: Dict[str, Game] = {}

    def create_game(self, host_id: str, game_id: str) -> bool:
        if game_id in self.games:
            return False
        self.games[game_id] = Game(host_id, game_id)
        return True

    def get_game(self, game_id: str) -> Game:
        if game_id not in self.games:
            return None
        return self.games[game_id]

    def remove_game(self, game_id: str) -> None:
        if game_id not in self.games:
            return False
        self.games.pop(game_id)
        return True



manager = GameManager()