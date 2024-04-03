from pydantic import BaseModel

class CreateRequest(BaseModel):
    host_id: str

class JoinRequest(BaseModel):
    game_id: str
    player_id: str
