from fastapi import WebSocket
from typing import Optional

class Player:
    def __init__(self, player_id: str, websocket: WebSocket):
        self.player_id: str = player_id
        self.websocket: Optional[WebSocket] = websocket


