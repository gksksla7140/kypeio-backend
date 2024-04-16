from pydantic import BaseModel, Field

class CreateRequest(BaseModel):
    host_id: str = Field(..., min_length=1)

class JoinRequest(BaseModel):
    game_id: str
    player_id: str = Field(..., min_length=1)

class GameDetail(BaseModel):
    game_id: str
    host_id: str
    players: list

class BaseResponse(BaseModel):
    message: str
    game_detail: GameDetail