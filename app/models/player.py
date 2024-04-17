from fastapi import WebSocket
from typing import Optional
from enum import Enum


class PlayerStatus(Enum):
    CONNECTED: str = "CONNECTED"
    DISCONNECTED: str = "DISCONNECTED"
    JOINED: str = "JOINED"


class Player:
    def __init__(self, player_id: str):
        self.player_id: str = player_id
        self.status: str = PlayerStatus.JOINED
        self.websocket: Optional[WebSocket] = None

    def add_websocket(self, websocket: WebSocket):
        self.websocket = websocket
        self.status = PlayerStatus.CONNECTED
    
    def remove_websocket(self):
        self.websocket = None
        self.status = PlayerStatus.DISCONNECTED

