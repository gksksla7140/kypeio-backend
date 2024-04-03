import random
import string

def generate_game_id(length=6):
    """
    Generate a random game ID.

    Args:
        length (int): The length of the game ID. Default is 6.

    Returns:
        str: The random game ID.
    """
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
