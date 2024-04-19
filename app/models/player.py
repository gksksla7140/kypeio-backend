from fastapi import WebSocket
from typing import Optional
from enum import Enum


class PlayerStatus(Enum):
    JOINED: str = "JOINED"
    CONNECTED: str = "CONNECTED"
    DISCONNECTED: str = "DISCONNECTED"


class Player:
    def __init__(self, player_id: str):
        self.player_id: str = player_id
        self.status: str = PlayerStatus.JOINED
    
    def connected(self):
        self.status = PlayerStatus.CONNECTED

    def disconnected(self):
        self.status = PlayerStatus.DISCONNECTED

    def is_connected(self):
        return self.status == PlayerStatus.CONNECTED
