from fastapi import HTTPException, status

class GameNotFoundError(HTTPException):
    def __init__(self, game_id: str):
        detail = f"Game with ID {game_id} not found"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class PlayerIdAlreadyExistsError(HTTPException):
    def __init__(self, player_id: str, game_id: str):
        detail = f"Player with ID {player_id} already exists in the game room: {game_id}"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class PlayerIdNotExistsError(HTTPException):
    def __init__(self, player_id: str, game_id: str):
        detail = f"Player with ID {player_id} not in the in the game room: {game_id}"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
