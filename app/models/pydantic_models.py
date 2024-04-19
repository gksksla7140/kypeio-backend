from pydantic import BaseModel, Field
from typing import List


class CreateRequest(BaseModel):
    host_id: str = Field(..., min_length=1)


class JoinRequest(BaseModel):
    game_id: str
    player_id: str = Field(..., min_length=1)


class PlayerInfo(BaseModel):
    player_id: str
    status: str


class GameDetail(BaseModel):
    game_id: str
    host_id: str
    players: List[PlayerInfo]


class BaseResponse(BaseModel):
    message: str
    game_detail: GameDetail
