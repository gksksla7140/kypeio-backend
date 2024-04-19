import random
import string
from .models import Game, Player


def generate_game_id(length=6) -> str:
    """
    Generate a random game ID.

    Args:
        length (int): The length of the game ID. Default is 6.

    Returns:
        str: The random game ID.
    """
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_player_statuses_in_game(game: Game) -> list:
    """
    Get the player statuses in a game.

    Args:
        game (Game): The game object.

    Returns:
        list: The playerid and statuses in the game.
    """
    return [
        {"player_id": player.player_id, "status": player.status}
        for player in game.players.values()
    ]
